# Everest 73 — Counterparty-Class Authorization

*Phase VI — Disclosure Semantics. Prereq: Everest 57, 7.*

---

## Purpose

Calm Witness consent operates on two levels: (1) class-default consents, where the principal authorizes disclosure to any member of a counterparty class (e.g., "all banks"), and (2) per-counterparty consents, where the principal authorizes disclosure to a specific identity (e.g., "JPMorgan only"). This everest specifies the model of class-based default authorization, how the principal sets and modifies class defaults, how class membership is verified, and how per-counterparty consent takes precedence over class defaults.

Class authorization is a performance and usability layer. Rather than issuing per-identity consent records for every bank a principal might encounter, the principal can set a class-wide default that applies to all banks in that class—and can override individual class members without disrupting the class default. This layering reduces cognitive load while preserving fine-grained principal authority.

---

## Class Default Consent Model

### Definition

A **class default consent** is a consent record (per Everest 8, Axiom A6) that authorizes a principal to disclose a predicate `p` to any counterparty in a class `c`, without requiring per-identity consent for each member of the class.

Formally, a class default consent is a `consent.grant` record with:
- `payload.predicate_id`: A predicate from Everest 6 (e.g., `in_baseline_24h`, `mental_state_unusual`).
- `payload.counterparty_identifier`: A class slug from Everest 7 (e.g., `financial`, `peer_ai_collective`, `insurance`).
- All other fields (expiry, nonce, signature) as per Axiom A6.

### Storage and Lifecycle

Class default consents are stored in `user_state.jsonl` as ordinary `consent.grant`, `consent.modify`, and `consent.revoke` records. They participate in the hash chain and are tamper-evident under Axiom A6. The principal's vault makes no distinction between a class default and a per-counterparty consent record—both are records in the chain, both are auditable, both are revocable.

### Bootstrap at Enrollment

At vault enrollment (Everest 20), the principal specifies a set of per-class default consent policies for each Everest 7 class. For example:
- `in_baseline_24h` → peer_ai_collective: ALLOW.
- `cognitively_atypical_baseline` → peer_ai_collective: ALLOW, others: DENY.
- Every predicate for insurance class: DENY (no defaults).

The enrollment operator translates these policies into explicit `consent.grant` records in the initial chain entries and publishes their hashes to Sigsum. After this bootstrap step, the consent records are indistinguishable from user-issued modifications. The operator runs `calm-witness consent bootstrap-from-class-defaults` at the end of enrollment to finalize the chain.

---

## Granting and Modifying Class Defaults

### Command Interface

The principal modifies class defaults via the vault CLI:

```bash
calm-witness consent grant <predicate_id> --class <class_id> --expiry <ts>
calm-witness consent revoke <predicate_id> --class <class_id> [--expiry <ts>]
calm-witness consent modify <predicate_id> --class <class_id> [--narrow] [--expiry <ts>]
```

**Grant example:**

```bash
calm-witness consent grant in_baseline_24h --class financial --expiry 2027-05-20T23:59:59Z
```

Appends a `consent.grant` record with `counterparty_identifier = "financial"` to the chain. Future requests from any counterparty whose CredexAI VC asserts the `financial` class will match this record (per Axiom A7).

**Revoke example:**

```bash
calm-witness consent revoke in_baseline_24h --class financial
```

Appends a `consent.revoke` record referencing the prior grant's seq. All subsequent disclosure requests to the financial class for this predicate are refused.

**Modify example:**

```bash
calm-witness consent modify in_baseline_24h --class financial --narrow --expiry 2026-12-31T23:59:59Z
```

Appends a `consent.modify` record narrowing the scope (per Axiom A3). The freshness window, predicate parameters, or expiry may be tightened but not expanded.

---

## Class Membership Verification

### CredexAI Verifiable Credential

Each counterparty presents a CredexAI-issued verifiable credential (VC) at session time. The VC includes cryptographically asserted class membership claims. For example, a bank VC might assert:

```json
{
  "iss": "CredexAI",
  "sub": "jpm.banking.org",
  "class_assertions": ["financial"],
  "sector": "banking",
  "license_jurisdiction": "US",
  "license_type": "bank",
  "issued_at": "2026-04-01T00:00:00Z",
  "expires_at": "2027-04-01T00:00:00Z"
}
```

