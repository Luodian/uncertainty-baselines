# coding=utf-8
# Copyright 2022 The Uncertainty Baselines Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Register parser tasks."""
import functools

import seqio
import t5.data

import metrics as ub_metrics  # local file import from baselines.t5.data
import deepbank as utils  # local file import from baselines.t5.data.tasks

TaskRegistry = seqio.TaskRegistry

# T5 shuffle buffer size.
_DEFAULT_SHUFFLE_BUFFER_SIZE = 10000

_DEFAULT_SMCAL_TRAIN_PATTERNS = []
_DEFAULT_SMCAL_EVAL_PATTERNS = {}
_DEFAULT_MWOZ_TRAIN_PATTERNS = []
_DEFAULT_MWOZ_EVAL_PATTERNS = {}


# In-domain training and evaluation data.
smcalflow_config = utils.dataset_configs(
    train_patterns=_DEFAULT_SMCAL_TRAIN_PATTERNS,
    eval_patterns=_DEFAULT_SMCAL_EVAL_PATTERNS)
multiwoz_config = utils.dataset_configs(
    train_patterns=_DEFAULT_MWOZ_TRAIN_PATTERNS,
    eval_patterns=_DEFAULT_MWOZ_EVAL_PATTERNS)

# Academic parsing tasks for data flow datasets.
# TODO(jereliu): Deprecate in favor of seqio.TaskRegistry.

t5.data.TaskRegistry.add(
    'smcalflow',
    t5.data.Task,
    dataset_fn=functools.partial(
        utils.parsing_dataset, params=smcalflow_config),
    splits={'train': 'train', 'validation': 'validation', 'test': 'validation'},
    text_preprocessor=None,
    metric_fns=[ub_metrics.seq2seq_metrics],
    shuffle_buffer_size=_DEFAULT_SHUFFLE_BUFFER_SIZE)

t5.data.TaskRegistry.add(
    'multiwoz',
    t5.data.Task,
    dataset_fn=functools.partial(utils.parsing_dataset, params=multiwoz_config),
    splits={'train': 'train', 'validation': 'validation', 'test': 'test'},
    text_preprocessor=None,
    metric_fns=[ub_metrics.seq2seq_metrics],
    shuffle_buffer_size=_DEFAULT_SHUFFLE_BUFFER_SIZE)
