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
