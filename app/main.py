from charset_normalizer.md import getLogger
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from .database.dbConfig import Base, engine
from .exceptions.external import ExternalServiceError
from .router import received_router, issued_router
from app.app_config.logging_config import setup_logging,get_logger
import logging

from .schemas.api_schema import APIResponse

Base.metadata.create_all(bind=engine)

setup_logging()

logger = get_logger('chainagex')

app = FastAPI()


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    logger.exception(
        "Database error | path=%s | method=%s",
        request.url.path,
        request.method,
    )

    return JSONResponse(
        status_code=500,
        content={
            "message": "Database error occurred",
            "status": "error",
            "data": None
        }
    )


@app.exception_handler(ExternalServiceError)
async def external_service_handler(request: Request, exc: ExternalServiceError):
    logger.warning(
        "External Service failure | path=%s | details=%s",
        request.url.path,
        exc,
    )

    return JSONResponse(
        status_code=503,
        content={
            "message": str(exc),
            "status": "error",
            "data": None
        }
    )


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled exception | path=%s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "message": "Unexpected server error",
            "status": "error",
            "data": None
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            message=str(exc.detail),
            status="failure",
            data = None
        ).model_dump()
    )

app.include_router(received_router.router, prefix='/api')
app.include_router(issued_router.router, prefix='/api')


@app.get("/")
async def root():
    return {"Hello": "World"}
