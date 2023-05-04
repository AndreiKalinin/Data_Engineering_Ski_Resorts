{{ config(materialized='table') }}

WITH cte_snow AS (
    SELECT month,
           snow,
           latitude,
           longitude
    FROM {{ source('ski_resorts_data', 'snow_cover') }} ),

 cte_resorts AS (
    SELECT id,
           resort,
           country,
           continent,
           latitude_snow,
           longitude_snow
    FROM {{ source('ski_resorts_data', 'resorts_data') }} )
SELECT id,
       resort,
       country,
       continent,
       month,
       snow
FROM cte_snow INNER JOIN cte_resorts
ON cte_snow.latitude = cte_resorts.latitude_snow AND cte_snow.longitude = cte_resorts.longitude_snow
