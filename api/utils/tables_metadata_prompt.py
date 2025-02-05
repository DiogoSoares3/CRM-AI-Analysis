from typing import List
from pydantic import BaseModel


class ColumnMetadata(BaseModel):
    name: str
    description: str

class TableMetadata(BaseModel):
    name: str
    description: str
    columns: List[ColumnMetadata]


TABLES_METADATA = [
    TableMetadata(
        name="stg-won_deal_stage",
        description="Centralized table containing enriched data for sales opportunities, customer features, and predictive model outputs.",
        columns=[
            ColumnMetadata(name="opportunity_id", description="Unique identifier for each sales opportunity."),
            ColumnMetadata(name="sales_agent", description="Sales agent responsible for managing the opportunity."),
            ColumnMetadata(name="product", description="Product associated with the sales opportunity."),
            ColumnMetadata(name="customer", description="Customer account involved in the sales opportunity."),
            ColumnMetadata(name="business_deal_stage", description="Current stage of the sales opportunity in the deal pipeline."),
            ColumnMetadata(name="business_engage_date", description="Date when the engagement with the customer began."),
            ColumnMetadata(name="business_close_date", description="Date when the sales opportunity was closed."),
            ColumnMetadata(name="business_close_value", description="Monetary value of the closed deal."),
            ColumnMetadata(name="customer_sector", description="Industry sector of the customer."),
            ColumnMetadata(name="customer_partnership_year_established", description="Year when the partnership with the customer was established."),
            ColumnMetadata(name="customer_revenue", description="Annual revenue of the customer."),
            ColumnMetadata(name="customer_number_of_employees", description="Number of employees in the customer's organization."),
            ColumnMetadata(name="customer_office_location", description="Office location of the customer."),
            ColumnMetadata(name="customer_is_subsidiary_of", description="Parent organization of the customer, if any."),
            ColumnMetadata(name="product_series", description="Series or category of the product."),
            ColumnMetadata(name="product_retail_sales_price", description="Retail sales price of the product."),
            ColumnMetadata(name="sales_agent_manager", description="Manager responsible for supervising the sales agent."),
            ColumnMetadata(name="sales_agent_regional_office", description="Regional office associated with the sales agent."),
            ColumnMetadata(name="business_sales_cycle_duration", description="Duration of the sales cycle for the opportunity."),
            ColumnMetadata(name="agent_won_deal_effectiveness", description="Effectiveness rate of the sales agent in closing deals."),
            ColumnMetadata(name="business_opportunities_per_customer", description="Number of sales opportunities associated with the customer."),
            ColumnMetadata(name="business_opportunities_per_sales_agent", description="Number of opportunities handled by the sales agent."),
            ColumnMetadata(name="customer_first_purchase", description="Date of the customer's first purchase."),
            ColumnMetadata(name="customer_last_purchase", description="Date of the customer's most recent purchase."),
            ColumnMetadata(name="absolute_customer_recency_value", description="Recency of the customer's activity."),
            ColumnMetadata(name="absolute_customer_frequency_value", description="Frequency of the customer's activity."),
            ColumnMetadata(name="absolute_customer_monetary_value", description="Monetary value associated with the customer."),
            ColumnMetadata(name="customer_recency_score", description="Score representing the recency of the customer's activity."),
            ColumnMetadata(name="customer_frequency_score", description="Score representing the frequency of the customer's activity."),
            ColumnMetadata(name="customer_monetary_score", description="Score representing the monetary value of the customer."),
            ColumnMetadata(name="customer_recency_frequency_monetary_score", description="Combined RFM score for the customer."),
            ColumnMetadata(name="customer_recency_frequency_monetary_segment", description="Segment classification based on the customer's RFM score."),
            ColumnMetadata(name="customer_engagement_score", description="Score representing the customer's overall engagement."),
            ColumnMetadata(name="actual_customer_lifetime_value", description="Actual/Present lifetime value of the customer."),
            ColumnMetadata(name="recency_frequency_ratio", description="Ratio of recency to frequency for the customer."),
            ColumnMetadata(name="customer_average_transaction_value", description="Average transaction value for the customer."),
            ColumnMetadata(name="customer_days_since_first_purchase", description="Number of days since the customer's first purchase."),
            ColumnMetadata(name="prob_alive_customer", description="Probability that the customer is still active."),
            ColumnMetadata(name="customer_expected_purchases_day", description="Expected number of purchases by the customer per day."),
            ColumnMetadata(name="customer_expected_purchases_week", description="Expected number of purchases by the customer per week."),
            ColumnMetadata(name="customer_expected_purchases_monthly", description="Expected number of purchases by the customer per month."),
            ColumnMetadata(name="customer_expected_purchases_bimonthly", description="Expected number of purchases by the customer every two months."),
            ColumnMetadata(name="customer_expected_purchases_trimester", description="Expected number of purchases by the customer per trimester."),
            ColumnMetadata(name="customer_expected_purchases_half_year", description="Expected number of purchases by the customer every six months."),
            ColumnMetadata(name="customer_expected_purchases_year", description="Expected number of purchases by the customer per year."),
            ColumnMetadata(name="customer_expected_average_profit", description="Expected average profit per customer."),
            ColumnMetadata(name="predicted_year_customer_lifetime_value", description="Predicted/Expected customer lifetime value for the upcoming year."),
            ColumnMetadata(name="predicted_customer_lifetime_value_segment", description="Segment classification based on predicted CLTV."),
        ]
    ),
    TableMetadata(
        name="sector_wise_revenue_analysis",
        description="Analysis of revenue and sales cycle duration across different customer sectors.",
        columns=[
            ColumnMetadata(name="customer_sector", description="Industry sector of the customer."),
            ColumnMetadata(name="total_revenue", description="Total revenue generated from the customer sector."),
            ColumnMetadata(name="average_sales_cycle_duration", description="Average duration of the sales cycle for the sector."),
        ]
    ),
    TableMetadata(
        name="sales_performance_analysis",
        description="Analysis of sales agent performance, focusing on opportunities, revenue, and efficiency metrics.",
        columns=[
            ColumnMetadata(name="sales_agent", description="Sales agent responsible for the opportunities."),
            ColumnMetadata(name="total_opportunities", description="Total number of distinct sales opportunities handled by the agent."),
            ColumnMetadata(name="total_revenue", description="Total revenue generated by the sales agent."),
            ColumnMetadata(name="avg_close_rate", description="Average effectiveness rate of the sales agent in closing deals."),
            ColumnMetadata(name="avg_sales_cycle_duration", description="Average duration of the sales cycle for opportunities handled by the agent."),
        ]
    ),
    TableMetadata(
        name="sales_agent_performance",
        description="Detailed performance metrics for individual sales agents.",
        columns=[
            ColumnMetadata(name="sales_agent", description="Sales agent responsible for the sales."),
            ColumnMetadata(name="total_sales_value", description="Total value of sales closed by the agent."),
            ColumnMetadata(name="average_sales_cycle_duration", description="Average duration of the sales cycle for deals handled by the agent."),
            ColumnMetadata(name="average_won_deal_effectiveness", description="Average effectiveness rate of the sales agent in winning deals."),
        ]
    ),
    TableMetadata(
        name="regional_sales_performance",
        description="Performance metrics for sales across different regional offices.",
        columns=[
            ColumnMetadata(name="sales_agent_regional_office", description="Regional office responsible for sales."),
            ColumnMetadata(name="total_sales_value", description="Total value of sales closed in the regional office."),
            ColumnMetadata(name="average_won_deal_effectiveness", description="Average effectiveness rate of agents in the regional office in closing deals."),
        ]
    ),
    TableMetadata(
        name="products_sales_analysis",
        description="Analysis of product sales, including total sales value and ranking by revenue.",
        columns=[
            ColumnMetadata(name="product", description="The name or type of the product."),
            ColumnMetadata(name="product_series", description="The series or category of the product."),
            ColumnMetadata(name="total_sales_value", description="Total value of sales for the product."),
            ColumnMetadata(name="total_opportunities", description="Total number of sales opportunities associated with the product."),
            ColumnMetadata(name="sales_rank", description="Rank of the product based on total sales value."),
        ]
    ),
    TableMetadata(
        name="customer_segmentation_analysis",
        description="Analysis of customer segmentation based on RFM scores and other metrics.",
        columns=[
            ColumnMetadata(name="customer", description="The account or identifier for the customer."),
            ColumnMetadata(name="customer_revenue", description="Total revenue generated by the customer."),
            ColumnMetadata(name="customer_office_location", description="Location of the customer's office."),
            ColumnMetadata(name="customer_recency_frequency_monetary_segment", description="RFM segment classification of the customer."),
            ColumnMetadata(name="customer_average_transaction_value", description="Average transaction value for the customer."),
            ColumnMetadata(name="customer_engagement_score", description="Engagement score for the customer."),
            ColumnMetadata(name="actual_customer_lifetime_value", description="Actual lifetime value of the customer."),
            ColumnMetadata(name="customer_expected_purchases_week", description="Expected number of purchases per week by the customer."),
            ColumnMetadata(name="customer_expected_purchases_half_year", description="Expected number of purchases over six months by the customer."),
            ColumnMetadata(name="customer_expected_purchases_year", description="Expected number of purchases over a year by the customer."),
            ColumnMetadata(name="customer_expected_average_profit", description="Expected average profit from the customer."),
            ColumnMetadata(name="prob_alive_customer", description="Probability that the customer is still active."),
            ColumnMetadata(name="predicted_year_customer_lifetime_value", description="Predicted customer lifetime value for the year."),
            ColumnMetadata(name="predicted_customer_lifetime_value_segment", description="Segment classification based on predicted customer lifetime value."),
        ]
    ),
    TableMetadata(
        name="customer_retention_analysis",
        description="Analysis of customer retention metrics focusing on active customers.",
        columns=[
            ColumnMetadata(name="customer", description="The account or identifier for the customer."),
            ColumnMetadata(name="customer_recency_frequency_monetary_segment", description="RFM segment classification of the customer."),
            ColumnMetadata(name="prob_alive_customer", description="Probability that the customer is still active."),
            ColumnMetadata(name="customer_engagement_score", description="Engagement score for the customer."),
        ]
    ),
    TableMetadata(
        name="customer_profitability_analysis",
        description="Analysis of customer profitability, including ranking within RFM segments.",
        columns=[
            ColumnMetadata(name="customer", description="The account or identifier for the customer."),
            ColumnMetadata(name="customer_revenue", description="Total revenue generated by the customer."),
            ColumnMetadata(name="customer_recency_frequency_monetary_segment", description="RFM segment classification of the customer."),
            ColumnMetadata(name="customer_average_transaction_value", description="Average transaction value for the customer."),
            ColumnMetadata(name="actual_customer_lifetime_value", description="Actual lifetime value of the customer."),
            ColumnMetadata(name="customer_expected_average_profit", description="Expected average profit from the customer."),
            ColumnMetadata(name="profitability_rank", description="Ranking of the customer within their RFM segment based on expected profit."),
        ]
    )
]

def generate_tables_metadata_prompt(metadata: List[TableMetadata]) -> str:
    """
    Generates a descriptive string for table metadata.

    Args:
        metadata: List[TableMetadata]: A list of TableMetadata objects containing table information.

    Returns:
        str: A formatted string describing the tables and their columns.
    """
    table_descriptions = []
    for table in metadata:
        column_descriptions = "\n".join(
            [f"- {col.name}: {col.description}" for col in table.columns]
        )
        table_descriptions.append(
            f"Table: {table.name}\nDescription: {table.description}\nColumns:\n{column_descriptions}"
        )
    return "\n\n".join(table_descriptions)
