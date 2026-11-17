"""The public API, exercised against a real database and checked against the contract."""

from pathlib import Path

import psycopg
import pytest
import yaml
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator

from apps.api.db import public_connection
from apps.api.main import app
from tools.fixtures.generate import FX01_BFE, MUNICIPALITY_ID, ZIP_ID

CONTRACT = yaml.safe_load(
    (Path(__file__).resolve().parents[2] / "contracts" / "openapi.yaml").read_text("utf-8")
)


def conforms(payload, schema_name, is_list=False):
    """Validate a response body against a schema in the contract."""
    ref = {"$ref": f"#/components/schemas/{schema_name}"}
    schema = {"components": CONTRACT["components"],
              **({"type": "array", "items": ref} if is_list else ref)}
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert not errors, errors[0].message


@pytest.fixture
def client(db_url, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", db_url)
    return TestClient(app)


# ---------------------------------------------------------------- health and tracing


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    conforms(response.json(), "Health")


def test_every_response_carries_a_trace_id(client):
    a = client.get("/health").headers["X-Trace-Id"]
    b = client.get("/health").headers["X-Trace-Id"]
    assert a and b and a != b


# ---------------------------------------------------------------- areas


def test_areas_without_query_lists_widest_first(client):
    body = client.get("/areas").json()
    conforms(body, "AreaSummary", is_list=True)
    assert body[0]["area_id"] == MUNICIPALITY_ID
    assert body[1]["area_id"] == ZIP_ID
    assert len(body) <= 20


def test_areas_search_by_name(client):
    body = client.get("/areas", params={"q": "testvej 3"}).json()
    assert [a["name"] for a in body] == ["Testvej 3"]


def test_areas_filter_by_level(client):
    body = client.get("/areas", params={"level": "NEIGHBOURHOOD"}).json()
    assert len(body) == 4
    assert {a["level"] for a in body} == {"NEIGHBOURHOOD"}


def test_search_wildcards_are_taken_literally(client):
    assert client.get("/areas", params={"q": "%"}).json() == []
    assert client.get("/areas", params={"q": "_"}).json() == []


@pytest.mark.parametrize("params", [{"level": "COUNTRY"}, {"q": "x" * 81}])
def test_invalid_query_is_rejected(client, params):
    assert client.get("/areas", params=params).status_code == 422


# ---------------------------------------------------------------- profile


def test_profile_conforms_to_the_contract_on_every_level(client, dataset):
    seen = set()
    for area in dataset["areas"]:
        if area["level"] in seen:
            continue
        seen.add(area["level"])
        response = client.get(f"/areas/{area['area_id']}/profile")
        assert response.status_code == 200
        conforms(response.json(), "AreaProfile")
    assert seen == {"MUNICIPALITY", "ZIP", "NEIGHBOURHOOD", "STREET"}


def test_profile_facts_for_the_postal_area(client, dataset):
    body = client.get(f"/areas/{ZIP_ID}/profile").json()
    fakta = body["layers"]["fakta"]
    assert fakta["dwelling_count"] == 300
    assert fakta["non_residential_count"] == 3
    assert sum(c["count"] for c in fakta["by_usage"]) == 300
    owners = {c["key"]: c["count"] for c in fakta["by_owner_kind"]}
    assert owners["ANDELSFORENING"] == 40 and owners["COMPANY"] == 12
    assert fakta["areal"]["p25"] <= fakta["areal"]["median"] <= fakta["areal"]["p75"]
    assert [a["area_id"] for a in body["path"]] == [MUNICIPALITY_ID, ZIP_ID]
    assert len(body["children"]) == 4


def test_layers_without_data_are_null_not_zero(client):
    """S1-11: an empty demand layer must read as 'no data yet', never as zero buyers."""
    body = client.get(f"/areas/{ZIP_ID}/profile").json()
    assert body["layers"]["efterspoergsel"] is None
    assert body["layers"]["hverdag"] is None
    assert body["meta"]["layer_status"] == {
        "fakta": "OK", "bevaegelse": "NO_DATA_YET", "hverdag": "NO_DATA_YET",
        "efterspoergsel": "NO_DATA_YET",
    }


def test_synthetic_data_is_labelled(client):
    """Generated figures must never be mistaken for real ones."""
    assert client.get(f"/areas/{ZIP_ID}/profile").json()["meta"]["synthetic"] is True


def test_street_profile_shows_the_cooperative_as_forty_dwellings(client, dataset):
    street = next(p["street_id"] for p in dataset["properties"] if p["bfe"] == FX01_BFE)
    body = client.get(f"/areas/{street}/profile").json()
    owners = {c["key"]: c["count"] for c in body["layers"]["fakta"]["by_owner_kind"]}
    assert owners["ANDELSFORENING"] == 40
    assert [a["level"] for a in body["path"]] == ["MUNICIPALITY", "ZIP", "NEIGHBOURHOOD", "STREET"]
    assert body["children"] == []


def test_unknown_area_is_404_in_contract_shape(client):
    response = client.get("/areas/NOPE/profile")
    assert response.status_code == 404
    conforms(response.json(), "Error")
    assert response.json()["trace_id"] == response.headers["X-Trace-Id"]


# ---------------------------------------------------------------- property


def test_property_lookup(client, dataset):
    prop = dataset["properties"][100]
    response = client.get(f"/properties/{prop['address_id']}")
    assert response.status_code == 200
    body = response.json()
    conforms(body, "Property")
    assert body["bfe"] == prop["bfe"]
    assert body["attrs"] == prop["attrs"]
    assert "max-age" in response.headers["Cache-Control"]


def test_owner_cvr_is_not_exposed(client, dataset):
    company = next(p for p in dataset["properties"] if p["owner_cvr"])
    body = client.get(f"/properties/{company['address_id']}").json()
    assert body["owner_kind"] == "COMPANY"
    assert company["owner_cvr"] not in str(body)


@pytest.mark.parametrize("address_id", [
    "00000000-0000-4000-8000-000000000000", "not-a-uuid", "1; DROP TABLE zone_a.property",
])
def test_unknown_and_malformed_ids_give_the_same_404(client, address_id):
    response = client.get(f"/properties/{address_id}")
    assert response.status_code == 404
    assert response.json()["message"] == "Unknown address"
    conforms(response.json(), "Error")


def test_lookup_returns_the_current_version_only(client, db_url, dataset):
    """A superseded or closed version must never be served."""
    prop = dataset["properties"][100]
    body = client.get(f"/properties/{prop['address_id']}").json()
    with psycopg.connect(db_url) as conn:
        versions = conn.execute(
            "SELECT count(*) FROM zone_a.property WHERE address_id = %s"
            " AND superseded_at IS NULL AND valid_to IS NULL", (prop["address_id"],)
        ).fetchone()[0]
    assert versions == 1
    assert body["valid_from"] == prop["valid_from"]


# ---------------------------------------------------------------- the role behind it


def test_public_requests_run_as_public_reader_and_read_only(db_url, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", db_url)
    connection = public_connection()
    conn = next(connection)
    try:
        assert conn.execute("SELECT current_user").fetchone()[0] == "public_reader"
        with pytest.raises(psycopg.errors.InsufficientPrivilege), conn.transaction():
            conn.execute("SELECT 1 FROM zone_b.orders LIMIT 1")
        with pytest.raises(psycopg.errors.InsufficientPrivilege), conn.transaction():
            conn.execute("SELECT 1 FROM zone_b.area_density LIMIT 1")
        with pytest.raises(psycopg.errors.ReadOnlySqlTransaction), conn.transaction():
            conn.execute("CREATE TEMP TABLE scratch (x int)")
    finally:
        connection.close()


def test_missing_database_url_fails_loudly(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        next(public_connection())
