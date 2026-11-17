"""Apply SQL migrations in order. Forward-only; each file runs once, in a transaction."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import psycopg

MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "migrations"


def migrate(conn: psycopg.Connection) -> list[str]:
    """Apply pending migrations on an autocommit connection. Returns the versions applied."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS public.schema_migrations ("
        "version text PRIMARY KEY, applied_at timestamptz NOT NULL DEFAULT now())"
    )
    applied = {row[0] for row in conn.execute("SELECT version FROM public.schema_migrations")}
    done: list[str] = []
    for path in sorted(MIGRATIONS_DIR.glob("*.sql")):
        if path.stem in applied:
            continue
        with conn.transaction():
            conn.execute(path.read_text(encoding="utf-8"))
            conn.execute("INSERT INTO public.schema_migrations (version) VALUES (%s)", (path.stem,))
        done.append(path.stem)
    return done


def main() -> int:
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("DATABASE_URL is not set", file=sys.stderr)
        return 2
    with psycopg.connect(url, autocommit=True) as conn:
        done = migrate(conn)
    print("applied: " + (", ".join(done) if done else "nothing to do"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
