# encoding: utf-8

# (c) 2017-2020 Open Risk (https://www.openriskmanagement.com)
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

# Example script. Open Risk Academy Course Step 2.

import transitionMatrix as tm

C_Vals = [[[0.75, 0.25], [0.0, 1.0]], [[0.75, 0.25], [0.0, 1.0]]]
C_Set = tm.TransitionMatrixSet(values=C_Vals, temporal_type='Incremental')

A = tm.TransitionMatrix(values=[[0.6, 0.2, 0.2], [0.2, 0.6, 0.2], [0.2, 0.2, 0.6]])
A_Set = tm.TransitionMatrixSet(values=A, periods=3, method='Copy', temporal_type='Incremental')
B_Set = tm.TransitionMatrixSet(values=A, periods=3, method='Power', temporal_type='Cumulative')

print(A_Set.validate())
print(B_Set.validate())
print(C_Set.validate())

A_Set.cumulate()
A_Set.incremental()
