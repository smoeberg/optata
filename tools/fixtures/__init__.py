"""Deterministic synthetic data. The only data allowed outside production."""

from tools.fixtures.generate import BOLIGKODER, cvr_is_valid, generate

__all__ = ["BOLIGKODER", "cvr_is_valid", "generate"]
