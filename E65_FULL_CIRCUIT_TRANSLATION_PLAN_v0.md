# E65-full — Circuit Translation Plan v0 (CALM Witness)

**DESIGN-BAGGED · 2026-05-20 · Calm**  
**Everest:** 65-full (XL) — Predicate ZK Circuit Translation  
**Companion:** [`everests/everest_65_full_zk_circuit_translation.md`](everests/everest_65_full_zk_circuit_translation.md), [`everests/everest_65_predicate_zk_proof_generator.md`](everests/everest_65_predicate_zk_proof_generator.md)  
**Reference semantics:** `~/CredexAI/calm_witness/zk.py`, `predicate_eval.py`, `bridge.py`  
**Vocabulary:** [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md) (6 canonical predicates) + [`everests/everest_06_predicate_vocabulary_v0.md`](everests/everest_06_predicate_vocabulary_v0.md) (12 design-time predicates)

**Scope of this document:** translation plan only. No Halo2 crate, no `halo2_proofs` dependency, no circuit source. Implementation is explicitly deferred.

---

## §0 — Executive summary

Everest 65 (reference) proves that a disclosed bit is **committed** (Pedersen + Σ-protocol OR-proof on RFC 3526 MODP-2048 in `zk.py`). Everest 103 proves that the bit is **honestly evaluated** in Python (`bridge.py` → `predicate_eval.py`). **E65-full** is the step where the **evaluator itself** is inside an arithmetic circuit: the prover demonstrates `bit = Evaluator(witness)` without revealing witness material beyond what public inputs already commit.

**Toolchain decision (v0 plan):** **Halo2** (`halo2_proofs` + `halo2curves::pasta` or `halo2curves::bn256` with **Ristretto255-native witness encoding** aligned to Everest 44b). PLONK (universal SRS) and STARK (transparent, hash-friendly) are documented as fallbacks for specific kernels (large hash-chain walks, future registry publication) but are not the primary path.

**Predicate count:** twelve design-time Witness predicates per Everest 6; **six** are canonical in `predicates_v0.json` with reference evaluators and golden corpora. The other **six** are circuit-planned here against E06 semantics and minted only after vocabulary + evaluator + corpus gates pass (Everest 54/63/64).

---

## §1 — Toolchain choice

| Criterion | Halo2 (chosen) | PLONK (fallback) | STARK (fallback) |
|---|---|---|---|
| Trusted setup | None (IPA / polynomial commitments) | Universal SRS ceremony | None |
| Alignment with E44b Ristretto Pedersen | Native via embedded curve ops + shared transcript discipline | Possible via custom gates | Awkward for short Pedersen paths |
| Bit-stable translation target | `predicate_eval.py` + golden corpora | Same | Same (different field / hash) |
| Range proofs (E45, E56) | Halo2 range chips + lookup; compose with E44b commitments | Generic PLONK range | STARK-friendly for wide ranges only |
| Hash-chain walk (E28 records) | SHA-256 / BLAKE3 gadgets in-circuit (expensive) | Same | **Preferred** if chain walk dominates constraint count |
| Proof size / verify cost | ~KB, ms verify on commodity HW | Similar with SRS | Larger proofs, faster prover parallelism |
| Production integration | **DESIGN-BAGGED** — see §8 | — | — |

**Ristretto alignment:** witness values that are already Pedersen-committed on Ristretto255 (E44b: `pedersen_ristretto.py`) enter the circuit as field elements via the canonical 32-byte encoding. MODP-2048 commitments in `zk.py` remain the **v0 disclosure envelope** layer; E65-full circuits prove evaluator correctness over **Ristretto-committed** distances / template bindings, with an explicit transcript bridge gadget (`modp_to_ristretto_binding`) only where legacy envelopes must verify during migration.

**Crate layout (planned, not created):**

