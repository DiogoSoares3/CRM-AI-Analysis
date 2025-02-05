from pydantic import BaseModel, NonNegativeFloat
from datetime import date

class SalesPipelineSourceSchema(BaseModel):
    """
    Represents a sales pipeline entry.

    Attributes:
        opportunity_id (str): 
            The unique identifier for the sales opportunity.
        sales_agent (str): 
            The sales agent associated with the opportunity.
        product (str): 
            The product being sold.
        account (str): 
            The account linked to the sales opportunity.
        deal_stage (str): 
            The current stage of the sales deal.
        engage_date (date): 
            The date when the engagement started.
        close_date (date): 
            The expected or actual closing date of the deal.
        close_value (NonNegativeFloat): 
            The monetary value of the closed deal.
    """
    opportunity_id: str
    sales_agent: str
    product: str
    account: str
    deal_stage: str
    engage_date: date
    close_date: date
    close_value: NonNegativeFloat
