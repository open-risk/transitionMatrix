Estimation
========================
The estimation of a transition matrix is one of the core functionalities of transitionMatrix. Several methods and variations are available in the literature depending on aspects such as:

* The nature of the observations / data (e.g., whether temporal homogeneity is a valid assumption)
* Whether or not there are competing risk effects
* Whether or not observations have coincident values
* Treating the Right-Censorship of observations (Outcomes beyond the observation window)
* Treating the Left-Truncation of observations (Outcomes prior to the the observation window)

Estimator Types
----------------
* **Cohort Based Methods** that group observations in cohorts
* **Duration** (also Hazard Rate or Intensity) Based Methods that utilize the actual duration of each state



The main estimators currently implemented are as follows:


.. toctree::
   :maxdepth: 1
   :caption: Implemented Estimators

   simple_estimator
   cohort_estimator
   aalen-johansen_estimator


Whichever the estimator choice, the outcome of the estimation is an *Empirical Transition Matrix* (or potentially a matrix set)

Implementation Notes
^^^^^^^^^^^^^^^^^^^^^^

* All estimators derive from the highest level *BaseEstimator* class.
* Duration type estimators derive from the *DurationEstimator* class


Estimation Examples
----------------------

The first example of estimating a transition matrix is covered in the :ref:`Getting Started` section. Here we have a few more examples:


Estimation Example 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example workflows using transitionMatrix to estimate an empirical transition matrix from duration type data. The datasets are produced using examples/generate_synthetic_data.py This example uses the
`Aalen-Johansen estimator <https://www.openriskmanual.org/wiki/Aalen-Johansen_Estimator>`_

* Script: examples/python/empirical_transition_matrix.py

By setting the example variable the script covers a number of variations:

* Version 1: Credit Rating Migration example
* Version 2: Simple 2x2 Matrix for testing
* Version 3: Credit Rating Migration example with timestamps in raw date format


Plot of estimated transition probabilities

.. image:: ../../examples/transition_probabilities.png

Estimation Example 2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example workflows using transitionMatrix to estimate a transition matrix from data that are in duration format. The datasets are first grouped in period cohorts

* Script: examples/python/matrix_from_duration_data.py








