from pydantic import (
    BaseModel,
    NonNegativeFloat, 
    field_validator,
    model_validator
)
from typing import Optional
from datetime import date


class UserInput(BaseModel):
    sales_agent: str
    product: str
    account: str
    unknow_customer: Optional[str] = None
    deal_stage: str
    engage_date: Optional[date] = None
    close_date: Optional[date] = None
    close_value: Optional[NonNegativeFloat] = None

    @field_validator("unknow_customer", mode="before")
    def validate_unknown_customer(cls, value, info):
        if info.data.get("account") == "Other" and not value:
            raise ValueError("If 'Other' was selected, the field 'unknow_customer' must be filled.")
        return value

    @field_validator("close_date", mode="before")
    def validate_close_date(cls, value, info):
        if (info.data.get("deal_stage") != "Engaging" and info.data.get("deal_stage") != "Prospecting") and not value:
            raise ValueError("The closing date must be entered for stages 'Won' or 'Lost'.")
        return value

    @model_validator(mode="after")
    def validate_date_difference(cls, data):
        engage_date = data.engage_date
        close_date = data.close_date
        if close_date and close_date < engage_date:
            raise ValueError("The close date must be later than or equal to the engage date.")
        return data

    @field_validator("close_value")
    def validate_close_value(cls, value, info):
        if not info.data.get("deal_stage") == 'Prospecting':
            if info.data.get("deal_stage") == "Won" and value <= 0:
                raise ValueError("The closing value must be greater than 0 for 'Won' stages.")
            return value
