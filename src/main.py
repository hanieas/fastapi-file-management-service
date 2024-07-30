from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.config import config
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.system('alembic revision --autogenerate -m "Added account table"')
    if config.ENV == "testing":
        os.system("alembic upgrade head")
    else:
        os.system("alembic downgrade base")
        os.system("alembic upgrade head")
    yield


def create_application() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    return app

app = create_application()

@app.get('/home')
def home():
    return "Hello World!"