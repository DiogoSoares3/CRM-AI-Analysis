
{{ config(materialized='view') }}

SELECT 
    *
FROM
    {{ source('CRM-db', 'general_enriched_dataset_source')}}
