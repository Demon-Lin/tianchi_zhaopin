# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 23:57:27 2019

@author: hugh2
"""

import pandas as pd

test_raw_data=pd.read_table('dataset/user_ToBePredicted')

def split_first_city(x):
    a=x.split(',',1)[0]
    return a

def split_second_city(x):
    a=x.split(',',2)[1]
    return a

def split_third_city(x):
    a=x.split(',',3)[2]
    return a

def count_diff_desire_city(x):
    a=x.split(',',3)[0]
    b=x.split(',',3)[1]
    c=x.split(',',3)[2]
    i=1
    if (a!=b)&(b!='-'):
        i+=1
    elif(a!=c)&(c!='-'):
        i+1
    elif(b!=c)&(c!='-'):
        i+1
    
    return i

def add_the_symbol(x):
    a=x.count(',')
    if a==0:
        return x+',,'
    elif a==1:
        return x+','
    else:
        return x

def split_first_job_id(x):
    a=x.split(',',1)[0]
    return a

def split_second_job_id(x):
    a=x.split(',',2)[1]
    if a =='':
        return '无'
    else:
        return a

def split_third_job_id(x):
    a=x.split(',',3)[2]
    if a =='':
        return '无'
    else:
        return a

def salary_trans_rank(x):
    len_a=len(str(x))
    behind_a=len_a+x*(0.1**(len_a))
    return behind_a


process_data1=pd.DataFrame()

process_data1['user_id']=test_raw_data['user_id']


process_data1['desire_jd_city_id1']=test_raw_data['desire_jd_city_id'].map(split_first_city)
process_data1['desire_jd_city_id2']=test_raw_data['desire_jd_city_id'].map(split_second_city)
process_data1['desire_jd_city_id3']=test_raw_data['desire_jd_city_id'].map(split_third_city)
#这里同样出现了逗号，所以需要切分出来，借用下split_job_id的方法，函数内容是一样的，所以就不再写多一个了，名字也不改了>_<
process_data1['desire_jd_type_id']=test_raw_data['desire_jd_type_id'].map(add_the_symbol)
process_data1['desire_jd_type_id1']=process_data1['desire_jd_type_id'].map(split_first_job_id)
process_data1['desire_jd_type_id2']=process_data1['desire_jd_type_id'].map(split_second_job_id)
process_data1['desire_jd_type_id3']=process_data1['desire_jd_type_id'].map(split_third_job_id)
#接下来有块比较复杂的操作，就是需要把这三列合并成一列

#temp_data1=process_data1[['user_id','desire_jd_type_id1']]
#temp_data1.rename(columns={'desire_jd_type_id1':'user_key'},inplace=True)
#temp_data2=process_data1[['user_id','desire_jd_type_id2']]
#temp_data2.rename(columns={'desire_jd_type_id2':'user_key'},inplace=True)
#temp_data3=process_data1[['user_id','desire_jd_type_id3']]
#temp_data3.rename(columns={'desire_jd_type_id3':'user_key'},inplace=True)
#temp_data=pd.concat([temp_data1,temp_data2,temp_data3],axis=0)
#process_data1.drop(['desire_jd_type_id','desire_jd_type_id1','desire_jd_type_id2','desire_jd_type_id3'],axis=1,inplace=True)

test_raw_data['cur_salary_id'].replace('-',0,inplace=True)
process_data1['cur_salary_min']=test_raw_data['cur_salary_id'].map(lambda x:str(x)[:len(str(x))//2])
process_data1['cur_salary_max']=test_raw_data['cur_salary_id'].map(lambda x:str(x)[len(str(x))//2:])

process_data1['desire_salary_min']=test_raw_data['desire_jd_salary_id'].map(lambda x:str(x)[:len(str(x))//2])
process_data1['desire_salary_max']=test_raw_data['desire_jd_salary_id'].map(lambda x:str(x)[len(str(x))//2:])

process_data1['desire_jd_industry_id']=test_raw_data['desire_jd_industry_id'].map(add_the_symbol)
process_data1['desire_jd_industry_id1']=process_data1['desire_jd_industry_id'].map(split_first_job_id)
process_data1['desire_jd_industry_id2']=process_data1['desire_jd_industry_id'].map(split_second_job_id)
process_data1['desire_jd_industry_id3']=process_data1['desire_jd_industry_id'].map(split_third_job_id)

process_data1['desire_jd_city_id1'].replace('-',0,inplace=True)
process_data1['desire_jd_city_id2'].replace('-',0,inplace=True)
process_data1['desire_jd_city_id3'].replace('-',0,inplace=True)

process_data1['desire_salary_min_rank']=process_data1['desire_salary_min']
process_data1['desire_salary_min_rank'].replace('10','0',inplace=True)
process_data1['desire_salary_min_rank']=pd.to_numeric(process_data1['desire_salary_min_rank'])
process_data1['desire_salary_min_rank'].fillna(0,inplace=True)
process_data1['desire_salary_min_rank']=process_data1['desire_salary_min_rank'].astype('int')

process_data1['desire_salary_max_rank']=process_data1['desire_salary_max']
process_data1['desire_salary_max_rank'].replace('00','1000',inplace=True)
process_data1['desire_salary_max_rank']=pd.to_numeric(process_data1['desire_salary_max_rank'])
process_data1['desire_salary_max_rank'].fillna(0,inplace=True)
process_data1['desire_salary_max_rank']=process_data1['desire_salary_max_rank'].astype('int')

process_data1['desire_salary_min_rank']=process_data1['desire_salary_min_rank'].map(salary_trans_rank)
process_data1['desire_salary_max_rank']=process_data1['desire_salary_max_rank'].map(salary_trans_rank)

process_data1['cur_salary_min_rank']=process_data1['cur_salary_min']
process_data1['cur_salary_min_rank'].replace('10','0',inplace=True)
process_data1['cur_salary_min_rank']=pd.to_numeric(process_data1['cur_salary_min_rank'])
process_data1['cur_salary_min_rank'].fillna(0,inplace=True)
process_data1['cur_salary_min_rank']=process_data1['cur_salary_min_rank'].astype('int')

process_data1['cur_salary_max_rank']=process_data1['cur_salary_max']
process_data1['cur_salary_max_rank'].replace('00','1000',inplace=True)
process_data1['cur_salary_max_rank']=pd.to_numeric(process_data1['cur_salary_max_rank'])
process_data1['cur_salary_max_rank'].fillna(0,inplace=True)
process_data1['cur_salary_max_rank']=process_data1['cur_salary_max_rank'].astype('int')

process_data1['cur_salary_min_rank']=process_data1['cur_salary_min_rank'].map(salary_trans_rank)
process_data1['cur_salary_max_rank']=process_data1['cur_salary_max_rank'].map(salary_trans_rank)

degree_dict={'其他':1,'初中':2,'高中':3,'中专':3,'中技':3,'大专':4,'本科':5,'硕士':6,'MBA':6,'EMBA':7,'博士':8}
process_data1['cur_edu_degree']=test_raw_data['cur_degree_id']
process_data1['cur_edu_degree'].fillna('其他',inplace=True)

process_data1['cur_edu_degree']=process_data1['cur_edu_degree'].map(lambda x:degree_dict[x])
process_data1['experience']=test_raw_data['experience']
#process_data1=pd.merge(process_data1,temp_data,how='left',on='user_id')

#process_data2=process_data1.drop(process_data1[process_data1['user_key']=='无'].index.tolist(),axis=0)

#test_raw_data['start_work_date']=test_raw_data['start_work_date'].astype('int')

tmp_df=pd.DataFrame()
tmp_df['user_id']=test_raw_data['user_id']
tmp_df['work_years']=test_raw_data['start_work_date'].map(lambda x:2019-int(x) if x!='-' else 0)
process_data1=pd.merge(process_data1,tmp_df,on='user_id',how='left')
process_data1.fillna(0,inplace=True)

process_data1.to_csv('test_data_processed_2.csv',index=False)






















