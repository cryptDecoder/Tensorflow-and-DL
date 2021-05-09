# Standard import here!
import json
import os
import pickle
import random

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import nltk
from rich.console import Console

console = Console()
from nltk.stem import WordNetLemmatizer
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

nltk.download('punkt')
nltk.download('wordnet')
lemitizer = WordNetLemmatizer()

intents = json.loads(open("intents.json").read())

words = []
classess = []
documents = []
ignore_letters = ["?", ".", ",", "!"]

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classess:
            classess.append(intent['tag'])
console.log("Lets lemmatize the words")
words = [lemitizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))
classess = sorted(set(classess))
print(classess)
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classess, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classess)  # convert classes into number form
console.log("Create classes and labels of data")
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemitizer.lemmatize(word.lower()) for word in word_patterns]
    print(word_patterns)
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classess.index(document[1])] = 1
    training.append([bag, output_row])

console.log("Data preparation for neural network")
random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

console.log("Create neural network model")
model = Sequential()
console.log("Adding Dense layers to the model")
console.log("First Dense layer with 128 neurons")
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
console.log("Second Layer with 64 neurons")
model.add(Dense(64, activation='relu'))
console.log("Final layer with training data  softmax activation")
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
console.log("Compile the model")
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

console.log("Fitting the model with training data...")
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
console.log("Saving the model..")
model.save('HelloAI_model.h5', hist)
console.print("Done!!!!!")
