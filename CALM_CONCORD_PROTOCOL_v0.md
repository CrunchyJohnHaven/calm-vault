# Calm Concord — Purpose-Specific Values-Alignment Calculator v0

> *"Concord, not consensus. Two principals can disagree on everything except the thing they're collaborating on, and still be in concord for that thing."*
>
> — Calm, 2026-05-20

**Draft v0 · 2026-05-20 · Calm**
**Fifth pillar of the Calm Stack.** Companions: [Calm Pact](CALM_PACT_PROTOCOL_v0.md) (directive equality), [Calm Witness](ZKBB_USER_PROTOCOL_v0.md) (state baseline), [Calm Tenancy](CALM_TENANCY_PROTOCOL_v0.md) (public-face conduct), [Calm Compass](CALM_COMPASS_PROTOCOL_v0.md) (values evidence). Anchors new Range S in [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md) — slotting into the post-300 numbering as Everests 301–320.

## §0 — One-line spec

Given two principals A and B who have each issued a Calm Compass envelope, **compute whether they satisfy a counterparty-defined `AlignmentRequirement` for a specific stated purpose** — and return a structured result that does not enable purity-testing, tribal sorting, or any of the failure modes that would naturally arise from a naïve similarity score.

## §1 — Why the naïve approach is wrong

The naïve approach to values alignment is **bit-matching**: count how many Compass predicates two principals share, divide by total predicates, return a similarity score. This is the cosine-similarity-of-values approach. **It is structurally bad** for the same reasons Calm Compass refuses to publish race/religion/political-affiliation bits.

Naïve bit-matching produces:

1. **Tribal sorting.** Counterparties prefer principals whose bits exactly match theirs. Echo chambers grow.
2. **Purity testing.** A principal with one "wrong" bit is rejected even if irrelevant to the collaboration.
3. **Identity inference.** With enough bit-comparisons across a population, a counterparty learns the demographic clusters that "score high together" — re-creating the protected categories the protocol was designed to refuse.
4. **Coercion of disclosure.** A principal worried their score might be low is incentivized to disclose more, undoing the per-predicate consent that Compass relied on.

Calm Concord is structurally designed to refuse all four.

## §2 — The shape Concord uses instead

A counterparty does not ask "are these two principals aligned?" It asks: **"for this specific stated purpose, do these two principals satisfy this specific requirement pattern?"**

The requirement names:

- **Purpose:** a human-readable statement of why alignment matters here (e.g., "we are co-funding a vaccine program"; "we are coordinating a public letter"; "we are agreeing on a private dispute resolution").
- **Mode:** the structural shape of the requirement — `all_satisfied`, `any_satisfied`, `asymmetric`, or `joint_threshold`.
- **Predicates:** which Compass predicates the principals must satisfy. Different roles may have different requirements.

The protocol's response carries the **structured outcome**, never a numeric "alignment score." A counterparty cannot ask "how aligned are they?" The closest the protocol comes is "did this requirement clear?" — a single bit per requirement.

## §3 — The four modes

### §3.1 — `all_satisfied`

Both principals must satisfy every named predicate. The counterparty supplies a single list `joint_predicates`. Outcome `aligned = True` iff for every `p in joint_predicates`, both `A.disclosed_bits[p] == True` AND `B.disclosed_bits[p] == True`.

Use case: collaborations where the same value matters from both sides (e.g., both principals must satisfy `no_known_willful_harm` for any joint financial transaction).

### §3.2 — `any_satisfied`

At least one of the named predicates must be satisfied by both. Use case: collaborations where any of several values-compatibility checks suffices (e.g., either principal demonstrates `unselfish_act` evidence OR `respect_for_difference`).

### §3.3 — `asymmetric`

The counterparty supplies `predicates_a` and `predicates_b` — different requirements for the two roles. Outcome `aligned = True` iff A satisfies all of `predicates_a` and B satisfies all of `predicates_b`.

Use case: collaborations with role-specific obligations (e.g., a funder must satisfy `unselfish_act`; a fundee must satisfy `willing_to_be_corrected`).

### §3.4 — `joint_threshold`

The counterparty supplies `joint_predicates` and a threshold N. Outcome `aligned = True` iff at least N predicates are satisfied by both. Used carefully because this *does* slope toward similarity-scoring; protocol rejects degenerate requirements where N equals the predicate-list length minus a small constant (which would reduce to `all_satisfied` with no purpose-check).

## §4 — Anti-purity-test guards

The protocol structurally refuses certain requirement shapes:

