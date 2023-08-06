#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
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
ReLU > MaxPool inversion helper.
"""

__all__ = ["invert_relu_maxpool"]

from copy import deepcopy

from keras.models import Sequential
from keras.layers import MaxPool2D, ReLU

from .transforms_utils import get_layer_index, update_inbound, get_layers_by_type


def _find_relu_maxpool_pairs(model):
    """ Retrieves ReLU > MaxPool layer pairs that can be inverted.

    Args:
        model (keras.Model): a model

    Returns:
        dict: map between a ReLU and the MaxPool that follows
    """
    map_relu_mp = {}

    # Get all MaxPool2D layers present in the model
    maxpools = get_layers_by_type(model, MaxPool2D)

    # Find MaxPooling2D layers that have only one inbound layer being a ReLU
    for mp in maxpools:
        if (len(mp.inbound_nodes) == 1 and isinstance(mp.inbound_nodes[0].inbound_layers, ReLU)):
            map_relu_mp[mp.inbound_nodes[0].inbound_layers] = mp
    return map_relu_mp


def _invert_relu_mp_pairs(model, map_relu_mp):
    """ Edits the model configuration to invert the ReLU/MaxPool pairs and rebuilds a model.

    Args:
        model (keras.Model): a model
        map_relu_mp (dict): map between a ReLU and the MaxPool that follows

    Returns:
        keras.Model: an updated model
    """
    # get_config documentation mentions that a copy should be made when planning to modify the
    # config
    config = deepcopy(model.get_config())
    layers = deepcopy(config['layers'])
    new_output_name = None

    for relu, mp in map_relu_mp.items():
        # Retrieve layer indexes
        relu_index = get_layer_index(layers, relu.name)
        mp_index = get_layer_index(layers, mp.name)

        if isinstance(model, Sequential):
            # For Sequential model, inverting the indexes is enough
            layers[mp_index], layers[relu_index] = layers[relu_index], layers[mp_index]
        else:
            # For functional models, inbounds must be updated
            original_relu_inbound = layers[relu_index]['inbound_nodes'][0][0][0]

            # Update MaxPool2D by replacing the ReLU inbound with the ReLU previous layer
            update_inbound(layers[mp_index], relu.name, original_relu_inbound)
            # Update ReLU by replacing the original inbound with MaxPool2D
            update_inbound(layers[relu_index], original_relu_inbound, mp.name)

            # Then get the layers after MaxPool2D, ie. outbounds layers
            mp_outbound_names = [outbound.layer.name for outbound in mp.outbound_nodes]
            outbound_ids = [
                get_layer_index(layers, bn_outbound)
                for bn_outbound in mp_outbound_names
            ]

            # If MaxPool2D is the last layer (no outbound), store its name and the associated ReLU
            # name so that the model output can be updated later
            if len(outbound_ids) == 0:
                new_output_name = relu.name
                last_mp = mp.name

            # Finally, update the outbounds by replacing their MaxPool inbound with ReLU
            for id in outbound_ids:
                update_inbound(layers[id], mp.name, relu.name)

    # Set the updated layers in config
    config['layers'] = layers

    # Update the model outputs if needed
    if new_output_name:
        for index, out_layer in enumerate(config['output_layers']):
            if out_layer[0] == last_mp:
                config['output_layers'][index][0] = new_output_name

    # Reconstruct model from the config, using the cloned layers
    return model.from_config(config)


def invert_relu_maxpool(model):
    """ Inverts ReLU and MaxPool2D layers in a model to have MaxPool2D before ReLU.

    This transformation produces a strictly equivalent model.

    Args:
        model (keras.Model): a model

    Returns:
        keras.Model: keras.Model: the original model or the updated model
    """
    # Find ReLU followed by MaxPool2D layer pairs that are candidates for inversion
    map_relu_mp = _find_relu_maxpool_pairs(model)

    # When there are no valid candidates, return the original model
    if not map_relu_mp:
        return model

    # Rebuild a model without ZeroPadding2D by editing the configuration
    updated_model = _invert_relu_mp_pairs(model, map_relu_mp)

    # Restore model weights
    updated_model.set_weights(model.get_weights())
    return updated_model
