{{ config(materialized='view') }}

WITH agent_performance_data AS (
    SELECT 
        sales_agent,
        SUM(business_close_value) AS total_sales_value,
        AVG(business_sales_cycle_duration) AS average_sales_cycle_duration,
        AVG(agent_won_deal_effectiveness) AS average_won_deal_effectiveness
    FROM 
        {{ ref("stg-won_deal_stage") }}
    GROUP BY 
        sales_agent
    ORDER BY
        average_won_deal_effectiveness DESC
)

SELECT 
    *
FROM 
    agent_performance_data
