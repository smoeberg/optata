import json

import pytest

from core.events import validate_event
from tools.fixtures import BOLIGKODER, generate
from tools.fixtures.generate import FX01_BFE, FX02_BFE, ZIP_ID


def test_same_seed_gives_identical_output():
    a = generate(seed=7, dwellings=200, orders=40)
    b = generate(seed=7, dwellings=200, orders=40)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_different_seed_gives_different_output():
    a = generate(seed=7, dwellings=200, orders=40)
    b = generate(seed=8, dwellings=200, orders=40)
    assert a["properties"][0]["address_id"] != b["properties"][0]["address_id"]


def test_fx01_one_bfe_has_forty_dwellings(dataset):
    """BFE -> address is one-to-many. Counting BFE would count 1 instead of 40."""
    units = [p for p in dataset["properties"] if p["bfe"] == FX01_BFE]
    assert len(units) == 40
    assert len({p["address_id"] for p in units}) == 40
    assert {p["owner_kind"] for p in units} == {"ANDELSFORENING"}


def test_fx02_company_owned_rental(dataset):
    units = [p for p in dataset["properties"] if p["bfe"] == FX02_BFE]
    assert len(units) == 12
    assert {p["owner_kind"] for p in units} == {"COMPANY"}
    assert len({p["owner_cvr"] for p in units}) == 1


def test_dwelling_count_excludes_non_residential(dataset):
    zip_area = next(a for a in dataset["areas"] if a["area_id"] == ZIP_ID)
    non_residential = [p for p in dataset["properties"]
                       if p["attrs"]["anvendelse"] not in BOLIGKODER]
    assert non_residential
    assert zip_area["dwelling_count"] == 300
    assert len(dataset["properties"]) == 300 + len(non_residential)


def test_levels_add_up(dataset):
    """Streets sum to their neighbourhood, neighbourhoods to the postal area."""
    by_id = {a["area_id"]: a for a in dataset["areas"]}
    for level, parent_level in (("STREET", "NEIGHBOURHOOD"), ("NEIGHBOURHOOD", "ZIP"),
                                ("ZIP", "MUNICIPALITY")):
        totals: dict[str, int] = {}
        for area in dataset["areas"]:
            if area["level"] == level:
                totals[area["parent_id"]] = totals.get(area["parent_id"], 0) + \
                    area["dwelling_count"]
        for parent_id, total in totals.items():
            assert by_id[parent_id]["level"] == parent_level
            assert by_id[parent_id]["dwelling_count"] == total


def test_verified_ratio_is_respected(dataset):
    verified = [o for o in dataset["orders"] if o["level"] == "VERIFIED"]
    assert len(verified) == 15
    assert {o["level"] for o in dataset["orders"]} == {"QUALIFIED", "VERIFIED"}


def test_one_order_per_household(dataset):
    keys = [(o["household_key"], o["scope"], o["address_id"] or o["area_id"])
            for o in dataset["orders"]]
    assert len(keys) == len(set(keys))


def test_every_event_satisfies_its_contract(dataset):
    assert len(dataset["order_events"]) == 60 + 15
    for record in dataset["order_events"]:
        validate_event(record["envelope"])


def test_too_few_dwellings_is_rejected():
    with pytest.raises(ValueError):
        generate(dwellings=50)
