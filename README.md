ORBITAL ATLAS

Space Rockets & Satellite Launches

Exploratory Data Analysis | Data Visualization | Streamlit Dashboard

ORBITAL ATLAS is a data analysis project that explores rocket launches and satellite records from 1957 to 2026.

The project focuses on understanding launch trends, mission outcomes, satellite distributions, and orbital characteristics using Python and Exploratory Data Analysis (EDA).

The final results are presented through an interactive Streamlit dashboard.

⸻

Project Overview

The project uses two datasets:

1. Rocket Launches Dataset

Contains information about rocket launches, including launch dates, organizations, countries, and mission outcomes.

2. Satellites Dataset

Contains information about satellites, including orbital periods, inclination angles, and orbital altitudes.

Both datasets were merged using launch_id to combine launch information with satellite records.

Dataset Summary

Dataset Information	Value
Rocket Launches	7,640
Satellite Records	28,056
Merged Rows	28,736
Final Columns	32
Time Period	1957–2026

⸻

Exploratory Data Analysis (EDA)

The analysis started by exploring the dataset structure, checking data quality, and preparing the data for visualization.

Data Cleaning & Preprocessing

The main steps included:

* Missing Values: Checked missing values, removed unnecessary columns, and handled selected missing categorical data.
* Data Types: Converted date columns to datetime.
* Duplicates: Checked duplicate records and avoided counting repeated launch IDs.
* Column Selection: Removed unnecessary columns and selected relevant features.
* Outliers: Used the IQR method and boxplots to identify extreme orbital values.

Some outliers were kept because they may represent real space missions rather than incorrect data.

Data Visualization

Three types of analysis were performed:

Univariate Analysis

* Histograms
* Countplots
* Boxplots

Bivariate Analysis

* Scatter plots
* Bar charts
* Correlation heatmap

Multivariate Analysis

* Line charts
* Stacked bar charts
* Scatter plots grouped by categories

These visualizations helped identify patterns, compare categories, and understand relationships between orbital measurements.

⸻

Key Findings

The analysis revealed several interesting results:

* Launch Trends: Rocket launch activity reached its highest recorded annual count in 2025, with 341 launches.
* Launch Success: 92.71% of recorded rocket launches were successful.
* Top Organization: The Soviet Space Program recorded the highest number of launches.
* Orbit Categories: Low Earth Orbit (LEO) was the most common category, with 19,423 satellite records.
* Orbital Relationship: A strong positive correlation (+0.964) was found between highest orbital altitude and orbital period.

⸻

Streamlit Dashboard

An interactive dashboard was created to make the analysis easier to explore.

The dashboard includes:

* Interactive filters for launch year, country, organization, outcome, and orbit category.
* Dataset preview and summary statistics.
* Interactive charts and visualizations.
* Key performance indicators.
* Insights based on the selected data.

Dashboard Pages

Page	Description
Overview	General statistics and launch trends
Launch Analysis	Launch organizations and outcomes
Orbital Analysis	Satellite orbital characteristics
Multivariate	Relationships between multiple variables
Data Explorer	Explore and preview the dataset

Live Dashboard

Dashboard Link: Open ORBITAL ATLAS

⸻

Tools & Libraries

The project was developed using:

* Python — Data analysis
* Pandas — Data cleaning and preprocessing
* NumPy — Numerical operations
* Matplotlib & Seaborn — EDA visualizations
* Plotly — Interactive charts
* Streamlit — Dashboard development
* Google Colab — Data exploration and analysis
* VS Code — Dashboard development

⸻

How to Run the Dashboard

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/ORBITAL-ATLAS.git

2. Open the project folder

cd ORBITAL_ATLAS

3. Install the required libraries

pip install -r requirements.txt

4. Run the Streamlit application

Make sure Space_Cleaned2.csv is in the same folder as app.py.

streamlit run app.py

The dashboard will open in your browser.

⸻

Project Files

The repository includes the main files used in the project:

* app.py — Streamlit dashboard.
* Space_Cleaned2.csv — Cleaned dataset.
* requirements.txt — Required Python libraries.
* README.md — Project documentation.
* Jupyter Notebook — EDA code and visualizations.
* PDF Report — Project analysis and results.
* Presentation — Final project presentation.

⸻

Conclusion

ORBITAL ATLAS shows how EDA can be used to understand rocket launch activity and satellite orbital data.

The project combines data cleaning, statistical analysis, and visualization to explore patterns and relationships in the dataset.

The Streamlit dashboard brings these results together in one place, making the data easier to explore and understand.

⸻

ORBITAL ATLAS | Data Science Final Project
