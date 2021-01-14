import numpy as np
import requests
import pandas as pd
import pypyodbc
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import warnings
import seaborn as sns
from sklearn.preprocessing import scale
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor 
import tensorflow
from tensorflow import keras
from keras.layers.core import Dense
from keras import Sequential
import sklearn.utils
sklearn.utils.safe_indexing = sklearn.utils._safe_indexing
from yellowbrick.model_selection import FeatureImportances
from yellowbrick.datasets import load_occupancy
from sklearn.ensemble import RandomForestClassifier



# connect to sql database
conn1 = pypyodbc.connect("Driver={SQL Server};"
                     "Server=DESKTOP-KOOIS0J;"
                     "Database=Horses;"
                     "Trusted_Connection=yes;",
                     autocommit=True)



#print(conn1)
#mycursor = conn1.cursor()

sql2 = ('''SELECT Betfairdata.*, horses.* FROM horses JOIN Betfairdata on Betfairdata.runnerName = horses.HorseName and Betfairdata.day = horses.DayCalender''')

#mycursor.execute(sql2)

#print(mycursor)

data1 = pd.read_sql(sql2, conn1)
#data1.columns.tolist()

results = pd.DataFrame(data1)
print(results)

#results1 = pd.concat([results, pd.get_dummies(results['venue'])], axis=1); df

dummyvenue = pd.get_dummies(results['venue'])



results = pd.concat([results, dummyvenue], axis=1)
#print(results1)
warnings.filterwarnings("ignore")


#np.random.seed(0)
feature_list = list(results)






print(feature_list)


#comment out because i know it works line 64-80
#for i in range(len(results['place'])):
    #temp = results.loc[ : (i + 1)][results.horsename == results.horsename[i]][['place']]
    #temp = temp['place'].values.tolist()[::-1]
    #print(temp)
 
   


    #if len(temp) != 0:
    #    temp_int = map(int, temp)
    #    temp_ave = np.mean(list(temp_int))
    #    results['recentaverank'][i] = temp_ave
    #    print(temp_ave)
    #if len(temp) != 0:
    #    temp_int = map(int, temp[:5])
    #    temp_ave5 = np.mean(list(temp_int))
    #    results['lastfiverank'][i] = temp_ave
    #    print(temp_ave5)
#

#results['Driver'] = driver
placer1 = results['place']
placer1 = str(results['place'])


print(placer1)
driver = results['driver'].unique()
trainer = results['trainer'].unique()
print(trainer)

#for i in range(len(driver)):

   # temp1 = results.loc[results.driver == results.driver[i]][['place']]
   # temp1 = temp1['place'].values.tolist()
   # print(temp1)

   # if len(temp1) != 0:
      #  temp_int = map(int, temp1)
     #   jockeywinave = np.mean(list(temp_int))
    #    print(jockeywinave)
        #results['jockeywin'][i] = jockeywinave
   # if len(temp1) != 0:
      #  temp_int = map(int, temp1[:10])
      #  jockeyrecentwinave = np.mean(list(temp_int))
     #   print(jockeyrecentwinave)
    #    results['recentjock'][i] = jockeyrecentwinave


#results2 = []        
#for i in range(len(trainer)):

    #temp2 = results.loc[results.trainer == results.trainer[i]][['place']]
    #temp2 = temp2['place'].values.tolist()
    #print(temp2)
    #if len(temp2) != 0:
        #temp_int2 = map(int, temp2)
        #trainerwinave = np.mean(list(temp_int2))
        #print(trainerwinave)
        #results['trainerwin'][i] = trainerwinave


    



#placer1 = results[(results.place == 1) | (results.place == 2) | (results.place == 3)] 

#print(placer1)

#index = results.index[results['place'] == '1'].tolist()




#results['recentaverank'].append(temp_ave)
#results['lastfiverank'].append(temp_ave5)

#results1 = pd.concat([results, pd.DataFrame(results, trainerwinave)], axis=1)

#results2 = results.merge(trainerwinave, how='outer').fillna(0)

