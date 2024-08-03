from fastapi.responses import JSONResponse
from typing import Any

class Response:

    def success(self, data: Any, message: str = None, status: int = 200) -> JSONResponse:
        content = {
            "data": data,
            "message": message,
            "success": True
        }
        return JSONResponse(content=content, status_code=status)
    
    def error(self, data: any, error: str = None, status: int = 400):
        content = {}
        content["data"] = data
        content["error"] = error
        content["success"] = False
        return JSONResponse(content=content, status_code=status)
