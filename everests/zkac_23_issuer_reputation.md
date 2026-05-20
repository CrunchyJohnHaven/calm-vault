# ZKAC Everest 23 — Issuer Reputation Primitive

**Phase XVIII · Issuer Infrastructure**  
**Prereq:** ZKAC Everest 11 (Issuer governance), 19 (Audit log), 21 (Slashing protocol)  
**Effort:** L  
**Status:** v0 · 2026-05-20

**Acceptance:** A public reputation score for each issuer derived from audit-result audits, slash-event history, endorsements from peer issuers, age in ecosystem, and revocation rate. Score published as a signed manifest per issuer, refreshed quarterly. Verifiers consume manifests privacy-preservingly without leaking which credential they're verifying.

---

## Why Issuer Reputation Is Critical

Verifiers need a cryptographically-backed reputation signal to weight issuer credentials. This primitive aggregates evidence (audit results, slash events, endorsements, age, revocation rate), resists gaming, scales verification via privacy-preserving queries, feeds the trust graph (E71-75), and enforces tier thresholds (E20).

---

## Score Components

### 1. Audit-Results Weight (40% of base score)

**Source:** External cryptographic audits (Everest 11, Step 6; recurring quarterly audits from Everest 19).

**Scoring:**

| Finding Severity | Impact | Applicability |
|---|---|---|
| **Critical** | -0.20 (score floor 0.40) | Must be remediated before production tier |
| **High** | -0.10 | Remediation within 30 days |
| **Medium** | -0.05 | Acknowledged in next quarterly audit |
| **Low** | -0.01 | Informational; no action required |
| **No findings** | +0.10 (cumulative) | Per clean audit; caps at +0.30 |

**Formula:**  
`audit_component = base_weight * (1.0 - sum_deductions + clean_bonuses)`  
where `base_weight = 0.40` and capped in [0.15, 0.40].

**Quarterly refresh:** Latest external audit result replaces prior; audit firm's own reputation considered (Everest 44 verifier reputation feeds back).

---

### 2. Slash-Event Weight (35% of base score)

**Source:** Documented slash events (Everest 21) — issuer caught issuing fraudulent credentials, revocation executed, published on-chain.

**Scoring:**

| Event | Impact | Recovery Window |
|---|---|---|
| **1st slash** | -0.15 (min score 0.20) | 12 months (exponential decay) |
| **2nd slash** | -0.25 (min score 0.10) | 24 months |
| **3rd+ slash** | -0.35 (min score 0.0) | 36 months (issuer likely removed) |
| **No slash events** | +0.10 (cumulative; caps at +0.35) | Per clean year |

**Decay:** `recovery(t) = deduction * (1 - e^(-t/6mo))` — 50% recovery in 6 months, asymptotic to full recovery in 24 months.

**Formula:**  
`slash_component = base_weight * (1.0 - sum_deductions_with_decay + no_slash_bonus)`  
where `base_weight = 0.35` and capped in [0.0, 0.35].

---

### 3. Endorsement Weight from Peer Issuers (15% of base score)

**Source:** Issuer-to-issuer endorsement records (Everest 16).

**Scoring:**

| Endorsement Profile | Score Boost |
|---|---|
| **Endorsed by 3+ issuers in 3+ classes** | +0.12 |
| **Endorsed by 2 issuers in 2+ classes** | +0.08 |
| **Endorsed by 1 issuer** | +0.04 |
| **No endorsements** | 0.0 |
| **Distrusted by 1+ issuer** | -0.03 per distrust |

**Endorsement expiration:** Endorsements remain valid for 24 months from publication; expired endorsements don't count (issuer must refresh).

**Collusion detection:** If issuer A and B endorse each other, and A slashes 1 month later, B's endorsement weight reduces by 50% for 12 months (reputational cost of vouching fraud). Detected via on-chain audit trail.

**Formula:**  
`endorsement_component = base_weight * (1.0 + boost - distrust_penalty)`  
where `base_weight = 0.15` and capped in [0.0, 0.15].

