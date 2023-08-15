# Creating a simple multilayer neural network

We will be using a simple multilayer neural network to figure out if an images falls under one of
10 different categories. We are just going to use the fashion_mnist dataset provided by tensorflow
for training the model.  fashion_mnist comes with 70,000 labelled images.

| Label	| Description |
|-------|-------------|
| 0 	| T-shirt/top |
| 1 	| Trouser     |
| 2 	| Pullover    |
| 3 	| Dress       |
| 4 	| Coat        |
| 5 	| Sandal      |
| 6 	| Shirt       |
| 7 	| Sneaker     |
| 8 	| Bag         |
| 9 	| Ankle boot  |

### loading the data
```python
import tensorflow as tf
mnist = tf.keras.datasets.fashion_mnist
(training_images, training_labels), (test_images, test_labels) = mnist.load_data()
```
Now, we have both training and test datasets. Note: the labels are number from 0 to 9, instead of
the actual words. This is because computers understand numbers much better than words, esp in
machine learning.

### Normalizing the data
```python
training_images /= 255.0
test_images /= 255.0
```
NOTE: Add reason later

## Creating models
```python
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation=tf.nn.relu)
    tf.keras.layers.Dense(10, activation=tf.nn.softmax)
])
```
First layers, Flatten will only flatten the input image data into a one dimensional array. There are
not neurons in that layer. The second Dense layers has 128 and an activation of function called relu.
relu is a function that discards every negative values from the neurons and returns the positive values
as is. This is useful because negative outputs will cancel out the positive outputs, giving invalid results.
Third layers has 10 neuron, the output of each one will refer to the 10 category labels and it has 
the activation functions of softmax, which will take the output of all 10 neurons and set the max value
to 1 and everything else to 0. This will make it easier for us to determine which label has the max value.

## Compiling models and fitting the models
```python
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
model.fit(train_images, train_labels, epochs=5)
test_loss, test_acc = model.evaluate(test_images, test_labels)
```

## Predicting images
```python
model.predict(my_images)
```