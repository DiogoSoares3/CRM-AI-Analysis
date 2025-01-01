{{ config(materialized='view') }}

SELECT 
    *
FROM
    {{ source('CRM-db', 'model_predictions_summary_source')}}