#results2 = results['trainerwin'].append(trainerwinave)
#results['jockeywin'].append(jockeywinave)
#results['placer'].append(placer1)
# here is the problem converting

#newdata.assign(**{'Placer' : Placer})
#table1 = pd.DataFrame(results1, columns=['placer1'])


#sql1 = '''UPDATE horses (Placer) VALUES (?)'''


#mycursor.execute(sql1, Values)

#conn1.commit()




#feature_list['time1'] = pd.to_datetime(data['gross_time']).dt.time
#feature_list['time2'] = pd.to_datetime(data['mile_rate']).dt.time
#feature_list['time3'] = pd.to_datetime(data['lead_time']).dt.time
#feature_list['time4'] = pd.to_datetime(data['first_quarter']).dt.time
#feature_list['time5'] = pd.to_datetime(data['second_quarter']).dt.time
#feature_list['time6'] = pd.to_datetime(data['third_quarter']).dt.time
#feature_list['time7'] = pd.to_datetime(data['fourth_quarter']).dt.time




feature_list.remove('place')
#feature_list.remove('win_odds_bsp')
feature_list.remove('day')
feature_list.remove('raceno')
feature_list.remove('daycalender')
feature_list.remove('id')
feature_list.remove('venuename')
feature_list.remove('weather')
feature_list.remove('trackcondition')
feature_list.remove('runnername')
feature_list.remove('horsename')
feature_list.remove('racename')
feature_list.remove('racetitle')
feature_list.remove('trainer')
feature_list.remove('driver')
feature_list.remove('stewardscomments')
feature_list.remove('scratching')
feature_list.remove('trackrating')
feature_list.remove('row')
feature_list.remove('gross_time')
feature_list.remove('mile_rate')
feature_list.remove('lead_time')
feature_list.remove('first_quarter')
feature_list.remove('second_quarter')
feature_list.remove('third_quarter')
feature_list.remove('fourth_quarter')
feature_list.remove('venue')
#feature_list.remove('recentaverank')
#feature_list.remove('lastfiverank')
#feature_list.remove('trainerwin')
#feature_list.remove('jockeywin')
feature_list.remove('placer')
feature_list.remove('horseid')
#feature_list.remove('age')
feature_list.remove('colour')
feature_list.remove('sex')
#feature_list.remove('recentjock')
#feature_list.remove('recenttrain')
feature_list.remove('sire')

print(feature_list)
missing_count1 = results.isnull().sum()
print(missing_count1)




#x = np.sort(results1['win_odds_bsp'])

#y = np.arange(1, len(x)+1) / len(x)

#_ = plt.plot(x, y, marker = '.', linestyle = 'none')

#_ = plt.xlabel('')

#_ = plt.ylabel('ECDF')

#plt.margins(0.02)
#plt.show()



X = results[feature_list]
y = results['place']
print(X)
print(y)

#feature_list = scale(feature_list)

#X = np.array(X).reshape(-1, 1)
#y = np.array(y).reshape(-1, 1)


print(X.shape)
print(y.shape)

n_cols = X.shape[1]

#model = Sequential()

#model.add(Dense(50, activation='relu', input_shape=(n_cols, )))


#model.add(Dense(32, activation='relu'))

#model.add(Dense(1))

#model.compile(optimizer='adam', loss = 'mean_squared_error')

#model.fit(X, y)

#print("Loss function: " + model.loss)

#model.save('harness_file')

#print("model saved")

#print(model.summary())

#shap.initjs()

#explainer = shap.KernelExplainer(model.predict, X)
#shap_values = explainer.shap_values(X)

#print(explainer.shap_values(X))

#shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:])

#shap.summary_plot(shap_values, X, plot_type = "bar")

sql3 = ('''SELECT * FROM Field WHERE ''')



data3 = pd.read_sql(sql3, conn1)
#data1.columns.tolist()

results3 = pd.DataFrame(data3)

print(results3)

feature_list3 = list(results3)

