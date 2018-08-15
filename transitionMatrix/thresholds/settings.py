# encoding: utf-8

# (c) 2017-2018 Open Risk (https://www.openriskmanagement.com)
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

""" Integration Settings """

GRID_POINTS = 2000
PRECISION = 1.e-8
SCALE = 7.0
DELTA = 2000

# Select the autoregressive model AR(1) to fit
# Mu is the process drift
# Phi is the process autocorrelation parameter
# [X_0, X_1] are th process initial conditions

AR_Model = {
    "Mu": 0.0,
    "Phi": [1.0],
    "Initial Conditions": [1.0, 0.0]
}
