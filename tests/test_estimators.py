# encoding: utf-8

# (c) 2017-2018 Open Risk, all rights reserved
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
from transitionMatrix.estimators import aalen_johansen_estimator as aj

ACCURATE_DIGITS = 2


class TestSimpleEstimator(unittest.TestCase):
    pass


class TestCohortEstimator(unittest.TestCase):

    def test_cohort_estimator_counts(self):
        dataset_path = source_path + "datasets/"
        data = pd.read_csv(dataset_path + 'synthetic_data5.csv')
        event_count = data[data['Timestep'] < 4]['ID'].count()
        definition = [('0', "Stage 1"), ('1', "Stage 2"), ('2', "Stage 3")]
        myState = tm.StateSpace(definition)
        sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
        myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
        result = myEstimator.fit(sorted_data)
        self.assertEqual(event_count, myEstimator.counts)


class TestAalenJohansenEstimator(unittest.TestCase):
    """
    Test the estimation of a simple 2x2 transition matrix with absorbing state

    .. note: The result is subject to sampling error! Ensure the required accuracy corresponds to the input data size

    """

    def test_aalenjohansen_simple_transitions(self):
        dataset_path = source_path + "datasets/"
        data = pd.read_csv(dataset_path + 'synthetic_data8.csv')
        sorted_data = data.sort_values(['Time', 'ID'], ascending=[True, True])
        definition = [('0', "G"), ('1', "B")]
        myState = tm.StateSpace(definition)
        myEstimator = aj.AalenJohansenEstimator(states=myState)
        labels = {'Timestamp': 'Time', 'From_State': 'From', 'To_State': 'To', 'ID': 'ID'}
        result, times = myEstimator.fit(sorted_data, labels=labels)
        self.assertAlmostEqual(result[0, 0, -1], 0.5, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertAlmostEqual(result[0, 1, -1], 0.5, places=ACCURATE_DIGITS, msg=None, delta=None)
        self.assertEqual(result[1, 0, -1], 0.0)
        self.assertEqual(result[1, 1, -1], 1.0)