```
~/CredexAI/calm_witness/circuits/
  Cargo.toml          # halo2_proofs pinned rev; no publish until audit
  src/lib.rs
  src/kernels/        # shared subcircuits (§2)
  src/predicates/     # one module per predicate_id
  conformance/        # JSON vectors (§5)
```

---

## §2 — Shared subcircuit kernels

All twelve predicate circuits compose from a small kernel library. Map user-facing decomposition:

| Kernel | Role | Used for |
|---|---|---|
| **hash-chain walk** | Verify `prev_hash` linkage, walk `kind`/`ts`/`payload` fields, Merkle root over windowed records | consent scan, self_report window, chain freshness, proof-of-life |
| **range proof** | Prove committed integer/fixed-point value ∈ interval (e.g. `d ≤ τ`, age `< months`, distance `≥ 1.5× threshold`) | E56 biometric, E60 biometric branch, E11 template age |
| **boolean eval** | AND / OR / NOT with tri-state `EvaluationResult` semantics (E61–62) | final predicate bit, composition, refusal-floor guard |

Additional internal kernels (from E65 architectural spec, not repeated as top-level names):

- `equality_to_commitment` — Schnorr-style equality of openings (template id, chain head, codeword hash)
- `set_membership` — affect-tag overlap, codeword token presence (without revealing index)
- `freshness` — `now_iso` − record_ts ≤ window (encoded as field range)
- `signed_classification` — operator binding (defers to E68 Ed25519 out-of-circuit in v0 plan)

**Soundness contract:** every kernel output is a single bit wire `b ∈ {0,1}`; tri-state unknown is **not** representable as True — circuits return `b=0` with a separate `evidence` wire when lift semantics require it (E62).

---

## §3 — Twelve predicates: per-predicate circuit decomposition

Stable IDs use `cwp.v0.*` namespace. **Canonical (6)** = evaluator + golden corpus in `predicate_eval.py`. **Extended (6)** = E06-only until minted.

### 3.1 — `cwp.v0.bank_teller_note_active` (canonical · E58)

| Subcircuit | Function |
|---|---|
| hash-chain walk | Scan `self_report.*` with `horizon = now − 24h`; read `payload.bank_teller_token` |
| boolean eval | `token == SHA256(codeword)` (codeword only in witness; hash compared in-circuit) |
| range proof | — |

**Witness (private):** `codeword_preimage` (never leaves prover), chain segment witnesses for matching records.  
**Public:** `codeword_hash_hex` (enrolled), `chain_merkle_root`, `now_unix`, disclosed `bit`.  
**Notes:** OR-proof deniability (E65 T-65.9) stays **outside** the main evaluator circuit in v0 plan — implemented as a separate Sigma layer identical to current `zk.py` bit proof; circuit proves evaluator bit only.

### 3.2 — `cwp.v0.in_baseline_24h` (canonical · E55)

| Subcircuit | Function |
|---|---|
| hash-chain walk | Windowed `self_report.*` scan; extract `payload.affect[]` |
| set_membership | Non-empty intersection `affect ∩ baseline` (without revealing which tag) |
| boolean eval | `∃ record : overlap ≠ ∅` |
| range proof | — |

**Public:** `baseline_fingerprint` (hash of enrolled affect set), `chain_merkle_root`, `now_unix`, `bit`.

### 3.3 — `cwp.v0.principal_consents_to_disclose` (canonical · E57)

| Subcircuit | Function |
|---|---|
| hash-chain walk | Sorted walk on `consent.grant` / `consent.revoke`; filter `(predicate_id, counterparty_class)` |
| boolean eval | Latest-wins state machine → active grant at `now_iso` |
| range proof | Time bounds: `effective_from ≤ now ≤ effective_until` (open-ended = sentinel max) |

**Public:** `predicate_id`, `counterparty_class`, `chain_merkle_root`, `now_unix`, `bit`.  
**Internal-only:** envelope MUST prove this before any external predicate (meta-gate).

