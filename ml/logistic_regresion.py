"""
## Script to use logistic regression to predict digit
* I am using the default dataset provided by the sklearn to train the model
* The dataset consists of 1797 8x8 images.
* I have split that data into train and test set train and test set using the
  sklearn train_test_split method.
* I am using the LogisticRegression model with multi_class option of ovr.
* Tried with both ovr and multinomial got similar score of around 0.95.
* I am also calculating the confusion matrix (simple way to compare prediction vs
  ground truth value)
* I am using seaborn to plot the heatmap for the confusion matrix.

packages used:
scikit-learn==1.0.2
matplotlib==3.5.3
seaborn==0.12.2
"""

import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import seaborn as sb
import numpy as np

digits = load_digits()

print(f"No of images: {len(digits.images)}")

# splitting data into train and test sets
x_train, x_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2)

# model
model = LogisticRegression(multi_class='multinomial')

# training the model
model.fit(x_train, y_train)
print(f"Model: {model.get_params()}")
# getting the score for the datasets
print(f"score: {model.score(x_test, y_test)}")

# checking some of the predictions
predictions = model.predict(digits.data[:9])
targets = digits.target[:9]
for pred, target in zip(predictions, targets):
    print(f"pred: {pred}, target: {target}")

# calculating the confusion matrix
y_preds = model.predict(x_test)
cm = confusion_matrix(y_test, y_preds)

# plotting the confusion_matrix
print(cm)
plt.figure(figsize=(8,6))
sb.heatmap(cm, annot=True)
plt.xlabel('Predicted')
plt.ylabel('Truth')
plt.show()


"""
Same thing for iris dataset
"""
from sklearn.datasets import load_iris

iris = load_iris()

# viewing the scatter plot data
_, ax = plt.subplots()
scatter = ax.scatter(iris.data[:, 0], iris.data[:, 1], c=iris.target)
ax.set(xlabel=iris.feature_names[0], ylabel=iris.feature_names[1])
ax.legend(
    scatter.legend_elements()[0],
    iris.target_names,
    loc="lower right",
    title="Classes",
)

_, ax1 = plt.subplots()
scatter1 = ax1.scatter(iris.data[:, 2], iris.data[:, 3], c=iris.target)
ax1.set(xlabel=iris.feature_names[2], ylabel=iris.feature_names[3])
ax1.legend(
    scatter1.legend_elements()[0],
    iris.target_names,
    loc="lower right",
    title="Classes",
)

# spitting test train data
x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)
print(f"{len(x_train)} {len(y_train)}")
print(f"{len(x_test)} {len(y_test)}")
print(x_train[0])
print(y_train[0])

# create and train mdoel
model = LogisticRegression()
model.fit(x_train, y_train)
# checking model score
score = model.score(x_test, y_test)
print(f"model score: {score}")

# trying prediction
pred = model.predict([[10, 6, 1.6, 0.6]])
print(iris.target_names[pred])

# generating confusion matrix
preds = model.predict(x_test)
cm = confusion_matrix(y_test, preds)

# drawing the confustino matrix
plt.figure(figsize=(6, 4))
plt.xlabel('Predicted')
plt.ylabel('Truth')
sb.heatmap(cm, annot=True)
plt.show()
