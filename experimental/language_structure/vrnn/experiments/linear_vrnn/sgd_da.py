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

r"""Vizier for linear VRNN for SGDDataset.

"""

import sgd_da_tmpl as tmpl  # local file import from experimental.language_structure.vrnn.experiments.linear_vrnn


def get_config():
  """Returns the configuration for this experiment."""
  config = tmpl.get_config()
  return config


def get_sweep(hyper):
  """Returns hyperparameter sweep."""
  domain = [
      hyper.sweep('config.word_weights_file_weight',
                  hyper.discrete([0.25 * i for i in range(5)])),
      hyper.sweep('config.psl_constraint_learning_weight',
                  hyper.discrete([0, 0.01, 0.05, 0.1, 0.5, 1])),
      hyper.sweep('config.bow_loss_weight',
                  hyper.discrete([0.01, 0.1, 0.5, 1, 2, 5])),
      hyper.sweep('config.base_learning_rate', hyper.discrete([5e-4, 1e-3]))
  ]
  sweep = hyper.product(domain)
  return sweep
