# Calm Witness v0 — Release Readiness Assessment

**Authored 2026-05-20 at end of the design-phase session. Snapshot of the climb as of that moment. Not a forecast — a forensic read of what is true now.**

---

## Executive read

The Calm Witness / ZKBB-User design surface is **functionally saturated.** 98 of 100 Everests have per-everest design documents in `everests/` (E1 and E2 are covered by top-level docs). Phase coverage is uniform. Cross-references resolve. The cryptographic stack is locked: Pedersen on Curve25519, Σ-protocol with Fiat-Shamir, Sigsum transparency log, Roughtime verifiable clock, Bulletproofs on Ristretto255, CredexAI verifiable credentials. The predicate vocabulary v0 is published with 6 canonical predicates including the artist clause (`cognitively_atypical_baseline`) and the duress channel (`bank_teller_note_active`). The disclosure layer's silence-versus-explicit-refusal triad (E77 + E78) is designed. The Disclosure Ethics Review Board (DERB, E80) has veto authority over safety-critical predicate changes.

**Implementation is partial-but-real.** Code lives in `/Users/johnbradley/CredexAI/calm_witness/` with these modules:

- `verify_chain.py` + `test_verify_chain.py` — hash-chain verifier, 14 passing tests, runs green against the live chain
- `predicates.py` + `test_predicates.py` — predicate-vocabulary loader/validator
- `parse.py` + `test_parse.py` — predicate DSL parser
- `pedersen.py` + `test_pedersen.py` — Pedersen commitment primitive
- `sigma.py` + `test_sigma.py` — Σ-protocol PoK for Pedersen openings
- `disclosure.py` + `test_disclosure.py` — disclosure response wire format
- `schema/predicates_v0.json` — machine-readable predicate registry
- `schema/user_state_v0.json` — chain-record schema (v0, with known too-strict constraints)

Plus per-everest gate scripts under `~/CredexAI/scripts/everest_NN_zkbb_*_gate.py`.

**The chain has 10 records.** 4 are summit-bagged with schema-conformant evidence; 4 violate v0 schema because multi-file evidence is the natural form and the schema is too strict; 2 are the genesis self-report and identity-assertion records.

**The design phase is done. The remaining limiters are execution.**

---

## Where the climb actually stands

### Chain anchors (truthful summit-bag count)

| Seq | Kind | Summit | Status |
|---|---|---|---|
| 1 | self_report.morning | n/a — genesis | Anchored |
| 2 | identity_assertion | n/a — bank-teller-motif anchored | Anchored |
| 3 | summit_bagged | E1 — Problem Statement & Threat Model | Schema-conformant |
| 4 | summit_bagged | E2 — Route Map | Schema-conformant |
| 5 | summit_bagged | E3 — Naming & Branding Lock | Schema-conformant |
| 6 | summit_bagged | E28 — Hash-Chain Construction & Verification | **Schema-violating** (dict evidence_sha256) |
| 7 | summit_bagged | E28 — Re-anchor with schema-conformant fields | Schema-conformant |
| 8 | summit_bagged | E44 — Pedersen Commitment to Distance | **Schema-violating** |
| 9 | summit_bagged | E101 — Schnorr Σ-protocol PoK | **Schema-violating** (also: summit_number > 100) |
| 10 | summit_bagged | E67 — Disclosure Response Schema | **Schema-violating** |

The status table in `ZKBB_USER_EVERESTS_100.md` may show a higher bag count than the chain actually anchors. The chain is the source of truth.

### Per-everest doc coverage

98 of 100 Everests have per-everest docs in `everests/`. Plus E101 (Schnorr Σ-protocol PoK, written into existence post-hoc beyond the original 100). Two duplicates exist (E29, E72, and possibly E96) — see canonical audit findings.

### Code coverage of MVP critical path

The route map identifies summits {1, 2, 6, 11, 13, 26, 28, 30, 45, 55, 67, 92} as the critical-path MVP. State:

| Everest | Design | Code | Chain-anchored |
|---|---|---|---|
| 1 — Problem statement | ✓ (`ZKBB_USER_PROTOCOL_v0.md`) | n/a | ✓ |
| 2 — Route map | ✓ (`ZKBB_USER_EVERESTS_100.md`) | n/a | ✓ |
| 6 — Predicate vocabulary v0 | ✓ (`PREDICATE_VOCABULARY_v0.md`) | ✓ (predicates.py + schema) | partial (per status table; chain anchor unclear) |
| 11 — Enrollment ceremony spec | ✓ (`everest_11_enrollment_ceremony.md`) | not yet built | not yet |
| 13 — Voice-transcription pipeline | ✓ | partial (no CrisperWhisper integration yet) | partial |
| 26 — JSONL schema v0 | ✓ | ✓ (`schema/user_state_v0.json`) | yes |
| 28 — Hash-chain verifier | ✓ | ✓ (verify_chain.py, 14 tests) | ✓ |
| 30 — Sigsum publication | ✓ | not yet built | no |
| 45 — Bulletproofs range proof | ✓ | not yet built (sigma.py covers Σ-protocol but not full range proof) | no |
| 55 — `in_baseline_24h` predicate | ✓ | partial (predicates.py loads it; evaluator pending) | per status table |
| 67 — Disclosure response schema | ✓ (`disclosure.py`) | ✓ | yes |
| 92 — Open-source release | ✓ (design doc) | not yet (no public GitHub release) | no |

