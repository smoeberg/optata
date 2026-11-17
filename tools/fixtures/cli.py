"""Command line entry point for the synthetic data generator.

    optata-fixtures generate --seed 42 --out fixtures/generated/
    optata-fixtures load --seed 42            # needs DATABASE_URL and OPTATA_ENV=dev
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import psycopg

from tools.fixtures.generate import generate
from tools.fixtures.load import load


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--dwellings", type=int, default=10_000)
    parser.add_argument("--orders", type=int, default=1_000)
    parser.add_argument("--verified-ratio", type=float, default=0.25)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="optata-fixtures")
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate", help="write the dataset as JSON files")
    _common(gen)
    gen.add_argument("--out", type=Path, default=Path("fixtures/generated"))
    ld = sub.add_parser("load", help="insert the dataset into DATABASE_URL")
    _common(ld)
    args = parser.parse_args(argv)

    data = generate(args.seed, args.dwellings, args.orders, args.verified_ratio)

    if args.command == "generate":
        args.out.mkdir(parents=True, exist_ok=True)
        for name, rows in data.items():
            path = args.out / f"{name}.json"
            path.write_text(json.dumps(rows, indent=1, sort_keys=True) + "\n", encoding="utf-8")
            print(f"{path}: {len(rows)} records")
        return 0

    url = os.environ.get("DATABASE_URL")
    if not url:
        print("DATABASE_URL is not set", file=sys.stderr)
        return 2
    with psycopg.connect(url) as conn:
        counts = load(conn, data)
    print(", ".join(f"{name}: {n}" for name, n in counts.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
