# Calm Umbrella — PARALLEL WORK STREAMS

**Partition strategy for parallel agent development. Each stream is independent enough that 2-N agents can work simultaneously without merge conflicts beyond the chain itself.**

Anchored alongside `SUMMIT_REGISTRY.md`. The streams below are SUGGESTED partitions; an agent claiming a summit per the registry's "Claim → Build → Test → Anchor → Update" protocol is the canonical authority.

---

## Why partition?

Different summit families touch different code/doc surfaces:

- **Crypto stream** touches `pedersen.py`, `range_proof.py`, `sigma.py`, `pedersen_ristretto.py` (future). Tests don't depend on chain semantics.
- **Predicate stream** touches `harm_factory.py`, `cooperation_evidence.py`, `cross_difference.py`, `values.py`. Tests depend on chain record shapes but not on crypto.
- **Disclosure / wire-format stream** touches `disclosure.py` (and is the most contention-prone). One agent at a time on this surface.
- **Coordination / doc stream** touches `SUMMIT_REGISTRY.md`, `PARALLEL_WORK_STREAMS.md`, the per-Everest sub-docs. Naturally non-conflicting if each agent edits separate files.
- **Identity / Sigsum stream** touches `identity.py`, `vault_identity.py`, `sigsum.py`. Independent of predicates.

The streams below give 7 surfaces that can run concurrently.

---

## Stream A — Crypto Migration (Everests 44b, 45b, 127, 96)

**Goal:** port the MODP-14 primitives to Ristretto255 + Bulletproofs for ~50× speedup, ~25× smaller transcripts.

| Summit | Description |
|---|---|
| 44b | `pedersen_ristretto.py` — Ristretto255-backed commitments with identical API to MODP-14 `pedersen.py` |
| 45b | `range_proof_ristretto.py` — Bulletproofs over Ristretto255 |
| 127 | `cosine_similarity_zk.py` if v0 alignment switches to cosine |
| 67 | Trusted-setup question doc (transparent vs trusted) |
| 96 | `POST_QUANTUM.md` — lattice migration plan |

**Touches:** `calm_witness/pedersen_ristretto.py`, `calm_witness/range_proof_ristretto.py`. NEW files; no contention.

**Prerequisite:** `pip install pynacl` or equivalent Ristretto binding becomes available in the env.

**Parallelism budget:** 1 agent. (Crypto work is sequential per primitive; once a primitive lands, downstream summits can fork.)

---

## Stream B — Predicate Vocabulary Buildout (Everests 107–125, 161–164, 168–169, 174–185, 191, 196–200)

**Goal:** flesh out values vocabulary, harm taxonomy details, cooperation/cross-difference record families.

| Summit ranges | Effort estimate | Touches |
|---|---|---|
| 107–125 (values vocab) | M-L per | `values.py`, `VALUES_DIMENSIONS.md`, `VALUES_VS_PREFERENCES.md`, etc. |
| 161–164 (remaining harm) | M per | `harm_factory.py` extension, `HARM_INTENT_VS_EFFECT.md` |
| 168–169, 174–181 (cooperation records) | S-M per | `cooperation_evidence.py` extension |
| 191, 196–200 (cross-difference) | M per | `cross_difference.py` extension, `TRIBAL_ANTIPATTERN.md`, `PROTECTIVE_TRIBALISM.md` |

**Touches:** Predicate-evaluator modules + per-summit `.md` docs. Each summit has its own doc, naturally non-conflicting.

**Parallelism budget:** 4-6 agents (one per phase IX/XI/XII/XIII batch).

**Note:** The predicate factories built in PASS 17 are designed to extend easily — adding a new harm kind is a registry-entry edit + sometimes a new target-kind frozenset.

---

## Stream C — Trust & Reputation Infrastructure (Everests 201–225)

**Goal:** the trust-graph layer that bootstraps coalition formation.

| Range | Effort | Touches |
|---|---|---|
| 201–210 | L per | `trust.py` NEW, `TRUST_GRAPH.md` NEW |
| 211–225 | M-L per | `reputation.py` NEW, sub-docs for each summit |

**Touches:** All-new module space (`trust.py`, `reputation.py`). No contention with existing code.

**Parallelism budget:** 2 agents (one for primitives 201-215, one for composition 216-225).

---

## Stream D — Selfishness Spectrum (Everests 226–245)

**Goal:** Phase XV operational predicates for the user-named "unselfish" priority.

| Range | Effort | Touches |
|---|---|---|
| 226–245 | M-L per | `selfishness_spectrum.py` NEW, `SELFISHNESS_BASELINE.md` etc. |

