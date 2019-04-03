# encoding: utf-8

# (c) 2017-2019 Open Risk (https://www.openriskmanagement.com)
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


""" transitionMatrix - Python package for statistical analysis and visualization of state space transition events """

from .model import *
from .estimators import *
from .utils import *

__version__ = '0.4.2'

package_name = 'transitionMatrix'
module_path = os.path.dirname(__file__)
source_path = module_path[:-len(package_name)]
dataset_path = os.path.join(source_path, 'datasets/')

#
# PREDEFINED STATE SPACES
#

#
# Rating Agency State Spaces
#

# S&P Basic
definition = [('0', "AAA"), ('1', "AA"), ('2', "A"), ('3', "BBB"), ('4', "BB"), ('5', "B"), ('6', "CCC"), ('7', "D")]


SnP_Simple_SS = StateSpace(definition=definition)

# AM Best Europe-Rating Services Ltd.
originator = 'AM Best Europe-Rating Services Ltd.'
full_name = 'Long-term issuer credit ratings scale'
definition = [('0', "aaa"), ('1', "aa+"), ('2', "aa"), ('3', "aa-"),
              ('4', "a+"), ('5', "a"), ('6', "a-"),
              ('7', "bbb+"), ('8', "bbb"), ('9', "bbb-"),
              ('10', "bb+"), ('11', "bb"), ('12', "bb-"),
              ('13', "b+"), ('14', "b"), ('15', "b-"),
              ('16', "ccc+"), ('17', "ccc"), ('18', "ccc-"),
              ('19', "cc"), ('20', "c"), ('21', "rs")]
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
               '21': '6'
               }

AM_Best_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=cqs_mapping)

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
               '11': '4',
               '12': '4'
               }

Cerved_SS = StateSpace(definition=definition, originator=originator, full_name=full_name, cqs_mapping=cqs_mapping)


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
full_name = 'Long-term issuer credit ratings scale'
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


# Standard & Poor’s Ratings Services
originator = 'Standard & Poor’s Ratings Services'
full_name = 'Long-term issuer credit ratings scale'
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