
{{ config(materialized='view') }}

SELECT 
    *
FROM
    {{ source('CRM', 'general_enriched_dataset_source')}}
