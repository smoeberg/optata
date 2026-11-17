"""Shared fixtures.

Database tests run against a throwaway database created from the migrations
and filled with synthetic data. Locally they are skipped when no Postgres is
reachable. In CI a missing database is a failure, never a skip: a guard that
did not run has not passed.
"""

from __future__ import annotations

import os

import psycopg
import pytest
from psycopg.conninfo import make_conninfo

from tools.fixtures import generate
from tools.fixtures.load import load
from tools.migrate import migrate

ADMIN_URL = os.environ.get(
    "OPTATA_TEST_DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/postgres"
)

os.environ.setdefault("OPTATA_ENV", "test")


@pytest.fixture(scope="session")
def dataset():
    return generate(seed=42, dwellings=300, orders=60, verified_ratio=0.25)


@pytest.fixture(scope="session")
def db_url(dataset):
    name = f"optata_test_{os.getpid()}"
    try:
        admin = psycopg.connect(ADMIN_URL, autocommit=True)
    except psycopg.OperationalError as exc:
        if os.environ.get("CI"):
            pytest.fail(f"database tests cannot run in CI: {exc}")
        pytest.skip(f"no Postgres reachable at OPTATA_TEST_DATABASE_URL: {exc}")
    admin.execute(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')
    admin.execute(f'CREATE DATABASE "{name}"')
    url = make_conninfo(ADMIN_URL, dbname=name)
    try:
        with psycopg.connect(url, autocommit=True) as conn:
            migrate(conn)
            load(conn, dataset)
        yield url
    finally:
        admin.execute(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')
        admin.close()


@pytest.fixture
def conn(db_url):
    """A superuser connection. Tests switch role with SET LOCAL ROLE; all changes roll back."""
    with psycopg.connect(db_url) as connection:
        # Open the outer transaction now. Every `conn.transaction()` in a test is
        # then a savepoint. Without this, a block that is first on the connection
        # would commit on success, and a failing guard would leak into later tests.
        connection.execute("SELECT 1")
        yield connection
        connection.rollback()
