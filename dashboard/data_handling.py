import pandas as pd
from prefect.blocks.system import Secret


con = Secret.load('pgdb-connection').get()
df_resorts = pd.read_sql(sql='SELECT * FROM core.resorts_dash', con=con)
df_snow = pd.read_sql(sql='SELECT * FROM core.snow_dash', con=con)
