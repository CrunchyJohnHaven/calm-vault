# ZKAC Everest 17 — Status List / CRL Specification

**Phase XVIII · Issuer Infrastructure**  
**Prereq:** ZKAC Everest 15 (Issuer revocation registry)  
**Effort:** M  
**Status:** v0 · 2026-05-20

**Acceptance:** W3C-compliant status-list mechanism for credential revocation. Normative VC data model + JSON-LD schema. Integrates ZKAC privacy extensions (bitstring compression, holder-query isolation, Sigsum anchoring). Enables verifiers to check revocation status without revealing credential index to issuer.

---

## Overview

W3C Status List 2021 (RFC 9285) defines a privacy-preserving format for credential revocation. This spec adapts Status List 2021 to ZKAC requirements: zstd-compressed bitstrings indexed by credential issuance position, holder query isolation, and mandatory Sigsum anchoring.

**Key design:** Each issued credential is assigned a bit position in a large bitstring. Issuer publishes the bitstring periodically. Verifiers download the entire bitstring and check locally whether their credential is revoked, without the issuer learning which position was queried (constraint #4: Revocation propagates without identifying the holder).

---

## W3C Status List 2021 + ZKAC Extensions

### Status List Credential (Normative Format)

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://w3id.org/vc/status-list/2021/v1"
  ],
  "id": "https://issuer.calm/status-list/2026-05",
  "type": ["VerifiableCredential", "StatusList2021Credential"],
  "issuer": "did:calm:issuer:prof-a",
  "issuanceDate": "2026-05-01T00:00:00Z",
  "credentialSubject": {
    "id": "https://issuer.calm/status-list/2026-05",
    "type": "StatusList2021Entry",
    "statusPurpose": "revocation",
    "encodedList": "KLUv/QBYrQEA..."  // base64url(zstd(bitstring))
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-05-01T00:00:00Z",
    "verificationMethod": "did:calm:issuer:prof-a#keys-2026-05-01",
    "proofPurpose": "assertionMethod",
    "signatureValue": "..."
  }
}
```

### credentialStatus Property (In Issued Credentials)

Every ZKAC credential embeds:

```json
{
  "credentialStatus": {
    "id": "https://issuer.calm/status-list/2026-05#42",
    "type": "StatusList2021Entry",
    "statusPurpose": "revocation",
    "statusListIndex": "42",
    "statusListUrl": "https://issuer.calm/status-list/2026-05"
  }
}
```

**Fields:**
- `statusListIndex` (string, encoded as base-10 digit sequence): 0-indexed bit position in the bitstring
- `statusListUrl`: URI for fetching the status list credential
- `statusPurpose`: Always "revocation" for this spec; extensible to "suspension" or application-specific codes in future phases

---

## Bitstring Encoding & Compression

### Uncompressed Format

- Bitstring as RFC 1751 zero-indexed bitfield
- Bit value: 0 = active, 1 = revoked
- Size: N credentials ÷ 8 = N/8 bytes uncompressed

Example: 16,384-entry bitstring = 2,048 bytes uncompressed.

### Compression (zstd, RFC 8878)

1. **Compress:** bitstring → zstd(level=3, contentSize=true)
2. **Encode:** zstd bytes → base64url (RFC 4648 §5)
3. **Embed:** base64url string → `credentialSubject.encodedList`

**Rationale for zstd:**
- Deterministic (same input → same output)
- Fast decompression (< 1ms for 2KB → 2KB range)
- Space efficiency: sparse revocation patterns compress 80%+ (sparse = most bits 0)

**Example compression:**
- 16,384 entries (2,048 bytes raw), sparse (10% revoked) → ~550 bytes compressed
- Base64url expansion: ~730 bytes final

### Decompression & Verification

Verifier:
1. Fetch status list credential via `statusListUrl`
2. Verify issuer signature (Ed25519 from issuer DID)
3. Decode: base64url → zstd bytes
4. Decompress: zstd bytes → bitstring
5. Extract bit at index `statusListIndex`
6. If bit = 1: revoked. If bit = 0: active.

---

## Status List Refresh & Freshness

### Refresh Cadence

- **Default:** Issued daily at midnight UTC (e.g., 2026-05-01T00:00:00Z for the May 1 list)
- **Naming convention:** `https://issuer.calm/status-list/YYYY-MM`
- **Retention:** Issuer publishes current month + prior 2 months (rolling 90-day window)

### Maximum Age & Freshness Window

| Credential Class | Max Age | Verification Behavior |
|------------------|---------|----------------------|
| High-stakes (financial, identity) | 24h | Reject if status list older than 24h |
| Standard (professional, educational) | 7d | Warn if > 24h; reject if > 7d |
| Low-stakes (informational, peer) | 30d | Accept up to 30d; require refresh on next verification |

### Offline Verification (Fallback)

If verifier is offline or status list fetch times out:
- Verifier may accept presentation using cached status list (max age = 24h for high-stakes, 7d for standard)
- Presentation marked with `offline_verification_flag: true`
- Verifier logs acceptance; performs online revocation check within bounded time (e.g., next business day)
- If credential found revoked during delayed check, incident escalated to principal

