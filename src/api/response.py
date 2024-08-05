from fastapi.responses import JSONResponse
from typing import Any, TypeVar, Generic, Type, Optional, Sequence
from pydantic import BaseModel

T = TypeVar('T')

class SuccessResponse(BaseModel,Generic[T]):
    data: T
    message: Optional[str] = ''
    success: bool = True

class ErrorResponse(BaseModel):
    errors: Optional[Sequence[str]] = []
    message: Optional[str] = ''
    success: bool = False

class Response:
    def success(self, content: SuccessResponse, status: int = 200) -> JSONResponse:
        return JSONResponse(content=content.model_dump(), status_code=status)
    
    def error(self, content: ErrorResponse, status: int = 400) -> JSONResponse:
        return JSONResponse(content=content.model_dump(), status_code=status)

response = Response()