feature_list3.remove('racenumber')
feature_list3.remove('racename')
feature_list3.remove('racedistance')
feature_list3.remove('venue')
feature_list3.remove('horsenumber')
feature_list3.remove('horsename')
feature_list3.remove('form')
feature_list3.remove('trainer')
feature_list3.remove('driver')
feature_list3.remove('horseclass')
feature_list3.remove('handicap')
feature_list3.remove('racetitle')
feature_list3.remove('row')
feature_list3.remove('horseid')

#array3 = np.array(feature_list3)

#print(array3)

#logreg = LogisticRegression()
#logreg.fit(X, y)
#print(logreg)

#predictions = model.predict(array3)

#print(predictions)

#predicted_prob_true = predictions

#print(predicted_prob_true)


#np.any(np.isnan(results))
#np.all(np.isfinite(results))
  

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, train_size=0.85)

#lm = LinearRegression()
#lm.fit(X_train, y_train)



#lmcoef1 = lm.coef_

#for i,v in enumerate(lmcoef1):
    #print('Feature: %0d, Score: %.5f' % (i,v))

#lm = LinearRegression()
#lm.fit(X_train, y_train)

# print(lmcoef1)
#predictions = lm.predict(X_test)

#print("Linear Regression Train score:")
#print(lm.score(X_train, y_train))

#print("Linear Regression Test score:")
#print(lm.score(X_test, y_test))

#logreg = LogisticRegression()
#logreg.fit(X, y)

#predictions = logreg.predict(X_test)

#print("Logistic Regression Train score:")
#print(logreg.score(X_train, y_train))

#print("Logistic Regression Test score:")
#print(logreg.score(X_test, y_test))

#lm = svm.SVR()
#lm.fit(X_train, y_train)

#predictions = lm.predict(X_test)

#print("SVR Train score:")
#print(lm.score(X_train, y_train))

#print("SVR Test score:")
#print(lm.score(X_test, y_test))

#lm = DecisionTreeClassifier()
#lm.fit(X_train, y_train)

#predictions = lm.predict(X_test)

#print("Decision Tree Train score:")
#print(lm.score(X_train, y_train))

#print("Decision Tree Test score:")
#print(lm.score(X_test, y_test))

#lm = KNeighborsClassifier()
#lm.fit(X_train, y_train)

#predictions = lm.predict(X_test)

#print("KNeighborsClassifier Train score:")
#print(lm.score(X_train, y_train))

#print("KNeighborsClassifier Test score:")
#print(lm.score(X_test, y_test))

#lm = LinearDiscriminantAnalysis()
#lm.fit(X, y)

#predictions = lm.predict(X_test)

#print("LinearDiscriminantAnalysis Train score:")
#print(lm.score(X_train, y_train))

#print("LinearDiscriminantAnalysis Test score:")
#print(lm.score(X_test, y_test))

#lm = GaussianNB()
#lm.fit(X_train, y_train)

#predictions = lm.predict(X_test)

#print("GaussianNB Train score:")
#print(lm.score(X_train, y_train))

#print("GaussianNB Test score:")
#print(lm.score(X_test, y_test))

#lm = SVC()
#lm.fit(X_train, y_train)

#predictions = lm.predict(X_test)

#print("SVC Train score:")
#print(lm.score(X_train, y_train))

#print("SVC Test score:")
#print(lm.score(X_test, y_test))
#X, y = load_occupancy()

#model1 = RandomForestClassifier(n_estimators = 10, random_state = 1)

#visualizer = FeatureImportances(model1)
#visualizer.fit(X, y)

#visualizer.score(X_test, y_test)

#visualizer.show()

newlist = pd.DataFrame(feature_list)

lm = RandomForestRegressor()
lm.fit(X_train, y_train)

predictions = lm.predict(X_test)

feat_importances = pd.Series(lm.feature_importances_, index=newlist.columns)
feat_importances.nlargest(4).plot(kind='barh')



plt.bar([x for x in range(len(importance))], importance)
plt.show()


predictions = lm.predict(X_test)

print("RandomForestRegressor Train score:")
print(lm.score(X_train, y_train))

print("RandomForestRegressor Test score:")
print(lm.score(X_test, y_test))



#conn1.commit()

