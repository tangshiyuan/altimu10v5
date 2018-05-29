import model_function
import math
import os
import time
import numpy as np
import pandas as pd

from keras.models import load_model
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler

# load model
lstm_model = load_model('20180529-144437/gait_lstm.73-0.37511-0.35151.h5')
lstm_model.summary()

# load scaler
predict_scaler = joblib.load('scaler.save')

# prepare data
look_back = 25
n_features = 8

# load sample dataset
df = pd.read_csv("R_predictAct.csv",header=0, index_col=0)
df.reset_index(level=0, inplace=True)
dataset = df.filter(items=['accX_L','accY_L','accZ_L','total_acc_L','accX_R','accY_R','accZ_R','total_acc_R'])
predict_df = dataset[25:25+1+look_back]

predict_values = predict_df.values

# ensure all data is float
predict_values = predict_values.astype('float32')
# normalize features
#scaler = MinMaxScaler(feature_range=(0, 1))
scaled_predict = predict_scaler.transform(predict_values)

# frame as supervised learning
reframed_predict = model_function.series_to_supervised(scaled_predict, look_back, 1) #look back window of 25
# drop columns we don't want to predict
#reframed.drop(reframed.columns[[9,10,11,12,13,14,15]], axis=1, inplace=True)
reframed_predict.head()

# reshape input to be 3D [samples, timesteps, features]
reframed_predict = reframed_predict.values.reshape((reframed_predict.shape[0], look_back+1, n_features))

# predict
prediction = lstm_model.predict(reframed_predict).argmax(axis=1)
print('Prediction:', prediction[0])
