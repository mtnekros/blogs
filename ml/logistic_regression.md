# Logistic Regression
Logistic regression is a classification algorithm used for binary or
multi-class classification tasks. Logistic regression estimates the probability
that an input belongs to a particular class. Despite its name, it's a
classification algorithm, not a regression algorithm, which is used for
predicting continuous algorithm. However, it can be seen as an extension of the
linear regression, mathematically speaking, as it is achieved by applying the
sigmoid function on the linear equation. 

# How Logistic Regression Works
1. **Binary Classification**: In binary classification, logistic regression predicts
   of two classes (e.g. Yes/No, Spam/Not Spam, True/False).
2. **Linear Combination**: Like linear regression, logistic regression starts with
   linear combination of input features, but this linear combination doesn't
   represent the final prediction. It's denoted as:
   ```math
   z = w1*x1 + w2*x2 + ... + wn * xn + b 
   ```
   * xi represents the input features.
   * wi are the model weights
   * b is the bias term
3. **Sigmoid Function**: The linear combination `z` is then passed through the
   sigmoid function (also called the logistic fuction):
   ```
   sigma(z) = 1 / (1 + e ^-z)
   ```
   The sigmoid function maps `z` to a probability value between 0 and 1.
4. **Thresholding**: A threshold (usually 0.5) is applied to the predicted
   probability to make the final binary classification decision.

This is how the normal logistic regression works. While the basic form of
logistic regression is designed for binary classification, there are techniques
and extensions that allow it to be adapted for multi-class problems. There are
two common approaches for this:

## One-vs-Rest (OvR) or One-vs-All (OvA):
In this approach, you create a separate binary logistic regression model for
each class. For example, if you have three classes (Class A, Class B, and Class
C), you would create three separate models: one for distinguishing Class A from
not Class A, another for Class B from not Class B, and the third for Class C
from not Class C. During prediction, each model produces a probability score,
and the class associated with the highest probability becomes the predicted
class.

## Softmax Regression (Multinomial Logistic Regression):
In this approach, you extend logistic regression to handle multiple classes
directly without creating binary models. The softmax function is used to
calculate the probabilities of each class, and the class with the highest
probability is chosen as the predicted class. Softmax regression is sometimes
called multinomial logistic regression.
```
P(Y=j|x) = e ^ zj / (e ^ z1 + e ^ z2 + ... e ^ zk)
```
   * P(Y=j|x) is the probability of class j
   * zi is the linear combination of input features and model parameters for class i
   * k is the no of classes

