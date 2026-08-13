#!/usr/bin/env python3
"""Lead Intelligence CLI (MISSION-002 V1).

Turn a (market, location) into a structured, scored lead list. Fixture provider
runs fully offline with no credentials.

Examples:
  python3 cli.py --market "electrical contractors" --location "Austin, TX"
  python3 cli.py --market "electrical contractors" --location "Austin, TX" \
      --limit 5 --out out/
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running as a script from the product directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from leadintel.models import Query
from leadintel.pipeline import run
from leadintel.providers.fixture import FixtureProvider
from leadintel.providers.live import LiveProvider


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="AION Lead Intelligence (V1)")
    p.add_argument("--market", required=True, help='e.g. "electrical contractors"')
    p.add_argument("--location", required=True, help='e.g. "Austin, TX"')
    p.add_argument("--limit", type=int, default=None, help="max leads to return")
    p.add_argument(
        "--provider", choices=["fixture", "live"], default="fixture",
        help="data source (default: fixture — offline, synthetic)",
    )
    p.add_argument("--fixture", default=None, help="path to a fixture JSON (fixture provider)")
    p.add_argument("--out", default="out", help="output directory (default: out/)")
    p.add_argument("--run-id", default=None, help="override run id / output basename")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.provider == "live":
        # Disabled seam — will raise with a clear approval message.
        provider = LiveProvider(enabled=False)
    else:
        provider = FixtureProvider(fixture_path=args.fixture)

    query = Query(market=args.market, location=args.location, limit=args.limit)

    try:
        result = run(query, provider=provider, out_dir=args.out, run_id=args.run_id)
    except Exception as exc:  # noqa: BLE001 - surface provider gating cleanly
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(f"Lead Intelligence run — provider={result.provider}")
    print(f"  query: {query.market} @ {query.location}")
    print(f"  leads: {result.total_leads}  avg score: {result.average_score}")
    print(f"  by status: {result.by_status}")
    print("  files:")
    for kind, path in result.files.items():
        print(f"    {kind:8} {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
