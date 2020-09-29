Multi-Period Transitions
========================

transitionMatrix adopts a multi-period data storage paradigm that is more general than a Markov-Chain framework.

The TransitionMatrixSet object stores a family of TransitionMatrix objects as a time ordered list. Besides
    storage this allows a variety of simultaneous operations on the collection of matrices

There are two basic representations of the a multi-period set of transitions:

- The first (cumulative form) is the most fundamental. Each successive (k-th) element stores transition rates from an initial time to timepoint k. This could be for example the input of an empirical transition matrix dataset
- In the second (incremental form) successive elements store transition rates from timepoint k-1 to timepoint k.

TransitionMatrixSet allows converting between the two representations


Matrix *Set* Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: matrix_set_operations.py

Contains examples using transitionMatrix to perform various transition matrix **set** operations (Multi-period measurement context)


Default Curves
--------------

Absorbing states (in credit risk context a borrower default) are particularly important therefore some specific functionality to isolate the corresponding default rate *curve*. (See Also the CreditCurve object)

