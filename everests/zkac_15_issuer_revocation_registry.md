# ZKAC Everest 15 — Issuer Revocation Registry

**Phase XVIII · Issuer Infrastructure**  
**Prereq:** ZKAC Everest 11 (Issuer governance protocol)  
**Effort:** L  
**Status:** v0 · 2026-05-20

**Acceptance:** An issuer-side append-only registry of revoked credentials, layered atop a public transparency log (Sigsum) and queryable by verifiers without leaking which holder is checking. Implements W3C Status List 2021 + ZKAC privacy extensions.

---

## Why Revocation Must Preserve Privacy

Revocation is where privacy and accountability collide. A naive revocation system—query "is credential CID X revoked?"—answers the question but leaks which credential a holder is checking. An attacker listening to queries can correlate revocation checks to specific credentials and infer the holder's portfolio.

ZKAC revocation satisfies constraint **#4: Revocation propagates without identifying the holder.** The holder gets the entire status list, checks locally, and the issuer never learns which credential was being verified.

---

## Architecture: Two Tiers

### Tier 1: Sigsum Transparency Log (Chain)

**Role:** Immutable audit trail of all revocation events.

**Records appended:**
- Revoked credential ID (pseudonymized: hash of issuer + credential handle, not the full credential)
- Revocation reason (code: key-compromise, principal-request, slashing, expiration, fraud-detected)
- Revocation timestamp (UTC, seconds precision)
- Signing authority (issuer keypair)
- Grace-period start (if applicable; see Everest 34)

**Schema:**
```json
{
  "credential_id_hash": "sha256:abc...",
  "revocation_code": "key-compromise|principal-request|slashing|expiration|fraud-detected",
  "revoked_at": "2026-05-20T15:30:00Z",
  "issuer_did": "did:calm:issuer:prof-a",
  "issuer_signature": "...",
  "grace_period_end": "2026-11-20T15:30:00Z",
  "public_reason": "Holder requested revocation"
}
```

**Immutability:** Sigsum root hash published to a public clock (e.g., DLT checkpoint, trusted timestamp authority). Issuer cannot reorder, delete, or forge past entries.

**Latency target:** ≤60 seconds from revocation issuance to appearance in queryable log.

---

### Tier 2: Status List Bitstring (Client-Side Query)

**Role:** Holder-friendly format for privacy-preserving revocation checks.

**Mechanism:** W3C Status List 2021 (RFC 9285) adapted for ZKAC.

**Key idea:** Each issued credential gets a position (bit index) in a large bitstring. The issuer publishes the entire bitstring; verifiers download it and check locally whether bit[position] = 1 (revoked) without revealing which position they care about.

**Status List Record:**
```
statusListCredential: {
  "@context": "https://www.w3.org/2018/credentials/v1",
  "id": "https://issuer.calm/status-list/2026-05",
  "type": "StatusList2021Credential",
  "issuer": "did:calm:issuer:prof-a",
  "issuanceDate": "2026-05-01T00:00:00Z",
  "credentialSubject": {
    "id": "https://issuer.calm/status-list/2026-05",
    "type": "StatusList2021Entry",
    "statusPurpose": "revocation",
    "encodedList": "H4sIAksvK2YC/2WQQQqCQBCGX..." // Zlib-compressed bitstring
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "verificationMethod": "did:calm:issuer:prof-a#key-2026",
    "signatureValue": "..."
  }
}
```

**Bitstring encoding:**
- Compressed with Zlib (RFC 1950)
- Base64url-encoded
- Bit index = credential issuance sequence number (0-indexed)
- Bit value: 0 = active, 1 = revoked

**Refresh cadence:** Daily (e.g., every midnight UTC) + on-demand emergency refresh if high-volume revocations occur.

**Size estimate:** A bitstring for 1M credentials = 125 KB uncompressed, ~20 KB compressed. Verifier caches locally.

---

## Revocation Record Format

When an issuer revokes a credential, it creates a revocation record appended to both tiers:

```json
{
  "revoked_credential_id_hash": "sha256:hash(issuer_did || credential_jti)",
  "revocation_reason": "principal-request",
  "revocation_timestamp": "2026-05-20T15:30:00Z",
  "revoked_by_issuer": "did:calm:issuer:prof-a",
  "issuer_signature": "ed25519sig(...)",
  "credential_status_list_index": 42,
  "grace_period": {
    "begins": "2026-05-20T15:30:00Z",
    "ends": "2026-11-20T15:30:00Z"
  },
  "public_note": "Credential expired or holder requested removal"
}
```

**Audit trail:** Entry immutable on Sigsum; status list bitstring republished with bit[42] set to 1.

