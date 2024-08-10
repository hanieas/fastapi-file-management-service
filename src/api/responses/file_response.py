from pydantic import BaseModel
from typing import Optional, Dict, Any

class UploadInitResponse(BaseModel):
    chunck_size: int
    upload_id: str


class UploadChunkResponse(BaseModel):
    chunk_index: int
    upload_id: str


class FileResponse(BaseModel):
    id: str
    path: str
    content_type: str
    detail:  Optional[Dict[str, Any]]
    credential:  Optional[Dict[str, Any]]
    download_url: str
