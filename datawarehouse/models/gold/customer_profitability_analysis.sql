{{ config(materialized='view') }}

WITH customer_profitability_data AS (
    SELECT 
        customer,
        customer_revenue,
        customer_recency_frequency_monetary_segment,
        customer_average_transaction_value,
        actual_customer_lifetime_value,
        customer_expected_average_profit
    FROM 
        {{ ref("stg-won_deal_stage") }}
),

customer_profitability_ranking AS (
    SELECT 
        customer,
        customer_revenue,
        customer_recency_frequency_monetary_segment,
        customer_average_transaction_value,
        actual_customer_lifetime_value,
        customer_expected_average_profit,
        RANK() OVER (
            PARTITION BY customer_recency_frequency_monetary_segment 
            ORDER BY customer_expected_average_profit DESC
        ) AS profitability_rank
    FROM 
        customer_profitability_data
)

SELECT DISTINCT
    *
FROM 
    customer_profitability_ranking
ORDER BY
    profitability_rank
