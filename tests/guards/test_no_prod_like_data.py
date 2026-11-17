"""Guard: fixtures contain nothing that could be real personal data (CI gate 10, ADR-012).

DRAFT written by an AI assistant. Guard tests are a red field: a human owner
must review this file before it counts as a guard (projektgrundlag §7.1).
"""

import re
from datetime import date

from tools.fixtures import cvr_is_valid

# A standalone run of digits that is not part of an id such as a UUID.
_CPR = re.compile(r"(?<![\w-])(\d{2})(\d{2})(\d{2})-?\d{4}(?![\w-])")
_PHONE = re.compile(r"(?<![\w-])(?:\+45\s?)?\d{2}\s?\d{2}\s?\d{2}\s?\d{2}(?![\w-])")
_EMAIL = re.compile(r"[\w.+-]+@([\w-]+\.)+[\w-]+")


def _strings(value, key=None):
    if isinstance(value, dict):
        for k, child in value.items():
            yield from _strings(child, k)
    elif isinstance(value, list):
        for child in value:
            yield from _strings(child, key)
    elif isinstance(value, str):
        yield key, value


def _looks_like_cpr(text):
    for match in _CPR.finditer(text):
        day, month, year = (int(g) for g in match.groups())
        try:
            date(1900 + year, month, day)
        except ValueError:
            continue
        return True
    return False


def test_every_record_is_watermarked(dataset):
    for name, rows in dataset.items():
        assert rows, f"{name} is empty"
        for row in rows:
            assert row["_synthetic"] is True, name
            assert row["_seed"] == 42, name


def test_no_cpr_phone_or_real_email(dataset):
    for name, rows in dataset.items():
        for row in rows:
            for key, text in _strings(row):
                if key in {"cvr", "owner_cvr"}:
                    continue
                assert not _looks_like_cpr(text), f"{name}.{key}: {text}"
                assert not _PHONE.search(text), f"{name}.{key}: {text}"
                for match in _EMAIL.finditer(text):
                    assert match.group(0).endswith(".invalid"), f"{name}.{key}: {text}"


def test_cvr_numbers_are_invalid_on_purpose(dataset):
    cvrs = {p["owner_cvr"] for p in dataset["properties"] if p["owner_cvr"]}
    assert cvrs
    for cvr in cvrs:
        assert len(cvr) == 8 and cvr.isdigit()
        assert not cvr_is_valid(cvr), cvr


def test_names_are_obviously_fake(dataset):
    for contact in dataset["identity_contacts"]:
        assert re.fullmatch(r"Testperson \d{5}", contact["full_name"])


def test_the_detectors_actually_detect():
    """A guard that cannot fail is not a guard."""
    assert _looks_like_cpr("cpr 010190-1234")
    assert not _looks_like_cpr("id 991390-1234")
    assert _PHONE.search("ring 20 45 66 77")
    assert _PHONE.search("+45 20456677")
    assert _EMAIL.search("skriv til a@example.com")
    assert cvr_is_valid("10150817")


def test_database_rows_are_all_marked_synthetic(conn):
    for table in ("zone_a.area", "zone_a.property", "zone_b.identity", "zone_b.orders",
                  "zone_b.order_event", "vault.identity_contact"):
        unmarked = conn.execute(
            f"SELECT count(*) FROM {table} WHERE synthetic_seed IS NULL"
        ).fetchone()[0]
        assert unmarked == 0, table
