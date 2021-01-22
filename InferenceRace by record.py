import pypyodbc
import pandas as pd
import numpy as np
import tensorflow as tf
import sklearn.preprocessing as preprocessing
import sklearn.model_selection as model_selection
import matplotlib.pyplot as plt
import keras
from keras.models import model_from_json
import pickle
from collections import OrderedDict
from datetime import datetime, timedelta

# connect to sql database
conn1 = pypyodbc.connect("Driver={SQL Server};"
                     "Server=DESKTOP-KOOIS0J;"
                     "Database=Horses;"
                     "Trusted_Connection=yes;",
                     autocommit=True)
today = datetime.today()
tomorrow = today + timedelta(days=1)
start_date = today.strftime("%Y-%m-%d")
end_date = tomorrow.strftime("%Y-%m-%d")

sql3 = ("SELECT * FROM Field WHERE CAST(DayCalender as date)>='{0}' and CAST(DayCalender as date)<='{1}'".format(start_date, end_date))
print(sql3)



data3 = pd.read_sql(sql3, conn1)
# #data1.columns.tolist()

future_races_df = pd.DataFrame(data3)
# future_races_df = pd.read_csv('dataset4(AutoRecovered).csv')
# load json and create model
model_json = 'model-32-64-32-8-1(all relu)-20210122-03-06.json'
json_file = open(model_json, 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

# load weights into new model
model_name = 'model-32-64-32-8-1(all relu)-20210122-03-06-epoch=35-val_loss=0.516928.hdf5'
model.load_weights(model_name)

# load MinMax scaler
scaler_name = 'MinMaxScaler.pkl'
mms = pickle.load(open(scaler_name, 'rb'))

# load LabelEncoder for Venue Name
venue_encoder_name = 'Venue_Encoder.pkl'
venue_le = pickle.load(open(venue_encoder_name, 'rb'))

# load LabelEncoder for row
row_encoder_name = 'Row_Encoder.pkl'
row_le = pickle.load(open(row_encoder_name, 'rb'))

# load LabelEncoder for Trainer
trainer_encoder_name = 'Trainer_Encoder.pkl'
trainer_le = pickle.load(open(trainer_encoder_name, 'rb'))

# load LabelEncoder for Driver
driver_encoder_name = 'Driver_Encoder.pkl'
driver_le = pickle.load(open(driver_encoder_name, 'rb'))

# load LabelEncoder for horsename
horsename_encoder_name = 'HorseName_Encoder.pkl'
horsename_le = pickle.load(open(horsename_encoder_name, 'rb'))

# choose the important features from dataframe
feature_df = future_races_df[['daycalender', 'racenumber', 'venue', 'racedistance', 'horsename', 'row', 'trainer', 'driver','startingodds', 'handicap', 'age']].copy()
feature_df = feature_df.rename(columns={"daycalender": "day", "racenumber": "raceno"})

orig_df = feature_df.copy()

# apply Encoders
# venue encoder
feature_df['venue'] = feature_df['venue'].map(lambda s: '<unknown>' if s not in venue_le.classes_ else s)
venue_le.classes_ = np.append(venue_le.classes_, '<unknown>')
feature_df['venue'] = venue_le.transform(feature_df['venue'])
# row encoder
feature_df['row'] = feature_df['row'].map(lambda s: '<unknown>' if s not in row_le.classes_ else s)
row_le.classes_ = np.append(row_le.classes_, '<unknown>')
feature_df['row'] = row_le.transform(feature_df['row'])
# trainer encoder
feature_df['trainer'] = feature_df['trainer'].map(lambda s: '<unknown>' if s not in trainer_le.classes_ else s)
trainer_le.classes_ = np.append(trainer_le.classes_, '<unknown>')
print(trainer_le.classes_)
feature_df['trainer'] = trainer_le.transform(feature_df['trainer'])
# driver encoder
feature_df['driver'] = feature_df['driver'].map(lambda s: '<unknown>' if s not in driver_le.classes_ else s)
driver_le.classes_ = np.append(driver_le.classes_, '<unknown>')
feature_df['driver'] = driver_le.transform(feature_df['driver'])

# horsename encoder
feature_df['horsename'] = feature_df['horsename'].map(lambda s: '<unknown>' if s not in horsename_le.classes_ else s)
horsename_le.classes_ = np.append(horsename_le.classes_, '<unknown>')
feature_df['horsename'] = horsename_le.transform(feature_df['horsename'])

test_df = feature_df.drop(columns=['day', 'raceno'])


# apply StandardScaler
test_x = pd.DataFrame(mms.transform(test_df),columns = test_df.columns)

# convert dataframe to numpy array
test_x = test_x.to_numpy()

# prediction
y_predictions = model.predict(test_x)
# print(y_predictions)

orig_df['probability'] = y_predictions * 100

orig_df.to_csv('Predict Result.csv', index=None)

