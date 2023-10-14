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
# plt.show()

