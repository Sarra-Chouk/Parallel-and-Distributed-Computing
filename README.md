# Description

This project is Lab 03 part 2 from the DSAI3202 - Parallel and Distributed Computing course. It implements a complete machine learning regression pipeline to predict housing prices using a real dataset. 

Beyond building a predictive model, this project investigates how various execution strategies—sequential, multithreaded, and multiprocessing—can influence the performance of data processing and model training.

---

## Breakdown

`1. Data Loading`

- Loads training data from a CSV file.

`2. Data Preprocessing`

- Cleans missing or invalid values
  
- Caps outliers using the IQR method

- Encodes categorical variables

- Scales numerical features

`2. Modeling`

- Splits the data into training and testing sets

- Trains a regression model

- Makes predictions on the test set

`3. Evaluation`

- Evaluates performance using appropriate metrics (e.g., MAE, RMSE)

`4. Execution Strategies`

- A standard sequential approach

- A multithreading-based implementation

- A multiprocessing-based implementation

---

## How to run

<pre><code>pip install -r requirements.txt 
python main.py</code></pre>
