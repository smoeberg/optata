"""FastAPI application.

Every route added here must first exist in contracts/openapi.yaml.
tests/contract/test_openapi.py fails the build otherwise (CI gate 1).
"""

from __future__ import annotations

import uuid
from typing import Annotated, Any

import psycopg
from fastapi import Depends, FastAPI, Query, Request, Response
from fastapi.responses import JSONResponse

from apps.api.db import public_connection
from core.registry import read

app = FastAPI(title="Optata Core API", docs_url=None, redoc_url=None, openapi_url=None)

PublicConn = Annotated[psycopg.Connection, Depends(public_connection)]
_CACHE = "public, max-age=300"


class NotFound(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


@app.middleware("http")
async def trace(request: Request, call_next):
    """Give every request a trace id and return it, so a report can be followed in the logs."""
    request.state.trace_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Trace-Id"] = request.state.trace_id
    return response


@app.exception_handler(NotFound)
async def not_found(request: Request, exc: NotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"code": "NOT_FOUND", "message": exc.message,
                 "trace_id": request.state.trace_id},
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/areas")
def areas(conn: PublicConn, response: Response,
          q: Annotated[str | None, Query(max_length=80)] = None,
          level: Annotated[str | None, Query(pattern="^(MUNICIPALITY|ZIP|NEIGHBOURHOOD|STREET)$")]
          = None) -> list[dict[str, Any]]:
    response.headers["Cache-Control"] = _CACHE
    return read.search_areas(conn, q, level)


@app.get("/areas/{area_id}/profile")
def area_profile(area_id: str, conn: PublicConn, response: Response) -> dict[str, Any]:
    profile = read.area_profile(conn, area_id)
    if profile is None:
        raise NotFound("Unknown area")
    response.headers["Cache-Control"] = _CACHE
    return profile


@app.get("/properties/{address_id}")
def property_lookup(address_id: str, conn: PublicConn, response: Response) -> dict[str, Any]:
    # A malformed id and an unknown id give the same answer: nothing to enumerate.
    try:
        key = str(uuid.UUID(address_id))
    except ValueError:
        raise NotFound("Unknown address") from None
    found = read.current_property(conn, key)
    if found is None:
        raise NotFound("Unknown address")
    response.headers["Cache-Control"] = _CACHE
    return found
