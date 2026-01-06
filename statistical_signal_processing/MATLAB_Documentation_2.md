# Documentation for MATLAB Scripts in Statistical_Signal Processing_1_MATLAB_Daris_2

This document summarizes the MATLAB scripts found in the folder `Statistical_Signal Processing_1_MATLAB_Daris_2`.

---

## 1. gaussian_distribution.m

- Generates two Gaussian random variables \( x \sim \mathcal{N}(0,1) \) and \( y \sim \mathcal{N}(0.5, 2) \) with 500 samples each.
- Computes their sum \( z = x + y \).
- Calculates sample mean and variance of \( z \) and compares with theoretical values.
- Plots a histogram of \( z \) with the theoretical probability density function (PDF) overlay.

---

## 2. gaussian_white.m

- Defines a 2x2 covariance matrix \( \Sigma \).
- Generates white Gaussian noise samples.
- Uses Cholesky decomposition of \( \Sigma \) to create correlated Gaussian samples.
- Computes and compares the sample covariance matrix with the original \( \Sigma \).

---

## 3. probability_density_function.m

- Generates samples from a uniform distribution between \( a = -1 \) and \( b = 5 \).
- Plots a histogram of the samples normalized as a PDF.
- Overlays the theoretical uniform PDF.
- Prints sample mean and variance compared to expected values.

---

## 4. svd_frobenius.m

- Generates a complex random matrix \( A \) with specified mean and variance.
- Computes the singular value decomposition (SVD) of \( A \).
- Reconstructs \( A \) from its SVD components.
- Calculates the Frobenius norm of the difference between \( A \) and its reconstruction to verify accuracy.

---

# Summary

These MATLAB scripts provide practical examples of statistical signal processing concepts including Gaussian distributions, covariance matrix manipulation, probability density functions, and matrix decompositions.
