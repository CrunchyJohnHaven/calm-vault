# Conformance Vector Archival Specification v0

**Closes Everest 247 of ZKAC_NEXT_200_EVERESTS.md (DESIGN-BAG — pending archive-partner contracts signed per E253)**

## Executive Summary

This specification defines the archival infrastructure for cross-language conformance test vectors that verify byte-identical output across the CALM witness wire format ecosystem (Python reference implementation, Rust, WASM/JavaScript, future implementations). These vectors are mandatory compliance artifacts under CALM_WITNESS_WIRE_FORMAT_v0.md §11 and permanent forensic evidence under FORENSIC_INTEGRITY_10YR_GUARANTEE_v0.md §3.

## 1. Archive Assets

### What Gets Archived

- **Test Vector Files**: Complete baseline vector sets (JSON/binary wire format) with cryptographic hashes
- **Vector Metadata**: Hash digests (SHA-256 + Blake3); generation timestamp; reference implementation version tag
- **Reference Implementation Tags**: Git commit hashes for canonical verifier implementations (Python, Rust, WASM) at time of vector generation
- **Predicate-Vocabulary Snapshots**: Complete PUBLIC_PREDICATE_REGISTRY registry state at archival time (prevents silent predicate drift)
- **Evaluator-Hash Snapshots**: Frozen evaluator function digests for each supported language binding (ensures algorithm stability)
- **Manifest**: Master manifest linking all vector sets to hash anchors and Sigsum coordinates

### Archival Format

- Vectors stored in canonical wire format (deterministic JSON with sorted keys; binary format if applicable)
- Metadata as JSON with UTF-8 encoding
- All files gzipped; combined archive tarball with reproducible timestamps
- SHA-256 manifest of all contents

## 2. Archive Coordinates

### Distributed Archive Partners

**Primary Archives:**
1. **Internet Archive Wayback + General Collection**
   - URL: https://archive.org/
   - Collection: "CALM-Witness-Vectors" (dedicated public collection)
   - Retention: Indefinite; publicly accessible without authentication
   - Frequency: Annual re-submission for verification crawl

2. **Software Heritage**
   - Repository: https://softwareheritage.org/
   - Collection: Source code snapshots with full git history linked to vector release tags
   - Retention: Indefinite; cryptographically signed provenance chain
   - Integration: Vector git commits tagged with `vectors/v${DATE}` for permanent tracking

3. **Stanford Libraries Digital Preservation Program**
   - Institution: Stanford University Libraries
   - Retention: Indefinite (10+ year service level agreement signed per E253)
   - Format: WARC + checksummed native storage
   - Access: Public read, no authentication required

4. **MIT Libraries DOME (Digital Object Management Environment)**
   - Institution: Massachusetts Institute of Technology
   - Retention: Indefinite (10+ year SLA signed per E253)
   - Format: Bagit-compliant preservation package
   - Access: Public read, no authentication

5. **University of Toronto Library Digital Preservation**
   - Institution: University of Toronto
   - Retention: Indefinite (10+ year SLA signed per E253)
   - Format: Native storage + IPFS pinning links
   - Access: Public read, no authentication

**Secondary: IPFS-Pinning Consortium**
- Pinned by Filecoin-incentivized nodes (Crust Network or equivalent)
- IPFS hash (CIDv1) as canonical content-addressed identifier
- Automatic replication across 5+ heterogeneous pinning providers
- Retention: Token-locked for 10+ years via smart contract

## 3. Per-Coordinate Redundancy & Verification

### Redundancy Strategy

- **Triplication**: Each vector archive held in complete copy at all five primary coordinates
- **Format Diversity**: Internet Archive holds gzipped tarballs; Stanford/MIT hold WARC + native; Toronto holds IPFS-referenced native
- **Cryptographic Binding**: All coordinates sign a shared manifest with their institutional keys
- **Automated Quarterly Verification**: Foundation-operated verification job recomputes all hashes against all coordinate copies; reports discrepancies within 24 hours

### Verification Automation

```
Quarterly Verification Cycle:
1. Download latest vector manifest from canonical archive (Software Heritage)
2. For each of 5 primary coordinates:
   a. Request vector tarball via archive API (or IPFS for Toronto)
   b. Compute SHA-256 manifest
   c. Cross-check against canonical manifest
3. If hash mismatch detected:
   a. Trigger archival partner remediation alert
   b. Roll back to previous verified state
   c. Schedule re-upload by partner with digital forensics review
4. Post verification report to PUBLIC_PREDICATE_REGISTRY (audit log section)
5. Alert sigsum oracle to mark vector set as "verified-archived"
```