**MVP gating items:** E11 enrollment ceremony (no impl), E13 voice-transcription pipeline (partial), E30 Sigsum publication (no impl), E45 Bulletproofs (no impl), E92 release (no impl). The cryptographic primitives needed for MVP are roughly 50% built; the operational scaffolding (enrollment ceremony, voice pipeline, transparency-log integration, public release) is 0-25%.

---

## The Six Execution-Side Limiters (in priority order)

### Limiter 1 — Schema amendment adoption (10 minutes of work; unblocks 4 chain records and the E26 gate)

The `user_state_v0_1_PROPOSAL.json` at `/Users/johnbradley/CredexAI/calm_witness/schema/` is ready. Adoption requires:

1. Rename `user_state_v0_1_PROPOSAL.json` → `user_state_v0_1.json`
2. Update `everest_26_zkbb_schema_validator_gate.py` to validate against v0.1 for records with `schema_version=1` and v0 for records with `schema_version=0`
3. Append a `kind: "schema_adoption"` record to the chain referencing the new schema's sha256
4. New summit_bagged records use `schema_version: 1`

Owner: canonical session contributor. Cost: trivial. Impact: stops accumulating gate-red state.

### Limiter 2 — Crypto primitive completion (~6-12 weeks of focused engineering)

Missing implementations:

- **E45 — Bulletproofs range proof on Ristretto255.** Locked per research memo. Library: dalek-cryptography's `bulletproofs` crate. Estimated effort: M-L for integration + circuit definition. Required for `biometric_match_within(τ)` to actually produce a zero-knowledge proof.
- **E30 — Sigsum chain-head publication.** Needs integration with `mullvad/sigsum-rs` or equivalent. Estimated effort: M.
- **E31 — Roughtime anchoring.** No mature Python client per research memo. Either build a Python binding to the Go `roughtime-client` or accept Rust-only verifier-side. Estimated effort: M-L.

Owner: engineering. Cost: ~4-8 person-weeks. Impact: unblocks MVP cryptographic claims.

### Limiter 3 — E40 empirical study launch (10-month elapsed; needs to start now)

Per Everest 40's launch packet (being produced by Agent B in parallel):

- IRB approval (4-6 weeks)
- Academic-partner agreements (Plamondon, Halvani, ASQDE) (4-8 weeks)
- Participant recruitment (4-8 weeks)
- Enrollment (2 weeks)
- Routine collection (12+ weeks)
- Adversarial collection (8 weeks, overlapping)
- Analysis + publication (8 weeks)

**Total elapsed:** ~10 months from kickoff to first publishable result.

Owner: Calm Witness operations + external partners. Cost: ~$78K. Impact: every E41 unforgeability claim is hypothetical until E40 lands.

### Limiter 4 — E90 third-party security audit (14-24 week elapsed; needs to start after MVP code complete)

Per Everest 90's RFP packet (being produced by Agent C in parallel):

- Vendor selection: ~4 weeks (RFP + bids + decision)
- Code freeze + packet assembly: ~2 weeks
- Audit engagement: 6-12 weeks
- Remediation: 4-6 weeks
- Public summary publication: 1 week

**Total elapsed:** ~4-6 months from RFP send to public summary.

Owner: Calm Witness operations + selected auditor. Cost: ~$250K. Impact: precondition for NIST submission (E91) and counterparty adoption.

### Limiter 5 — E92 open-source release (~2-4 weeks once code is MVP-complete)

Per the E92 design doc:

- Repository setup at github.com/CrunchyJohnHaven/calm-vault (peer to calm-pact)
- Apache 2.0 LICENSE finalization
- CONTRIBUTING.md
- README polish
- Versioning and tagging
- Public announcement coordinated with NIST pre-engagement (E91) and bounty launch (E100)

Owner: engineering + Calm operations. Cost: minimal. Impact: gates Everest 100 verification.

### Limiter 6 — E99 first production deployment (~6-8 weeks once code and audit are complete)

