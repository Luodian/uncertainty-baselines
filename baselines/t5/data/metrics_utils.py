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

"""Utility functions for metrics computation."""
import re
from typing import Dict, List, Text

# Argument edge types shared by DeepBank 1.0 and DeepBank 1.1.
MISC = ['-of']

ARG_EDGES = [
    ':ARG', ':ARG1', ':ARG2', ':ARG3', ':ARG4', ':BV', ':carg', ':L-INDEX',
    ':R-INDEX', ':L-HNDL', ':R-HNDL'
]

FUNC_NODES = {
    'v0': [  # 87 function nodes used by DeepBank 1.0.
        'every_q', 'ellipsis', 'interval_p_end', 'unknown', 'place_n',
        'meas_np', 'implicit_conj', 'little-few_a', 'number_q', 'property',
        'loc_nonsp', 'timezone_p', 'relative_mod', 'generic_entity', 'holiday',
        'unspec_adj', 'comp_enough', 'much-many_a', 'dofw', 'reason', 'measure',
        'temp', 'neg', 'dofm', 'ellipsis_ref', 'thing', 'refl_mod', 'excl',
        'id', 'manner', 'free_relative_q', 'addressee', 'fraction', 'v_event',
        'times', 'eventuality', 'comp_less', 'compound', 'num_seq', 'of_p',
        'with_p', 'interval', 'subord', 'idiom_q_i', 'proper_q', 'named_n',
        'cop_id', 'generic_verb', 'superl', 'comp_too', 'ellipsis_expl',
        'comp_equal', 'ord', 'nominalization', 'polite', 'abstr_deg',
        'elliptical_n', 'udef_q', 'recip_pro', 'card', 'yofc', 'discourse',
        'plus', 'numbered_hour', 'interval_p_start', 'year_range', 'pronoun_q',
        'def_implicit_q', 'season', 'appos', 'fw_seq', 'not_x_deg',
        'unspec_manner', 'def_explicit_q', 'parenthetical', 'comp_so', 'time_n',
        'prpstn_to_prop', 'mofy', 'person', 'named', 'comp', 'comp_not+so',
        'pron', 'poss', 'part_of', 'temp_loc_x'
    ],
    'v1': [  # 88 function nodes used by DeepBank 1.0.
        'udef_q', 'compound', 'named', 'proper_q', 'card', 'pronoun_q', 'pron',
        'def_explicit_q', 'poss', 'parg_d', 'focus_d', 'loc_nonsp',
        'nominalization', 'times', 'appos', 'def_implicit_q', 'nn_u_unknown',
        'generic_entity', 'comp', 'neg', 'implicit_conj', 'subord', 'named_n',
        'mofy', 'time_n', 'yofc', 'nns_u_unknown', 'part_of', 'number_q',
        'much-many_a', 'jj_u_unknown', 'ord', 'unknown', 'superl', 'place_n',
        'of_p', 'dofw', 'which_q', 'dofm', 'thing', 'comp_equal', 'measure',
        'fraction', 'plus', 'eventuality', 'with_p', 'idiom_q_i',
        'little-few_a', 'parenthetical', 'person', 'ellipsis_ref',
        'elliptical_n', 'interval', 'interval_p_end', 'interval_p_start',
        'season', 'rb_u_unknown', 'comp_so', 'free_relative_q', 'id',
        'vbn_u_unknown', 'temp_loc_x', 'vb_u_unknown', 'comp_too',
        'unspec_manner', 'manner', 'discourse', 'excl', 'vbg_u_unknown',
        'year_range', 'every_q', 'vbd_u_unknown', 'numbered_hour', 'abstr_deg',
        'temp', 'comp_less', 'reason', 'fw_u_unknown', 'comp_enough', 'holiday',
        'ellipsis', 'vbz_u_unknown', 'fw_seq', 'recip_pro',
        'free_relative_ever_q', 'vbp_u_unknown', 'timezone_p', 'refl_mod'
    ]
}