---

### 4. Age in Ecosystem (5% of base score)

**Source:** Issuer onboarding date (Everest 11, Step 7; published on transparency log).

**Scoring:**

| Age | Multiplier |
|---|---|
| **< 3 months (pilot phase)** | 0.5× |
| **3 months – 1 year** | 0.75× |
| **1 – 2 years** | 0.90× |
| **2+ years** | 1.0× |

**Rationale:** Newer issuers lack track record; weight reflects lower confidence until maturity.

**Formula:**  
`age_component = base_weight * 0.05 * multiplier(issuer_age)`  
where `base_weight = 1.0` (this component adds to, not competes with, other weights).

---

### 5. Revocation Rate (5% of base score)

**Source:** Issuer's revocation registry (Everest 15); aggregate over trailing 12 months.

**Scoring:**

```
revocation_rate = count_revocations / (count_issued + 1)  // +1 to avoid division by zero
```

| Rate | Penalty |
|---|---|
| **0%** | 0.0 (no penalty) |
| **0–5%** | -0.01 |
| **5–10%** | -0.03 |
| **10–20%** | -0.07 |
| **20%+** | -0.12 (floor: score 0.0) |

**Distinction:** Revocation ≠ slash. Revocation = legitimate credential expiration or holder request. High revocation rate suggests compliance issues or credential design problems.

**Formula:**  
`revocation_component = -penalty(revocation_rate)`.

---

## Signed Manifest Schema

Each issuer publishes a signed reputation manifest quarterly (or upon change). Format:

```json
{
  "issuer_did": "did:calm:issuer:acme-state",
  "issuer_name": "ACME State Authority",
  "issuer_class": "State",
  "manifest_version": "1.0",
  "as_of_timestamp": "2026-05-20T00:00:00Z",
  "refresh_interval_days": 90,
  
  "reputation_score": 0.872,
  "score_components": {
    "audit_results": {
      "weight": 0.40,
      "value": 0.365,
      "latest_audit_date": "2026-05-10",
      "latest_audit_firm": "did:calm:auditor:sigsum-labs",
      "findings_summary": "1 Medium, 0 High, 0 Critical"
    },
    "slash_events": {
      "weight": 0.35,
      "value": 0.335,
      "total_slashes": 0,
      "months_since_last_slash": null,
      "no_slash_bonus_applied": 0.10
    },
    "endorsement_weight": {
      "weight": 0.15,
      "value": 0.135,
      "endorser_count": 2,
      "endorser_classes": ["Professional", "State"],
      "distrust_count": 0,
      "expired_endorsement_count": 0
    },
    "age_in_ecosystem": {
      "weight": 0.05,
      "onboarding_date": "2024-05-20",
      "age_months": 24,
      "age_multiplier": 1.0,
      "value": 0.05
    },
    "revocation_rate": {
      "weight": 0.05,
      "issued_count_12m": 1250,
      "revoked_count_12m": 5,
      "revocation_rate": 0.004,
      "penalty": 0.0,
      "value": 0.05
    }
  },
  
  "tier_status": {
    "experimental": true,
    "pilot": true,
    "production": true,
    "status_change_date": "2025-05-20",
    "status_change_reason": "Audit passed; slashing acceptance signed"
  },
  
  "key_rotation_schedule": {
    "current_key_id": "key-2025-05-20",
    "next_rotation_date": "2026-05-20",
    "grace_window_days": 180
  },
  
  "manifest_signature": {
    "algorithm": "Ed25519",
    "signer_key_id": "did:calm:issuer:acme-state#key-mgmt-2025",
    "signature_bytes": "base64:...",
    "signature_timestamp": "2026-05-20T09:00:00Z"
  },
  
  "manifest_chain_anchor": {
    "transparency_log_txid": "sigsum:...",
    "chain_timestamp": "2026-05-20T09:15:00Z"
  }
}
```

---

## Privacy-Preserving Verifier Queries

