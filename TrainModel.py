# import Libraries
# pandas: for data reading and preprocessing
# keras: for neural network construction
# sklearn.preprocessing: for data encoding
# sklearn.model_selection: it has convenient method for training/test data spliting
# matplotlib.pyplot: to plot performance of the training process.

import pandas as pd
import numpy as np
import tensorflow as tf
import sklearn.preprocessing as preprocessing
import sklearn.model_selection as model_selection
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers.core import Activation
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras.layers import Flatten
from keras.layers import Input
from keras.models import Model
from keras.optimizers import SGD
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
import pickle

# Read Dataset
# from feature engineering stage
dataset = pd.read_csv('feature selection.csv', index_col=False)
print(dataset.head())

# Prepare training/test data
# Select right columns for X, y
    # select all the data except last 19 columns, because last 19 columns are is about 'place'
    # Select last 19 columns for y
# Split data into train/test sets
    # 80% for training
    # 20% for testing(validation)

# convert target data(from place1 to place19) to won or loss(1 or 0)
y = dataset[dataset.columns[-19:]].applymap(lambda x: 1.0 if 0.5 < x < 1.5 else 0.0)

# scaling X data
ss = preprocessing.StandardScaler()
X = pd.DataFrame(ss.fit_transform(X),columns = X.columns)

# save scaler
with open("StandardScaler.pkl", 'wb') as scaler_file:
    pickle.dump(ss, scaler_file)
    scaler_file.close()

# convert dataframe to numpy list

X = X.to_numpy()
y = y.to_numpy()

print(X.shape)
print(y.shape)

# split data into train and test sets
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, train_size=0.9, test_size=0.1, random_state=1)

print(X_train.shape)

# Build the model
# Use keras to build the model with easy-to-use api Sequential
# Have to mention that input layer has 116 inputs. The calculation is following:

    # 2 features from race data - venuename, racedistance
    # 19 horses has 6 features - horseid,row, trainer, driver, handicap, age
# Output layer has 19 nodes

# create model
model = Sequential()
model.add(Dense(128, input_dim=X_train.shape[1], kernel_initializer='normal', activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(512, kernel_initializer='normal', activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(128, kernel_initializer='normal', activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64, kernel_initializer='normal', activation='relu'))
model.add(Dense(19))
# initialize the optimizer
opt = Adam(lr=0.00001)
# opt = SGD(lr=0.01, nesterov=True, momentum=0.9)
# Compile model
model.compile(loss='mse', optimizer=opt)

print(model.summary())



# Train the model

from datetime import datetime
cur_date_time = datetime.strftime(datetime.now(), '%Y%m%d-%H-%M')
model_weight_name = 'model-128-256-512-256-128-64-19(all relu)-' + cur_date_time + '-' + 'epoch={epoch:02d}-val_loss={val_loss:.6f}.hdf5'
model_structure_name = 'model-128-256-512-256-128-64-19(all relu)-' + cur_date_time + '.json'
print(model_weight_name)

# create model checkpoint
from keras.callbacks import ModelCheckpoint
checkpoint = ModelCheckpoint(model_weight_name, monitor='val_loss', mode='min', save_best_only=True, verbose=1)

#set early stopping monitor so the model stops training when it won't improve anymore
early_stopping_monitor = EarlyStopping(patience=5)
#train model
H = model.fit(X_train, y_train, validation_split=0.2, epochs=200, callbacks=[checkpoint], batch_size=16)

# save the model structure into json format
model_json = model.to_json()
with open(model_structure_name, 'w') as json_file:
    json_file.write(model_json)

# display train-test loss curve
plt.plot(H.history['loss'], label='train')
plt.plot(H.history['val_loss'], label='test')
plt.legend()
plt.show()