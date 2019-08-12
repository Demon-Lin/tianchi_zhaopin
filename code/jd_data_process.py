# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 23:47:15 2019

@author: hugh2
"""

import pandas as pd
from numpy import nan 
import math

def salary_trans_rank(x):
    len_a=len(str(x))
    behind_a=len_a+x*(0.1**(len_a))
    return behind_a

jd_row_data=pd.read_csv('dataset/jd_processed.csv')
jd_row_data.drop(['Unnamed: 18','Unnamed: 19'],inplace=True,axis=1)

jd_train_data=pd.DataFrame()

jd_train_data['jd_no']=jd_row_data['jd_no']
jd_train_data['jd_key']=jd_row_data['jd_sub_type']

jd_train_data['city']=jd_row_data['city']

jd_train_data['salary_min']=jd_row_data['min_salary']
jd_train_data['salary_min'].fillna(0,inplace=True)
jd_train_data['salary_min']=jd_train_data['salary_min'].astype('int')

jd_train_data['salary_max']=jd_row_data['max_salary']
jd_train_data['salary_max'].fillna(0,inplace=True)
jd_train_data['salary_max']=jd_train_data['salary_max'].astype('int')

jd_train_data['salary_min']=jd_train_data['salary_min'].map(salary_trans_rank)
jd_train_data['salary_max']=jd_train_data['salary_max'].map(salary_trans_rank)

jd_train_data['need_edu_degree']=jd_row_data['min_edu_level']
jd_train_data['need_edu_degree'].fillna('其他',inplace=True)
jd_train_data['need_edu_degree'].replace('\\N','其他',inplace=True)
jd_train_data['need_edu_degree'].replace('请选择','其他',inplace=True)
jd_train_data['need_edu_degree'].replace('大专 ','大专',inplace=True)
jd_train_data['need_edu_degree'].replace('中技 ','中技',inplace=True)
jd_train_data['need_edu_degree'].replace('硕士 ','硕士',inplace=True)
jd_train_data['need_edu_degree'].replace('高中 ','高中',inplace=True)
jd_train_data['need_edu_degree'].replace('初中 ','初中',inplace=True)
jd_train_data['need_edu_degree'].replace('博士 ','博士',inplace=True)
degree_list=jd_train_data['need_edu_degree'].drop_duplicates().tolist()

degree_dict={'其他':1,'初中':2,'高中':3,'中专':3,'中技':3,'大专':4,'本科':5,'硕士':6,'MBA':6,'EMBA':7,'博士':8}

jd_train_data['need_edu_degree']=jd_train_data['need_edu_degree'].map(lambda x:degree_dict[x])

jd_train_data['min_years']=jd_row_data['min_years'].map(lambda x:x if x!=-1 else 0)
jd_train_data['max_years']=jd_train_data['min_years'].map(lambda x:str(x)[len(str(x))//2-1:])
jd_train_data['min_years']=jd_train_data['min_years'].map(lambda x:str(x)[:len(str(x))//2-1])
jd_train_data.replace('',0,inplace=True)
jd_train_data['min_years']=jd_train_data['min_years'].astype(float)
jd_train_data['max_years']=jd_train_data['max_years'].astype(float)
jd_train_data['job_description']=jd_row_data['job_description']
jd_train_data['required_num']=jd_row_data['require_nums']
jd_train_data['is_travel']=jd_row_data['is_travel']




jd_train_data.to_csv('jd_data_processed_1.csv',index=False)

#jd_row_data.to_csv('analyze_by_mysql_jd.csv',index=False)
