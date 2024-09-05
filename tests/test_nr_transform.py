# encoding: utf-8

# (c) 2017-2024 Open Risk, all rights reserved
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
import logging
import sys

import transitionMatrix as tm
from transitionMatrix import dataset_path
from transitionMatrix.model import TransitionMatrix
from transitionMatrix.creditratings.predefined import SP02, SP02NR

# ACCURATE_DIGITS = 7
ACCURATE_DIGITS = 2


class TestNRTransform(unittest.TestCase):
    """
    1. Load in-memory matrices
    2. Perform NR transformation
    3. Test with S&P Result

    .. todo:: SnP result rounding seems large

    """

    def test_nr_matrix_load(self):
        a = TransitionMatrix(values=SP02NR)
        # messages = a.validate()
        # log = logging.getLogger("Test.testNR")
        # log.debug("messages= %r", messages)
        # self.assertTrue(messages)
        self.assertEqual(a.shape[0], a.shape[1])
        self.assertEqual(a.dimension, 9)

    def test_nr_remove(self):
        a = TransitionMatrix(values=SP02NR)
        b = TransitionMatrix(values=SP02)
        a = 0.01 * a
        b = 0.01 * b
        a = a.remove(8, method='noninform')
        for i in range(a.dimension):
            for j in range(a.dimension):
                self.assertAlmostEqual(a[i, j], b[i, j], places=ACCURATE_DIGITS)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("Test.testNR").setLevel(logging.DEBUG)
    unittest.main()
