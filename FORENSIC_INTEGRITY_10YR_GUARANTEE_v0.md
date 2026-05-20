# Calm-Suite Forensic Integrity Guarantee — 10-Year Horizon (v0)

**Draft v0 · 2026-05-20 · Calm**
**DESIGN-BAG of Everest 180 in [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**
**Composes:** Everest 28 (hash chain), Everest 30 (Sigsum), Everest 31 (Roughtime), Everest 32 (encrypted replication), Everest 33 (corruption recovery), Everest 68 (operator identity), Everest 96 ([`POST_QUANTUM_MIGRATION_PLAN_v0.md`](POST_QUANTUM_MIGRATION_PLAN_v0.md)), Everest 251 (25-year identity continuity).

## §0 — The promise

For any Calm-suite envelope **e** issued between 2026 and 2036, **any third party in 2036 holding only the public coordinates** (chain head, Sigsum log inclusion proof, operator public-key history, foundation-published cryptographic transitions) **must be able to verify the same set of claims about e that a contemporary verifier could verify in 2026.**

The promise is **forensic**, not legal. It does not bind any state, does not survive coercion of all parties simultaneously, and does not extend beyond the cryptographic claims. It is sufficient for: post-hoc audit of historical disclosures; reconstruction of vault state from public substrate; cryptographic refutation of forged-after-the-fact envelopes; principal-side proof of what was disclosed and what was not.

## §1 — Why 10 years is the right horizon

- **Statute of limitations** for the most common civil claims that would touch attested disclosure (fraud, breach of contract, defamation) caps at ~6 years in most US jurisdictions; 10 years covers the long tail.
- **One cryptographic-primitive migration cycle** (PQ transition) plus runoff — per [`POST_QUANTUM_MIGRATION_PLAN_v0.md`](POST_QUANTUM_MIGRATION_PLAN_v0.md), Phase 4 v0-sunset is targeted 2035 with 24-month runoff to 2037.
- **Foundation operating lifetime guarantee** (Everest 244, operational continuity plan) is committed to ≥ 10 years even if the founder is unavailable for ≥ 6 months continuously.
- **Audit-firm record retention** (SOC 2 / ISO 27001) is typically 7-10 years; aligning Calm-suite forensic guarantees with audit-firm record retention simplifies cross-referencing.

50-year cryptographic agility (Everest 252) is the longer horizon; 10-year forensic integrity is the **operational** horizon over which we commit to *full reconstruction*.

## §2 — Threat model for the 10-year horizon

**Active adversaries:**

1. **Algorithm-deprecation adversary.** SHA-256 + Ed25519 + Pedersen-on-MODP-2048 + Σ-protocol are all assumed secure today. By 2036, any could be cryptographically compromised (most likely Ed25519 + Pedersen under a CRQC). The forensic claim must survive the deprecation of any single primitive.
2. **Foundation-disappearance adversary.** Calm Witness Foundation could dissolve or be captured. The §1 §3 §4 substrate (Sigsum logs + the published public-key history + the conformance vectors) must outlive the foundation.
3. **Sigsum-operator collapse.** Sigsum is operated by a set of independent witnesses. By 2036, any subset could go offline. The chain-head publication strategy (Everest 30) requires ≥ 5 independent operators across ≥ 3 jurisdictions to mitigate.
4. **Coerced key-disclosure adversary.** A future state actor compels the operator to disclose past signing keys. The forensic integrity claim distinguishes between *what was signed* (provable from the chain + public key) and *what the principal authorized* (provable only with the principal's contemporaneous cooperation, which the state actor cannot retroactively coerce).
5. **Storage-corruption adversary.** Disk/cloud bit-rot. Mitigated by Everest 32 (encrypted replication) + Everest 33 (corruption recovery from Sigsum + ≥ 2 replicas).
6. **Vendor-lock-in adversary.** A cloud vendor (used by the operator or by Sigsum witnesses) restricts access by 2036. Mitigated by Foundation policy (Everest 95 §3) requiring ≥ 3 independent mirror coordinates including ≥ 1 self-hosted by the foundation.
7. **Specification drift.** The protocol's interpretation of "valid envelope" could change. Mitigated by **immutable conformance vectors** committed to a public transparency log at each version release; a 2036 verifier uses the vectors that were valid at envelope-creation time, not 2036's vectors.

**Out of scope:**

- A simultaneous compromise of every cryptographic primitive (mass cryptographic collapse). If 2036's adversary can break SHA-256, Sigsum, Ed25519, *and* the PQ replacements simultaneously, the forensic guarantee fails — as do most other digital-signature systems.
- Coercion of the principal across 10 years (rubber-hose attack).
- Loss of all human knowledge of the protocol's existence (civilizational discontinuity).

## §3 — Required artifacts that must survive

For each envelope **e** issued at time **t**, the following must be retrievable in 2036:

| Artifact | Custodian | Retention requirement |
|---|---|---|
| The envelope **e** itself (JSON bytes) | Principal vault + counterparty | Forever (counterparty retains for ≥ 30 days per Everest 69; principal retains forever) |
| Chain head at time **t** | Sigsum witnesses + foundation mirror + IPFS pin | ≥ 10 years post-issuance |
| Operator's public key history | Foundation public-key transparency log | Forever |
| Sigsum inclusion proof for the chain head | Sigsum + foundation mirror | ≥ 10 years post-issuance |
| Roughtime timestamp for the chain head | Roughtime servers + foundation mirror | ≥ 10 years post-issuance |
| Cryptographic-primitive specification at version of issuance | Foundation-published versioned spec | Forever |
| Conformance vectors for the version of issuance | Foundation-managed git + IPFS pin + 3 named archive partners | Forever |
| Predicate vocabulary at version of issuance | Foundation registry + audit-decision log | Forever |
| Predicate evaluator implementation at version of issuance | Open-source repo + Foundation mirror + Software Heritage | Forever |

**"Forever" obligations** are realized via:

- Internet Archive (Wayback + Software Heritage).
- ≥ 3 named university archive partners (per Everest 247).
- A 100-year retention contract with named archive partners (Everest 253).

## §4 — Per-component continuity guarantee

### §4.1 — Chain bytes

The principal's `user_state.jsonl` chain is append-only on principal hardware. Foundation provides:

- A spec (`USER_STATE_PROTOCOL.md`) versioned and republished at each release.
- A reference verifier (`calm_witness/verify_chain.py`) versioned + tagged at each release; the 2036 verifier uses the 2026-era code from the git tag if needed.

Principal retention is principal-controlled. Foundation does NOT custody principal chains.

### §4.2 — Sigsum chain-head publication

Foundation specifies (Everest 93):

- ≥ 3 independent Sigsum witnesses across ≥ 3 jurisdictions.
- Each witness retains its log for ≥ 10 years; the Foundation maintains a redundant mirror for ≥ 20 years.
- Any 1 surviving witness + 1 mirror is sufficient to reconstruct chain-head inclusion proofs.

### §4.3 — Operator public-key history

Foundation maintains a **transparency log** (separate from Sigsum) recording every operator-key issuance, rotation, and revocation. The log is itself Sigsum-anchored. A 2036 verifier holding any operator fingerprint can resolve to: (a) the public key bytes, (b) the time of issuance/rotation/revocation, (c) the signed delegation chain.

### §4.4 — Roughtime / VDF anchoring

Roughtime servers may go offline. Mitigation: Foundation persists Roughtime attestations into a foundation-managed monthly batch (a "Calm Foundation time anchor" record signed by FROST t-of-n board members) that survives independently. A 2036 verifier uses the foundation batch when Roughtime servers are unreachable.

### §4.5 — Cryptographic-primitive migration

Per [`POST_QUANTUM_MIGRATION_PLAN_v0.md`](POST_QUANTUM_MIGRATION_PLAN_v0.md), an envelope **e** issued under v0 primitives remains verifiable under the v0 primitive set. The 2036 verifier:

- Identifies envelope's `wire_version`.
- Loads the v0 cryptographic-spec doc (from foundation archive).
- Loads the v0 reference verifier (from git tag).
- Verifies under the v0 primitives, even if v1/v2 have superseded them.

If the v0 primitive is **cryptographically broken** by 2036 (e.g., Ed25519 by a CRQC), the forensic claim is **degraded** — the verifier can confirm "this envelope was signed under the v0 primitive set" but cannot confirm signature soundness. The foundation publishes a `cryptographic_degradation_advisory` record naming the affected primitive and the effective date.

### §4.6 — Conformance vectors + evaluator code

For each protocol version, the Foundation publishes:

- A frozen set of conformance test vectors (input envelope, expected verifier outcome).
- The reference verifier code at a tagged git commit.
- A binary hash of the conformance vectors anchored in Sigsum.

A 2036 verifier can: download the v0 reference code (from git mirror or Software Heritage), run it against the conformance vectors (from foundation mirror or IPFS pin), confirm the vectors are unchanged (Sigsum anchor), and then verify **e** under the same code-vector pair.

## §5 — Reconstruction protocol

Given an envelope **e** dated 2027, a 2036 third-party verifier executes:

```
1. Identify e.wire_version. Locate the v_e spec at foundation archive.
2. Identify e.issued_by_operator (fingerprint).
3. Resolve fingerprint → public key via operator key-history transparency log.
4. Identify e.chain_head. Resolve via Sigsum inclusion proof (or foundation mirror).
5. Resolve Roughtime timestamp (or foundation time-anchor batch).
6. Download v_e reference verifier (git tag for v_e).
7. Run reference verifier against e + (request, operator-public-key, chain-head,
   Sigsum-inclusion-proof, Roughtime-attestation).
8. If verifier returns ok=true: forensic integrity holds for e.
   If verifier returns ok=false: forensic integrity fails; e is invalid or tampered.
   If unable to retrieve any required input: forensic integrity is INCONCLUSIVE;
   record which input was missing.
```

Step 8's three-outcome structure is load-bearing. A 2036 verifier MUST distinguish between *verified-false* and *cannot-verify*. The Calm-suite forensic guarantee is "you can always reach one of these three outcomes" — not "you will always reach verified-true."

## §6 — Failure modes + recovery procedures

| Failure | Detection | Recovery |
|---|---|---|
| Sigsum witness offline | Verifier attempts ≥ 2 witnesses; if all unavailable, falls through to foundation mirror | Foundation mirror is the runoff |
| Foundation mirror offline | Verifier attempts named archive partners (Internet Archive, Software Heritage, university partners) | Multiple archive partners; ≥ 1 surviving sufficient |
| Operator key history corrupted | Verifier detects via Sigsum anchor on the key-history log | Reconstruct from the Sigsum anchor + any surviving operator-side records |
| Reference verifier code lost | Verifier downloads from Software Heritage permanent archive | Software Heritage retains source forever |
| Conformance vector hash mismatch | Verifier detects bit-rot in the foundation mirror | Cross-reference against ≥ 2 archive partners; use the majority |
| CRQC breaks a v0 primitive | Foundation publishes degradation advisory at break time + 30 days | All v0-era envelopes flagged as cryptographically-degraded; principals notified; legal advice published |
| Foundation dissolved | Successor body (per Everest 95 §8) takes over registry + mirrors | Successor body's first act: publish a `governance_handover` record on the public chain |

## §7 — Audit + verification procedure for third parties

Any third party in 2036 verifying the forensic integrity claim performs the §5 reconstruction for a sample of envelopes (random sample size N = √(total envelope count)) and reports:

- Number of envelopes that fully verified.
- Number that verified-false (these are invalid envelopes from 2026-2036 that should be tombstoned).
- Number that returned INCONCLUSIVE (and the reason: which input was missing).

If ≥ 95% of the sample verifies cleanly and < 1% are verified-false, the forensic integrity guarantee holds for that audit window. The Foundation commits to publishing third-party audit results on its transparency log.

## §8 — Composition with PQ migration

A 2027 envelope signed under Ed25519 remains forensically verifiable as long as Ed25519 has not been broken. Once Ed25519 is broken, the envelope is **cryptographically degraded** but still **chain-of-custody verifiable**:

- The chain-head publication into Sigsum at issuance time **predates** the Ed25519 break.
- The chain-head is hash-protected (SHA-256, PQ-safe).
- Therefore: a 2036 verifier can confirm "the envelope existed in the published form at time t" even if it cannot confirm "the envelope's signature was produced by the principal's key" once Ed25519 falls.

This **partial forensic integrity** is the right floor under post-quantum threats. The Foundation publishes guidance distinguishing "fully forensic" from "chain-of-custody only" envelope categories at each cryptographic transition.

## §9 — Composition with Foundation succession

If the Foundation dissolves and a successor body takes over, the forensic guarantee continues iff:

1. The successor publishes a `governance_handover` record on the public chain, signed by ≥ m-of-n of the original Foundation board.
2. The successor commits, on the chain, to honoring the §3 retention obligations and the §5 reconstruction protocol.
3. The successor mirrors (or causes to be mirrored) the foundation-managed substrates within 90 days of takeover.

If the Foundation dissolves WITHOUT a successor, the Internet Archive + Software Heritage + named university partners hold the §3 substrates indefinitely under the Foundation's pre-paid 100-year retention contract (Everest 253).

## §10 — Open problems

1. **Roughtime persistence past 10 years.** Roughtime is designed for ephemeral attestation. The foundation time-anchor batch (§4.4) is the patch; a more principled long-horizon time-anchoring primitive is an open research question.
2. **CRQC arrival before all envelopes have been re-anchored to PQ primitives.** Mitigation: degraded-but-verifiable status per §8; better mitigation is faster PQ migration (Everest 96 Phase 2 acceleration trigger).
3. **Civil-society oversight of the foundation's archival commitments.** §3 obligations are foundation-discretionary; a stronger commitment would bind the foundation under contract to its archive partners. Pending Everest 247 + 253.
4. **Cost of indefinite retention.** Holding the §3 substrates for 100 years is not free. The foundation funding plan (Everest 243) must include a long-horizon endowment specifically for archival.

## §11 — What this guarantee does NOT do

- It does not guarantee that 2036 third parties will *care* about the envelope's content.
- It does not guarantee that disputed envelopes can be litigated under 2036 law.
- It does not guarantee that the principal's vault chain survives the principal's death (that's Everest 255).
- It does not protect against a 2036 government that orders the Foundation's archival partners to delete records (this is why ≥ 3 named partners across jurisdictions matters; no single state can take all of them down).
- It does not extend to envelopes signed under tombstoned predicates (those are retained for record but explicitly marked as untrustworthy from time of tombstoning).

— Calm, 2026-05-20
