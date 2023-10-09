Testing
==================

Testing transitionMatrix has two major components:

* normal code testing aiming to certify the correctness of code execution
* algorithm testing aiming to validate the correctness of algorithmic implementation

.. note:: In general algorithmic testing is not as precise as code testing and may be more subject to uncertainties such as numerical accuracy. To make those tests as revealing as possible transitionMatrix implements a number of standardized *round-trip tests*:

  * starting with a matrix
  * generating compatible data
  * estimate a matrix from the data
  * comparing the values of input and estimated matrices

Running all the examples
------------------------
Running all the examples is a quick way to check that everything is installed properly, all paths are defined etc. At the root of the distribution:

.. code:: bash

    python3 run_examples.py


The file simply iterates and executes a standalone list of :ref:`Usage Examples`.

.. code:: python

    filelist = ['adjust_nr_state', 'credit_curves', 'empirical_transition_matrix', 'fix_multiperiod_matrix', 'generate_synthetic_data', 'generate_visuals', 'matrix_from_cohort_data', 'matrix_from_duration_data', 'matrix_lendingclub', 'matrix_set_lendingclub', 'matrix_operations', 'matrix_set_operations']

.. warning:: The script might generate a number of files / images at random places within the distribution


Test Suite
-------------
The testing framework is based on unittest. Before you get started and depending on how you obtained / installed the library check:

- If required adjust the source directory path in transitionMatrix/__init__
- Unzip the data files in the datasets directory

Then run all tests

.. code:: bash

    python3 test.py

For an individual test:

.. code:: bash

    pytest tests/test_TESTNAME.py


