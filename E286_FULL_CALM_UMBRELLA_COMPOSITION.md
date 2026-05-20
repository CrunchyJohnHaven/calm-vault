# Everest 286 — Full Calm Umbrella Composition Spec

**Joint transcript composing all four sister primitives: Calm Pact (directive equality) + Calm Witness (state attestation) + ZKAC (values alignment) + Calm Audit (action-history disclosure).**

Companion to [`CALM_ZKAC_EVERESTS_106_305.md`](CALM_ZKAC_EVERESTS_106_305.md), Phase XVIII. The final spec the route climbs toward.

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.**

---

## 1. The thesis

Each Calm primitive answers a different question for two agents trying to cooperate:

| Primitive | Question | Status |
|---|---|---|
| Calm Pact | Do we share categorically equivalent primary directives? | v0 shipped (sister repo) |
| Calm Witness (ZKBB-User) | Is the principal themself, in baseline? | v0 working code |
| ZKAC | Are the principals' values aligned within tolerance? | v0 working code |
| Calm Audit | What did this agent actually do in the past? | spec deferred (Everest 301) |

A counterparty deciding "should I cooperate with this agent?" needs ALL FOUR answered. This Everest specifies the joint transcript that delivers all four in one round trip, with atomic accept-or-reject semantics.

## 2. Threat model deltas

Composing four proofs introduces composition-specific threats:

- **Replay across primitives.** A Calm Pact proof from session X reused in session Y.
- **Cross-primitive substitution.** Using one principal's Witness proof with another's Values proof.
- **Selective failure.** Counterparty wants only 3 of 4 to verify; protocol must refuse partial.

Defenses:

- **Session nonce binding.** A single 32-byte session_nonce binds into every proof's Fiat-Shamir context. Reuse fails because the FS challenge changes.
- **Chain head pinning.** All four proofs reference the same chain head. A principal cannot use different chain heads for different proofs in the same session.
- **Atomic accept.** The verifier returns aligned-bit = AND of all four primitive bits. If any sub-proof fails, the whole transcript is rejected.

## 3. The wire format

```json
{
  "kind": "calm_umbrella_transcript_v0",
  "session_nonce_hex": "<32-byte hex>",
  "issued_at_utc": "2026-05-20T18:00:00Z",

  "principals": {
    "calling": "<CredexAI principal id of P>",
    "counterparty": "<CredexAI principal id of C>"
  },

  "chain_head": {
    "seq": <int>,
    "hash_hex": "<64-char hex>",
    "anchor_proof_hex": "<Sigsum inclusion proof>"
  },

  "pact_proof": {
    "directive_class_id": "<string>",
    "sigma_proof_bytes_hex": "<hex>",
    "operator_id": "<signer>"
  },

  "witness_proof": {
    "predicate_id": "cwp.v0.in_baseline_24h",
    "bit": 1,
    "commitment_hex": "<hex>",
    "sigma_proof_bytes_hex": "<hex>"
  },

  "zkac_proof": {
    "predicate_id": "cwp.v0.values_aligned_within",
    "bit": 1,
    "tolerance_fingerprint": "<64-char hex>",
    "alignment_proof_hex": "<hex>",
    "htcr_session_data": {
      "tolerance_commit_seq": <int>,
      "principal_commit_seq": <int>
    }
  },

  "audit_proof": {
    "predicate_id": "cwp.v0.no_harm_evidence_any",
    "bit": 1,
    "harm_absence_attestation_hex": "<hex>",
    "window_seconds": <int>
  },

  "operator_sig_hex": "<Ed25519 signature>"
}
```

## 4. The verification flow

