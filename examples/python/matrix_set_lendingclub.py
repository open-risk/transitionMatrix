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


"""
Example workflow using transitionMatrix to estimate a set of matrix from LendingClub data
Input data are in a special cohort format as the published datasets have some limitations

"""

import pandas as pd

import transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import simple_estimator as es

dataset_path = source_path + "datasets/"

# Example: LendingClub Style Migration Matrix Set
# Load historical data into pandas frame
# Format:
# Expected Data Format is (ID, State_IN, State_OUT)

definition = [('A', "Grade A"), ('B', "Grade B"), ('C', "Grade C"),
               ('D', "Grade D"), ('E', "Grade E"), ('F', "Grade F"),
               ('G', "Grade G"), ('H', "Delinquent"), ('I', "Charged Off"),
               ('J', "Repaid")]
myState = tm.StateSpace(definition)

# Load the data sets into a pandas frame in sequence
# Check matrix_lendingclub.py for comments

matrix_set = []
for letter in ['a', 'b', 'c', 'd']:
    # store the derived one-period matrices in a list
    data = pd.read_csv(dataset_path + 'LoanStats3' + letter + '_Step2.csv')
    myEstimator = es.SimpleEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
    result = myEstimator.fit(data)
    myEstimator.summary()
    myMatrix = tm.TransitionMatrix(result)
    myMatrix[7, 9] = 1.0
    myMatrix[8, 9] = 1.0
    myMatrix[9, 9] = 1.0
    matrix_set.append(myMatrix)

# collect all matrices in a matrix set
LC_Set = tm.TransitionMatrixSet(values=matrix_set, temporal_type='Incremental')
LC_Set.print_matrix()
