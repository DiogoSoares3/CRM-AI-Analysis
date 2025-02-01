
{{ config(materialized='view') }}

SELECT 
    *
FROM
    {{ source('CRM', 'customers_rfm_features_source')}}