# Content node postfixes shared by DeepBank 1.0 and DeepBank 1.1.
CONTENT_NODE_POSTFIX_NAMES = [
    'n_1', 'q', 'n_of', 'v_1', 'p', 'a_1', 'c', 'v_to', 'v_modal', 'x_deg',
    'v_id', 'x', 'q_dem', 'v_cause', 'p_temp', 'a_for', 'p_state', 'x_subord',
    'a_of', 'v_for', 'p_per', 'a_to', 'x_then', 'n_temp', 'n_to', 'v_from',
    'n_in', 'v_with', 'v_there', 'v_2', 'v_of', 'v_up', 'p_namely', 'v_as',
    'v_on', 'v_qmodal', 'p_dir', 'v_in', 'a_at-for-of', 'x_h', 'v_at',
    'p_means', 'n_of-on', 'n_of-n', 'n_2', 'v_out', 'n_for', 'v_state', 'v_prd',
    'a_again', 'v_into', 'a_with', 'v_about', 'v_off', 'n_about', 'n_of-to',
    'a_as', 'v_nv', 'n_of-about', 'a_rvrs', 'n_cur', 'v_name', 'v_down', 'a_on',
    'a_about', 'a_from', 'v_from-to', 'n_on-about', 'n_i', 'p_nbar', 'p_time',
    'a_at', 'a_ante', 'a_than-from', 'a_in', 'v_back', 'x_prd', 'a_also',
    'v_over', 'a_thus', 'n_item', 'q_indiv', 'n_of-for', 'v_of-i', 'a_disc',
    'v_by', 'v_to-about', 'n_at', 'v_away', 'c_btwn', 'n_with', 'v_unspec',
    'v_on-upon', 'v_seem-to', 'v_seem-about', 'n_on', 'v_i', 'v_itcleft',
    'p_except', 'v_out-to', 'a_of-about', 'v_so', 'p_ind', 'v_with-for',
    'a_error', 'v_for-as', 'v_to-with', 'v_buy', 'n_of-as', 'p_1',
    'a_with-about-of', 'a_2', 'v_through', 'v_transfer', 'x_cond', 'v_around',
    'n_from', 'v_mental', 'n_meas', 'v_dir', 'v_like', 'v_coll', 'v_cause-on',
    'a', 'v_against', 'a_expl-for', 'a_same-as', 'v_together', 'a_to-for',
    'v_aside', 'v_do', 'v_be', 'a_of-for', 'p_comp', 'v_along', 'x_cause',
    'v_adv', 'a_true', 'v_onto', 'c_from', 'a_with-at', 'v_towards',
    'v_out-aim', 'v_ahead', 'a_at-by-in', 'v_even', 'n_abb', 'v_up-to',
    'v_up-for', 'v_up-of', 'a_at-by-with', 'v_yet', 'n_num', 'n_money',
    'v_cope', 'a_former', 'a_of-to', 'v_ing', 'n_against', 'c_not', 'v_open',
    'v_behind', 'v_x', 'v_after', 'v_forward-to', 'v_seem', 'a_for-as', 'v_loc',
    'v_upon', 'v_home', 'a_accept', 'v_across', 'n_do-be', 'v_away-with',
    'x_preph', 'v_to-i', 'v_sound', 'v_apart', 'v_up2', 'v_cause-to', 'v_yield',
    'v_suffice', 'v_it', 'n_pair', 'v_x-off', 'v_forth', 'v_out-of', 'c_mod',
    'v_without', 'x_1', 'v_out+of', 'v_up-with', 'p_time-on', 'v_up-cause',
    'v_cause-into', 'p_place-in', 'n_at-with', 'n_into', 'v_seem+to'
]

