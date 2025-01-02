{{ config(materialized='view') }}

WITH retention_data AS (
    SELECT 
        customer,
        customer_recency_frequency_monetary_segment,
        prob_alive_customer,
        customer_engagement_score
    FROM 
        {{ ref("stg-won_deal_stage") }}
    WHERE 
        prob_alive_customer > 0.7
)

SELECT 
    *
FROM 
    retention_data
