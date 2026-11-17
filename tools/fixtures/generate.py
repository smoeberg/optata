"""Synthetic data generator v0 (S0-05).

Rules:
  * Deterministic: the same arguments always give byte-identical output.
    Nothing here reads the clock or an unseeded random source.
  * Watermarked: every record carries `_synthetic: true` and `_seed`.
  * No real personal data: no CPR numbers, no e-mail addresses, no phone
    numbers, no real names. CVR numbers are deliberately invalid (they fail
    the modulus-11 check), so they can never collide with a real company.
  * Place names, area ids and coordinates are fictional. The coordinates lie
    in open sea.

Fixtures built in on every run:
  FX-01  andelsforening: one BFE with 40 dwellings (one-to-many must hold)
  FX-02  rental property: one BFE with 12 dwellings, owned by a company
  FX-03  two identities in the same household, one order between them
"""

from __future__ import annotations

import hashlib
import json
import random
import uuid
from datetime import UTC, date, datetime, timedelta
from typing import Any

_NAMESPACE = uuid.UUID("0f7a7a2e-5d0c-4c1b-9a53-6f7074617461")
_EPOCH = datetime(2026, 1, 1, tzinfo=UTC)

# BBR-like usage codes. Only these count as dwellings in the density denominator.
BOLIGKODER = frozenset({"120", "130", "140"})
_NON_RESIDENTIAL = "320"

MUNICIPALITY_ID = "SYN-MUN-01"
ZIP_ID = "SYN-ZIP-0001"
FX01_BFE = "SYN-BFE-1001"
FX02_BFE = "SYN-BFE-2002"
FX01_UNITS = 40
FX02_UNITS = 12
_NEIGHBOURHOODS = 4

_ACTIVE_BASE = {"VILLA": "120", "RAEKKEHUS": "130", "LEJLIGHED": "140"}


def cvr_is_valid(cvr: str) -> bool:
    """Danish CVR modulus-11 check."""
    weights = (2, 7, 6, 5, 4, 3, 2, 1)
    return (
        len(cvr) == 8
        and cvr.isdigit()
        and sum(int(c) * w for c, w in zip(cvr, weights, strict=True)) % 11 == 0
    )


def _rng(seed: int, label: str) -> random.Random:
    return random.Random(f"{seed}:{label}")


def _uid(seed: int, kind: str, index: int | str) -> str:
    return str(uuid.uuid5(_NAMESPACE, f"{seed}:{kind}:{index}"))


def _invalid_cvr(seed: int, index: int) -> str:
    rng = _rng(seed, f"cvr:{index}")
    while True:
        candidate = str(rng.randrange(10_000_000, 100_000_000))
        if not cvr_is_valid(candidate):
            return candidate


def _mark(seed: int, record: dict[str, Any]) -> dict[str, Any]:
    return {"_synthetic": True, "_seed": seed, **record}


