# Runbooks

One file per job or incident type. A runbook says what triggers it, how to
confirm the problem, what to do, and who to tell.

None are written yet. The list is the index from bilag 14, adjusted to v5.1.

| Runbook | Trigger | Priority |
|---|---|---|
| `vault-anomaly` | Vault read by anything other than `disclosure_service` | P1 |
| `zone-leak` | Zone B field in a public payload | P1, roll back |
| `ingestion-failed` | Source run failed or quarantine spike | P2 after 24 h |
| `expiry-failed` | Expired attestations still visible to owners or agents | P2, freeze lists |
| `retention-failed` | Deletion job failed | P2 |
| `redaction-bypass` | Reported circumvention in relay | P2 |
| `dwelling-count-jump` | Denominator changed more than 2 % between runs | Freeze density KPI |
| `mailbox-delivery-failed` | Opt-in notification not delivered to the digital mailbox | P3 |
| `dso-breach` | Receivables older than 45 days | P3 |
