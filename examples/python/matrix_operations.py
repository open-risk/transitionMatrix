# encoding: utf-8

# (c) 2017-2021 Open Risk, all rights reserved
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
Examples using transitionMatrix to perform various transition matrix operations.

"""

import numpy as np
from scipy.linalg import expm

import transitionMatrix as tm
from transitionMatrix.creditratings.predefined import JLT, SP02NR
from transitionMatrix import dataset_path

print("> Initialize a 3x3 matrix with values")
A = tm.TransitionMatrix(values=[[0.6, 0.2, 0.2], [0.2, 0.6, 0.2], [0.2, 0.2, 0.6]])
print(A)
A.print_matrix(format_type='Standard', accuracy=2)
A.print_matrix(format_type='Percent', accuracy=1)

print("> Initialize a generic matrix of dimension n")
B = tm.TransitionMatrix(dimension=4)
print(B)

print("> Any list can be used for initialization (but not all shapes are valid transition matrices!)")
C = tm.TransitionMatrix(values=[1.0, 3.0])
print(C)

print("> Any numpy array can be used for initialization (but not all are valid transition matrices!)")
D = tm.TransitionMatrix(values=np.identity(5))
print(D)

print("> Values can be loaded from json or csv files")
F = tm.TransitionMatrix(json_file=dataset_path + "JLT.json")
print(F)

print("> Validate that a matrix satisfies probability matrix properties")
print(A.validate())
print(B.validate())
print(C.validate())
print(D.validate())
print(F.validate())

print("> All the numpy.matrix / ndarray functionality is available")
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

print("> Multiplying all elements of a matrix by a scalar")
print(0.01 * A)

print("> Transition Matrix algebra is very intuitive")
print(A * A)
print(A ** 2)
print(A ** 10)

print("> Lets fix the invalid matrix C")
# numpy operations that return numpy arrays can be used as follows:
C = tm.TransitionMatrix(values=np.resize(C, (2, 2)))
C[0, 1] = 0.0
C[1, 0] = 0.0
C[1, 1] = 1.0
print(C.validate())

print("> Computing the generator of a transition matrix")
# Generator of A
G = A.generator()
print(A, expm(G))

print("> Transition matrices properties can be analyzed")
print(A.characterize())

print("> Lets look at a realistic example from the JLT paper")
# Reproduce JLT Generator
# We load it using different sources
E = tm.TransitionMatrix(values=JLT)
E_2 = tm.TransitionMatrix(json_file=dataset_path + "JLT.json")
E_3 = tm.TransitionMatrix(csv_file=dataset_path + "JLT.csv")
# Lets check there are no errors
Error = E - E_3
print(np.linalg.norm(Error))
print("> Lets look at validation and generators")
# Empirical matrices will not satisfy constraints exactly
print(E.validate(accuracy=1e-3))
print(E.characterize())
print(E.generator())
Error = E - expm(E.generator())
# Frobenious norm
print(np.linalg.norm(Error))
# L1 norm
print(np.linalg.norm(Error, 1))

print("> Use pandas style API for saving to files")
E.to_csv("JLT.csv")
E.to_json("JLT.json")


def main():
    print("Done")


if __name__ == "__main__":
    main()