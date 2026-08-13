"""Research providers — the pluggable data-acquisition boundary.

`FixtureProvider` is the default (deterministic, synthetic, offline).
`LiveProvider` is a disabled seam for real acquisition (YELLOW gate).
"""
from .base import ResearchProvider, RawBusiness
from .fixture import FixtureProvider
from .dataaxle import DataAxleProvider, DataAxleGateError

__all__ = [
    "ResearchProvider", "RawBusiness", "FixtureProvider",
    "DataAxleProvider", "DataAxleGateError",
]
