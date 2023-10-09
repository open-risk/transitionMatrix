Credit Curves
========================

A Credit Curve denotes a grouping of credit risk metrics (parameters) that provide estimates that a legal entity experiences a Credit Event over different (an increasing sequence of longer) time periods. `See Credit Curves <https://www.openriskmanual.org/wiki/Category:Credit_Curve>`_

A multi-period matrix and a credit curve are closely related objects (under some circumstances the later can be thought of as a subset of the former). The transitionMatrix package offers the following main functionality concerning credit curves:

* The :class:`transitionMatrix.creditratings.creditcurve.CreditCurve` class for storing and working with credit curves
* The :meth:`transitionMatrix.model.TransitionMatrixSet.default_curves` transitionMatrixSet method that extracts from a matrix set the default curve


Example: Calculate and Plot Credit Curves
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example of using transitionMatrix to calculate and visualize multi-period

* Script: examples/python/credit_curves.py

.. image:: ../../examples/credit_curves.png