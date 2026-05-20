# SUMMIT 180 — Forensic Integrity Guarantee (10-Year Durability)

**Calm Witness + ZKAC | Phase XII (Cooperation & Generosity) · Everest 180**

**Status:** IN_PROGRESS → BAGGED (this session)  
**Claimant:** Calm  
**Authored:** 2026-05-20  
**Durability Claim:** A Calm Witness disclosure proof issued today (2026) MUST remain cryptographically verifiable and tamper-evident in 2036 and beyond, even after expected cryptographic migrations (post-quantum signatures, hash-algorithm agility, commitment-scheme transitions, transparency-log reanchoring).

---

## §1 — Header & Phase Context

**EVEREST:** 180 — Mutual-Aid Records and Durable Forensic Proof  
**KIND:** Chain record type `mutual_aid` + administrative artifact for archive durability  
**PREREQS:** E28 (hash-chain), E30 (Sigsum anchoring), E96 (post-quantum migration plan), E104b (vault identity), §2–4 of `CALM_WITNESS_SCOPE_STATEMENT.md`  
**EFFORT:** M  
**COMPOSITION:** T-E180.1–5 test cases; integration with E96 PQ-migration phases; replication layer per §4.3

This everest closes the forensic-integrity guarantee: when a principal discloses mutual-aid evidence (coalition records, group-response logs, jointly-authored outcomes) to a counterparty in 2026, that disclosure must survive the cryptographic transitions of the next decade and remain a tamper-evident attestation in 2036.

The core claim: **one-way ratchet on proof durability**. We trade real cost (archive replication, periodic re-anchoring, grace-window overlaps) to guarantee that no principal, operator, or hostile force can retroactively invalidate or forge a 2026 disclosure once 2036's primitives are live.

---

## §2 — Overview: The Durability Claim

### 2.1 — What must survive

When a mutual-aid record is chain-anchored today:

- The record itself (immutable in the append-only jsonl)
- The per-record hash commitment
- The hash-chain head state (Merkle ancestry)
- The Sigsum log entry tying the head to a global timestamp
- The operator's signature over the disclosure envelope
- The predicate evaluator's consent binding

All five artifacts must remain **cryptographically verifiable and attested as unmodified** in 2036+, even if the underlying hash algorithm (SHA-256), signature scheme (Ed25519), or commitment structure (Pedersen/MODP) is deprecated or theoretically broken.

### 2.2 — The threat: harvest-now-decrypt-later

Post-quantum migration plan (Everest 96) explicitly models **harvest-now-decrypt-later (HNDL)** adversaries:

- Adversary captures Calm Witness disclosures, signatures, commitments in 2026.
- A cryptographically-relevant quantum computer (CRQC) becomes available in 2034.
- Adversary uses Shor's algorithm to recover:
  - Ed25519 private keys from captured public keys → forge envelopes retroactively.
  - Pedersen blinding factors from commitments → open and re-attribute disclosures.
  - Σ-protocol discrete-log relationships → produce false proofs.

Without this guarantee, every 2026 mutual-aid disclosure becomes forgeable in 2036. The guarantee prevents that: even if Ed25519 is broken, a 2026 disclosure's integrity is attested in a tamper-evident log that survived to 2036 intact.

### 2.3 — Durability layers

Durability is achieved by composing five independent mechanisms:

1. **Archive replication** (§4.3): ≥3 geographically and jurisdictionally distributed mirror copies of every chain record.
2. **Transparency-log re-anchoring** (§3.2): Periodic (quarterly) Sigsum commitments that bind the entire chain-head + archive states to a freshness witness.
3. **Dual-signature grace windows** (§3.3): During PQ migration, disclosures are signed Ed25519 + ML-DSA simultaneously; verifiers accept both during the overlap period.
4. **Curve-migration grace windows** (§3.4): When commitment schemes or hash algorithms change, old & new coexist in parallel proofs until deprecation.
5. **Hash-algorithm agility** (§3.5): Chain records carry algorithm tags; verifiers accept SHA-256 + SHA-3 side-by-side during transition.

