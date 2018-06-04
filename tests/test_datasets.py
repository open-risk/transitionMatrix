# encoding: utf-8

# (c) 2017 Open Risk, all rights reserved
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

import transitionMatrix as tm
from datasets import Minimal
from transitionMatrix import dataset_path

ACCURATE_DIGITS = 7


class TestDatasets(unittest.TestCase):
    '''
    Load in-memory matrices
    '''

    def test_minimal_matrix(self):
        a = tm.TransitionMatrix(values=Minimal)
        a.validate()
        self.assertEqual(a.dimension, 3)

    def test_matrix_set_load_csv(self):
        a = tm.TransitionMatrixSet(csv_file=dataset_path + "sp_1981-2016.csv", temporal_type='Cumulative')
        a.validate()
        self.assertEqual(a.periods, [1, 2, 3, 5, 7, 10, 15, 20])


if __name__ == "__main__":
    unittest.main()
