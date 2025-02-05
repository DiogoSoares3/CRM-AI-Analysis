from core.configs import settings
from sqlalchemy import Column, String
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid

class SalesTeamsSourceModel(settings.DBBaseModel):
    """
    Represents sales team data stored in the database.

    Attributes:
        __tablename__ (str): 
            The name of the database table ("sales_teams_source").
        id (UUID): 
            The unique identifier for the sales team record.
        sales_agent (str): 
            The name of the sales agent.
        manager (str): 
            The name of the sales agent's manager.
        regional_office (str): 
            The regional office the agent is associated with.
    """
    __tablename__ = 'sales_teams_source'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sales_agent = Column(String, nullable=False)
    manager = Column(String, nullable=False)
    regional_office = Column(String, nullable=False)