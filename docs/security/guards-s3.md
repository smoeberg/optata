# Guard-tests til S3 (specifikation, udkast)

**Placering:** `tests/guards/` · **Ejer:** DK-reviewer · **Må ikke AI-genereres.**
Disse tests er *specifikationen*. Koden skal bestå dem — ikke omvendt.

## B1 · `tests/guards/conftest.py`

```python
"""
Fælles fixtures til guard-tests.
Alle data er syntetiske (ADR-012). Seed er fast for reproducerbarhed.
"""
import pytest
from datetime import date, timedelta

SEED = 42

@pytest.fixture
def fx03_samboende(db):
    """To identiteter, samme household_key (DAR-adresse)."""
    hh = "addr-0a3f50a1"
    a = db.identity(provider="MITID_PRIVATE", household_key=hh)
    b = db.identity(provider="MITID_PRIVATE", household_key=hh)
    return a, b

@pytest.fixture
def fx04_udloebent_attest(db, order):
    """Attest udløbet i går, status stadig VALID — skal nedgraderes af job."""
    return db.verification(
        order_id=order.id,
        method="BANK_DOCUMENT",
        approved_amount=4_200_000,
        issued_at=date.today() - timedelta(days=100),
        expires_at=date.today() - timedelta(days=1),
        status="VALID",
    )

@pytest.fixture
def high_value_attest(db, order):
    """Over dual-control-grænsen."""
    return db.verification(order_id=order.id, approved_amount=12_000_000,
                           status="PENDING")

@pytest.fixture
def stepup_fresh(auth):
    return auth.step_up(age_seconds=60)

@pytest.fixture
def stepup_stale(auth):
    return auth.step_up(age_seconds=400)  # > 5 min
```

## B2 · `test_no_cpr_persisted.py`

```python
"""ADR-005: CPR må aldrig persisteres eller logges."""
import re
import pytest

CPR_PATTERN = re.compile(r"\b\d{6}-?\d{4}\b")

def test_cpr_not_in_identity_table(db, mitid_login_with_cpr):
    mitid_login_with_cpr(cpr="0102031234")  # syntetisk, ugyldigt
    rows = db.dump_table("identity")
    assert not CPR_PATTERN.search(str(rows)), "CPR fundet i identity"

def test_cpr_not_in_events(db, mitid_login_with_cpr):
    mitid_login_with_cpr(cpr="0102031234")
    events = db.dump_table("order_event") + db.dump_table("audit_log")
    assert not CPR_PATTERN.search(str(events)), "CPR fundet i event/audit"

def test_cpr_not_in_logs(log_capture, mitid_login_with_cpr):
    mitid_login_with_cpr(cpr="0102031234")
    assert not CPR_PATTERN.search(log_capture.text), "CPR fundet i logs"

def test_pseudonym_stable_across_logins(db, mitid_login_with_cpr):
    p1 = mitid_login_with_cpr(cpr="0102031234").pseudonym
    p2 = mitid_login_with_cpr(cpr="0102031234").pseudonym
    assert p1 == p2, "Samme person skal give samme pseudonym (dedup)"
```

## B3 · `test_vault_only_disclosure.py`

```python
"""ADR-004/007: Kun disclosure_service må læse vault."""
import pytest

VAULT_TABLES = ["identity_contact", "verification_evidence", "ownership_evidence"]

@pytest.mark.parametrize("role", ["app_role", "support_role", "agent_role", "insights_role"])
def test_other_roles_cannot_select_vault(db, role):
    for t in VAULT_TABLES:
        with pytest.raises(PermissionDenied):
            db.as_role(role).execute(f"SELECT * FROM {t} LIMIT 1")

def test_disclosure_can_select_vault(db):
    rows = db.as_role("disclosure_service").execute(
        "SELECT 1 FROM identity_contact LIMIT 1")
    assert rows is not None

def test_vault_access_emits_audit(db, disclosure):
    disclosure.read_contact(identity_id="syn-1", purpose="REVEAL", grant_id="g-1")
    ev = db.last_event("vault.accessed")
    assert ev.payload["service"] == "disclosure"
    assert ev.payload["grant_id"] == "g-1"

def test_support_payload_has_no_vault_fields(api, support_session):
    r = api.get("/internal/support/case/syn-1", session=support_session)
    forbidden = {"name", "email", "phone", "cpr", "document", "evidence_key"}
    assert not forbidden & set(r.json().keys())
```