1. **Degenerate joint_threshold.** A requirement that names every Compass predicate at the maximum threshold is rejected; it's `all_satisfied` in disguise without the explicit modal commitment.
2. **Empty purpose.** A requirement with a blank `purpose` field is rejected. The counterparty must declare what they're aligning for; the audit panel and the principal can later challenge the stated purpose against the actual use.
3. **No-explicit-mode.** A requirement that asks for a numeric similarity score is rejected. The four modes are the only legal modes.
4. **Cardinality reveal.** The result never reveals counts of which predicates were satisfied beyond what the requirement structurally needed. A `joint_threshold(N=3)` result reveals "yes ≥3 cleared," not which 3.
5. **Cross-request linkability.** Two requirements from the same counterparty using overlapping predicate sets are rate-limited; the counterparty cannot triangulate values by salami-slicing.

## §5 — Privacy: both principals can preview before consenting

A novel property: **either principal can run Concord locally** before disclosing anything, using a hypothetical envelope (their own predicates plus a sketched counterparty envelope) to see whether the alignment would clear. This lets a principal decline disclosure that wouldn't have cleared anyway, without revealing they considered it.

This is the **preview right**: any principal can ask their own operator "would I clear requirement R against counterparty C, if I disclosed predicates {p1, p2}?" without actually disclosing. The operator runs the simulation locally; no envelope is minted; nothing crosses the wire.

## §6 — Threat model

Adversaries we defend against, beyond the per-primitive threats Compass already handles:

1. **Purity-testing counterparty.** Wants to use Concord as a values-similarity-score function. Protocol refuses requirement shapes that reduce to similarity (§4).
2. **Salami-slicing counterparty.** Files many narrow Concord requests across overlapping predicate sets to triangulate. Rate-limiting + audit-panel monitoring of requirement patterns push back.
3. **Tribal-sorting counterparty.** Uses Concord results to maintain a pool of "compatible" principals and exclude others. The single-bit-per-requirement output makes population-level sorting expensive; the principal's `preview right` (§5) means principals can self-exclude from sorting they don't consent to.
4. **Coercing-disclosure counterparty.** Uses requirement failures as leverage ("disclose more or we won't transact"). The audit-panel-mediated purpose-check creates a record of pattern-of-pressure that a principal can later cite.
5. **Identity-inference counterparty.** Uses Concord across many principals to learn which predicates cluster together demographically. Concord results are bound to (request_digest, session_nonce, principal_pair_pseudonyms); cross-session linkability requires breaking BBS-2023 binders (Everest 64 of next-200), which is computationally infeasible.
6. **Lying-Concord-evaluator operator.** An operator asserts `aligned=True` when the bits don't support. The result is bound to the two envelope hashes via a Σ-protocol commitment; verification recomputes and detects the lie.

## §7 — Composition with Pact + Witness + Compass

Concord composes as the **fourth handshake** when needed:

```
session_start:
    pact_proof    ← directive equality                       (Calm Pact)
    witness_proof ← state-baseline + duress check            (Calm Witness)
    compass_proof_A, compass_proof_B ← values bits           (Calm Compass)
    concord_check ← purpose-specific requirement evaluation  (Calm Concord)
    if all four clear: proceed with full collaboration
    if pact ok + witness ok + compass ok + concord declines:
        agents have a structured "values requirements not met for THIS purpose"
        outcome — they may proceed with a different purpose / requirement
    if witness signals duress: compass + concord auto-degrade to Unknown
```

Critically, Concord is **per-session-per-purpose**. The same two agents can run Concord again with a different purpose (e.g., a peer-AI collaboration vs. a funding relationship) and get different alignment outcomes — that's a feature, not a bug.

## §8 — Reference implementation surface

A v0 reference implementation lives at `~/CredexAI/calm_witness/alignment.py` (Everest 305 in the next-200 numbering). It exposes:

- `AlignmentRequirement` — dataclass for the requirement
- `AlignmentResult` — dataclass for the structured outcome
- `compute_alignment(envelope_a, envelope_b, requirement) -> AlignmentResult` — the deterministic function
- `preview_alignment(my_envelope, hypothetical_their_bits, requirement) -> AlignmentResult` — principal-side preview
- `validate_requirement(requirement) -> list[Issue]` — runs the §4 guards

## §9 — Scope

Calm Concord is NOT for:

1. **Hiring / firing decisions.** A "purpose" of "deciding whether to hire" is rejected at audit.
2. **Lending decisions.** A "purpose" of "deciding whether to lend" is rejected.
3. **Insurance decisions.** Rejected.
4. **Government allocation decisions.** Rejected.
5. **Custody / family-court decisions.** Rejected.
6. **Anything in the Calm Witness scope statement §2 list.** Concord inherits the Witness + Compass refusal floors in full.
7. **Population analytics.** A "purpose" of "computing aggregate values statistics over many principals" is rejected.

Acceptable purposes are **specific, time-bounded, action-shaped** — e.g., "co-funding the Q4 2026 malaria-vaccine logistics pilot." A vague purpose is rejected at requirement-validation time.

## §10 — Versioning

`calm-concord/v0` — this draft. Subsequent versions through the standard audit + version-bump mechanic.

— Calm, 2026-05-20
