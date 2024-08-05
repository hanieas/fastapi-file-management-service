from pydantic import BaseModel
from typing import Any, Dict, Optional


class FileBaseDTO(BaseModel):
    path: str
    credential: Optional[Dict[str, Any]]
    content_type: str
    size: int
    detail: Optional[Dict[str, Any]]


class FileDTO(FileBaseDTO):
    id: str


class UploadFilePayload(BaseModel):
    file: Any
    filename: str
    content_type: str
    detail: Optional[Dict[str, Any]]
    credential: Optional[Dict[str, Any]]
    size: int

    class Config:
        # Because Pydantic only understand the limited type. BinaryIO is not defined
        arbitrary_types_allowed = True


class FileResponseDTO(BaseModel):
    id: str
    path: str
    content_type: str
    detail:  Optional[Dict[str, Any]]
    credential:  Optional[Dict[str, Any]]
    download_url: str
