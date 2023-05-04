{{ config(materialized='table') }}

WITH cte_resorts AS (
    SELECT id,
           resort,
           country,
           continent,
           highest_point,
           lowest_point,
           beginner_slopes,
           intermediate_slopes,
           difficult_slopes,
           longest_run
    FROM {{ source('ski_resorts_data', 'resorts_data') }} )
SELECT * FROM cte_resorts
