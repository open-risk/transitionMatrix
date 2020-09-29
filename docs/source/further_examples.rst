Further Usage Examples
======================

The examples directory includes both **standalone python scripts** and **jupyter notebooks** to help you get started. (NB: Currently there are more scripts than notebooks). A selection of topics covered:

- Manipulating transition matrices
- Generating transition matrices from data (using various estimators)
- Computing and visualizing credit curves corresponding to a set of transition matrices
- Mapping rating states between different rating systems

Python Scripts
-------------------------------------------

The scripts are located in examples/python (For testing purposes all examples can be run using the run_examples.py script located in the root directory)


Adjust NR (Not Rated) States
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: adjust_nr_states.py

Example of using transitionMatrix to adjust the (not-rated) NR state. Input data are the Standard
and Poor's historical data (1981 - 2016) for corporate credit rating migrations. Example of handling
`right censoring issues <https://www.openriskmanual.org/wiki/Withdrawn_Ratings>`_

Fix a Multi-period Matrix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: fix_multiperiod_matrix.py

Example of using transitionMatrix to detect and solve various pathologies that might be affecting transition
matrix data

Generate a Full Multi-period Set
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: generate_full_multiperiod_set.py

Example of using the transitionMatrix generator methods to generate a full multi-period matrix set
The input data are processed Standard and Poor's matrices for a selection of cumulative observation points
NB: This example requires a substantial amount of custom code!

Generate Synthetic Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: generate_synthetic_data.py

Example workflows using transitionMatrix to generate synthetic data.
(Edit the dataset selector to switch between examples)

The first set of examples produce "duration" type data. Estimating transitions
for duration data is done directly with duration type estimators or after
cohorting (binning) the data for cohort (frequency) type estimators.

The subsequent set of examples produce cohort type data using markov chain simulation


Matrix from LendingClub Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: matrix_lendingclub.py
* Script: matrix_set_lendingclub.py

Example workflows using transitionMatrix to estimate a matrix from LendingClub data
Input data are in a special cohort format as the published datasets have some limitations


Jupyter Notebooks
-------------------------------------------

* Adjust_NotRated_State.ipynb
* Matrix_Operations.ipynb
* Monthly_from_Annual.ipynb

Open Risk Academy Scripts
-------------------------------------------
