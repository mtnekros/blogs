# Getting started with ML and tensorflow

### Introduction
We are trying to create a simple neural network to get the relationship
between to numbers. We have a simple linear equation and we are trying to find
the relation using some x and y data values.
```
def y(x) {
 return 3 * x + 1
}
```


## Lets' do this in steps
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
    * When compilnig the out neural network, we do it by defining two functions,
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


## References:
* [Google for developers](https://www.youtube.com/watch?v=_Z9TRANg4c0)
