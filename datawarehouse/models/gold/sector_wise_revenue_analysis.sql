{{ config(materialized='view') }}

WITH sector_revenue_data AS (
    SELECT 
        customer_sector,
        SUM(business_close_value) AS total_revenue,
        AVG(business_sales_cycle_duration) AS average_sales_cycle_duration
    FROM 
        {{ ref("stg-won_deal_stage") }}
    GROUP BY 
        customer_sector
    ORDER BY
        total_revenue DESC
)

SELECT 
    *
FROM 
    sector_revenue_data
