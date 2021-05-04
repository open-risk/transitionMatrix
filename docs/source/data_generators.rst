Data Generators
===================

The transitionMatrix distribution includes a number of data generators to support testing / training objectives.

* **exponential_transitions**: Generate continuous time events from exponential distribution and uniform sampling from state space. Suitable for testing cohorting algorithms and duration based estimators.
* **markov_chain**: Generate discrete events from a markov chain matrix in Compact data format. Suitable for testing cohort based estimators
* **long_format**: Generate continuous events from a markov chain matrix in Long data format. Suitable for testing duration based estimators
* **portfolio_lables**: Generate a collection of credit rating states emulating a snapshot of portfolio data. Suitable for mappings and transformations of credit rating states


.. note:: Do not confuse *data generators* with *matrix generators*

Data Generation Examples
-------------------------

All data data generation examples are in script examples/python/generate_synthetic_data.py
