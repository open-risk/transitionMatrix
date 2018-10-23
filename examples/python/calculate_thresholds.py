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


""" Example of calculating thresholds

"""

import numpy as np
from scipy.stats import norm

import transitionMatrix as tm
from datasets import Minimal, Generic
from transitionMatrix.thresholds.model import ThresholdSet
from transitionMatrix.thresholds.settings import AR_Model


# Initialize a single period transition matrix
# Example 1: Generic -> Typical Credit Rating Transition Matrix
# Example 2: Minimal -> Three state transition matrix

# M = tm.TransitionMatrix(values=Minimal)
M = tm.TransitionMatrix(values=Generic)
# Lets take a look at the values
print("> Load and validate a minimal transition matrix")
M.print()
M.validate()
print("> Valid Input Matrix? ", M.validated)

# The size of the rating scale
Ratings = M.dimension

# The Default (absorbing state)
Default = Ratings - 1

# Lets extend the matrix into multi periods
Periods = 10
T = tm.TransitionMatrixSet(values=M, periods=Periods, method='Power', temporal_type='Cumulative')
print("> Extend the matrix into 10 periods")


# Initialize a threshold set
As = ThresholdSet(TMSet=T)

# Calculate thresholds per initial rating state
print("> Calculate thresholds per initial rating state")
for ri in range(0, Ratings):
    print("Initial Rating: ", ri)
    As.fit(AR_Model, ri)

# Display the calculated thresholds
print("> Display the calculated thresholds")
As.print()