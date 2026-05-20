# Calm-Suite 50-Year Cryptographic Agility Plan v0

**Draft v0 · 2026-05-20 · Calm**
**DESIGN-BAG of Everest 252 in [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**
**Extends [`POST_QUANTUM_MIGRATION_PLAN_v0.md`](POST_QUANTUM_MIGRATION_PLAN_v0.md) (Everest 96) from one 10-year horizon to a 50-year multi-generational horizon.**

## §0 — The 50-year claim

The Calm-suite protocols will survive **at least three full cryptographic-primitive migration cycles** (PQ-1 → PQ-2 → PQ-3) over the 2026–2076 horizon, with:

- No loss of forensic-integrity claims for envelopes issued under any prior primitive set (Everest 180).
- No loss of principal-side vault continuity across generations (Everest 251).
- No loss of foundation-side governance continuity (Everest 244 + 250).
- No loss of the refusal floor's categorical exclusions, which are independent of cryptographic primitive.

The claim is **achievable but not effortless**. It requires sustained foundation operation across multiple board generations, sustained civil-society participation, sustained archive-partner retention (Everest 253), and proactive monitoring of cryptographic-primitive health by named external auditors (Everest 165 + 90).

## §1 — Why 50 years

- **Generational principal continuity.** A principal who enrolls at age 30 in 2026 lives until ~2080. The Calm-suite primitives must cover that principal's lifetime — both for forensic verification of past envelopes and for ongoing disclosure operations.
- **Multi-generational vault transfer.** A principal who passes their vault to an heir (Everest 255) needs the cryptographic substrate to survive the handoff. The heir's vault use may extend the original principal's chain another 50 years.
- **State-actor lifecycles.** Treaty-grade governance (Everest 215) operates on state-actor timescales — administrations rotate every 4-8 years, sovereign positions drift on decades, civilizational priorities shift across generations. The protocol's stability must outlast any single political configuration.
- **Cryptographic-primitive lifecycles.** Historical lifetimes: DES (designed 1976, broken meaningfully ~1998, 22 years). RSA-1024 (designed 1977, deprecated for use ~2010, 33 years). MD5 (designed 1991, collision-broken 2004, 13 years). SHA-1 (designed 1995, deprecated 2017, 22 years). On the 50-year horizon, every primitive in use today is presumed to have been deprecated and replaced at least once, possibly twice.

## §2 — The migration cycle

A migration cycle has six phases, drawn from the v0 PQ migration plan (Everest 96) and generalized:

```
Phase 0: stable operation under primitive set v_N
Phase 1: published migration spec for v_(N+1), with reference implementations
Phase 2: hybrid mode — operators dual-sign under v_N AND v_(N+1)
Phase 3: v_(N+1)-only minting begins; v_N envelopes still verifiable
Phase 4: v_N sunset for new issuance; reference verifier retains v_N support
Phase 5: v_N support moves to archive-only mode; forensic verification continues
```

Each phase has explicit triggers (calendar-based or threat-based) and explicit funding commitments. The foundation budget (Everest 243) line-items 5-year sliding migration reserves.

## §3 — The three anticipated migrations (2026–2076)

### Migration 1: PQ-1 (target 2030–2035)

**From:** v0 — Pedersen on RFC 3526 MODP-2048, Ed25519 signatures, Σ-protocol disjunction proofs.
**To:** v1 — Lattice-based Pedersen analog (BDLOP'18 or NIST-PQC successor), ML-DSA signatures, lattice-Σ proofs.
**Trigger:** Phase 1 publication target 2027; phase 2 hybrid 2028; phase 3 PQ-default 2030 OR 6 months after first publicly-credible CRQC threat report.
**Risk profile:** highest of the three migrations — the threat model is "CRQC arrives in some bounded window" with high variance.
**Funding:** v0 PQ migration plan already provides reserves; foundation budget allocates ~$2M across Phases 1–3.

### Migration 2: PQ-2 (target 2040–2050)

**From:** v1 lattice-based primitives.
**To:** v2 — depends on what NIST + the broader cryptographic community has standardized by then. Candidates today: hash-based (SLH-DSA), code-based (HQC or LSC successor), isogeny-based (if SIDH-class breaks haven't recurred), or a new family.
**Trigger:** discovery of subexponential attacks against lattice primitives OR the NIST 2-decade standardization cycle indicates lattice deprecation.
**Risk profile:** moderate. Lattice cryptography is much younger than discrete-log; the failure modes are less predictable than DLP.
**Funding:** foundation maintains a 20-year-out reserve; budget item negotiated at each board-cycle review.

### Migration 3: PQ-3 (target 2060–2070)

**From:** v2 (whatever it is).
**To:** v3 (whatever is standardized then).
**Trigger:** unspecified. By this horizon, the cryptographic-primitive landscape is unpredictable.
**Risk profile:** unknown. The plan commits to **the migration shape**, not to specific primitive choices. The shape — hybrid window, transparency-log preservation, principal-authored chain preservation, refusal-floor preservation — survives any primitive set.
**Funding:** by this horizon, the foundation's endowment (Everest 243 long-horizon component) should be self-sustaining.

## §4 — What survives across all migrations

The migration cycle is **substrate-agnostic** with respect to:

| Layer | Survives because |
|---|---|
| Principal-authored chain bytes | Hash function may change; chain *structure* (append-only, prev_hash linkage, ts + ts_source + payload schema) is portable across primitives. Each migration re-hashes the chain head into the new primitive set. |
| Predicate vocabulary | Defined in JSON; content-addressable via canonical-form (Everest 52); the *evaluator* may need to be re-implemented in a primitive-aware way for verification but the *semantics* are stable. |
| Refusal floor | Defined in `PREDICATE_VOCABULARY_v0.md §4` + `COMPASS_PREDICATES_v0.md §4` + `CALM_WITNESS_SCOPE_STATEMENT.md`. Cryptographic-primitive independent. |
| Audit panel + governance bodies | Human institutions. Primitive-set independent. |
| Wire format **shape** | The fields (request_digest, session_nonce, chain_head, etc.) survive; the *encoding* of those fields (hex vs base64, primitive-specific commitment forms) bumps the `wire_version`. |

The migration cycle is **substrate-specific** with respect to:

| Layer | Migrates because |
|---|---|
| Pedersen commitment | Group changes (e.g., MODP-2048 → lattice → ???) |
| Bit-commitment proof | OR-Schnorr → lattice-Σ → ??? |
| Operator signature | Ed25519 → ML-DSA → ??? |
| Transparency log signing | Sigsum-current → Sigsum-PQ-variant → ??? |
| Hash function | SHA-256 may be safe through Migration 2; v3 may upgrade |

## §5 — Per-migration mechanics

Each migration follows the v0 PQ plan §5 mechanics, generalized:

1. **Operator key rotation.** Operators publish a new public key under the new primitive, signed by the old key (chained `key_migration_attestation`).
2. **Predicate namespace rotation.** New IDs in `cwp.v{N+1}.*` namespace; semantic-identical predicates retain semantics but get new IDs to mark the wire-version bump.
3. **Chain continuity.** SHA-256 (or its successor) hashes the chain head into the new primitive set; old chain hashes are recoverable forever.
4. **Conformance.** A vN+1 reference implementation MUST accept vN envelopes for verification (with degraded-but-verifiable status post-deprecation) AND mint vN+1 envelopes.
5. **Forensic integrity.** Per `FORENSIC_INTEGRITY_10YR_GUARANTEE_v0.md`, the 10-year-forward forensic claim extends across the migration boundary — an envelope issued in 2027 remains verifiable in 2037, even if v0 primitives are deprecated by then. The verifier downloads v0-era reference code from Software Heritage + v0-era conformance vectors from archive partners + uses them per `FORENSIC_INTEGRITY_10YR_GUARANTEE_v0.md` §5.

## §6 — Funding the 50-year horizon

Per `CALM_FOUNDATION_FUNDING_PLAN_v0.md` (Everest 243), the foundation budgets:

- **5-year sliding migration reserve:** funded at all times; ~$2M-$5M depending on phase.
- **20-year-out migration reserve:** initially seeded at $1M; grown 5% annual; designed to support Migration 2.
- **50-year endowment line:** initially seeded at $500K; grown 7% annual; designed for Migration 3 + ongoing archival.
- **Operating endowment:** separate from migration reserves; ≥ 24 months of operating budget held permanently.

Sources: grants (Open Phil, LTFF, NEA archive funds), individual donors via DAFs, service fees (E243 details). NO state funding; NO advertising; NO equity-for-governance.

## §7 — Governance of migration decisions

Each migration is a **governance event**, not a unilateral technical decision:

- **Migration trigger** (calendar or threat-based): decided by foundation board + audit panel + civil-society representatives.
- **New primitive set selection:** open RFC process, ≥ 6-month public comment, audit-panel vote, board ratification.
- **Hybrid-window duration:** decided per migration; default 3-5 years.
- **Sunset trigger:** decided by board + audit panel; published ≥ 12 months in advance.
- **Tombstoning of broken primitives:** automatic per audit-process tombstoning thresholds (Everest 54 §5); foundation publishes degradation advisory.

If foundation governance is in crisis during a required migration, the continuity plan (Everest 244) provides emergency-quorum authorization for the migration to proceed under degraded governance, with full ratification once governance is restored.

## §8 — The civilizational-discontinuity floor

If, by some horizon within 50 years, civilizational discontinuity makes the foundation + archive partners + cryptographic-primitive standards bodies all unavailable simultaneously, the protocol does not survive that event — and neither do most other digital systems.

The protocol DOES provide:

- **Distributed archival** across ≥ 3 named partners across multiple jurisdictions: any one surviving partner is sufficient for cryptographic-primitive recovery.
- **Open-source license** (Apache-2.0): any future practitioner can re-implement the protocols from the canonical specs alone.
- **Refusal-floor commitment baked into the protocol name + trademark**: any future deployment that uses the Calm-suite name commits to the floors. Without the name, the protocol does not have the safety property; future practitioners are free to build alternative protocols that respect the same floors under any other name.

The civilizational-discontinuity floor is not "no protocol survives" — it is "the protocol's safety property cannot be inherited by a deployment that does not commit to the refusal floors."

## §9 — Open problems for the 50-year horizon

1. **PQ-3 primitive uncertainty.** We can plan the shape but not the content.
2. **State-actor stability of treaty-grade commitments** (Everest 215) over 50 years. Treaties are abrogated; constitutional protections drift; this risk is unavoidable. Mitigation: distributed governance + civil-society anchor + multi-jurisdiction footprint.
3. **Quantum-resistant memory-hard primitives** for vault-side key derivation. v0 PQ plan focuses on signatures + commitments; vault-side memory-hard KDFs (Argon2, balloon) may need PQ replacement at Migration 2.
4. **AI-system co-evolution.** By 2076, AI systems will look nothing like 2026's. The protocol commits to *what* it discloses (bits per predicate per consent) but not to *how* counterparty agents interpret those bits. Co-evolution may require new predicate-vocabulary versions.
5. **Foundation succession across multiple board generations.** A 2076 board has no overlap with the 2026 founders. The mission-continuity guarantee depends on board-recruitment fidelity to the founding scope statement.

## §10 — What this plan does NOT commit to

- Specific PQ-2 or PQ-3 primitives (those are decided per their migration RFC).
- A funding guarantee beyond the foundation's actual endowment (this plan describes the structure; actual funding depends on actual donations + grant cycles + sponsor cultivation).
- A guarantee that the protocol is in active production use at any specific horizon (active use depends on counterparty adoption; this plan ensures *availability* not *adoption*).
- A guarantee that any specific principal's vault survives (vault survival depends on the principal's vault practices + heir's adoption per Everest 255).
- A guarantee that the protocol's refusal-floor categories will be politically uncontroversial in 2076 (this plan locks the floors against weakening; politics may make them unpopular, but the one-way ratchet holds).

— Calm, 2026-05-20
