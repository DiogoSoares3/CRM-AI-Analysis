from core.configs import settings
from sqlalchemy import Column, String, Date, Float
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid

class SalesPipelineSourceModel(settings.DBBaseModel):
    __tablename__ = 'sales_pipeline_source'
    
    opportunity_id = Column(String, nullable=False, primary_key=True)
    sales_agent = Column(String, nullable=False)
    product = Column(String, nullable=False)
    account = Column(String, nullable=True)
    deal_stage = Column(String, nullable=False)
    engage_date = Column(String, nullable=True)
    close_date = Column(String, nullable=True)
    close_value = Column(String, nullable=True)
