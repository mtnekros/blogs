# Transformer Model: Model that powers chatGPT

## Components of transformers
1. Word Embedding
Transformer is just a type of neural network. And neural network only takes
numbers as input values. So word embedding helps us to convert our words into
numbers. Both the input words and output words. 

    * Tokens: vocabulary can be mix of words, symbols and word-fragments. Each
      token has to be converted to number.
    * Let’s go <EOS> => 3 tokens
    * The whole sentences goes through a network to determine the weights.
      (research more about word embedding here!). From what I understood, we are
      not only converting a single word to a some random number. But it is done
      in relation to the other words present in the sentence. So when forming
      the network to convert the token to a number, all the tokens are taken
      into consideration. Actually all the tokens in a sentences has to be an
      input in the neural networks. So it makes sense that the network will
      include all the inputs .i.e. All the tokens.
    * Back propagation for calculating the weights.
    * More here: https://www.youtube.com/watch?v=viZrOnJclY0

## Word Order (Positional Embedding):
Position of the words is important when understanding a sentence. “Ram ate the
apple” and “The apple ate Ram” has completely different meanings. Positional
encoding is a technique used by transformers to track word order.	

    * Single word gets many embedding (thousands even) ??? (embedding of each
      words is solely related to the word not the position)
    * Each embedding for each token will be assigned a position values.
    * If we have four embeddings for a word, we need 4 alternating sines and
      cosines function of increasingly wider wavelength to calculate the
      positional values. (Positional values are not related to the words, just
      the position of the words)
    * Lastly, add embedding values to positional values, we get the positional
      encoding for the entire sentence. By combining both we get positional
      encoding. Cosine Simiarity: https://www.youtube.com/watch?v=e9U0QAFbfLI

## Self-Attention
Calculates similarity between every word including itself in the sentence.
* I squeezed the lotion out of the packet and rubbed it on my wound.
The model needs a way to understand that *it* in that sentence is associated to
the lotion instead of the packet. Although you could rub the packet on the
wound, that doesn't make much sense.

More on attention here: https://www.youtube.com/watch?v=PSs6nxngL6k
Decoder Embedding
Continue here:https://youtu.be/zxQyTK8quyY?t=1258

Complete playlist: https://www.youtube.com/playlist?list=PLblh5JKOoLUIxGDQs4LFFD--41Vzf-ME1

Building ChatGPT from Scratch: https://www.youtube.com/watch?v=kCc8FmEb1nY

TODO: just ask chat gpt for deep explanation on transformer model

