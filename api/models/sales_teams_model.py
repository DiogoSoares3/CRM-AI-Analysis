from core.configs import settings
from sqlalchemy import Column, String
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid

class SalesTeamsSourceModel(settings.DBBaseModel):
    __tablename__ = 'sales_teams_source'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sales_agent = Column(String, nullable=False)
    manager = Column(String, nullable=False)
    regional_office = Column(String, nullable=False)