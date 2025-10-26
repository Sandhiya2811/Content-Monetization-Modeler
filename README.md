# Content-Monetization-Modeler

📊 YouTube Analytics Data Project
🧠 1. Project Overview

This project focuses on analyzing YouTube video performance data to understand viewer engagement, content trends, and ad revenue patterns.
The dataset includes key performance metrics (views, likes, comments, watch time, revenue) along with metadata such as category, device, and country.

🗂️ 2. Dataset Information

The dataset is stored in a CSV file and includes the following features:

Column Name	                    Description
date	                  The date on which the data was recorded
views	                  Number of views the video received
likes	                  Number of likes given by viewers
comments	              Number of comments received
watch_time_minutes	    Total minutes watched by viewers
video_length_minutes	  Length of the video in minutes
subscribers	            Subscriber count (or change) for the channel
category	              Category of the video (e.g., Education, Entertainment, etc.)
device	                Type of device used by the audience (Mobile, Desktop, etc.)
country	                Country of the viewers
ad_revenue_usd	        Revenue generated from ads in USD

🧹 3. Data Preprocessing

Data preprocessing was performed to ensure data quality and prepare it for analysis and modeling.

3.1 Drop Unwanted Columns

Removed any unnecessary columns that do not contribute to the analysis.

Focused only on relevant performance and demographic features.

3.2 Check for Duplicates

Verified and removed duplicate rows to maintain data integrity.

3.3 Handle Missing (NaN) Values

Checked for null or missing values in each column.

Filled missing numeric values using the mean/median strategy and categorical columns using the mode.

3.4 Correct Spelling Mistakes & Case Sensitivity

Standardized text fields (category, device, country) to correct inconsistent spellings or letter cases (e.g., "mobile" → "Mobile").

3.5 Check Data Types

Ensured each column has the correct data type.

Converted date to datetime format for time-based analysis.

3.6 Feature Engineering

New features were derived to enhance insights:

| New Feature              | Formula / Description                       |
| ------------------------ | ------------------------------------------- |
| **year**                 | Extracted from `date`                       |
| **month**                | Extracted from `date`                       |
| **day_of_week**          | Extracted from `date` (Monday–Sunday)       |
| **like_per_view**        | `likes / views`                             |
| **comments_per_view**    | `comments / views`                          |
| **watchtime_per_view**   | `watch_time_minutes / views`                |
| **watchtime_per_minute** | `watch_time_minutes / video_length_minutes` |


These new features help identify engagement and performance efficiency over time.

3.7 Outlier Handling

Identified outliers using statistical methods (IQR or Z-score)(Box plot).

Applied capping for extreme anomalies in views.

📊 4. Data Visualization

Visualization was used to explore relationships between variables and the target feature (ad_revenue_usd).

| Chart Type       | Purpose                                                                              |
| ---------------- | ------------------------------------------------------------------------------------ |
| **Scatter Plot** | Relationship between numerical features (e.g., views, likes, watch time) and revenue |
| **Bar Chart**    | Comparison of categorical features (e.g., device, category, country) vs. revenue     |
| **Pie Chart**    | Share distribution across categories or countries                                    |
| **Line Plot**    | Trend of revenue or views over time                                                  |
These new features help identify engagement and performance efficiency over time.

🧩 5. Data Splitting

Dataset was split into training and testing sets (e.g., 80%–20%) to enable model validation.

Ensured random shuffling to maintain unbiased samples.

Target variable: ad_revenue_usd

Features: All other numeric and categorical columns.

⚙️ 6. Preprocessing Pipeline

To ensure consistent and efficient data transformation, a scikit-learn preprocessing pipeline was built using Pipeline and ColumnTransformer.
This allows automatic handling of missing values, scaling of numerical features, and encoding of categorical variables — all in one unified process.

6.1. Numerical Continuous Transformer

Used for continuous numerical columns such as views, likes, comments, watch_time_minutes, and ad_revenue_usd.

