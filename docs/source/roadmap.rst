Roadmap
=========================

transitionMatrix is an ongoing project. Several significant extensions are already in the pipeline. transitionMatrix aims to become the most intuitive and versatile tool to analyse discrete transition data. The **Roadmap** lays out upcoming steps / milestones in this journey. The **Todo** list is a more granular collection of outstanding items.

You are welcome to contribute to the development of transitionMatrix by creating Issues or Pull Requests on the github repository. Feature requests, bug reports and any other issues are welcome to log at the `Github Repository <https://github.com/open-risk/transitionMatrix/issues>`_

Discussing general usage of the library is `happening here <https://www.openriskcommons.org/t/analysis-of-credit-migration-using-python-transitionmatrix/74>`_


0.5
--------------------------
The 0.5 will be the next major release (still considered alpha) that will be available e.g. on PyPI


0.4.X
--------------------------

The 0.4.X family of updates will focus on rounding out and (above all) documenting a number of functionalities already introduced


Todo List
=========================

A list of todo items, no triaging / prioritisation implied

Core Architecture and API
---------------------------------------------------

- Introduce exceptions / error handling throughout
- Solve numpy.matrix deprecation (implement equivalent API in terms of ndarray)
- Complete testing framework

Input Data Preprocessing
---------------------------------------------------

- Handing of markov chain transition formats (single entity)
- Native handling of Wide Data Formats (concrete data sets missing)
- Generalize cohorting algorithm to user specified function

Reference Data
---------------------------------------------------

- Additional credit rating scales (e.g short term ratings)
- Integration with credit rating ontology


Transition Matrix Analysis Functionality
---------------------------------------------------

- Further validation and characterisation of transition matrices (mobility indexes)
- Generate random matrix subject to constraints
- Fixing common problems encountered by empirically estimated transition matrices

Statistical Analysis Functionality
---------------------------------------------------

- Aalen Johansen Estimator
    - Covariance calculation
    - Various other improvements / tests
- Cohort Estimator
    - Read Data by labels
    - Edge cases
- Kaplan Meier Estimator NEW
    - (link to survival frameworks)
- Duration based methods
- Bootstrap based confidence intervals


State Space package
---------------------------------------------------

- Multiple absorbing states (competing risks)
- Automated coarsening of states (merging of similar)

Credit Rating Related
---------------------------------------------------
- Import data defined according to CRO ontology
- Absorbing State Identification, Competing Risks
- Compute hazard rates
- Characterize hazard rates


Utilities
---------------------------------------------------

- Continuous time data generation from arbitrary chain

Further Refactoring of packages
---------------------------------------------------

- Introduce visualization objects / API


Performance / Big data
---------------------------------------------------

- Handling very large data sets, moving away from in-memory processing


Documentation
---------------------------------------------------
- Sphinx documentation (complete)
- Expand the jupyter notebook collection to (at least) match the standalone scripts

Releases / Distribution
---------------------------------------------------

- Adopt regular github/PyPI release schedule
- Conda distribution