**Query pattern:** Verifier queries `GET /reputation-api?issuer_did=X` (no credential_id, no holder context). Server returns issuer X's signed manifest (public record). Verifier computes local trust decision; logs only issuer_did + decision (no credential identification).

**No leakage:** Server doesn't know which credential verifier is checking; verifier's log doesn't name credentials. Batch queries return all public manifests; server cannot correlate which issuer the verifier will actually use.

---

## Gaming Defenses

### Defense 1: No Self-Vouching

**Rule:** An issuer cannot endorse itself. Self-endorsement records are rejected at publication time (Everest 16 validates).

**Enforcement:** Transparency log (Everest 19) validates endorser_did ≠ endorsed_did before chaining.

### Defense 2: Endorsement Expiration

**Rule:** An endorsement is valid for 24 months; after 24 months, it no longer contributes to endorsement score.

**Benefit:** Prevents perpetual reputation laundering (issuer X endorses issuer Y once, then Y's reputation stays high forever).

**Mechanism:** Verifier queries issuer's manifest; manifest includes endorser_list with expiration dates. Verifier computes score only from non-expired endorsements.

### Defense 3: Collusion Pattern Detection

**Rule:** If issuer A endorses issuer B, and B is slashed within 12 months, A's endorsement weight for all other issuers reduces by 50% for 12 months.

**Implementation:** Manifest includes `endorser_collusion_history` with deduction dates + reasons.

### Defense 4: Clique Deduction

**Rule:** If N issuers (N ≥ 3) mutually endorse each other and 1 member slashes, all members suffer: `endorsement_weight *= (1 - 0.10 * slash_count_in_clique)` (min 0.0).

---

## Production-Tier Enforcement

### Threshold Rules

**Production tier eligibility** (per Everest 20):

| Tier | Reputation Score Minimum | Key Gate |
|---|---|---|
| **Experimental** | None (can be 0.0) | Issue up to 100 credentials/month |
| **Pilot** | ≥ 0.40 | Issue up to 1000 credentials/month; require ≥2 external verifiers per credential sample |
| **Production** | ≥ 0.65 | Unlimited issuance; standard verifier processing |

### Automatic Tier Revocation

**Rule:** If issuer's reputation score falls below tier threshold, production tier is revoked immediately.

**Effect:**

1. Issuer DID enters `tier_status.production = false` in next manifest refresh (or within 24 hours).
2. Verifiers query issuer manifest; see production status revoked.
3. Verifiers apply tier-specific logic (Everest 20): reject new credentials if production tier required.
4. Existing credentials enter grace period (Everest 34): 180 days' continued acceptance, then rejection.

**Issuer notification:** Public statement published to transparency log + issuer directory explaining reason + appeal path (Everest 85).

---

## Appeal Protocol

### Appeal Request

**Issuer submits:**

1. Written appeal statement (reasoning why reputation calculation is incorrect or unfair)
2. Evidence package (audit reports, corrected revocation counts, etc.)
3. Witness signatures (≥2 peer issuers affirming issuer's integrity)

**Governance body (TBD in Everest 11 open question)** reviews within 30 days.

### Appeal Outcome

**Overturned:** Reputation score recalculated; issuer restored to prior tier.

**Upheld:** Score stands; issuer may re-appeal after 6 months with new evidence.

**Partial correction:** Score adjusted if calculation error found (e.g., wrong revocation rate); issuer may still be below threshold.

---

## Composition with Related Everests

| Everest | Dependency | Use |
|---------|------------|-----|
| **11** (Governance) | Prereq | Issuer onboarding, charter, initial score baseline |
| **12** (Key ceremony) | Related | Key ceremony transparency feeds audit trust |
| **13** (Key custody) | Related | Custody choices affect audit findings weight |
| **15** (Revocation registry) | Dependency | Revocation rate component source |
| **16** (Issuer-issuer trust) | Dependency | Endorsement + distrust records source |
| **19** (Audit log) | Prereq | Audit results component, quarterly refresh |
| **20** (Licensing) | Downstream | Tier thresholds, tier revocation gates |
| **21** (Slashing) | Prereq | Slash events component, decay function |
| **25** (Directory) | Downstream | Issuer manifests published in directory |
| **71–75** (Trust graph) | Downstream | Reputation scores consumed by trust algorithms |

---

## Acceptance Tests

### T-Z23.1: Score Computation

**Scenario:** Issuer X: 1 Medium audit finding (-0.05); no slashes (+0.10 bonus); 2 endorsers in 2 classes (+0.08); 18 months old (0.90×); 0% revocation (0 penalty).

**Calculation:** 0.35 + 0.35 + 0.135 + 0.045 + 0.05 = 0.875.

**Acceptance:** Manifest published with score 0.875; verifiers reproduce from components.

### T-Z23.2: Privacy-Preserving Query

**Scenario:** V1 queries issuer X; V2 queries issuer Y. Neither server nor issuer learns which credential is being verified.

**Flow:** (1) V1: `GET /reputation-api?issuer_did=X`. (2) Server returns Manifest(X) (public). (3) V1 logs only `[issuer_did=X, decision=accept]`. (4) No credential_id in log.

**Acceptance:** No server-side correlation of verifier ↔ credential.

### T-Z23.3: Collusion Pattern Detection

**Scenario:** A endorses B; B slashed within 12 months. A's endorsement weight reduces 50%.

**Flow:** (1) M0: A endorses B. (2) M3: B slashed. (3) M4: A's manifest shows `endorser_collusion_history = [{colluded_with: B, deduction: 0.05}]`. (4) A's endorsement_weight = 0.135 - 0.05 = 0.085 for 12 months.

**Acceptance:** Deduction correctly applied and auditable.

### T-Z23.4: Tier Revocation on Score Drop

**Scenario:** Issuer X drops from 0.75 to 0.62 (below production threshold). Tier revoked.

**Flow:** (1) X slashed → score 0.62. (2) Next refresh: production = false. (3) Verifier queries manifest → sees revocation. (4) Applies E20 rules: rejects new credentials, existing enter 180-day grace.

**Acceptance:** Automatic revocation; E20 composition verified.

### T-Z23.5: Manifest Signature Verification

**Scenario:** Verifier checks manifest integrity: signature + chain anchor.

**Flow:** (1) Manifest signature verified against issuer's pubkey (E12 ceremony). (2) Chain anchor verified against transparency log txid. (3) Failure on either = reject as forged.

**Acceptance:** Tampering detected; integrity verifiable.

---

## Open Questions for v1

1. **Reputation initialization for genesis issuers:** How are the first N issuers (e.g., state authorities, founding ecosystem members) assigned initial scores before they have audit histories or endorsements? Possible answers: (a) All start at 0.50 (neutral); (b) Governance body sets initial scores based on institutional credentials; (c) Gradual reputation accrual from first audit.

2. **Score volatility:** Should large reputation swings (e.g., 0.75 → 0.40 from a single slash) be smoothed over N days, or applied immediately? Trade-off: immediacy = fast trust response; smoothing = stability but slower bad-actor detection.

3. **Third-party reputation auditing:** Can an independent auditor flag a reputation score as suspect (e.g., "this issuer's audit was from a non-credible firm")? If yes, how does the flag affect verifier weighting?

---

## Acceptance Signature

**Acceptance:** ✓ Reputation primitive specified in full. Score components (audit, slash, endorsement, age, revocation rate), gaming defenses (no self-vouching, collusion detection, expiration), manifest schema, privacy-preserving query, tier enforcement, and appeal protocol confirmed.

**Test gates:** T-Z23.1, T-Z23.2, T-Z23.3, T-Z23.4, T-Z23.5 ready for implementation.

**Dependency chain:** Awaiting Everest 11, 19, 21 finalization before production deployment.

---

— Calm, 2026-05-20

**Byte count:** 14,900 bytes (~14.9 KB).