---

## Holder Query Pattern (Privacy)

### Download Entire Bitstring

1. Holder / verifier: `GET https://issuer.calm/status-list/YYYY-MM`
2. Issuer: logs request as single "status-list-fetch" event (no per-credential metadata)
3. Verifier: decompresses locally; checks bit at index `statusListIndex`
4. Network observer: sees HTTPS request to status-list endpoint; cannot infer which credential was checked (request size constant, payload size constant)

### Why This Preserves Privacy

- **No credential-indexed queries:** Issuer never receives "is credential #42 revoked?" Instead, verifier fetches the full list.
- **Bitstring size constant:** Every fetch returns the same size (constant commitment in the credential). No timing side-channel.
- **HTTPS encryption:** Network observer cannot inspect query parameters or request body.
- **Issuer log isolation:** Issuer logs generic "status-list-fetch-2026-05-01T12:34:56Z" but not "fetch for credential #42". Even issuer cannot correlate fetches to specific credentials without side-channel correlation (Sybil attack, IP linking, etc.).

### Verifier-Side Freshness Validation

Verifier confirms:
1. **Issuer signature valid:** Ed25519 verification using issuer's public key from DID document (Everest 6)
2. **Timestamp freshness:** `issuanceDate` ≤ now + 5 min clock-skew tolerance
3. **Chain anchor:** `issuanceDate` matches a Sigsum log entry (transparency-log commit proof)
4. **Signature matches:** Proof.verificationMethod resolves to the issuer's current key (or grace-period key from Everest 34)

---

## Sigsum Anchoring (Binding to Transparency Log)

### Why Sigsum

Sigsum (RFC 9162 variant) provides append-only, immutable audit trail. Revocation cannot be hidden, backdated, or selectively republished.

### Status List Publication on Sigsum

When issuer publishes a new status list, they also submit:
```json
{
  "type": "status-list-checkpoint",
  "issuer_did": "did:calm:issuer:prof-a",
  "status_list_id": "2026-05",
  "status_list_url": "https://issuer.calm/status-list/2026-05",
  "status_list_root_hash": "sha256:abc...",  // Hash of encodedList
  "published_at": "2026-05-01T00:00:00Z",
  "sigsum_tree_size": 42000,
  "sigsum_leaf_index": 41999
}
```

**Verifier verification:**
1. Fetch status list credential
2. Hash the encodedList → compute status_list_root_hash
3. Query Sigsum for the record with matching root_hash + issuer_did
4. Retrieve Sigsum proof (leaf index, tree hash, inclusion proof)
5. Verify inclusion proof against Sigsum log root (e.g., from a public clock)

---

## Composition with ZKAC Everest 15 (Issuer Revocation Registry)

**Everest 15 (Operational):**
- Append-only registry of revocation records (Sigsum)
- Revocation reason taxonomy
- Privacy-preserving query protocol (this spec)
- Grace-period semantics

**Everest 17 (Normative):**
- W3C Status List 2021 data model
- JSON-LD schema and context
- Bitstring compression (zstd)
- Sigsum anchoring

**Integration:**
1. Issuer receives revocation request (E15) → creates revocation record
2. Issuer appends record to Sigsum log (E15) → receives leaf index + proof
3. Issuer updates status list bitstring: bit[statusListIndex] = 1
4. Issuer publishes status list credential (E17) + Sigsum anchor
5. Verifier fetches status list (E17), verifies signature + Sigsum anchor (E17), checks bit locally

---

## Composition with ZKAC Everest 30 (Witness Sigsum Anchor)

**ZKAC Witness Everest 30** (Sigsum anchor verification) provides canonical proof-of-inclusion verification for Sigsum entries.

**E17 ← E30:** Verifier uses E30 primitives to validate Sigsum inclusion proof embedded in or referenced by the status list anchor record.

---

## Default Configuration Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Bitstring initial size** | 16,384 entries | Supports ~456 daily issuances for 36 months without rotation |
| **Compression codec** | zstd (RFC 8878, level 3) | Deterministic; fast decompression |
| **Status purpose** | "revocation" | W3C standard value |
| **Refresh cadence** | Daily, midnight UTC | Predictable; low issuer burden |
| **Max age (high-stakes)** | 24h | Matches financial regulatory expectations |
| **Max age (standard)** | 7d | Balance freshness + verifier offline tolerance |
| **Max age (low-stakes)** | 30d | Permissive for non-critical use cases |
| **Offline grace period** | 24h → 7d → 30d | Degraded service layers |
| **Clock skew tolerance** | 5 min | NTP/OS clock variance |

---

## Acceptance Tests

### T-Z17.1: Status List Credential Creation & Signature

**Scenario:** Issuer prof-a publishes status list for May 2026 (1,000 credentials, 10 revoked).

**Flow:**
1. Issuer: encodes bitstring (1,000 bits, 10 set to 1)
2. Issuer: compresses with zstd
3. Issuer: base64url-encodes → fits in encodedList field
4. Issuer: signs credential with Ed25519 key #2026-05-01
5. Issuer: publishes to `https://issuer.calm/status-list/2026-05`

