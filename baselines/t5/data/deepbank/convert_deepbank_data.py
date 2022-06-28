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

r"""Converts DeepBank data to T5 Seq2Seq format.

Usage:
  blaze run -c opt \
    third_party/py/uncertainty_baselines/baselines/t5/data/deepbank:convert_deepbank_data
"""
import os
from typing import Generator, Text

from absl import app
from absl import flags
import tensorflow.compat.v1 as tf

data_utils = None
gfile = None

FLAGS = flags.FLAGS

flags.DEFINE_string('input_dir', '/cns/nm-d/home/jereliu/public/deepbank/',
                    'Input directory.')

flags.DEFINE_string('output_dir', '/cns/nm-d/home/jereliu/public/deepbank/t5',
                    'Output directory.')

flags.DEFINE_string(
    'seq_type', 'tok', 'The type of node sequence, should be in '
    '["align", "bfs", "dfs", "graph", "tok"].')

flags.DEFINE_list(
    'splits', ['train', 'train1024', 'dev', 'test'], 'Data splits.')


def _text_line_generator(filename: Text) -> Generator[Text, None, None]:
  with gfile.Open(filename, 'rt') as reader:
    for line in reader:
      # Handles non-ascii characters.
      yield line.strip().encode('utf_8').decode('unicode_escape')
    reader.close()


def _convert_onmt_datata(src_filename: Text, tgt_filename: Text,
                         output_filename: Text):
  """Converts data in OpenNMT format to Seq2Seq format."""
  src_gen_fn = _text_line_generator(src_filename)
  tgt_gen_fn = _text_line_generator(tgt_filename)

  line_counter = 0
  with tf.io.TFRecordWriter(output_filename) as writer:
    for src in src_gen_fn:
      try:
        tgt = next(tgt_gen_fn)
        tf_example = data_utils.Seq2SeqExample(
            input_str=src, output_str=tgt).to_tf_example()
        writer.write(tf_example.SerializeToString())
        line_counter += 1
      except StopIteration:
        tf.logging.info(f'Mismatched src and tgt at line {line_counter}.')
    writer.close()

  print(f'Wrote {line_counter} examples to {output_filename}')


def main(_):
  # Recursively creates the output directory.
  output_file_path = os.path.join(FLAGS.output_dir, FLAGS.seq_type)
  tf.logging.info(f'Creating output directory: {output_file_path}')
  tf.io.gfile.makedirs(output_file_path)

  for split in FLAGS.splits:
    _convert_onmt_datata(
        src_filename=os.path.join(FLAGS.input_dir, f'{split}.src'),
        tgt_filename=os.path.join(FLAGS.input_dir,
                                  f'{split}.tgt.{FLAGS.seq_type}'),
        output_filename=os.path.join(FLAGS.output_dir, FLAGS.seq_type,
                                     f'{split}.tfr-00000-of-00001'))


if __name__ == '__main__':
  app.run(main)
