import uuid
from datetime import UTC, date, datetime

import pytest

from core.registry import PropertyVersion
from workers.ingestion import Issue, RawRecord, run

T1 = datetime(2026, 1, 10, tzinfo=UTC)
T2 = datetime(2026, 2, 10, tzinfo=UTC)


class ListAdapter:
    """A source that serves a fixed list. Stands in for DAR/BBR until access exists."""

    source = "TEST"

    def __init__(self, records, fail_after=None):
        self.records = records
        self.fail_after = fail_after

    def fetch(self, since):
        served = 0
        for record in self.records:
            if since is not None and record.cursor <= since:
                continue
            if self.fail_after is not None and served == self.fail_after:
                raise ConnectionError("source went away")
            served += 1
            yield record

    def normalize(self, raw):
        data = dict(raw.data)
        data["valid_from"] = date.fromisoformat(data["valid_from"])
        return PropertyVersion(**data)

    def validate(self, version):
        areal = version.attrs.get("areal", 0)
        if not 0 < areal < 2000:
            return [Issue("areal", "OUT_OF_RANGE", f"areal {areal} is outside 1-1999")]
        return []


@pytest.fixture
def records(dataset):
    base = dataset["properties"][100]

    def make(i, areal=120, **extra):
        data = {
            "address_id": str(uuid.uuid5(uuid.NAMESPACE_OID, f"ingest-{i}")),
            "bfe": f"SYN-BFE-ING-{i}", "municipality_id": base["municipality_id"],
            "zip_id": base["zip_id"], "neighbourhood_id": base["neighbourhood_id"],
            "street_id": base["street_id"], "valid_from": "2020-01-01",
            "attrs": {"anvendelse": "120", "areal": areal, "vaerelser": 4},
            "owner_kind": "PRIVATE", **extra,
        }
        return RawRecord(natural_key=data["address_id"], cursor=f"{i:06d}", data=data)

    return [make(i) for i in range(1, 6)], make


def _count(conn, table, where="true"):
    return conn.execute(f"SELECT count(*) FROM zone_a.{table} WHERE {where}").fetchone()[0]


def test_run_applies_every_record(conn, records):
    rows, _ = records
    result = run(conn, ListAdapter(rows), recorded_at=T1, run_id="r1", batch_size=2)
    assert (result.fetched, result.changed, result.unchanged, result.quarantined) == (5, 5, 0, 0)
    assert result.checkpoint == "000005"
    assert _count(conn, "property", "bfe LIKE 'SYN-BFE-ING-%'") == 5


def test_second_run_fetches_nothing(conn, records):
    rows, _ = records
    run(conn, ListAdapter(rows), recorded_at=T1, run_id="r1")
    result = run(conn, ListAdapter(rows), recorded_at=T2, run_id="r2")
    assert result.fetched == 0


def test_replaying_the_same_records_creates_no_duplicates(conn, records):
    rows, _ = records
    run(conn, ListAdapter(rows), recorded_at=T1, run_id="r1")
    events = _count(conn, "property_event")
    conn.execute("DELETE FROM zone_a.ingestion_checkpoint WHERE source = 'TEST'")

    result = run(conn, ListAdapter(rows), recorded_at=T2, run_id="r2")

    assert (result.fetched, result.changed, result.unchanged) == (5, 0, 5)
    assert _count(conn, "property", "bfe LIKE 'SYN-BFE-ING-%'") == 5
    assert _count(conn, "property_event") == events


def test_invalid_record_is_quarantined_not_dropped(conn, records):
    rows, make = records
    bad = make(3, areal=-10)
    result = run(conn, ListAdapter([rows[0], rows[1], bad, rows[3]]), recorded_at=T1, run_id="r1")

    assert (result.fetched, result.changed, result.quarantined) == (4, 3, 1)
    assert _count(conn, "property", f"address_id = '{bad.natural_key}'") == 0
    issues = conn.execute(
        "SELECT issues FROM zone_a.ingestion_quarantine WHERE natural_key = %s",
        (bad.natural_key,),
    ).fetchone()[0]
    assert issues[0]["code"] == "OUT_OF_RANGE"


def test_record_that_cannot_be_parsed_is_quarantined(conn, records):
    rows, make = records
    broken = make(2, valid_from="not-a-date")
    result = run(conn, ListAdapter([rows[0], broken]), recorded_at=T1, run_id="r1")
    assert (result.changed, result.quarantined) == (1, 1)
    code = conn.execute(
        "SELECT issues->0->>'code' FROM zone_a.ingestion_quarantine WHERE natural_key = %s",
        (broken.natural_key,),
    ).fetchone()[0]
    assert code == "NORMALIZE_FAILED"


def test_quarantine_is_idempotent(conn, records):
    _, make = records
    bad = make(1, areal=5000)
    run(conn, ListAdapter([bad]), recorded_at=T1, run_id="r1")
    conn.execute("DELETE FROM zone_a.ingestion_checkpoint WHERE source = 'TEST'")
    run(conn, ListAdapter([bad]), recorded_at=T2, run_id="r2")
    assert _count(conn, "ingestion_quarantine", f"natural_key = '{bad.natural_key}'") == 1


def test_out_of_order_version_is_quarantined(conn, records):
    rows, make = records
    older = make(1, areal=90, valid_from="2019-01-01")
    older = RawRecord(older.natural_key, "000009", older.data)
    result = run(conn, ListAdapter([rows[0], older]), recorded_at=T1, run_id="r1")
    assert (result.changed, result.quarantined) == (1, 1)


def test_interrupted_run_resumes_from_the_last_committed_batch(conn, records):
    rows, _ = records
    with pytest.raises(ConnectionError):
        run(conn, ListAdapter(rows, fail_after=3), recorded_at=T1, run_id="r1", batch_size=2)
    # Batch one (two records) committed. The third record was fetched but its
    # batch never completed, so it is not there and the checkpoint has not moved past it.
    assert _count(conn, "property", "bfe LIKE 'SYN-BFE-ING-%'") == 2
    checkpoint = conn.execute(
        "SELECT cursor FROM zone_a.ingestion_checkpoint WHERE source = 'TEST'"
    ).fetchone()[0]
    assert checkpoint == "000002"

    result = run(conn, ListAdapter(rows), recorded_at=T2, run_id="r2", batch_size=2)

    assert (result.fetched, result.changed) == (3, 3)
    assert _count(conn, "property", "bfe LIKE 'SYN-BFE-ING-%'") == 5


def test_runner_works_with_ingest_role_only(conn, records):
    rows, make = records
    conn.execute("SET LOCAL ROLE ingest_role")
    result = run(conn, ListAdapter([*rows, make(6, areal=0)]), recorded_at=T1, run_id="r1")
    assert (result.changed, result.quarantined) == (5, 1)
