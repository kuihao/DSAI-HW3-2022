import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras import Model

timestep = 7
n_feature = 1
ipt = tf.keras.Input(shape=(timestep,n_feature))
x = LSTM(64, activation='sigmoid', batch_input_shape=(None, ))(ipt)
opt = Dense(1, activation='sigmoid')(x)
model = Model(inputs=ipt, outputs=opt)

import pandas as pd
import numpy as np

TrainData_df = pd.read_csv('./sample_data/consumption.csv')
TrainData_np = TrainData_df['consumption'].to_numpy()

# Make training dataset
X = np.zeros((160, 7))
Y = np.zeros((160, 1))
for i in range(len(TrainData_np)-8):
  X[i] = TrainData_np[i:i+7]
  Y[i] = TrainData_np[i+8]

model.compile(optimizer='rmsprop',
              loss='mse')

#print(X.shape, Y.shape)

model.fit(X[:np.newaxis], Y[:np.newaxis], batch_size=16, epochs=100, validation_split=0.2)
model.save('./model/lstm_model')