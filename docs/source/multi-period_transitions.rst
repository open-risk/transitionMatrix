Multi-Period Transitions
========================

Th transitionMatrix package adopts a *multi-period paradigm* that is more general than a Markov-Chain framework that imposes the Markov assumption over successive periods. In this direction, the **TransitionMatrixSet object** stores a family of TransitionMatrix objects as a time ordered list. Besides basic storage this structure allows a variety of simultaneous operations on the collection of related matrices

There are two basic representations of the a multi-period set of transitions:

- The first (*cumulative form*) is the most fundamental. Each successive (k-th) element stores transition rates from an initial time to timepoint k. This could be for example the input of an empirical transition matrix dataset
- In the second (*incremental form*) successive elements store transition rates from timepoint k-1 to timepoint k.

The TransitionMatrixSet class allows converting between the two representations


Matrix *Set* Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: matrix_set_operations.py

Contains examples using transitionMatrix to perform various transition matrix **set** operations (Multi-period measurement context)


Default Curves
--------------

Absorbing states (in credit risk context a borrower default) are particularly important therefore some specific functionality to isolate the corresponding default rate *curve*. (See Also the CreditCurve object)

