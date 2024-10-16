from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router)

# if __name__ == "__main__":
#     import uvicorn
#
#     logger.info("Starting the server...")
#     uvicorn.run(app, host="0.0.0.0", port=8000,
#                 reload_dirs=["app"], reload_excludes=["logs"])
