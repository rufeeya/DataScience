'''Problem Statement: You are working for a new-age insurance company and employ multiple outreach plans to sell term insurance to your customers.
Telephonic marketing campaigns still remain one of the most effective ways to reach out to people however they incur a lot of cost.
Hence, it is important to identify the customers that are most likely to convert beforehand so that they can be specifically targeted via call.
We are given the historical marketing data of the insurance company and are required to build a ML model that will predict if a client will subscribe to the insurance.

Features: ● age (numeric) ● job : type of job ● marital : marital status ● educational_qual : education status ● call_type : contact communication type
● day: last contact day of the month (numeric) ● mon: last contact month of year ● dur: last contact duration, in seconds (numeric)
● num_calls: number of contacts performed during this campaign and for this client
● prev_outcome: outcome of the previous marketing campaign (categorical: "unknown","other","failure","success")
Output variable (desired target): ● y - has the client subscribed to the insurance?

Problem Statements: https://drive.google.com/drive/folders/175l0_vdLyiVs-kxJpd1Os6NHykiGwlVi
'''

import numpy as np
import pandas as pd
import statistics as st

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb

# reading data from a .csv file to a Pandas DataFrame
df = pd.read_csv('Customer_Conversion_Prediction.csv')
pd.set_option('display.max_columns',None)
df.head()

#Encoding Categorical Variables

df['job'] = df['job'].map({'blue-collar':0,'management':1,'technician':2,'admin.':3,'services':4,'retired':5,'self-employed':6,'entrepreneur':7,'unemployed':8,'housemaid':9,'student':10,'unknown':11})
df['marital'] = df['marital'].map({'married':0,'single':1,'divorced':2})
df['education_qual'] = df['education_qual'].map({'primary':0,'secondary':1,'tertiary':2,'unknown':3})
df['call_type'] = df['call_type'].map({'cellular':0,'unknown':1,'telephone':2})
df['mon'] = df['mon'].map({'jan':0,'feb':1,'mar':2,'apr':3,'may':4,'jun':5,'jul':6,'aug':7,'sep':8,'oct':9,'nov':0,'dec':11})
df['prev_outcome'] = df['prev_outcome'].map({'success':0,'failure':1,'other':2,'unknown':3})
df['y'] = df['y'].map({'no':0,'yes':1})

#Split the data into input and output data
input = df.drop('y',axis=1)
output = df['y']

input_train, input_test, output_train, output_test = train_test_split(input,output,test_size=0.2,random_state=3378)

#Option - 1: Linear Regression - Fit and Predict

from sklearn.linear_model import LinearRegression 
linear_model=LinearRegression(fit_intercept=True) 
linear_model.fit(input_train, output_train) 
linear_output = linear_model.predict(input_test)

#Option - 2:  K Nearest Neighbor Regression - Fit and Predict

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(input_train)
input_train_scaled = scaler.transform(input_train)
input_test_scaled = scaler.transform(input_test)

knn_values=np.arange(1,50)
cross_val_knn=[]
for k in knn_values:
  knn_regressor=KNeighborsRegressor(n_neighbors=k)
  knn_regressor.fit(input_train_scaled,output_train)
  print("K value : ", k, " train score : ", knn_regressor.score(input_train_scaled,output_train)  ,"cross_val_score : ", cross_val_score(knn_regressor,input_train_scaled,output_train,cv = 10).mean())
  cross_val_knn.append(cross_val_score(knn_regressor,input_train_scaled,output_train,cv = 10).mean())
  
print("The Cross_val_score is",cross_val_knn_regressor )
  
#Implementing best Knearest neighbor
knn_regressor=KNeighborsRegressor(n_neighbors=27) #Best neighbor based on above prediction
knn_regressor.fit(input_train_scaled,output_train)
knn_output = knn_regressor.predict(input_test_scaled)

#Option - 3: Random Forest Regression

max_depth=np.array([2,4,8,10,11,12,13,15,18,20])
cross_val_rf=[]
for d in max_depth:
  rf_regressor=RandomForestRegressor(max_depth=d, random_state=0)
  rf_regressor.fit(input_train,output_train)
  print("Depth : ", d, "cross_val_score : ", cross_val_score(rf_regressor,input_train,output_train,cv = 15).mean())
  cross_val_rf.append(cross_val_score(rf_regressor,input_train,output_train,cv = 15).mean())
  
print("The cross value score is ", max(cross_val_rf))

rf_regressor=RandomForestRegressor(max_depth=4, random_state=0) #Best deth based on abov e prediction
rf_regressor.fit(input_train,output_train)
rfr_output = rf_regressor.predict(input_test)

#Option - 4: Extreme Gradient Boosting Regression

cross_val_xgb=[]
for lr in [0.01,0.05,0.08,0.09,0.1,0.11,0.12,0.13,0.15,0.18,0.2,0.25,0.3]:
  xgb_regressor= xgb.XGBRegressor(colsample_bytree=0.4,learning_rate = lr,n_estimators=1000) 
  xgb_regressor.fit(input_train,output_train) 
  print("Learning rate : ", lr,"cross_val_score:", cross_val_score(xgb_regressor,input_train,output_train,cv = 15).mean())
  cross_val_xgb.append(cross_val_score(xgb_regressor,input_train,output_train,cv = 15).mean())
  
print("The cross value score is ", max(cross_val_xgb))

xgb_regressor= xgb.XGBRegressor(learning_rate =0.01,n_estimators=100) # best learning rate based on above prediction
xgb_regressor.fit(input_train,output_train)
xgbr_output = xgb_regressor.predict(input_test)

#creatin separate dataframes for each model and append the predicted value of each model

input_test_linear_model = input_test.copy(deep=True)
input_test_knn_model = input_test.copy(deep=True)
input_test_rfr_model = input_test.copy(deep=True)
input_test_xgbr_model = input_test.copy(deep=True)

input_test_linear_model['predicted_value'] = linear_output
input_test_knn_model['predicted_value'] = knn_output
input_test_rfr_model['predicted_value'] = rfr_output
input_test_xgbr_model['predicted_value'] = xgbr_output

#Writing the predicted value of each model as CSV file
input_test_linear_model.to_csv('input_test_linear_model.csv')
input_test_knn_model.to_csv('input_test_knn_model.csv')
input_test_rfr_model.to_csv('input_test_rfr_model.csv')
input_test_xgbr_model.to_csv('input_test_xgbr_model.csv')

#Printing Max values
print("KNN: ",cross_val_knn_regressor)
print("Random Forest: ",max(cross_val_rf))
print("Extreme Gradient: ", max(cross_val_xgb))

'''
Based on above models, Random Forest model seem to be givng near appropriate prediction
'''
