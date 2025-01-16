import subprocess
import os

import requests
import fireducks.pandas as pd
from fastapi import APIRouter, Depends, Response
from sqlalchemy import MetaData, Table, Column, String, inspect, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import ProgrammingError
from langchain_openai import ChatOpenAI
import requests
from langchain_community.utilities.sql_database import SQLDatabase
from dotenv import load_dotenv

from core.database import engine
from core.deps import get_session
from core.configs import settings


load_dotenv()

router = APIRouter()


@router.get('/text-to-sql/', status_code=200, description='Run DBT models for data transformation and agregation')
def text_to_sql(session = Depends(get_session)):
    db = SQLDatabase(
        engine=engine,
        schema='dev',
        view_support=True,
    )
    
    view_to_query = [table for table in db.get_usable_table_names() if not table.endswith('_source') and not table.startswith('raw-') and not table.startswith('stg-')]
    print(view_to_query)
