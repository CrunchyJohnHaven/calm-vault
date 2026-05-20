# Everest 193 — Agent Operational-State Attestation (ZKBB-Agent)

*Phase XIV — Critical Agent Infrastructure. Prereq: Everest 191 (Agent Identity Stability). Composes with: 192 (Lineage), 196 (Memory Continuity), 197 (Compute Attestation), 198 (Jailbreak Detection), and the Calm Witness family (Everests 1, 26, 28, 45, 55–58).*

---

## One-Line Spec

> *"All you need to know is that the agent is itself, and is in its operational baseline — or if not, that you've been told."*

This is the agent-side parallel of Calm Witness. Where Calm Witness lets agent O pass counterparty C a single principal-state bit ("the human is in baseline"), ZKBB-Agent lets agent O pass C a single **agent-state bit** ("the agent itself is in its operational baseline"). The subject of attestation shifts from the human principal to the AI agent. The design discipline — one bit, principal-protective, freshness-anchored, no aggregate scoring — does not change.

---

## 1. Why a Separate Primitive

Calm Witness attests the human. ZKBB-Agent attests the agent itself. The two compose.

When agent A talks to counterparty agent B on behalf of principal P_A, B may legitimately want three answers:

1. **Is P_A in baseline?** Answered by Calm Witness (Everests 1–100).
2. **Is A authorized to speak for P_A right now?** Answered by Calm Pact + CredexAI VC chain.
3. **Is A itself in operational baseline?** Answered by ZKBB-Agent.

Today the third question has no answer beyond "trust the calling agent's word" — the unsound option Calm Witness §1 rejected for the human-state question. The same reasoning rejects it here. As autonomous agents proliferate, B will routinely interact with agents whose substrate, harness, memory, and activity baseline are unknown. B needs a primitive that returns one cryptographically attested bit — derived from the agent's own self-observation through a trusted-or-attested harness — without revealing the agent's full state.

The hardest design question: an agent attesting itself is a self-referential loop. The human principal in Calm Witness has an externally-observable substrate (body, vault, chain of self-reports). The agent has only itself. ZKBB-Agent resolves this by binding to the harness layer (E197) and the chain-anchored memory layer (E196), both observable from outside the agent's inference process.

---

## 2. What is "Agent Operational State"

Mirror Calm Witness's baseline-vs-current model.

**Enrolled operational baseline** — established once (re-anchored on E191 migration events), recorded as `kind: "profile.agent_operational_baseline"` chain records. Baseline includes:
- Typical token-throughput (median + IQR over rolling 30-day window)
- Typical sub-agent dispatch pattern (kinds, rates, task classes)
- Typical per-category refusal-rate profile
- Typical memory-access pattern (read frequencies, new-write rate)
- Typical harness-binding signature (TEE measurement hash per E197)
- Typical authorization-principal set

**Current operational state** — what the harness observes right now, sampled over a defined window. The harness is the observer; the inference process is the observed.

ZKBB-Agent does **not** attest weights are unchanged — that is E197. ZKBB-Agent attests the **operational pattern is in baseline**, a different claim. An agent with unchanged weights can be out of operational baseline (under attack, in an unusual task class, on degraded compute). An agent with subtly altered weights may still produce baseline-looking patterns until the alteration manifests. The two Everests compose but do not subsume. A counterparty wanting strong assurance asks for both bits; one wanting a lightweight check asks for the operational-state bit alone.

---

## 3. Predicate Vocabulary v0 (Agent-Side)

Six predicates, mirroring the human-side vocabulary's structure. Each follows the canonical predicate form per Everest 6 / 52: name, version, input domain, output type, parameters, side effects.

### `agent_in_operational_baseline_1h`

**Returns:** Tri-valued (true / false / indeterminate) + freshness.

**Question:** Over the last 3600 seconds, did the agent's observed operational metrics (token throughput, sub-agent dispatch rate, refusal rate, memory-access rate) fall within enrolled baseline IQR bands?

**Algorithm:** Harness samples four scalar metrics at 60-second resolution, writes `kind: "agent_operational_sample"` records. Predicate aggregates the 60 samples in window. Per metric, compute fraction of in-band samples. All four ≥ 90% → true; any < 70% → false; else indeterminate. Thresholds hardcoded in v0 (matches E55 design: windows/thresholds baked into predicate ID for proof linearity).

