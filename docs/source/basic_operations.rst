Basic Operations
========================
The core TransitionMatrix object implements a typical (one period) transition matrix. It supports a variety of operations (more details are documented in the API section)

- Initialize a matrix (from data, predefined matrices, TODO random etc)
- Validate a matrix
- Attempt to fix a matrix
- Compute generators, powers etc.
- Output to json/csv formats

.. note:: All standard numerical matrix operations are available as per the numpy API.

Single Matrix Operation Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: matrix_operations.py

Maybe the best point to get started as it contains simple single matrix examples


Empirical Transition Matrix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: empirical_transition_matrix.py

Example workflows using transitionMatrix to estimate an empirical transition matrix from duration type data
The datasets are produced in examples/generate_synthetic_data.py This example uses the
`Aalen-Johansen estimator <https://www.openriskmanual.org/wiki/Aalen-Johansen_Estimator>`_

Plot of estimated transition probabilities

.. image:: ../../examples/transition_probabilities.png


Estimate Matrix from Cohort Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: matrix_from_cohort_data.py

Example workflows using transitionMatrix to estimate a transition matrix from data that are already grouped in cohorts


Matrix from Duration Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: matrix_from_duration_data.py

Example workflows using transitionMatrix to estimate a transition matrix from data that are in duration format. The datasets are first grouped in period cohorts


