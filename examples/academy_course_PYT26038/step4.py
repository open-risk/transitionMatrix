# encoding: utf-8

# (c) 2017-2020 Open Risk (https://www.openriskmanagement.com)
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

# Example script. Open Risk Academy Course Step 4.


import pandas as pd
import transitionMatrix as tm
from transitionMatrix.estimators import cohort_estimator as es

dataset_path = "../../datasets/"

data = pd.read_csv(dataset_path + 'synthetic_data2.csv', dtype={'State': str})
sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])

myState = tm.StateSpace([('0', "Basic"), ('1', "Default")])
myState.describe()
print(myState.validate_dataset(dataset=sorted_data))

cohort_data, cohort_intervals = tm.utils.bin_timestamps(data, cohorts=5)

myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
labels = {'Timestamp': 'Cohort', 'State': 'State', 'ID': 'ID'}
result = myEstimator.fit(cohort_data, labels=labels)

myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
print(myMatrixSet.temporal_type)
myMatrixSet.print_matrix()
