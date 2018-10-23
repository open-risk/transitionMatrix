transitionMatrix.portfolio_model_lib subpackage
===============================================


Portfolio Models Library
----------------------------------------------

A simple python library that provides semi-analytical functions useful for testing the accuracy of credit portfolio simulation models
The basic formulas are reasonably simple and well known: They underpin the calculation of RWA (risk weighted assets), and in turn required capital, thus ensuring stability for the entire banking systems worldwide

The library provides support for the Monte Carlo testing framework

Dependencies: scipy, sympy

Examples
---------

Check the jupyter notebooks and python scripts

Current Functions
-----------------

* vasicek_base
* vasicek_base_el
* vasicek_base_ul
* vasicek_lim
* vasicek_lim_el
* vasicek_lim_ul
* vasicek_lim_q

The Vasicek Base family produces finite pool loss probabilities and measures (EL, UL)

The Vasicek Lim family produces asymptotic pool loss probabities and measures (EL, UL, Quantile)


Todo List
---------

Provide additional functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Complete the universe of analytic solutions for Gaussian models
  * Include some interesting special cases (e.g., large pool + single exposure)
  * Include some tractable inhomogeneous problems
* Calculate more statistical moments (e.g., skew, kurtosis)
* Expand to non-Gaussian distributions

Make a more robust implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The functions should ultimately be coded to a high standard of robustness:
* input validation
* exception handling
* controlled accuracy

The idea would be to follow best practises from some of the more mainstream python mathematical libraries


.. automodule:: transitionMatrix.portfolio_model_lib
    :members:
    :undoc-members:
    :show-inheritance:
