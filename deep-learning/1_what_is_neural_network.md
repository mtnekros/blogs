To explain neural network, we need to understand what a perceptron is.
Perceptron is a single neuron. It is simple linear function.
x --> y

y = wx + b

w => weight
b => bias

This has a single input and a single output & a single layer.
Now, more complex neural network is going to have multiple inputs, multiple outputs
and multiple layers.

For eg. for a image of 64x64 pixels. The input is going to be the value of each
pixel, let's call it brightness. Suppose this is just a simple grayscale image.

So we have 64x64 = 4096 pixels as input. And we may have multiple layers as well.
Let's say we have two layers. The each neuron in the first layers is going to
take in 4096 inputs. The second layers let's say we have 1000 neurons. Now,
we have

`4096 * 1000 weights + 1000 biases = 4100096 parameters in the first layers`

Which is then going to go through a sigmoid function to give us the uniform
output from -1 to 1.

sigmoid function => 1 / 1 + e^(-x)

So the formulata is output_matrix => sigmoid(Weight Matrix * Input Matrix + bias matrix)

So let's say the second layer we have 100 neuron.
The outputs from the first layer is going to be the input for the second layers.
So we have 1000 weights + 1 bias for each neuron that means we have

`1000 * 100 + 100 = 100100 parameters for second layers.`

And the final layers let's has 10 neurons, saying which finally says which number

`100 * 10 + 10 = 1010 parameters in the final layer` 

So finally, we have 

`4100096 + 100100 + 1010 = 4,201,206 parameters total in our neural network.`


RelU = max(0, x) => This is the most popular replacement for the sigmoid function (This is called the activation function)


# Edit
I was wrong about one thing here. input data is also a layer. So in total we had 4 layers here.
