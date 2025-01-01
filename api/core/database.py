from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.configs import settings

engine = create_engine(settings.DB_URL, echo=False, future=True)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)
