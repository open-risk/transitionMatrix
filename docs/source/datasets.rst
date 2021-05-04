Datasets
===================

The transitionMatrix distribution includes a number of datasets to support testing / training objectives. Datasets come in two main types:

* State Transition Data (used in estimation). There are both dummy (synthetic) examples and some actual data. Transition data are usually in CSV format.
* Transition Matrices and Multi-period Sets of matrices (again both dummy and actual examples). Transition matrices are usually in JSON format.

State Transition Data
-------------------------------------------

The scripts are located in examples/python. For testing purposes all examples can be run using the run_examples.py script located in the root directory. Some scripts have an example flag that selects alternative input data or estimators.

.. csv-table:: List of Transition Datasets
   :header-rows: 1
   :widths: 15 5 5 5 5 15 50
   :file: ../../datasets/dataset_list.csv


Transition Matrices
--------------------------------------------

* generic_monthly
* generic_multiperiod
* JLT
* sp 2017