# Special SentencePiece tokens to be used to represent content-node postfixes.
CONTENT_NODE_POSTFIX_TOKENS = [
    'au\u00dfergew\u00f6hnlich', 'ver\u00f6ffentlicht', 'responsabilit\u00e9',
    'ausschlie\u00dflich', 'suppl\u00e9mentaire', 'fonctionnalit\u00e9',
    'repr\u00e9sentation', 'compl\u00e9mentaire', 'pr\u00e9sidentielle',
    'ber\u00fccksichtigt', 'Pers\u00f6nlichkeit', 't\u00e9l\u00e9chargement',
    'r\u00e9glementation', 'd\u00e9veloppement', 'M\u00f6glichkeiten',
    'Unterst\u00fctzung', 'dumneavoastr\u0103', 'r\u00e9guli\u00e8rement',
    'grunds\u00e4tzlich', 'interna\u021bional', 'interna\u0163ional',
    'imm\u00e9diatement', 'gew\u00e4hrleisten', 'B\u00fcrgermeister',
    'reprezentan\u021bi', 'probl\u00e9matique', 'disponibilit\u00e9',
    'gew\u00e4hrleistet', 'haupts\u00e4chlich', 'Einschr\u00e4nkung',
    'Besch\u00e4ftigung', 'collectivit\u00e9s', 'compr\u00e9hension',
    'Grunds\u00e4tzlich', 'Interna\u021bional', 'unterst\u00fctzen',
    'durchgef\u00fchrt', 'anschlie\u00dfend', '\u00e9lectronique',
    'pr\u00e9sentation', 'personnalis\u00e9', 'wundersch\u00f6ne',
    'particuli\u00e8re', 'compl\u00e8tement', 'ausdr\u00fccklich',
    'urspr\u00fcnglich', 'pr\u00e4sentieren', 'biblioth\u00e8que',
    'repr\u00e9sentant', 'Durchf\u00fchrung', 'participan\u021bi',
    'personnalit\u00e9', 'profesional\u0103', '\u00dcberraschung',
    'besch\u00e4ftigen', 't\u00e9l\u00e9phonique', 'g\u00e9ographique',
    '\u00eenregistrare', 'op\u00e9rationnel', 'M\u00f6glichkeit',
    'diff\u00e9rentes', 'possibilit\u00e9', 'd\u00e9partement',
    'unterst\u00fctzt', 'tats\u00e4chlich', 'int\u00e9ressant',
    'Universit\u00e4t', 'r\u00e9alisation', 'comp\u00e9tences',
    'temp\u00e9rature', 'pers\u00f6nliche', 'zus\u00e4tzliche',
    'n\u00e9cessaires', '\u00eenregistrat', 'vollst\u00e4ndig',
    'erm\u00f6glichen', 'cons\u00e9quence', 'pr\u00e4sentiert',
    'Ver\u00e4nderung', 'pr\u00e9paration', 'ind\u00e9pendant',
    'Bed\u00fcrfnisse', 'enti\u00e8rement', 'zuverl\u00e4ssig',
    '\u00eentotdeauna', 'besch\u00e4ftigt', 'sp\u00e9cialiste',
    'Bev\u00f6lkerung', 'd\u00e9placement', 'comp\u00e9tition',
    'd\u00e9claration', 'Aktivit\u00e4ten', '\u00e9nerg\u00e9tique',
    '\u00e9quipements', 'ausf\u00fchrlich', 'r\u00e9servation',
    't\u00e9l\u00e9charger', 'langj\u00e4hrige', 'Verst\u00e4ndnis',
    'autorit\u0103\u021bil', 'strat\u00e9gique', 'F\u00e4higkeiten',
    '\u00fcberraschen', 'autorit\u0103\u0163il', 'k\u00f6rperliche',
    'str\u0103in\u0103tate', 'tradi\u021bional', '\u00dcbersetzung',
    'pr\u00e9cis\u00e9ment', 'p\u00e9dagogique', 'Kreativit\u00e4t',
    'litt\u00e9rature', 'diff\u00e9rents', '\u00e9conomique', 'n\u00e9cessaire',
    'exp\u00e9rience', 'regelm\u00e4\u00dfig', 'reprezint\u0103',
    'zus\u00e4tzlich', '\u00e9lectrique', 'sp\u00e9cialis\u00e9',
    'erm\u00f6glicht', 'sp\u00e9cifique', 'communaut\u00e9', 'informa\u021bii',
    'europ\u00e9enne', 'd\u00e9velopper', 'diff\u00e9rence', 'd\u00e9couverte',
    'activit\u0103\u021bi', 'pers\u00f6nlich', '\u00f6ffentlich',
    'repr\u00e9sente', 'unabh\u00e4ngig', 'b\u00e9n\u00e9ficier',
    'conf\u00e9rence', 'accompagn\u00e9', 'financi\u00e8re', 'erh\u00e4ltlich',
    'activit\u0103\u0163i', 'Oberfl\u00e4che', 'R\u00e9publique',
    'm\u00e9dicament', 'informa\u0163ii', 'ausgew\u00e4hlt', '\u00fcbernehmen',
    'D\u00fcsseldorf', 'd\u00e9coration', 'r\u00e9paration', 'produc\u0103tor',
    'Zus\u00e4tzlich', '\u00fcberzeugen', 'modific\u0103ri', 'vielf\u00e4ltig',
    'gew\u00fcnschte', 'Atmosph\u00e4re', '\u00e9v\u00e9nements',
    '\u00e9videmment', 'r\u00e9volution', 'experien\u021b\u0103',
    'r\u00e9sistance', 'communiqu\u00e9', '\u00fcbertragen', 'Grundst\u00fcck',
    'enregistr\u00e9', 'institu\u021bii', 't\u00e9l\u00e9vision',
    'recommand\u00e9', 'caract\u00e9ris', '\u00e9cologique', 'Einf\u00fchrung',
    'cons\u00e9quent', 'pr\u00e9vention', '\u00fcbernommen', 'r\u00e9solution',
    'r\u00e9novation', 'institu\u0163ii', 'pre\u0219edinte',
    'rom\u00e2neasc\u0103', 'compl\u00e9ment', 'd\u00e9finitive',
    'd\u00e9finition', 'Ausf\u00fchrung', 'kilom\u00e8tres', 't\u00e9moignage',
    'zug\u00e4nglich', 'performan\u021b', 'd\u00e9terminer', 'm\u00e9tallique',
    'coordonn\u00e9e', 'comunit\u0103\u021bi', 'sorgf\u00e4ltig',
    'Angeh\u00f6rige', '\u00eenv\u0103\u021b\u0103m\u00e2nt',
    'pr\u00e9f\u00e9rence', '\u00eenchisoare', '\u00f6kologisch',
    'comp\u00e9tence', '\u00eenv\u0103\u0163\u0103m\u00e2nt'
]