## B4 · `test_stepup_freshness.py`

```python
"""ADR-008: Step-up skal være ≤5 minutter gammel."""
def test_fresh_stepup_allowed(api, stepup_fresh, verified_order):
    r = api.post(f"/orders/{verified_order.id}/verification",
                 headers={"X-Step-Up-Ref": stepup_fresh.ref})
    assert r.status_code in (200, 202)

def test_stale_stepup_rejected(api, stepup_stale, verified_order):
    r = api.post(f"/orders/{verified_order.id}/verification",
                 headers={"X-Step-Up-Ref": stepup_stale.ref})
    assert r.status_code == 403
    assert r.json()["code"] == "STEP_UP_REQUIRED"

def test_login_alone_is_not_stepup(api, mitid_session, verified_order):
    r = api.post(f"/orders/{verified_order.id}/verification", session=mitid_session)
    assert r.status_code == 403
    assert r.json()["code"] == "STEP_UP_REQUIRED"

def test_stepup_is_audited(db, api, stepup_fresh, verified_order):
    api.post(f"/orders/{verified_order.id}/verification",
             headers={"X-Step-Up-Ref": stepup_fresh.ref})
    ev = db.last_event("auth.step_up")
    assert ev.payload["assurance"] == "HIGH"
```

## B5 · `test_identity_merge_no_duplicate.py`

```python
"""ADR-006: Ordre opgraderes in-place — aldrig slet+genskab."""
def test_email_order_upgraded_in_place(db, api):
    o = api.post("/orders", json={"scope": "ADDRESS", "address_id": "addr-1",
                                  "area_id": "ZIP-2900", "criteria": {}}).json()
    before_id = o["order_id"]
    api.post(f"/orders/{before_id}/qualify", mitid=True)
    after = db.get_order(before_id)
    assert after.id == before_id, "Ordre-ID må ikke ændres"
    assert after.level == "QUALIFIED"
    assert db.count_orders(buyer=after.buyer_id) == 1, "Dublet opstået"

def test_link_has_causation(db, api):
    o = api.post("/orders", json={"scope": "AREA", "area_id": "ZIP-2900",
                                  "criteria": {}}).json()
    api.post(f"/orders/{o['order_id']}/qualify", mitid=True)
    ev = db.last_event("identity.linked")
    assert ev.causation_id is not None
    assert ev.payload["from_pseudonym"] != ev.payload["to_pseudonym"]

def test_historic_events_preserved(db, api):
    o = api.post("/orders", json={"scope": "AREA", "area_id": "ZIP-2900",
                                  "criteria": {}}).json()
    n_before = db.count_events(o["order_id"])
    api.post(f"/orders/{o['order_id']}/qualify", mitid=True)
    assert db.count_events(o["order_id"]) > n_before, "Historik må ikke slettes"
```

## B6 · `test_household_dedup.py`

```python
"""§2.3: Én aktiv ordre pr. husstand+scope. Samboende = co-buyer."""
def test_second_order_same_household_rejected(api, fx03_samboende):
    a, b = fx03_samboende
    api.post("/orders", session=a, json={"scope": "ADDRESS",
             "address_id": "addr-1", "area_id": "ZIP-2900", "criteria": {}})
    r = api.post("/orders", session=b, json={"scope": "ADDRESS",
                 "address_id": "addr-1", "area_id": "ZIP-2900", "criteria": {}})
    assert r.status_code == 409
    assert r.json()["code"] == "ORDER_ALREADY_ACTIVE"

def test_cobuyer_added_to_same_order(db, api, fx03_samboende):
    a, b = fx03_samboende
    o = api.post("/orders", session=a, json={"scope": "ADDRESS",
                 "address_id": "addr-1", "area_id": "ZIP-2900", "criteria": {}}).json()
    api.post(f"/orders/{o['order_id']}/parties", session=b)
    assert db.count_orders(household=a.household_key) == 1
    assert len(db.order_parties(o["order_id"])) == 2

def test_different_scope_allowed(api, fx03_samboende):
    a, _ = fx03_samboende
    api.post("/orders", session=a, json={"scope": "ADDRESS",
             "address_id": "addr-1", "area_id": "ZIP-2900", "criteria": {}})
    r = api.post("/orders", session=a, json={"scope": "AREA",
                 "area_id": "ZIP-2900", "criteria": {}})
    assert r.status_code == 201, "Andet scope skal være tilladt"
```

