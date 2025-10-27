# -*- coding: utf-8 -*-
"""
@author: elamr
"""
import os
import pandas as pd
# kaggle
#from kaggle.api.kaggle_api_extended import KaggleApi
#api = KaggleApi()
#api.authenticate()
#path = api.dataset_download_files("jboysen/mri-and-alzheimers", path='./ModelTraining/BIOFM/data/', unzip=True)
print("Done downloading dataset")

df = pd.read_csv("./ModelTraining/BIOFM/data/oasis_longitudinal.csv", header=0)
#print head of df
print(df.head())

df.drop('Subject ID')
df.drop ('MR Delay')
df.drop ('Hand')
df.drop ('MRI ID')
df.drop ('Group')
df.drop ('Visit')
df.replace({'M/F' : {'F':1, 'M':0}})
df.dropna()
df.convert_dtypes()

def change_cdr(cdr):
    if cdr == 0.5:
        return 1
    elif cdr == 1:
        return 2
    elif cdr == 2:
        return 3
    else:
        return 0

df['CDR'] = df['CDR'].map(change_cdr)

df.to_csv('./ModelTraining/BIOFM/data/clean_oasis.csv', index=False,  header=False)
