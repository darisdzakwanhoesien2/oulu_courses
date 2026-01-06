# Statistical Signal Processing

This directory contains materials related to statistical signal processing, including Python notebooks and MATLAB scripts.

## Python Notebooks

### 1. joint_pdf.ipynb

This notebook defines and visualizes a joint probability density function (PDF) for two random variables \( Y_1 \) and \( Y_2 \). The joint PDF is defined as:

\[
f_{Y_1,Y_2}(y_1, y_2) = 
\begin{cases}
y_1 e^{-y_1}, & y_1 > 0 \text{ and } 0 < y_2 < 1 \\
0, & \text{otherwise}
\end{cases}
\]

The notebook includes:

- Implementation of the joint PDF function.
- Visualization of the PDF using heatmaps and contour plots.
- 3D surface plots to illustrate the PDF shape.
- Examples of double integration over a unit square to demonstrate integration concepts.
- 3D surface plots of constant functions for visualization purposes.

### 2. projection_matrix.ipynb

This notebook demonstrates the computation of the best approximation (projection) of a vector \( \mathbf{v} \) onto the span of two vectors \( \mathbf{u}_1 \) and \( \mathbf{u}_2 \) using symbolic mathematics with the `sympy` library.

Key features include:

- Calculation of projections using the formula:

\[
\text{proj}_{\mathbf{u}_1, \mathbf{u}_2}(\mathbf{v}) = \frac{\mathbf{v} \cdot \mathbf{u}_1}{\mathbf{u}_1 \cdot \mathbf{u}_1} \mathbf{u}_1 + \frac{\mathbf{v} \cdot \mathbf{u}_2}{\mathbf{u}_2 \cdot \mathbf{u}_2} \mathbf{u}_2
\]

- Computation of the projection matrix \( P = U (U^T U)^{-1} U^T \), where \( U \) is the matrix with columns \( \mathbf{u}_1 \) and \( \mathbf{u}_2 \).
- Projection of \( \mathbf{v} \) onto the span of \( \mathbf{u}_1 \) and \( \mathbf{u}_2 \) using the projection matrix.
- Functions to save the projection process and results in JSON format (commented out).
- Symbolic printing of matrices and projection results.

---

Further materials in MATLAB folders are available but not yet documented.
