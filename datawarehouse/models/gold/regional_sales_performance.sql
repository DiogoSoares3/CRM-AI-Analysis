{{ config(materialized='view') }}

WITH regional_sales_data AS (
    SELECT 
        sales_agent_regional_office,
        SUM(business_close_value) AS total_sales_value,
        AVG(agent_won_deal_effectiveness) AS average_won_deal_effectiveness
    FROM 
        {{ ref("stg-won_deal_stage") }}
    GROUP BY 
        sales_agent_regional_office
)

SELECT 
    *
FROM 
    regional_sales_data
