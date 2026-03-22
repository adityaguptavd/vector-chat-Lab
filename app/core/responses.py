from .logging.context import request_id_ctx
from fastapi.responses import JSONResponse
import json
from typing import AsyncGenerator, Optional

class ResponseBuilder:

    @staticmethod
    def success(message: str, status_code: int = 200, data = None) -> JSONResponse:
        return JSONResponse(
            status_code=status_code, 
            content={
                "success": True,
                "message": message,
                "data": data,
                "request_id": request_id_ctx.get()
            }
        )
    
    @staticmethod
    def error(
        status_code: int,
        message: str,
        errors=None,
        error_code: str | None = None,
        metadata: dict | None = None,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message,
                "error_code": error_code,
                "errors": errors,
                "metadata": metadata,
                "request_id": request_id_ctx.get(),
            },
        )


class StreamResponseBuilder:

    @staticmethod
    def chunk(data: str) -> str:
        return f"event: chunk\ndata: {data}\n\n"

    @staticmethod
    def error(message: str) -> str:
        return f"event: error\ndata: {json.dumps({'message': message})}\n\n"

    @staticmethod
    def warning(message: str) -> str:
        return f"event: warning\ndata: {json.dumps({'message': message})}\n\n"

    @staticmethod
    def end(payload: Optional[dict]) -> str:
        return f"event: end\ndata: {json.dumps(payload)}\n\n"
