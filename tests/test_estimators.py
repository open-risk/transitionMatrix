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
from transitionMatrix.estimators import cohort_estimator as es
from transitionMatrix import source_path
import pandas as pd


class TestSimpleEstimator(unittest.TestCase):
    pass


class TestCohortEstimator(unittest.TestCase):

    def test_cohort_estimator_counts(self):

        dataset_path = source_path + "datasets/"
        data = pd.read_csv(dataset_path + 'synthetic_data5.csv')
        event_count = data[data['Timestep'] < 4]['ID'].count()
        description = [('0', "Stage 1"), ('1', "Stage 2"), ('2', "Stage 3")]
        myState = tm.StateSpace(description)
        sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
        myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
        result = myEstimator.fit(sorted_data)
        self.assertEqual(event_count, myEstimator.counts)
