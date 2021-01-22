import pandas as pd
from collections import OrderedDict
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
import pickle

# connect to sql database
conn1 = pypyodbc.connect("Driver={SQL Server};"
                     "Server=DESKTOP-KOOIS0J;"
                     "Database=Horses;"
                     "Trusted_Connection=yes;",
                     autocommit=True)


sql2 = ('''SELECT Betfairdata.*, horses.* FROM horses JOIN Betfairdata on Betfairdata.runnerName = horses.HorseName and Betfairdata.day = horses.DayCalender''')


# load data from database
data1 = pd.read_sql(sql2, conn1)


# read dataset

dataframe = pd.DataFrame(data1)

# dataframe = pd.read_csv('dataset.csv')

# select important features from dataset
feature_df = dataframe[['day', 'raceno', 'venue', 'racedistance', 'horsename', 'row', 'trainer', 'driver', 'startingodds', 'handicap', 'age', 'placer']].copy()

# shuffle dataset
# feature_df = shuffle(feature_df)


# Label Encoding of feature and store them

# venue encoding
venue_le = LabelEncoder()
feature_df['venue'] = venue_le.fit_transform(feature_df['venue'])


with open("Venue_Encoder.pkl", 'wb') as venue_file:
    pickle.dump(venue_le, venue_file)
    venue_file.close()

# row encoding
horsename_le = LabelEncoder()
feature_df['horsename'] = horsename_le.fit_transform(feature_df['horsename'])
with open("HorseName_Encoder.pkl", 'wb') as horsename_file:
    pickle.dump(horsename_le, horsename_file)
    horsename_file.close()

# row encoding
row_le = LabelEncoder()
feature_df['row'] = row_le.fit_transform(feature_df['row'])


with open("Row_Encoder.pkl", 'wb') as row_file:
    pickle.dump(row_le, row_file)
    row_file.close()

# trainer encoding
trainer_le = LabelEncoder()
feature_df['trainer'] = trainer_le.fit_transform(feature_df['trainer'])


with open("Trainer_Encoder.pkl", 'wb') as trainer_file:
    pickle.dump(trainer_le, trainer_file)
    trainer_file.close()

# driver encoding
driver_le = LabelEncoder()
feature_df['driver'] = driver_le.fit_transform(feature_df['driver'])


with open("Driver_Encoder.pkl", 'wb') as driver_file:
    pickle.dump(driver_le, driver_file)
    driver_file.close()

print(feature_df.shape)


feature_df = feature_df.drop(columns=['day', 'raceno'])

feature_df.to_csv('feature engineering for top 3.csv', index=None)


