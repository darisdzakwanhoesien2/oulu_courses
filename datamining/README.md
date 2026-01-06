o# Data Mining Project - Marketing Campaign Analysis

## Overview
This project performs a comprehensive data mining analysis on a marketing campaign dataset. The goal is to understand customer purchasing behavior, segment customers, and build predictive models to forecast spending and campaign response. The analysis includes data preprocessing, feature engineering, clustering, regression, classification, and visualization.

## Dataset
The dataset used is a marketing campaign dataset containing customer demographics, purchase history, and campaign response information. It includes features such as income, age, education, marital status, spending on various product categories, and purchase channels.

## Data Preparation
- Loaded the dataset and handled missing values by imputing medians.
- Created new features such as age, total spending, number of purchases, purchase frequency, and recency of purchase.
- Transformed categorical variables using one-hot encoding.
- Handled outliers and cleaned inconsistent data points.
- Engineered interaction features to capture relationships between spending and demographics.

## Modeling
- **Regression Models:** Linear regression and Ridge regression were trained to predict total customer spending based on engineered features.
- **Classification Model:** Logistic regression and Random Forest classifiers were used to predict customer response to marketing campaigns.
- **Clustering:** K-means clustering was applied to segment customers based on demographics and spending behavior. PCA was used for dimensionality reduction and visualization.

## Evaluation and Visualization
- Model performance was evaluated using metrics such as RMSE, R-squared, MAE for regression, and accuracy, precision, recall, F1-score for classification.
- Clustering quality was assessed using silhouette score, Davies-Bouldin score, and Calinski-Harabasz index.
- Visualizations include histograms, box plots, scatter plots, heatmaps, confusion matrices, ROC curves, and cluster analysis bar charts.
- SHAP values were used to interpret feature importance in the Random Forest model.

## Key Findings
- Income, education, marital status, and age significantly influence customer spending.
- Customer segmentation revealed distinct groups with varying income, spending, and purchase behaviors.
- Logistic regression achieved good accuracy in predicting campaign response, though precision and recall indicate room for improvement.
- Targeted marketing strategies can be developed based on identified customer segments and their preferences.

## Folder Contents
- `progress.ipynb`: Main notebook detailing the full data mining workflow including data exploration, cleaning, modeling, clustering, and visualization.
- `data.ipynb`: Complementary notebook with additional preprocessing, clustering with PCA, classification with Random Forest, and SHAP analysis.
- Various PNG images (`classification_report.png`, `feature_important.png`, `output.png`, etc.): Visualizations generated during the analysis.
- `label/`: Subfolder containing additional data or labels related to the project.

## Usage
1. Ensure the dataset file `marketing_campaign.csv` is available in the working directory.
2. Install required Python packages:
   ```
   pip install pandas numpy scikit-learn matplotlib seaborn shap yellowbrick
   ```
3. Run the notebooks in order (`data.ipynb` and `progress.ipynb`) to reproduce the analysis and visualizations.
4. Review the generated plots and model evaluation metrics for insights.

## Dependencies
- Python 3.x
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- shap
- yellowbrick

## Next Steps
- Refine customer segmentation with advanced clustering techniques.
- Improve predictive models with hyperparameter tuning and alternative algorithms.
- Explore personalized marketing strategies based on customer segments.
- Extend analysis to include time series or campaign effectiveness over time.

---

This README provides a comprehensive guide to the data mining project and should help users understand, reproduce, and extend the analysis.
