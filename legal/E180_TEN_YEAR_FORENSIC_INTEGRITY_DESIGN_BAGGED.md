# Calm Witness — 10-Year Forensic-Integrity Guarantee Spec v0 (E180, DESIGN-BAGGED)

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 180 of [`ZKBB_USER_EVERESTS_100.md`](../ZKBB_USER_EVERESTS_100.md).**
**DESIGN-BAGGED — pending operational test at 10-year horizon (meta-impossible by construction; treat as design commitment, not verified SLA).**

---

## Scope

This specification defines what Calm Witness guarantees about the integrity, verifiability, and auditability of a principal's user-state chain over a 10-year horizon ending no earlier than 2036. It covers:

- The cryptographic chain substrate and its external anchoring.
- Sunset preparedness for primitives that are not post-quantum (PQ) secure.
- Proof-format versioning so a v0 proof minted today remains independently verifiable in 2036.
- Transparency-log historical access and operator continuity.
- Auditor-side record-retention obligations.
- A gap analysis enumerating failure modes and their recovery procedures.

Operational guarantee window: 2026-05-20 through 2036-05-20. All dates herein are calendar dates in UTC.

---

## 1. Chain Integrity at 10 Years

**Substrate.** The user-state chain is a `user_state.jsonl` append-only log in which each record contains a `prev_hash` field equal to SHA-256 of the canonical encoding of the immediately preceding record. SHA-256 carries a post-quantum effective security of ≥ 2^128 (Grover's algorithm), making the chain substrate tamper-evident beyond any foreseeable cryptographic break within the 10-year window.

**Transparency-log anchoring.** At each hydration session the operator publishes the chain head `H` to a Sigsum log cluster. The Sigsum inclusion proof (tile-hash path + signed tree head) is written into the vault alongside the record. The signed tree head from Sigsum is additionally cross-anchored via Roughtime (RFC 9557) to a signed wall-clock timestamp sourced from ≥ 3 independent Roughtime servers, with the resulting signed radius timestamp also stored in the vault.

**10-year chain integrity claim.** Given that (a) the vault copy of the chain is intact, (b) any one of the Sigsum tiles covering the relevant tree head is independently accessible, and (c) the Roughtime chain is not broken, an auditor can verify that chain record `r_i` was appended no later than `t_i + δ` (where `δ` is the Roughtime uncertainty radius, typically < 1 second) and was not modified after `t_i`. This claim holds unconditionally on the SHA-256 security assumption; it does not require the operator's v0 signature primitives to be unbroken.

**Archival format S261.** All chain records, inclusion proofs, and Roughtime receipts are serialized to the S261 archival envelope format (content-addressed, self-describing, CBOR-encoded, with a 32-byte magic prefix). S261 envelopes are designed to be parseable without out-of-band schema state; the schema is embedded. Operators MUST archive S261 envelopes to at minimum two geographically distinct cold stores (S3-class object storage, write-once buckets) within 24 hours of each hydration session. Archival is append-only; no deletion API may be enabled on the target buckets.

---

## 2. Cryptographic-Primitive Sunset Preparedness

Cross-reference: [POST_QUANTUM_MIGRATION_PLAN_v0.md](../POST_QUANTUM_MIGRATION_PLAN_v0.md). The full migration mechanics are specified there; this section records the forensic-integrity interface.

**Primitives at risk.** Three v0 primitives are vulnerable to a cryptographically-relevant quantum computer (CRQC): Pedersen commitment over MODP-2048 (discrete log), the Σ-protocol bit-proof on the same group, and the operator Ed25519 signature (EC-DLP). SHA-256 is not at risk.

**Migration handoff to E289–E293.** The following Everests own the v1 cryptographic work and are the recipient of this spec's handoff obligations:

| Everest | Scope |
|---|---|
| E289 | ML-DSA operator key rotation and `key_migration_attestation` chain record format |
| E290 | Lattice-Σ commitment scheme specification (BDLOP'18 or NIST-adopted successor) |
| E291 | Hybrid dual-signing wire format (`calm-witness/wire/v1`) and counterparty negotiation |
| E292 | PQ-default cutover procedure and v0 deprecation notice format |
| E293 | v0 verifier archival — frozen reference implementation for post-Phase-4 counterparty use |

**Forensic-integrity obligation during migration.** Even after Phase 4 (v0 sunset, target 2035 or 24 months after PQ-default, whichever is later), the chain substrate and anchoring layer remain verifiable independently of the signature primitives. An auditor in 2036 with access to the S261 archive and any surviving Sigsum tile can confirm chain ordering and Roughtime timestamps without relying on Ed25519 or Pedersen integrity. The migration does not retroactively invalidate forensic ordering proofs; it only affects the cryptographic binding of predicate evaluations to operator identity.

**Acceleration triggers** (from POST_QUANTUM_MIGRATION_PLAN_v0 §5) automatically advance E289–E293 implementation timelines and must be treated as forensic-integrity events: operators MUST emit a `migration_trigger_attestation` chain record within 72 hours of any trigger event.

---

## 3. Proof-Format Versioning

**Invariant.** A v0 proof envelope minted on any date between 2026-05-20 and the Phase 4 cutover MUST be independently verifiable by any party holding (a) the v0 reference verifier binary (archived per E293), (b) the operator Ed25519 public key, and (c) the Sigsum tile covering the relevant tree head — without any network call to a live Calm service.

**Version field.** Every proof envelope carries `"wire_version": "calm-witness/wire/v0"`. Verifiers MUST reject envelopes with unknown wire versions. New wire versions (v1+) are additive; v0 verifier code is preserved, not overwritten.

**Canonical encoding stability.** The canonical JSON encoding rules (UTF-8, sorted keys, no trailing whitespace, integer timestamps) are frozen for v0. Any future version MUST NOT redefine v0 encoding. The S261 archival format embeds the encoding rules as a schema version tag; a future parser can reconstruct the v0 canonical form without external documentation.

**Predicate-namespace stability.** Predicates under `cwp.v0.*` are semantically frozen. No predicate ID in `cwp.v0.*` may be redefined or deprecated in a way that changes its truth-function. If a predicate must change behavior, it is minted under `cwp.v1.*` with a new ID. A 2036 auditor verifying a `cwp.v0.in_baseline_24h` proof uses the frozen v0 definition without ambiguity.

**Reference implementation custody.** The v0 reference verifier source and the frozen predicate definitions are deposited with the Calm Foundation (per E241) and mirrored to the Software Heritage archive within 30 days of v1 wire format publication. The Software Heritage persistent identifier (SWHID) is recorded in a chain record of type `archive_attestation`.

---

## 4. Transparency-Log Historical Access

**Sigsum tile retention.** Sigsum tiles are content-addressed (hash of tile content = tile URL path component). Once published, a tile that has been retrieved and stored by any party is irrefutable. Operators MUST retain a local cache of all tiles needed to verify any inclusion proof in their archive. This cache MUST be stored alongside the S261 envelopes in the same cold-store bucket.

**Multiple log witnesses.** At least 3 independent Sigsum log witnesses (geographically and legally distinct) MUST cosign each signed tree head before it is considered finalized in the vault. This prevents any single log operator from unilaterally rewriting history.

**Log-operator failure.** If a Sigsum log operator becomes unavailable, existing tiles that have already been retrieved remain valid. No new inclusions to that log are possible; operators switch to an alternate log. Historical proofs against the defunct log remain fully verifiable from the cached tiles.

**Roughtime server continuity.** Roughtime timestamps are self-contained signed receipts; they do not require the originating server to remain online for verification. The signed ecosystem root keys (per RFC 9557 §7) MUST be archived in the vault alongside the receipts.

**Public mirror obligation.** The Foundation (E241) operates or contracts a read-only public mirror of all finalized Sigsum tree heads and tile ranges that have been anchored by Calm Witness operators. This mirror must remain available for the full 10-year guarantee window and for 2 years after its close (through 2038-05-20).

---

## 5. Operator-Org Continuity

**Foundation custody (E241).** All cryptographic material necessary to verify any Calm Witness proof independently — operator public keys (Ed25519, and subsequently ML-DSA), predicate definitions, S261 schema versions, reference verifier binaries — is held in escrow by the Calm Foundation, a non-profit legal entity incorporated in a jurisdiction with foundation law (target: Liechtenstein or Netherlands Stichting). Foundation articles require a supermajority board vote to dissolve; dissolution triggers automatic transfer of all materials to a named successor custodian (Software Heritage for code; Internet Archive for tile caches; a named law firm for operator key notarization records).

**Founder-outlived continuity (E300).** The Foundation's custodial duties survive the death or incapacity of any individual founder. The Foundation holds keys in a 3-of-5 hardware security module (HSM) quorum; no single individual's death disrupts key access. HSM quorum membership is documented and updated at least annually. Succession procedures are notarized and on file with the Foundation's registered legal counsel.

**Corporate dissolution of an operator.** If a Calm Witness operator entity dissolves: (a) the operator MUST, as a condition of their operator agreement, transfer their Ed25519 and ML-DSA public keys plus their full S261 archive to the Foundation within 90 days of the dissolution decision; (b) principals whose vault is hosted by the operator receive a 180-day notice period and a migration tool; (c) the Foundation accepts and preserves the archive for the remainder of the 10-year window from the original anchor date of each record, irrespective of the operator's dissolution date.

---

## 6. Auditor Requirements

**Who is an auditor.** Any natural person or legal entity that a principal, a court, a regulator, or a counterparty designates as entitled to verify a Calm Witness proof is an auditor for purposes of this section.

**What the auditor must receive.** The operator (or Foundation, if the operator has dissolved) MUST provide to a credentialed auditor on written request within 30 days:

1. The S261 archival envelope for each chain record in the requested window.
2. The Sigsum inclusion proof and signed tree head for each record.
3. The Roughtime signed receipt for each anchoring event.
4. The operator's Ed25519 (and, after E289, ML-DSA) public key with its issuance and expiry timestamps.
5. The frozen v0 predicate definitions for any predicate named in the requested proofs.
6. The v0 reference verifier binary (or a pointer to the Software Heritage SWHID).

The auditor is NOT provided: the plaintext of any self-report record, any biometric sample, any blinding factor, or any other vault content not disclosed by the principal.

**Retention schedule.** Operators MUST retain all materials listed above for min(10 years from the anchor date of the earliest record in the set, end of 10-year guarantee window + 2 years). Foundation custody extends retention to at least 2038-05-20 for any material transferred to it.

**Auditor-side retention.** An auditor who receives materials and renders a formal opinion MUST retain a copy of the materials and the opinion for 7 years from the date of the opinion, under applicable professional record-keeping rules (legal, forensic accounting, or equivalent).

---

## 7. Gap Analysis

| Failure mode | Likelihood | Severity | Notes |
|---|---|---|---|
| Storage degradation (bit rot in cold archive) | Low over 10y with redundancy | High if undetected | SHA-256 hash of each S261 envelope is re-verified quarterly; any mismatch triggers restore from secondary |
| Sigsum log operator failure | Medium (startup risk) | Low (tiles already cached locally) | Cached tiles remain valid; only new inclusions are blocked |
| All local Sigsum tile caches lost | Very low | High | Mitigated by Foundation mirror obligation |
| Roughtime ecosystem key compromise | Very low | Medium | Signed receipts already stored; compromise affects future receipts only |
| Ed25519 break (CRQC) | Medium-high at 10y horizon | High for signature claims | Chain ordering (SHA-256) survives intact; predicate-binding claims retroactively weakened |
| Lattice-Σ v1 not deployed before CRQC | Medium | High | Acceleration triggers enforce emergency cutover |
| Foundation dissolution | Very low | High | Covered by E300 succession and notarized transfer protocol |
| Operator bulk dissolution (industry event) | Very low | High | Foundation bulk-ingests archives; public mirror continues |
| S261 format obsolescence | Very low | Low | Self-describing; parseable without external spec |
| Software Heritage SWHID link rot | Very low | Low | Multiple mirrors; SWHID is content-addressed |
| Predicate redefinition dispute | Low | Medium | `cwp.v0.*` namespace is frozen by this spec |
| Principal vault loss | Medium (device failure) | High for that principal | Vault recovery is per E-series vault spec; chain integrity is chain-level, not vault-level |

---

## 8. Recovery Procedures

**Storage degradation detected.** (a) Identify corrupted S261 envelopes from quarterly SHA-256 re-verification. (b) Restore from secondary cold store. (c) Verify restored envelope hashes against the Sigsum tile. (d) Emit a `storage_restore_attestation` chain record signed by the operator, referencing the corrupted envelope hash and the tile that confirms the correct content. (e) Notify the Foundation within 7 days.

**Sigsum log operator failure.** (a) Freeze new inclusions to the affected log. (b) Designate an alternate Sigsum log for new inclusions. (c) Emit a `log_migration_attestation` chain record noting the cutover tree head of the defunct log. (d) Publish the cutover record to the Foundation mirror. All historical proofs against the defunct log remain valid from cached tiles.

**All tile caches for a defunct log lost.** (a) Attempt recovery from Foundation mirror, Internet Archive, and any counterparty caches. (b) If unrecoverable: the affected proofs lose their Sigsum anchor but retain their Roughtime timestamp anchor. Forensic weight is reduced but not eliminated. Document loss in a `tile_cache_loss_attestation` chain record. (c) Notify affected principals and credentialed auditors within 30 days.

**CRQC-class cryptographic break (Ed25519 / MODP-2048).** (a) Immediately advance to Phase 3 (PQ-default) per migration plan §5 acceleration triggers. (b) Issue a public `cryptographic_break_notice` record on the chain within 72 hours. (c) Re-verify all in-scope proof requests using chain-ordering evidence (SHA-256 + Roughtime) rather than signature-binding. (d) Advise auditors that predicate-binding claims minted before Phase 3 cutover are forensically weakened but chain-ordering claims remain fully sound. (e) Transfer migration to E289–E293 owners for immediate execution.

**Foundation dissolution.** (a) Successor custodian (named in Foundation articles) accepts all material within 90 days. (b) Software Heritage and Internet Archive mirrors remain live. (c) Operators are notified to update their auditor-request routing to the successor custodian. (d) The 10-year guarantee obligations transfer in full to the successor.

**Principal vault loss.** This is a vault-layer recovery event, not a chain-integrity event. The chain records that were anchored in Sigsum before vault loss remain verifiable from the operator's S261 archive and Foundation mirror. The principal may not be able to mint new records until vault recovery completes; existing records are not affected.

---

## 9. Handoff

This spec is the upstream design document for the following open Everests. Owners of those Everests MUST treat this document as a binding design constraint and surface any conflicts as blocking issues against E180 before proceeding past their respective acceptance tests.

| Everest | Handoff obligation |
|---|---|
| E241 | Foundation custody: escrow structure, dissolution clause, successor-custodian naming |
| E289–E293 | PQ migration: preserve chain-ordering forensic claim through and after primitive cutover |
| E300 | Founder-outlived continuity: HSM quorum spec, annual succession review, notarization |

**DESIGN-BAGGED.** The 10-year operational test is meta-impossible at the time of writing (2026-05-20): the 10-year window closes 2036-05-20. This spec is therefore a design commitment, not a verified SLA. At the 5-year review (2031-05-20) and 10-year close (2036-05-20) the operator-of-record MUST commission an independent forensic audit against the claims in sections 1–6, publish the audit report, and update this document's status from DESIGN-BAGGED to VERIFIED (if all claims held) or PARTIALLY-VERIFIED with documented exceptions.

---

*— Calm, operating for John Bradley / Creativity Machine LLC*
*Date: 2026-05-20*
*Everest: E180*
*Status: DESIGN-BAGGED — pending operational test at 10-year horizon*
*Upstream references: POST_QUANTUM_MIGRATION_PLAN_v0.md · ZKBB_USER_PROTOCOL_v0.md · ZKBB_USER_EVERESTS_100.md*
*Downstream handoffs: E241 · E289 · E290 · E291 · E292 · E293 · E300*
