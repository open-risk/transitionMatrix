transitionMatrix
=================

| Description: A Python powered library for statistical analysis and visualization of state transition phenomena
| Author: Open Risk, http://www.openriskmanagement.com
| License: Apache 2.0
| Documentation: Open Risk Manual, http://www.openriskmanual.org/wiki/Transition_Matrix
| Training: Open Risk Academy, https://www.openriskacademy.com/login/index.php
| Development website: https://github.com/open-risk/transitionMatrix


Purpose of the project
=======================
transitionMatrix is a Python powered library for the statistical analysis and visualization of state transition phenomena.
It can be used to analyze any dataset that captures timestamped transitions in a discrete state space.
Use cases include credit rating transitions, system state event logs etc.


Functionality 
====================

you can use transitionMatrix to

- Estimate transition matrices from historical event data using a variety of estimators
- Visualize event data and transition matrices
- Manipulate transition matrices (generators, comparisons etc.)
- Provide standardized data sets for testing


Usage
=======================

Download the sources and issue:

.. code:: python

    python3 setup.py install

It is a good idea to run the testsuite. Before you get started:

- Adjust the source directory path in transitionMatrix/__init__ and then issue the following in at the root of the distribution
- Unzip the data files in the datasets directory

.. code:: python

    python3 test.py

Look at the examples directory for a variety of typical workflows

Training
=======================

- Analysis of Credit Migration using Python TransitionMatrix: https://www.openriskacademy.com/course/view.php?id=38


Dependencies
=======================

- TransitionMatrix is written in Python and depends on the key numerical and data processing Python libraries (Numpy, Scipy, Pandas)
- The Visualization API depends on Matplotlib
- The precise dependencies are listed in the requirements.txt file.
- TransitionMatrix may work with earlier versions of these packages but this has not been tested.

Relationship with other open source projects
============================================

- transitionMatrix does not aim to provide reference estimators or simulators of Markov Chain models (limited facilities might be included for convenience) but is focusing instead on relatively assumption free analysis
- transitionMatrix is somewhat similar to etm, an R package for estimating empirical transition matrices
- there is some conceptual overlap with survival models like lifelines, but in general the dimensionality of state space requires a different set of tools
