# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 23:12:54 2019

@author: hugh2
"""

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix as cm

train_data=pd.read_csv('the_data_need_train.csv')
the_data_need_predict=pd.read_csv('the_data_need_predict.csv')

train_data.drop(['browsed','delivered'],axis=1,inplace=True)

plus_samples=train_data[train_data['satisfied']==1]
len_plus=len(plus_samples)
minus_samples=train_data[train_data['satisfied']==0].sample(n=round(len_plus*1.15),random_state=960705)
concat_data=pd.concat([plus_samples,minus_samples],axis=0)


the_label=concat_data.pop('satisfied')

X_train,X_test,y_train,y_test=train_test_split(concat_data,the_label,test_size=0.2,random_state=960705)
the_xgb_model=xgb.XGBClassifier(n_jobs=-1,n_estimators=135,max_depth=5,learning_rate=0.2,gamma=0.2)
#the_xgb_model=xgb.XGBClassifier(n_jobs=-1)
#
#gsCv = GridSearchCV(the_xgb_model,{'learning_rate': [i*0.1 for i in range(1,11,1)]})
#gsCv.fit(X_train,y_train)
#print(gsCv.grid_scores_,gsCv.best_params_,gsCv.best_score_)



the_xgb_model.fit(X_train,y_train)
y_predict=the_xgb_model.predict(X_test)

print(cm(y_test,y_predict))


predict=the_xgb_model.predict_proba(the_data_need_predict.iloc[:,2:])[:,1]

the_data_need_predict['predict_prob']=predict
the_data_need_predict.sort_values(by='predict_prob',axis=0,inplace=True,ascending=False)
the_data_need_predict.to_csv('result9.csv',index=False)

