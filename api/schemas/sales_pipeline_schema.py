from pydantic import BaseModel, NonNegativeFloat
from datetime import date

class SalesPipelineSourceSchema(BaseModel):
    opportunity_id: str
    sales_agent: str
    product: str
    account: str
    deal_stage: str
    engage_date: date
    close_date: date
    close_value: NonNegativeFloat
