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

    csv_path = 'filename.csv.gz'
    os.system(f"wget {url} -O {csv_path}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df_iter = pd.read_csv(csv_path, iterator=True, chunksize=100000, compression='gzip')
    df = next(df_iter)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        start_time = time()
        df = next(df_iter)
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
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
