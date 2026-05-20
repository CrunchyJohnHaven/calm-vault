# Calm Witness — Commerce Compliance Receipts v0 (S205)

**Status:** Draft · Summit S205 · 2026-05-20
**Scope:** Compliance receipt generation for ZKAC commerce transactions that cross configurable reporting thresholds. Selective compliance — minimum necessary disclosure, maximum regulatory defensibility.

---

## Threshold Triggers

Threshold evaluation runs at transaction finalization, before settlement confirmation is returned to participants.

**Configurable fields per jurisdiction profile:**

| Parameter | Type | Description |
|---|---|---|
| `threshold_amount` | uint128 (base units) | Transaction value above which a receipt is mandatory |
| `threshold_currency` | string (ISO 4217 / asset ID) | Denomination for threshold comparison |
| `aggregation_window` | duration | Rolling window for cumulative threshold evaluation |
| `counterparty_class_filter` | string[] | Restrict trigger to specific counterparty classifications |
| `jurisdiction_tag` | string (ISO 3166-1 / custom) | Jurisdiction whose rules govern this profile |

Threshold profiles are stored in the jurisdiction registry (S192). Each ZKAC node loads the active profile for the originating jurisdiction at transaction time. If a transaction touches multiple jurisdictions (e.g., cross-border settlement), the most restrictive threshold applies. Threshold config changes take effect at the next epoch boundary; retroactive application is disallowed.

Cumulative aggregation uses a sliding window keyed by `(principal_pseudonym, counterparty_class, jurisdiction_tag)`. Windowed totals are maintained in a side-chain accumulator; they do not leak transaction-level amounts to the accumulator's operator.

---

## Receipt Schema

A compliance receipt is a structured, signed data object. It contains no identity material beyond what the applicable regulation explicitly requires. The zero-knowledge layer ensures that counterparty identity is replaced by a verified classification claim.

```
ComplianceReceipt {
  receipt_id:          UUID v4
  tx_ref:              bytes32           // opaque tx fingerprint, not reversible to tx content
  timestamp_utc:       ISO 8601
  jurisdiction_tag:    string            // from jurisdiction registry (S192)
  transaction_class:   enum              // GOODS, SERVICES, FINANCIAL_INSTRUMENT, DIGITAL_ASSET, OTHER
  counterparty_class:  enum              // INDIVIDUAL, BUSINESS, GOVERNMENT, UNCLASSIFIED
  kyc_tier_summary:    enum              // TIER_0 (unverified), TIER_1 (basic), TIER_2 (enhanced), TIER_3 (full)
  threshold_triggered: string            // label of the threshold profile that fired
  amount_band:         enum              // BAND_1 (<10k), BAND_2 (10k–100k), BAND_3 (100k–1M), BAND_4 (>1M)
  sanctions_clear:     bool              // result of sanctions screen at tx time (S171, S216)
  sanctions_screen_ref: UUID             // pointer to sanctions check log entry
  obligations_ref:     UUID              // pointer to active E66 obligations contract snapshot
  receipt_version:     "S205-v0"
  issuer_sig:          bytes             // ZKAC node signature over canonical receipt bytes
}
```

`amount_band` is used in place of exact amounts where regulation permits banded reporting. Jurisdictions that require exact amounts must set `exact_amount_reporting: true` in their profile; in that case the field `exact_amount` is appended and the amount_band field is omitted.

No name, address, account number, or biometric identifier appears in a receipt. KYC-tier-summary attests that a counterparty has completed a specific verification tier without exposing the verification data itself.

---

## Composition with Obligations

Compliance receipts are bound to the principal's active E66 obligations contract at the time of transaction. The `obligations_ref` field holds a content-addressed pointer to the obligations snapshot.

Obligations contract interaction:

1. At threshold trigger, the ZKAC node queries E66 for the current obligations snapshot hash.
2. The snapshot hash is embedded in the receipt before signing.
3. If the obligations contract is in a suspended or breached state, receipt generation is blocked and the transaction is held pending resolution.
4. Receipts produced under a specific obligations version remain valid even if the contract is subsequently amended; the snapshot pointer provides the interpretive context.

E66 may impose additional receipt fields as contract terms (e.g., a specific tax-category code required by a jurisdiction agreement). Those fields are appended in an `e66_extensions` map within the receipt object and are validated against the contract schema at generation time.

---

## Retention

Retention periods are jurisdiction-specific and encoded in the jurisdiction profile.

Default retention schedule (absent jurisdiction override):

- **Standard receipts:** 7 years from transaction date
- **Receipts tied to disputed transactions:** extended to resolution + 2 years
- **Sanctions-triggered receipts:** 10 years minimum, flagged for regulatory hold

Receipts are stored encrypted at rest. The encryption key is derived from the principal's vault key; the ZKAC node retains no plaintext copy after delivery. The node retains a content-addressed hash of each receipt for audit-query responses.

At retention expiry, receipts are cryptographically shredded (key deletion). The hash entry is tombstoned with a deletion timestamp but not removed, to support audit-completeness proofs.

---

## Principal Audit Interface

The principal may query their own receipt store through a permissioned API. No third party — including the ZKAC node operator — can pull receipt content without a signed principal authorization or a valid legal process instrument.

**Query operations:**

| Method | Description |
|---|---|
| `list_receipts(date_range, jurisdiction_tag?)` | Returns receipt_id list and metadata stubs |
| `fetch_receipt(receipt_id)` | Returns full receipt object, decrypted with principal key |
| `verify_receipt(receipt_id)` | Re-derives and checks issuer signature; confirms hash integrity |
| `export_receipts(date_range, format)` | Produces a signed export bundle (JSON-L or CSV) for regulatory submission |
| `generate_audit_proof(receipt_id)` | Returns a zero-knowledge proof that the receipt exists and was validly issued, without revealing content |

`generate_audit_proof` is used to respond to regulatory inquiries that require proof of compliance without disclosing counterparty class or transaction class beyond what was already reported. This keeps selective disclosure operative even in audit contexts.

---

## Sanctions Integration

Sanctions screening runs synchronously at threshold trigger, before receipt generation. Two list sources:

- **S171 (primary sanctions list):** OFAC SDN-equivalent, updated on a configurable polling interval (default 4h).
- **S216 (secondary/jurisdiction-specific list):** jurisdiction-level additions, layered on top of S171.

Screening uses a privacy-preserving matching protocol: the counterparty's KYC-tier credential is checked against a bloom filter representation of the sanctions list. The counterparty's identity is not transmitted to the screening service. If the bloom filter produces a candidate match, the ZKAC node escalates to a supervised resolution flow — the transaction is suspended and the principal is notified.

Receipt field `sanctions_clear: true` means the counterparty's credential passed screening against both S171 and S216 at transaction time. The `sanctions_screen_ref` points to the screening log entry, which records the list versions used and the timestamp. The log entry is stored separately from the receipt, also encrypted, with the same retention rules.

Sanctions list updates during a transaction's aggregation window do not retroactively invalidate issued receipts; they apply to subsequent transactions.

---

## Cross-References

| Reference | Role |
|---|---|
| E66 | Obligations contract; provides jurisdictional compliance terms and extension fields |
| S171 | Primary sanctions list integration and screening protocol |
| S192 | Jurisdiction registry; authoritative source for threshold profiles and jurisdiction tags |
| S216 | Secondary/jurisdiction-specific sanctions list; layered screen |

---

*Calm 2026-05-20*
