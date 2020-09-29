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

# Example script. Open Risk Academy Course Step 5.


import pandas as pd
import transitionMatrix as tm
from transitionMatrix.estimators import simple_estimator as es
dataset_path = "../../datasets/"
data = pd.read_csv(dataset_path + 'LoanStats3a_Step2.csv')
print(data.describe())

description = [('A', "Grade A"), ('B', "Grade B"), ('C', "Grade C"),
               ('D', "Grade D"), ('E', "Grade E"), ('F', "Grade F"),
               ('G', "Grade G"), ('H', "Delinquent"), ('I', "Charged Off"),
               ('J', "Repaid")]
myState = tm.StateSpace(description)

labels = {'State': 'State_IN'}
print(myState.validate_dataset(dataset=data, labels=labels))
labels = {'State': 'State_OUT'}
print(myState.validate_dataset(dataset=data, labels=labels))

myEstimator = es.SimpleEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
result = myEstimator.fit(data)
myEstimator.summary()

myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
print(myMatrixSet.temporal_type)
myMatrixSet.print_matrix()

myMatrix = myMatrixSet.entries[0]
myMatrix[7, 9] = 1.0
myMatrix[8, 9] = 1.0
myMatrix[9, 9] = 1.0
print(myMatrix.validate())
print(myMatrix.characterize())
myMatrix.print()
