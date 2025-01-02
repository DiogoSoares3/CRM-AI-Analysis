{{ config(materialized='view') }}

WITH dataset_won_deal_stage AS (
    SELECT 
        sales_agent,
        opportunity_id,
        business_close_value,
        agent_won_deal_effectiveness,
        business_sales_cycle_duration
    FROM 
        {{ ref("stg-won_deal_stage") }}
),

sales_performance_metrics AS (
    SELECT 
        sales_agent,
        COUNT(DISTINCT opportunity_id) AS total_opportunities,
        SUM(business_close_value) AS total_revenue,
        AVG(agent_won_deal_effectiveness) AS avg_close_rate,
        AVG(business_sales_cycle_duration) AS avg_sales_cycle_duration
    FROM 
        dataset_won_deal_stage
    GROUP BY 
        sales_agent
    ORDER BY 
        total_revenue DESC
)

SELECT
    *
FROM
    sales_performance_metrics
