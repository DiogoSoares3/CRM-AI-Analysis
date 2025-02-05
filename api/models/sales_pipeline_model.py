from core.configs import settings
from sqlalchemy import Column, String, Date, Float
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid

class SalesPipelineSourceModel(settings.DBBaseModel):
    """
    Represents sales pipeline data stored in the database.

    Attributes:
        __tablename__ (str): 
            The name of the database table ("sales_pipeline_source").
        opportunity_id (str): 
            The unique identifier for the sales opportunity.
        sales_agent (str): 
            The sales agent handling the opportunity.
        product (str): 
            The product associated with the opportunity.
        account (str, optional): 
            The account linked to the opportunity.
        deal_stage (str): 
            The current stage of the sales deal.
        engage_date (str, optional): 
            The date the opportunity was first engaged.
        close_date (str, optional): 
            The date the opportunity was closed.
        close_value (str, optional): 
            The closing value of the deal.
    """
    __tablename__ = 'sales_pipeline_source'
    
    opportunity_id = Column(String, nullable=False, primary_key=True)
    sales_agent = Column(String, nullable=False)
    product = Column(String, nullable=False)
    account = Column(String, nullable=True)
    deal_stage = Column(String, nullable=False)
    engage_date = Column(String, nullable=True)
    close_date = Column(String, nullable=True)
    close_value = Column(String, nullable=True)