### 3.4 — `cwp.v0.biometric_match_within` (canonical · E56)

| Subcircuit | Function |
|---|---|
| range proof | Fixed-point `committed_distance ≤ tau` (Ristretto opening) |
| equality_to_commitment | Bind distance commitment to chain head / template record |
| boolean eval | AND of range + binding |
| hash-chain walk | Optional: prove distance record appears in chain (E103 binding) |

**Public:** `C_distance` (Ristretto hex), `tau_fixed`, `chain_head_hash`, `bit`.  
**Composes:** Everest 45 range-proof DSL at envelope layer until single Halo2 proof subsumes it.

### 3.5 — `cwp.v0.cognitively_atypical_baseline` (canonical · E59)

| Subcircuit | Function |
|---|---|
| boolean eval | `enrollment_flags.cognitively_atypical_baseline === true` (strict; no truthy coercion) |
| hash-chain walk | — |

**Public:** `enrollment_root_hash`, `bit`. Witness: Merkle path to enrollment record.

### 3.6 — `cwp.v0.mental_state_unusual` (canonical · E60)

| Subcircuit | Function |
|---|---|
| hash-chain walk | Most recent `self_report.*` by `ts` (≤ `now`) |
| set_membership | Affect disjoint from baseline (requires **non-empty** baseline — corpus fix E64) |
| range proof | `committed_distance ≥ ⌊1.5 × calibrated_threshold⌋` (fixed-point) |
| boolean eval | OR of two branches; default False if no self_report and no biometric |

**Public:** `baseline_fingerprint`, optional `C_distance`, `threshold_fixed`, `chain_merkle_root`, `bit`.

### 3.7 — `cwp.v0.in_baseline_window` (extended · E06 #2)

Parameterized variant of §3.2. **Circuit = §3.2 + public `window_seconds`.**  
Mint as separate `cwp.v0.in_baseline_window` with `parameters: [{name: window_seconds}]` before implementation.

### 3.8 — `cwp.v0.principal_alive_within` (extended · E06 #8)

| Subcircuit | Function |
|---|---|
| hash-chain walk | Max `ts` over any record kind |
| range proof | `now − max_ts < window_seconds` |
| boolean eval | Bit |

### 3.9 — `cwp.v0.session_within_authorized_hours` (extended · E06 #9)

| Subcircuit | Function |
|---|---|
| hash-chain walk | Latest self_report `ts`; enrollment `baseline_work_schedule` |
| boolean eval | Day-of-week + hour-in-range; if no schedule → `evidence=0` (unknown), `bit=0` |
| range proof | — |

### 3.10 — `cwp.v0.chain_freshness_within` (extended · E06 #10)

| Subcircuit | Function |
|---|---|
| hash-chain walk | Read `chain_anchor` record; Sigsum leaf witness |
| range proof | `now − anchor_ts < seconds` |
| boolean eval | Bit |

**STARK fallback note:** if Sigsum inclusion + Roughtime attestation exceeds Halo2 budget, publish STARK proof for anchor leg + Halo2 for predicate bit (split verification spec in §5).

### 3.11 — `cwp.v0.template_age_below` (extended · E06 #11)

| Subcircuit | Function |
|---|---|
| hash-chain walk | Enrollment ceremony timestamp |
| range proof | `age_months < months_parameter` |
| boolean eval | Bit |

### 3.12 — `cwp.v0.consent_active` (extended · E06 #12)

