{{ config(materialized='view') }}

SELECT 
    *
FROM
    {{ source('CRM', 'model_predictions_summary_source')}}