## B7 · `test_expiry_downgrade.py`

```python
"""ADR-006/§2.3: Udløben attest må ikke sælges som verificeret."""
from datetime import date

def test_expired_verification_downgrades(db, fx04_udloebent_attest, order):
    db.run_job("verification.expiry")
    assert db.get_verification(fx04_udloebent_attest.id).status == "EXPIRED"
    assert db.get_order(order.id).level == "QUALIFIED"

def test_expired_removed_from_agent_leads(db, api, agent_session,
                                          fx04_udloebent_attest, order):
    assert order.pseudonym in api.get("/agent/leads", session=agent_session).pseudonyms
    db.run_job("verification.expiry")
    assert order.pseudonym not in api.get("/agent/leads", session=agent_session).pseudonyms

def test_expiry_emits_event(db, fx04_udloebent_attest):
    db.run_job("verification.expiry")
    ev = db.last_event("verification.expired")
    assert ev.payload["new_level"] == "QUALIFIED"
    assert ev.payload["removed_from_lead_lists"] is True

def test_failed_job_freezes_lead_lists(db, api, agent_session, monkeypatch):
    monkeypatch.setattr(db, "run_job", lambda *a: (_ for _ in ()).throw(RuntimeError))
    db.mark_job_failed("verification.expiry")
    r = api.get("/agent/leads", session=agent_session)
    assert r.json() == [], "Lead-lister skal fryses ved fejlet expiry-job"
```

## B8 · `test_dual_control_and_attest_fields.py`

```python
"""Attest-review: dual control og minimal eksponering."""
def test_high_value_requires_second_reviewer(api, high_value_attest, staff_a, staff_b):
    r = api.post(f"/internal/verifications/{high_value_attest.id}/review",
                 session=staff_a, json={"decision": "APPROVE"})
    assert r.status_code == 409, "Én godkender må ikke være nok over 10 mio."
    r2 = api.post(f"/internal/verifications/{high_value_attest.id}/review",
                  session=staff_b, json={"decision": "APPROVE"})
    assert r2.status_code == 200

def test_same_reviewer_cannot_double_approve(api, high_value_attest, staff_a):
    api.post(f"/internal/verifications/{high_value_attest.id}/review",
             session=staff_a, json={"decision": "APPROVE"})
    r = api.post(f"/internal/verifications/{high_value_attest.id}/review",
                 session=staff_a, json={"decision": "APPROVE"})
    assert r.status_code == 409

def test_only_attest_fields_exposed(db, api, owner_session, verified_order):
    r = api.get(f"/owner/interest/{verified_order.address_id}", session=owner_session)
    allowed = {"pseudonym", "level", "badges", "budget_band", "verification_expires_at"}
    for item in r.json():
        assert set(item.keys()) <= allowed, f"Uventede felter: {set(item)-allowed}"

def test_document_never_in_public_payload(api, owner_session, verified_order):
    r = api.get(f"/owner/interest/{verified_order.address_id}", session=owner_session)
    assert "evidence_key" not in r.text
    assert "document" not in r.text
```

## B9 · Kørsel i CI

```yaml
# .github/workflows/ci.yml (uddrag)
guards:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: make dev-db          # syntetiske data, seed 42
    - run: pytest tests/guards/ -x -q --tb=short
      # -x: stop ved første fejl. Ingen continue-on-error. Ingen override.
```

---
