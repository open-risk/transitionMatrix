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
Example workflow using transitionMatrix to estimate a matrix from LendingClub data
Input data are in a special cohort format as the published datasets have some limitations

"""

import pandas as pd

import transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import simple_estimator as es

dataset_path = source_path + "datasets/"

# Example: LendingClub Style Migration Matrix
# Load historical data into pandas frame
# Format:
# Expected Data Format is (ID, State_IN, State_OUT)

# Step 1
# Load the data set into a pandas frame
# Make sure state is read as a string and not as integer
print("Step 1")
data = pd.read_csv(dataset_path + 'LoanStats3a_Step2.csv')
# Data is in pandas frame, all pandas methods are available
print(data.describe())

# Step 2
# Describe and validate the State Space against the data
print("Step 2")
definition = [('A', "Grade A"), ('B', "Grade B"), ('C', "Grade C"),
               ('D', "Grade D"), ('E', "Grade E"), ('F', "Grade F"),
               ('G', "Grade G"), ('H', "Delinquent"), ('I', "Charged Off"),
               ('J', "Repaid")]
myState = tm.StateSpace(definition)
myState.describe()
labels = {'State': 'State_IN'}
print(myState.validate_dataset(dataset=data, labels=labels))
labels = {'State': 'State_OUT'}
print(myState.validate_dataset(dataset=data, labels=labels))

# Step 3
# Estimate matrices using Simple Estimator (Frequency count)
# compute confidence interval using goodman method at 95% confidence level

print("Step 3")
myEstimator = es.SimpleEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
# resulting matrix array is returned as result
result = myEstimator.fit(data)
# confidence levels are stored with the estimator
myEstimator.summary()

# Step 4
# Review numerical results
print("Step 4")
myMatrix = tm.TransitionMatrix(result)
myMatrix.print_matrix()

# In the LendingClub example we need to fix some matrix rows
# because there are no state_IN observations besides initial grade assignment
myMatrix[7, 9] = 1.0
myMatrix[8, 9] = 1.0
myMatrix[9, 9] = 1.0
print(myMatrix.validate())
print(myMatrix.characterize())
myMatrix.print_matrix()


def main():
    print("Done")


if __name__ == "__main__":
    main()
