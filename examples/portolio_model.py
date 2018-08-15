# coding: utf-8

# Finite portfolio with N credits - Calculate probability of k losses


import transitionMatrix.portfolio_models.model as vs

# Calculate the probability of four losses in a portfolio of ten credits when the PD is 0.1 and correlation is 20%


print("p=", vs.vasicek_base(10, 0, 0.34140, 0.2))
