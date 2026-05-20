# CO-17 — Stripe Live-Mode Verification

**Acceptance:** Recurring automated check that the operator's Stripe account remains in Live mode (not Test mode). The check probes Stripe API every 6 hours and alerts the principal if the mode deviates from Live or becomes indeterminate.

## Post-2026-05-17 Incident Lesson

On 2026-05-17, the operator's Stripe account remained in Test mode longer than intended, causing payment transactions to be simulated rather than collected. This gate prevents a recurrence by enforcing continuous visibility into the operator's Stripe mode flag and alerting on drift with fail-closed semantics: if the mode cannot be determined, the alert fires immediately.

**What this prevents:** undetected Test-mode transactions, loss of revenue, customer confusion about payment completion, audit gaps in bookkeeping.

## Detection Logic

The probe reads the operator's Stripe secret key (from env `STRIPE_SECRET_KEY` or CLI argument) and makes two independent checks:

1. **Key prefix inspection:** Stripe secret keys are predictable in format.
   - `sk_test_*` → Test mode
   - `sk_live_*` → Live mode
   - Unset or malformed → UNKNOWN

2. **API livemode field:** A no-cost probe to `GET /v1/charges?limit=1` returns a JSON object with a `livemode` boolean field. This is the authoritative signal.
   - `livemode: true` → Live
   - `livemode: false` → Test
   - Network error or parse failure → UNKNOWN

**Result:** If key prefix and API livemode agree, the probe reports that mode. If they disagree, the probe reports UNKNOWN (fail-closed). If the API is unreachable after one retry, mode=UNKNOWN.

## Schedule & Chain Record

- **Default cadence:** Every 6 hours (cron `0 */6 * * *` or explicit Calm Operations loop invocation).
- **Chain record schema:** `stripe.mode.probe`
  - `timestamp`: ISO8601 UTC
  - `mode`: "live" | "test" | "unknown"
  - `key_kind`: "sk_live" | "sk_test" | "unset" | "other"
  - `livemode_field`: boolean | null (null if API unreachable)
  - `probed_at`: ISO8601 UTC
  - `fingerprint`: SHA-256 hex digest of the first 16 characters of the key after the `sk_` prefix. **Never includes the full secret key.**

## Alert Thresholds

1. **Mode != live** (any single probe result where mode ∈ {test, unknown}): **Page principal immediately.**
2. **UNKNOWN for ≥ 3 consecutive probes:** **Page principal.** This indicates a persistent API or configuration issue.
3. **Test mode detected:** Include the fingerprint and the timestamp in the alert. Do not include any part of the secret key.

## Refusal Floor

- **No secret key value** shall appear in any log, alert, or chain record. Logging is limited to:
  - The key kind prefix (e.g., "sk_test" or "sk_live").
  - The SHA-256 fingerprint of the first 16 characters after the prefix.
  - The mode and timestamp.
- **Fail-closed:** If Stripe API is unreachable or the secret key is unset, the probe returns mode=UNKNOWN and does not guess or assume Live.
- **No account enumeration:** The probe uses only a single read-only API call to `GET /v1/charges?limit=1` and does not enumerate balances, customers, payment intents, or other sensitive data.

## Cross-Links

- **CO-18** — Payment Link Health. Depends on CO-17 passing (assumes operator is in Live mode before probing Payment Links).
- **CO-20** — Bookkeeping Chain. Depends on CO-17 passing (assumes recorded transactions are real Stripe Live-mode transactions).

## Implementation References

- Probe implementation: `/Users/johnbradley/CredexAI/calm_operations/stripe_mode_probe.py`
- Gate (acceptance tests): `/Users/johnbradley/CredexAI/scripts/co_17_calm_operations_stripe_live_mode_gate.py`
