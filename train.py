from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, GlobalMaxPooling1D, Flatten
import random
import math
import sklearn
import model
import torch
from sklearn import preprocessing
from tensorflow.keras.preprocessing.sequence import pad_sequences
import string
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.text import Tokenizer

import nltk
import json
import pandas as pd
import numpy as np
import tensorflow as tf
from flask import Flask, request, render_template, jsonify

df = pd.read_csv("ProductDetails.csv")
df = df.drop(['uniq_id'], axis=1)
df.rename(columns={'uniq_id.1': 'uniq_id'}, inplace=True)
result = ''
text1 = ''
with open('content.json') as content:
    data1 = json.load(content)
tag = []
patterns = []
responses = {}
for intent in data1['intents']:
    responses[intent['tag']] = intent['responses']
    for lines in intent['patterns']:
        patterns.append(lines)
        tag.append(intent['tag'])
data = pd.DataFrame({"patterns": patterns, "tag": tag})
# removing punctuation
data['patterns'] = data['patterns'].apply(
    lambda wrd: [ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
data['patterns'] = data['patterns'].apply(lambda wrd: ''.join(wrd))
# tokenize data
tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data['patterns'])
print(data['patterns'])
train = tokenizer.texts_to_sequences(data['patterns'])

print(train)
# apply padding
x_train = pad_sequences(train)
print(x_train)
# encoding
le = preprocessing.LabelEncoder()
y_train = le.fit_transform(data['tag'])
print(data['tag'])
input_shape = x_train.shape[1]
vocabulary = len(tokenizer.word_index)
print(tokenizer.word_index)
print(input_shape)
print("........")
print(y_train)
print("........")
print(vocabulary)
print("........")
output_length = le.classes_.shape[0]
print(le.classes_)
print(output_length)
obj = model.ModelC(input_shape, output_length, vocabulary)
model1 = obj.getmodel()

model1.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
model1.fit(x_train, y_train, epochs=400)

data1 = {
    "le": le,
    "y_train": y_train,
    "input_shape": input_shape,
    "output_length": output_length,
    "vocabulary": vocabulary,
    "x_train": x_train,
    "df": df,
    "tag": tag,
    "patterns": patterns,
    "data": data,
    "responses": responses,
    "tokenizer": tokenizer
    # "model": model1
}
FILE = "data.pth"
torch.save(data1, FILE)

model1.save("model.h5")
print(df)
