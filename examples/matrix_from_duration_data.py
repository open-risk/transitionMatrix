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


"""
Example workflows using transitionMatrix to estimate a matrix from duration type data
The the datasets are produced in examples/generate_synthetic_data.py

"""

import pandas as pd
import transitionMatrix as tm
from transitionMatrix.estimators import cohort_estimator as es

dataset_path = "../../transitionMatrix/datasets/"
example = 2

if example == 1:

    # An example with inadequate data (dataset contains only one entity)
    data = pd.read_csv(dataset_path + 'synthetic_data1.csv', dtype={'State': str})
    sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
    myState = tm.StateSpace([('0', "A"), ('1', "B"), ('2', "C"), ('3', "D")])
    print(myState.validate_dataset(dataset=sorted_data))
    cohort_data, cohort_intervals = tm.utils.bin_timestamps(data, cohorts=5)
    myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
    labels = {'Timestamp': 'Cohort', 'State': 'State', 'ID': 'ID'}
    result = myEstimator.fit(cohort_data, labels=labels)
    # Check significance of some estimates
    # First period
    myEstimator.summary(k=0)
    # Last period
    myEstimator.summary(k=4)

elif example == 2:

    # Step 1
    # Load the data set into a pandas frame
    # Make sure state is read as a string and not as integer
    # Second synthetic data example:
    # n entities with ~10 observations each, [0,1] state, 50%/50% transition matrix
    print(">>> Step 1")
    data = pd.read_csv(dataset_path + 'synthetic_data2.csv', dtype={'State': str})
    sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
    print(sorted_data.describe())

    # Step 2
    # Describe and validate the State Space against the data
    print(">>> Step 2")
    myState = tm.StateSpace([('0', "Basic"), ('1', "Default")])
    myState.describe()
    print(myState.validate_dataset(dataset=sorted_data))

    # Step 3
    # Arrange the data in period cohorts
    print(">>> Step 3")
    cohort_data, cohort_intervals = tm.utils.bin_timestamps(data, cohorts=5)

    # Step 4
    # Estimate matrices using method of choice
    # compute confidence interval using goodman method at 95% confidence level
    print(">>> Step 4")
    myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
    labels = {'Timestamp': 'Cohort', 'State': 'State', 'ID': 'ID'}
    result = myEstimator.fit(cohort_data, labels=labels)

    # Step 5
    # Print out the set of estimated matrices
    print(">>> Step 5")
    myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
    print(myMatrixSet.temporal_type)
    myMatrixSet.print()


elif example == 3:

    data = pd.read_csv(dataset_path + 'synthetic_data3.csv', dtype={'State': str})
    sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
    myState = tm.StateSpace([('0', "A"), ('1', "B"), ('2', "C"), ('3', "D"), ('4', "E"), ('5', "F"), ('6', "G")])
    print(myState.validate_dataset(dataset=sorted_data))
    cohort_data, cohort_intervals = tm.utils.bin_timestamps(data, cohorts=5)
    myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
    labels = {'Timestamp': 'Cohort', 'State': 'State', 'ID': 'ID'}
    result = myEstimator.fit(cohort_data, labels=labels)
    myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
    myMatrixSet.print()
