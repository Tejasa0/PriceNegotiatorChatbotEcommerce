import random
import math
import sklearn
from sklearn import preprocessing
from tensorflow.keras.preprocessing.sequence import pad_sequences
import string
import torch
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow import keras
import re

model1 = keras.models.load_model('model.h5')

import json
import pandas as pd
import numpy as np

# import model
# import train

with open('content.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

le = data["le"]
y_train = data["y_train"]
input_shape = data["input_shape"]
output_length = data["output_length"]
vocabulary = data["vocabulary"]
x_train = data["x_train"]
df = data["df"]
tag = data["tag"]
patterns = data["patterns"]
data1 = data["data"]
responses = data["responses"]
tokenizer = data["tokenizer"]

# model1=data["model"]

#
# def getInfo():
#     return [model1, le, input_shape, df, data, tag, patterns, responses]

import random
import math


# texts_p = []


def Isdigit(pred_inp):
    price_regex = r"\d+(?:\.\d+)?"
    match = re.search(price_regex, pred_inp)
    if match:
        price = match.group()
        return int(price)
    else:
        return False
    # numbers = []
    # for word in pred_inp.split():
    #     if word.isdigit():
    #         numbers.append(int(word))
    # if len(numbers) != 0:
    #     return numbers[0]
    # else:
    #     return False


class product():
    min_price = 0
    max_price = 0
    lower_bound = 0
    upper_bound = 0
    iterator = 0
    bot_price = 0
    id = ""
    prod_name = ""
    prod_desc=""

    def __init__(self, min_price, max_price, iterator, id, prod_name,prod_desc):
        self.min_price = min_price
        self.max_price = max_price
        self.lower_bound = min_price
        self.upper_bound = max_price
        self.iterator = iterator
        self.bot_price = max_price
        self.id = id
        self.prod_name = prod_name
        self.done = 0
        self.prod_desc=prod_desc

    def get_response(self, prediction_input=""):
        # if self.done == 1:
        #     return random.choice(responses["deal"])
        # resp1 = ""

        if str(prediction_input).lower() == 'yes':
            self.done = 1
            resp1 = random.choice(responses["goodbye"])
            return resp1

        elif Isdigit(prediction_input):
            prediction_input = Isdigit(prediction_input)

            if prediction_input < self.min_price:
                resp1 = random.choice(responses["incompatible"])
                return resp1
            if prediction_input < self.lower_bound:
                resp1 = random.choice(responses["dogla"])
                return resp1
            if prediction_input - self.lower_bound <= 2 and prediction_input != self.bot_price:
                self.lower_bound = prediction_input
                return "Please increase some price"
            else:
                if prediction_input >= self.bot_price:
                    self.bot_price = prediction_input
                    resp1 = "Deal for product " + str(self.id) + ", " + str(
                        self.prod_name) + " is finalized at " + str(
                        prediction_input) + " Please enter 'Yes' to process further"
                    return resp1
                elif int(prediction_input) >= self.lower_bound:
                    self.lower_bound = prediction_input
                self.upper_bound = self.bot_price

                self.bot_price = random.randint(
                    int(self.lower_bound + (self.upper_bound - 1 - self.lower_bound) * 60 / 100),
                    self.upper_bound)
            if prediction_input >= self.min_price and self.iterator >= 5:
                resp1 = "Deal for product " + str(self.id) + ", " + str(
                    self.prod_name) + " is finalized at " + str(
                    prediction_input) + " Please enter 'Yes' to process further"
            elif int(prediction_input) >= self.bot_price:
                resp1 = "Deal for product " + str(self.id) + "," + str(self.prod_name) + " : is finalized at " + str(
                    prediction_input) + " Please enter 'Yes' to process further"
                return resp1
            else:
                resp1 = random.choice(responses["final"]).format(str(self.bot_price))
            self.iterator = self.iterator + 1
            # resp1=str(self.lower_bound)

        else:
            texts_p = []
            # removing punctuation and converting to lowercase
            prediction_input = [letters.lower() for letters in prediction_input if letters not in string.punctuation]
            prediction_input = ''.join(prediction_input)
            texts_p.append(prediction_input)

            # tokenizing and padding
            prediction_input = tokenizer.texts_to_sequences(texts_p)
            prediction_input = np.array(prediction_input).reshape(-1)
            prediction_input = pad_sequences([prediction_input], input_shape)

            # getting output form model
            output = model1.predict(prediction_input)
            output = output.argmax()

            # finding right tag and predicting
            response_tag = le.inverse_transform([output])[0]
            if response_tag == "done":
                resp1 = "Deal for product " + str(self.id) + "," + str(self.prod_name) + " : is finalized at " + str(
                    self.bot_price) + " Please enter 'Yes' to process further"
                return resp1
            if response_tag == "proddetails":
                return self.prod_desc
            resp1 = random.choice(responses[response_tag])

        return resp1


def getId(id):
    min_price = 0
    max_price = 0
    id = id
    prod_name = "none"
    # print(df.iloc[0, 1])
    # print(id)
    for i in range(len(df)):
        if df.iloc[i, 1] == str(id):
            # op1 = df.iloc[i, 2]
            # op2 = " for price "
            max_price = int(df.iloc[i, 3])
            min_price = int(df.iloc[i, 4])
            # output = op1 + op2 + str(op3)
            # obj.upper_bound = int(op4)
            prod_name = df.iloc[i, 2]
            # obj.lower_bound = int(op4)
            # min_price = int(op4)
            # max_price = int(op3)
            id = df.iloc[i, 1]
            prod_desc=df.iloc[i,5]
            # obj.bot_price = int(op3)
            break
    obj = product(min_price, max_price, 0, id, prod_name,prod_desc)

    return obj


product_actual_id = ''
if __name__ == "__main__":
    pass
    # obj = product(730, 1500, 0)
    #
    # while True:
    #     prediction_input = input('You : ')
    #
    #
    #     resp = get_response(prediction_input,id)
    #     print(resp)