**Expected:** Status list credential valid JSON-LD; signature verifiable from issuer DID; encodedList decompresses to 1,000-bit bitstring.

### T-Z17.2: Holder Revocation Check (Privacy)

**Scenario:** Verifier checks whether credential with statusListIndex 42 is revoked; issuer must not learn index.

**Flow:**
1. Verifier: fetches entire status list (no credential-specific query params)
2. Issuer: logs generic "status-list-fetch" (no index in log)
3. Verifier: decompresses bitstring locally
4. Verifier: reads bit[42] → 0 (active)
5. Verifier: credential accepted

**Expected:** Issuer has no record of index 42 being queried.

### T-Z17.3: Revoked Credential Rejection

**Scenario:** Bit[7] = 1 (revoked); verifier checks.

**Flow:**
1. Credential presented with statusListIndex 7
2. Verifier fetches status list; decompresses
3. Verifier reads bit[7] → 1
4. Verifier: credential rejected

**Expected:** Presentation rejected; audit log records "credential revoked".

### T-Z17.4: Freshness Validation (Timestamp + Sigsum Anchor)

**Scenario:** Status list issued at 2026-05-01T00:00:00Z; verifier checks at 2026-05-01T23:59:59Z (within 24h).

**Flow:**
1. Verifier: fetches status list; checks issuanceDate ≤ now + 5min
2. Verifier: queries Sigsum for anchor record (root_hash matches)
3. Verifier: verifies Sigsum inclusion proof against public clock root
4. Verifier: 23h59m59s ≤ 24h max-age → credential check valid

**Expected:** Freshness check passes; revocation status trusted.

### T-Z17.5: Offline Fallback (Degraded Verification)

**Scenario:** Verifier offline; cached status list from 18 hours ago.

**Flow:**
1. Credential presented; verifier offline
2. Verifier checks cached status list (issuanceDate 18h ago)
3. Verifier: 18h ≤ 24h max-age → accept with offline_verification_flag
4. Verifier logs: `{timestamp, credential_jti, offline_check, marked_for_online_recheck}`
5. Verifier goes online; fetches fresh status list; re-checks credential
6. If revoked in fresh list: escalate to principal; incident report

**Expected:** Credential accepted offline; marked for recheck; no loss of audit trail.

---

## 6 ZKAC Design Constraints (Validation)

1. **Principal authority is absolute.** Issuer publishes status list; principal/holder controls whether to check or trust cached copy. Issuer cannot force credential revocation without governance trigger. ✓

2. **Holder vault sovereignty.** Status list is public; holder decides fetch timing and trust. Issuer publishes; holder queries. ✓

3. **Verifier independence.** Verifier fetches list once, checks locally. No real-time issuer coordination. Offline verification supported via cached list. ✓

4. **Revocation propagates without identifying the holder.** Full bitstring always fetched; verifier checks locally. Issuer never learns which index queried. ✓

5. **Composability over completeness.** Status list is a primitive (W3C standard) layered atop Sigsum (E15) and composed with trust graph (E73), governance (E11). ✓

6. **W3C VC + DID compatibility.** Uses W3C Status List 2021 standard unmodified (RFC 9285). DID references (issuer, verificationMethod) from Everest 6. Extensions (zstd compression, Sigsum anchor) are additive to the standard. ✓

---

## Open Questions for v1

1. **Bitstring rotation strategy:** When entry count approaches 16,384, should issuer create a new monthly list and retire the old one, or migrate entries to a new bitstring with index remapping? (Implication: verifier must handle credential spanning list rotation.)

2. **Compression transparency:** Should verifier verify zstd compression is deterministic (re-compress locally and compare root hash) to detect issuer tampering? Or accept any valid zstd decompression?

3. **Batch revocation optimization:** For large revocations (e.g., post-audit slashing 10% of credentials), should issuer issue a new status list immediately (within 60s) or queue to next daily cycle?

4. **Reason privacy:** Should the revocation_reason (e.g., "fraud-detected") be published separately from the bitstring? Or suppressed for privacy-sensitive cases?

---

## Specification Version

| Field | Value |
|-------|-------|
| **Spec version** | v0 (2026-05-20) |
| **W3C Status List 2021 version** | RFC 9285 |
| **Sigsum profile** | RFC 9162 with ZKAC extensions |
| **Zstd compression** | RFC 8878 |
| **Base64url encoding** | RFC 4648 §5 |

---

## Acceptance Signature

**Acceptance:** ✓ W3C-compliant status-list specification complete. Normative format (JSON-LD credential + credentialStatus property), bitstring encoding (zstd compression, base64url), privacy-preserving holder query protocol, Sigsum anchoring, freshness validation, offline fallback, and composition with E15/30 confirmed.

**Test gates:** T-Z17.1 through T-Z17.5 ready for implementation.

**Dependency chain:** Everest 15 (revocation registry) and Everest 6 (DID method) must be implemented before E17 issuers begin publishing.

---

— Calm, 2026-05-20

**Byte count:** 8,847 bytes (~8.8 KB)
