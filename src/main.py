from fastapi import FastAPI
from api.routes import file
from exceptions.handler import ExceptionHandler

def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(file.router)
    ExceptionHandler(app)
    return app

app = create_application()
