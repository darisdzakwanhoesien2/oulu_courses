# Machine Vision Exercises and Analysis

## Overview
This folder contains exercises and analysis related to fundamental concepts in machine vision and image processing. The main focus is on understanding convolution operations, spatial moments, and related matrix computations through practical coding exercises.

Additionally, the folder includes a comprehensive collection of study materials under the `Machine Vision Concept` directory. This directory contains lecture notes, quizzes, mid-term exercises, and reference books covering a wide range of machine vision topics such as imaging, light and color, binary image analysis, texture analysis, local features, recognition, motion, 2D and 3D vision, and more.

The `Machine Vision Concept` directory is organized as follows:

- **Quizzes:** Covering topics including imaging, light and color, binary image analysis, texture analysis, local features, recognition, motion, 2D models and transformations, depth, and 3D vision.
- **Mid-term Exercises:** Two mid-term folders containing exercises with questions and detailed solutions for exam preparation.
- **Reference Books:** PDFs of leading computer vision textbooks by Richard Szeliski, Linda Shapiro, and Forsyth & Ponce.

## Contents
- `machine_vision.ipynb`: Jupyter notebook containing detailed exercises on convolution with and without padding, sliding summation, spatial moments calculation, and matrix operations. The notebook includes code examples, explanations, and results for each exercise.
- `questions.csv`: A CSV file containing questions or data related to the exercises in the notebook.
- `Machine Vision Concept/`: Directory containing extensive machine vision study materials including lecture PDFs, quizzes, mid-term exam exercises and solutions, and reference books by leading authors in the field.
- `supplementary/`: A subfolder that may contain additional resources, data, or supporting files for the exercises.
- `Programming Assignment/`: Folder containing programming assignments A1 through A8 covering topics such as Imaging, Color, Segmentation, Texture, Recognition, Motion, Hough Transform, and Triangulation. Each assignment includes Jupyter notebooks, images, and detailed instructions.

## Programming Assignments Summary

### Assignment 1 – Imaging
This assignment involves reading and displaying images, simulating a synthetic Bokeh effect using depth maps and the thin-lens model, and applying a vignetting effect to create brightness fall-off near image edges. The tasks include image processing using OpenCV and visualization with Matplotlib.

### Assignment 2 – Color
This assignment explores white balance correction using the gray world assumption, color transformations, and visualization of color distributions in the CIELAB color space through 2D scatter plots. The goal is to correct color casts and analyze the effects of white balancing.

### Assignment 3 – Binary Image Analysis
This assignment focuses on image segmentation to separate puzzle pieces from the background using Otsu's method for automatic thresholding, morphological operations for noise reduction, connected component labeling, and contour extraction. It also includes removal of small unwanted objects based on contour area.

### Assignment 4 – Texture
This assignment covers face recognition using texture analysis. It includes computing grayscale histograms, applying filter banks (Gabor filters), calculating Local Binary Patterns (LBP) and patch-based LBP histograms, and evaluating classification performance with confusion matrices.

### Assignment 5 – Recognition
This assignment involves classifying apples and pears using shape (eccentricity) and color (hue) features. It implements nearest centroid classification with Euclidean distance, visualization of test data and decision boundaries, and classification using Mahalanobis distance for improved accuracy.

### Assignments 6 to 8
Folders for assignments 6 (Motion), 7 (Hough), and 8 (Triangulation) are present but currently empty.

## Exercises Covered
- Implementing convolution operations on binary matrices with and without zero-padding.
- Calculating spatial moments and centroids of binary images.
- Performing sliding summation with kernels.
- Understanding and visualizing matrix transformations relevant to image processing.

## Usage
1. Ensure you have Python 3.x installed with the following packages:
   ```
   pip install numpy pandas matplotlib
   ```
2. Open and run the `machine_vision.ipynb` notebook in a Jupyter environment to explore the exercises and their solutions.
3. Refer to `questions.csv` for related questions or data inputs used in the exercises.
4. Explore the `Machine Vision Concept/` directory for comprehensive study materials to deepen your understanding of machine vision topics.

## Dependencies
- Python 3.x
- numpy
- pandas
- matplotlib

## Next Steps
- Extend the exercises to include more advanced image processing techniques such as edge detection, filtering, and feature extraction.
- Integrate visualization tools to better illustrate the effects of convolution and spatial moment calculations.
- Apply these concepts to real-world image datasets for practical machine vision applications.
- Utilize the extensive materials in the `Machine Vision Concept/` directory for further study and exam preparation.

---

This README provides a guide to the machine vision exercises, resources, and study materials contained in this folder.
