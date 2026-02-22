from .logging.context import request_id_ctx


class ResponseBuilder:

    @staticmethod
    def success(message: str, data=None):
        return {
            "success": True,
            "message": message,
            "data": data,
            "request_id": request_id_ctx.get()
        }
