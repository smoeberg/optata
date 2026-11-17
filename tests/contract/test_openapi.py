"""CI gate 1 (contract first) and the schema part of gate 5 (zone leakage)."""

from pathlib import Path

import yaml

from apps.api.main import app

CONTRACT = yaml.safe_load(
    (Path(__file__).resolve().parents[2] / "contracts" / "openapi.yaml").read_text("utf-8")
)

# Objects that are open on purpose. Each needs a reason in the contract, and
# none may ever carry personal data.
OPEN_BY_DESIGN = {"QualityFlags", "Property.attrs"}


def _open_objects(schema, path):
    """Yield the path of every object schema that does not close itself."""
    if not isinstance(schema, dict):
        return
    kind = schema.get("type")
    is_object = kind == "object" or (isinstance(kind, list) and "object" in kind)
    if is_object and schema.get("additionalProperties") is not False and path not in OPEN_BY_DESIGN:
        yield path
    for name, child in schema.get("properties", {}).items():
        yield from _open_objects(child, f"{path}.{name}")
    if "items" in schema:
        yield from _open_objects(schema["items"], f"{path}[]")


def test_every_route_in_the_app_is_in_the_contract():
    for route in app.routes:
        methods = getattr(route, "methods", set()) - {"HEAD", "OPTIONS"}
        for method in methods:
            assert route.path in CONTRACT["paths"], f"{route.path} is not in openapi.yaml"
            assert method.lower() in CONTRACT["paths"][route.path], f"{method} {route.path}"


def test_every_public_path_in_the_contract_is_served():
    served = {route.path for route in app.routes}
    assert set(CONTRACT["paths"]) == served


def test_response_schemas_are_closed_at_every_depth():
    """additionalProperties: false is a security control: an undeclared field cannot leak."""
    found = []
    for name, schema in CONTRACT["components"]["schemas"].items():
        found.extend(_open_objects(schema, name))
    assert found == []


def test_there_is_no_email_session():
    """v5.1: login is MitID. Nothing is identified by e-mail."""
    assert "emailSession" not in CONTRACT["components"]["securitySchemes"]
    assert "email" not in yaml.safe_dump(CONTRACT["paths"]).lower()


def test_public_schemas_carry_no_personal_fields():
    text = yaml.safe_dump(CONTRACT["components"]["schemas"]).lower()
    for word in ("cpr", "full_name", "phone", "owner_cvr", "household", "pseudonym"):
        assert word not in text, word
