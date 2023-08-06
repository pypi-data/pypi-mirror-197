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
Common utility methods used in calibration procedures.
"""
import os
from contextlib import contextmanager
import numpy as np


__all__ = ["update_calibrable_variables"]


@contextmanager
def update_calibrable_vars_env(update_value):
    """Change the context of ``UPDATE_CALIBRABLE_VARS``

    Args:
        update_value(str): new value of the context
    """
    _prev_state = os.environ.get("UPDATE_CALIBRABLE_VARS", None)
    try:
        os.environ["UPDATE_CALIBRABLE_VARS"] = update_value
        yield
    finally:
        # Recover default value
        if _prev_state is not None:
            os.environ["UPDATE_CALIBRABLE_VARS"] = _prev_state
        else:
            os.environ.pop("UPDATE_CALIBRABLE_VARS")


def update_calibrable_variables(model):
    """Helper method to update calibration variables in a model, passing a dummy sample

    Args:
        model (:class:`keras.models.Model`): model to be calibrated
    """
    def _gen_dummy_sample(shape):
        sample = np.random.randint(0, 255, size=(1, *shape))
        return sample.astype(np.float32)

    with update_calibrable_vars_env("1"):
        # Create sample and pass it through the model to calibrate variables
        sample = _gen_dummy_sample(model.input.shape[1:])
        model(sample)