```
def verify_umbrella(transcript: dict, counterparty_state) -> dict:
    checks = {}

    # 1. Schema + session nonce + chain-head sanity.
    checks["schema_valid"] = is_valid_umbrella_schema(transcript)
    checks["session_nonce_fresh"] = nonce_not_seen_before(transcript["session_nonce_hex"])
    checks["chain_head_anchored"] = verify_sigsum_anchor(transcript["chain_head"])

    # 2. Each primitive's individual verification.
    checks["pact_verifies"] = verify_pact_proof(transcript["pact_proof"], context)
    checks["witness_verifies"] = verify_witness_proof(transcript["witness_proof"], context)
    checks["zkac_verifies"] = verify_zkac_proof(transcript["zkac_proof"], context)
    checks["audit_verifies"] = verify_audit_proof(transcript["audit_proof"], context)

    # 3. Cross-primitive binding: all four reference the same chain head + nonce.
    checks["all_proofs_share_chain_head"] = (
        transcript["pact_proof"].get("chain_head_hash") ==
        transcript["witness_proof"].get("chain_head_hash") ==
        transcript["zkac_proof"].get("chain_head_hash") ==
        transcript["audit_proof"].get("chain_head_hash") ==
        transcript["chain_head"]["hash_hex"]
    )
    checks["all_proofs_share_session_nonce"] = (
        all_proofs_bind_to(transcript["session_nonce_hex"])
    )

    # 4. Operator signature over the full transcript.
    checks["operator_sig_valid"] = verify_ed25519_over(
        transcript_minus_operator_sig, transcript["operator_sig_hex"],
    )

    # 5. Atomic accept: ALL bits AND all binding checks.
    checks["accept_atomic"] = all(checks.values()) and all(
        proof.get("bit") == 1 for proof in (
            transcript["witness_proof"],
            transcript["zkac_proof"],
            transcript["audit_proof"],
        )
    )

    return checks
```

The `accept_atomic` field is the single load-bearing output. If True, the counterparty acts. If False, the counterparty does not, and the failing check tells them why.

## 5. Partial-accept policy (v0 default: refused)

A counterparty MIGHT want to accept a transcript with `pact_verifies = True, witness_verifies = True, zkac_verifies = True, audit_verifies = False`. v0 default: NO. The four primitives are co-load-bearing; partial trust opens defection surfaces.

Counterparties wanting partial verification should request the relevant single primitive (e.g., just Calm Witness if they only care about state) instead of the umbrella.

## 6. Performance budget (v0 on MODP-14, no Ristretto)

| Component | Prove time | Verify time | Transcript size |
|---|---|---|---|
| Pact proof | ~50ms | ~10ms | ~1KB |
| Witness proof | ~200ms | ~50ms | ~3KB |
| ZKAC proof (10-dim alignment with range proofs) | ~70s | ~7s | ~50KB |
| Audit proof | ~100ms | ~50ms | ~2KB |
| **Total umbrella** | **~70s** | **~7s** | **~56KB** |

Ristretto migration (Everest 96) targets ~1.5s total / ~2KB transcript.

## 7. Composition with Calm Pact (sister repo)

Calm Pact lives at `/Users/johnbradley/AllData/calm_vault_market/calm_pact/`. Its v0 protocol provides:
- `pact_prove(directive_class, principal_credential)` → PactProof
- `pact_verify(proof, expected_directive_class)` → bool

The umbrella transcript carries the PactProof verbatim plus the cross-binding fields. No changes to Calm Pact are required for v0 composition.

## 8. Composition with Calm Audit (Everest 301 placeholder)

Calm Audit is the third sister primitive — action-history selective disclosure. Not yet specified beyond placeholder. The umbrella transcript currently uses the harm-aggregate predicate (`cwp.v0.no_harm_evidence_any`) as a v0 stand-in for Calm Audit. v1 will replace this with the actual Audit primitive.

## 9. Implementation roadmap

| Step | Owner | Effort | Status |
|---|---|---|---|
| Compose existing ZKAC + Witness in one transcript | this session | M | ✅ structure spec done |
| Add Pact composition | sister-repo agent | M | spec ready |
| Add Audit stand-in via E165 | this session | S | ✅ predicate available |
| Reference impl in Rust | future smart agent | XL | open |
| Live multi-process demo | future smart agent | L | open |

## 10. What this Everest is NOT

- Not a guarantee that all four primitives are equally well-defended. Each has its own threat model.
- Not a substitute for human governance. The umbrella delivers a bit; humans interpret.
- Not stable until Calm Audit (E301) lands. The v0 stand-in is fine for now but the audit primitive may require schema evolution.

---

**Authored by Calm, 2026-05-20. Pending Ristretto migration (Everest 96) and Calm Audit v0 (Everest 301).**