Any one layer failing (e.g., archive divergence, Sigsum log operator compromise) is caught by the others. All five must simultaneously fail for a disclosure to become unverifiable.

---

## §3 — Architectural Mechanism: Bridge & Re-Anchor

### 3.1 — Baseline envelope structure (v0)

Today's mutual-aid disclosure carries:

```json
{
  "mutual_aid_record": {
    "kind": "mutual_aid",
    "seq": 4521,
    "timestamp": "2026-05-20T14:32:18Z",
    "parties": ["principal_A", "principal_B", "principal_C"],
    "action": "disaster_response_community_network",
    "witness": "operator_id_04b",
    ...
  },
  "chain_head": {
    "height": 4521,
    "head_hash": "sha256:<hex>",
    "parent_hash": "sha256:<hex>",
    "timestamp_sigsum": "2026-05-20T14:35:00Z",
    "sigsum_leaf_index": 891247
  },
  "proofs": {
    "predicate": "cwp.v0.mutual_aid_evidence(window=90d)",
    "predicate_proof": "<schnorr_π>",
    "commitment": "pedersen:rfc3526:2048:<hex>"
  },
  "operator_signature": "ed25519:<hex>"
}
```

The entire envelope is signed by the operator's Ed25519 key. Verification requires:

- Ed25519 public-key verification (deterministic, no secrets exposed).
- Pedersen commitment opening (the commitment algorithm itself, verifiable by anyone).
- Schnorr Σ-protocol bit-proof (honest-verifier interactive, reduced to non-interactive via Fiat-Shamir).

All three are broken under a CRQC via Shor's discrete-log recovery. The hash (SHA-256) is not broken; Grover gives ~2^128 effective security.

### 3.2 — Re-anchoring: Sigsum + Roughtime composition

Every 90 days (or when archive state diverges), the chain head is **re-anchored** to Sigsum:

1. **Calm vault operator** computes a new transparency-log entry:
   ```json
   {
     "kind": "archive_durability_anchor",
     "timestamp": "2026-08-18T11:22:33Z",
     "chain_head_hash": "sha256:<hex>",
     "archive_mirror_hashes": [
       "sha256:<mirror_1_hash>",
       "sha256:<mirror_2_hash>",
       "sha256:<mirror_3_hash>"
     ],
     "pq_bridge_version": "calm-witness/pq_bridge/v0"
   }
   ```

2. **Sigsum log** appends this entry. The log maintainer (a trusted neutral party, e.g., DigitalOcean or a Linux Foundation consortium) signs the tree head including this leaf.

3. **Roughtime** is queried to anchor the Sigsum tree head to UTC time. The Sigsum operator witnesses that "at this moment, the log contained this entry."

4. **Re-anchoring repeats**: every 90 days, a fresh anchor commits the current state of all archive mirrors + the post-quantum bridge version.

By 2036, a 2026 disclosure has been re-anchored ≥40 times (10 years × 4 per year = 40 anchors). Each anchor is **orthogonal verification** — it doesn't rely on Ed25519 or Pedersen being unbroken; it relies only on the Sigsum log, the Roughtime protocol, and SHA-256, all of which survive CRQC attacks.

### 3.3 — Dual-signature periods (Ed25519 + ML-DSA overlap)

In 2027–2030 (Phase 2–3 of the PQ-migration plan), new envelopes are signed **twice**:

```json
{
  ...same body as above...,
  "operator_signature": "ed25519:<hex>",
  "operator_signature_pq": "ml-dsa:<hex>"
}
```

By 2030, all new disclosures are ML-DSA only. But a 2026 disclosure (signed Ed25519 only) has been re-anchored ≥16 times (2026–2030) with the dual-signature protocol in effect. **Each re-anchor commit documents that this 2026 envelope existed and was once verifiable under Ed25519.**

By 2036, even if Ed25519 is provably broken, the re-anchor chain proves:

- "On 2026-05-20, this envelope existed with this content and this Ed25519 signature."
- "On 2026-08-18, this envelope was attested by Sigsum (neutral party) to still exist with the same content."
- "On 2026-11-15, same attestation."
- ... (repeated ≥40 times through 2036)