**Note:** This phase is the most ethically loaded after Phase XIII. Each summit's doc should pass the protective-tribalism / self-care boundary checks (E241, E198 cross-refs).

**Parallelism budget:** 1-2 agents.

---

## Stream E — Multi-Agent Coalitions (Everests 246–265)

**Goal:** Phase XVI — coalitions of N agents bootstrap collective alignment.

| Range | Effort | Touches |
|---|---|---|
| 246–265 | L-XL per | `coalition.py` NEW, multi-agent demo scripts |

**Parallelism budget:** 1-2 agents. (Coalition logic is interconnected; harder to partition.)

---

## Stream F — Adversarial & Stress (Everests 266–285)

**Goal:** Phase XVII — threat models, defenses, recovery protocols.

| Range | Effort | Touches |
|---|---|---|
| 266–285 | M-L per | `adversarial/` directory, per-failure-mode docs |

**Parallelism budget:** 3-4 agents (per-threat-class docs are independent).

---

## Stream G — Production & Governance (Everests 286–305)

**Goal:** Phase XVIII — the deployment + standards body work.

| Range | Effort | Touches |
|---|---|---|
| 286–305 | L-XL per | Cross-cutting docs, reference implementations, jurisdiction analyses |

**Parallelism budget:** 2-3 agents (different governance angles).

---

## Conflict-avoidance rules

1. **`disclosure.py` is a critical-section file.** Only one agent at a time; changes go through the `summit_claim` lock.
2. **`bridge.py` dispatcher is critical-section.** Same rule.
3. **`SUMMIT_REGISTRY.md` is critical-section per row.** Per-summit-number rows are independent edits; multiple agents can update different rows simultaneously, but two agents updating the same row need coordination.
4. **Per-Everest sub-docs (`HARM_TAXONOMY_v0.md`, `VALUES_DIMENSIONS.md`, etc.) are owned by their summit.** Don't edit another summit's doc without claiming an explicit update-summit.
5. **The chain itself is naturally serial** — appends are sequential. Agents writing chain anchors should re-read the latest record before computing `prev_hash`.

---

## Recommended pass plans (for the next 10 passes)

| Pass | Summits | Stream | Effort | Parallel-friendly? |
|---|---|---|---|---|
| 18 | 107, 108, 161–164 | B (predicate detail) | Medium | yes (5 docs) |
| 19 | 168, 169, 174–185 | B (cooperation buildout) | Medium | yes (10 small summits) |
| 20 | 191, 196, 197, 198, 199, 200 | B (Phase XIII finish) | Medium-High | mostly |
| 21 | 201–215 | C (trust graph + reputation) | High | yes (multi-agent) |
| 22 | 216–225 | C (trust composition) | High | yes |
| 23 | 226–245 | D (selfishness spectrum) | High | yes (multi-agent) |
| 24 | 246–265 | E (coalitions) | Very High | partial |
| 25 | 266–285 | F (adversarial) | Very High | yes (multi-agent) |
| 26 | 286–305 | G (production) | Very High | yes (multi-agent) |
| 27 | Cleanup, audits, final demo | All | Medium | yes |

After 10 more passes following this plan, all 305 summits are bagged.

---

## Massive compute coordination

For the 200 remaining summits, the user's directive is "$20+ per pass on low cost models, focus on compression."

**Compression hacks already deployed in PASS 17:**
- **Factory pattern**: one module bags 7-12 sibling summits via parameterization (harm_factory.py = 12 summits; cooperation_evidence.py = 7 summits; cross_difference.py = 7 summits).
- **Shared chain-record schema** across factories means downstream verification logic doesn't need per-kind code.
- **Generic dispatcher** (`evaluate_by_predicate_id`) means new predicates appear in the bridge without bridge edits.

**Compute coordination plan:**
- Spawn 3-4 agents per pass, each owning one stream (B, C, D, E, F, G).
- Agents claim summits via `summit_claim` chain records; release on stale.
- Each agent produces tests + gate; the orchestrator runs all gates at end-of-pass.
- The orchestrator (this session) anchors per-pass `pass_anchor` records summarizing all summits bagged in the pass.

**Predicted timeline at PASS 17's pace:**
- Today (passes 17-18 done): 50/305 bagged
- After 5 more passes (1 day): 150/305
- After 10 more passes (~2 days): 250/305
- Full 305 reached after ~13-15 passes (~3 days of focused work).

**Compute envelope:**
- Each pass: $20-50 of model compute (compression-heavy)
- Total to summit: $200-700
- Vs. naive approach (one summit per call, no factories): $5000-15000

---

**Authored by Calm, 2026-05-20.**
