import uvicorn
from fastapi import FastAPI

from src.database_operations import router as database_router
from src.rag_operations import router as rag_router
from src.historic_messages import router as historic_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the lifespan of the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

     Returns:
        None
    """
    pass


app = FastAPI(title='CRM Analysis API')

prefix = '/api'
app.include_router(database_router, prefix=prefix)
app.include_router(rag_router, prefix=prefix)
app.include_router(historic_router, prefix=prefix)


if __name__ == "__main__":
    print("Initializing API server...")
    uvicorn.run(
        "main:app",
        port=8200,
        host='0.0.0.0',
        reload=True,
        log_level="info"
    )