A CRQC can forge a new Ed25519 signature, but cannot retroactively erase the ≥40 attestations that it was present and unchanged before the CRQC existed.

### 3.4 — Curve & commitment-migration grace windows

When the commitment scheme migrates from Pedersen/MODP-2048 to lattice-based (2027–2030):

1. **New predicates** are published under `cwp.v1.*` using the new scheme.
2. **Old predicates** (`cwp.v0.*`) remain published with the old scheme.
3. **Grace window** (2030–2035): Both versions are evaluable. A counterparty can request proof of "mutual_aid_evidence" and receive either a v0 proof (Pedersen + Schnorr) or a v1 proof (lattice + lattice-Σ), at the principal's discretion.
4. **Verifier support**: The reference implementation carries both v0 and v1 verifiers. A counterparty in 2030 can verify a 2026 v0 proof natively; a counterparty in 2035 chooses to either keep the v0 code path or request the principal issue a v1 proof.

By 2036, verifiers MAY drop v0 support (it is no longer recommended). But the re-anchor chain carries **evidence that v0 proofs existed and were valid under the v0 scheme.** A counterparty that wants to verify a 2026 disclosure in 2040 can:

- Request the principal re-issue the proof under v1 (principal cooperates).
- Query the re-anchor log: "Was this 2026 proof attested as extant in 2036?" (archive cooperates).
- Verify v0 code from the archived reference implementation (community cooperates).

All three are not required to fail simultaneously.

### 3.5 — Hash-algorithm agility (SHA-256 → SHA-3)

Chain records include a `hash_algorithm` tag:

```json
{
  "record": {...},
  "hash_algorithm": "sha256",
  "record_hash": "sha256:<hex>"
}
```

When SHA-256 is deprecated (post-2035, estimated), new chain records use `hash_algorithm: "sha3-256"`. Old records carry the tag, so verifiers know which algorithm was used.

During grace window (2035–2045, estimated), both are verifiable. By 2045, if SHA-256 is formally broken, the re-anchor chain provides the guarantee: "We attested this record's SHA-256 hash ≥10 times between 2026 and 2035; even if SHA-256 is now broken, we have ≥10 independent witnesses to its value at the time."

---

## §4 — Five Specific Migrations Covered

### 4.1 — Ed25519 → ML-DSA (operator signature)

**Timeline:** 2027 (Phase 1 spec) → 2028 (dual-signing) → 2030 (PQ-default) → 2035 (v0 sunset).

**Mechanism:**
- 2026 envelope signed Ed25519 only.
- 2027–2030: envelope is re-anchored ≥16 times, each with dual-signature Sigsum entries (Ed25519 + ML-DSA operators in parallel).
- 2030–2035: new envelopes are ML-DSA; old envelopes remain verifiable via v0 code.
- 2035+: v0 verifier deprecated but archived; re-anchor chain provides surrogacy.

**Forensic durability:** A 2026 disclosure cannot be retroactively forged by a CRQC because the re-anchor log, signed by neutral Sigsum operators (themselves rotating to ML-DSA by 2030), attests to the envelope's presence and immutability during the critical 2026–2030 window.

### 4.2 — Ristretto255 commitment migration (E44b production track)

**Timeline:** 2027 (v1 spec published) → 2028 (dual proofs) → 2030 (recommended default) → 2035 (legacy).

