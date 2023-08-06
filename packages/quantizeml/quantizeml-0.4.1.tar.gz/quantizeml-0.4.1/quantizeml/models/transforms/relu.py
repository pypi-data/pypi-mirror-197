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
"""
ReLU transformation for quantized models.
"""
import numpy as np

from keras.layers import ReLU, Conv2D, SeparableConv2D

from ...models.utils import deep_clone_model

__all__ = ["rescale_relu"]


def rescale_relu(model):
    """Rescale relu activations to a target FixedPoint bitwidth.

    When quantizing the outputs of a ReLU into a FixedPoint with a specified bitwidth,
    the ReLU outputs are clipped to a maximum value that corresponds to the
    FixedPoint representation of its target maximum value.

    For instance, with an output bitwidth of 4:

    - ReLU2 values will be clipped to 1.875,
    - ReLU4 values will be clipped to 3.75,
    - ReLU6 values will be clipped to 7.5,
    - ReLU8 values will be clipped to 7.5.

    This represents a loss in accuracy as compared to the float model.

    When the ReLU is surrounded by layers whose operations have a globally
    linear response to the scale of their inputs, like a Conv2D or a Dense, we
    can compensate for that effect by rescaling the weights of the previous and
    next layers.

    Args:
        model (keras.Model): the Keras model to modify
        bitwidth (int): the target ReLU output bitwidth

    Returns:
        keras.Model: the model with its ReLU clipped to FixedPoint values
    """
    supported_neightbours = [Conv2D, Dense]

    # Create a clone model
    clone_model = deep_clone_model(model)

    # Iterate over layers
    for layer in clone_model.layers:
        # We only look for ReLU layers that are already clipped
        if isinstance(layer, ReLU) and layer.max_value is not None:
            # They must have a single inbound and outbound layers
            if len(layer.inbound_nodes) == 1 and len(outbound_nodes) == 1:
                prev_layer = layer.inbound_nodes[0]
                next_layer = layer.outbound_nodes[0]
                if (isinstance(prev_layer, supported_neighbours) and
                    isinstance(nex_layer, supported_neighbours)):
                    # Evaluate the max_value as a FixedPoint for the target bitwidth
                    max_value = FixedPoint.quantize(layer.max_value, bitwidth)
                    # Evaluate the rescaling ratio so that the quantized and
                    # float max_values are equal
                    rescaling = max_value.to_float() / layer.max_value
                    # The weights of the previous layer must be multiplied by
                    # the rescaling ratio
                    # The weights of the next layer must be divided by
                    # the rescaling ratio
                    # We can now set the max_value to its target value
                    layer.max_value = max_value.to_float()

    return clone_model
