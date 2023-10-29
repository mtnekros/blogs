## Demystifying Support Vector Machines: Understanding Gamma, Regularization and Kernels

### What is a Support Vector Machine?
A support vector machine is a supervised learning algorithm used for classfication
and regression tasks. SVM works by finding the optimal hyperplane that best
separates data into distinct classes. This hyperplane is chosen to maximize the
margin, which is the distance between the hyperplane and the nearest data points
from each class. These closest data points are known as support vectors, which are
critical in determining the hyperplane's position and orientation.

### What is Gamma?
Gamma, often denoted as γ, is a crucial parameter in SVMs, particularly when
using non-linear kernels. It influences the shape of the decision boundary,
impacting how well the SVM can fit the training data and generalize to unseen
data. In simple terms, gamma controls the reach of individual data points in
defining the decision boundary. The range for gamma typically varies from 0.01
to 10 or even higher.

Mathematically, gamma influences the shape of the Radial Basis Function (RBF)
kernel, which is one of the most commonly used kernels in SVMs. A higher gamma
value makes the boundary more curved and sensitive to small-scale features in
the data, whereas a lower gamma results in a smoother and more global decision
boundary.


## What is Regularization?
Regularization is a technique used in machine learning to prevent overfitting.
In the context of SVM, the regularization parameter is commonly known as 'C'.
The range of regularization parameter C typically varies from 0.1 to 1000 or
even higher.

A smaller C value imposes a higher degree of regularization, while a larger C
allows the SVM to fit the training data more closely.

## What is a Kernel?
Kernels are an integral part of SVMs, especially when dealing with non-linear
data. Kernels are mathematical functions that transform the input data from it's
original feature space into a higher-dimensional space. Some commonly used
kernel functions include: linear kernel, ploynomial kernel and radial basis
function (rbf) kernel.

Understanding these mathematical functions and their parameters is key to
effectively using SVMs in various applications. Careful parameter tuning and
kernel selection can lead to highly accurate models in tasks ranging from text
classification to image recognition

### Code example:
```python
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

digits = load_digits()

print(dir(digits))
x_train, x_test, y_train, y_test = train_test_split(digits.data, digits.target)

model = SVC(kernel="rbf", gamma=0.00101, C=1)
model.fit(x_train, y_train)

print(model.score(x_test, y_test))

for i in range(10):
    x = digits.data[i]
    y = digits.target[i]
    y_pred = model.predict([x])
    print(f"Y: {y}\t y_pred: {y_pred[0]}")


y_preds = model.predict(x_test)
cm = confusion_matrix(y_test, y_preds)

plt.figure(figsize=(8,6))
sb.heatmap(cm, annot=True)
plt.xlabel('Predicted')
plt.ylabel('Truth')
plt.show()
```
