from core.configs import settings
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid

class AccountsSourceModel(settings.DBBaseModel):
    """
    Represents account-related data stored in the database.

    Attributes:
        __tablename__ (str): 
            The name of the database table ("accounts_source").
        id (UUID): 
            The unique identifier for the account.
        account (str): 
            The name of the account.
        sector (str): 
            The business sector of the account.
        year_established (str): 
            The year the account was established.
        revenue (str): 
            The revenue of the account.
        employees (str): 
            The number of employees in the company.
        office_location (str): 
            The primary office location of the account.
        subsidiary_of (str, optional): 
            Indicates if the account is a subsidiary of another company.
    """
    __tablename__ = 'accounts_source'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    year_established = Column(String, nullable=False)
    revenue = Column(String, nullable=False)
    employees = Column(String, nullable=False)
    office_location = Column(String, nullable=False)
    subsidiary_of = Column(String, nullable=True)
