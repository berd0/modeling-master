#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: tom verguts
does estimation of weights for RL purposes in TF2
note that action is separate from estimation; only the estimation part is thus optimal

"""

#%% imports and initializations
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

learning_rate = 0.1
n_rep = 10
epochs = 10 # how often to go through the whole data set
p = np.array([0.2, 0.4, 0.6, 0.8])  # payoff probabilities
train_x = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]) # four responses (bandits)
test_x  = train_x
train_x_sample = np.tile(train_x, (n_rep, 1))
train_y = np.random.uniform(size = train_x_sample.shape[0])
train_y = (train_y[:, np.newaxis] < np.tile(p[:, np.newaxis], (n_rep, 1)))*1
train_y = train_y.reshape(train_y.size, 1)

model = tf.keras.Sequential([
			tf.keras.Input(shape=(train_x.shape[1],)),
			tf.keras.layers.Dense(1, activation = "sigmoid")
			] )
model.build()

#%% main code
opt = tf.keras.optimizers.Adam(learning_rate = learning_rate)
model.compile(optimizer = opt, loss=tf.keras.losses.MeanSquaredError())
history = model.fit(train_x_sample, train_y, batch_size = 1, epochs = epochs)
model.summary()
test_data = model.predict(test_x)

#%% show results
# error curve
plt.plot(history.history["loss"], color = "black")

# weights
print("predictions on the test data:")
print(model.layers[0].weights)