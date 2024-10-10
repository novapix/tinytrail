from contextlib import asynccontextmanager

from fastapi import FastAPI
from logger import setup_logger

logger = setup_logger(name="tinytrail")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    logger.info("Starting up the application...")
    yield
    # Shutdown event
    logger.info("Shutting down the application...")

app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
