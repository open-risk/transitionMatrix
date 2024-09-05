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

import pandas as pd

import transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import cohort_estimator as es

ACCURATE_DIGITS = 2


class TestSimpleEstimator(unittest.TestCase):
    pass


class TestCohortEstimator(unittest.TestCase):
    """
    Test the estimation of a simple 3x3 transition matrix with absorbing state

    .. note: The result is subject to sampling error! Ensure the required accuracy corresponds to the input data size

    """

    def test_cohort_estimator_counts(self):
        """
        Test that the total counts constructed by the estimator is the same as the event count in the dataset

        """
        dataset_path = source_path + "datasets/"
        data = pd.read_csv(dataset_path + 'synthetic_data5.csv')
        event_count = data['ID'].count()
        # event_count = data[data['Time'] < 4]['ID'].count()
        definition = [('0', "Stage 1"), ('1', "Stage 2"), ('2', "Stage 3")]
        myState = tm.StateSpace(definition)
        sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
        myEstimator = es.CohortEstimator(states=myState, cohort_bounds=[0, 1, 2, 3, 4],
                                         ci={'method': 'goodman', 'alpha': 0.05})
        result = myEstimator.fit(sorted_data)
        self.assertEqual(event_count, myEstimator.counts)

    def test_cohort_estimator_matrix(self):
        """
        Test that the estimated matrix is same as the matrix that was used to generate the data

        matrix = [[0.8, 0.15, 0.05],
                  [0.1, 0.7, 0.2],
                  [0.0, 0.0, 1.0]]

        """
        dataset_path = source_path + "datasets/"
        data = pd.read_csv(dataset_path + 'synthetic_data5.csv')
        definition = [('0', "Stage 1"), ('1', "Stage 2"), ('2', "Stage 3")]
        myState = tm.StateSpace(definition)
        sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
        myEstimator = es.CohortEstimator(states=myState, cohort_bounds=[0, 1, 2, 3, 4],
                                         ci={'method': 'goodman', 'alpha': 0.05})
        result = myEstimator.fit(sorted_data)
        am = myEstimator.average_matrix
        self.assertAlmostEqual(am[0, 0], 0.8, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(am[0, 1], 0.15, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(am[0, 2], 0.05, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(am[1, 0], 0.1, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(am[1, 1], 0.7, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(am[1, 2], 0.2, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(am[2, 0], 0.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(am[2, 1], 0.0, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(am[2, 2], 1.0, places=ACCURATE_DIGITS, msg=None, delta=None)
