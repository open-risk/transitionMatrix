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
Example workflows using transitionMatrix to estimate a matrix from duration type data
Cohort type dataset (Generic Rating Matrix). Offers a semi-realistic example

"""

import pandas as pd

import transitionMatrix as tm
from transitionMatrix import source_path
from transitionMatrix.estimators.aalen_johansen_estimator import AalenJohansenEstimator
from transitionMatrix.estimators.cohort_estimator import CohortEstimator
from transitionMatrix.statespaces.statespace import StateSpace
from transitionMatrix.utils.converters import to_canonical
from transitionMatrix.utils.preprocessing import unique_timestamps

dataset_path = source_path + "datasets/"
data = pd.read_csv(dataset_path + 'synthetic_data4.csv', dtype={'State': str})
myState = StateSpace(transition_data=data)
cohort_bounds = unique_timestamps(data)

# Estimate matrices using the Cohort estimator
myEstimator = CohortEstimator(states=myState, cohort_bounds=cohort_bounds, ci={'method': 'goodman', 'alpha': 0.05})
result = myEstimator.fit(data)
myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')
myMatrixSet.cumulate()
myMatrixSet.print_matrix(period=8)

# Estimate matrices using the Aalen-Johansen estimator
canonical_data = to_canonical(data)
myEstimator2 = AalenJohansenEstimator(states=myState)
etm, times = myEstimator2.fit(canonical_data)
myMatrix2 = tm.TransitionMatrix(etm[:, :, -1])
print('Cumulative Empirical Matrix')
myMatrix2.print_matrix()


def main():
    print("Done")


if __name__ == "__main__":
    main()