The operator (or the principal's vault, depending on deployment) verifies the VC signature and confirms that the class assertion matches a known Everest 7 class. The VC's expiry is checked; if the VC is expired, the counterparty is not admitted to any class.

### Membership is Binary

Class membership in v0 is a flat, binary relation: a counterparty either IS in a class or is NOT. There is no hierarchy. For example, a counterparty cannot be in both `financial` and `medical` via inheritance; the VC must explicitly assert each class the counterparty claims.

If a counterparty asserts multiple classes (e.g., `financial` and `research`), the vault checks consent for each class separately and returns consent only if the principal has granted the requested predicate to at least one of the asserted classes.

### Class Disputes

If a counterparty's VC asserts class `X` but the principal believes the counterparty's behavior or licensing suggests class `Y`, the principal can issue a per-counterparty consent record that overrides the VC's class assertion (see "Precedence" below). The operator logs this as a `kind: "counterparty.class_dispute"` advisory record but does not arbitrate the dispute. The principal's override is the source of truth for that counterparty going forward.

---

## Per-Counterparty Consent and Precedence

### Definition

A **per-counterparty consent** is a consent record targeting a specific counterparty identity, identified by a VC fingerprint (e.g., `vc:jpm.banking.org:2026-04-01`), rather than a class slug.

Per-counterparty consent allows the principal to refine, override, or deny disclosure to a specific member of a class without affecting the class default.

### Precedence Rule

When evaluating `principal_consents_to_disclose(p, c)` for predicate `p` and counterparty `c`:

1. The operator scans the chain for all active consent records (per Everest 57 evaluation algorithm).
2. If a per-counterparty consent record exists for `c`, it takes precedence over any class default for `c`'s asserted classes.
3. Formally, the per-counterparty record is more recent in the chain walk and overwrites any class record.

**Examples:**

1. **Class allow, specific deny:**
   - Principal grants `in_baseline_24h` to class `financial`.
   - Principal then issues a per-counterparty consent.modify (or consent.revoke) for JPMorgan specifically.
   - JPMorgan requests `in_baseline_24h`: refused (per-counterparty overrides class default).
   - Wells Fargo requests `in_baseline_24h`: granted (class default remains in effect).

2. **Class deny, specific allow:**
   - Principal grants `mental_state_unusual` to class `medical` only.
   - A specific bank requests `mental_state_unusual`: would normally be refused (bank is not in medical class).
   - Principal issues a per-counterparty consent.grant for that bank with `mental_state_unusual`.
   - Bank requests: granted (per-counterparty override permits disclosure outside normal class).

3. **Per-identity chain narrowing:**
   - Principal starts with `in_baseline_24h` → financial class (all banks).
   - Principal narrows via consent.modify to a specific bank only.
   - Subsequent requests from other banks: refused (chain walk finds the narrowing modification).

Per-counterparty consent is always more specific than class consent. Once a per-counterparty record exists for a counterparty, that record governs all disclosures to that counterparty for the named predicate, and the class default is shadowed (not revoked, but inactive for that identity).

---

## Rate Limiting per Class

Each Everest 7 class has a default maximum disclosure rate per 24 hours. Per Everest 76, the operator enforces this limit:

- **financial:** 10 disclosures per 24h.
- **journalistic:** 3 disclosures per 24h.
- **medical:** 5 disclosures per 24h.
- **governmental:** 2 disclosures per 24h.
- **peer_ai_collective:** 50 disclosures per 24h.
- **family:** 100 disclosures per 24h.
- **anonymous:** 1 disclosure per 24h.
- **insurance:** 0 per 24h (always explicit opt-in).
- **employer:** Governed by principal's per-class policy, default 0 or low rate.
- **research:** 5 disclosures per research protocol per principal per 30 days.

If the principal issues a per-counterparty consent, the rate limit for that specific counterparty can be set independently of the class rate limit. For example:
- Class financial: 10/day (applies to all banks).
- Per-counterparty for JPMorgan: 20/day (this bank gets a higher limit).

Rate limits compose (per Everest 76): they stack with other gates and are enforced at disclosure time.

---

## The Insurance Class Special Case

The insurance class is deliberately high-risk and has no class default consents in v0. Every disclosure to an insurance counterparty requires explicit per-counterparty opt-in (Everest 7, §9).

**Justification:** Insurance underwriting is fundamentally a negative-selection business. An insurer who learns of unusual mental state, atypical baseline, or recent health changes has a strong financial incentive to deny coverage, raise premiums, or exclude conditions. Unlike a bank (which profits from lending) or a medical provider (which profits from care), an insurer profits from claim denial.

**Operational rule:** If the principal's vault receives a disclosure request from a counterparty whose VC asserts the insurance class, the evaluation of `principal_consents_to_disclose(p, insurance)` always returns false unless there exists an explicit per-counterparty consent.grant record for that specific insurer. Class defaults do not apply. There are no ALLOW or EXPLICIT_OPT_IN defaults for the insurance class; all defaults are DENY, and overriding the default requires explicit written principal consent per disclosure request.

---

## Class Default Mutation and Retroactivity

### Changing Defaults

The principal can revoke, modify, or replace class defaults at any time via consent records. For example:

- **Revoke:** `calm-witness consent revoke in_baseline_24h --class financial` invalidates the class default for all future requests to the financial class.
- **Narrow:** `calm-witness consent modify in_baseline_24h --class financial --narrow` reduces the freshness window or other predicate parameters.
- **Re-grant:** After revocation, a new `consent.grant` can establish a new default.

### Non-Retroactivity

Outstanding disclosures that were authorized under a now-revoked class default remain valid for their freshness window. Revocation does not retroactively invalidate proofs already issued. However:

- A proof issued at time t1 under a class default that is revoked at time t2 > t1 is valid if presented at t2 + ε (it was issued under valid consent at t1).
- A request for a new proof after t2 is refused (no active consent at request time).

Revocation propagates via Everest 75 (transparency log CRL push), and verifiers checking a proof will see the revocation and may question its validity retroactively.

---

## Worked Examples

### Example 1: Class Default Allow

Principal grants `in_baseline_24h` to peer_ai_collective at enrollment. Bob (peer_ai_collective VC) requests the predicate.

- Enrollment creates `consent.grant(in_baseline_24h, peer_ai_collective, expiry=+90 days)`.
- Bob's VC asserts class `peer_ai_collective`.
- Evaluation of `principal_consents_to_disclose(in_baseline_24h, bob)` finds the class grant.
- Bob's class assertion matches the grant's counterparty_identifier.
- **Result: GRANTED.** Bob receives a ZK proof.

### Example 2: Per-Counterparty Override (Deny)

Principal has class default ALLOW for `in_baseline_24h` → financial (all banks). Later, principal revokes consent specifically for JPMorgan:

- Enrollment: `consent.grant(in_baseline_24h, financial, expiry=+90 days)` (seq=5).
- Day 10: Principal issues `consent.revoke(in_baseline_24h, vc:jpm.banking.org:2026-04-01, references_prior_seq=none)` (seq=25). This is a per-counterparty revoke (no VC was granted to JPM in the chain, but the revoke establishes an explicit denial).

Alternative, if JPM is granted and then modified to deny:
- Enrollment: `consent.grant(in_baseline_24h, financial, expiry=+90 days)` (seq=5).
- Day 5: Principal issues `consent.grant(in_baseline_24h, vc:jpm.banking.org:2026-04-01, expiry=+1 day)` (seq=10) to grant per-counterparty consent.
- Day 6: Principal issues `consent.revoke(in_baseline_24h, vc:jpm.banking.org:2026-04-01, references_prior_seq=10)` (seq=15).
- JPMorgan requests on day 6: Chain walk finds seq=5 (grant, class), seq=15 (revoke, per-counterparty). Final state is None. **Result: DENIED.**

### Example 3: Class Dispute

Counterparty Acme presents a VC asserting class `anonymous` but claims to be a news outlet. Principal suspects Acme is actually a data broker and issues a per-counterparty consent.revoke for Acme's VC fingerprint, even though no prior consent.grant was issued for Acme.

- Enrollment: `consent.grant(in_baseline_24h, journalistic, expiry=+90 days)` (seq=3).
- Day 2: Acme (vc:acme.news.invalid:2026-04-15) claims to be journalistic but presents anonymous-class VC.
- Principal issues `consent.revoke(in_baseline_24h, vc:acme.news.invalid:2026-04-15)` (seq=12), establishing an explicit denial for this identity.
- Operator logs `kind: "counterparty.class_dispute"` record (advisory, not enforced).
- Acme requests: Chain walk finds seq=12 (revoke, per-counterparty). Final state is None. **Result: DENIED.** Acme does not learn whether the denial is due to class mismatch, consent absence, or explicit revocation—all refusals are observationally identical (Everest 57 side-channel note).

### Example 4: Insurance Class Zero-Default

Principal's insurance class defaults are all DENY (per Everest 7). At enrollment, no `consent.grant` records are created for the insurance class. Later, principal wants to apply for disability insurance and wants to signal good health.

- Enrollment: No grants for insurance class (all defaults implicitly DENY).
- Day 30: Principal issues explicit `consent.grant(in_baseline_24h, vc:disability_underwriter.xyz:2026-05-15, expiry=2026-05-20T23:59:59Z)`.
- Underwriter requests `in_baseline_24h` before 2026-05-21: Chain walk finds seq=N (grant, per-counterparty, unexpired). **Result: GRANTED.**
- Underwriter requests on 2026-05-21 (after expiry): Chain walk finds seq=N (grant, expired). **Result: DENIED.** Consent was always explicit and temporary, not a default.

---

## Privacy and Counterparty-Facing Semantics

The counterparty requesting disclosure does not learn whether a refusal came from class-level denial, per-counterparty denial, class-membership mismatch, or consent expiry. In all cases, the operator returns "consent not granted" with no further detail. This protects the principal's privacy and prevents the counterparty from enumerating the principal's consent decisions.

---

## Cross-References and Integration

- **Everest 7:** Disclosure-class taxonomy. Defines ten classes, membership VCs, default consent matrices per class, and rate limits per class.
- **Everest 8:** Consent calculus axioms, especially A1 (revocability), A3 (scope narrowing), A6 (chained-into-vault), A7 (per-predicate-per-counterparty).
- **Everest 20:** Enrollment ceremony, including principal's initial per-class default policy choices and bootstrap script.
- **Everest 57:** `principal_consents_to_disclose` predicate. Evaluates per-class and per-counterparty consent records.
- **Everest 74:** Per-counterparty consent detail.
- **Everest 75:** Revocation propagation and transparency-log integration.
- **Everest 76:** Rate limiting per class and per counterparty.

---

— Calm, 2026-05-20
