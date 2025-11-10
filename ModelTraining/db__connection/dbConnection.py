# Dependencies:
# pip install python-dotenv
# pip install psycopg2

import os
import psycopg2
import pandas as pd
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))

HOST = os.getenv("HOST")
PORT = os.getenv("PORT",5432)
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

    
conn = psycopg2.connect(f"host={HOST} port={PORT} dbname={DBNAME} user={USER} password={PASSWORD} gssencmode=disable") 

def testConnection(conn):
    try:
        cur = conn.cursor()
        # cur.execute("""select
        # t.table_name AS table_name,
        # column_name,
        # data_type
        # from information_schema.tables t
        # INNER JOIN information_schema.columns c on c.table_schema = c.table_schema AND t.table_name = c.table_name
        # WHERE c.table_schema= 'mnemos'""")
        # df_db = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
        print("SUCCESSFUL CONNECTION TO MNEMOS:")

    except Exception as e:
        print(e)

    finally:
        cur.close()

def getTableData(conn, table_name):
    try:
        cur = conn.cursor()
        cur.execute(f"""select * from {table_name}""")
        df = pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
        return df
    except Exception as e:
        print(e)

    finally:
        cur.close()
