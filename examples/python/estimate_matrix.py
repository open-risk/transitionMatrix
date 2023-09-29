# encoding: utf-8

# (c) 2017-2023 Open Risk, all rights reserved
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
An end-to-end example of estimating a credit rating matrix from historical data using two different estimators

"""
import pprint as pp

import pandas as pd
from scipy.linalg import expm

import transitionMatrix as tm
from transitionMatrix.estimators.aalen_johansen_estimator import AalenJohansenEstimator
from transitionMatrix.estimators.cohort_estimator import CohortEstimator
from transitionMatrix.statespaces.statespace import StateSpace
from transitionMatrix.utils import transitions_summary
from transitionMatrix.utils.converters import to_canonical

# Load the data into a pandas frame
input_data = pd.read_csv('../../datasets/rating_data.csv')
print('> Transitions Summary Input Data')
pp.pprint(transitions_summary(input_data))

# Infer and describe state space
myState = StateSpace(transition_data=input_data)
myState.describe()
print('> The order of states is not important for estimation but it is important for presentation!')

# Convert format to canonical form
canonical_data = to_canonical(input_data)

# Group the data into temporal cohorts
print(80 * '=')
cohort_data, cohort_intervals = tm.utils.bin_timestamps(input_data, cohorts=5, remove_stale=True)
print('Intervals : ', cohort_intervals)

print('> Transitions Summary Cohorted Data')
pp.pprint(transitions_summary(cohort_data))

myEstimator = CohortEstimator(states=myState, cohort_bounds=cohort_intervals, ci={'method': 'goodman', 'alpha': 0.05})

myEstimator.fit(cohort_data)

myMatrix = tm.TransitionMatrix(myEstimator.average_matrix, states=myState)
myMatrix.print_matrix(accuracy=3, format_type='Standard', labels=False)

myEstimator2 = AalenJohansenEstimator(states=myState)
labels = {'Time': 'Time', 'From': 'From', 'To': 'To', 'ID': 'ID'}
etm, times = myEstimator2.fit(canonical_data, labels=labels)
myMatrix2 = tm.TransitionMatrix(etm[:, :, -1])
G = myMatrix2.generator()
oneyear = tm.TransitionMatrix(expm(0.2 * G))
oneyear.print_matrix(accuracy=3)


def main():
    print("Done")


if __name__ == "__main__":
    main()
