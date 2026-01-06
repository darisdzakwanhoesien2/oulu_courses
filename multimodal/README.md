# Multi-Modal Data Fusion Course (521161S)

This directory contains materials and exercises for the Multi-Modal Data Fusion course.

## Course Introduction

The course is hosted on JupyterHub provided by the IT Center for Science ([CSC](https://www.csc.fi/en/home)), which offers computing resources for running the exercises.

Please conduct yourselves appropriately while using the resources, as any misconduct will be addressed seriously.

Images used in the course materials are generated with DALL·E 2 AI using input text "Multimodal data fusion".

## Exercise Workflow

1. **Fetch the exercise**  
   Use the **Fetch** button under **Nbgrader -> Assignment List** in JupyterHub to download the exercise. Remember to save your work occasionally.

2. **Do the exercise**  
   Complete the exercises on time. Deadlines are available on the course [Moodle](https://moodle.oulu.fi/course/view.php?id=25414) page. Open exercises by clicking their names under Downloaded assignments in the Assignments tab.

3. **Submit the exercise**  
   Save your changes and submit the exercise from the Assignments tab by pressing the Submit button.

4. **Fetch feedback**  
   Grades are given in Moodle. To see comments on your work, fetch feedback from the Assignments tab under Submitted assignments by pressing the Fetch Feedback button when available.

## General Guidelines

- **Answer to the given variables**  
  Many exercises have variables labeled "Your answer here". Use these variables to provide your answers, which helps course staff in grading.

- **NotImplementedError**  
  This error indicates that code is required in the cell. Remove it when you provide your answer. Leave it if you do not want to answer the problem.

- **Shutdown unnecessary notebooks**  
  After finishing your work session, shut down notebooks to save computing resources. Save your changes before shutting down. Kernels are automatically terminated after 8 hours of inactivity.

---

The following sections will document each exercise notebook in detail.

## Exercise 1: Python tools and data fusion basics

This exercise introduces fundamental Python tools and concepts essential for multi-modal data fusion.

### Learning Goals

- Compute and plot Probability Density Function (PDF) and Cumulative Distribution Function (CDF) of normal distributions.
- Use decision tree and logistic regression classifiers for classification problems.
- Split datasets into training and testing sets and evaluate model performance using confusion matrices.
- Understand basics of data fusion.
- Apply clustering algorithms such as K-means and Spectral Clustering.
- Model multi-sensor uncertainty in simplified settings.

### Content Overview

- Tutorial on using `scipy.stats` for normal distribution functions.
- Using `scikit-learn` for machine learning tasks including data splitting, classification, and evaluation.
- Multiple choice questions on sensor fusion concepts and sensor errors.
- Coding assignments involving plotting distributions, classification, clustering, and sensor measurement modeling.
- Practical exercises on calculating probabilities, training classifiers, plotting confusion matrices, and interpreting clustering results.

This exercise builds foundational skills required for subsequent exercises in the course.

## Exercise 2: Common representation

This exercise focuses on common representation techniques in multi-modal data fusion, including dimensionality reduction and ensemble learning methods.

### Learning Goals

- Implement Principal Component Analysis (PCA) manually and using sklearn.
- Implement Linear Discriminant Analysis (LDA).
- Implement bootstrapping algorithm.
- Apply Gradient Boosting algorithm for classification problems.

### Content Overview

- Coding assignments to implement bootstrapping and PCA from scratch.
- Use of sklearn for PCA and Gradient Boosting classification.
- Implementation and visualization of LDA for class separation.
- Data splitting into training, validation, and testing sets.
- Evaluation of models using confusion matrices and validation scores.

This exercise builds on foundational Python and machine learning skills to explore advanced data representation and ensemble methods.

## Exercise 3: Data Alignment

This exercise explores different types of data alignment in multimodal data fusion, including spatial, temporal, and semantic alignment, as well as radiometric normalization.

### Learning Goals

- Understand and apply spatial alignment techniques such as image registration using mutual information.
- Apply dynamic time warping (DTW) for temporal alignment of time-series data.
- Use k-means clustering for semantic alignment and image segmentation.
- Perform radiometric normalization to calibrate variable scales.

### Content Overview

- Tutorials on image processing, histogram calculation, dynamic time warping, and clustering.
- Assignments on image rotation, histogram analysis, mutual information calculation, and plotting.
- DTW similarity calculation and visualization for time-series gesture data.
- K-means clustering applied to different color spaces and fused features for image segmentation.
- Radiometric normalization techniques including Z-transform and Min-Max scaling applied to real datasets.

This exercise deepens understanding of alignment techniques critical for effective multimodal data fusion.

## Exercise 4: Bayesian Inference and Parameter Estimation

This exercise focuses on the Bayesian framework and parameter estimation techniques essential for data fusion systems.

### Learning Goals

- Understand the basic elements of Bayesian inference.
- Apply traditional and Bayesian methods in parameter estimation tasks such as curve fitting.
- Use outlier-robust methods like RANSAC for parameter estimation.
- Apply Gaussian Mixture Models for clustering problems.

### Content Overview

- Tutorials on sinusoidal data generation, Bayesian inference, and robust estimation.
- Assignments on calculating statistical measures, linear and Bayesian regression, and RANSAC.
- Application of Gaussian Mixture Models for clustering and comparison with K-means.
- Visualization of regression fits, confidence intervals, and clustering results.

This exercise builds skills in probabilistic modeling and robust parameter estimation for multimodal data fusion.

## Exercise 5: Sequential Bayesian Inference

This exercise focuses on sequential modeling of multimodal data using recursive Bayesian filtering, especially Kalman filters.

### Learning Goals

- Apply Kalman filter for simple dynamic problems with single sensor data.
- Apply Kalman filter for multi-sensor fusion and localization.
- Become familiar with the filterpy library for Kalman filtering.

### Content Overview

- Tutorials on Kalman filter theory and implementation.
- Assignments on implementing 1D Kalman filter, using filterpy, and applying Kalman filters to robot localization.
- Multi-sensor fusion using Kalman filters with random walk and constant velocity models.
- Visualization of filtering results and error metrics.

This exercise develops skills in dynamic state estimation and sensor fusion using Bayesian filtering techniques.

## Exercise 6: Bayesian Decision Theory and Ensemble Learning

This exercise focuses on Bayesian decision theory in pattern classification, naive Bayes classification, and ensemble learning methods.

### Learning Goals

- Apply naive Bayes classifier to typical classification problems.
- Apply ensemble methods such as bagging and boosting to combine hypotheses.
- Combine classifier outputs using different approaches for data fusion.

### Content Overview

- Tutorials on Bayesian decision theory and naive Bayes classification.
- Assignments on classifying animal species, handling class imbalance, and improving models.
- Exploration of ensemble learning methods including bagging and boosting.
- Classifier combination strategies, diversity measures, and meta-learning with support vector machines.
- Visualization of learning curves, classifier accuracies, and combination results.

This exercise builds understanding of probabilistic classification and ensemble techniques for multimodal data fusion.

## Project Work: Multi-Modal Physical Exercise Classification

This project applies multi-modal data fusion techniques to classify physical exercises using wearable accelerometer and depth camera data from the MEx dataset.

### Learning Goals

- Study real-world multi-modal data and perform data preparation and visualization.
- Extract features and build unimodal and multimodal classification models.
- Apply feature-level and decision-level fusion techniques for improved classification.
- Evaluate models using confusion matrices, F1 scores, and analyze results.
- Optionally, perform biometric identification of persons using multi-modal data.

### Project Phases

1. Data preparation, exploration, and visualization.
2. Feature extraction and unimodal fusion for classification.
3. Feature extraction and feature-level fusion for multimodal classification.
4. Decision-level fusion for multimodal classification.
5. Bonus task: Multimodal biometric identification of persons.

### Techniques and Methods

- Windowing and synchronization of accelerometer and depth camera data.
- Dimensionality reduction using PCA and LDA.
- Classification using k-Nearest Neighbors, Support Vector Machines, AdaBoost, and ensemble methods.
- Hyperparameter tuning with grid search and cross-validation.
- Fusion of classifier outputs using fixed rules and voting classifiers.
- Performance evaluation with confusion matrices and weighted F1 scores.

This project demonstrates practical application of multi-modal data fusion and machine learning techniques for human activity recognition.
