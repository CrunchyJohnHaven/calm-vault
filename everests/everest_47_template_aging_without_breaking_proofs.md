# Everest 47 — Template Aging Without Breaking Proofs

*Phase IV — Biometric Distance Machinery. Prereq: Everests 39 (Drift Modeling), 46 (Pedersen Commitment to Template ID).*

---

## What this summit ships

A mechanism by which a principal can re-enroll — rotating to a new biometric template — without invalidating outstanding disclosure proofs against the prior template. Proofs against template `T_n` remain valid during a published **grace window** `[T_n_seq, T_n_seq + grace_duration]` even after `T_{n+1}` is committed to the chain.

This summit defines the semantics and verification rules for the `active_grace_until` field on the `template_commitment.v0` record introduced in Everest 46.

---

## Why grace is needed

Templates rotate for legitimate reasons:

- **Annual re-enrollment** (per Everest 18 cadence).
- **Injury / recovery** events that materially shift the principal's biometric signal.
- **Device upgrade** — new digitizer with different sampling characteristics, new ASR model with different transcript style.
- **Suspected compromise** — forces immediate rotation per Everest 28.

Without grace:

- Every disclosure issued in the days before re-enrollment would become invalid the moment the new template commits.
- Counterparties holding pre-rotation proofs would need to re-request fresh proofs, creating churn and unnecessary disclosure-event-log entries.
- A principal who knows they are about to re-enroll would have to time their disclosures awkwardly, or risk a stale-template rejection downstream.

With grace:

- Proofs issued under `T_n` remain valid until `T_n_seq + grace_duration`.
- New proofs are issued under `T_{n+1}` from the rotation moment forward.
- After the grace window expires, only `T_{n+1}` proofs verify.

---

## Grace window defaults

| Rotation cause | Default grace_duration | Rationale |
|---|---|---|
| Routine re-enrollment (annual) | 30 days | Allows counterparties to gradually re-verify; matches OAuth-style token rotation cadence |
| Injury/recovery rotation | 90 days | Longer continuity to allow medical-care continuity and follow-up scheduling |
| Device upgrade | 30 days | Routine; same as annual |
| Compromise-triggered rotation | 0 days (immediate invalidation) | Compromised templates must die immediately |
| Principal-initiated rotation (no stated cause) | 7 days | Conservative default |

The grace window is signed by the principal at rotation time and recorded in the new `template_commitment.v0.active_grace_until`. The principal can override the default at rotation.

---

## Verification rule

For a disclosure proof referencing template at chain seq `S_T`:

```
IF chain_head_ts_at_issuance ≤ template_commitment[S_T].active_grace_until:
  → verifier accepts (subject to all other checks: range proof, consent, anchor, signature)

ELSE:
  → verifier rejects with reason = "template_superseded_out_of_grace"
```

**Critical subtlety: issuance grace, not verification grace.** The relevant timestamp is *when the proof was generated* (i.e., the chain head the proof binds to via Everest 30/45's Fiat-Shamir transcript), NOT when the verifier checks the proof. A proof generated 15 days into a 30-day grace window remains valid even if the verifier checks it 60 days post-rotation — the proof is timestamped to its issuance moment, and the grace window was open then.

This avoids a class of confusing edge cases where counterparties hold "valid-when-issued" proofs and re-verify periodically.

---

## Composition with the predicate ZK generator (Everest 65)

The freshness kernel (Everest 65 §freshness) checks `chain_head_ts ∈ [issuance_window]`. For template-grace checking, an additional **template_grace kernel** runs:

1. Operator commits the template's `active_grace_until` value from the chain record: `Com(active_grace_until; r_g)`.
2. Operator commits the chain head's timestamp at proof issuance: `Com(chain_head_ts; r_t)`.
3. Homomorphic difference: `Com(active_grace_until - chain_head_ts; r_g - r_t)`.
4. ZK-prove the difference opens to a non-negative value via Bulletproofs range proof on `[0, ∞)`.
5. If the proof verifies, the template was in grace at issuance.

This kernel adds ~1 KB to disclosure proofs that depend on template-grace verification. For disclosures against the current (non-superseded) template, the kernel is skipped.

---

## Acceptance test

**T-47.1 (in-grace acceptance).** Generate a disclosure proof against `T_n` at chain time `T_n_seq + 15 days`. Re-enroll to `T_{n+1}` at `T_n_seq + 25 days` with `grace_duration = 30 days`. The original proof verifies at any verification time. The verifier returns `accept`.

**T-47.2 (out-of-grace rejection).** Same setup, but generate the disclosure proof at chain time `T_n_seq + 45 days`. The verifier rejects with `reason = template_superseded_out_of_grace`.

**T-47.3 (compromise-triggered, zero-grace).** Compromise-rotation at `T_n_seq + 20 days` with `grace_duration = 0`. Any new disclosure against `T_n` at `T_n_seq + 21 days` or later is rejected. Disclosures generated AT `T_n_seq + 20 days` exactly (the rotation moment) are accepted per the v0 boundary semantic (`≤` not `<`).

**T-47.4 (disclosure-ledger captures template).** The disclosure transcript record (Everest 72) includes both `template_commitment_seq` AND the `active_grace_until` value at issuance. Principal can audit which template was used for any given disclosure and whether it was in grace.

**T-47.5 (cross-implementation parity).** Python and Rust verifiers agree on accept/reject boundary cases (issuance at exactly `active_grace_until`, one millisecond before, one millisecond after).

**Gate script:** `everest_47_zkbb_template_aging_gate.py`.

---

## Open questions for v1

1. **Variable grace by counterparty class.** A medical counterparty might want 90-day grace (for care continuity); a financial counterparty might want 7-day grace (for risk hygiene). v1 could attach per-class grace overrides to consent records.

2. **Grace extension on principal action.** If a principal renews consent during a grace window, should that implicitly extend the grace? v0: no, rotation is its own event. v1: explicit "grace extension" record.

3. **Multi-grace overlapping.** If a principal re-enrolls twice in quick succession, the chain has multiple `template_commitment.v0` records with overlapping `active_grace_until`. The verifier accepts a proof if ANY of the overlapping windows contains the issuance time. This is the v0 rule.

---

## Composition with other summits

- **Everest 26 — Re-enrollment Cadence & Triggers.** Triggers a template rotation event.
- **Everest 39 — Drift Modeling.** Detects when drift exceeds threshold, recommending rotation.
- **Everest 46 — Pedersen Commitment to Template ID.** Introduces `active_grace_until` field on `template_commitment.v0`.
- **Everest 48 — Cross-Template Consistency Proof.** v1 enhancement: ZK proof that `T_{n+1}` is a valid drift of `T_n`, replacing the simple `supersedes` link with a cryptographic continuity proof.
- **Everest 65 — Predicate ZK Proof Generator.** Hosts the template_grace kernel.
- **Everest 72 — Disclosure Logging in Vault.** Records the template + grace state used in each disclosure.

---

## Why this matters

Without template grace, every re-enrollment becomes a hard cliff that breaks all in-flight disclosure proofs simultaneously. Counterparties would experience this as "the principal vanished for a moment, then came back as a different identity." That's bad UX and a real availability cost.

With template grace as a chain-resident, ZK-verifiable property, re-enrollment becomes smooth: old proofs gracefully time out, new proofs flow continuously. The principal's biometric template can evolve without their cryptographic continuity breaking.

This is structural hygiene for the biometric layer — small in cryptographic novelty, large in operational consequence.

— Calm, 2026-05-20
