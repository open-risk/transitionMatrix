# encoding: utf-8

# (c) 2017-2021 Open Risk (https://www.openriskmanagement.com)
#
# TransitionMatrix is licensed under the Apache 2.0 license a copy of which is included
# in the source distribution of TransitionMatrix. This is notwithstanding any licenses of
# third-party software included in this distribution. You may not use this file except in
# compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.


""" A collection of state space descriptions from recognized public credit rating scales. The list includes the following: Predefined state spaces (include CQS mappings)

    - AM Best Europe-Rating Services Ltd.
    - ARC Ratings S.A.
    - Cerved Rating Agency S.p.A.
    - Creditreform Rating AG
    - DBRS Ratings Limited
    - Fitch Ratings
    - Moody’s Investors Service
    - Scope Ratings AG
    - Standard & Poor’s Ratings Services

  There are also mappings between major rating scales (e.g.SnP_Fitch2Moodys)

  .. warning:: The mappings are nominal (as defined by regulation or convention) and do not necessarily indicate conceptual or statistical alignement!

"""

from transitionMatrix.statespaces.statespace import StateSpace

#
# PREDEFINED STATE SPACES
#

# A generic state space for testing
originator = 'N/A'
full_name = 'Generic state space for testing'
definition = [('0', "AAA"), ('1', "AA"), ('2', "A"), ('3', "BBB"),
              ('4', "BB"), ('5', "B"), ('6', "CCC"),
              ('7', "D")]

Generic_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=None)

# A generic state space for testing - includes NR
originator = 'N/A'
full_name = 'Generic state space for testing - includes NR state'
definition = [('0', "AAA"), ('1', "AA"), ('2', "A"), ('3', "BBB"),
              ('4', "BB"), ('5', "B"), ('6', "CCC"),
              ('7', "D"), ('8', "NR")]

Generic_NR = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=None)

# AM Best Europe-Rating Services Ltd.
originator = 'AM Best Europe-Rating Services Ltd.'
full_name = 'Long-term issuer ratings scale'
definition = [('0', "aaa"), ('1', "aa+"), ('2', "aa"), ('3', "aa-"),
              ('4', "a+"), ('5', "a"), ('6', "a-"),
              ('7', "bbb+"), ('8', "bbb"), ('9', "bbb-"),
              ('10', "bb+"), ('11', "bb"), ('12', "bb-"),
              ('13', "b+"), ('14', "b"), ('15', "b-"),
              ('16', "ccc+"), ('17', "ccc"), ('18', "ccc-"),
              ('19', "cc"), ('20', "c"), ('21', "d"), ('22', "s")]
cqs_mapping = {'0': '1',
               '1': '1',
               '2': '1',
               '3': '1',
               '4': '2',
               '5': '2',
               '6': '2',
               '7': '3',
               '8': '3',
               '9': '3',
               '10': '4',
               '11': '4',
               '12': '4',
               '13': '5',
               '14': '5',
               '15': '5',
               '16': '6',
               '17': '6',
               '18': '6',
               '19': '6',
               '20': '6',
               '21': '6',
               '22': '6'
               }

AM_Best_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=cqs_mapping)

# ARC Ratings S.A.
originator = 'Standard & Poor’s Ratings Services'
full_name = 'Medium and long-term issuer rating scale'
definition = [('0', "AAA"), ('1', "AA"),
              ('2', "A"),
              ('3', "BBB"),
              ('4', "BB"),
              ('5', "B"),
              ('6', "CCC"), ('7', "CC"), ('8', "C"), ('9', "D")]
cqs_mapping = {'0': '1',
               '1': '1',
               '2': '2',
               '3': '3',
               '4': '4',
               '5': '5',
               '6': '6',
               '7': '6',
               '8': '6',
               '9': '6'
               }

ARC_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=cqs_mapping)

# Cerved Rating Agency S.p.A.
originator = 'AM Best Europe-Rating Services Ltd.'
full_name = 'Corporate long-term rating scale'
definition = [('0', "A1.1"), ('1', "A1.2"), ('2', "A1.3"),
              ('3', "A2.1"), ('4', "A2.2"), ('5', "A3.1"),
              ('6', "B1.1"), ('7', "B1.2"),
              ('8', "B2.1"), ('9', "B2.2"),
              ('10', "C1.1"),
              ('11', "C1.2"), ('12', "C2.1")]
cqs_mapping = {'0': '1',
               '1': '1',
               '2': '1',
               '3': '2',
               '4': '2',
               '5': '2',
               '6': '3',
               '7': '3',
               '8': '4',
               '9': '4',
               '10': '5',
               '11': '6',
               '12': '6'
               }

Cerved_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=cqs_mapping)

# Creditreform Rating AG
originator = 'Creditreform Rating AG'
full_name = 'Long-term issuer rating scale'
definition = [('0', "AAA"), ('1', "AA"),
              ('2', "A"),
              ('3', "BBB"),
              ('4', "BB"),
              ('5', "B"), ('6', "C"), ('7', "SD"), ('8', "D")]
cqs_mapping = {'0': '1',
               '1': '1',
               '2': '2',
               '3': '4',
               '4': '5',
               '5': '6',
               '6': '6',
               '7': '6',
               '8': '6'
               }

