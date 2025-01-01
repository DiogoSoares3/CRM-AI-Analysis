{{ config(materialized='view') }}

-- import

WITH general_enriched_dataset AS (
    SELECT 
        *
    FROM 
        {{ref ("raw-general_enriched_dataset")}}  
),

customers_rfm_features AS (
    SELECT 
        *
    FROM 
        {{ref ("raw-customers_rfm_features")}}  
),

model_predictions_summary AS (
    SELECT 
        *
    FROM 
        {{ref ("raw-model_predictions_summary")}}  
),

-- Podemos realizar filtros como round, etc. Talvez melhorar seus nomes, etc
-- Ideia: colocar um ratio de won/lost por account

renamed_merged_data AS (
    SELECT 
        g.opportunity_id AS opportunity_id,
        g.sales_agent AS sales_agent,
        g.product AS product,
        g.account AS customer,
        g.deal_stage AS business_deal_stage,
        g.engage_date AS business_engage_date,
        g.close_date AS business_close_date,
        g.close_value AS business_close_value,
        g.sector AS costumer_sector,
        g.year_established AS customer_partnership_year_established,
        g.revenue AS customer_revenue,
        g.employees AS customer_number_of_employees,
        g.office_location AS customer_office_location,
        COALESCE(g.subsidiary_of, 'Unknown') AS customer_is_subsidiary_of,
        g.series AS product_series,
        g.sales_price AS product_retail_sales_price,
        g.manager AS sales_agent_manager,
        g.regional_office AS sales_agent_regional_office,
        g.sales_cycle_duration AS business_sales_cycle_duration,
        g.agent_close_rate AS agent_won_deal_effectiveness,
        g.opportunities_per_account AS business_opportunities_per_customer,
        g.opportunities_per_sales_agent AS business_opportunities_per_sales_agent,
        c.first_purchase AS customer_first_purchase,
        c.last_purchase AS customer_last_purchase,
        c."Recency" AS absolute_customer_recency_value,
        c."Frequency" AS absolute_customer_frequency_value,
        c."Monetary" AS absolute_customer_monetary_value,
        c."R_Score" AS customer_recency_score,
        c."F_Score" AS customer_frequency_score,
        c."M_Score" AS customer_monetary_score,
        c."RFM_Score" AS customer_recency_frequency_monetary_score,
        CASE 
            WHEN c."RFM_Custom_Segment" ~ '^[0-9]+$' THEN 'Other'
            ELSE c."RFM_Custom_Segment"
        END AS customer_recency_frequency_monetary_segment,
        c.engagement_score AS customer_engagement_score,
        c."Actual_CLTV" AS actual_customer_lifetime_value,
        c."RF_Ratio" AS recency_frequency_ratio,
        c."ATV" AS customer_average_transaction_value,
        m."T" AS customer_days_since_first_purchase,
        m.prob_alive AS prob_alive_customer,
        m.expected_purchases_day AS customer_expected_purchases_day,
        m.expected_purchases_week AS customer_expected_purchases_week,
        m.expected_purchases_monthly AS customer_expected_purchases_monthly,
        m.expected_purchases_bimonthly AS customer_expected_purchases_bimonthly,
        m.expected_purchases_trimester AS customer_expected_purchases_trimester,
        m.expected_purchases_half_year AS customer_expected_purchases_half_year,
        m.expected_purchases_year AS customer_expected_purchases_year,
        m.expected_average_profit AS customer_expected_average_profit,
        m."Predicted_Year_CLTV" AS customer_predicted_year_cltv,
        m."Predicted_CLTV_Segment" AS customer_predicted_cltv_segment
    FROM 
        general_enriched_dataset g

    INNER JOIN customers_rfm_features c
        ON c.account = g.account

    INNER JOIN model_predictions_summary m
        ON c.account = m.account
)

SELECT
    * 
FROM 
    renamed_merged_data