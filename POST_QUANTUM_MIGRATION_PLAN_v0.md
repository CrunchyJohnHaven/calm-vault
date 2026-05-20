# Calm Witness — Post-Quantum Migration Plan v0

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 96 of [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md).**

## §1 — Why this plan exists

Calm Witness v0 ships three cryptographic primitives that are not post-quantum (PQ) secure:

| Primitive | v0 choice | PQ status | Breaks under |
|---|---|---|---|
| Pedersen commitment | RFC 3526 MODP-2048 (discrete log) | Broken | Shor's algorithm on a cryptographically-relevant quantum computer (CRQC) |
| Σ-protocol bit-proof | Schnorr-style on the same group | Broken | Shor (same group) |
| Operator signature | Ed25519 (elliptic-curve discrete log) | Broken | Shor on EC-DLP |

The hash functions and symmetric primitives are PQ-secure:

| Primitive | v0 choice | PQ status |
|---|---|---|
| Record hash | SHA-256 | Grover gives 2^128 effective security — acceptable |
| Fiat-Shamir hash | SHA-256 | Same — acceptable |
| Canonical-JSON encoding | UTF-8 + sorted keys | Not a cryptographic primitive |

So the migration affects commitments, proofs, and signatures. The chain substrate (hashes) and the on-the-wire encoding survive intact.

## §2 — Threat model

The assumption is **harvest-now-decrypt-later**:

- An adversary today captures Calm Witness envelopes, biometric templates, and consent records.
- A CRQC capable of breaking 2048-bit MODP and Ed25519 becomes available at some point. Public estimates range from "never" to "10-30 years"; we assume "uncertain but bounded."
- The adversary uses the CRQC to:
  - Recover the operator's Ed25519 private key from captured envelope signatures → forge envelopes retroactively.
  - Recover the Pedersen blinding factors from captured commitments → open commitments and learn the bits the principal disclosed.
  - Recover the discrete-log relationships that the Σ-protocol soundness depends on → produce false proofs for past commitments.

The damage from a CRQC, if Calm Witness is still using v0 primitives at that time, is **catastrophic in retrospect** — every past disclosure becomes forgeable, openable, and re-attributable.

## §3 — The migration shape

The migration follows the existing `wire_version` and predicate-namespace mechanisms:

