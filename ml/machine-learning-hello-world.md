# Getting Started with Machine Learning and TensorFlow

## Introduction
This blog post is a great introduction to using TensorFlow to create a simple
neural network and understand the relationship between two numbers. We'll
explore how to build a network that can learn a linear equation based on some
sample data.

## Understanding the Problem
The provided code defines a simple linear equation y = 3x + 1. Our goal is to
create a neural network that can learn this relationship without being
explicitly told the equation. We'll give the network some example input-output
pairs (x, y values), and it will learn to approximate the function that relates
them.

You might have seen a lot more complex neural networks but for simplicity, we
are just going to learn with the following neural network.

Input -> Neuron -> Output

Every neuron has associated weight and biases. In our final equation, the weight
is 3 and the bias is 1. Hence the equation y = 3x + 1. But we don't know that 
yet. We are only given the input and output values. Let's dive into the code
and write the neural network that will figure out that for us.

<Insert image of a complex neural network here.>

* Let's just dive into the code
    ```python
    import tensorflow as tf
    import numpy as np
    from tensorflow import keras
    ```
* create the simplest possible neural network with 1 layer and 1 neuron and the input
    shape is also just 1 value
    ```python
    model = keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])
    ```
    * When compiling the out neural network, we do it by defining two functions,
      a loss and an optimizer.
    * When computer tries to learn it, the computer guess, maybe `y = 4x + 10`.
      The *loss* function measures the guessed answer against the right answers
    * and gives a number denoting how bad or good it did.
      It then uses the *optimizer* function to make another guess that will minimize
      the loss. maybe 'y=3x + 5'
    * It will repeatedly try to guess and minimize the loss. How many times you
      repeat it is called epochs.
      ```python
      # specifying loss and optimizer
      model.compile(optimizer='sgd', loss='mean_squared_error')
      ```
    * here we are using stochastic gradient descent as the optimizer and mean squared
     error as the loss function

* providing the data
    ```python
    xs = np.arrray([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
    ys = np.array([-2.0, 1.0, 4.0, 7.0, 10.0, 13.0], dtype=float)
    ```
    Here `xs` are our data and `ys` are our labels
* training the neural network
    ```python
    model.fit(xs, ys, epochs=500)
    ```
    Here model.fit is used to train the model to learn to predict the values of y
    based on the values of x. After it keeps guessing and calculating the loss and
    optimizing the new guess for 500 epochs (i.e. 500 hundred times), it will be able to 
    somewhat predict the value of y for any given value of x.
* predicting new values.
  ```python
   print(model.predict([10.0])
   ````
   neural networks deal with probabilities, so the answer won't be exactly 31 but
   very close it (31.0001297)