def _budget_band(budget_max: int) -> str:
    lower = (budget_max // 500_000) * 0.5
    return f"{lower:.1f}-{lower + 0.5:.1f}M"


def _areas_and_properties(
    seed: int, dwellings: int
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    n_streets = max(_NEIGHBOURHOODS, dwellings // 40)
    neighbourhood_ids = [f"SYN-NBH-{k:02d}" for k in range(1, _NEIGHBOURHOODS + 1)]
    street_ids = [f"SYN-STR-{j:04d}" for j in range(1, n_streets + 1)]
    street_parent = {
        sid: neighbourhood_ids[j % _NEIGHBOURHOODS] for j, sid in enumerate(street_ids)
    }

    rng = _rng(seed, "property")
    properties: list[dict[str, Any]] = []

    def add(index: int, bfe: str, street_id: str, usage: str, owner_kind: str,
            owner_cvr: str | None) -> None:
        properties.append(
            _mark(seed, {
                "address_id": _uid(seed, "address", index),
                "bfe": bfe,
                "municipality_id": MUNICIPALITY_ID,
                "zip_id": ZIP_ID,
                "neighbourhood_id": street_parent[street_id],
                "street_id": street_id,
                "attrs": {
                    "anvendelse": usage,
                    "areal": rng.randrange(45, 220),
                    "vaerelser": rng.randrange(1, 7),
                    "opfoerelsesaar": rng.randrange(1900, 2024),
                },
                "owner_kind": owner_kind,
                "owner_cvr": owner_cvr,
                "lon": round(11.0 + rng.random() * 0.05, 6),
                "lat": round(56.5 + rng.random() * 0.03, 6),
                "valid_from": date(2020, 1, 1).isoformat(),
                "valid_to": None,
                "recorded_at": _EPOCH.isoformat(),
            })
        )

    index = 0
    for _ in range(FX01_UNITS):  # FX-01
        add(index, FX01_BFE, street_ids[0], "140", "ANDELSFORENING", None)
        index += 1
    company_cvr = _invalid_cvr(seed, 0)
    for _ in range(FX02_UNITS):  # FX-02
        add(index, FX02_BFE, street_ids[1], "140", "COMPANY", company_cvr)
        index += 1
    for i in range(dwellings - FX01_UNITS - FX02_UNITS):
        usage = rng.choice(sorted(BOLIGKODER))
        add(index, f"SYN-BFE-{10_000 + i}", street_ids[i % n_streets], usage, "PRIVATE", None)
        index += 1
    # Non-residential units. They exist in the register but must never be
    # counted as dwellings.
    for i in range(max(1, dwellings // 100)):
        add(index, f"SYN-BFE-{90_000 + i}", street_ids[i % n_streets], _NON_RESIDENTIAL,
            "COMPANY", _invalid_cvr(seed, i + 1))
        index += 1

    def count(key: str, value: str) -> int:
        return sum(
            1 for p in properties if p[key] == value and p["attrs"]["anvendelse"] in BOLIGKODER
        )

    areas = [
        _mark(seed, {
            "area_id": MUNICIPALITY_ID, "level": "MUNICIPALITY", "parent_id": None,
            "name": "Syntetisk Kommune",
            "dwelling_count": count("municipality_id", MUNICIPALITY_ID),
        }),
        _mark(seed, {
            "area_id": ZIP_ID, "level": "ZIP", "parent_id": MUNICIPALITY_ID,
            "name": "0001 Testby", "dwelling_count": count("zip_id", ZIP_ID),
        }),
    ]
    for k, nid in enumerate(neighbourhood_ids, start=1):
        areas.append(_mark(seed, {
            "area_id": nid, "level": "NEIGHBOURHOOD", "parent_id": ZIP_ID,
            "name": f"Testkvarter {k}", "dwelling_count": count("neighbourhood_id", nid),
        }))
    for j, sid in enumerate(street_ids, start=1):
        areas.append(_mark(seed, {
            "area_id": sid, "level": "STREET", "parent_id": street_parent[sid],
            "name": f"Testvej {j}", "dwelling_count": count("street_id", sid),
        }))
    return areas, properties


def _envelope(seed: int, event_type: str, version: str, order_id: str, pseudonym: str,
              occurred_at: datetime, payload: dict[str, Any],
              causation_id: str | None = None) -> dict[str, Any]:
    stamp = occurred_at.isoformat()
    return {
        "event_id": _uid(seed, f"event:{event_type}", order_id),
        "type": event_type,
        "schema_version": version,
        "occurred_at": stamp,
        "recorded_at": stamp,
        "actor": {"kind": "USER", "pseudonym": pseudonym, "org_id": None},
        "zone": "B",
        "aggregate": {"kind": "ORDER", "id": order_id},
        "trace_id": f"synthetic-{seed}-{order_id[:8]}",
        "causation_id": causation_id,
        "payload": payload,
    }


def generate(seed: int = 42, dwellings: int = 10_000, orders: int = 1_000,
             verified_ratio: float = 0.25) -> dict[str, list[dict[str, Any]]]:
    """Build a complete synthetic dataset for one fictional postal area."""
    if dwellings < 100:
        raise ValueError("dwellings must be at least 100 so FX-01 and FX-02 fit")
    if not 0 <= verified_ratio <= 1:
        raise ValueError("verified_ratio must be between 0 and 1")

    areas, properties = _areas_and_properties(seed, dwellings)
    private_addresses = [p["address_id"] for p in properties if p["owner_kind"] == "PRIVATE"
                         and p["attrs"]["anvendelse"] in BOLIGKODER]
    neighbourhood_ids = [a["area_id"] for a in areas if a["level"] == "NEIGHBOURHOOD"]

    identities: list[dict[str, Any]] = []
    contacts: list[dict[str, Any]] = []
    order_rows: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []

    def add_identity(index: int, household_key: str) -> dict[str, Any]:
        identity_id = _uid(seed, "identity", index)
        identity = _mark(seed, {
            "identity_id": identity_id,
            "provider": "MITID_PRIVATE",
            "pseudonym": f"K-{hashlib.sha256(identity_id.encode()).hexdigest()[:8].upper()}",
            "provider_sub": f"synthetic-sub-{identity_id}",
            "assurance": "SUBSTANTIAL",
            "cvr": None,
            "household_key": household_key,
            "created_at": _EPOCH.isoformat(),
            "erased_at": None,
        })
        identities.append(identity)
        contacts.append(_mark(seed, {
            "identity_id": identity_id, "full_name": f"Testperson {index:05d}",
        }))
        return identity

    n_verified = round(orders * verified_ratio)
    rng = _rng(seed, "orders")
    for i in range(orders):
        household_key = _uid(seed, "household", i)
        buyer = add_identity(i, household_key)
        if rng.random() < 0.4:
            scope, address_id, area_id = "ADDRESS", rng.choice(private_addresses), ZIP_ID
        else:
            scope, address_id = "AREA", None
            area_id = ZIP_ID if rng.random() < 0.5 else rng.choice(neighbourhood_ids)
        criteria = {
            "type": rng.choice(sorted(_ACTIVE_BASE)),
            "areal_min": rng.choice([60, 80, 100, 120, 140]),
            "rooms_min": rng.randrange(2, 6),
            "budget_max": rng.randrange(20, 80) * 100_000,
            "horizon": rng.choice(["0-3M", "3-6M", "6-12M", "12M+"]),
        }
        level = "VERIFIED" if i < n_verified else "QUALIFIED"
        created = _EPOCH + timedelta(days=rng.randrange(0, 270), minutes=rng.randrange(0, 1440))
        order_id = _uid(seed, "order", i)
        order_rows.append(_mark(seed, {
            "order_id": order_id,
            "buyer_id": buyer["identity_id"],
            "household_key": household_key,
            "scope": scope,
            "area_id": area_id,
            "address_id": address_id,
            "criteria": criteria,
            "level": level,
            "status": "ACTIVE",
            "created_at": created.isoformat(),
            "last_signal_at": created.isoformat(),
        }))
        criteria_hash = hashlib.sha256(
            json.dumps(criteria, sort_keys=True).encode()
        ).hexdigest()
        created_event = _envelope(seed, "order.created", "1.1.0", order_id, buyer["pseudonym"],
                                  created, {
                                      "scope": scope, "area_id": area_id,
                                      "address_id": address_id, "level": "QUALIFIED",
                                      "household_key": household_key,
                                      "criteria_hash": criteria_hash, "channel": None,
                                  })
        events.append(_mark(seed, {"order_id": order_id, "envelope": created_event}))
        if level == "VERIFIED":
            verified_at = created + timedelta(days=2)
            events.append(_mark(seed, {"order_id": order_id, "envelope": _envelope(
                seed, "order.verified", "1.0.0", order_id, buyer["pseudonym"], verified_at, {
                    "verification_id": _uid(seed, "verification", i),
                    "method": "BANK_DOCUMENT",
                    "issuer_code": None,
                    "budget_band": _budget_band(criteria["budget_max"]),
                    "expires_at": (verified_at + timedelta(days=90)).date().isoformat(),
                    "reviewed_by": "synthetic-reviewer",
                }, causation_id=created_event["event_id"])}))

    # FX-03: a second person in the first household. No second order: co-buyers
    # share one order.
    add_identity(orders, order_rows[0]["household_key"] if order_rows
                 else _uid(seed, "household", 0))

    return {
        "areas": areas,
        "properties": properties,
        "identities": identities,
        "identity_contacts": contacts,
        "orders": order_rows,
        "order_events": events,
    }