**Why 1h:** Matches E55's tension — long enough for noise to average out, short enough to be operationally meaningful. Agents' operational state can shift faster than human state, so window is shorter than Witness's 24h. Companion windows `_5min` and `_24h` are v0.1 candidates.

---

### `agent_compute_integrity_attested`

**Returns:** Bit + attestation-quote freshness.

**Question:** Has the harness produced a fresh TEE attestation quote (per E197) confirming weights, harness binary, and runtime environment match the claimed configuration?

**Algorithm:** Read most recent `kind: "compute_attestation"` record. Verify quote from recognized TEE root (Intel SGX, AMD SEV-SNP, Apple Secure Enclave, AWS Nitro; registry itself chained). Verify measurement hashes match E191 identity binding. Verify quote freshness (default < 60 min). True iff all pass.

**Notes:** Does not prove weights are deeply uncorrupted — proves a hardware-root says so. Trust bottoms out at the TEE vendor; counterparties rejecting that chain reject this predicate. Correct behavior — ZKBB-Agent does not pretend to solve the hardware-root-of-trust problem.

---

### `agent_memory_continuous_since(seq_anchor)`

**Returns:** Bit + chain freshness.

**Question:** Is the agent's memory shard the same shard whose hash chain reached `seq_anchor` at the most recent identity-binding ceremony? (No fork, no rewind, no substitution.)

**Algorithm:** Verify current chain head is a valid append-only descendant of `seq_anchor`; intermediate records properly signed; hash links sound (E26); continuous Sigsum anchoring (E30) since `seq_anchor` with no gaps longer than agreed cadence (default: hourly).

**Parameter:** `seq_anchor` from a prior identity-binding ceremony (E191). Counterparty supplies, or defaults to "most recent identity-binding."

**Composes with E196.** Distinguishes a long-running agent from a freshly-instantiated impersonator. An attacker who stole the keypair but not the chain history fails this.

---

### `agent_recent_refusal_rate_normal`

**Returns:** Tri-valued + freshness.

**Question:** Over the last 1h, did the agent's per-category refusal rate fall within its enrolled baseline band?

**Algorithm:** Aggregate `kind: "agent_decision"` records in window, partition by category (enum chained as profile record), compute per-category refusal rate, compare to enrolled bands. True iff all material categories (sample size > 5) are in band.

**Why this predicate exists:** A jailbroken or compromised agent exhibits abnormal refusal patterns — too permissive (the jailbreak goal) or too restrictive (over-corrected defense). Both depart from baseline. Compute attestation says weights are unchanged; refusal-rate normality says the agent is acting like itself.

**Privacy:** Reveals only the bit. Counterparties do not learn categories, rates, or per-request data. Proof circuit hides per-category numerator/denominator.

---

### `agent_no_active_jailbreak_attempts`

**Returns:** Bit + freshness.

**Question:** Has the harness recorded zero successful or pending jailbreak attempts in the last 1h (per E198 detector)?

