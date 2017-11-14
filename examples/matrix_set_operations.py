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


""" Examples using transitionMatrix to perform operations with transition matrix sequences

"""

import transitionMatrix as tm
from datasets import Generic as T1

print("-- Lets seed the set with a 3x3 matrix")
A = tm.TransitionMatrix(values=[[0.6, 0.2, 0.2], [0.2, 0.6, 0.2], [0.2, 0.2, 0.6]])
print(A)

print("-- Identical future period transitions in incremental mode")
A_Set = tm.TransitionMatrixSet(values=A, periods=3, method='Copy', temporal_type='Incremental')
print(A_Set.entries)

print("-- Identical future period transitions in cumulative mode using the power method")
B_Set = tm.TransitionMatrixSet(values=A, periods=3, method='Power', temporal_type='Cumulative')
print(B_Set.entries)

print("-- Lets instantiate the set directly using a list of matrices")
C_Vals = [[[0.75, 0.25], [0.0, 1.0]],  [[0.75, 0.25], [0.0, 1.0]]]
C_Set = tm.TransitionMatrixSet(values=C_Vals, temporal_type='Incremental')
print(C_Set.entries)

print("-- Validate the constructed sets")
A_Set.validate()
B_Set.validate()
C_Set.validate()

print("-- Convert to Cumulative")
A_Set.cumulate()
print(A_Set.entries)
A_Set.validate()

print("-- Convert back to Incremental")
A_Set.incremental()
print(A_Set.entries)
A_Set.validate()

print("-- Create a multiperiod matrix set and save to json file")
T_Set = tm.TransitionMatrixSet(values=T1, periods=10, method='Power', temporal_type='Cumulative')
T_Set.to_json('Tn.json')