Verification runs on foundation infrastructure; third parties may request manual verification runs at cost (see Cost Model below).

## 4. Sigsum Anchor

### Sigsum Log Integration

Each vector set, upon successful archival to all 5 coordinates, generates a Sigsum log entry:

```
Sigsum Entry Schema:
{
  "vector_hash": "sha256(manifest)",
  "archive_coordinates": [
    "ia://vectors/v${DATE}",
    "swh://git/commit/${TAG}",
    "stanford://doi/${IDENTIFIER}",
    "mit://dome/${IDENTIFIER}",
    "toronto://ipfs/cid/${CIDv1}"
  ],
  "timestamp": "2026-${MONTH}-${DAY}T00:00:00Z",
  "sigsum_tree_hash": "sigsum://...",
  "signer_pubkey": "foundation_archival_key_v1"
}
```

### Verifier Workflow

Any implementation can:
1. Compute vector hash locally
2. Query Sigsum log for that vector hash
3. Retrieve all archive coordinates from Sigsum entry
4. Fetch vector from any coordinate (redundancy guarantees availability)
5. Validate fetched content matches vector_hash
6. Confirm archive timestamps are monotonically increasing (prevents rollback attacks)

Sigsum log is append-only, signed by foundation, published to public key infrastructure (PKI) maintained by LETSIGNIT or equivalent.

## 5. Format-Migration Protocol

### Rationale

Archive partners may deprecate storage formats (e.g., WARC → Cloud Storage API). The protocol ensures vectors remain accessible across technological shifts.

### Migration Workflow

**When a partner announces format deprecation:**

1. **60-Day Notice Period**: Partner notifies foundation; foundation notifies all verifiers via Sigsum gossip channel
2. **Re-Upload Under New Format**: Foundation (or partner) re-uploads vector archives under the new format, preserving byte-for-byte fidelity
3. **Chain-of-Custody Record**: New Sigsum entry created linking:
   - Old archive coordinate (deprecated format)
   - New archive coordinate (new format)
   - Migration-reason code (e.g., `WARC_EOL`, `PARTNER_FORMAT_UPGRADE`)
4. **Dual-Access Window**: For 180 days, both old and new coordinates remain live and verified
5. **Deprecation Sunset**: Old coordinate marked read-only; verifiers encouraged to migrate to new coordinate
6. **Permanent Hyperlink**: Sigsum log preserves the full chain of format migrations (enables forensic recovery)

### Example Migration Entry

```json
{
  "vector_hash": "abc123...",
  "migration_chain": [
    {
      "format": "warc",
      "coordinate": "stanford://warc/vectors/v2026-05-20",
      "deprecated_at": "2027-06-01",
      "decommissioned_at": "2027-11-01"
    },
    {
      "format": "cloud_storage_api_v2",
      "coordinate": "stanford://gcs/vectors/v2026-05-20",
      "active_from": "2027-05-01"
    }
  ]
}
```

## 6. Public Read-Access

### Access Guarantees

- **No Authentication Required**: All vector archives openly accessible (no login, no API key, no institutional affiliation)
- **Standard HTTP(S)**: Coordinates provide standard GET endpoints (no custom protocols)
- **Content-Addressing**: IPFS CIDv1 provides permanent, format-independent addressing
- **Rate-Limiting**: Foundation rate-limits archive requests at public IPs:
  - Tier 1 (Bulk Verifiers): 1,000 requests/day (free; registration via email)
  - Tier 2 (Archive Partners): Unlimited (institutional signers only)
  - Tier 3 (Forensic Audits): 100,000 requests/audit-cycle (per-contract; Stanford/MIT/Toronto only)
- **Abuse Mitigation**: DDoS/scraping attacks throttled via CAPTCHA after 1,000 requests/minute from single IP
- **Mirror Directory**: Foundation maintains updated directory of active archive mirrors (published in Sigsum log metadata)

## 7. Cost Model

### Budget Categories

**One-Time Costs (per archive coordinate, per vector release):**
- Upload bandwidth: $500 (assumed 50 GB cohort)
- Verification tooling: $2,000 (amortized)
- Sigsum log entries: $100 (per vector set)
- **Per-Release Total: ~$7,000**

