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

# Example script. Open Risk Academy Course Step 1.

import transitionMatrix as tm
import numpy as np
from scipy.linalg import expm
from transitionMatrix.predefined import JLT
from transitionMatrix import dataset_path

A = tm.TransitionMatrix(values=[[0.6, 0.2, 0.2], [0.2, 0.6, 0.2], [0.2, 0.2, 0.6]])
B = tm.TransitionMatrix(dimension=4)
C = tm.TransitionMatrix(values=[1.0, 3.0])
F = tm.TransitionMatrix(json_file=dataset_path + "JLT.json")
F.to_csv("JLT.csv")

print(A.validate())
print(B.validate())
print(C.validate())
print(F.validate())

C = tm.TransitionMatrix(values=np.resize(C, (2, 2)))
C[0, 1] = 0.0
C[1, 0] = 0.0
C[1, 1] = 1.0

E = tm.TransitionMatrix(values=[[0.75, 0.25], [0.0, 1.0]])
print(E.validate())
# ATTRIBUTES
# Getting matrix info (dimensions, shape)
print(E.ndim)
print(E.shape)
# Obtain the matrix transpose
print(E.T)
# Obtain the matrix inverse
print(E.I)
# Summation methods:
# - along columns
print(E.sum(0))
# - along rows
print(E.sum(1))

print(A * A)
print(A ** 2)
print(A ** 10)

G = A.generator()
print(A, expm(G))

A.characterize()

# Load and validate the matrix
E = tm.TransitionMatrix(values=JLT)
print(E.validate(accuracy=1e-3))
print(E.characterize())
print("-- Lets look at generators")
# Empirical matrices will not satisfy constraints exactly
print(E.generator())
Error = E - expm(E.generator())
# Frobenious norm
print(np.linalg.norm(Error))
# L1 norm
print(np.linalg.norm(Error, 1))