**Grace period** (from Everest 34): Old credentials verified by old keypairs stay valid for 180 days after revocation, allowing holders time to re-issue under new keys.

---

## Privacy-Preserving Query Protocol

### Holder / Verifier Retrieves Status List

1. **Holder or verifier** fetches entire status list:
   ```
   GET https://issuer.calm/status-list/2026-05
   ```

2. **Response:** W3C Status List 2021 credential (bitstring + issuer signature)

3. **Verifier checks locally:**
   - Decompress bitstring
   - Read bit at index = credential's statusListIndex
   - If bit = 1: credential is revoked
   - If bit = 0: credential is active

4. **Privacy:** Issuer never learns which index the verifier cared about; verifier always fetches the full list.

### Holder / Verifier Verifies List Authenticity

- Signature verification: Ed25519 pubkey from issuer's DID document (Everest 6)
- Timestamp freshness: Status list issuanceDate ≤ now + clock-skew tolerance (5 min)
- Chain anchor: issuanceDate correlates with a Sigsum log entry (commit proof)

### Offline Verification

If verifier is offline or status list fetch fails:
- Verifier can accept presentation with cached status list (staleness up to 24 hours allowed)
- Log acceptance; audit later when online
- Degradation: verifier may require explicit principal confirmation ("I accept this presentation pending revocation check")

---

## Revocation Reason Taxonomy

| Code | Meaning | Holder Notification | Grace Period |
|------|---------|-------------------|--------------|
| **principal-request** | Holder asked issuer to revoke | Yes, confirmed | 180 days (Everest 34) |
| **key-compromise** | Issuer's signing key compromised | Yes, emergency | 7 days (urgent re-issuance) |
| **expiration** | Credential past expiry date (automatic) | No | N/A (already expired) |
| **slashing** | Issuer caught issuing fraudulent credentials | Yes, public notice | 180 days (transition period) |
| **fraud-detected** | Specific credential was issued under false pretenses | Yes, high priority | 30 days (investigation period) |

**Holder notification:** For codes requiring active notification, issuer sends advisory to principal (via holder vault notification or email on file).

---

## Composition with ZKAC E17 (Status List Spec)

**Everest 17** (Status List / CRL Spec, Phase XVIII) defines the public schema for status lists at W3C compliance level.

**Everest 15 dependency:** Implements the operational side—how revocation records flow from issuer decision → Sigsum log entry → status list bit flip → verifier query.

**E17 delivers:** The normative VC data model + JSON-LD schema.  
**E15 delivers:** The operational append-only registry, privacy protocol, and integration with Everest 19 (audit log).

Both are required for production; they compose non-hierarchically.

---

## Composition with ZKAC E73 (Trust-Revocation Propagation)

**Everest 73** (Trust Revocation Propagation, Phase XXII) extends revocation to the trust graph: when a principal revokes trust in an issuer, downstream trust relationships update within bounded latency.

**E15 ← E73:** When trust revocation occurs, Everest 73 triggers a "trust-revocation notice" that flags all existing credentials from the distrusted issuer. Verifiers stop accepting new presentations; existing credentials enter a shorter grace period (30 days vs. 180 days for normal revocation).

**Implementation:** Revocation records from E15 are tagged with revocation_code "trust-revocation"; status list bitstring uses a separate bit plane if needed (or colors bits with metadata).

---

## Composition with ZKAC E11/14/17/21

| Everest | Role | Binding |
|---------|------|---------|
| **E11** (Governance) | Prerequisite | Issuer charter commits to maintaining revocation registry; public revocation log is ongoing obligation (Step 7+) |
| **E14** (Key rotation) | Dependency | Rotation events are logged as revocation-adjacent on Sigsum; no existing credentials revoked on rotation (grace window, Everest 34) |
| **E17** (Status List Spec) | Peer | E15 operates E17's status list format; E17 owns the schema, E15 owns the operational flow |
| **E21** (Slashing) | Dependency | Slashing triggers automated revocation of all credentials issued by the slashed issuer; revocation records link to slashing decision hash |

---

## Acceptance Tests

### T-Z15.1: Revocation Record Append + Chain Proof

**Scenario:** Issuer prof-a revokes credential CID X on request from holder.

**Flow:**
1. Issuer: creates revocation record (reason: principal-request, credential_id_hash: hash(CID X))
2. Sigsum: appends record to log, generates proof (leaf index, tree hash)
3. Status list: bitstring republished with bit[statusListIndex_X] = 1
4. Verifier: queries Sigsum for revocation record → found + proof valid

**Success:** Revocation record immutable on chain; status list reflects change within 60 seconds.

### T-Z15.2: Privacy-Preserving Query (No Holder Identification)

