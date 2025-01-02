{{ config(materialized='view') }}

WITH product_sales_data AS (
    SELECT 
        product,
        product_series,
        SUM(business_close_value) AS total_sales_value,
        COUNT(opportunity_id) AS total_opportunities
    FROM 
        {{ ref("stg-won_deal_stage") }}
    GROUP BY 
        product, product_series
),

top_selling_products AS (
    SELECT 
        product,
        product_series,
        total_sales_value,
        total_opportunities,
        RANK() OVER (
            ORDER BY total_sales_value DESC
        ) AS sales_rank
    FROM 
        product_sales_data
)

SELECT 
    *
FROM 
    top_selling_products
