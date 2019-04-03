# encoding: utf-8

# (c) 2017-2019 Open Risk, all rights reserved
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


""" Example of using transitionMatrix to detect and solve various pathologies that might be affecting transition
matrix data

"""

import transitionMatrix as tm
import numpy as np
from transitionMatrix import dataset_path

print("> Loading historical multi-period transitional matrices (cumulative mode) from csv file")
SnP_Set0 = tm.TransitionMatrixSet(csv_file=dataset_path + "sp_1981-2016.csv", temporal_type='Cumulative')
print("> Validate")
print(SnP_Set0.validate())
print(
    "> We detect dimensionality problems. The matrices are not square (missing the trivial Default and NR transitions)")
print("> We must fix that to proceed. Augment matrices in set by fixing Default and NR transitions")
C_Vals = []
for matrix in SnP_Set0.entries:
    C = tm.TransitionMatrix(values=np.resize(matrix, (9, 9)))
    # set the migration from NR or D state to a rated state to zero
    C[7, 0:9] = 0.0
    C[8, 0:9] = 0.0
    # set the probability of remaining to a D state to unity
    C[7, 7] = 100.0
    # set the probability of remaining to an NR state to unity
    C[8, 8] = 100.0
    C_Vals.append(C)
SnP_Set1 = tm.TransitionMatrixSet(values=C_Vals)
print("> Validate Again")
print(SnP_Set1.validate())

print("> Now we have square matrices but the format is not in probabilities!")
print("> Divide all entries by 100")

SnP_Set2 = SnP_Set1 * 0.01
# SnP_Set2.print()
print("> Validate Again")
print(SnP_Set2.validate())

print("> Hurrah, we have a probability matrix set. Lets save it")

SnP_Set2.to_json(dataset_path + 'sp_1981-2016.json', accuracy=5)
