import pandas as pd 
from sqlalchemy import create_engine
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    url = params.url
    table_name = params.table_name

    parquet_path = 'filename.parquet'
    csv_path = 'filename.csv'
    os.system(f"wget {url} -O {parquet_path}")
    
    df_parquet = pd.read_parquet(parquet_path)
    df_parquet.to_csv(csv_path)
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df_iter = pd.read_csv(csv_path, iterator=True, chunksize=100000, index_col=0)
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        start_time = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists='append')
        end_time = time()
        print(f"Inserted another chunk, took {end_time - start_time:3f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest data to postgres')
    parser.add_argument('--user') 
    parser.add_argument('--password') 
    parser.add_argument('--host') 
    parser.add_argument('--port') 
    parser.add_argument('--db') 
    parser.add_argument('--table-name') 
    parser.add_argument('--url') 

    args = parser.parse_args()
    main(args)
