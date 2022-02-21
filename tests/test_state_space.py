# encoding: utf-8

# (c) 2017-2022 Open Risk, all rights reserved
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


import unittest

import pandas as pd
from scipy.linalg import expm

import transitionMatrix as tm
from transitionMatrix import source_path

ACCURATE_DIGITS = 7


class TestStateSpace(unittest.TestCase):

    def test_instantiate_state(self):
        definition = [('0', "AAA"), ('1', "AA"), ('2', "A"), ('3', "BBB"),
                       ('4', "BB"), ('5', "B"), ('6', "CCC"), ('7', "D")]
        s = tm.StateSpace(definition)
        self.assertEqual(s.definition[0][1], 'AAA')

    def test_get_states(self):
        definition = [('0', "AAA"), ('1', "AA"), ('2', "A"), ('3', "BBB"),
                       ('4', "BB"), ('5', "B"), ('6', "CCC"), ('7', "D")]
        s = tm.StateSpace(definition)
        self.assertEqual(s.get_states()[0], '0')

    def test_get_state_labels(self):
        definition = [('0', "AAA"), ('1', "AA"), ('2', "A"), ('3', "BBB"),
                       ('4', "BB"), ('5', "B"), ('6', "CCC"), ('7', "D")]
        s = tm.StateSpace(definition)
        self.assertEqual(s.get_state_labels()[0], 'AAA')

    def test_generic(self):
        s = tm.StateSpace()
        n = 10
        s.generic(n=n)
        self.assertEqual(s.get_state_labels()[n-1], str(n-1))

    def test_validate_dataset(self):
        dataset_path = source_path + "datasets/"
        data = pd.read_csv(dataset_path + 'test.csv', dtype={'State': int})
        # definition = [('0', "Stage 1"), ('1', "Stage 2"), ('2', "Stage 3")]
        definition = [('0', "0"), ('1', "1"), ('2', "2")]
        s = tm.StateSpace(definition)
        self.assertEqual(s.validate_dataset(dataset=data)[0], "Dataset contains the expected states.")


if __name__ == "__main__":

    unittest.main()

