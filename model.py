from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, GlobalMaxPooling1D, Flatten
from tensorflow.keras.models import Model

# creating model
class ModelC:
    def __init__(self, input_shape=0, output_length=0, vocabulary=0):
        i = Input(shape=(input_shape,))
        x = Embedding(vocabulary + 1, 10)(i)
        x = LSTM(10, return_sequences=True)(x)
        flatten_ = Flatten()(x)
        x = flatten_
        x = Dense(output_length, activation="softmax")(x)
        self.model = Model(i, x)

    def getmodel(self):
        return self.model
