from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request

from ..routers import routers
from .sio_server import *
from .utils import *


server = FastAPI(
    title="DispatchXchange REST API Server",
    lifespan=lifespan,
)

sio_server.other_asgi_app = server
server.mount("/ws", sio_app, name="websocket")


# Custom middleware to handle large file uploads
class MaxUploadSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_size: int = 4 * 1024 * 1024 * 1024):  # 4GB in bytes
        super().__init__(app)

        self.max_size = max_size

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_size:
            return JSONResponse(
                {
                    "detail": f"File size exceeds the maximum allowed size of {self.max_size // 1024 // 1024 // 1024}GB."
                },
                status_code=413,
            )
        response = await call_next(request)
        return response


server.add_middleware(MaxUploadSizeMiddleware)  # 4GB


server.add_middleware(
    CORSMiddleware,
    allow_origins=wildcard,
    allow_methods=wildcard,
    allow_headers=wildcard,
    allow_credentials=True,
    expose_headers=wildcard,
)

server.include_router(routers)