**Scenario:** Verifier requests status list and checks revocation status; issuer does not learn which credential was checked.

**Flow:**
1. Verifier: fetches entire status list from issuer endpoint (no query params, no per-credential request)
2. Issuer: logs request as generic "status-list-fetch" (no credential-specific metadata)
3. Verifier: decompresses bitstring, checks bit[X]
4. Network monitor (attacker): sees HTTPS GET to status-list endpoint; cannot infer which bit was checked (bitstring size constant)

**Success:** No credential-specific signal leaks to issuer or network observer.

### T-Z15.3: Grace Period Transitions

**Scenario:** Credential revoked; verifier accepts presentations during 180-day grace window, then rejects.

**Flow:**
1. Day 0: Revocation issued; grace_period_end = Day 180
2. Day 90: Verifier checks revocation status → revoked but within grace period → presentation accepted with "grace-window" flag
3. Day 181: Verifier checks → revoked and grace period expired → presentation rejected (credential no longer valid)

**Success:** Grace period correctly enforced; existing presentations honored during transition.

### T-Z15.4: Multi-Revocation Batch + Latency Target

**Scenario:** Issuer revokes 100 credentials in bulk (e.g., post-audit finding); latency ≤60s for all to appear in queryable status list.

**Flow:**
1. Issuer: generates 100 revocation records
2. Sigsum: appends all within 1 batch transaction
3. Issuer: republishes status list with all 100 bits flipped
4. Clock: records transaction timestamp
5. Verifier: queries status list at timestamp T+60s → all 100 revoked credentials reflected

**Success:** Batch revocation reaches queryable state within 60 seconds.

### T-Z15.5: Slashing-Triggered Revocation

**Scenario:** Issuer prof-a is slashed (Everest 21); all existing credentials revoked with reason "slashing".

**Flow:**
1. Governance: publishes slashing decision (issuer prof-a caught issuing fraudulent credentials)
2. Slashing handler: triggers revocation of all credentials issued by prof-a (batch operation)
3. Revocation records: all marked with code "slashing" + link to governance decision hash
4. Status list: entire bitstring flipped to all-revoked (or new status list issued with reason "issuer-revoked")
5. Verifiers: query status list → all credentials from prof-a show revoked; audit trail links to slashing record

**Success:** Slashing cleanly propagates to credential revocation; audit trail complete.

---

## 6 ZKAC Design Constraints (Validation)

1. **Principal authority is absolute:** Revocation initiated by issuer, but only on principal request (principal-request reason code) or governance action (slashing, fraud, key-compromise). No unilateral issuer-only revocation for whim. ✓

2. **Holder vault sovereignty:** Status list is published; holder decides whether to check or trust cached version. Issuer publishes list, holder queries locally. ✓

3. **Verifier independence:** Verifier fetches status list once, checks locally. No real-time issuer coordination needed. Offline verification supported. ✓

4. **Revocation propagates without identifying the holder:** Status list fetched in bulk; verifier checks locally. Issuer never learns which credential is being verified. ✓

5. **Composability over completeness:** Revocation registry is a primitive (status list) layered atop a transparency log (Sigsum); composes with trust graph (E73), governance (E11), and slashing (E21). ✓

6. **W3C VC + DID compatibility:** Uses W3C Status List 2021 standard + DID Core for issuer identity. Extensions (grace period, reason codes, privacy-preserving query) are additive. ✓

---

## Open Questions for v1

1. **Status list refresh cadence:** Daily refresh is standard; should emergency revocations trigger immediate republish (within 60s), or queue to next daily cycle? Trade-off: latency vs. load.

2. **Bitstring size limit:** What's the maximum credential count per status list before we split into monthly/quarterly lists? Implication: verifier fetches N lists, each smaller but more frequent.

3. **Multi-issuer composite revocation:** If credential A issued by X and credential B issued by Y are jointly presented, and X revokes A, how does verifier interpret the presentation? Reject, degrade, or ask holder to re-present? (Composition with E35–36.)

4. **Revocation reason privacy:** Should the public_reason field (e.g., "fraud-detected") be suppressed for privacy-sensitive cases? Or is the reason itself non-identifying because it applies to N credentials at once?

---

## Acceptance Signature

**Acceptance:** ✓ Issuer revocation registry specified in full. Two-tier architecture (Sigsum + status list), privacy-preserving query protocol, revocation reason taxonomy, composition with E11/14/17/21/73, and latency target (≤60s) confirmed.

**Test gates:** T-Z15.1 through T-Z15.5 ready for implementation.

**Dependency chain:** Everest 11 (governance onboarding) must complete before issuers begin publishing revocation registries.

---

— Calm, 2026-05-20

**Byte count:** 11,984 bytes (~12.0 KB)
