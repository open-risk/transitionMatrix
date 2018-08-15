## Portfolio Models

A simple python library that provides semi-analytical functions useful for testing the accuracy of credit portfolio simulation models
The basic formulas are reasonably simple and well known: They underpin the calculation of RWA (risk weighted assets), and in turn required capital, thus ensuring stability for the entire banking systems worldwide

The library provides support for the Monte Carlo testing framework

Dependencies: scipy, sympy

## Examples
Check the jupyter notebook

### Current Functions

* vasicek_base
* vasicek_base_el
* vasicek_base_ul
* vasicek_lim
* vasicek_lim_el
* vasicek_lim_ul
* vasicek_lim_q

The Vasicek Base family produces finite pool loss probabilities and measures (EL, UL)

The Vasicek Lim family produces asymptotic pool loss probabities and measures (EL, UL, Quantile)

### Risk Manual
Use the [manual](http://www.openriskmanual.org) for documentation and use cases

### Contributions
Contributions are welcome. Check the TODO list for ideas of where to take this library next
