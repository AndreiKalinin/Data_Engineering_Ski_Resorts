# Data Engineering Ski Resorts
### Description
This is the final project of Data Engineering Zoomcamp. <br>
The project works locally using Postgres DB. <br>
The dataset was taken from https://maven-datasets.s3.amazonaws.com/Ski+Resorts/Ski+Resorts.zip. It contains data about 500 world ski resorts and percent of snow cover in every month in 2022. 
The workflow is provided with Prefect, data transformation is performed using DBT, the dashboard is built using Plotly Dash framework. <br>
The goal of this project is to compare resorts details like the longest run, slopes amount, snow cover, etc in different countries and continents.
![alt text](https://github.com/AndreiKalinin/Data_Engineering_Ski_Resorts/blob/master/images/project_schema.png)

### Instructions
To reproduce the project follow these steps:
1. Run `docker-compose.yaml` with the command `docker-compose up -d`
2. Open localhost:80, create server with connection parameters from docker-compose file (use container name as a host name) and two schemas in `ski_resorts` database: `stg` and `core`.
3. Install necessary python libraries from `requirements.txt`.
4. Execute `prefect orion start` to enter administration panel (localhost:4200) and create secret block ('pgdb-connection') with connection string like `postgresql://username:password@host:port/database` with the parameters from docker-compose file.
5. Run `etl_flow.py` to fetch the data from the web page and insert into the database.
6. Add to your `profiles.yml` connection parameters from docker-compose file.
7. Change directory to dbt_transformation/resorts_dbt and execute `dbt run` command.
8. Run `main.py` to launch the dashboard at localhost:8050.
![alt text](https://github.com/AndreiKalinin/Data_Engineering_Ski_Resorts/blob/master/images/dashboard.png)
