#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
import tensorflow as tf
import keras

from ..tensors import FixedPoint, floor_through, round_log2, MAX_BUFFER_BITWIDTH, pow2
from .layers import deserialize_quant_object, Calibrable, CalibrableVariable


__all__ = ["softmax2", "QuantizedSoftmax2"]


def softmax2(logits, axis=-1):
    """Computes softmax-like activations, but using base 2 for the exponential.

    Used as approximation of the softmax activation.

    This function performs the equivalent of
    ```python
    logits = tf.floor(logits)
    exp = 2 ** logits
    sum_exp_shift = tf.round(tf.log2(tf.reduce_sum(exp, axis, keepdims=True)))
    softmax = exp / 2 ** sum_exp_shift = 2 ** (logits -  sum_exp_shift)
    ```

    When 2 ** :attr:`sum_exp_shift` is an approximated of sum_exp as a Power-of-Two (PoT)

    Args:
        logits (:obj:`tf.Tensor`): a non-empty `Tensor`.
        axis (int, list, optional): the dimension softmax2 would be performed
            on. The default is -1 which indicates the last dimension.

    Returns:
        :obj:`tf.Tensor` value of softmax2 function with the same type and
            shape as `logits`.

    Raises:
        InvalidArgumentError: if `logits` is empty or `axis` is beyond the last
            dimension of `logits`.

    Note:
        We floor the :attr:`logits` to approximate the results to those expected
        when quantizing the operation.
    """
    logits = floor_through(logits)
    exp = tf.cast(2**logits, dtype=logits.dtype)
    sum_exp = tf.reduce_sum(exp, axis=axis, keepdims=True)
    sum_exp_shift = round_log2(sum_exp)
    return 2 ** (logits - sum_exp_shift)


@tf.keras.utils.register_keras_serializable()
class QuantizedSoftmax2(Calibrable, keras.layers.Layer):
    """A quantized layer to do a quantized function similar to the softmax, but
    using base 2 instead of e. So we replace

        softmax(x_i) = e^x_i / sum(e^x_k)

    With this:

        softmax2(x_i) = 2^x_i / sum(2^x_k)

    As in the case of the softmax function, the summation of the pseudo-softmax
    outputs is always equal to one. Consequently, the values softmax2(x_i) can
    be interpreted as probabilities.

    Implementation is inspired from this paper:

    Cardarilli, G.C., Di Nunzio, L., Fazzolari, R. et al.
    A pseudo-softmax function for hardware-based high speed image classification.
    Sci Rep 11, 15307 (2021). https://doi.org/10.1038/s41598-021-94691-7
    """

    def __init__(self, *args, quant_config={}, **kwargs):
        super().__init__(*args, **kwargs)
        self.quant_config = quant_config
        self.out_quantizer = deserialize_quant_object(
            self.quant_config, "output_quantizer", False)
        self.buffer_bitwidth = self.quant_config.get("buffer_bitwidth", MAX_BUFFER_BITWIDTH) - 1
        self.exp_bitwidth = self.quant_config.get("exp_bitwidth", 8)
        if self.buffer_bitwidth <= 2 * self.exp_bitwidth:
            raise ValueError(f"exp_bitwidth={self.exp_bitwidth} must be less than "
                             f"half of buffer_size={self.buffer_bitwidth}.")
        # Add objects that will store the shift values.
        self.input_shift = CalibrableVariable()

    def call(self, x, training=None):
        # raise an error if the inputs are not FixedPoint or tf.Tensor
        if not isinstance(x, FixedPoint):
            raise TypeError(f"QuantizedSoftmax2 only accepts FixedPoint\
                              inputs. Receives {type(x)} inputs.")

        # To avoid overflowing, some modifications are made to the input.
        # First remove the fractional part of the input (floor(x)). We can do
        # this because the exponential function will return very big numbers,
        # so fractional ones can be ignored in the ratio with the sum.
        x, shift = x.floor()
        # update shift values if calibration is enabled
        self.input_shift(shift)

        # Since x has been floored, we can directly use its values
        x = x.values

        # The pseudo-softmax is defined as:
        #
        # p = 2^x/sum(2^x)
        #
        # but we do this instead:
        #
        # p' = p = 2^y/sum(2^y)
        #
        # where
        #
        # y = x - x0
        #
        # because,
        #
        # p' = 2^y/sum(2^y) = 2^(x - x0)/sum(2^(x - x0)) = (2^x * 2^-x0)/(2^-x0 * sum(2^x))
        #    = 2^x/sum(2^x) = p
        #
        # On the other hand, we choose x0 to be the maximum of x, minus a positive
        # integer constant "exp_bitwidth". So now
        #
        # y = x - (max(x) - exp_bitwidth)
        #
        # This makes sure that y is never higher than exp_bitwidth
        x_max = tf.reduce_max(x, axis=-1, keepdims=True)
        x0 = x_max - self.exp_bitwidth
        y = x - x0

        # To evaluate exp = 2^y, we target a maximum precision of exp_bitwidth.
        # As a consequence, we will neglect all values that are below -exp_bitwidth,
        # considering:
        # - that they don't contribute much to the exponential sum,
        # - that they would be quantized to zero after the division.
        exp_values = tf.where(y >= -self.exp_bitwidth, pow2(y + self.exp_bitwidth), 0)
        # Note that we could do the operation directly on the values, but we store
        # values in a FixedPoint to make sure we don't saturate the underlying buffer
        exp = FixedPoint(exp_values, self.exp_bitwidth, self.buffer_bitwidth)
        # To calculate 2^y, hardware can just:
        # - set exp to zero if y < -exp_bitwidth,
        # - do a left shift applying a fixed offset of self.exp_bitwidth.
        # Example:
        #   exp_bitwidth = 4
        #   y = [-5, 3, -4, -1, 1]
        #   exp = [0, 1 << (4 + 3), 1 << (4 - 4), 1 << (4 - 1), 1 << (4 + 1)]
        #   exp = [0, 128, 1, 8, 32]

        # Calculate the sum of the exponential (saturation may happen here).
        sum_exp = tf.reduce_sum(exp, axis=-1, keepdims=True)

        # Like the float version, instead of dividing by sum_exp, we simply approximate
        # it to the closest integer log2 to perform a shift instead of a division.
        # Please refer to the description of round_log2 for a description of the hardware operation.
        # Note here that we need to substract the frac_bits as the values are scaled up.
        sum_exp_shift = round_log2(sum_exp.values) - sum_exp.frac_bits
        outputs = exp >> sum_exp_shift

        # Since sum_exp > exp, the results are between [0,1].
        # We can therefore rewrite the output as:
        outputs = FixedPoint(outputs.values, self.exp_bitwidth, self.exp_bitwidth + 1)

        # Finally, the output is quantized to allow reducing the bitwidth
        if self.out_quantizer is not None:
            outputs = self.out_quantizer(outputs, training=training)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config
