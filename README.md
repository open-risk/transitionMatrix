[![Documentation Status](https://readthedocs.org/projects/transitionmatrix/badge/?version=latest)](https://transitionmatrix.readthedocs.io/en/latest/?badge=latest)
![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/Naereen/badges.svg)](http://isitmaintained.com/project/Naereen/badges "Percentage of issues still open")


Intro
=========================
transitionMatrix is a Python powered library for the statistical analysis and visualization of state transition phenomena. It can be used to analyze any dataset that captures timestamped transitions in a discrete state space. Use cases include credit rating transitions, system state event logs etc. 

You can use transitionMatrix to

- Estimate transition matrices from historical event data using a variety of estimators
- Manipulate transition matrices (generators, comparisons etc.)
- Visualize event data and transition matrices
- Provide standardized data sets for testing
- Model transitions using threshold processes
- Map credit ratings using mapping tables between popularly used rating systems 

Key Information
================

* Author: [Open Risk](http://www.openriskmanagement.com)
* License: Apache 2.0
* Code Documentation: [Read The Docs](https://transitionmatrix.readthedocs.io/en/latest/index.html)
* Mathematical Documentation: [Open Risk Manual](https://www.openriskmanual.org/wiki/Transition_Matrix)
* Development website: [Github](https://github.com/open-risk/transitionMatrix)
* Project Chat: [Open Risk Commons](https://www.openriskcommons.org/c/open-source/transitionmatrix/15)

**NB: transitionMatrix is still in active development. If you encounter issues or have suggestions please raise them in our github repository or come discuss at our discourse server**

Support and Training
=========================

* The Open Risk Academy has free courses demonstrating the use of the library. The current list is: 
    * [Analysis of Credit Migration using Python TransitionMatrix](https://www.openriskacademy.com/course/view.php?id=38)
* Support for transitionMatrix and other open source libraries developed by [Open Risk](https://www.openriskmanagement.com) is available upon request


Examples
========

The [code documentation](https://transitionmatrix.readthedocs.io/en/latest/index.html) includes a large number of examples, jupyter notebooks and more. 


Plotting individual transition trajectories

![single entity](examples/single_entity.png)

Sampling transition data

![sampled histories](examples/sampled_histories.png)

Estimation of transition matrices using cohort methods

![estimation](examples/estimation.png)

Estimation of transition matrices using duration methods

![transition probabilities](examples/transition_probabilities.png)

Visualization of a transition matrix

![transition matrix](examples/TransitionMatrix.png)

Visualization using a Logarithmic Sankey diagram

![logarithmic sankey](examples/sankey.png)

Generating stochastic process transition thresholds

![thresholds](../portfolioAnalytics/examples/Thresholds.png)

Stressing Transition Matrices

![stressing transition matrices](../portfolioAnalytics/examples/stressed_density.png)

Computation and Visualization of Credit Curves

![credit curves](examples/credit_curves.png)

Working with credit states

![image](examples/scale_conversions.png)

