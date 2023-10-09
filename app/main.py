import logging
import os

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

from app.api import user_endpoints, image_endpoints

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(RateLimitExceeded)
async def ratelimit_exception(request: Request, exc: RateLimitExceeded):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


app.include_router(user_endpoints.router)
app.include_router(image_endpoints.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.exception_handler(HTTPException)
def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

