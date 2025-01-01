from core.configs import settings
from sqlalchemy import Column, String, ForeignKey
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid

class ProductsSourceModel(settings.DBBaseModel):
    __tablename__ = 'products_source'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product = Column(String, nullable=False)
    series = Column(String, nullable=False)
    sales_price = Column(String, nullable=False)