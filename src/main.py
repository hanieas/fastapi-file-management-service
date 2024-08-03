from fastapi import FastAPI, APIRouter
from api.routes import file

router = APIRouter()

@router.get('/ping')
def pong():
    return {"ping":"pong"}

def create_application() -> FastAPI:
    app = FastAPI() 
    app.include_router(router) 
    app.include_router(file.router) 
    return app

app = create_application()

