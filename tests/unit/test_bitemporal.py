import uuid
from dataclasses import replace
from datetime import UTC, date, datetime

import pytest

from core.events import validate_event
from core.registry import OutOfOrderVersion, PropertyVersion, property_as_of, upsert_property

JAN = datetime(2026, 1, 10, tzinfo=UTC)
MAR = datetime(2026, 3, 10, tzinfo=UTC)
JUN = datetime(2026, 6, 10, tzinfo=UTC)


@pytest.fixture
def version(dataset):
    base = dataset["properties"][100]
    return PropertyVersion(
        address_id=str(uuid.uuid4()), bfe="SYN-BFE-TEST", municipality_id=base["municipality_id"],
        zip_id=base["zip_id"], neighbourhood_id=base["neighbourhood_id"],
        street_id=base["street_id"], valid_from=date(2020, 1, 1),
        attrs={"anvendelse": "120", "areal": 140, "vaerelser": 5, "opfoerelsesaar": 1975},
        owner_kind="PRIVATE", lon=11.01, lat=56.51,
    )


def _rows(conn, address_id):
    return conn.execute(
        "SELECT count(*) FROM zone_a.property WHERE address_id = %s", (address_id,)
    ).fetchone()[0]


def _events(conn, address_id):
    return conn.execute(
        "SELECT payload->>'change' FROM zone_a.property_event WHERE address_id = %s ORDER BY seq",
        (address_id,),
    ).fetchall()


def test_first_version_is_created(conn, version):
    event = upsert_property(conn, version, recorded_at=JAN, trace_id="t")
    assert event["payload"]["change"] == "CREATED"
    assert event["payload"]["old_hash"] is None
    validate_event(event)
    assert _rows(conn, version.address_id) == 1


def test_identical_version_changes_nothing(conn, version):
    upsert_property(conn, version, recorded_at=JAN, trace_id="t")
    assert upsert_property(conn, version, recorded_at=MAR, trace_id="t") is None
    assert _rows(conn, version.address_id) == 1
    assert _events(conn, version.address_id) == [("CREATED",)]


def test_change_keeps_what_we_knew_before(conn, version):
    """The moat: we can always answer what we knew at an earlier time."""
    upsert_property(conn, version, recorded_at=JAN, trace_id="t")
    bigger = replace(version, valid_from=date(2026, 3, 1),
                     attrs={**version.attrs, "areal": 165})
    event = upsert_property(conn, bigger, recorded_at=MAR, trace_id="t")

    assert event["payload"]["change"] == "CHANGED"
    assert event["payload"]["fields"] == ["attrs"]
    assert _rows(conn, version.address_id) == 3

    def areal(valid_on, known_at=None):
        row = property_as_of(conn, version.address_id, valid_on=valid_on, known_at=known_at)
        return row and row["attrs"]["areal"]

    # Today's knowledge.
    assert areal(date(2025, 6, 1)) == 140
    assert areal(date(2026, 6, 1)) == 165
    # In February we did not yet know about the extension.
    feb = datetime(2026, 2, 1, tzinfo=UTC)
    assert areal(date(2026, 6, 1), known_at=feb) == 140
    # After the change was recorded, the old period is still answered correctly.
    assert areal(date(2025, 6, 1), known_at=JUN) == 140
    assert areal(date(2026, 6, 1), known_at=JUN) == 165
    # Before we had the address at all.
    assert areal(date(2026, 6, 1), known_at=datetime(2025, 1, 1, tzinfo=UTC)) is None
    assert areal(date(2019, 1, 1)) is None


def test_correction_on_the_same_date(conn, version):
    upsert_property(conn, version, recorded_at=JAN, trace_id="t")
    fixed = replace(version, attrs={**version.attrs, "vaerelser": 4})
    event = upsert_property(conn, fixed, recorded_at=MAR, trace_id="t")

    assert event["payload"]["change"] == "CORRECTED"
    assert _rows(conn, version.address_id) == 2
    now = property_as_of(conn, version.address_id, valid_on=date(2021, 1, 1))
    then = property_as_of(conn, version.address_id, valid_on=date(2021, 1, 1),
                          known_at=datetime(2026, 2, 1, tzinfo=UTC))
    assert now["attrs"]["vaerelser"] == 4
    assert then["attrs"]["vaerelser"] == 5


def test_older_version_is_refused(conn, version):
    upsert_property(conn, version, recorded_at=JAN, trace_id="t")
    older = replace(version, valid_from=date(2019, 1, 1), attrs={**version.attrs, "areal": 90})
    with pytest.raises(OutOfOrderVersion), conn.transaction():
        upsert_property(conn, older, recorded_at=MAR, trace_id="t")
    assert _rows(conn, version.address_id) == 1


def test_only_one_open_version_exists(conn, version):
    upsert_property(conn, version, recorded_at=JAN, trace_id="t")
    for month, areal in ((2, 150), (3, 160), (4, 170)):
        upsert_property(
            conn, replace(version, valid_from=date(2026, month, 1),
                          attrs={**version.attrs, "areal": areal}),
            recorded_at=datetime(2026, month, 5, tzinfo=UTC), trace_id="t",
        )
    open_versions = conn.execute(
        "SELECT count(*) FROM zone_a.property"
        " WHERE address_id = %s AND superseded_at IS NULL AND valid_to IS NULL",
        (version.address_id,),
    ).fetchone()[0]
    assert open_versions == 1
    assert [c for (c,) in _events(conn, version.address_id)] == \
        ["CREATED", "CHANGED", "CHANGED", "CHANGED"]
    # Current knowledge has no gaps and no overlaps.
    periods = conn.execute(
        "SELECT valid_from, valid_to FROM zone_a.property"
        " WHERE address_id = %s AND superseded_at IS NULL ORDER BY valid_from",
        (version.address_id,),
    ).fetchall()
    for (_, end), (start, _) in zip(periods, periods[1:], strict=False):
        assert end == start
    assert periods[-1][1] is None


def test_ownership_change_is_visible_in_the_event(conn, version):
    """Revocation of ownership verification hangs on this event (v5.1 §4.4)."""
    upsert_property(conn, version, recorded_at=JAN, trace_id="t")
    sold = replace(version, valid_from=date(2026, 5, 1), owner_kind="COMPANY",
                   owner_cvr="12345670")
    event = upsert_property(conn, sold, recorded_at=JUN, trace_id="t")
    assert set(event["payload"]["fields"]) == {"owner_kind", "owner_cvr"}


def test_ingest_role_has_the_rights_it_needs(conn, version):
    conn.execute("SET LOCAL ROLE ingest_role")
    upsert_property(conn, version, recorded_at=JAN, trace_id="t")
    upsert_property(conn, replace(version, valid_from=date(2026, 3, 1),
                                  attrs={**version.attrs, "areal": 165}),
                    recorded_at=MAR, trace_id="t")
    assert _rows(conn, version.address_id) == 3