# Makes a mapping between graph element names and their corresponding tokens
# for both DeepBank 1.0 and DeepBank 1.1.
_TOKEN_TO_NAME_MAPS = {}
for version in ('v0', 'v1'):
  token_to_name_map = {}
  # Uses the 100 extra_ids for argument edges and function nodes.
  names = MISC + ARG_EDGES + FUNC_NODES[version]
  tokens = [f'<extra_id_{i}>' for i in range(len(names))]
  token_to_name_map = dict(zip(tokens, names))

  # Uses the special tokens for the content post-fixes.
  names = CONTENT_NODE_POSTFIX_NAMES
  tokens = CONTENT_NODE_POSTFIX_TOKENS
  token_to_name_map.update(dict(zip(tokens, names)))

  _TOKEN_TO_NAME_MAPS[version] = token_to_name_map


def token_transfer(graph_str: Text, data_version: str = 'v0') -> Text:
  """Transfers special tokens to thir original names."""
  token_map = _TOKEN_TO_NAME_MAPS[data_version]

  new_graph_list = []
  pattern = re.compile(r'<extra_id_[0-9]+>')
  for x in graph_str.split():
    retoken = x
    search_result = re.search(pattern, retoken)
    if search_result:
      match_str = search_result.group(0)
      if match_str:
        retoken = token_map[match_str]
    if retoken.endswith('_'):
      postfix = '_'.join(retoken.split('_')[:-2])
      lemma = retoken.split('_')[-2]
      if postfix in token_map:
        retoken = '_' + lemma + '_' + token_map[postfix]
      else:
        retoken = '_' + lemma + '_' + postfix
    if retoken == '-of' and new_graph_list:
      new_graph_list[-1] = new_graph_list[-1] + '-of'
    else:
      new_graph_list.append(retoken)

  graph_str = ' '.join(new_graph_list)

  return graph_str


def graph_to_nodeseq(graph_str: Text,
                     data_version: str = 'v0') -> Dict[Text, List[Text]]:
  """Extracting node sequence from a graph string."""
  nodeseq = []
  cont_nodeseq = []
  func_nodeseq = []
  entity_nodeseq = []
  graph_str_split = graph_str.split()
  for x in graph_str_split:
    if x in ['(', ')', '"']:
      continue
    if x[0] == ':':
      continue
    if x[0] == '*':
      node_name = nodeseq.pop()
      nodeseq.append(node_name + x)
      continue
    nodeseq.append(x)

  for x in nodeseq:
    if x[0] == '_':
      cont_nodeseq.append(x)
    elif x in FUNC_NODES[data_version]:
      func_nodeseq.append(x)
    else:
      entity_nodeseq.append(x)

  return dict(
      all=nodeseq, cont=cont_nodeseq, func=func_nodeseq, entity=entity_nodeseq)


def find_root(graph_str: Text) -> Text:
  """Find the root node of the graph."""
  root = ''
  for x in graph_str.split():
    if root == '' and x[0] not in ['(', ')', '"', '*', ':']:  # pylint:disable=g-explicit-bool-comparison
      root = x
      break
  return root
