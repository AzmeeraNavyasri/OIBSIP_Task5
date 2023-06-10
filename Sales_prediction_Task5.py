# -*- coding: utf-8 -*-
"""sales prediction using python

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cu55f20DETAdrM8JnP6-rtle0ytRVkND

# sales  prediction using python
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("/content/archive.zip")

df.head()

df.shape

df.columns.values.tolist()

df.info()

df.describe()

df.isnull().sum()

import matplotlib.pyplot as plt
import seaborn as sns

fig, axs = plt.subplots(3, figsize = (5,5))
plt1 = sns.boxplot(df['TV'], ax = axs[0])
plt2 = sns.boxplot(df['Newspaper'], ax = axs[1])
plt3 = sns.boxplot(df['Radio'], ax = axs[2])
plt.tight_layout()

sns.distplot(df['Newspaper'])

iqr = df.Newspaper.quantile(0.75) - df.Newspaper.quantile(0.25)

lower_bridge = df['Newspaper'].quantile(0.25) - (iqr*1.5)
upper_bridge = df['Newspaper'].quantile(0.75) + (iqr*1.5)
print(lower_bridge)
print(upper_bridge)

data = df.copy()

data.loc[data['Newspaper']>=93,'Newspaper']=93

sns.boxplot(data['Newspaper']);

sns.boxplot(data['Sales']);

sns.pairplot(data,x_vars=['TV','Newspaper','Radio'],y_vars='Sales',height=4, aspect=1, kind='scatter')
plt.show()

sns.heatmap(data.corr(),cmap='YlGnBu', annot = True)
plt.show()

important_features = list(df.corr()['Sales'][(df.corr()['Sales']>+0.5)|(df.corr()['Sales']<-0.5)].index)

print(important_features)

x = data['TV']
y = data['Sales']

x = x.values.reshape(-1,1)

x

y

print(x.shape,y.shape)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y, test_size=0.33)

print(x_train.shape,y_train.shape)

from sklearn.metrics import mean_squared_error , r2_score
from sklearn.model_selection import cross_val_score,GridSearchCV
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

knn = KNeighborsRegressor().fit(x_train, y_train)
knn

knn_train_pred = knn.predict(x_train)

knn_test_pred = knn.predict(x_test)

print(knn_train_pred, knn_test_pred)

Results = pd.DataFrame(columns=['Model','Train R2','Test R2','Test RMSE','Variance'])

r2 = r2_score(y_test,knn_test_pred)
r2_train = r2_score(y_train,knn_train_pred)
rmse = np.sqrt(mean_squared_error(y_test,knn_test_pred))
variance = r2_train - r2
Results = Results.append({'Model':'K-Nearest Neighbors','Train R2':r2_train,'Test R2':r2,'Test RMSE':rmse,'Variance':variance},ignore_index=True)
print('R2:',r2)
print('RMSE:',rmse)

Results.head()

svr = SVR().fit(x_train,y_train)
svr

svr_train_pred = svr.predict(x_train)
svr_test_pred = svr.predict(x_test)

print(svr_train_pred,svr_test_pred)

r2 = r2_score(y_test,svr_test_pred)
r2_train = r2_score(y_train,svr_train_pred)
rmse = np.sqrt(mean_squared_error(y_test,svr_test_pred))
variance = r2_train - r2
Results = Results.append({'Model':'Support Vector Machine','Train R2':r2_train,'Test R2':r2,'Test RMSE':rmse,'Variance':variance},ignore_index=True)
print('R2:',r2)
print('RMSE',rmse)

Results.head()

import statsmodels.api as sm

x_train_constant = sm.add_constant(x_train)

model = sm.OLS(y_train, x_train_constant).fit()

model.params

print(model.summary())

plt.scatter(x_train, y_train)
plt.plot(x_train, 6.9955 + 0.0541 * x_train, 'y')

y_train_pred = model.predict(x_train_constant)
res = (y_train - y_train_pred)
res

y_train_pred

fig = plt.figure()
sns.distplot(res, bins = 15)
fig.suptitle('Error Terms',fontsize = 15)
plt.xlabel('Difference in y_train and y_train_pred',fontsize = 15)
plt.show()

plt.scatter(x_train, res)
plt.show()

x_test_constant = sm.add_constant(x_test)
y_pred = model.predict(x_test_constant)

y_pred

from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

np.sqrt(mean_squared_error(y_test, y_pred))

r2 = r2_score(y_test, y_pred)
r2

plt.scatter(x_test, y_test)
plt.plot(x_test, 6.9955 + 0.0541 * x_test,'y')
plt.show()