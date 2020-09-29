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

# Example script. Open Risk Academy Course Step 3.

import pandas as pd
import transitionMatrix as tm
from transitionMatrix.estimators import cohort_estimator as es

dataset_path = "../../datasets/"

description = [('0', "AAA"), ('1', "AA"), ('2', "A"), ('3', "BBB"),
               ('4', "BB"), ('5', "B"), ('6', "CCC"), ('7', "D")]
myState = tm.StateSpace(description)

myState.describe()
print(myState.get_states())
print(myState.get_state_labels())

data = pd.read_csv(dataset_path + 'synthetic_data4.csv', dtype={'State': str})

sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])

print(myState.validate_dataset(dataset=sorted_data))

myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
result = myEstimator.fit(sorted_data)
myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')

myEstimator.summary()
