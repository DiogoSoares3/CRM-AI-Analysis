
{{ config(materialized='view') }}

SELECT 
    *
FROM
    {{ source('CRM-db', 'customers_rfm_features_source')}}
