# -*- coding: utf-8 -*-
"""
@author: elamr
"""
import os
import pandas as pd
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()
path = api.dataset_download_files("jboysen/mri-and-alzheimers", path='./ModelTraining/BIOFM/data/', unzip=True)
print("Done downloading dataset")

df = pd.read_csv("datasets\oasis_crosssectional.csv", header=None)

df = df.drop(columns=['ID', 'Delay', 'Dominant_Hand'])
df = df.replace({'Sex' : {'F':1, 'M':0}})
df = df.convert_dtypes()

df.to_csv('./ModelTraining/BIOFM/data/clean_oasis.csv', index=False,  header=False)
