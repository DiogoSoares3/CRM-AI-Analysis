from core.database import Session
from typing import Generator

def get_session() -> Generator[Session, None, None]:
    """
    Provides a database session, ensuring proper resource management.

    Yields:
        Session:
            A SQLAlchemy session for executing database queries.
    """
    session = Session()
    try:
        yield session
    finally:
        session.close()