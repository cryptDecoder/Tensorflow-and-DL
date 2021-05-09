"""
    This is training model python file
"""
# standard import here!

import datetime
import json
import os
import pickle

import nltk
from rich.console import Console

datetime = datetime.datetime.utcnow()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

console = Console()
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import numpy as np
from BotMain import animText
import random

console.log("if required download nltk ")
nltk.download('punkt')
nltk.download('wordnet')


def train_nlp_model():
    lemmatizer = WordNetLemmatizer()

    console.log("Reading chatbot dataset...")
    dataset = json.loads(open('dataset.json').read())
    console.log("Reading dataset done!")

    console.log("Let's tokenize the dataset...")
    words = []  # create a wordlist of dataset
    classes = []  # create a classes (greeting,goodbye,calender)
    documents = []  # creaye a list with class and words
    ignore_letters = [",", '?', '.', "!"]  # ignore the letters
    console.log("Preparing dataset in documents and classes form")
    for intent in dataset['dataset']:
        for pattern in intent['patterns']:
            word_list = nltk.word_tokenize(pattern)
            words.extend(word_list)
            documents.append((word_list, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])
    console.log("let's Lemmatize the words (charge,charging,charged)")
    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
    words = sorted(set(words))
    classes = sorted(set(classes))
    # console.log(f"lemmatize words {words}", end='')
    # pickling the data => pickle is used to serialize and de-serialize the data\
    console.log("Pickling the data for serialization and de-serialization")
    pickle.dump(words, open('words.pkl', 'wb'))
    pickle.dump(classes, open('classes.pkl', 'wb'))

    # training the nlp model
    console.log("Let's begin the main game of NLP, Start the training model")
    training = []
    output_empty = [0] * len(classes)
    console.log(output_empty)
    console.log("Create class and labels of dataset")
    for doc in documents:
        wordBag = []
        word_patterns = doc[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            wordBag.append(1) if word in word_patterns else wordBag.append(0)
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([wordBag, output_row])
    console.log("Data preparation for neural network")
    random.shuffle(training)
    training = np.array(training)
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    console.log("Creating neural network..")
    model = Sequential()
    console.log("Adding first Dense layer..")
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    console.log("Adding second Dense layer..")
    model.add(Dense(64, activation='relu'))
    console.log("Preparing final layer..")
    model.add(Dense(len(train_y[0]), activation='softmax'))

    console.log("Add optimizer to the model..")
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    console.log("Compile the model..")
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    console.log('And finally we are in final stage fit model and save!')
    hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
    console.log("Saving the model")
    model.save("HelloAI.h5", hist)
    console.log("Model trained and saved successfully")
    animText("Yesss!!!! WE did that !!!!!!!")


if __name__ == '__main__':
    train_nlp_model()
