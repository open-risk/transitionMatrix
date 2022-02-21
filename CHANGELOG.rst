ChangeLog
===========================

PLEASE NOTE THAT THE API OF TRANSITION MATRIX IS STILL UNSTABLE AS MORE USE CASES / FEATURES ARE ADDED REGULARLY

v0.5.0 (21-02-2022)
-------------------
* Installation:
    * Bump python dependency to 3.7
    * PyPI release update

v0.4.9 (04-05-2021)
-------------------

* Refactoring: All non-core functionality moved to separate directories/sub-packages
    * credit curve stuff moved to creditratings modules
    * data generators moved to generators modules
    * etc.
* Documentation: Major expansion (Still incomplete)
    * Expanded Data Formats
    * Rating Scales, CQS etc
    * Listing all datasets and examples
* Testing / Training: An interesting use case raised as issue #20
    * Added an end-to-end example of estimating a credit rating matrix from raw data
    * Includes various data preprocessing examples
* Datasets:
    * rating_data.csv (cleaned up credit data)
    * synthetic_data10.csv Credit Rating Migrations in Long Format / Compact Form (for testing)
    * deterministic generator (replicate given trajectories)
* Tests:
    * test_roundtrip.py testing via roundtriping methods


v0.4.8 (07-02-2021)
-------------------

* Documentation: Pulled all rst files in docs
* Refactoring: credit rating data moved into separate module


v0.4.7 (29-09-2020)
-------------------

* Documentation: Expanded and updated description of classes
* Documentation: Including Open Risk Academy code examples
* Feature: logarithmic sankey visualization

v0.4.6 (22-05-2019)
-------------------

* Feature: Update of CQS Mappings, addition of new rating scales
* Documentation: Documentation of rating scale structure and mappings
* Training: Example of mapping portfolio data to CQS

v0.4.5 (21-04-2019)
-------------------

* Training: Monthly_from_Annual.ipynb (a Jupyter notebook illustrating how to obtain interpolate transition rates on monthly intervals)
* Datasets: generic_monthly.json
* Feature: print_matrix function for generic matrix pretty printing
* Feature: matrix_exponent function for obtaining arbitrary integral matrices from a given generator

v0.4.4 (03-04-2019)
-------------------

* Documentation: Cleanup of docs following separation of threshold / portfolio models
* Datasets: generic_multiperiod.json
* Feature: CreditCurve class for holding credit curves


v0.4.3 (29-03-2019)
-------------------

* Refactoring: Significant rearrangement of code (the threshold models package moved to portfolioAnalytics for more consistent structure of the code base / functionality)

v0.4.2 (29-01-2019)
-------------------

* Feature: converter function in transitionMatrix.utils.converters to convert long form dataframes into canonical float form
* Datasets: synthetic_data9.csv (datetime in string format)
* Training: new data generator in examples/generate_synthetic_data.py to generate long format with string dates
* Training: Additional example (=3) in examples/empirical_transition_matrix.py to process long format with string dates
* Documentation: More detailed explanation of Long Data Formats with links to Open Risk Manual
* Documentation: Enabled sphinx.ext.autosectionlabel for easy internal links / removed duplicate labels

v0.4.1 (31-10-2018)
-------------------

* Feature: Added functionality for conditioning multi-period transition matrices
* Training: Example calculation and visualization of conditional matrices
* Datasets: State space description and CGS mappings for top-6 credit rating agencies


v0.4.0 (23-10-2018)
-------------------

* Installation: First PyPI and wheel installation options
* Feature: Added Aalen-Johansen Duration Estimator
* Documentation: Major overhaul of documentation, now targeting ReadTheDocs distribution
* Training: Streamlining of all examples
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

* Refactoring: Dataset paths
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