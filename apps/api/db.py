"""Database access for the API.

Public endpoints run as `public_reader` on a read-only transaction. That role
cannot reach zone B at all, so the database stops a leak even if a query in
the application is wrong (ADR-004).

One connection per request for now. A pool is added with the hosting setup (S0-02).
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import psycopg


def database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return url


def public_connection() -> Iterator[psycopg.Connection]:
    """FastAPI dependency: a read-only connection acting as public_reader."""
    with psycopg.connect(database_url()) as conn:
        conn.read_only = True
        conn.execute("SET ROLE public_reader")
        try:
            yield conn
        finally:
            conn.rollback()
