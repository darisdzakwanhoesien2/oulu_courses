# Big Data Project Documentation

## bdpa_exercise_01.ipynb

This notebook performs climate data analysis using PySpark and Python visualization libraries. The main steps include:

- **Data Downloading:** (commented out) Code to download raw climate data CSV from a URL and clean it by removing header lines.
- **Data Loading:** Using PySpark's SparkSession to load the cleaned CSV file into a DataFrame with inferred schema.
- **Data Exploration:** Displaying sample rows and schema of the DataFrame.
- **Data Wrangling:** Casting columns to appropriate data types, renaming columns, and filtering data based on temperature and precipitation.
- **Data Preparation:** Registering the DataFrame as a temporary SQL view for Spark SQL queries.
- **Data Analysis:** Performing SQL queries to aggregate and analyze air temperature data.
- **Data Visualization:** Converting Spark DataFrames to Pandas DataFrames for plotting with matplotlib and seaborn. Visualizations include scatter plots, line plots, histograms, and boxplots showing relationships and trends in temperature, precipitation, wind speed, humidity, dew point, and vapor pressure.
- **Temporal Feature Extraction:** Extracting timestamp, year, month, and hour from date strings for temporal analysis.
- **Weather Correlations and Trends:** Analyzing correlations between weather variables and temporal trends by month and hour.

This notebook demonstrates a comprehensive workflow for big data climate analysis combining Spark's distributed processing with Python's rich visualization ecosystem.

## bdpa_exercise_02.ipynb

This notebook demonstrates a machine learning classification task on climate data using PySpark's MLlib. The key steps include:

- **Data Loading:** Loading the cleaned climate CSV data into a Spark DataFrame.
- **Feature Engineering:** Converting date strings to indexed numeric features using StringIndexer, casting columns to double, and discretizing temperature into three categories (cold, moderate, hot) using QuantileDiscretizer.
- **Feature Vector Assembly:** Combining relevant features into a single vector column for ML input.
- **Data Splitting:** Splitting the dataset into training and testing sets.
- **Model Definition:** Defining a Multilayer Perceptron Classifier (MLP) with specified input, hidden, and output layers.
- **Model Training:** Training the MLP model on the training data.
- **Prediction and Evaluation:** Making predictions on the test data and evaluating accuracy using MulticlassClassificationEvaluator.

This notebook illustrates the application of deep learning techniques for classification on big data using PySpark.

## bdpa_exercise_03.ipynb

This notebook performs a classification task on climate data using PySpark. The main steps include:

- **Setup:** Initializing Spark session and importing necessary ML and SQL functions.
- **Data Loading:** Loading the cleaned climate CSV data into a Spark DataFrame.
- **Feature Engineering:** Indexing the time column, casting relevant columns to double, and discretizing air temperature into categories for classification.
- **Feature Vector Assembly:** Combining features into a vector column for ML input.
- **Data Splitting:** Splitting the dataset into training and test sets.
- **Model Definition:** Defining a Multilayer Perceptron Classifier (MLP) with specified layers.
- **Model Training and Evaluation:** Training the MLP model and evaluating classification accuracy on the test set.

This notebook demonstrates the use of PySpark MLlib for classification tasks on big data.

## data.ipynb

This notebook performs basic data handling and preparation tasks using pandas. The key steps include:

- **Data Loading:** Reading a CSV file ('2009.csv') into a pandas DataFrame.
- **Data Subsetting:** Extracting the first 1000 rows and saving them to a new CSV file ('2009_1000.csv').
- **Data Downloading and Cleaning:** Downloading a raw climate data CSV from a URL, cleaning it by removing header lines, and saving the cleaned data to 'hly1075_cleaned.csv'.

This notebook provides foundational data preparation steps for subsequent big data analysis.

## evaluation_notebook.ipynb

This notebook is used for data exploration and preprocessing on a games dataset using PySpark. The main steps include:

