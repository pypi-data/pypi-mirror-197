import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

# Load and preprocess the dataset
data = open('data.txt').read()
tokenizer = Tokenizer()
tokenizer.fit_on_texts([data])
vocab_size = len(tokenizer.word_index) + 1
sequences = tokenizer.texts_to_sequences([data])[0]
sequences = np.array(sequences)
X, y = sequences[:-1], sequences[1:]
X = pad_sequences([X], maxlen=50, padding='pre')
y = pad_sequences([y], maxlen=50, padding='pre')
y = np.eye(vocab_size)[y]

# Define the neural network architecture
model = Sequential()
model.add(Embedding(vocab_size, 50, input_length=50))
model.add(LSTM(100, return_sequences=True))
model.add(LSTM(100))
model.add(Dense(100, activation='relu'))
model.add(Dense(vocab_size, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(X, y, batch_size=128, epochs=100)

# Evaluate the model
loss, acc = model.evaluate(X, y)
print('Loss:', loss)
print('Accuracy:', acc)

# Generate new sentences
seed_text = 'The quick brown fox'
for i in range(10):
    encoded = tokenizer.texts_to_sequences([seed_text])[0]
    encoded = pad_sequences([encoded], maxlen=50, padding='pre')
    yhat = model.predict_classes(encoded, verbose=0)
    out_word = ''
    for word, index in tokenizer.word_index.items():
        if index == yhat:
            out_word = word
            break
    seed_text += ' ' + out_word
print(seed_text)