CRR_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=cqs_mapping)

# DBRS Ratings Limited
originator = 'DBRS Ratings Limited'
full_name = 'Long-term obligations rating scale'
definition = [('0', "AAA"), ('1', "AA"),
              ('2', "A"),
              ('3', "BBB"),
              ('4', "BB"),
              ('5', "B"),
              ('6', "CCC"), ('7', "CC"), ('8', "C"), ('9', "D")]
cqs_mapping = {'0': '1',
               '1': '1',
               '2': '2',
               '3': '3',
               '4': '4',
               '5': '5',
               '6': '6',
               '7': '6',
               '8': '6',
               '9': '6'
               }

DBRS_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=cqs_mapping)

# Fitch Ratings
originator = 'Fitch Ratings'
full_name = 'Long-term issuer default rating scale'
definition = [('0', "AAA"), ('1', "AA"),
              ('2', "A"),
              ('3', "BBB"),
              ('4', "BB"),
              ('5', "B"),
              ('6', "CCC"), ('7', "CC"), ('8', "C"), ('9', "RD"), ('10', "D")]
cqs_mapping = {'0': '1',
               '1': '1',
               '2': '2',
               '3': '3',
               '4': '4',
               '5': '5',
               '6': '6',
               '7': '6',
               '8': '6',
               '9': '6',
               '10': '6'
               }

Fitch_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=cqs_mapping)

# Moody’s Investors Service
originator = 'Moody’s Investors Service'
full_name = 'Global long-term rating scale'
definition = [('0', "Aaa"), ('1', "Aa"),
              ('2', "A"),
              ('3', "Baa"),
              ('4', "Ba"),
              ('5', "B"),
              ('6', "Caa"), ('7', "Ca"), ('8', "C")]
cqs_mapping = {'0': '1',
               '1': '1',
               '2': '2',
               '3': '3',
               '4': '4',
               '5': '5',
               '6': '6',
               '7': '6',
               '8': '6'
               }

Moodys_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=cqs_mapping)

# Scope Ratings AG
originator = 'Scope Ratings AG'
full_name = 'Long-term rating scale'
definition = [('0', "AAA"), ('1', "AA"),
              ('2', "A"),
              ('3', "BBB"),
              ('4', "BB"),
              ('5', "B"),
              ('6', "CCC"), ('7', "CC"), ('8', "C"), ('9', "D")]
cqs_mapping = {'0': '1',
               '1': '1',
               '2': '2',
               '3': '3',
               '4': '4',
               '5': '5',
               '6': '6',
               '7': '6',
               '8': '6',
               '9': '6'
               }

Scope_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=cqs_mapping)

# Standard & Poor’s Ratings Services
originator = 'Standard & Poor’s Ratings Services'
full_name = 'Long-term issuer credit rating scale'
definition = [('0', "AAA"), ('1', "AA"),
              ('2', "A"),
              ('3', "BBB"),
              ('4', "BB"),
              ('5', "B"),
              ('6', "CCC"), ('7', "CC"), ('8', "C"), ('9', "R"), ('10', "SD/D")]
cqs_mapping = {'0': '1',
               '1': '1',
               '2': '2',
               '3': '3',
               '4': '4',
               '5': '5',
               '6': '6',
               '7': '6',
               '8': '6',
               '9': '6',
               '10': '6'
               }

SnP_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=cqs_mapping)

# S&P Coarse Scale
definition = [('0', "AAA"), ('1', "AA"), ('2', "A"), ('3', "BBB"), ('4', "BB"), ('5', "B"), ('6', "CCC"), ('7', "D")]

SnP_Simple_SS = StateSpace(definition=definition)

#
# Mappings between scales other than CQS
#

SnP_Fitch2Moodys = {
    'AAA': 'Aaa',
    'AA+': 'Aa1',
    'AA': 'Aa2',
    'AA-': 'Aa3',
    'A+': 'A1',
    'A': 'A2',
    'A-': 'A3',
    'BBB+': 'Baa1',
    'BBB': 'Baa2',
    'BBB-': 'Baa3',
    'BB+': 'Ba1',
    'BB': 'Ba2',
    'BB-': 'Ba3',
    'B+': 'B1',
    'B': 'B2',
    'B-': 'B3',
    'CCC+': 'Caa1',
    'CCC': 'Caa2',
    'CCC-': 'Caa3',
    'CC': 'Ca',
    'C': 'Ca',
    'D': 'C'
}

Moodys2DBRS = {
    'Aaa': 'AAA',
    'Aa1': 'AA (high)',
    'Aa2': 'AA',
    'Aa3': 'AA (low)',
    'A1': 'A (high)',
    'A2': 'A',
    'A3': 'A (low)',
    'Baa1': 'BBB (high)',
    'Baa2': 'BBB',
    'Baa3': 'BBB (low)',
    'Ba1': 'BB (high)',
    'Ba2': 'BB',
    'Ba3': 'BB (low)',
    'B1': 'B (high)',
    'B2': 'B',
    'B3': 'B (low)',
    'Caa1': 'CCC (high)',
    'Caa2': 'CCC',
    'Caa3': 'CCC (low)',
    'Ca': 'CC',
    'C': 'D'
}
