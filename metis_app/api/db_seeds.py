import pandas as pd
from os import path
import sqlite3

DB_NAME = 'metis_app/api/static/api/data/visuals.db'

def csv_to_sqlite3(filename, tablename):
    filename = path.join(path.expanduser('~'), 'Downloads', filename)
    df = pd.read_csv(filename)
    
    conn = sqlite3.connect(DB_NAME)
    df.to_sql(tablename, conn)
    conn.close()
    
    return {'db': DB_NAME, 'tablename': tablename}

def seed_databases():

    if not path.isfile(DB_NAME):
        csv_to_sqlite3(
            filename='index_component_stocks_022420.csv',
            tablename='index_component_stocks',
        )
        csv_to_sqlite3(
            filename='treasury_yield_curve_110221-022421.csv',
            tablename='treasury_yield_curve',
        )

if __name__ == '__main__':
    seed_databases()