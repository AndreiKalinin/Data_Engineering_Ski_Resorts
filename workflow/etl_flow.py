import requests
from zipfile import ZipFile
import io
import pandas as pd
from prefect import flow, task
from sqlalchemy import create_engine
from prefect.blocks.system import Secret
import time
from typing import Tuple


@task(retries=3)
def fetch_data(url: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Fetch data from web"""
    r = requests.get(url)
    zipfile = ZipFile(io.BytesIO(r.content))
    zipfile.extractall('./data')
    df_resorts = pd.read_csv('./data/resorts.csv', encoding='cp1252')
    df_snow = pd.read_csv('./data/snow.csv', encoding='cp1252')
    return df_resorts, df_snow


@task()
def change_data_type(df: pd.DataFrame) -> pd.DataFrame:
    """Fix data types issues"""
    df['Month'] = pd.to_datetime(df['Month'])
    return df


@task()
def fix_resort_names(df: pd.DataFrame) -> pd.DataFrame:
    """Fix resorts' names issues"""
    df['Resort'] = df['Resort'].str.replace('?', '')
    return df


@task()
def change_columns_names(df: pd.DataFrame) -> pd.DataFrame:
    """Fix columns' names to use them with PostgreSQL"""
    cols = [col.lower().replace(' ', '_') for col in df.columns]
    df.columns = cols
    df = df.rename(columns={'location_account_#': 'location_account'})
    return df


@task()
def add_columns(df_resorts: pd.DataFrame, df_snow: pd.DataFrame) -> pd.DataFrame:
    """Add the closest latitude and longitude from snow dataset"""
    latitudes = df_snow['latitude'].unique()
    longitudes = df_snow['longitude'].unique()
    df_resorts['latitude_snow'] = latitudes[df_resorts['latitude'].apply(lambda x: abs(x - latitudes).argmin())]
    df_resorts['longitude_snow'] = longitudes[df_resorts['longitude'].apply(lambda x: abs(x - longitudes).argmin())]
    return df_resorts


@task()
def write_resorts_data_to_postgres(df: pd.DataFrame, engine: create_engine) -> None:
    """Upload dataframe to database"""
    df.to_sql('resorts_data',
              con=engine,
              schema='stg',
              if_exists='replace',
              index=False)
    return


@task()
def write_snow_data_to_postgres(df: pd.DataFrame, engine: create_engine) -> None:
    """Upload dataframe to database"""
    df.to_sql('snow_cover',
              con=engine,
              schema='stg',
              if_exists='replace',
              index=False)
    return


@flow()
def etl_web_to_database() -> None:
    """The main ETL function"""
    start_time = time.time()
    dataset_url = 'https://maven-datasets.s3.amazonaws.com/Ski+Resorts/Ski+Resorts.zip'
    secret_block = Secret.load('pgdb-connection')
    con = secret_block.get()
    engine = create_engine(con)
    df_resorts, df_snow = fetch_data(dataset_url)
    df_snow = change_data_type(df_snow)
    df_resorts = fix_resort_names(df_resorts)
    df_resorts = change_columns_names(df_resorts)
    df_snow = change_columns_names(df_snow)
    df_resorts = add_columns(df_resorts, df_snow)
    write_resorts_data_to_postgres(df_resorts, engine)
    write_snow_data_to_postgres(df_snow, engine)
    print(f'Data has been loaded. Elapsed time: {round(time.time() - start_time, 2)} seconds')


if __name__ == '__main__':
    etl_web_to_database()
