"""Upcasting: old event versions are converted when read, never rewritten in the store.

Stored events are immutable (ADR-003). When a schema gains a field, an
upcaster registered here brings older events up to the current shape at read
time. Each upcaster moves an event exactly one version forward.
"""

from __future__ import annotations

import copy
from collections.abc import Callable
from typing import Any

Event = dict[str, Any]
Upcaster = Callable[[Event], Event]

_UPCASTERS: dict[tuple[str, str], Upcaster] = {}


def register(event_type: str, from_version: str) -> Callable[[Upcaster], Upcaster]:
    def decorator(fn: Upcaster) -> Upcaster:
        _UPCASTERS[(event_type, from_version)] = fn
        return fn

    return decorator


def upcast(event: Event) -> Event:
    """Return a copy of `event` at the newest known version. The input is not modified."""
    current = copy.deepcopy(event)
    seen: set[str] = set()
    while (current["type"], current["schema_version"]) in _UPCASTERS:
        version = current["schema_version"]
        if version in seen:
            raise RuntimeError(f"upcaster loop for {current['type']} at {version}")
        seen.add(version)
        current = _UPCASTERS[(current["type"], version)](current)
    return current


@register("order.created", "1.0.0")
def _order_created_1_0_to_1_1(event: Event) -> Event:
    event["payload"].setdefault("household_key", None)
    event["schema_version"] = "1.1.0"
    return event
