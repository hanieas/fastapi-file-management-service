from pydantic import BaseModel
from typing import Any, Dict, Optional
from fastapi import UploadFile
from constants.file_extensions import FileExtension

class UploadChunkDTO(BaseModel):
    chunk_size: int
    file: UploadFile
    upload_id: str
    chunk_index: int

class UploadFileDTO(BaseModel):
    upload_id: str
    total_chunks: int
    file_extension: FileExtension
    total_size: int
    content_type: str
    detail: Optional[Dict[str, Any]]
    credential: Optional[Dict[str, Any]]

class RetryUploadFileDTO(BaseModel):
    id: str
    credential: Optional[Dict[str, Any]]


class FileBaseDTO(BaseModel):
    path: str
    credential: Optional[Dict[str, Any]]
    content_type: str
    size: int
    detail: Optional[Dict[str, Any]]
    celery_task_id: str

class FileDTO(FileBaseDTO):
    id: str