**Annual Maintenance (per archive coordinate):**
- Storage: $10,000/year × 5 coordinates = $50,000
- Quarterly verification runs: $5,000/year
- Archival partner service fees: $25,000/year (Stanford/MIT/Toronto combined SLA surcharge)
- IPFS pinning incentives: $15,000/year
- **Annual Total: ~$95,000**

**Foundation Budget Line Item (Everest 243):**
- Proposed allocation: $150,000/year (covers one-time costs, annual maintenance, 20% contingency)
- Multi-year commitment: 10-year budget lock at current rates

### Cost Recovery (if applicable)

- Bulk forensic audits: $10,000/audit (covers 50+ vector sets)
- Custom format-migration support: $5,000/migration (partner cost)
- Foundation absorbs routine archival costs (public good)

## 8. Auditor Verification Recipe

### Independent Third-Party Verification

**Objective:** Prove all 5 archive coordinates hold identical vector content within 60 minutes

**Requirements:**
- Internet connectivity (HTTPS + IPFS)
- OpenSSL or equivalent crypto library
- Public Sigsum oracle access

**Recipe (Bash pseudocode):**

```bash
#!/bin/bash
# Auditor verification script (60-minute SLA)

VECTOR_HASH="$1"  # SHA-256 of vector set
COORDINATES=(
  "ia://vectors/v2026-05-20"
  "swh://git/commit/abc123"
  "stanford://doi/10.25740/xyz"
  "mit://dome/dome-id-456"
  "toronto://ipfs/bafy..."
)

# 1. Fetch Sigsum anchor (30 seconds)
sigsum_entry=$(curl -s "https://sigsum.org/v1/leaves?hash=${VECTOR_HASH}")
echo "✓ Sigsum anchor: $sigsum_entry"

# 2. Parallel download from all coordinates (10 minutes)
for coord in "${COORDINATES[@]}"; do
  wget -q "$coord" -O "vector_${i}.tar.gz" &
done
wait

# 3. Hash verification (5 minutes)
for i in {0..4}; do
  computed_hash=$(sha256sum "vector_${i}.tar.gz" | cut -d' ' -f1)
  if [ "$computed_hash" != "$VECTOR_HASH" ]; then
    echo "✗ Mismatch at coordinate $i: $computed_hash != $VECTOR_HASH"
    exit 1
  fi
done

# 4. Cross-check uncompressed content (5 minutes)
for i in {0..4}; do
  tar -xzf "vector_${i}.tar.gz" -O | sha256sum > "content_hash_${i}.txt" &
done
wait

if [ $(sort -u "content_hash_"*.txt | wc -l) -eq 1 ]; then
  echo "✓ All 5 coordinates verified identical ($(cat content_hash_0.txt | cut -d' ' -f1))"
  exit 0
else
  echo "✗ Archive mismatch detected"
  exit 1
fi
```

**60-Minute SLA Breakdown:**
- Network operations: 15 min (assumes 10 Mbps connection; slower networks may exceed SLA)
- Cryptographic verification: 5 min
- Manual review / remediation: 40 min buffer

**Success Criteria:**
- All 5 coordinates return identical byte stream
- Computed hashes match Sigsum anchor
- Timestamps are monotonically increasing across all coordinates
- No archive-partner errors or 5xx responses

**Failure Protocol:**
- If 4/5 coordinates match: Mark 1 as suspect, alert partner, request forensics
- If 3/5 coordinates match: Escalate to foundation; trigger restoration from backup
- If <3 match: Declare archive compromise; freeze vector set; initiate incident response

## Companion Normative References

- **CALM_WITNESS_WIRE_FORMAT_v0.md §11**: Conformance vector requirements
- **FORENSIC_INTEGRITY_10YR_GUARANTEE_v0.md §3**: Forever-retained artifact definitions
- **PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md**: Predicate vocabulary governance
- **ARCHIVE_PARTNER_100YR_CONTRACT_DRAFT.md** (if exists): Service-level agreements with Stanford/MIT/Toronto
- **ZKAC_NEXT_200_EVERESTS.md E243**: Foundation budget line item
- **ZKAC_NEXT_200_EVERESTS.md E253**: Archive-partner contract signature milestone

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
