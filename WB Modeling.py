import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from xgboost import plot_importance

class modeling(data_cleanup):

    def fix_dtypes(self):
        self.Train.country=self.Train.country.astype('category')
        self.Train.date=self.Train.date.astype('int16')
        return self.Train

    def create_val_set(self):
        self.Val=self.Train[self.Train['date']==2012]
        self.Train.drop(index=self.Val.index,inplace=True)
        self.Train.reset_index(inplace=True)
        self.Val.reset_index(inplace=True)
        self.Train.drop(labels='index',axis=1,inplace=True)
        self.Val.drop(labels='index',axis=1,inplace=True)
        return self.Val, self.Train

    def create_mod_Dfs(self):
        self.Xtrain= self.Train.loc[:,self.Train.columns!='Temp(C)']
        self.ytrain= self.Train.loc[:,'Temp(C)']
        self.Xval= self.Val.loc[:,self.Train.columns!='Temp(C)']
        self.yval= self.Val.loc[:,'Temp(C)']
        Xtrain.drop(labels='date',axis=1,inplace=True)
        Xval.drop(labels='date',axis=1,inplace=True)
        return self.Xtrain, self.ytrain, self.Xval, self.yval

    def model_xgboost(self):
        xgb=XGBRegressor(objective='reg:squarederror',n_jobs=-1,n_estimators=5000,subsample=0.75,colsample_bytree=0.75, colsample_bylevel=0.75,learning_rate=0.06)
        xgb.fit(self.Xtrain,self.ytrain, eval_set=[(self.Xtrain,self.ytrain),(self.Xval,self.yval)],eval_metric='rmse', early_stopping_rounds=70)
