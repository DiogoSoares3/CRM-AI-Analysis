from typing import ClassVar
import os

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

class Settings(BaseSettings):

    """
    General configs used for the the aplication
    """

    DBBaseModel: ClassVar = declarative_base()

    load_dotenv()
    DB_URL: ClassVar = os.getenv("DB_URL")
    PROJECT_PATH: ClassVar = os.getenv("PROJECT_PATH")

    class Config:
        case_sensitive = True


settings: Settings = Settings()
