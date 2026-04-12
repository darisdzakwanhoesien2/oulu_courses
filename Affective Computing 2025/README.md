# Documentation for AffComp/exercise

## exercise1_darisdzakwan_hoesien_2406778.ipynb

### Objective
This exercise focuses on building a facial expression recognition system. The system includes face preprocessing, feature extraction, and classification. The tasks involve preprocessing facial expression images, extracting features from images or videos, and classifying videos into categories.

The region of interest (facial image) is extracted using face tracking, face registration, and face cropping functions. Basic spatiotemporal features (LBP-TOP) are extracted, and Support Vector Machine (SVM) classifiers are trained using 50 videos from 5 participants for training and 50 videos for evaluation.

### Database
The dataset is a subset of eNTERFACE, containing 100 facial expression samples from ten actors acting happy and sadness behaviors.

### Task 1: Face Preprocessing
- **Task 1.1:** Detect face and facial landmarks using the DLib library.
- **Task 1.2:** Perform face registration using fixed landmarks from a standard model and extract the face from the registered image.
- **Task 1.3:** Visualize results using subplots.

### Task 2: Feature Extraction
- Extract Local Binary Pattern (LBP) features using `skimage.feature.local_binary_pattern`.
- Define parameters P=8, R=1.0, method='nri_uniform'.
- Calculate and normalize the histogram of the LBP face.
- Visualize the LBP face and normalized histogram.

### Task 3: Feature Classification
- Load training and testing data from `.mat` files.
- Train SVM classifiers using a linear kernel.
- Evaluate classifiers by predicting training and testing data.
- Calculate classification accuracies and confusion matrices.

### Questions
The exercise includes several reflective questions about the differences between cropped images, the purpose of face registration, reasons for feature extraction, and analysis of classification results.

---
## exercise2_darisdzakwan_hoesien_2406778.ipynb

### Objective
This exercise focuses on extracting prosodic correlates (suprasegmental speech parameters) and cepstral features from speech recordings to build an emotion recognition system distinguishing happy versus sad emotional speech.

The dataset consists of simulated emotional speech from ten speakers, each speaking five pre-segmented sentences in two emotional states (happy and sad), totaling 100 samples.

### Task 0: Preparation
- Downsample the speech sample from 48 kHz to 11.025 kHz using `scipy.signal.resample`.
- Visualize the resampled signal.

### Task 1: Feature Extraction
- **Task 1.1:** Calculate MFCC coefficients after pre-emphasizing the resampled signal.
- **Task 1.2:** Extract short time energy (STE) contour using a Hamming window and calculate distribution parameters.
- **Task 1.3:** Extract pitch/F0 contour using a provided function and calculate distribution parameters.
- **Task 1.4:** Extract rhythm/duration parameters by segmenting voiced and unvoiced speech and calculating segment statistics.

### Task 2: Speech Emotion Classification
- Train SVM classifiers with prosodic and MFCC features using a 3rd order polynomial kernel.
- Test classifiers on training and testing data.
- Calculate and print classification accuracies.
- Plot confusion matrices for both classifiers on training and testing data.

### Questions
The exercise includes reflective questions on pre-emphasis, STE clipping, voiced vs unvoiced sounds, feature performance comparison, confusion matrix interpretation, and alternative classification metrics.

