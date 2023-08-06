import random
import csv


def preprocessorx(list):
    import random

    my_list = list

    used_numbers = []

    for i in range(len(my_list)):
        if my_list[i] in used_numbers:
            continue
        else:
            random_number = random.randint(1, 10000)
            while random_number in used_numbers:
                random_number = random.randint(1, 10000)
            my_list[i] = str(random_number)
            used_numbers.append(random_number)

    print(my_list)


import json

def extractor(text):
    text = text.split("\n")
    text = [s.split(" ") for s in text]
    words = []
    for sentence in text:
        for word in sentence:
            words.append(word)
    return words

def preprocessor(words):
    used_values = {}
    output = {}
    for word in words:
        if word in used_values:
            output[word] = used_values[word]
        else:
            value = round(random.uniform(0, 1), 8)
            used_values[word] = value
            output[word] = value

    with open('preprocessed_fr_eng.json', 'w') as f:
        json.dump(output, f)

#with open('input.txt', 'r') as f:
    #text = f.read()

#words = extractor(text)
#preprocessor(words)
import numpy as np

# Sigmoid activation function
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

# Derivative of sigmoid function
def sigmoid_derivative(x):
    return sigmoid(x) * (1.0 - sigmoid(x))

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize weights
        self.weights1 = np.random.rand(self.input_size, self.hidden_size)
        self.weights2 = np.random.rand(self.hidden_size, self.output_size)

    def feedforward(self, X):
        # Propagate input through the network
        self.hidden_layer = sigmoid(np.dot(X, self.weights1))
        self.output_layer = sigmoid(np.dot(self.hidden_layer, self.weights2))
        return self.output_layer

    def backpropagation(self, X, y, learning_rate):
        # Calculate errors and deltas for each layer
        output_error = y - self.output_layer
        output_delta = output_error * sigmoid_derivative(self.output_layer)

        hidden_error = np.dot(output_delta, self.weights2.T)
        hidden_delta = hidden_error * sigmoid_derivative(self.hidden_layer)

        # Update weights with deltas and learning rate
        self.weights2 += learning_rate * np.dot(self.hidden_layer.T, output_delta)
        self.weights1 += learning_rate * np.dot(X.T, hidden_delta)

    def train(self, X, y, learning_rate, epochs):
        for i in range(epochs):
            # Feedforward through the network

            output = self.feedforward(X)

            # Backpropagation to update weights
            self.backpropagation(X, y, learning_rate)
            print("Iterating Epoch :", i,"/",epochs)

    def predict(self, X):
        # Predict output for new input
        return self.feedforward(X)


def preprocess(text):
    # Convert text to lowercase and split into words
    words = text.lower().split()

    # Create dictionary mapping each unique word to a unique integer index
    word_to_index = {word: i for i, word in enumerate(set(words))}

    # Convert each word in the text to its corresponding integer index
    indices = [word_to_index[word] for word in words]

    # Convert integer indices to one-hot vectors
    num_words = len(word_to_index)
    input_vectors = np.zeros((len(indices), num_words))
    input_vectors[np.arange(len(indices)), indices] = 1

    return input_vectors, word_to_index


# Define neural network class
class NeuralNetwork2:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        # Initialize weights
        self.weights1 = np.random.rand(self.input_size, self.hidden_size)
        self.weights2 = np.random.rand(self.hidden_size, self.output_size)

    def feedforward(self, X):
        # Propagate input through the network
        self.hidden_layer = sigmoid(np.dot(X, self.weights1))
        self.output_layer = sigmoid(np.dot(self.hidden_layer, self.weights2))
        return self.output_layer

    def backpropagation(self, X, y, learning_rate):
        # Calculate errors and deltas for each layer
        output_error = y - self.output_layer
        output_delta = output_error * sigmoid_derivative(self.output_layer)

        hidden_error = np.dot(output_delta, self.weights2.T)
        hidden_delta = hidden_error * sigmoid_derivative(self.hidden_layer)

        # Update weights with deltas and learning rate
        self.weights2 += learning_rate * np.dot(self.hidden_layer.T, output_delta)
        self.weights1 += learning_rate * np.dot(X.T, hidden_delta)

    def train(self, X, y, learning_rate, epochs):
        for i in range(epochs):
            # Feedforward through the network
            output = self.feedforward(X)

            # Backpropagation to update weights
            self.backpropagation(X, y, learning_rate)
            print("Iterating Epoch: ", i, " / ", epochs)

    def predict(self, X):
        # Predict output for new input
        return self.feedforward(X)