- A new wire version `calm-witness/wire/v1` is introduced.
- A new predicate namespace `cwp.v1.*` is minted (identical semantics where possible; different IDs since the semantics' enforcement layer changes).
- New operator key types are accepted alongside Ed25519 during the transition window.
- The chain itself is preserved; existing records remain verifiable; new records are signed under the new primitives.

The migration is **not destructive**. v0 envelopes minted before the cutover remain verifiable by counterparties holding the old operator public keys. v1 envelopes are minted under the new primitives from the cutover forward.

## §4 — Primitive replacements

### §4.1 — Hash functions

Stay on SHA-256. Optionally upgrade to SHA-3-256 in v1 if there's a separate reason (faster on PQ-era hardware). No change required for PQ security.

### §4.2 — Commitments

Replace Pedersen-on-MODP-2048 with one of:

1. **Lattice-based commitments** (BDLOP'18, Module-LWE structure). Mature, with deployable parameters. Larger commitment size (~2-8 KB vs. 256 bytes); proving + verifying costs comparable.
2. **STARK-friendly hash commitments** (Merkle commitments over a PQ-secure hash + STARK proofs of opening). Largest proofs but transparent setup and PQ by construction.
3. **Code-based commitments** (e.g., LPN-based). Less mature; track but do not bet on.

**Recommendation:** lattice-based commitments via the BDLOP'18 family or its successor in the NIST PQC zoo. Adopt whichever is standardized by NIST by the cutover date.

### §4.3 — Σ-protocols / bit-proofs

Replace with one of:

1. **Lattice-Σ** — direct lattice analogue of the v0 Σ-protocol on the new commitment scheme.
2. **STARKs** — transparent, PQ-by-default, but heavier proofs (~50-150 KB) and slower verifiers.
3. **Hybrid (PLONK over a PQ-secure cryptographic compiler)** — open research.

**Recommendation:** lattice-Σ first, with STARK as a parallel verifier option for counterparties that want the strongest PQ assumptions.

### §4.4 — Signatures

Replace Ed25519 with one of the NIST PQC signature standards:

1. **ML-DSA (Dilithium)** — fast verify, moderate sign cost, ~2.5-5 KB signatures. **Recommended default.**
2. **SLH-DSA (SPHINCS+)** — stateless hash-based, conservative assumptions, ~8-16 KB signatures.
3. **FN-DSA (Falcon)** — small signatures (~700 B) but complex implementation with side-channel concerns.

**Recommendation:** ML-DSA as primary. SLH-DSA as the conservative fallback for high-stakes envelopes (audit, judicial counterparties).

### §4.5 — Hybrid mode

During transition (estimated 3-5 years), envelopes MAY be **dual-signed**: Ed25519 + ML-DSA. Counterparties that have only Ed25519 verifying capability accept the v0 signature; PQ-aware counterparties verify both. The wire format extension is:

```json
{
  ...,
  "operator_signature": "ed25519:<hex>",
  "operator_signature_pq": "ml-dsa:<hex>"
}
```

Hybrid mode terminates on the cutover date, at which point ML-DSA-only envelopes are minted and verifiers must support PQ signatures.

## §5 — Triggers

The plan moves through phases on these triggers (any of which fires the next phase):

| Phase | Triggers |
|---|---|
| Phase 0 (today) | Plan published; v0 in production. |
| Phase 1: Hybrid spec | Calm Foundation publishes lattice-Σ + ML-DSA wire format `calm-witness/wire/v1`. Target: 2027. |
| Phase 2: Dual-signing | Operator wallets emit Ed25519 + ML-DSA signatures. Target: 2028. |
| Phase 3: PQ-default | New envelopes are PQ-only. v0 envelopes still verifiable. Target: 2030, or 6 months after the first publicly-credible CRQC threat report, whichever is sooner. |
| Phase 4: v0 sunset | v0 verifier support removed from reference implementation. Target: 2035, or 24 months after Phase 3, whichever is later. |

**Acceleration triggers** that immediately escalate to Phase 3:

- A credible peer-reviewed paper demonstrating a quantum attack on Ed25519 or MODP-2048.
- NIST publication of an emergency PQC migration advisory naming the v0 primitives.
- Confirmed nation-state CRQC capability per multiple intelligence agency advisories.

## §6 — Migration mechanics

### §6.1 — Operator key rotation

Each operator publishes:

- Their existing Ed25519 public key.
- A new ML-DSA public key.
- A `key_migration_attestation` record on the chain, signed by Ed25519, asserting "this Ed25519 fingerprint maps to this ML-DSA fingerprint." Any counterparty holding the Ed25519 fingerprint can now look up the ML-DSA fingerprint.

### §6.2 — Predicate namespace rotation

Predicates whose evaluator uses commitment-bound parameters (e.g., `biometric_match_within(τ)`) get re-minted under `cwp.v1.*` with the new commitment scheme. Pure deterministic predicates (`in_baseline_24h`, `cognitively_atypical_baseline`) retain their semantics; their IDs migrate to `cwp.v1.*` purely to mark the wire-version bump.

### §6.3 — Chain continuity

The user_state.jsonl chain does NOT migrate. SHA-256 is PQ-secure; the chain remains valid forever. Only the cryptographic *envelope* layer migrates.

### §6.4 — Conformance

A reference v1 implementation MUST:

- Accept v0 envelopes (verify via the original primitives).
- Mint v1 envelopes (under PQ primitives).
- Emit a deprecation warning when handling v0.

A counterparty that wants to verify v0 envelopes after Phase 4 must vendor in the v0 verifier code from the archived reference.

## §7 — What we will NOT do

1. **Roll our own PQC.** We adopt NIST-standardized algorithms only. No proprietary lattice schemes, no hand-tuned parameters.
2. **Ship before audits.** v1 will not ship until the implementations have passed independent cryptography audits (Everest 90).
3. **Skip hybrid mode.** A direct cutover from Ed25519 to ML-DSA without a hybrid window would orphan counterparties that haven't updated. Hybrid is mandatory.
4. **Hide the migration.** The migration plan is public, the timeline is published, and any acceleration trigger is publicly announced before the phase advances.

## §8 — Open questions

- **Optimal commitment scheme.** Lattice vs. STARK-based vs. hybrid. The lattice family currently has the operational lead but the field is moving.
- **Right time to start dual-signing.** Earlier dual-signing pays compute cost upfront and limits the harvest-now window; later saves cost but increases retroactive-forgery risk if CRQCs arrive faster than expected.
- **Mobile-vault impact.** ML-DSA signing is ~5-10× slower than Ed25519 on commodity ARM. Mobile budget (Everest 89) needs to be revisited under PQ assumptions.

These are tracked as separate Everests for v1 planning.

— Calm, 2026-05-20
