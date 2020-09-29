# encoding: utf-8

# (c) 2017-2020 Open Risk, all rights reserved
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
Examples using transitionMatrix to perform various state space operations

"""

import transitionMatrix as tm
from transitionMatrix import SnP_Fitch2Moodys, Moodys2DBRS
from transitionMatrix.utils import dataset_generators as dg

print("Some Basics")
print(80*"=")
# Lets load a credit rating scale
myState = tm.SnP_SS
# Print the states
print("The States of our starting scale: ", myState.get_states())
# Print the state labels
print("The State Labels: ", myState.get_state_labels())
# Print the complete definition
print("The Full Description: ", myState.definition)

# Convert SnP ratings to Moody's and DBRS
# Escape R (regulatory default) and SD (selective default)
print("")
print("Convert labels to other rating scales scales")
print(80*"=")
for state in myState.get_state_labels():
    if state not in ['R', 'SD/D']:
        print(state, ' ----> (', SnP_Fitch2Moodys[state], Moodys2DBRS[SnP_Fitch2Moodys[state]],')')

print("")
print("Convert data to other scales")
print(80*"=")
print("Input S&P Labels: ")
# Generate some portfolio data and map to CQS
portfolio = dg.portfolio_labels(myState, 100)
print(portfolio)
print("")
print("Output CQS Labels: ")
mapped_portfolio = []
for label in portfolio:
    mapped_portfolio.append(myState.cqs_map(label))
print(mapped_portfolio)