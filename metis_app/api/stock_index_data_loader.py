import requests
import json
from os import environ, path
import pandas as pd
import boto3
import sqlite3
from metis_app.api import S3Downloader

class StockIndexDataLoader(object):
    
    uris = ['sp500', 'dowjones']

    def __init__(self, stock_index_name, from_s3):
        self.stock_index_name = stock_index_name
        self.from_s3 = from_s3
        self.data = self.load_data()
    
    def load_data(self):
        if self.stock_index_name not in self.uris:
            msg = f'stock_index_name must be in {self.uris}'
            raise ValueError(msg)
        
        data_loader = self.load_from_s3 if self.from_s3 else self.load_from_db
        df = data_loader()
    
        data = (df
            .reset_index()
            .to_dict(orient='records')
        )
        return data
    
    def load_from_db(self):
        db_dir = 'metis_app/api/static/api/data'
        db_filename = 'visuals.db'
        db_filepath = path.join(db_dir, db_filename)
        s3 = S3Downloader(db_dir)
        s3.download(db_filename, db_filename)

        conn = sqlite3.connect(db_filepath)
        
        sql = ("SELECT * FROM index_component_stocks "
               f"WHERE stock_index_name= '{self.stock_index_name}'")

        df = (pd.read_sql(sql, conn)
            .rename(columns=lambda x: x.replace('_', ' ').title())
            .set_index('Symbol')
        )

        conn.close()

        return df
    
    def load_from_s3(self):
        aws_config = {
            'aws_access_key_id': environ.get('METIS_APP_AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': environ.get('METIS_APP_AWS_SECRET_KEY'),
        }
        client = boto3.client('s3', **aws_config)
    
        response = client.get_object(
            Bucket='metis-projects',
            Key=f"stock_index_data/{self.stock_index_name}.json",
        )
        data = json.load(response.get('Body'))
        df = (pd.DataFrame(data['data'])
            .set_index('Symbol')
        )
    
        return df