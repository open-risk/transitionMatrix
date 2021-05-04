Basic Operations
========================
The core TransitionMatrix object implements a typical (one period) transition matrix. It supports a variety of operations (more details are documented in the API section)

- Initialize a matrix (from data, predefined matrices etc)
- Validate a matrix
- Attempt to fix a matrix
- Compute generators, powers etc.
- Print a matrix
- Output to json/csv/xlsx formats
- Output to html format


Simple Operation Examples
----------------------------------------

.. note:: The script examples/python/matrix_operations.py contains the below and plenty more simple single matrix examples


Initialize a matrix with values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a growing list of ways to initialize a transition matrix

* Initialize a generic matrix of dimension n
* Any list can be used for initialization (but not all shapes are valid transition matrices!)
* Any numpy array can be used for initialization (but not all are valid transition matrices!)
* Values can be loaded from json or csv files
* The transitionMatrix.creditratings.predefined module includes a number of predefined matrices


.. code::

    A = tm.TransitionMatrix(values=[[0.6, 0.2, 0.2], [0.2, 0.6, 0.2], [0.2, 0.2, 0.6]])
    print(A)
    A.print_matrix(format_type='Standard', accuracy=2)

    [[0.6 0.2 0.2]
     [0.2 0.6 0.2]
     [0.2 0.2 0.6]]

    0.60 0.20 0.20
    0.20 0.60 0.20
    0.20 0.20 0.60

    A.print_matrix(format_type='Standard', accuracy=2)

    60.0% 20.0% 20.0%
    20.0% 60.0% 20.0%
    20.0% 20.0% 60.0%

Both the intrinsic print function and the specific print_matrix will print you the matrix, but the print_matrix method clearly aims to present the values in a more legible formats.


General Matrix Algebra
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. note:: All standard numerical matrix operations are available as per the numpy API.

Some example operations that leverage the underlying numpy API:

.. code::

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
    # Multiplying all elements of a matrix by a scalar
    print(0.01 * A)
    # Transition Matrix algebra is very intuitive
    print(A * A)
    print(A ** 2)
    print(A ** 10)


Validating, Fixing and Characterizing a matrix
-----------------------------------------------------------

Validate a Matrix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The validate() method of the object checks for required properties of a valid transition matrix:

    1. check squareness
    2. check that all values are probabilities (between 0 and 1)
    3. check that all rows sum to one

.. code::

    C = tm.TransitionMatrix(values=[1.0, 3.0])
    print(C.validate())

    [('Matrix Dimensions Differ: ', (1, 2))]


Characterise a Matrix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The characterise() method attempts to characterise a matrix

    1. diagonal dominance