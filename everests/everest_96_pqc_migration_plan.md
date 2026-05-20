# Everest 96 — Post-Quantum Migration Plan

*Phase VIII — Governance & Scale. Prereq: Everest 81 (production impl) — soft-met by v0.*

Calm Witness v0 rests on the discrete-logarithm assumption over Ristretto255. A sufficiently large quantum computer running Shor's algorithm breaks discrete log in polynomial time. This summit specifies the migration path BEFORE that computer exists, so deployed Calm Witness disclosures do not become a future single-day liability.

## §1. The threat model — what breaks first

| Primitive | Quantum risk | Likely break year |
|---|---|---|
| Pedersen commitment (binding) | YES — Shor on ECDLP | first cryptographically-relevant quantum computer |
| Pedersen commitment (hiding) | NO — information-theoretic | safe |
| Σ-protocol soundness | YES — Shor on ECDLP | same as Pedersen binding |
| Schnorr signatures (FROST, Ed25519) | YES — Shor on ECDLP | same |
| Sigsum transparency log | NO if backed by hash-based signing | safe under Grover (key sizes doubled) |
| Halo2 (Poseidon hashes) | NO — Grover-bound, halve security | safe under doubled-size variants |
| Bulletproofs range proofs | YES — discrete log over G | same as Pedersen binding |

So: every Pedersen / Schnorr / Bulletproof piece needs replacement; every hash-and-Merkle piece is fine (with constant-factor adjustments).

## §2. Replacement primitives (v2 candidates)

| Role | v0 (DL-based) | v2 (PQC) | Status |
|---|---|---|---|
| Commitment | Pedersen on Ristretto255 | Lattice-based: Ajtai or FALCON-style; alt: hash-based (Merkle commit) | research-grade as of 2026 |
| Membership proof (Σ-protocol) | Schnorr on Ristretto255 | LWE-based or hash-based ring sig (sphincs+ family) | NIST standardised SPHINCS+ (FIPS 205, 2024) |
| Range proof | Bulletproofs | Lattice-based range proof (e.g., Lyubashevsky-style) | research-grade as of 2026 |
| Signature (operator identity) | Ed25519 | ML-DSA (FIPS 204, formerly Dilithium) | NIST standardised 2024 |
| Threshold signature (FROST) | FROST-Schnorr | FROST-ML-DSA (research) or threshold SPHINCS+ | research as of 2026 |
| Transparency log | SHA-256 + RFC 6962 | unchanged (Grover halves security; SHA-384 or SHAKE256 in v2) | trivial migration |

NIST standardised the underlying KEMs and signatures in 2024 (FIPS 203, 204, 205). The cryptographic community is ~24 months into building higher-level protocols (commitments, ZK, threshold) on top of those primitives. By the time Calm Witness needs to migrate, the higher-level layer should be production-ready.

## §3. Migration sequencing (when to start)

| Trigger | Action |
|---|---|
| 2026 (now) | Document the plan (this summit). |
| 2027–2028 | Track PQC commitment / range-proof research; pin candidate libraries. |
| 2029–2031 | Implement a parallel v2 stack; ship as opt-in for new vaults. |
| First credible quantum-relevance signal | Hard-cutover: every new disclosure issued under v2; v0 verifiers still accept legacy responses but mark them with a `legacy_v0` flag. |
| ~24 months after cutover | Verifiers stop accepting legacy v0 responses; principals re-enroll under v2. |

The pacing is deliberate: too early and we burn cycles on draft standards; too late and pre-quantum recordings of v0 responses become exploitable. The 2029–2031 implementation window is calibrated to NIST's current 2030 deprecation guidance for ECDLP-based primitives.

## §4. Forward-compatibility hooks shipped in v0

v0 disclosure envelopes already carry a `wire_version` field. v2 will be `wire_version: 2`; verifiers can advertise their accepted versions and operators can produce both during the migration window.

Field-level: `pedersen_commitment_hex` becomes `commitment_hex` (algorithm-agnostic name) in v0.1 if not already, so the v2 substitution requires no field rename. The interpretation is governed by the `wire_version`.

CredexAI VCs (E22) ship today with Ed25519 signatures; v2 VCs ship with ML-DSA signatures. The DID method (`did:credexai:v1` → `did:credexai:v2`) bumps to signal.

## §5. What this DOES NOT do

- It does not promise that Calm Witness disclosures issued under v0 will be safe forever. They are safe under current-day cryptanalysis; they will become extractable once a cryptographically-relevant quantum computer exists. Principals concerned about long-term forward secrecy should not rely on Calm Witness for irrevocable life-or-death scenarios beyond the 2029–2031 migration window.
- It does not pre-commit to a specific PQC primitive — that choice waits for the higher-level cryptographic community to settle the 2026–2028 wave of research-grade constructions.
- It does not handle "harvest now, decrypt later." Calm Witness disclosures are bits, not encrypted blobs; the worst case for harvesting is that an adversary learns which historical predicate values an operator emitted. That's a meaningful leak, but one bounded by the principal's disclosure history; Sigsum already exposes the chain head, so an adversary already has a finite history.

## §6. Acceptance test

This is a design summit. The runtime acceptance lands with v2:

```bash
$ python3 cli.py verify-chain --wire-version 2
$ python3 cli.py eval-predicate --wire-version 2 ...
```

For v0, acceptance is the existence of this plan and the forward-compat hooks in place (wire_version field, algorithm-agnostic field naming candidate, VC method-bump path).

— Calm, 2026-05-20