- **Data Loading:** Loading a CSV file ('converted.csv') into a Spark DataFrame.
- **Data Cleaning:** Dropping irrelevant columns containing URLs and other non-essential data.
- **Data Casting:** Cleaning and casting columns to appropriate data types, including price conversion and numeric fields casting.
- **Date Conversion:** Converting release date strings to date objects with legacy parser settings.
- **SQL Views and Queries:** Creating temporary SQL views and running queries to extract release dates and other features.
- **Data Transformation:** Splitting string columns like Tags, Genres, and Categories into arrays and trimming whitespace.
- **Visualization:** Plotting average game prices over the years using matplotlib.
- **Next Steps and Responsibilities:** Notes on further preprocessing, feature engineering, advanced analysis, and team responsibilities.

This notebook supports exploratory data analysis and preparation for further big data projects.

### 🌟 **BDPA – Steam Games Dataset Project: STAR Summary**

---

### 🔹 1. **Data Preprocessing and Cleaning**

**S**: The dataset contained 45+ columns of mixed-format Steam game metadata including URLs, inconsistent price values, nested genre/tag fields, and ambiguous date formats.

**T**: Prepare a clean, structured DataFrame for meaningful analysis and modeling by removing noise, standardizing formats, and handling inconsistencies.

**A**:

- Dropped irrelevant columns (e.g., URLs, support emails).
- Removed non-numeric and duplicate `AppID`s.
- Standardized prices and cast to `DoubleType`.
- Parsed inconsistent release dates with fallback methods (e.g., appending "01" to parse `MMM yyyy`).
- Cast gameplay and engagement columns to numeric types.
- Split comma-separated arrays like Tags and Genres, then trimmed white space.

**R**:

- Cleaned dataset with consistent schema: 30+ refined features.
- Enabled reliable Spark SQL operations and ML pipelines downstream.
- Reduced conversion failures to zero after fallback logic for dates.

---

### 🔹 2. **Exploratory Data Analysis (EDA)**

**S**: The team aimed to understand what drives popularity and engagement across game platforms, genres, tags, and player types (single/multi-player).

**T**: Conduct an EDA that reveals trends in game pricing, popularity, genre-tag combinations, and player preferences over time.

**A**:

- Used Spark SQL to analyze yearly trends of average game prices and gameplay durations.
- Visualized top 100 games by positive reviews and playtime across Mac, Windows, and Linux.
- Created heatmaps of genre-tag combinations and bar plots for most common genres.
- Examined release frequency of single vs multi-player games over the years.
- Built interactive comparisons (e.g., bar charts of platform-based reviews and engagement).

**R**:

- Identified dominant genres (e.g., Action, Indie), platforms with highest engagement (Windows), and rising tags.
- Observed historical shifts in game type frequency (multi-player rise post-2015).
- Created visual insights that shaped downstream modeling hypotheses.

---

### 🔹 3. **Machine Learning Model Development**

**S**: The team wanted to predict a game's popularity (measured via positive reviews) using features like price, genre, playtime, and release year.

**T**: Develop, train, and evaluate multiple regression models to predict popularity and extract key feature importance.

**A**:

- Engineered features: capped prices, log-transformed playtime and engagement scores, one-hot encoded top genres.
- Built Spark ML pipelines using `VectorAssembler`, `RandomForestRegressor`, `LinearRegression`, and `PoissonRegression`.
- Split the data (80/20) and evaluated models using RMSE, MAE, and R².
- Extracted feature importances and visualized results (e.g., prediction vs actual, bar charts of top features).

**R**:

- Achieved strong predictive performance (Random Forest RMSE < 0.5 in log scale).
- Identified key drivers: `Log_Playtime`, `Peak CCU`, and `Achievements`.
- Poisson model further validated genre impacts using interpretable coefficients.

---

### 🔹 4. **Summary and Insights**

**S**: The analysis was expected to provide actionable insights for understanding Steam game success factors and predicting future hits.

**T**: Summarize findings into impactful conclusions and propose extensions for future work.

**A**:

- Consolidated insights from EDA and ML (e.g., engagement metrics matter more than price).
- Proposed new metrics like Engagement Ratio and Playtime Per Owner.
- Suggested advanced directions: clustering for player segmentation, tag-based recommendation engines.

**R**:

- Presented results to stakeholders with clear data stories and visuals.
- Laid the foundation for a recommender system and deeper behavioral modeling in future versions.