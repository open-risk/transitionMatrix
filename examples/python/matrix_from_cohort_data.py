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


"""
Example workflows using transitionMatrix to estimate a transition matrix from data in cohort format

"""


import pandas as pd

import transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators import cohort_estimator as es

dataset_path = source_path + "datasets/"

# Select the example to run
# 1-> S&P Style Credit Rating Migration Matrix
# 2-> IFRS 9 Style Migration Matrix
# 3-> Simplest Absorbing Case for validation

example = 2

if example == 1:
    # Example: S&P Style Credit Rating Migration Matrix

    # S&P Ratings State Space
    definition = [('0', "AAA"), ('1', "AA"), ('2', "A"), ('3', "BBB"),
                   ('4', "BB"), ('5', "B"), ('6', "CCC"), ('7', "D")]

    myState = tm.StateSpace(definition)
    print("> Describe state space")
    myState.describe()
    print("> List of states")
    print(myState.get_states())
    print("> List of state labels")
    print(myState.get_state_labels())

    print("> Load and validate dataset")
    data = pd.read_csv(dataset_path + 'synthetic_data4.csv', dtype={'State': str})
    sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
    print(myState.validate_dataset(dataset=sorted_data))

    # compute confidence interval using goodman method at 95% confidence level
    myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
    result = myEstimator.fit(sorted_data)

    # Print confidence intervals
    print("> Compute confidence interval using goodman method at 95% confidence level")
    myEstimator.summary()

    # Print the estimated results
    myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
    # print(myMatrixSet.temporal_type)
    print("> Print Estimated Matrix Set")
    myMatrixSet.print_matrix()

elif example == 2:
    # Example: IFRS 9 Style Migration Matrix
    # Load historical data into pandas frame
    # Format:
    # discrete time grid (already arranged in cohorts)

    # Step 1
    # Load the data set into a pandas frame
    # Make sure state is read as a string and not as integer
    # Fifth synthetic data example: IFRS 9 Migration Matrix
    print(">>> Step 1")
    data = pd.read_csv(dataset_path + 'synthetic_data5.csv', dtype={'State': str})
    sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
    # Data is in pandas frame, all methods are available
    print(sorted_data.describe())

    # Step 2
    # Describe and validate the State Space against the data
    print(">>> Step 2")
    definition = [('0', "Stage 1"), ('1', "Stage 2"), ('2', "Stage 3")]
    myState = tm.StateSpace(definition)
    myState.describe()
    print(myState.validate_dataset(dataset=sorted_data))

    # Step 3
    # Estimate matrices using method of choice
    # compute confidence interval using goodman method at 95% confidence level
    print(">>> Step 3")
    myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
    # myMatrix = matrix.CohortEstimator(states=myState)
    result = myEstimator.fit(sorted_data)
    myEstimator.summary()

    # Step 4
    # Review numerical results
    print(">>> Step 4")
    myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
    print(myMatrixSet.temporal_type)
    myMatrixSet.print_matrix()

elif example == 3:
    # Example: Simplest Absorbing Case for validation
    data = pd.read_csv(dataset_path + 'synthetic_data6.csv', dtype={'State': str})
    sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
    myState = tm.StateSpace()
    myState.generic(2)
    print(myState.validate_dataset(dataset=sorted_data))
    myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
    result = myEstimator.fit(sorted_data)
    myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')

    myEstimator.print(select='Counts', period=0)
    myEstimator.print(select='Frequencies', period=18)

