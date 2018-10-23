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


""" Visualize Calculated Thresholds

"""

import matplotlib.pyplot as plt
from matplotlib import collections as mc

import transitionMatrix as tm
from datasets import Generic
from transitionMatrix.thresholds.model import ThresholdSet
from transitionMatrix.thresholds.settings import AR_Model

# Initialize a single period transition matrix
# Example 1: Generic -> Typical Credit Rating Transition Matrix
# Example 2: Minimal -> Three state transition matrix

M = tm.TransitionMatrix(values=Generic)

# The size of the rating scale
Ratings = M.dimension

# The Default (absorbing state)
Default = Ratings - 1

# Lets extend the matrix into multi periods
Periods = 10
T = tm.TransitionMatrixSet(values=M, periods=Periods, method='Power', temporal_type='Cumulative')

# Initialize a threshold set
As = ThresholdSet(TMSet=T)

for ri in range(0, Ratings):
    print("RI: ", ri)
    As.fit(AR_Model, ri)

lines = []
ri = 3
for rf in range(0, Ratings):
    for k in range(0, Periods):
        if rf != ri:
            value = As.A[ri, rf, k]
            line = [(k, value), (k + 1.0, value)]
            lines.append(line)

lc = mc.LineCollection(lines, linewidths=2)
fig, ax = plt.subplots()
ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)
ax.set_xlabel("Periods")
ax.set_ylabel("Normalized Z Level")
plt.title("Rating Transition Thresholds")
plt.savefig("Thresholds.png")
