from fastapi import APIRouter, UploadFile, Form, Request
from fastapi.responses import JSONResponse
from infrastructure.db.mysql import mysql as db
from repositories.file_repository import FileRepo
from services.file_service import FileService
from handlers.file_handler import FileHandler
from api.responses.file_response import FileResponse, UploadInitResponse, UploadChunkResponse, UploadStatusResponse
from typing import Optional
from api.responses.response import SuccessResponse, ErrorResponse
from core.config import config
from constants.file_extensions import FileExtension

router = APIRouter(
    prefix="/api/v1/file",
    tags=["file"]
)

file_handler = FileHandler(service=FileService(repo=FileRepo(db=db)))


@router.post("/upload/init/", response_model=SuccessResponse[UploadInitResponse])
async def endpoint():
    return await file_handler.upload_initialize()


@router.post("/upload/chunk/", response_model=SuccessResponse[UploadChunkResponse], responses={
    422: {"model": ErrorResponse},
})
async def endpoint(chunk_size: int = Form(..., le=config.APP_MAX_CHUNK_SIZE),
                   upload_id: str = Form(...), chunk_index: int = Form(...), file: UploadFile = Form(...)):
    return await file_handler.upload_chunk(chunk_size=chunk_size, upload_id=upload_id, chunk_index=chunk_index, file=file)


@router.post("/upload/complete/", response_model=SuccessResponse[FileResponse], responses={
    422: {"model": ErrorResponse},
})
async def endpoint(upload_id: str = Form(...), total_chunks: int = Form(...),
                   total_size: int = Form(...), credential: Optional[str] = Form(None),
                   file_extension: FileExtension = Form(...), content_type: str = Form(...),
                   detail: Optional[str] = Form(None)):
    return await file_handler.upload_complete(upload_id=upload_id, total_chunks=total_chunks, total_size=total_size,
                                          file_extension=file_extension, content_type=content_type,
                                          credential=credential, detail=detail)


@router.get('/get/{id}', response_model=SuccessResponse[FileResponse], responses={
    404: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    403: {"model": ErrorResponse}
})
async def endpoint(id: str, request: Request) -> JSONResponse:
    credential = dict(request.query_params)
    return await file_handler.get_file(id, credential=credential)


@router.get('/status/{file_id}', response_model=SuccessResponse[UploadStatusResponse], responses={
    404: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    403: {"model": ErrorResponse}
})
async def endpoint(file_id: str, request: Request) -> JSONResponse:
    credential = dict(request.query_params)
    return await file_handler.get_upload_status(file_id=file_id, credential=credential)


@router.post('/upload/retry', response_model=SuccessResponse[FileResponse], responses={
    404: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    403: {"model": ErrorResponse}
})
async def endpoint(file_id: str = Form(...), credential: Optional[str] = Form(None)) -> JSONResponse:
    return await file_handler.retry_upload(file_id=file_id, credential=credential)
