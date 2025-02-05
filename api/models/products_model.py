from core.configs import settings
from sqlalchemy import Column, String, ForeignKey
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid

class ProductsSourceModel(settings.DBBaseModel):
    """
    Represents product-related data stored in the database.

    Attributes:
        __tablename__ (str): 
            The name of the database table ("products_source").
        id (UUID): 
            The unique identifier for the product.
        product (str): 
            The name of the product.
        series (str): 
            The series to which the product belongs.
        sales_price (str): 
            The sales price of the product.
    """
    __tablename__ = 'products_source'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product = Column(String, nullable=False)
    series = Column(String, nullable=False)
    sales_price = Column(String, nullable=False)