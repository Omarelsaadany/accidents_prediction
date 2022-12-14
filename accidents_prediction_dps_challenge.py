# -*- coding: utf-8 -*-
"""accidents_prediction_DPS_CHALLENGE.ipynb



pip install colab-convert

colab-convert accidents_prediction_DPS_CHALLENGE.ipynb accidents_prediction_DPS_CHALLENGE.py

import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error

"""Read the data set"""

url = 'https://opendata.muenchen.de/dataset/5e73a82b-7cfb-40cc-9b30-45fe5a3fa24e/resource/40094bd6-f82d-4979-949b-26c8dc00b9a7/download/220511_monatszahlenmonatszahlen2204_verkehrsunfaelle.csv'



data_set1 = pd.read_csv(url)
data_set1

"""Take only the first 5 columns and drop the rest.
Remove space from columns names.
"""

data_set2 = data_set1.drop(['VORJAHRESWERT', 'VERAEND_VORMONAT_PROZENT','VERAEND_VORJAHRESMONAT_PROZENT','ZWOELF_MONATE_MITTELWERT'], axis=1)

data_set2.rename(columns=lambda x:x.replace(' ','_').lower(), inplace=True)

"""Drop the rows of years(2021,2022).

"""

ds = data_set2.drop(data_set2[data_set2.jahr.isin([2021,2022])].index).reset_index(drop=True)

ds = ds.drop(ds[ds.monat.isin(['Summe'])].index).reset_index(drop=True)


ds.head()

"""Remove the year and keeponly month in month column."""

ds['monat'] = ds['monat'].str[4:]
ds = ds.astype({'monat':'int'})

"""Make sure no missing values"""

ds.info()
ds.isna().sum()

"""Show statistical summary of all the quantitative variables"""

ds.describe()

"""Calculate the number of accidents per category."""

df_grouped = ds.groupby(by="auspraegung")["wert"].sum().plot(kind='bar',legend=True)

df_grouped

"""Calculate the number of categorize. """

obj = (ds.dtypes == 'object')
object_cols = list(obj[obj].index)
print("Categorical variables:",len(object_cols))

"""Analyze the different categorical features."""

unique_values = []
for col in object_cols:
  unique_values.append(ds[col].unique().size)
plt.figure(figsize=(10,6))
plt.title('No. Unique values of Categorical Features')
plt.xticks(rotation=90)
sns.barplot(x=object_cols,y=unique_values)

"""OneHotEncoder :
firstly collect all the features which have the object datatype.

"""

s = (ds.dtypes == 'object')
object_cols = list(s[s].index)
print("Categorical variables:")
print(object_cols)
print('No. of. categorical features: ',
      len(object_cols))

""" once we have a list of all the features. We can apply OneHotEncoding to the whole list."""

OH_encoder = OneHotEncoder(sparse=False)
OH_cols = pd.DataFrame(OH_encoder.fit_transform(ds[object_cols]))
OH_cols.index = ds.index
OH_cols.columns = OH_encoder.get_feature_names()
df = ds.drop(object_cols, axis=1)
df = pd.concat([df, OH_cols], axis=1)
df

"""Splitting Dataset into Training and Testing."""

X = df.drop(['wert'], axis=1)
Y = df['wert']

# Split the training set into
# training and validation set
X_train, X_test, Y_train, Y_test = train_test_split(
	X, Y, train_size=0.8, test_size=0.2, random_state=0)
X_test
Y_test

"""I wil train the model to determine the continuous values, I will be using these regression model of Random Forest Regressor.

Random Forest is an ensemble technique that uses multiple of decision trees .
"""

model_RFR = RandomForestRegressor(n_estimators=10)
model_RFR.fit(X_train, Y_train)
Y_pred = model_RFR.predict(X_test)
 
mean_absolute_percentage_error(Y_test, Y_pred)

"""Forecasts the values for:

Category: 'Alkoholunf??lle'

Type: 'insgesamt

Year: '2021'

Month: '01'
"""

test_set = pd.read_csv(url)
test_set = test_set.drop(['VORJAHRESWERT', 'VERAEND_VORMONAT_PROZENT','VERAEND_VORJAHRESMONAT_PROZENT','ZWOELF_MONATE_MITTELWERT'], axis=1)

test_set.rename(columns=lambda x:x.replace(' ','_').lower(), inplace=True)
test_set = test_set.drop(test_set[test_set.monat.isin(['Summe'])].index).reset_index(drop=True)
test_set['monat'] = test_set['monat'].str[4:]
test_set = test_set.astype({'monat':'int'})
test_set

s = (test_set.dtypes == 'object')
object_cols = list(s[s].index)
print("Categorical variables:")
print(object_cols)
print('No. of. categorical features: ',
      len(object_cols))

OH_encoder = OneHotEncoder(sparse=False)
OH_cols = pd.DataFrame(OH_encoder.fit_transform(test_set[object_cols]))
OH_cols.index = test_set.index
OH_cols.columns = OH_encoder.get_feature_names()
test_set = test_set.drop(object_cols, axis=1)
test_set = pd.concat([test_set, OH_cols], axis=1)
test_set

"""Extract the year of 2021 which we want to predict."""

X_test1=test_set.iloc[12:24].drop(['wert'], axis=1)
 
Y_test1 = test_set['wert'].iloc[12:24]
X_test1

Y_test1

"""Make the prediction for year of 2021."""

Y_pred = model_RFR.predict(X_test1)
 
mean_absolute_percentage_error(Y_test1, Y_pred)
Y_pred

"""The predicted (wert) is 28"""
