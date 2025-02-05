from pydantic import (
    BaseModel,
    NonNegativeFloat, 
    field_validator,
    model_validator
)
from typing import Optional
from datetime import date

class UserInput(BaseModel):
    """
    A model representing the input data from the user, with validation for various fields.

    Attributes:
        sales_agent (str): The sales agent handling the deal.
        product (str): The product being dealt with.
        account (str): The account associated with the deal.
        unknow_customer (Optional[str]): An optional field for unknown customer details.
        deal_stage (str): The current stage of the deal.
        engage_date (Optional[date]): The date when the deal was engaged.
        close_date (Optional[date]): The date when the deal was closed.
        close_value (Optional[NonNegativeFloat]): The value of the closed deal, if applicable.
    """

    sales_agent: str
    product: str
    account: str
    unknow_customer: Optional[str] = None
    deal_stage: str
    engage_date: Optional[date] = None
    close_date: Optional[date] = None
    close_value: Optional[NonNegativeFloat] = None

    @field_validator("unknow_customer", mode="before")
    def validate_unknown_customer(cls, value: Optional[str], info) -> Optional[str]:
        """
        Validates the 'unknow_customer' field to ensure it's filled if the account is 'Other'.

        Args:
            value (Optional[str]): The value of the 'unknow_customer' field.
            info: Additional information about the validation context.

        Returns:
            Optional[str]: The validated value of 'unknow_customer'.
        
        Raises:
            ValueError: If 'unknow_customer' is required but not provided.
        """
        if info.data.get("account") == "Other" and not value:
            raise ValueError("If 'Other' was selected, the field 'unknow_customer' must be filled.")
        return value

    @field_validator("close_date", mode="before")
    def validate_close_date(cls, value: Optional[date], info) -> Optional[date]:
        """
        Validates the 'close_date' field to ensure it's provided for 'Won' or 'Lost' deal stages.

        Args:
            value (Optional[date]): The value of the 'close_date' field.
            info: Additional information about the validation context.

        Returns:
            Optional[date]: The validated value of 'close_date'.
        
        Raises:
            ValueError: If 'close_date' is required but not provided for certain deal stages.
        """
        if (info.data.get("deal_stage") not in ["Engaging", "Prospecting"]) and not value:
            raise ValueError("The closing date must be entered for stages 'Won' or 'Lost'.")
        return value

    @model_validator(mode="after")
    def validate_date_difference(cls, data: "UserInput") -> "UserInput":
        """
        Validates that the 'close_date' is later than or equal to the 'engage_date'.

        Args:
            data (UserInput): The instance of the class being validated.

        Returns:
            UserInput: The validated instance of the class.

        Raises:
            ValueError: If 'close_date' is earlier than 'engage_date'.
        """
        engage_date = data.engage_date
        close_date = data.close_date
        if close_date and close_date < engage_date:
            raise ValueError("The close date must be later than or equal to the engage date.")
        return data

    @field_validator("close_value")
    def validate_close_value(cls, value: Optional[NonNegativeFloat], info) -> Optional[NonNegativeFloat]:
        """
        Validates the 'close_value' field to ensure it's greater than 0 if the deal is 'Won'.

        Args:
            value (Optional[NonNegativeFloat]): The value of the 'close_value' field.
            info: Additional information about the validation context.

        Returns:
            Optional[NonNegativeFloat]: The validated value of 'close_value'.
        
        Raises:
            ValueError: If 'close_value' is less than or equal to 0 for a 'Won' deal stage.
        """
        if info.data.get("deal_stage") == "Won" and value is not None and value <= 0:
            raise ValueError("The closing value must be greater than 0 for 'Won' stages.")
        return value