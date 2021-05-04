# encoding: utf-8

# (c) 2017-2021 Open Risk, all rights reserved
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


class TestTransitionMatrix(unittest.TestCase):
    '''
    Default instance (2x2 identity matrix)
    '''
    def test_instantiate_matrix(self):
        a = tm.TransitionMatrix()
        self.assertAlmostEqual(a[0, 0], 1.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[0, 1], 0.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[1, 0], 0.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[1, 1], 1.0, places=ACCURATE_DIGITS, msg=None, delta=None)

        b = tm.TransitionMatrix([[1.0, 3.0], [1.0, 4.0]])
        self.assertAlmostEqual(b[0, 0], 1.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(b[0, 1], 3.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(b[1, 0], 1.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(b[1, 1], 4.0, places=ACCURATE_DIGITS, msg=None, delta=None)

    def test_csv_io(self):
        a = tm.TransitionMatrix()
        a.to_csv("test.csv")
        b = tm.TransitionMatrix(csv_file="test.csv")
        self.assertAlmostEqual(a[0, 0], b[0, 0], places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[0, 1], b[0, 1], places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[1, 0], b[1, 0], places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[1, 1], b[1, 1], places=ACCURATE_DIGITS, msg=None, delta=None)

    def test_json_io(self):
        a = tm.TransitionMatrix()
        a.to_json("test.json")
        b = tm.TransitionMatrix(json_file="test.json")
        self.assertAlmostEqual(a[0, 0], b[0, 0], places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[0, 1], b[0, 1], places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[1, 0], b[1, 0], places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[1, 1], b[1, 1], places=ACCURATE_DIGITS, msg=None, delta=None)

    def test_validation(self):
        a = tm.TransitionMatrix()
        self.assertEqual(a.validate(), True)
        b = tm.TransitionMatrix(values=[1.0, 3.0])
        self.assertEqual(b.validate()[0][0], 'Matrix Dimensions Differ: ')
        c = tm.TransitionMatrix(values=[[0.75, 0.25], [0.0, 0.9]])
        self.assertEqual(c.validate()[0][0], 'Rowsum not equal to one: ')
        d = tm.TransitionMatrix(values=[[0.75, 0.25], [-0.1, 1.1]])
        self.assertEqual(d.validate()[0][0], 'Negative Probabilities: ')

    def test_generator(self):
        a = tm.TransitionMatrix([[1.0, 3.0], [1.0, 4.0]])
        self.assertAlmostEqual(a[0, 0], expm(a.generator())[0, 0], places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[0, 1], expm(a.generator())[0, 1], places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[1, 0], expm(a.generator())[1, 0], places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a[1, 1], expm(a.generator())[1, 1], places=ACCURATE_DIGITS, msg=None, delta=None)


class TestTransitionMatrixSet(unittest.TestCase):

    def test_instantiate_matrix_set(self):
        periods = 5
        a = tm.TransitionMatrixSet(dimension=2, periods=periods)
        self.assertEqual(a.temporal_type, 'Incremental')
        self.assertAlmostEqual(a.entries[0][0, 0], 1.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(a.entries[periods-1][0, 0], 1.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        pass

    def test_set_validation(self):
        a = tm.TransitionMatrixSet(dimension=2, periods=5)
        self.assertEqual(a.validate(), True)

    def test_set_cumulate_incremental(self):
        a = tm.TransitionMatrix(values=[[0.6, 0.2, 0.2], [0.2, 0.6, 0.2], [0.2, 0.2, 0.6]])
        a_set = tm.TransitionMatrixSet(values=a, periods=3, method='Copy', temporal_type='Incremental')
        b_set = a_set
        b_set.cumulate()
        b_set.incremental()
        self.assertAlmostEqual(a_set.entries[2][0, 0], b_set.entries[2][0, 0], places=ACCURATE_DIGITS, msg=None, delta=None)
        pass

    def test_set_csv_io(self):
        pass

    def test_set_json_io(self):
        pass


if __name__ == "__main__":

    unittest.main()

