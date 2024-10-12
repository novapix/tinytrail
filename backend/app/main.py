from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from .logger import logger
from .database import close_db, initialize_db
from .routes import router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the application...")
    await initialize_db()
    yield
    await close_db()
    logger.info("Shutting down the application.")


app = FastAPI(lifespan=lifespan)
app.include_router(router)

# if __name__ == "__main__":
#     import uvicorn
#
#     logger.info("Starting the server...")
#     uvicorn.run(app, host="0.0.0.0", port=8000,
#                 reload_dirs=["app"], reload_excludes=["logs"])