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


"""
Create deterministic transitions

"""

import pandas as pd

import transitionMatrix as tm
from transitionMatrix.estimators import cohort_estimator as es
from transitionMatrix.generators import dataset_generators
from transitionMatrix.utils.converters import datetime_to_float, to_compact

sequences = [[(0.0, 0), (0.5, 1), (1.0, 2)],
             [(0.0, 1), (0.3, 0), (0.8, 1)],
             [(0.0, 2), (0.2, 1), (0.7, 2)]]

replication_count = 10

definition = [('0', "A"), ('1', "B"), ('2', "C")]
myState = tm.StateSpace(definition)

# myState = tm.StateSpace(definition)
input_data = dataset_generators.deterministic(sequences, replication_count)
print(input_data)
sorted_data = input_data.sort_values(['ID', 'Time'], ascending=[True, True])
cohort_data, cohort_bounds = tm.utils.bin_timestamps(sorted_data, cohorts=100)
print(80*'=')
print(cohort_data)
myEstimator = es.CohortEstimator(states=myState, cohort_bounds=cohort_bounds, ci={'method': 'goodman', 'alpha': 0.05})
result = myEstimator.fit(cohort_data, labels={'Time': 'Time', 'State': 'State', 'ID': 'ID'})
myMatrix = tm.TransitionMatrix(myEstimator.average_matrix)
myEstimator.print(select='Counts')
myMatrix.print_matrix(accuracy=3)