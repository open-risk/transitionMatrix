ChangeLog
===========================

PLEASE NOTE THAT THE API IS STILL UNSTABLE AS MORE USE CASES / FEATURES ARE ADDED REGULARLY

v0.4.0 (23-10-2018)
-------------------

* Feature: Added Aalen-Johansen Duration Estimator
* Documentation: Major overhaul of documentation, now targeting ReadTheDocs distribution
* Training: Streamlining of all examples
* Installation: Pypi and wheel installation options
* Datasets: Synthetic Datasets in long format

v0.3.1 (21-09-2018)
-------------------

* Feature: Expanded functionality to compute and visualize credit curves

v0.3 (27-08-2018)
-------------------

* Feature: Addition of portfolio models (formerly portfolio_analytics_library) for data generation and testing
* Training: Added examples in jupyter notebook format

v0.2 (05-06-2018)
-------------------

* Feature: Addition of threshold generation algorithms

v0.1.3 (04-05-2018)
-------------------

* Documentation: Sphinx based documentation
* Training: Additional visualization examples

v0.1.2 (05-12-2017)
-------------------

* Refactoring dataset paths
* Bugfix: Correcting requirement dependencies (missing matplotlib)
* Documentation: More detailed instructions

v0.1.1 (03-12-2017)
-------------------

* Feature: TransitionMatrix model: new methods to merge States, fix problematic probability matrices, I/O API's
* Feature: TransitionMatrixSet mode: json and csv readers, methods for set-wise manipulations
* Datasets: Additional multiperiod datasets (Standard and Poors historical corporate rating transition rates)
* Feature: Enhanced matrix comparison functionality
* Training: Three additional example workflows
    * fixing multiperiod matrices (completing State Space)
    * adjusting matrices for withdrawn entries
    * generating full  multi-period sets from limited observations

v0.1.0 (11-11-2017)
-------------------

* First public release of the package