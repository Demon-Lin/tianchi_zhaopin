# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 00:29:22 2019

@author: hugh2
"""

import pandas as pd
from collections import Counter

action=pd.read_table('dataset/table3_action')

jd_data,user_data=pd.read_csv('jd_data_processed_1.csv'),pd.read_csv('user_data_processed_2.csv')

combine_upload_data=pd.merge(action,user_data,on='user_id',how='left')
combine_upload_data=pd.merge(combine_upload_data,jd_data,on='jd_no',how='left')

combine_upload_data['pairing_city_cd']=combine_upload_data['desire_jd_city_id1']==combine_upload_data['city']

combine_upload_data['pairing_city_cd_tmp']=combine_upload_data['desire_jd_city_id2']==combine_upload_data['city']
combine_upload_data['pairing_city_cd']=combine_upload_data['pairing_city_cd']|combine_upload_data['pairing_city_cd_tmp']
combine_upload_data['pairing_city_cd_tmp']=combine_upload_data['desire_jd_city_id3']==combine_upload_data['city']
combine_upload_data['pairing_city_cd']=combine_upload_data['pairing_city_cd']|combine_upload_data['pairing_city_cd_tmp']
combine_upload_data.drop('pairing_city_cd_tmp',axis=1,inplace=True)
combine_upload_data['pairing_city_cd']=combine_upload_data['pairing_city_cd'].map(lambda x:1 if x else 0)

combine_upload_data['desire_diff']=combine_upload_data['salary_max']+combine_upload_data['salary_min']-combine_upload_data['desire_salary_max_rank']-combine_upload_data['desire_salary_min_rank']

combine_upload_data['cur_diff']=combine_upload_data['salary_max']+combine_upload_data['salary_min']-combine_upload_data['cur_salary_min_rank']-combine_upload_data['cur_salary_max_rank']

combine_upload_data['edu_diff']=combine_upload_data['need_edu_degree']-combine_upload_data['cur_edu_degree']

combine_upload_data['years_fit']=(combine_upload_data['work_years']>combine_upload_data['min_years'])&(combine_upload_data['work_years']<combine_upload_data['max_years'])
combine_upload_data['years_fit']=combine_upload_data['years_fit'].map(lambda x:1 if x else 0)



combine_upload_data=combine_upload_data.fillna(value={'cur_salary_min':0,'desire_salary_min':0})




combine_upload_data.dropna(inplace=True)
combine_upload_data.reset_index(inplace=True,drop=True)


cnt=[]
for len_i in range(len(combine_upload_data)):
    i=combine_upload_data['experience'][len_i]
    j=combine_upload_data['job_description'][len_i]
    cnt_tmp=0
    tmp=i.split('|')
    for k in tmp:
        if str(k) in j:
            cnt_tmp+=1
    cnt.append(cnt_tmp)

combine_upload_data['experience_cnt']=cnt




the_data_need_predict=combine_upload_data[['desire_salary_min_rank','desire_salary_max_rank','cur_salary_min_rank',
                        'cur_salary_max_rank','cur_edu_degree','work_years','required_num','is_travel',
                        'salary_min','salary_max','need_edu_degree','min_years','max_years','pairing_city_cd','desire_diff','cur_diff','edu_diff','years_fit','experience_cnt','browsed','delivered','satisfied']]


the_data_need_predict.to_csv('the_data_need_train.csv',index=False)
#combine_upload_data.to_csv('analyze_by_mysql_train.csv',index=False)
