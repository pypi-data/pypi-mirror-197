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
Transforms utility methods.
"""

from keras.layers import Layer


def get_layers(config, layer_names):
    """Extracts layers from a model configuration.

    Args:
        config (dict): JSON formatted model configuration
        layer_names (list): list of layer names to extract

    Returns:
        list: layers configurations
    """
    return [layer for layer in config['layers'] if layer['config']['name'] in layer_names]


def get_layer_index(layers, layer_name):
    """Retrieves the layer index within the layer list.

    Args:
        layers (list): list of JSON formatted layers configurations
        layer_name (str): layer name to retrieve

    Returns:
        int: the layer index
    """
    for index, ly in enumerate(layers):
        if ly['config']['name'] == layer_name:
            return index
    return -1


def inbound_node_generator(layer):
    """Layer configuration inbound node generator.

    Args:
        layer (dict): JSON formatted layer configuration

    Yields:
        list: inbound node
    """
    for inbound_node in layer['inbound_nodes']:
        if (isinstance(inbound_node, list) and len(inbound_node) > 0 and
                isinstance(inbound_node[0], str)):
            yield [inbound_node]
        else:
            yield inbound_node


def replace_layer_name_for_connection_info(connection_info, match_name, replacement_name):
    """Updates an inbound node name.

    Args:
        connection_info (list): inbound node information
        match_name (str): inbound node name to update
        replacement_name (str): inbound node name to set

    Returns:
        list: the original inbound node if an update happened, None otherwise
    """
    # Note that is from tfmot and the connection_info structure is not really documented:
    # it is a nested list where the first item is the inbound layer name.
    # For example: [[['conv1', 0, 0, {} ]]] or [[['batch_normalization', 0, 0, {}]]]
    original_info = connection_info.copy()
    match_found = False
    if connection_info[0] == match_name:
        match_found = True
        connection_info[0] = replacement_name
    for key in connection_info[3]:
        if isinstance(connection_info[3][key], list):
            if connection_info[3][key][0] == match_name:
                match_found = True
                connection_info[3][key][0] = replacement_name
    return original_info if match_found else None


def get_layers_by_type(model, layer_type):
    """Recursively find layers matching the specified type.

    Args:
        model (:obj:`keras.Model`): the source model.
        layer_type (class): the Layer class to look for.

    Returns:
        list(:obj:`keras.layers.Layer`): a list of layers
    """
    def _get_layers(layer, layers):
        if isinstance(layer, layer_type):
            layers.append(layer)
        for attr in layer.__dict__.values():
            if isinstance(attr, Layer):
                _get_layers(attr, layers)
    layers = []
    for layer in model.layers:
        _get_layers(layer, layers)
    return layers


def update_inbound(layer_config, name, updated_inbound):
    """ Update the layer 'name' inbound in config with the provided name.

    Args:
        layer_config (dict): layer config to udpate
        name (str): name of the inbound to replace
        updated_inbound (str): new inbound name
    """
    for inbound_node in inbound_node_generator(layer_config):
        if isinstance(inbound_node, dict):
            inbound_node = inbound_node.values()
        for connection_info in inbound_node:
            replace_layer_name_for_connection_info(connection_info, name, updated_inbound)
