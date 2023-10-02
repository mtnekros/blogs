# A Comprehensive Guide to Multivariate Linear Regression

Linear regression is a fundamental technique in machine learning used for
predicting a continuous target variable based on one or more input features. In
this article, we will delve into multivariate linear regression, one of its
variants, and explore the steps involved in creating and applying a predictive
model. Before we dive into the details, let's understand the concept of
multivariate linear regression and its significance.

## What is Multivariate Linear Regression?

Multivariate linear regression is an extension of simple linear regression,
where instead of just one predictor (feature), we use multiple predictors to
model the relationship between the inputs and the target variable. It's
particularly useful when you want to understand how multiple variables
collectively affect the outcome.

## The Dataset

To illustrate multivariate linear regression, we'll use a sample dataset
consisting of four columns: `experience`, `test_score(out of 10)`,
`interview_score(out of 10)`, and `salary($)`.

| experience | test_score(out of 10) | interview_score(out of 10) | salary($) |
|------------|-----------------------|----------------------------|-----------|
|            | 8                     | 9                          | 50000     |
|            | 8                     | 6                          | 45000     |
| five       | 6                     | 7                          | 60000     |
| two        | 10                    | 10                         | 65000     |
| seven      | 9                     | 6                          | 70000     |
| three      | 7                     | 10                         | 62000     |
| ten        |                       | 7                          | 72000     |
| eleven     | 7                     | 8                          | 80000     |

## Data Cleaning

Before building a multivariate linear regression model, it's crucial to clean
the dataset. Here are the steps we'll take:

### 1. Handling Words and Missing Values

1. **Converting Words to Numbers:** In the `experience` column, we have values
   like "five," "two," etc., which should be converted into numerical values.
   We can use the `word2number` Python package for this task.

2. **Handling Missing Values:** Some entries in the dataset have missing
   values. In this example, we observe missing values in the `experience` and
   `test_score(out of 10)` columns. We'll fill these missing values with
   appropriate replacements. For `experience`, we'll use the median value, and
   for `test_score(out of 10)`, we'll use the median test score.

Here's the code for data cleaning:

```python
import math
import pandas as pd
from sklearn import linear_model
from word2number import w2n

# Load the dataset
df = pd.read_csv("salary.csv")

# Convert words to numbers in the 'experience' column
df.experience = df.experience.apply(lambda x: w2n.word_to_num(x) if type(x) == str else x)

# Fill missing 'experience' values with the median
df.experience = df.experience.fillna(math.floor(df.experience.median()))

# Calculate and fill missing 'test_score(out of 10)' values with the median
median_test_score = math.floor(df["test_score(out of 10)"].median())
df["test_score(out of 10)"] = df["test_score(out of 10)"].fillna(median_test_score)
```

## Model Fitting

Now that we have cleaned our dataset, we can proceed to fit a multivariate linear regression model.

### 1. Import Libraries and Initialize the Model

In this step, we import necessary libraries and initialize a linear regression model:

```python
from sklearn.linear_model import LinearRegression

# Initialize the linear regression model
model = LinearRegression()
```

### 2. Train the Model

Now, let's move forward and train the multivariate linear regression model.
We'll use the cleaned dataset with the features `experience`, `test_score(out
of 10)`, and `interview_score(out of 10)` to predict the `salary($)`.

To train the model, we'll use the following code:

```python
# Fit the model with the features and target variable
model.fit(df[["experience", "test_score(out of 10)", "interview_score(out of 10)"]], df["salary($)"])
```

By executing this code, we've created a model that has learned the
relationships between the input features and the target variable salary($). The
model is now ready to make predictions based on new input data.

### 3. Make Predictions
After successfully training the multivariate linear regression model, we can
use it to make predictions. Suppose we want to predict the salary for a
hypothetical candidate with the following attributes:

* experience: 20 years
* test_score(out of 10): 10
* interview_score(out of 10): 10

We can use the model to predict their salary using the following code:

```python
# Predict the salary for a candidate with specific attributes
predicted_salary = model.predict([[20, 10, 10]])
print("Predicted Salary: $", predicted_salary[0])
```
