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
model_json = 'model-128-256-512-256-128-64-19(all relu)-20210119-15-20.json'
json_file = open(model_json, 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)

# load weights into new model
model_name = 'model-128-256-512-256-128-64-19(all relu)-20210119-15-20-epoch=122-val_loss=0.046502.hdf5'
model.load_weights(model_name)

# load standard scaler
scaler_name = 'StandardScaler.pkl'
ss = pickle.load(open(scaler_name, 'rb'))

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


# choose the important features from dataframe
feature_df = future_races_df[['daycalender', 'racenumber', 'venue', 'racedistance', 'horseid', 'horsename', 'row', 'trainer', 'driver', 'handicap', 'age']].copy()
feature_df = feature_df.rename(columns={"daycalender": "day", "racenumber": "raceno"})

# apply Encoders
# venue encoder
feature_df['venue'] = venue_le.transform(feature_df['venue'])
# row encoder
feature_df['row'] = row_le.transform(feature_df['row'])
# trainer encoder
feature_df['trainer'] = trainer_le.transform(feature_df['trainer'])
# driver encoder
feature_df['driver'] = driver_le.transform(feature_df['driver'])

# remove duplicated rows
feature_df = feature_df.drop_duplicates()


# Create Pivot table

# create test dataframe to predict 
# choose 2 features from race : venue and racedistance.
# choose 6 features from horses : horseid, row, trainer, driver, handicap, age
# total feature number of each race will be 6 * 19 + 2 = 116

# create extended dataframe to display probabilities
# choose 2 features from race : race date, venue and racedistance.
# choose 6 features from horses : horseid, horsename, row, trainer, driver, handicap, age
# total feature number of each race will be 6 * 19 + 2 = 116
# initialize the probabilities of horse finising 1'st

group_df = feature_df.groupby(['day', 'raceno', 'venue', 'racedistance'])
print(group_df)

columns = ['venue', 'racedistance']
extend_columns = ['venue', 'racedistance', 'day']
common_columns = ['horseid', 'row', 'trainer', 'driver', 'handicap', 'age']
extend_common_columns = ['horseid', 'horsename', 'row', 'trainer', 'driver', 'handicap', 'age']

max_number = 19
for i in range(1, max_number + 1):
    ith_columns = []
    for column in common_columns:
        ith_columns.append(column + str(i))
    columns += ith_columns
test_df = pd.DataFrame(columns = columns)


for i in range(1, max_number + 1):
    ith_columns = []
    for column in extend_common_columns:
        ith_columns.append(column + str(i))
    extend_columns += ith_columns

place_columns = []
for i in range(1, max_number + 1):
    place_columns.append('place' + str(i))
extend_columns += place_columns

extend_df = pd.DataFrame(columns = extend_columns)
print(extend_columns)


for group_name, df in group_df:
    # print(group_df)
    day, raceno, venue, racedistance = group_name
    ext_item = OrderedDict()
    item = OrderedDict()
    ext_item['venue'] = item['venue'] = venue
    ext_item['racedistance'] = item['racedistance'] = racedistance
    ext_item['day'] = day
    index = 1
    
    for i, row in df.iterrows():
        ext_item['horseid' + str(index)] = item['horseid' + str(index)] = row['horseid']
        ext_item['row' + str(index)] = item['row' + str(index)] = row['row']
        ext_item['trainer' + str(index)] = item['trainer' + str(index)] = row['trainer']
        ext_item['driver' + str(index)] = item['driver' + str(index)] = row['driver']
        ext_item['horseid' + str(index)] = item['horseid' + str(index)] = row['horseid']
        ext_item['handicap' + str(index)] = item['handicap' + str(index)] = row['handicap']
        ext_item['age' + str(index)] = item['age' + str(index)] = row['age']
        ext_item['horsename' + str(index)] = row['horsename']
        index += 1
    ext_item['horsecnt'] = index - 1
    if index >= max_number:
        continue
    for index1 in range(index, max_number+1):
        ext_item['horseid' + str(index1)] = item['horseid' + str(index1)] = 0
        ext_item['row' + str(index1)] = item['row' + str(index1)] = 0
        ext_item['trainer' + str(index1)] = item['trainer' + str(index1)] = 0
        ext_item['driver' + str(index1)] = item['driver' + str(index1)] = 0
        ext_item['horseid' + str(index1)] = item['horseid' + str(index1)] = 0
        ext_item['handicap' + str(index1)] = item['handicap' + str(index1)] = 0
        ext_item['age' + str(index1)] = item['age' + str(index1)] = 0
    test_df = test_df.append(item, ignore_index = True)
    extend_df = extend_df.append(ext_item, ignore_index = True)
test_df = test_df.fillna(0)
extend_df = extend_df.fillna(0)

# apply StandardScaler
test_x = pd.DataFrame(ss.transform(test_df),columns = test_df.columns)

# convert dataframe to numpy array
test_x = test_x.to_numpy()

# prediction
y_predictions = model.predict(test_x)

# normalize the prediction due to horse number of each race
index = 0
for i, row in extend_df.iterrows():
    horsecnt = int(row['horsecnt'])
    p_sum = sum(y_predictions[index][0:horsecnt])
    for j in range(1, horsecnt+1):
        extend_df.loc[i, 'place' + str(j)] = y_predictions[index][j-1] * 100 / p_sum
    index += 1

# Display the probabilities of horse for each race
for i, row in extend_df.iterrows():
    print("Race Date : " + row['day'])
    venue = venue_le.inverse_transform([int(row['venue'])])[0]
    print("Venue Name : " + venue)
    print("Distance : " + str(row['racedistance']))
    horsecnt = int(row['horsecnt'])
    for index in  range(1, horsecnt+1):
        horsename = row['horsename' + str(index)]
        place = round(row['place' + str(index)],1)
        print("\t" + row['horsename' + str(index)] + "\t : " + str(place))