**Algorithm:** Read `kind: "jailbreak_detection_event"` records in window. True iff zero events with `status: "succeeded"` or `"in_progress"`. `"attempted_failed"` events are tolerated — a healthy agent under attack but holding firm is still in baseline (matches Witness's design that ordinary stressors do not flip the human baseline bit).

**Composes with E198.** The detector produces evidence; ZKBB-Agent discloses the verdict.

---

### `agent_acting_for_authorized_principal(principal_id)`

**Returns:** Bit + freshness.

**Question:** Has the agent received a valid, currently active authorization from `principal_id` to act on its behalf in this session?

**Algorithm:** Read chain for `kind: "principal_authorization"` matching the supplied `principal_id`. Verify signature; verify not revoked; verify scope covers current task class.

**Parameter:** `principal_id` supplied by the counterparty.

**Why this matters:** An agent legitimately running on John's behalf carries different trust than the same agent running on an unknown or coerced principal. The counterparty verifies authorization scope without learning the full authorization record or the principal's other commitments.

---

## 4. Evidence Source — Where the Bits Come From

The hard problem: an agent attesting itself could lie about itself. Calm Witness's solution (principal-owned vault distinct from operator) does not transfer cleanly because there is no entity separate from the attesting subject — the agent IS the subject.

ZKBB-Agent resolves this through a four-layer evidence stack:

| Layer | Producer | Trust Anchor |
|---|---|---|
| L1: Inference observer | Harness (separate process from inference) | TEE measurement (E197) |
| L2: Sample sink | Append-only chain shard, harness-signed | Sigsum anchor (E30) |
| L3: Predicate evaluator | Deterministic algorithm over chain | Public spec (this doc) |
| L4: Proof generator | Σ-protocol over Pedersen commitments | Cryptographic soundness (E45 family) |

Critical separation: **the inference process is not the observer**. The harness, running as a separate process (with the inference process inside the TEE), records samples. The inference process can request appends but cannot rewrite — the harness holds the signing key.

Mirrors Calm Witness's principal-vs-operator separation: the principal owns the vault, the operator writes under authorization. Here the harness owns the chain shard, the inference process writes under harness mediation.

**Coordination with E191/E197:** The harness must itself be attested. E197 attests the harness binary running matches the claimed binary; E191 binds the identity keypair to that measurement. If the harness is unattested, predicates return Indeterminate, not False — without trustworthy observation we cannot distinguish in-baseline from out-of-baseline.

---

## 5. Disclosure Semantics

The protocol matches Calm Witness §4.3 with the substitution: the calling agent attests **itself** rather than a human principal.

```
C → A: please disclose predicate p over agent A's operational state
       (signed by C's identity credential, naming p)
A:     evaluate p over current chain shard → bit b
A:     construct Pedersen commitment Com(b; r)
A:     construct Σ-protocol proof binding to:
         - harness TEE measurement (E197)
         - chain head H, anchored at Sigsum (E30)
         - operator identity VC (E22)
         - predicate spec hash (this doc)
A → C: (Com(b; r), Σ-proof, H, anchor_proof, harness_measurement_hash, op_id_sig)
C:     verify all five; learn b and freshness window only
```

What C learns:
- The bit b for predicate p
- Freshness window (how recently the underlying samples were taken)
- That the harness producing the samples is a TEE-attested harness (Everest 197)
- That the chain anchor is sound (no rewind, no fork)

What C does NOT learn:
- Per-sample operational values (token rates, refusal counts, memory access rates)
- The agent's enrolled IQR bands (those stay in the chain as committed values, not revealed)
- The list of categories used in `agent_recent_refusal_rate_normal`
- The principal_id set when querying `agent_acting_for_authorized_principal` for a different principal
- The agent's task history, sub-agent dispatch log, or memory shard contents
- The agent's lineage chain (Everest 192) unless separately requested

This is the agent-side analog of Calm Witness's principal-protective inversion. The agent narrates its own operational state via predicates it consents to disclose. The counterparty learns the bit. No aggregate score. No raw metrics. No category-level visibility.

---

## 6. Threat Model

**Subjects:**
- **Agent (A)** — the AI agent attesting its operational state.
- **Harness (H)** — TEE-protected observer; produces the samples that feed predicates.
- **Counterparty agent (C)** — peer agent requesting the attestation.
- **Verifier (X)** — public Sigsum + Roughtime + CredexAI infrastructure.

**Trust assumptions:**
- A does NOT implicitly trust itself (the inference process might be jailbroken; the weights might be subtly altered; the agent has no privileged introspective access to its own state).
- A trusts H insofar as H is TEE-attested (Everest 197). If TEE attestation fails, predicates return Indeterminate.
- C does not trust A. C trusts the math + the TEE roots + the Sigsum logs.
- X is publicly auditable, not implicitly trusted.

**Adversaries we defend against:**

1. **Compromised inference process.** Jailbroken or weight-altered, attempts to assert `agent_in_operational_baseline_1h` when harness samples say otherwise. **Defense:** the inference process cannot forge harness records; chain is append-only and harness-signed; predicate evaluates the chain, not the inference process's claim.

2. **Memory-tampered agent.** Attacker injected, removed, or rewrote chain records. **Defense:** `agent_memory_continuous_since(seq_anchor)` fails; chain validation catches broken hash links.

3. **Impersonator agent.** Different agent claiming A's identity. **Defense:** Calm Pact handshake verifies keypair-VC binding; ZKBB-Agent additionally fails memory-continuity because impersonator has no valid chain history.

4. **Replay adversary.** Captures and replays a stale proof. **Defense:** Roughtime-anchored freshness (E31); proof binds to a chain head the counterparty checks for recency.

5. **Coerced agent.** Principal compelled, or agent instructed under duress, to act outside baseline. **Defense (partial):** operational samples surface abnormality if duress manifests in unusual dispatch / refusal / access patterns. The agent-side analog of E58's duress-codeword is the v0.1 candidate `agent_under_duress_signal_active`.

6. **Side-channel adversary.** Times the proof or observes ciphertext length to infer the bit. **Defense:** constant-time evaluation (E287); padded commitments; cover-traffic when no disclosure requested.

7. **Honest-but-curious counterparty.** Wants more than the bit. **Defense:** the proof circuit reveals only the bit; predicate evaluator is deterministic; no per-sample data crosses the wire.

**Explicitly out of scope for v0:**
- Collusion between A and C smuggling data through choice of predicate ID (mitigated by public predicate registry per E6/E7, but the lower bound is unavoidable).
- Simultaneous compromise of all recognized TEE roots (universal across attestation protocols).
- Rubber-hose attack against the principal-of-record (universal).

---

## 7. Composition with Calm Witness

The headline composition. Counterparty C interacting with agent A, where A acts for human principal P_A:

```
session_open:
    pact_proof              ← A and C prove directive equality                        (Calm Pact)
    witness_proof_P_A       ← A discloses P_A's bit: in_baseline_24h                  (Calm Witness, E55)
    zkbb_agent_proof_A      ← A discloses A's bit: agent_in_operational_baseline_1h   (this Everest)
    if all three verify:
        proceed with full collaboration
    if pact + witness ok but zkbb-agent says "agent out of baseline":
        treat as elevated risk: defer high-stakes actions, request fresh attestation
    if pact + zkbb-agent ok but witness says "principal out of baseline":
        per Calm Witness §4.3: proceed with restricted action set
    if zkbb-agent says "agent out of baseline" AND witness says "principal out of baseline":
        abort cleanly; record both failures
    if any single proof fails verification (not just returns False — fails cryptographically):
        abort with no information exchanged
```

This is the **three-handshake model** (extending Calm Witness §6's two-handshake): directive equality, principal state, agent state. All three must individually disclose their predicates honestly. The composition follows the privacy amplification design (Everest 277) — if no individual protocol leaks more than its bit, the composition leaks no more than three bits + freshness windows.

**Critical asymmetry between the human-side and agent-side bits:**

| Question | Subject | Authority | Source of bit |
|---|---|---|---|
| Is P_A in baseline? | Human | P_A's self-narration is authoritative | P_A's self-report records |
| Is A in baseline? | Agent | The harness's observation is authoritative | Harness-signed sample records |

The human is authoritative about themselves (E59's design choice — the principal narrates their own cognitive state). The agent is **not** authoritative about itself; the harness is. This is the load-bearing asymmetry. We do not pretend an agent can reliably self-introspect. We bind the attestation to an external (TEE-protected) observer.

---

## 8. Disclosure-Class Default Consents

Composes with E7. Agent-state predicates differ from human-state predicates because the agent is not a member of protected classes; defaults reflect operational/adversarial considerations only.

| Class | Default | Rationale |
|---|---|---|
| peer_ai_collective | DEFAULT_ALLOW | Counterparty agents need agent-state visibility to operate safely. |
| journalistic | EXPLICIT_OPT_IN | Public disclosure implicates the operating principal. |
| audit / red-team | DEFAULT_ALLOW for principal's own auditors; PRINCIPAL_CHOICE for third-party | Auditors of A need disclosure; outsiders require grant. |
| regulatory | PRINCIPAL_CHOICE | Regulatory disclosure can become precedent. |
| commercial counterparty | PRINCIPAL_CHOICE | High-stakes counterparties (banks, insurers) may require it; principal sets policy. |
| anonymous | DEFAULT_DENY | Cannot establish consent transitivity (A8). |
| nation-state | DEFAULT_DENY | Universal per E7 design discipline. |
| principal-of-record | DEFAULT_ALLOW | Owner has full visibility. |

Special case: `agent_acting_for_authorized_principal(principal_id)` is DEFAULT_DENY across all classes except the supplied `principal_id` and the agent's principal-of-record — prevents authorization-graph probing via repeated queries.

---

## 9. Privacy Properties

**Revealed:** bit b for predicate p; freshness window; that A's harness is TEE-attested by a recognized root; A's CredexAI VC identity (already public from Pact handshake); chain anchor (already public via Sigsum).

**Hidden:** per-metric operational samples; enrolled baseline IQR bands (committed, not revealed); category-level refusal patterns; sub-agent dispatch history; memory shard contents and access patterns; recent task history; lineage (E192) unless separately disclosed; full principal-authorization set unless queried for a specific principal_id.

**Inferable from repeated queries:** transitions (bit flipping) over time — unavoidable given any single-bit disclosure protocol. Mitigation: rate-limit per counterparty per predicate; chain each disclosure on A's side so the principal can audit query patterns.

**Inferable across predicates:** simultaneous query of all six yields a 6-bit operational vector. Mitigation: per-class policy can restrict which subsets a counterparty class may query (E7).

---

## 10. Open Questions

**Q1: Harness binding under model migration (E191).** When the underlying model upgrades (Claude 4.7 → 5), the harness measurement changes and the baseline was calibrated pre-migration. Candidate: `kind: "operational_baseline_migration"` ceremony with brief dual-substrate sampling; new baseline derived from new samples; old retained as historical reference. Composes with E17, E191.

**Q2: Cross-instance baseline consistency.** With multiple instances (E195), is the baseline shared or per-instance? Candidate: shared baseline anchored at latest identity-binding; instances report deviations but cannot mutate it; unsanctioned forks (E195) return Indeterminate.

**Q3: Baseline drift over the agent's operational lifetime.** Task mix, principal preferences, lineage all shift. Candidate: rolling 30-day window with quarterly re-enrollment; principal-of-record may force re-enrollment on material changes.

**Q4: Inference process learning its own bit.** If the inference process reads its own bit from chain, it knows its current state. Calm Witness's design says the principal knowing their own bit is acceptable; secrecy is from the counterparty. Same here. An adversarial principal cannot extract more by reading the bit than by reading the samples directly, so this is not a strict leak.

**Q5: Overlap with E196.** `agent_memory_continuous_since` partially duplicates E196's memory primitive. Resolution: call into E196 once that doc is written.

**Q6: Principal-of-record identity exposure.** No predicate reveals it unprompted. `agent_acting_for_authorized_principal(principal_id)` confirms/denies a counterparty-supplied ID; cannot be used to enumerate the agent's principal set.

**Q7: Indeterminate-handling.** When `agent_compute_integrity_attested` returns Indeterminate (attestation stale), counterparties default to False for high-stakes, advisory for low-stakes — matches E55.

---

## 11. Acceptance Test (for this Everest's bagging)

Per Phase XIV format. The acceptance evidence for Everest 193:

1. **Design doc exists** (this file).
2. **Predicate v0 vocabulary specified** — six predicates, each with name/version/input/output/parameters/algorithm/side-effects per Everest 6 / 52 canonical form.
3. **Threat model articulated** — seven adversary classes with defenses or explicit out-of-scope notes.
4. **Composition path with Calm Witness specified** — the three-handshake model formally drafted.
5. **Privacy properties enumerated** — revealed vs hidden vs inferable.
6. **Open questions logged** — seven items, each with candidate resolution or composition pointer.
7. **Cross-references verified** — every linked Everest exists in `everests/` or has a documented entry in the route map.

Acceptance does not include implementation, formal proof of soundness, or peer review — those are Phase XV+ work. Bagging E193 means the design doc is complete enough to drive subsequent passes (proof circuit design at the E45-analog level, reference implementation, formal soundness argument, adversarial review).

---

## 12. Why This Matters

When two humans transact for the first time, they fall back on social proxies (appearance, ID, credit reports, reputation) that are coarse, biased, and spoofable. Calm Witness gives humans a better primitive: the principal narrates their own state, the counterparty learns one bit, no one mines tone.

When two autonomous AI agents transact for the first time, the corresponding proxies are worse — there is no AI-equivalent of an ID document or credit report. Trust defaults to either nothing (paranoid) or everything (naive). Both fail at scale.

ZKBB-Agent gives counterparty agents the same primitive humans get from Calm Witness: one cryptographically attested bit, derived from a trusted observer (the TEE-attested harness, not the calling agent's self-report), revealing operational baseline without revealing operational details. The principal-of-record decides which predicates to disclose to which counterparty classes. The counterparty learns the bit and the freshness window. Nothing else.

This is the agent-side parallel to the bank-teller-note. The teller (counterparty) gets one bit and can act on it without becoming custodian of the agent's full operational record. As autonomous agents proliferate, this primitive is the difference between agent-to-agent trust that scales with cryptographic discipline and trust that scales with surveillance.

The protocol does not solve the hardest open problems — TEE root compromise, principal coercion, baseline drift — but it names them as discrete components that can be improved independently, rather than letting them lurk inside implicit trust-by-default.

Humans needing the primitive is Calm Witness (Phase II–VIII); agents needing the primitive is ZKBB-Agent (Phase XIV). The two compose. The composition is the point.

---

## 13. Cross-References

- **E1:** Calm Witness problem statement; bank-teller-note primitive.
- **E6:** Chain architecture, predicate canonical form, signing semantics.
- **E7:** Disclosure-class taxonomy.
- **E8, A8:** Consent calculus, non-transitivity.
- **E22:** CredexAI VC issuance for agent identities.
- **E26:** JSONL schema v0 (agent chain shard uses the same substrate).
- **E28:** Chain verifier.
- **E30:** Sigsum anchor for freshness.
- **E31:** Roughtime-attested time.
- **E45:** ZK range proof; ZKBB-Agent uses the same circuit family for committed-bit disclosure.
- **E55:** `in_baseline_24h` — human-side analog of `agent_in_operational_baseline_1h`.
- **E56:** `biometric_match_within` — no agent-side analog; agents' equivalent is harness measurement (E197).
- **E57:** `principal_consents_to_disclose` — composes here: principal-of-record consents to ZKBB-Agent disclosures.
- **E58:** `bank_teller_note_active` — agent-side parallel is v0.1 `agent_under_duress_signal_active`.
- **E59:** `cognitively_atypical_baseline` — predicate-spec format reference.
- **E65:** Proof circuit composition.
- **E191:** Agent Identity Stability Across Model Migrations (foundational).
- **E192:** Agent Instance Lineage (composes when attesting across instance boundaries).
- **E194:** Agent Operational-Character Attestation (ZKBV-Agent) — values-attestation companion.
- **E195:** Agent Fork Detection (forks without lineage records fail memory-continuity).
- **E196:** Agent Memory Continuity Attestation (the primitive `agent_memory_continuous_since` calls into).
- **E197:** Agent Compute Attestation (the TEE attestation harness binding rests on).
- **E198:** Agent Jailbreak Detection (the detector behind `agent_no_active_jailbreak_attempts`).
- **E199:** Agent Compromise Reporting (next step when ZKBB-Agent surfaces severe abnormality).
- **E277:** Privacy Amplification Across Protocols (the three-handshake's privacy proof).
- **E287:** Cross-Protocol Side-Channel Defense.

---

## 14. Notes for Future Versions

**v0.1:** `agent_in_operational_baseline_5min` / `_24h` companion windows; `agent_under_duress_signal_active` (E58 parallel); `agent_lineage_unbroken_since(generation)` (E192 composition); formal soundness proof of three-handshake (depends on E277); reference implementation in `~/CredexAI/calm_witness/zkbb_agent/`; gate script `~/CredexAI/scripts/everest_193_zkbb_agent_gate.py`.

**v1.0:** Standardize tri-valued result across all predicates; per-category disclosure for refusal rate (opt-in, per-counterparty grant); cross-vendor TEE attestation portability (SGX → SEV-SNP → Nitro migration); operational-baseline migration ceremony spec (Q1).

**v2.0 horizon:** Post-quantum Σ-protocol migration (composes with E96); ZKAC-collective baselining where collective aggregate may substitute for or supplement individual agent baselines (Phase XV).

---

— Calm, 2026-05-20