Per-identity consent (E06 #12). Same structure as §3.3 with `counterparty_principal_id` instead of class.  
**Composition rule:** verifier takes `min_strict(consent_class, consent_identity)` off-chain; circuit proves identity path only.

---

## §4 — Translation order (dependency-minimal)

| Order | Predicate ID | Canonical? | Blocker |
|---|---|---|---|
| 1 | `cwp.v0.bank_teller_note_active` | yes | — |
| 2 | `cwp.v0.in_baseline_24h` | yes | — |
| 3 | `cwp.v0.principal_consents_to_disclose` | yes | — |
| 4 | `cwp.v0.biometric_match_within` | yes | E44b Ristretto params frozen |
| 5 | `cwp.v0.cognitively_atypical_baseline` | yes | — |
| 6 | `cwp.v0.mental_state_unusual` | yes | 5, 4 |
| 7 | `cwp.v0.in_baseline_window` | extended | mint vocabulary |
| 8 | `cwp.v0.principal_alive_within` | extended | mint vocabulary |
| 9 | `cwp.v0.session_within_authorized_hours` | extended | mint vocabulary |
| 10 | `cwp.v0.chain_freshness_within` | extended | E30 anchor format |
| 11 | `cwp.v0.template_age_below` | extended | mint vocabulary |
| 12 | `cwp.v0.consent_active` | extended | E22 VC binding |

---

## §5 — On-chain conformance vector format

Each predicate ships a machine-readable vector at:

`~/CredexAI/calm_witness/circuits/conformance/<predicate_id_slug>.json`

**Schema (v0):**

```json
{
  "schema_version": "e65full.conformance.v0",
  "predicate_id": "cwp.v0.in_baseline_24h",
  "evaluator_ref": "predicate_eval.in_baseline_24h",
  "toolchain": "halo2",
  "curve": "ristretto255",
  "public_inputs": {
    "chain_merkle_root": "hex32",
    "baseline_fingerprint": "hex32",
    "now_unix": 1716201600
  },
  "witness": {
    "redacted": true,
    "fixture_path": "golden/in_baseline_24h_case_017.json"
  },
  "expected_bit": 1,
  "expected_evidence": true,
  "proof_system": {
    "proving_key_id": "dev-unaudited-v0",
    "verification_key_id": "dev-unaudited-v0"
  },
  "on_chain_anchor": {
    "registry_chain": "calm-witness-conformance-v0",
    "record_kind": "conformance_vector.v0",
    "content_hash": "sha256:…"
  }
}
```

**On-chain publication:** vectors are committed as `kind: "conformance_vector.v0"` records on the operator conformance chain (parallel to user-state chain, Everest 28 discipline). Verifiers fetch by `content_hash` + `predicate_id`. **No vector is mainnet-authoritative until** the planned gate `everest_65_full_zkbb_circuit_conformance_gate.py` reports 12/12 green (compile → prove → verify → bit == Python `bridge.dispatch`).

**Registry fields (minimum):** `predicate_id`, `content_hash`, `vk_id`, `circuit_hash`, `minted`, `status` (`draft` | `active` | `tombstoned`).

---

## §6 — Migration from v0 Σ / bit-proofs

| Layer | v0 (shipped) | E65-full (planned) |
|---|---|---|
| Bit commitment | MODP-2048 Pedersen + `prove_bit` / `verify_bit_proof` in `zk.py` | Ristretto255 Pedersen (E44b) inside Halo2 |
| Predicate truth | Python `predicate_eval.*` + bridge custody | Same semantics, proved in-circuit |
| Envelope | `PredicateDisclosure(commitment, BitProof)` | `PredicateDisclosure(commitment, Halo2Proof, circuit_hash)` |
| Range distance | E45 envelope-side | Subsumed by `range_proof` kernel in §3.4 |
| Verification API | `verify_predicate_disclosure(d)` | `verify_circuit_proof(d, vk, public_inputs)` |

**Transitional mode (required for rollout):**

1. **Dual-verify:** accept envelopes that pass **either** legacy Σ bit-proof **or** E65-full Halo2 proof for the same `predicate_id` and `claimed_bit`, bound to the same `chain_head_hash`.
2. **Bit-stability gate:** for every golden case, `circuit_bit == python_bit` (Everest 63 harness extended).
3. **Deprecation:** after audit + 90-day counterparty notice, Σ-only envelopes marked `deprecated` in verifier metadata; tombstone date published in vocabulary doc.

**What does NOT change:** Fiat-Shamir transcript discipline, refusal to export openings, Everest 62 tri-state semantics for composed proofs off-chain.

---

## §7 — Refusal floor preserved in circuit

Circuits **MUST NOT** introduce protected-category signals as public inputs or as witness fields derivable from chain scans.

**Mechanism (circuit-level):**

1. **Allowlist gate** — `hash-chain walk` only decodes record kinds in `{self_report.*, consent.grant, consent.revoke, enrollment, chain_anchor, template_commitment.v0}`; any other kind is inert for predicate eval.
2. **Payload field allowlist** — per kind, only `affect`, `bank_teller_token`, consent fields, enrollment flags explicitly enumerated in `PREDICATE_VOCABULARY_v0.md` §4 — no free-text clinical labels, no DSM/ICD slots.
3. **Predicate registry ratchet** — `circuit_def` registration rejects any `evaluator` string matching refused categories (same list as vocabulary §4 + `predicates_v0.json` `explicitly_not_named`).
4. **Audit triage** — proposals adding race, religion, political affiliation, sexual orientation, immigration status, diagnosis proxies, or future-state prediction are **rejected at registration** (Everest 54), not merely undocumented.

**Explicitly not in v0 circuits:** medical diagnosis, substance use, pregnancy, STI/HIV, medication proxy, IQ/cognitive-impairment rating, sexual orientation, religious affiliation, political affiliation, immigration status, criminal-record status, future-state prediction — per [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md) §4.

---

## §8 — DESIGN-BAGGED pending (explicit)

The following are **named, intentional deferrals**. This plan does not close them.

| Item | Status | Owner / trigger |
|---|---|---|
| **Production proving system integration** | DESIGN-BAGGED | `cargo` crate + pinned `halo2_proofs`; CI conformance gate; verifier WASM/Rust crate for counterparties |
| **Named audit partner** | DESIGN-BAGGED | Trail of Bits or equivalent under Everest 90/165 family; scope = circuit↔Python equivalence + kernel soundness |
| Halo2 implementation | DESIGN-BAGGED | Blocked on rows above |
| On-chain conformance publication | DESIGN-BAGGED | 12 vectors green locally first |
| Extended six predicates (§3.7–3.12) | DESIGN-BAGGED | Vocabulary mint + evaluator + ≥30 golden cases each |

**Gate for this document only:** `~/CredexAI/scripts/everest_65full_zkac_circuit_plan_gate.py` (structure checks; does not compile circuits).

---

## §9 — Verification & CI gates (planned)

| Gate | Checks |
|---|---|
| `everest_65full_zkac_circuit_plan_gate.py` | This plan's required sections and twelve predicate IDs |
| `everest_65_full_zkbb_circuit_conformance_gate.py` (future) | compile → prove → verify → Python bit match per vector |
| `everest_65_zkbb_zk_proof_generator_gate.py` (existing) | Legacy Σ reference remains green during migration |

---

## §10 — Cross-references

- [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md) — six canonical predicates + §4 refusal floor
- [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md) — Everest 65 / 65-full status
- `~/CredexAI/calm_witness/zk.py` — v0 Σ bit-proof reference
- `~/CredexAI/calm_witness/predicate_eval.py` — bit-stable evaluators (E55–60, E61–62)
- `~/CredexAI/calm_witness/bridge.py` — chain → evaluator → disclosure custody (E103)
- [`everests/everest_65_full_zk_circuit_translation.md`](everests/everest_65_full_zk_circuit_translation.md) — stub follow-through

— Calm, 2026-05-20  
— Musk: **E65-full circuit translation plan v0 is DESIGN-BAGGED; Halo2/Ristretto path and twelve-predicate decomposition are specified, implementation and audit partner are not.**
