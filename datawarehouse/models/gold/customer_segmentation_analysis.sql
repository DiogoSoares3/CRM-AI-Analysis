{{ config(materialized='view') }}

WITH customer_segmentation AS (
    SELECT 
        customer,
        customer_revenue,
        customer_office_location,
        customer_recency_frequency_monetary_segment,
        customer_average_transaction_value,
        customer_engagement_score,
        actual_customer_lifetime_value,
        customer_expected_purchases_week,
        customer_expected_purchases_half_year,
        customer_expected_purchases_year,
        customer_expected_average_profit,
        prob_alive_customer,
        predicted_year_customer_lifetime_value,
        predicted_customer_lifetime_value_segment
    FROM 
        {{ ref("stg-won_deal_stage") }}
    WHERE 
        customer_recency_frequency_monetary_segment NOT IN ('Other')
    ORDER BY 
        predicted_year_customer_lifetime_value DESC
)

SELECT
    *
FROM
    customer_segmentation
