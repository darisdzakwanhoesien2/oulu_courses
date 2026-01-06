# Documentation for MATLAB Scripts in Statistical_Signal Processing_1_MATLAB_Daris_4

This document summarizes the MATLAB scripts found in the folder `Statistical_Signal Processing_1_MATLAB_Daris_4`.

---

## 1. estimator.m

### Overview

This script performs a Monte Carlo simulation to estimate the parameter \( \theta \) of a uniform distribution \( U[0, \theta] \) using two estimators:

- Maximum Likelihood Estimator (MLE): \( \hat{\theta}_{MLE} = \max(X) \)
- Mean-based estimator: \( \hat{\theta}_{mean} = 2 \times \text{mean}(X) \)

### Contents

- Defines the number of Monte Carlo simulations and sample size.
- Generates random samples from \( U[0, \theta] \).
- Computes both estimators for each simulation.
- Calculates and prints the mean of both estimators over all simulations.

---

## 2. monte_carlo_simulation.m

### Overview

This script performs Monte Carlo simulations to analyze the mean and variance of a random variable with different correlation coefficients \( \rho \).

### Contents

- Defines parameters including amplitude \( A \), noise variance \( \sigma^2 \), number of simulations, and correlation values.
- For each \( \rho \), generates correlated Gaussian noise samples.
- Computes the mean of the noisy samples.
- Calculates simulated means and variances and compares them with theoretical values.
- Prints a summary table of results.

---

# Summary

These MATLAB scripts provide practical examples of Monte Carlo simulations in statistical signal processing, focusing on parameter estimation and the effect of correlation on statistical properties.
