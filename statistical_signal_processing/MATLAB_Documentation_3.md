# Documentation for MATLAB Scripts in Statistical_Signal Processing_1_MATLAB_Daris_3

This document summarizes the MATLAB script found in the folder `Statistical_Signal Processing_1_MATLAB_Daris_3`.

---

## 1. mvue_zero_mean_white_gaussian_noise_variance.m

### Overview

This script performs a Monte Carlo simulation to estimate a parameter \( \theta \) in the presence of zero-mean white Gaussian noise with variance \( \sigma^2 \).

### Contents

- Defines parameters including number of Monte Carlo loops, sample size, noise variance, and true parameter value.
- Calculates the Cramer-Rao Lower Bound (CRLB) for the estimator variance.
- Runs Monte Carlo simulations to generate noisy data and estimate \( \theta \).
- Computes mean and variance of the estimator.
- Plots a histogram of the estimated \( \theta \) values with the theoretical PDF overlay.
- Displays simulation results including estimator mean, variance, CRLB, and efficiency.
- Analyzes CRLB behavior for different sample sizes \( N \) and plots CRLB vs. \( N \) on a logarithmic scale.

### Usage Notes

- Useful for understanding parameter estimation under noise.
- Demonstrates the efficiency of the minimum variance unbiased estimator (MVUE).
- Visualizes the relationship between sample size and estimator variance bound.

---

# Summary

This MATLAB script provides a practical example of statistical signal processing concepts related to parameter estimation, noise, and theoretical bounds on estimator performance.
