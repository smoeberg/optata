import copy

import pytest

from core.events import EventValidationError, upcast, validate_event


@pytest.fixture
def created(dataset):
    return copy.deepcopy(dataset["order_events"][0]["envelope"])


def test_valid_event_passes(created):
    validate_event(created)


def test_unknown_top_level_field_is_rejected(created):
    created["debug"] = "x"
    with pytest.raises(EventValidationError):
        validate_event(created)


def test_unknown_payload_field_is_rejected(created):
    created["payload"]["budget_exact"] = 4_200_000
    with pytest.raises(EventValidationError):
        validate_event(created)


def test_curios_level_no_longer_exists(created):
    created["payload"]["level"] = "CURIOS"
    with pytest.raises(EventValidationError):
        validate_event(created)


@pytest.mark.parametrize("key", ["cpr", "name", "email", "phone", "document", "message_body"])
def test_direct_identifier_in_payload_is_rejected(key):
    event = {
        "event_id": "e1", "type": "area.viewed", "schema_version": "1.0.0",
        "occurred_at": "2026-01-01T00:00:00+00:00", "recorded_at": "2026-01-01T00:00:00+00:00",
        "actor": {"kind": "SYSTEM"}, "zone": "A", "aggregate": {"kind": "PROPERTY", "id": "x"},
        "trace_id": "t", "payload": {key: "value"},
    }
    with pytest.raises(EventValidationError):
        validate_event(event)


def test_nested_identifier_is_rejected_too():
    event = {
        "event_id": "e1", "type": "area.viewed", "schema_version": "1.0.0",
        "occurred_at": "2026-01-01T00:00:00+00:00", "recorded_at": "2026-01-01T00:00:00+00:00",
        "actor": {"kind": "SYSTEM"}, "zone": "A", "aggregate": {"kind": "PROPERTY", "id": "x"},
        "trace_id": "t", "payload": {"contact": [{"Email": "a@example.invalid"}]},
    }
    with pytest.raises(EventValidationError, match="payload.contact"):
        validate_event(event)


def test_event_without_specific_schema_uses_the_envelope():
    validate_event({
        "event_id": "e1", "type": "area.viewed", "schema_version": "1.0.0",
        "occurred_at": "2026-01-01T00:00:00+00:00", "recorded_at": "2026-01-01T00:00:00+00:00",
        "actor": {"kind": "SYSTEM"}, "zone": "A", "aggregate": {"kind": "PROPERTY", "id": "x"},
        "trace_id": "t", "payload": {"area_id": "SYN-ZIP-0001"},
    })


def test_upcast_brings_old_event_to_current_version(created):
    old = copy.deepcopy(created)
    old["schema_version"] = "1.0.0"
    del old["payload"]["household_key"]
    snapshot = copy.deepcopy(old)

    new = upcast(old)

    assert new["schema_version"] == "1.1.0"
    assert new["payload"]["household_key"] is None
    assert old == snapshot, "the stored event must not be modified"
    validate_event(new)


def test_upcast_leaves_current_events_alone(created):
    assert upcast(created) == created
