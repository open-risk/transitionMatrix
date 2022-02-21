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

import transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import cohort_estimator as es
from transitionMatrix.generators import dataset_generators
from transitionMatrix.utils import to_canonical
from transitionMatrix.utils.converters import to_compact

ACCURATE_DIGITS = 7

Identity = [
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0]
]

dataset_path = source_path + "datasets/"

class TestRoundTrip(unittest.TestCase):
    """
    Round-trip testing: Identity Matrix Markov Chain
    Generate some trivial identity migrations
    Check that the cohort estimator computes identity

    """

    def test_roundtrip_identity(self):
        definition = [('0', "A"), ('1', "B"), ('2', "C"), ('3', "D")]
        myState = tm.StateSpace(definition)
        input_data = dataset_generators.long_format(myState, Identity, n=100, timesteps=2, mode='Canonical')
        compact_data = to_compact(input_data)
        cohort_data, cohort_bounds = tm.utils.bin_timestamps(compact_data, cohorts=1)
        sorted_data = cohort_data.sort_values(['ID', 'Time'], ascending=[True, True])
        myEstimator = es.CohortEstimator(states=myState, cohort_bounds=cohort_bounds,
                                         ci={'method': 'goodman', 'alpha': 0.05})
        result = myEstimator.fit(sorted_data, labels={'Time': 'Time', 'State': 'State', 'ID': 'ID'})
        myMatrix = tm.TransitionMatrix(myEstimator.average_matrix)

        self.assertAlmostEqual(myMatrix[0, 0], 1.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(myMatrix[1, 1], 1.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(myMatrix[2, 2], 1.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(myMatrix[2, 2], 1.0, places=ACCURATE_DIGITS, msg=None, delta=None)

    """
    Round-trip testing: Data Formats
    Load a data set in compact format
    Convert to canonical, back to compact and compare

    """

    def test_roundtrip_formats(self):
        input_data = pd.read_csv(dataset_path + 'rating_data.csv')
        canonical_data = to_canonical(input_data)
        compact_data = to_compact(canonical_data)

        self.assertEqual(len(compact_data.compare(input_data)), 0, msg=None)


if __name__ == "__main__":
    unittest.main()
