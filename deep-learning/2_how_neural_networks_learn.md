We give the weights and biases random values initially.
Then we use labeled data as input and calculate the output.
The output is obviously going to be incorrect.
Then we use the actual output of the labeled data to caculate the error.
But the error is not enough. We can know how big or small the error is but that
is not going to help us find the correct weights & baises.
Here we use a gradient descent to calculate the values of weights & biases
so that the error is minimum.

How we deal with local minima and maxima? No idea until now.
But I think it's just that we use all the inputs and start at different places
in order to arrive at the lowest minima using all the random starting points.
