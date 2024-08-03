from fastapi import APIRouter, UploadFile, Form, File, Request
from fastapi.responses import JSONResponse
from infrastructure.db.mysql import mysql as db
from repositories.file_repository import FileRepo
from services.file_service import FileService
from handlers.file_handler import FileHandler
from dto.file_dto import FileDTO
from typing import Annotated, Dict, Any, Optional

router = APIRouter(
    prefix="/api/v1/file",
    tags=["file"]
)

file_handler = FileHandler(service=FileService(repo=FileRepo(db=db)))


@router.post('/upload', response_model=FileDTO)
async def upload(
    file: UploadFile = File(...),
    size: int = Form(...),
    credential: Optional[str] = Form(None),
    detail: Optional[str] = Form(None)
) -> any:
    return await file_handler.upload_file(file, credential, detail, size)

@router.get('/get/{id}', response_model=FileDTO)
async def get_file(id: str, request: Request)-> JSONResponse:
    query_params = dict(request.query_params)
    return await file_handler.get_file(id, query_params=query_params)
