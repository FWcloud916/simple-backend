import secrets

from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.middlewares.request_logger_middleware import RequestLoggerMiddleware
from app.utils.settings import settings

app = FastAPI(
    title="Customer Relations System API",
    description="API for managing customer relations",
    version="0.1",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=RequestLoggerMiddleware()
)

security = HTTPBasic()

router = APIRouter()


def get_docs_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.DOCS_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, settings.DOCS_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/v1/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_docs_auth)):
    return get_swagger_ui_html(openapi_url="/api/v1/openapi.json", title="docs")


@router.get("/v1/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


@app.get("/api/health")
async def health(request: Request):
    request.state.user = "system"
    return {"status": "ok"}


app.include_router(router, prefix="/api")
