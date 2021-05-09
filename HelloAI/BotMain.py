"""
    Title : HelloAI is the natural language processing audion and chat enables bot developed by using tensorflow.
    Desc: In this bot i have given two opens to do conversion with HellpAI bot
        1. Text Based => you can ask your question using text based query
        2. Audio Based => yess!!! we have audio based HelloAI bot you can directly talk to the chat bot using audio interface
    Author: Pruthviraj Sonwane
"""
# Standard import here!!!
import datetime
import json
import os
import pickle
import random
import time

import nltk
import numpy as np
from cfonts import render
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

from mathematics import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
console = Console()
lemmatizer = WordNetLemmatizer()
dataset = json.loads(open('dataset.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('HelloAI.h5')


def cleanUp_message(message):
    message_word = nltk.word_tokenize(message)
    message_word = [lemmatizer.lemmatize(word) for word in message_word]
    return message_word


def wordBag(message):
    message_word = cleanUp_message(message)
    bag = [0] * len(words)
    for w in message_word:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict(message):
    bow = wordBag(message)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    result = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    result.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in result:
        return_list.append({'dataset': classes[r[0]], 'probabilty': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    try:
        tag = intents_list[0]['dataset']
        list_intents = intents_json['dataset']
        for i in list_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
    except IndexError:
        result = "sorry, I don't understand you please try again"
    return result


def animText(message):
    color = ['red', 'yellow', 'blue', 'green', 'cyan', 'Purple']

    for character in message:
        random.shuffle(color)
        console.print(character, end='', style=f'{color[0]} bold')
        time.sleep(0.05)


def helloAI():
    logo = render("Hello AI", align='left', font='chrome', colors=['red', 'blue', 'yellow'], background='transparent',
                  transition=True, space=False)
    print(logo)
    animText("Hey!, I am here. \n")
    animText("Yeess!!! we are online now \n")
    tDate = datetime.datetime.now()
    while True:
        message = input("Ask something >>> \n")
        ints = predict(message)
        res = get_response(ints, dataset)

        if message.__contains__('date') or message.__contains__('time'):
            animText(res + "\n")
            console.print(tDate, style='green bold')
        elif message.__contains__('add') or message.__contains__('addition') or message.__contains__('sum'):
            animText(res + "\n")
            console.print(add())
        elif message.__contains__('sub') or message.__contains__('subtraction') or message.__contains__('minus'):
            animText(res + "\n")
            console.print(subtraction())
        elif message.__contains__('mul') or message.__contains__('multiplication') or message.__contains__('mult'):
            animText(res + "\n")
            console.print(multiplication())
        elif message.__contains__('div') or message.__contains__('division') or message.__contains__('divide'):
            animText(res + "\n")
            console.print(division())
        else:
            animText(res + "\n")
    pass


if __name__ == '__main__':
    helloAI()