Steps Applied:

Imputation: Missing values replaced using the median strategy to reduce the effect of outliers.

Scaling: Features standardized using StandardScaler to normalize their range.

6.2. Numerical Discrete Transformer

Applied to discrete numeric columns such as subscribers, video_length_minutes, or other count-based fields.

Steps Applied:

Imputation: Missing values filled with the most frequent value to preserve categorical frequency behavior.

6.3. Categorical Transformer

Applied to categorical columns such as category, device, and country.

Steps Applied:

Imputation: Missing categorical values filled using the most frequent category.

Encoding: Categories encoded using OrdinalEncoder, guided by predefined ranking (cat_rank) to preserve category order or importance.

6.4. Column Transformer (Final Preprocessor)

All three transformers are combined into a single ColumnTransformer, which applies the appropriate preprocessing steps to each type of feature automatically.

🤖 7. Model Building — Linear Regression

After preprocessing the dataset, a Linear Regression model was used to predict the target variable — ad_revenue_usd — based on engagement and metadata features.

7.1 Model Setup

A Pipeline was constructed to streamline preprocessing and model training.
The pipeline ensures that data transformations are automatically applied during model fitting and prediction.

7.2 Model Training

The pipeline was trained using the training dataset (X_train, y_train) and tested on the testing dataset (X_test, y_test).

7.3 Model Evaluation Metrics

The performance of the model was evaluated using several regression metrics:

| Metric                             | Description                                                                  |
| ---------------------------------- | ---------------------------------------------------------------------------- |
| **MSE (Mean Squared Error)**       | Measures the average squared difference between predicted and actual values. |
| **RMSE (Root Mean Squared Error)** | Square root of MSE, providing error in original units.                       |
| **MAE (Mean Absolute Error)**      | Average of absolute differences between predicted and actual values.         |
| **R² (R-squared)**                 | Proportion of variance in the target variable explained by the model.        |


7.4 Interpretation

A high R² value on both training and testing sets indicates the model explains a strong proportion of variance in ad revenue.

Lower MSE/RMSE and MAE indicate better model accuracy.

If test metrics are close to training metrics, the model generalizes well; large differences may indicate overfitting.

💾 8. Model Deployment — Streamlit App

To make the model accessible and interactive, the trained pipeline was deployed using Streamlit, a Python-based web app framework for data science projects.

Model Serialization

After model training and evaluation, the entire pipeline (including preprocessing and regression model) was saved using the pickle module.
This allows the model to be reloaded and used for predictions without retraining.

9. Streamlit Application

A simple and interactive Streamlit web application was created to predict YouTube Ad Revenue (USD) based on user inputs such as:

Views
Likes
Comments
Watch time
Video length
Category
Country
Device type

The app uses the saved model (youtube_linear_model.pkl) to generate real-time revenue predictions.

App Features:

User-friendly input fields for all features.

Predicts ad revenue instantly using the trained regression pipeline.

Displays predicted revenue with supporting feature insights.

🧾 9. Conclusion

This project successfully demonstrates a complete YouTube Analytics Data Analysis and Prediction Pipeline, starting from raw data preprocessing to interactive deployment.

Key Highlights:
Cleaned, preprocessed, and engineered multiple data features.
Built an automated preprocessing and regression pipeline using scikit-learn.
Evaluated model performance using various regression metrics.
Saved and deployed the trained model using Streamlit for real-world usage.

The Linear Regression model achieved 95% accuracy (R² ≈ 0.95) on the test data, indicating excellent predictive performance and strong correlation between features and ad revenue.

✅ Final Outcome

The developed YouTube Ad Revenue Prediction System effectively analyzes viewer behavior, engagement, and content performance to forecast revenue outcomes.
The model achieved 95% predictive performance, making it a reliable analytical tool for content creators and marketers to optimize strategies and maximize monetization potential.
