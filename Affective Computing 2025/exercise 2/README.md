# Affective Computing - Exercise 2

## Objective
The objective of this exercise is to build a facial expression recognition system. This system involves face preprocessing, feature extraction, and classification. Key components include:
- **Face Preprocessing**: Extracting the region of interest (facial image) using face tracking, registration, and cropping.
- **Feature Extraction**: Using LBP-TOP (Local Binary Pattern - Three Orthogonal Planes) to extract basic spatiotemporal features.
- **Classification**: Training Support Vector Machine (SVM) classifiers to categorize videos based on extracted features.

The system is trained on 50 videos from 5 participants (happy and sadness behaviors) and evaluated on another 50 videos from the same dataset (a subset of eNTERFACE).

## Task 1. Face preprocessing
This task focuses on processing a face image, divided into three subtasks:
- **Task 1.1. Extract facial landmarks**: Detect faces and facial landmarks using the DLib library, transform the detected results into a 2-D numpy array, and visualize the landmarks on the image.
- **Task 1.2. Face normalization**: Load a standard face model's landmark positions, calculate the transformation between detected landmarks and the standard model using `skimage.transform.PolynomialTransform()`, and warp the example image using `skimage.transform.warp()`. Finally, crop the face from both the registered image and the original example image using `face_lib.crop_face`.
- **Task 1.3. Display result**: Visualize the original image with landmarks, cropped faces (from example and registered images), and their respective histograms using `matplotlib.pyplot.subplots()`.

## Task 2. Feature extraction
This task involves extracting LBP (Local Binary Pattern) features, which are widely used in face and facial expression recognition.
- Define LBP parameters (P=8, R=1.0, method='nri_uniform').
- Extract LBP features using `skimage.feature.local_binary_pattern()`.
- Calculate and normalize the histogram of the LBP face.
- Visualize the LBP face and its normalized histogram.

## Task 3. Feature Classification
This task utilizes Support Vector Machine (SVM) for feature classification, using `sklearn.svm.SVC()`.
- **Task 3.1. Load data**: Read `Task3_data.mat` using `scipy.io.loadmat()` to load training data, testing data, training class labels, and testing class labels.
- **Task 3.2. Train SVM classifiers**: Construct an SVM classifier object with a linear kernel and train it using the `fit()` method with training data and labels.
- **Task 3.3. Evaluate your classifiers**: Predict classes for training and testing data using the `predict()` method. Calculate classification accuracies and confusion matrices for both training and testing sets using `sklearn.metrics.confusion_matrix()`.

# `face_lib.py` Explanation

This file contains utility functions for facial processing, primarily used in Task 1 of the exercise.

## `shape2points` function
- **Purpose**: Transforms a `dlib` shape object (which represents facial landmarks) into a NumPy array.
- **Arguments**:
    - `shape`: A `dlib` shape object obtained from a `dlib` predictor.
    - `dtype` (optional): Data type of the returned array (default: "int").
    - `point_num` (optional): Number of points in the shape object (default: 68, for standard facial landmarks).
- **Returns**: A `np.ndarray` of shape `(point_num, 2)` containing the (x, y) coordinates of the landmarks.

## `crop_face` function
- **Purpose**: Crops a face from a given image based on detected facial landmarks. It also handles resizing the cropped face.
- **Arguments**:
    - `raw_image`: A NumPy array representing the input image.
    - `landmarks`: A NumPy array containing the facial landmarks.
    - `left_eye_inds` (optional): List of landmark indices for the left eye (default: 68-landmark model indices).
    - `right_eye_inds` (optional): List of landmark indices for the right eye (default: 68-landmark model indices).
    - `resize` (optional): A tuple `(width, height)` to resize the cropped image to (default: `(128, 128)`). If `None`, no resizing is performed.
- **Functionality**:
    1. Converts the image to grayscale if it's a color image.
    2. Calculates the center coordinates of the left and right eyes.
    3. Determines the distance and angle between the eyes to calculate a transformation for alignment.
    4. Iterates through the calculated face region to extract pixels, effectively rotating and translating the face.
    5. Resizes the `norm_face` to the specified `resize` dimensions if `resize` is not `None`.
- **Returns**: The cropped face as a NumPy array.
