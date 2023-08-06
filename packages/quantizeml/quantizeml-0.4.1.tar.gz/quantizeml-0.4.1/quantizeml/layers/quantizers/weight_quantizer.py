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

__all__ = ["WeightQuantizer"]

import tensorflow as tf

from ...tensors import QTensor, QFloat
from ..recorders import QFloatRecorder
from .quantizers import Quantizer


@tf.keras.utils.register_keras_serializable()
class WeightQuantizer(Quantizer):
    """A uniform quantizer that converts a float Tensor to a QFloat representation.

    In order, the WeightQuantizer:

        - evaluates the scales required to align the quantization ranges on powers of two,
        - quantizes the rescaled Tensor and returns a QFloat.

    Args:
        bitwidth (int, optional): the quantization bitwidth, defaults to 4.
        signed (bool, optional): whether the quantizer expects signed values or unsigned.
            Defaults to True.
        axis (str, optional): the quantization range is a scalar ('per-tensor') or a vector
            corresponding to the last axis ('per-axis'). Defaults to 'per-axis'.
    """

    def __init__(self, bitwidth=4, signed=True, axis="per-axis", **kwargs):
        super().__init__(bitwidth, signed, **kwargs)
        self._axis = axis
        if not (isinstance(axis, str) and axis in ["per-tensor", "per-axis"]):
            raise ValueError(f"Only support reduction 'per-tensor' or 'per-axis'. Given {axis}.")
        self.qweights = QFloatRecorder()

    def build(self, input_shape):
        """Build the layer.

        Args:
            input_shape (list): the shape of input tensor.
        """
        # Convert axis to a list of int
        if self._axis == "per-axis" and len(input_shape) > 1:
            axis_list = list(range(len(input_shape) - 1))
            # When input_shape last dimension is 1, move operation from axis -1 to axis -2 by
            # adding 1 to the last element in the list. Practical use case is for Depthwise kernels
            # that will be quantized per-channel.
            if input_shape[-1] == 1 and len(input_shape) > 2:
                axis_list[-1] = axis_list[-1] + 1
            self.axis = axis_list
        else:
            self.axis = None

    def call(self, inputs):
        """Quantize the float inputs

        The quantization is done in two steps:

            1. Compute the quantization ranges,
            2. Quantize the inputs.

        Args:
            inputs (:obj:`tensorflow.Tensor`): the inputs tensor.

        Returns:
            :obj:`QFloat`: the quantized tensor.
        """
        if isinstance(inputs, QTensor):
            raise ValueError(
                f"{type(inputs)} input is not supported. WeightQuantizer only accepts float"
                " inputs.")

        # Compute the quantization ranges from the inputs
        ranges = tf.math.reduce_max(tf.math.abs(inputs), self.axis)
        if self.axis is not None and inputs.shape[-1] == 1 and len(inputs.shape) > 2:
            # Expand the shape of the ranges so that it is broacastable on the inputs
            ranges = tf.expand_dims(ranges, -1)
        # Evaluate the scales to align on the optimal quantization ranges
        scales = QFloat.optimal_scales(ranges, self.value_bits)
        # Clip scales lower bound to avoid quantizing very tiny values. Minimum is defined
        # as 1e-6, enough value to be considered as zero.
        scales = tf.clip_by_value(scales, 1e-6, tf.reduce_max(scales))
        # Since we use the optimal quantization ranges [-int_max -1, int_max], the inner
        # FixedPoint can be quantized with exactly zero fractional bits
        qweights = QFloat.quantize(inputs, self.value_bits, scales, 0.)
        # Record the quantized weights (it does nothing if recording is disabled)
        self.qweights(qweights)
        return qweights

    def get_config(self):
        """Get the config of the layer.

        Returns:
            dict: the config of the layer.
        """
        config = super().get_config()
        config.update({"axis": self._axis})
        return config