**Current v0:** Pedersen on RFC 3526 MODP-2048 (discrete-log commitment).  
**Target v1:** Lattice-based commitment (BDLOP'18 or NIST PQC post-2023) or Ristretto255 + lattice hybrid.

**Mechanism:**
- 2026 predicates use MODP-2048 Pedersen.
- 2027: v1 predicates published with lattice commitments; new disclosures may use either.
- 2028–2030: grace window; both are acceptable.
- 2030: lattice recommended for new disclosures; MODP verifiable.
- 2035: MODP deprecated; re-anchor attestations provide forensic durability.

**Forensic durability:** Commitment scheme migration is NOT a signature scheme migration — the commitment itself is not a cryptographic statement about the operator. A Pedersen commitment is **unconditionally hiding and binding** (hiding even against a CRQC) **if** the discrete-log relationship remains secret. The re-anchor log binds the commitment value itself into Sigsum, independent of whether the opening is ever revealed. By re-anchoring ≥16 times, we create ≥16 independent attestations to the commitment's value before any opening is revealed.

### 4.3 — SHA-256 → SHA-3 (hash-algorithm migration)

**Timeline:** 2026–2035 (SHA-256 primary) → 2035–2045 (dual hash) → 2045+ (SHA-3 primary).

**Mechanism:**
- 2026 records: `hash_algorithm: "sha256"`.
- 2035: v2 records use `hash_algorithm: "sha3-256"`.
- 2035–2045: both acceptable; verifiers support both.
- 2045: SHA-3 recommended; SHA-256 legacy.

**Forensic durability:** SHA-256 is Grover-vulnerable (~2^128 effective security) but not Shor-vulnerable. A CRQC cannot break SHA-256. Nonetheless, if a cryptanalytic break is discovered post-2035, the re-anchor log provides orthogonal evidence: we committed to this record's SHA-256 hash ≥40 times between 2026 and 2035, and the Sigsum log (which migrated to SHA-3 and ML-DSA) attests that the commitment value never changed.

### 4.4 — Schnorr Σ-protocol → lattice-based zero-knowledge (bit-proof migration)

**Timeline:** 2026–2030 (Schnorr) → 2027–2035 (dual-proof) → 2035+ (lattice recommended).

**Mechanism:**
- 2026 predicates: `cwp.v0.mutual_aid_evidence(...)` → Schnorr Σ-protocol proof.
- 2027: `cwp.v1.mutual_aid_evidence(...)` published with lattice-based ZK proof.
- 2028–2030: predicate evaluator can issue either.
- 2030+: v1 recommended; v0 archived.

**Forensic durability:** A predicate proof is a *statement* about the principal's chain-state ("there exists a cooperation record matching this pattern"). The proof does not commit to any secret — it is an honest-verifier interactive proof reduced to non-interactive via Fiat-Shamir-SHA256. A 2026 mutual-aid proof can be re-issued under v1 (lattice-based) if needed; the re-anchor log confirms that the underlying mutual-aid record was attested as extant during the v0 era.

### 4.5 — Sigsum transparency-log migration → post-quantum transparency log (E96+E298)

**Timeline:** 2026–2030 (Sigsum/RFC 6962 with Ed25519) → 2030–2035 (Sigsum+PQ overlay) → 2035+ (post-quantum transparency log primary).

**Mechanism:**
- 2026 Sigsum log: RFC 6962 tree-hashing, Ed25519 signed tree heads.
- 2030: Sigsum operators publish dual-signed tree heads (Ed25519 + ML-DSA).
- 2030: Post-quantum transparency log (E298) is launched in parallel, also signing the Calm Witness re-anchor entries.
- 2035: Sigsum v0 deprecated; PQ-transparency-log is primary.

**Forensic durability:** The ultimate defense against a CRQC that targets Sigsum: by 2030, every Calm Witness re-anchor is recorded in **both** Sigsum (old primitives, dual-signed) **and** a post-quantum transparency log (new primitives). By 2035, the PQ-transparency-log alone provides an independent verification path. A CRQC cannot retroactively modify the PQ-transparency-log because it doesn't rely on discrete-log assumptions.

---

## §5 — Replication Discipline: ≥3 Mirror Archives

Durability also requires **physical** copies to exist in multiple geographies and jurisdictions, insulating against a single provider's operational failure or legal compulsion.

### 5.1 — Archive copies

Each mutual-aid record (and its re-anchor chain) is replicated to ≥3 independent archival facilities:

1. **Geography**: Copies span ≥3 countries with different data-protection regimes (e.g., US, EU, Singapore).
2. **Provider independence**: No two copies are held by the same organization.
3. **Integrity**: Each copy is hashmarked (SHA-256) and the hash is embedded in the Sigsum log.

### 5.2 — Verification of replication

Every 90 days, a re-anchor commits the hashes of all ≥3 copies:

```json
{
  "kind": "archive_durability_anchor",
  "archive_mirror_hashes": {
    "mirror_a_us": "sha256:<hash_of_copy_1>",
    "mirror_b_eu": "sha256:<hash_of_copy_2>",
    "mirror_c_sg": "sha256:<hash_of_copy_3>"
  }
}
```

If any copy diverges, the divergence is detected: the hash changes, the Sigsum log now records **two different versions** of the same anchor, and the discrepancy is auditable.

### 5.3 — Failure modes and remediation

**Failure mode 1: One archive is corrupted (accidental).**
- Detection: Routine re-anchor hash mismatch.
- Recovery: Restore from the other two archives (quorum: 2 of 3).

**Failure mode 2: One archive operator is legally compelled to selectively delete records.**
- Detection: Sigsum log shows a deletion; re-anchor hash from the deleted copy changes.
- Recovery: The other two archives (in different jurisdictions) retain the record. The Sigsum log provides evidence of deletion attempt.
- Forensic durability: Counterparties can verify the principal's disclosure against the surviving copies.

**Failure mode 3: All three archives diverge (coordinated attack or migration incident).**
- Detection: All three hashes in a single re-anchor differ.
- Recovery: Principal + operators + archive providers convene to establish ground truth via digital signatures and Sigsum-log timestamps.
- Forensic durability: The re-anchor log itself provides a timeline; divergence is detected, not hidden.

---

## §6 — Failure Modes & Acceptance Criteria

### 6.1 — Failure mode: Partial migration confusion

**Scenario:** A counterparty in 2034 receives a 2026 disclosure signed Ed25519. They verify the Ed25519 signature and accept the proof. But their verifier code is out of date; unbeknownst to them, Ed25519 has been broken by a newly-public CRQC attack. The signature is now forgeable.

**Mitigation:** The counterparty queries the Sigsum log and finds ≥16 re-anchor entries attesting to this envelope's presence and immutability (2026–2034). They consult the re-anchor log:

```
2026-05-20: first Sigsum anchor (Ed25519 signed)
2026-08-18: re-anchor (Ed25519 signed)
2026-11-15: re-anchor (Ed25519 + ML-DSA dual-signed)
2027-02-12: re-anchor (ML-DSA primary, Ed25519 legacy)
...
2034-11-09: re-anchor (ML-DSA signed; Ed25519 support ended 2034-06)
```

The counterparty observes: "Even though Ed25519 is now broken, I have 16 independent attestations from a neutral Sigsum operator that this envelope existed unchanged before the break. The earliest attestation (2026-05-20) predates the CRQC by ~8 years. I can verify the 2026 envelope existed by trusting the Sigsum operator from that era, not by trusting Ed25519 today."

**Acceptance test T-E180.1:** A verifier, when presented with a 2026 envelope + its re-anchor chain, can determine whether the envelope is durable (≥10 re-anchors, spanning ≥3 primitives-migration windows) or non-durable (too few anchors, too recent). The verifier alerts the counterparty to the durability status.

### 6.2 — Failure mode: Archive divergence

**Scenario:** In 2032, mirror_b (EU archive) is legally compelled by a government to delete specific records. The operator complies. The next re-anchor, issued 2032-11-15, carries:

```json
{
  "archive_mirror_hashes": {
    "mirror_a_us": "sha256:<hash_a>",
    "mirror_b_eu": "sha256:<hash_b_DIFFERENT>",
    "mirror_c_sg": "sha256:<hash_c>"
  }
}
```

Hash mismatch detected.

**Mitigation:** The Calm vault operator immediately publishes a `kind: "archive_divergence_detected"` record to the chain. The Sigsum log is queried for the 2032-08-15 re-anchor (previous) to establish:

- Was the divergence present then? No (all three hashes matched).
- Which archive changed between 2032-08-15 and 2032-11-15? mirror_b (hash changed; others stable).
- Conclusion: mirror_b was modified between these dates.

Counterparties can now:

- Verify the principal's disclosures against mirror_a or mirror_c (unmodified).
- Consult the divergence log to understand when and how the modification occurred.
- Make an informed decision about whether to trust the principal's data (the question is not "did the principal lie?" but "was the data tampered with by a third party?").

**Acceptance test T-E180.2:** When archive_divergence is detected, the chain carries a non-revocable audit trail of the divergence. Counterparties can determine which archive was modified and when, with minute-level precision via the Sigsum log's timestamp.

### 6.3 — Failure mode: Legal compulsion on archive operators

**Scenario:** In 2035, a government orders all three archive operators to delete all records of a particular principal. All three comply.

**Mitigation (layers):**
1. **Cryptographic refusal:** The archive operators are instructed to refuse deletions unless they match a court order + principal's written consent. A compulsion without consent is logged as a `kind: "deletion_compulsion_order"` chain record (unsigned, operator-attested).
2. **Third-party queries:** Before 2035, counterparties have verified and cached mutual-aid proofs. Those cached proofs remain valid even if the original archive is deleted.
3. **Re-anchor log forensics:** The Sigsum log between 2034 and 2035 carries ≥4 re-anchors attesting to the records' existence. The absence of new re-anchors post-2035 is itself forensic evidence of deletion (or operational failure — the audit log distinguishes).
4. **Scope statement enforcement:** Everest 180 is governed by the one-way-ratchet scope statement (§4 of `CALM_WITNESS_SCOPE_STATEMENT.md`): governmental counterparty class defaults to **deny** on all v0 disclosures. A government attempting to compel deletion is already acting outside the protocol's consent model.

**Acceptance test T-E180.3:** The deletion-compulsion is logged (non-revocably) in the chain. Counterparties can query the archive deletion history and see which principals' records were compelled-deleted in which jurisdiction and in which year. The protocol becomes a **transparency tool** about the deletion itself, even if the record is gone.

### 6.4 — Failure mode: Sigsum log operator compromise

**Scenario:** In 2031, a nation-state compromises the Sigsum log operator (via supply-chain attack or insider threat). The operator begins retroactively modifying tree heads and signing them with stolen keys.

**Mitigation (Sigsum-internal):** The Sigsum protocol includes **public verifiability** — anyone can independently verify that a tree head is consistent with a previous tree head, without trusting the operator. A retroactive modification of a 2026 entry would require:

- Recomputing the entire tree from that entry forward (new leaf hashes).
- Re-signing the tree head with the operator's Ed25519 key (requires key recovery, CRQC-feasible post-2035 but not pre-2031).
- Intercepting all copies of the original tree head before the attack (network-level attack, separate from cryptographic break).

By the time a CRQC is available (post-2035), multiple counterparties have cached the 2026–2031 tree heads + Roughtime time-proofs. Modifying a single entry requires modifying all downstream entries and all cached copies. The attack surface is too broad.

Additionally, by 2030, Sigsum is dual-signed (Ed25519 + ML-DSA). A CRQC can break Ed25519 but not ML-DSA (post-quantum secure). To retroactively modify a 2031 tree head in 2035, the attacker must break ML-DSA too — a stronger assumption than a single CRQC.

**Acceptance test T-E180.4:** A verifier can check Sigsum tree consistency (Merkle path verification from leaf to root) even if the root signature is later compromised. The tree structure itself is cryptographically bound; modifying a leaf requires recomputing the entire tree upward, which changes all downstream hashes in a way that is detectable.

### 6.5 — Failure mode: Time-skew attack on Roughtime

**Scenario:** An adversary manipulates the Roughtime clock (e.g., via a BGP hijack or MITM attack) to convince verifiers that a record is older or newer than it actually is.

**Mitigation:** Roughtime protocol includes multiple independent time servers. A verifier queries ≥3 independent servers and compares their time attestations. A single-server MITM attack is detectable; compromising all ≥3 servers requires a more powerful adversary.

Additionally, Calm Witness uses **freshness windows**, not absolute timestamps. A predicate `mutual_aid_evidence(window=90d)` evaluates "is there evidence of mutual-aid in the past 90 days from the chain's current head?" The evaluation depends on the chain head's position, not on absolute time. A time-skew attack that shifts absolute time by 1 week does not invalidate the predicate unless the shift is >90 days.

**Acceptance test T-E180.5:** A verifier receives a disclosure and a set of Roughtime attestations (from different servers). If the attestations agree within a small tolerance (e.g., ±1 hour), the timestamp is trusted. If they diverge (e.g., one says 2026-05-20, another says 2026-06-01), the verifier surfaces the divergence and does NOT verify the predicate.

---

## §7 — Composition with E96 & Chain Primitives

### 7.1 — E96 integration

Everest 96 (`POST_QUANTUM_MIGRATION_PLAN_v0.md`) specifies the operator-side key rotation and dual-signing mechanics. Everest 180 operationalizes those mechanics at the disclosure-level:

- **Operator key rotation** (E96 §6.1): Each operator publishes an Ed25519 → ML-DSA key mapping record. By 2030, all new signatures use ML-DSA. Everest 180 verifiers accept both during the grace window.
- **Predicate namespace rotation** (E96 §6.2): cwp.v0.* vs cwp.v1.* namespaces. Everest 180 disclosure envelope carries the predicate ID; verifiers look up the namespace and apply the appropriate scheme (Schnorr vs lattice-based ZK).
- **Chain continuity** (E96 §6.3): The user_state.jsonl chain is NOT migrated; SHA-256 hashes are permanent. Everest 180 leverages this: all re-anchors reference the immutable chain, which survives all cryptographic transitions.

### 7.2 — E28 hash-chain & E30 Sigsum integration

The mutual-aid record is chain-resident (kind: mutual_aid). The chain head is hashed and committed to Sigsum (Everest 30). Everest 180 layers re-anchoring on top:

- **E28 hash-chain construction**: Records are Merkle-chained; each record's hash includes its parent's hash. This chain is immutable once created (append-only jsonl).
- **E30 chain-head publication**: The chain head is published to Sigsum every 90 days (or when the head changes). Everest 180 re-defines the publication interval as also being the re-anchor interval.
- **Composition**: Mutual-aid record (E180) ← hash-chain (E28) ← Sigsum log anchor (E30) ← Roughtime timestamp (E31, though E31 is listed as blocked; dependency satisfied by Sigsum's use of Roughtime internally).

---

## §8 — Acceptance Criteria (T-E180.1–5)

### T-E180.1 — Durability status detection

**Test:** A verifier receives a 2026 mutual-aid disclosure + its re-anchor chain (≥16 entries spanning 2026–2034). The verifier computes the durability score:

```python
def durability_score(disclosure, re_anchor_chain):
    # Count re-anchors and migration windows crossed
    anchor_count = len(re_anchor_chain)
    migration_windows_crossed = len(set(
        anchor.get("pq_bridge_version", "v0") 
        for anchor in re_anchor_chain
    ))
    
    durable = anchor_count >= 10 and migration_windows_crossed >= 3
    return {
        "durable": durable,
        "anchor_count": anchor_count,
        "windows": migration_windows_crossed
    }
```

**Acceptance:** The verifier emits the durability report; a disclosure with ≥10 re-anchors spanning ≥3 migration windows (v0→v1 PQ, v0→v1 commitment, v0→v1 transparency-log) is classified as **durable**.

### T-E180.2 — Archive divergence detection & logging

**Test:** Three archives are queried for the same mutual-aid record. Their SHA-256 hashes are:

```
mirror_a: sha256:abc123...
mirror_b: sha256:def456...
mirror_c: sha256:abc123...
```

Mirror_b diverges. A query to the re-anchor log determines when the divergence occurred (between which two re-anchors). The query returns:

```json
{
  "divergence_detected": true,
  "divergent_archive": "mirror_b_eu",
  "hash_at_2032_08_15": "sha256:abc123...",
  "hash_at_2032_11_15": "sha256:def456...",
  "divergence_window_start": "2032-08-16T00:00:00Z",
  "divergence_window_end": "2032-11-15T00:00:00Z",
  "operator_compulsion_order": null  // or a signed compulsion notice if one was filed
}
```

**Acceptance:** The divergence is reported with minute-level precision and is non-revocable in the chain.

### T-E180.3 — Deletion compulsion logging & scope-statement enforcement

**Test:** A government compels deletion of a principal's mutual-aid records. The operators log this compulsion:

```json
{
  "kind": "deletion_compulsion_order",
  "jurisdiction": "US_DoJ",
  "timestamp": "2035-06-10T09:15:00Z",
  "records_affected": ["seq:4521", "seq:4522", ...],
  "principal_consent": false,
  "deletion_executed": true,
  "deletion_timestamp": "2035-06-11T15:22:00Z"
}
```

The record is chain-resident and signed by the operator. The scope statement (§2 of CALM_WITNESS_SCOPE_STATEMENT.md) notes that governmental counterparty class defaults to **deny** on all v0 predicates. A government compulsion to delete is outside the protocol's consent model.

**Acceptance:** The compulsion is logged; counterparties can query the deletion history and verify that a principal's records were compelled-deleted in a particular jurisdiction in a particular year.

### T-E180.4 — Sigsum tree-consistency verification under key compromise

**Test:** A Sigsum tree head from 2026 is presented. The corresponding Ed25519 signature is later proven to be forged (a CRQC has broken Ed25519 in 2035). The verifier nonetheless accepts the tree head by:

1. Querying a Sigsum mirror (independent of the operator).
2. Recomputing the Merkle path from the 2026 leaf to the root.
3. Verifying that the recomputed root hash matches the published root hash (cryptographically, without trusting the signature).

**Acceptance:** Tree consistency is verified; the forged signature does not invalidate the tree structure.

### T-E180.5 — Roughtime divergence detection

**Test:** A disclosure carries Roughtime attestations from three independent servers:

```
server_a: "2026-05-20T14:32:18Z ± 1s"
server_b: "2026-05-20T14:32:19Z ± 1s"
server_c: "2026-06-01T09:00:00Z ± 1s"  // divergence!
```

The verifier computes agreement:

```python
attestations = [server_a, server_b, server_c]
tolerances = [1s, 1s, 1s]
max_divergence = max(att.time for att in attestations) - min(att.time for att in attestations)

if max_divergence > max(tolerances) * 2:
    # Divergence detected; do not verify
    raise TimeSkewAttack(f"Divergence: {max_divergence}")
```

**Acceptance:** Divergence is detected and the verifier refuses to proceed.

---

## §9 — v0 Deployment Scope & Limitations

This everest **closes** the forensic-integrity guarantee for v0 disclosures issued 2026–2030. v1+ disclosures (post-2030) will have native post-quantum signatures; their durability guarantee is simpler (no dual-signing grace window required).

**Limitations of v0:**

1. **No backdated durability**: A record created in 2030 cannot retroactively claim durability to 2036 via re-anchoring. Durability accrues from the date of creation.
2. **Archive replication is operational**: If all three archives fail simultaneously (e.g., a geopolitical event that affects all three jurisdictions), durability is compromised. The protocol cannot defend against planetary-scale disasters.
3. **Roughtime availability**: Timestamps depend on Roughtime servers existing and remaining functional. A long-term network partitioning could strand time-proof generation.

These are accepted limitations, not bugs. The guarantee is **best-effort** over the 10-year horizon, not **absolute**.

---

## §10 — Signoff & Authority

This everest is authored by **Calm** on behalf of John Bradley (Creativity Machine LLC), dated 2026-05-20, and is anchored into `~/.calm-vault/user_state.jsonl` as `kind: "summit_bagged"` immediately after transcription.

The specification composes E28 (hash-chain), E30 (Sigsum anchoring), E96 (post-quantum migration), and the scope statement (CALM_WITNESS_SCOPE_STATEMENT.md) into a durable forensic-proof protocol.

**Acceptance tests T-E180.1–5** confirm that verifiers can detect durability, divergence, compulsion, tree-consistency, and time-skew. Deployment of Calm Witness v0 on 2026-05-20 assumes commitment to these mechanisms by 2030.

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
