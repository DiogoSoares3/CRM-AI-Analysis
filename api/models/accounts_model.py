from core.configs import settings
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid

class AccountsSourceModel(settings.DBBaseModel):
    __tablename__ = 'accounts_source'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    year_established = Column(String, nullable=False)
    revenue = Column(String, nullable=False)
    employees = Column(String, nullable=False)
    office_location = Column(String, nullable=False)
    subsidiary_of = Column(String, nullable=True)
