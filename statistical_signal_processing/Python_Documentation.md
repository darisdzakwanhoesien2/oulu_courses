# Documentation for Python Notebooks in Statistical Signal Processing

This document provides detailed explanations and summaries of the Python notebooks found in the `statistical_signal_processing/Python` directory.

---

## 1. joint_pdf.ipynb

### Overview

This notebook defines a joint probability density function (PDF) for two random variables \( Y_1 \) and \( Y_2 \) with the following properties:

- The joint PDF is nonzero only when \( y_1 > 0 \) and \( 0 < y_2 < 1 \).
- The PDF is given by \( f_{Y_1,Y_2}(y_1, y_2) = y_1 e^{-y_1} \) in the valid region.

### Contents

- **Function Definition:** Implements the joint PDF function with conditional checks.
- **Grid Creation:** Generates a mesh grid for \( y_1 \) and \( y_2 \) over specified ranges.
- **Visualization:**
  - Heatmap of the PDF values.
  - Contour plot overlay on the heatmap.
  - 3D surface plot showing the shape of the PDF.
- **Integration Example:** Demonstrates double integration over a unit square using `scipy.integrate.dblquad`.
- **3D Surface Plot:** Visualizes a constant function over the unit square for illustration.

### Usage Notes

- The notebook is useful for understanding joint distributions and visualizing PDFs.
- The integration examples help in understanding numerical integration in two dimensions.

---

## 2. projection_matrix.ipynb

### Overview

This notebook demonstrates the computation of the best approximation (projection) of a vector onto the span of two other vectors using symbolic mathematics with the `sympy` library.

### Contents

- **Projection Calculation:**
  - Uses the formula for projection onto two vectors.
  - Computes the projection matrix \( P = U (U^T U)^{-1} U^T \).
  - Projects vector \( v \) onto the span of \( u_1 \) and \( u_2 \).
- **JSON Export Functions:** (Commented out)
  - Functions to save the input, intermediate steps, and results in JSON format.
- **Symbolic Computation:**
  - Uses `sympy` matrices and symbolic operations.
  - Prints the projection matrix and projection vector.
- **Example Vectors:**
  - Demonstrates with example vectors \( v = [-1, 5, 3] \), \( u_1 = [-1, 1, 1] \), and \( u_2 = [-1, -2, 1] \).

### Usage Notes

- The notebook is useful for learning projection concepts in linear algebra.
- Symbolic computation allows for exact mathematical expressions.
- JSON export functions can be enabled for saving results programmatically.

---

# Summary

These notebooks provide foundational examples in statistical signal processing, focusing on probability distributions and linear algebraic projections. They combine numerical and symbolic computation with visualization to aid understanding.
