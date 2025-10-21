# -*- coding: utf-8 -*-
"""
@author: elamr
"""
import os
import psycopg2
import pandas as pd
from dotenv import find_dotenv, load_dotenv
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()
path = api.dataset_download_files("jboysen/mri-and-alzheimers", path='./ModelTraining/BIOFM/data/', unzip=True)
print("Done downloading dataset")


load_dotenv(find_dotenv(usecwd=True))

HOST = os.getenv("HOST")
PORT = os.getenv("PORT",5432)
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
   
conn = psycopg2.connect(f"host={HOST} port={PORT} dbname={DBNAME} user={USER} password={PASSWORD} gssencmode=disable") 

try:
    conn.autocommit = True #
    cur = conn.cursor()
    cur.execute("""select
    t.table_name AS table_name,
    column_name,
    data_type
    from information_schema.tables t
    INNER JOIN information_schema.columns c on c.table_schema = c.table_schema AND t.table_name = c.table_name
    WHERE c.table_schema= 'mnemos'""") 
    df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
    print(df)

except Exception as e:
    print(e)

finally:
    cur.close()

df.dropna(how='any', subset=['CDR'], inplace=True)
df.drop('Delay', axis=1, inplace=True)
df.drop('ID', axis=1, inplace=True)
df.drop('Identification', axis=1, inplace=True)
df.drop('Dominant_Hand', axis=1, inplace=True)
df['SES'] = df['SES'].fillna(2.0)
df = df.replace({'Sex' : {'F':1, 'M':0}})
df = df.convert_dtypes()

df.head()

df.to_csv('./ModelTraining/BIOFM/data/clean_oasis.csv', index=False,  header=False)
