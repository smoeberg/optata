"""CI gate 1 (contract first) and the schema part of gate 5 (zone leakage)."""

from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from apps.api.main import app

CONTRACT = yaml.safe_load(
    (Path(__file__).resolve().parents[2] / "contracts" / "openapi.yaml").read_text("utf-8")
)

# Schemas that are open on purpose. Each needs a reason in the contract.
OPEN_BY_DESIGN = {"QualityFlags"}


def test_every_route_in_the_app_is_in_the_contract():
    for route in app.routes:
        methods = getattr(route, "methods", set()) - {"HEAD", "OPTIONS"}
        for method in methods:
            assert route.path in CONTRACT["paths"], f"{route.path} is not in openapi.yaml"
            assert method.lower() in CONTRACT["paths"][route.path], f"{method} {route.path}"


def test_response_schemas_are_closed():
    """additionalProperties: false is a security control: an undeclared field cannot leak."""
    for name, schema in CONTRACT["components"]["schemas"].items():
        if schema.get("type") == "object" and name not in OPEN_BY_DESIGN:
            assert schema.get("additionalProperties") is False, name


def test_there_is_no_email_session():
    """v5.1: login is MitID. Nothing is identified by e-mail."""
    assert "emailSession" not in CONTRACT["components"]["securitySchemes"]
    assert "email" not in yaml.safe_dump(CONTRACT["paths"]).lower()


def test_health_matches_the_contract():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    schema = CONTRACT["components"]["schemas"]["Health"]
    assert set(response.json()) == set(schema["required"])
    assert response.json()["status"] in schema["properties"]["status"]["enum"]
