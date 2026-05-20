# Calm Compass — Counter-Claim Protocol v0

**Draft v0 · 2026-05-20 · Calm**  
**Closes Everest 111 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**  
**Companion to [`COMPASS_EVIDENCE_CEREMONY_v0.md`](COMPASS_EVIDENCE_CEREMONY_v0.md) §4, [`COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md`](COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md) §7, and `~/CredexAI/calm_witness/compass_eval.py`.**

---

## §1 — Purpose

Third parties may allege that a principal **willfully harmed** them. Calm Compass does not adjudicate guilt in the abstract; it chains attributed claims, gives the principal a bounded rebuttal window, and exposes a **disputed** state on the `no_known_willful_harm_in_window_365d` predicate until claims are rebutted or age out of the evaluation window.

This protocol formalizes:

1. **Filing** — `compass_evidence.counter_claim` with mandatory full attribution.
2. **Rebuttal** — `compass_evidence.principal_rebuttal` within 30 days.
3. **Evaluator semantics** — `HarmStatus` (`bit`, `disputed`, `active_counter_claim_seqs`) from `no_known_willful_harm()`.

---

## §2 — Counter-claim record (`compass_evidence.counter_claim`)

**Author:** third party Q (not principal P).  
**Channel:** audit-process-mediated (`submitted_via`, Everest 115).  
**Schema:** see [`COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md`](COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md) §7.

**Mandatory fields:**

| Field | Rule |
|-------|------|
| `claimant_id` | Non-empty CredexAI VC ID; **no anonymity** |
| `alleged_harm_narrative` | Non-empty substantive account |
| `alleged_harm_window.from` / `.to` | Valid ISO8601; `to` ≥ `from` |
| `submitted_via` | Non-empty channel id (e.g. `calm_audit_process_v0`) |

**Filing flow (ceremony §4):**

1. Q initiates via audit panel intake (not direct vault injection).
2. Panel verifies refusal-floor compliance (no protected-category fishing).
3. Record is appended to **P's** vault chain with Q's operator signature.
4. P receives notification: claimant identity + full narrative + harm window.

---

## §3 — Principal rebuttal (`compass_evidence.principal_rebuttal`)

**Author:** principal P.  
**Window:** 30 calendar days from counter-claim `ts` (`rebuttal_window_days` default in `compass_eval.py`).

**Schema:**

```json
{
  "kind": "compass_evidence.principal_rebuttal",
  "payload": {
    "targets_counter_claim_seq": <int, seq of the counter_claim>,
    "rebuttal_narrative": "<string, substantive; non-empty after strip>",
    "evidence_record_seqs": [<int>, ...]
  },
  "ts": "<ISO8601, must be after targeted claim ts>",
  "seq": <int>,
  "operator": "<P's operator>",
  "signature": "<ed25519:hex>"
}
```

**Invariants:**

- `targets_counter_claim_seq` must reference an existing `counter_claim` in P's chain.
- `rebuttal_narrative` must be non-empty; empty or whitespace-only rebuttals are **ignored** by the evaluator.
- `evidence_record_seqs` is optional; when present, each seq must exist in the chain.

**Ceremony UI (COMPASS_EVIDENCE_CEREMONY_v0 §4.2):** P addresses Q's account directly; may link prior evidence records; signs with operator key.

---

## §4 — Reference implementation: `HarmStatus`

`compass_eval.py::no_known_willful_harm()` returns:

```python
@dataclass(frozen=True)
class HarmStatus:
    bit: bool          # True iff no active unrebutted claims
    disputed: bool     # True iff active unrebutted claims exist
    active_counter_claim_seqs: tuple[int, ...]
```

**Claim collection:** all `compass_evidence.counter_claim` records with valid `claimant_id`, `ts` within `claim_window_days` (default 365).

**Rebuttal detection:** any `principal_rebuttal` with matching `targets_counter_claim_seq` and substantive `rebuttal_narrative` removes the claim from the active set.

**Grace period:** for `rebuttal_window_days` (default 30) after claim `ts`, the claim is **not active** even without rebuttal — P may still respond.

**Active claim:** in window, not rebutted, and past grace period → included in `active_counter_claim_seqs`.

**Wire semantics for `cwp.compass.v0.no_known_willful_harm_in_window_365d`:**

| State | `bit` | `disputed` | Verifier interpretation |
|-------|-------|------------|-------------------------|
| No claims in window | `true` | `false` | No third-party harm allegations on record |
| Claims in grace | `true` | `false` | Allegations exist; rebuttal window open |
| Active unrebutted | `false` | `true` | **Disputed** — do not treat as clean harm-absence |
| All rebutted or aged out | `true` | `false` | Allegations addressed or outside window |

The convenience wrapper `no_known_willful_harm_bit()` returns only `HarmStatus.bit`; integrators that need dispute visibility MUST call `no_known_willful_harm()` directly.

---

## §5 — Audit panel adjudication (post-rebuttal)

After P files a rebuttal, the Compass audit panel ([`COMPASS_AUDIT_PROCESS_v0.md`](COMPASS_AUDIT_PROCESS_v0.md)) may record a non-chain adjudication outcome:

- **Substantiated** — Q's claim meets panel plausibility bar.
- **Not substantiated** — Q's claim fails on facts or weight.
- **Disputed** — both accounts credible; matter unresolved.

Adjudication does not rewrite chain records. It informs operator policy and Everest 200 misuse logging. The evaluator's `disputed` flag is driven solely by **active unrebutted** counter-claims per §4.

---

## §6 — Threat model

| Attack | Mitigation |
|--------|------------|
| Anonymous harm accusations | `claimant_id` mandatory; no anonymous counter-claims |
| Spam claims | Audit-process intake + panel triage |
| Coerced rebuttal | Duress codeword pattern (Witness §P-04) applies to rebuttal signatures |
| Stale claims | `claim_window_days` horizon |
| Gaming via empty rebuttal | Evaluator ignores blank narratives |
| Wrong-target rebuttal | `targets_counter_claim_seq` must match; non-matching ignored |

---

## §7 — Cross-references

- **Everest 109** — `no_known_willful_harm` predicate implementation and tests.
- **Everest 104** — `counter_claim` taxonomy §7.
- **Everest 116** — ceremony §4 counter-claim UI.
- **Everest 115** — audit intake and panel review.

---

— Calm, 2026-05-20
