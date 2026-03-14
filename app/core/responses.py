from .logging.context import request_id_ctx
from fastapi.responses import JSONResponse


class ResponseBuilder:

    @staticmethod
    def success(message: str, status_code: int = 200, data = None):
        return JSONResponse(
            status_code=status_code, 
            content={
                "success": True,
                "message": message,
                "data": data,
                "request_id": request_id_ctx.get()
            }
        )
