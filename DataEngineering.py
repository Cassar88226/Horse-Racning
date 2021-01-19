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

# select important features from dataset
feature_df = dataframe[['day', 'raceno', 'venue', 'racedistance', 'horseid', 'row', 'trainer', 'driver', 'handicap', 'age', 'place']].copy()

# shuffle dataset
feature_df = shuffle(feature_df)


# Label Encoding of feature and store them

# venue encoding
venue_le = LabelEncoder()
feature_df['venue'] = venue_le.fit_transform(feature_df['venue'])


with open("Venue_Encoder.pkl", 'wb') as venue_file:
    pickle.dump(venue_le, venue_file)
    venue_file.close()

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

# remove the rows which place is 0
index_names = feature_df[ feature_df['place'] == 0 ].index
feature_df.drop(index_names,inplace = True)
feature_df = feature_df.drop_duplicates()

print(feature_df.shape)


# Create Pivot table

# choose 2 features from race : venue and racedistance.
# choose 6 features from horses : horseid, row, trainer, driver, handicap, age
# maximum horse number of race is 19.
# total feature number of each race will be 6 * 19 + 2 = 116
group_df = feature_df.groupby(['day', 'raceno', 'venue', 'racedistance'])
print(group_df)
columns = ['venue', 'racedistance']
common_columns = ['horseid', 'row', 'trainer', 'driver', 'handicap', 'age']
max_number = 19
for i in range(1, max_number + 1):
    ith_columns = []
    for column in common_columns:
        ith_columns.append(column + str(i))
    columns += ith_columns
place_columns = []
for i in range(1, max_number + 1):
    place_columns.append('place' + str(i))

columns += place_columns


result_df = pd.DataFrame(columns = columns)

print(columns)

for group_name, df in group_df:
    # print(group_df)
    day, raceno, venue, racedistance = group_name
    item = OrderedDict()
    item['venue'] = venue
    item['racedistance'] = racedistance
    index = 1
    for i, row in df.iterrows():
        item['horseid' + str(index)] = row['horseid']
        item['row' + str(index)] = row['row']
        item['trainer' + str(index)] = row['trainer']
        item['driver' + str(index)] = row['driver']
        item['horseid' + str(index)] = row['horseid']
        item['handicap' + str(index)] = row['handicap']
        item['age' + str(index)] = row['age']
        item['place' + str(index)] = row['place']
        index += 1
    if index >= max_number:
        continue
    for index1 in range(index, max_number+1):
        item['horseid' + str(index1)] = 0
        item['row' + str(index1)] = 0
        item['trainer' + str(index1)] = 0
        item['driver' + str(index1)] = 0
        item['horseid' + str(index1)] = 0
        item['handicap' + str(index1)] = 0
        item['age' + str(index1)] = 0
        item['place' + str(index1)] = 0
    result_df = result_df.append(item, ignore_index = True)

result_df = result_df.fillna(0)


result_df.to_csv('feature selection.csv', index=None)