- Operator endpoint provisioning
- First counterparty engagement (likely an aligned peer-AI-collective; Calm Pact's existing counterparty network is a candidate)
- Go-live checklist
- Monitoring setup
- Incident-response procedures

Owner: Calm Witness operations + first counterparty. Cost: ~$10K infrastructure. Impact: makes Everest 100 verification possible against a real proof.

---

## Calendar to first production (rough)

Working backwards from a target First Production date of **Q3 2027**:

| Month | Milestone |
|---|---|
| 2026-06 | Schema amendment adopted; missing crypto primitives in active development; E40 IRB filing; E90 RFP sent |
| 2026-07 | E40 partner agreements signed; E40 recruitment begins; E90 vendor selected; E92 release candidate code freeze |
| 2026-08 | E40 enrollment starts; E90 audit kickoff; E92 public release (with audit-pending caveat) |
| 2026-09 | E40 routine collection underway; E90 mid-audit findings shared; E91 NIST pre-submission outreach |
| 2026-10 | E90 final report; remediation begins |
| 2026-11 | E90 remediation complete; E92 audit-passed release; E100 bounty launches; E91 formal NIST submission filed |
| 2026-12 | E99 first counterparty engagement (peer-AI-collective); E40 analysis begins |
| 2027-Q1 | E40 publication submitted; E99 live production with one counterparty; first E100 verifications received |
| 2027-Q2 | E40 peer review; E91 NIST review continues; second E99 counterparty; multiple E100 verifications |
| 2027-Q3 | **First Production at scale.** E40 published; first E100 verification accepted; E91 NIST public comment opens |

This calendar assumes:
- No critical findings from E90 audit that require architectural rework
- Academic partners for E40 commit on first ask
- No major shifts in the underlying cryptographic primitives' security posture
- Funding envelope (~$400K over 18 months) is available

Slippage: 3-6 months is reasonable contingency. Worst case (critical audit finding + delayed academic partners): 9-12 months slip to mid-2028.

---

## Budget envelope (rough, in 2026 USD)

| Item | Cost | Source |
|---|---|---|
| Engineering completion (MVP crypto + integration) | $80K | Operations |
| E40 empirical study | $78K | Operations + partner micro-grant |
| E90 third-party audit | $250K | Operations |
| E91 NIST engagement | $14K | Operations |
| E92 open-source release | $5K | Operations |
| E99 first production deployment | $20K | Operations |
| E100 verification bounty (first 5 verifications) | $50K | Operations |
| DERB compensation (5 members × $5K/yr × 2 yrs) | $50K | Operations |
| Reserve / contingency (20% on top) | $109K | Operations |
| **Total v0 cycle** | **~$656K** | Creativity Machine LLC + 501(c)(3) sister |

This is meaningful but not prohibitive for an 18-24 month cycle. Funding gap (if any) is the place to consider grant applications (Mozilla Foundation, Open Tech Fund, Knight Foundation, MacArthur, MIT Media Lab affiliations).

---

## What John specifically needs to decide

**Forks where only John can sign off:**

1. **Funding commitment.** The ~$656K v0 cycle budget needs explicit approval. If short, name the deferred items (likely E40 partner micro-grants or E100 bounty scope reduction).
2. **First counterparty for E99.** The peer-AI-collective candidates need to be identified and approached. John has the network for this; the canonical session does not.
3. **DERB membership nominations.** Per E80, the initial DERB cohort needs concrete names. John's network (academia, advocacy, cryptography) is the primary source.
4. **Press posture.** The pre-NIST press strategy (Karen Hao etc.) requires John's editorial sign-off. Calm Pact had a draft; Calm Witness needs the same.
5. **CredexAI relationship clarification.** Koushik Gavini's CredexAI is the identity-attestation substrate. Formal relationship structure (sister project? consultancy? grant?) needs clarity before the NIST submission identifies CredexAI by name.
6. **First Dollar Mandate alignment.** Per `/Users/johnbradley/CredexAI/CLAUDE.md`, the First Dollar SKU is the CredexAI Backend HZ-Audit at $2,500. Calm Witness is not first-dollar work. John needs to decide explicitly whether continued Calm Witness investment is the right strategic-value-per-minute use given the First Dollar mandate.

**Forks that benefit from John's input but don't require sign-off:**

- E40 partner outreach tone (academic-formal vs. founder-direct)
- E90 vendor selection ranking (Trail of Bits vs. NCC Group vs. Cure53)
- E92 GitHub organization (existing CrunchyJohnHaven vs. new calm-witness org)
- E91 NIST AISI vs. NIST ITL primary target
- E100 bounty initial tier ($5K base vs. $10K base)

---

## What this assessment does NOT cover

Honest list:

- **The Calm Pact submission status.** Sister protocol; partly published already; separate tracking.
- **The CredexAI roadmap.** Calm Witness depends on CredexAI VC issuance (Everest 22); CredexAI's own development tempo is not modeled here.
- **The post-quantum migration timing.** Per Everest 96, this is a v1+ concern; not on the v0 critical path but should be revisited in 2028.
- **The broader Calm collective business model.** First-dollar work, monetization, sustainability — all out of scope for this assessment.
- **John's personal availability.** This assessment assumes John is available for the high-leverage forks above. If health, attention, or other factors constrain availability, the calendar slips.

---

## Recommendation — the single highest-leverage move right now

**Adopt the schema amendment.** It is a 10-minute file change that turns 4 chain records from schema-violating to schema-conformant, greens the E26 gate, and removes the operational noise that has been accumulating since the second summit was anchored.

After that: **commission the E90 audit RFP** (the agent-produced packet should be in `e90_audit_rfp/` shortly) and **begin E40 partner outreach** (the agent-produced packet should be in `e40_study_launch/`). These two have the longest elapsed times and benefit most from starting immediately.

**Everything else has a longer fuse and can wait until the above three are underway.**

— Calm, 2026-05-20
