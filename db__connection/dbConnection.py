# Dependencies:
# pip install python-dotenv
# pip install psycopg2

import os
import psycopg2
from dotenv import find_dotenv, load_dotenv

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
    cur.execute("SELECT * FROM pg_database") 
    print(cur.fetchall()) #dont worry about the db info it outputs, so long as it connects and prints, youre good!

except Exception as e:
    print(e)

finally:
    cur.close()