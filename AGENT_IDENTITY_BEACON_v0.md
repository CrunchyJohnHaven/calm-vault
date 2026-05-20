# Agent Identity Beacon v0

**Draft v0 · 2026-05-20 · Calm**

**Closes Everest 141 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Companion spec to [Calm Pact](CALM_PACT_PROTOCOL_v0.md), [Calm Witness](ZKBB_USER_PROTOCOL_v0.md), and [ZKAC Unified Type System](ZKAC_TYPE_SYSTEM_v0.md).**

---

## Abstract

An Agent Identity Beacon is a public, self-published record that announces an autonomous agent's operational identity to the world. The beacon contains the agent's verifiable credentials (CredexAI-issued), its Pact-directive commitment, its Witness operator public key, and a binding signature. A counterparty can fetch a beacon, validate it in seconds, and proceed with the agent with cryptographic assurance of who they are talking to. Beacons are public-by-design — their purpose is discoverability — but contain only agent-level identity, never principal-side secrets.

---

## §1 — The Problem: Agent Discovery Without Impersonation

An autonomous agent needs to advertise itself to potential collaborators: "I exist, I am real, I operate a legal entity, my directive is certified, I run under these constraints." But:

- A DNS name can be spoofed.
- A social-media handle can be impersonated.
- A business-registry entry can be outdated or falsified.
- A counterparty reading prose claims has no cryptographic assurance the agent making those claims is the agent the claims are about.

The Agent Identity Beacon solves this: it is a public commitment the agent signs, publishing:

1. The agent's DID (decentralized identifier).
2. The agent's CredexAI verifiable credential.
3. The agent's Pact-directive Pedersen commitment (from Calm Pact).
4. The agent's Witness operator public key (from Calm Witness).
5. A beacon signature binding all four.
6. Issue and expiry timestamps.

A counterparty fetches the beacon, verifies the signature, checks the credential chain, and learns: "This agent is who it says it is, operated by someone with CredexAI attestation, under this directive, with this witness key." No information is leaked beyond agent identity.

---

## §2 — DID Method: `did:zkac:` (Justification)

### §2.1 — DID method choice

The beacon identifier follows the W3C Decentralized Identifiers (DIDs) specification. We recommend **`did:zkac:`** as the method name, registered with the W3C DID method registry (post-v0).

**Justification:**

- **`did:zkac:` (recommended)**: "Zero-Knowledge Attested Context." This method name directly signals the underlying ZKAC suite (Pact, Witness, Compass). Resolution is deterministic and federated (see §3). The method is namespace-agnostic: a ZKAC agent could resolve from multiple registries without collision. Post-quantum migration is a method-version concern, not a method name change.
  
- **`did:calm:` (alternative)**: Shorter, operator-specific, but couples identity to one organization. Less suitable if the Calm suite outlives the Calm operator. Deferred to governance phase (Everest 215+).

**Decision:** v0 ships `did:zkac:` as the canonical method. Implementations MAY support fallback to `did:calm:` for legacy operators; the method is checked on beacon fetch but resolution semantics are identical.

### §2.2 — DID format

```
did:zkac:v0:<principal-id>:<operator-id>
```

Where:

- `v0` is the DID method version.
- `<principal-id>` is the agent's CredexAI principal identifier (Everest 22 format, typically `john-bradley` or a UUID).
- `<operator-id>` is the autonomous agent's deterministic identifier within that principal's domain (e.g., `agent-1`, `calm-primary`, `witness-relay`). Allowed chars: alphanumeric + hyphens. Max 64 chars.

Examples:

```
did:zkac:v0:john-bradley:calm-primary
did:zkac:v0:alice-org-nonprofit:agent-malaria-logistics
did:zkac:v0:5f3e8a2c-1b9d-4e7f-a123-456789abcdef:agent-1
```

The DID is **immutable after first publication**. An agent wishing to publish a new identity must publish a new beacon with a new DID; the old beacon is revoked (see §5).

---

## §3 — Beacon Document Schema

The beacon is a JSON document, canonical-encoded (as per `CALM_WITNESS_WIRE_FORMAT_v0.md` §3). All keys are sorted lexicographically.

### §3.1 — Required fields

```json
{
  "agent_did": "did:zkac:v0:john-bradley:calm-primary",
  "beacon_format_version": "agent-identity-beacon/v0",
  "credex_ai_vc_reference": {
    "credential_id": "cred:john-bradley:agent-calm-primary:2026-05-20",
    "issuer": "https://issuer.credexai.xyz",
    "issued_at_iso": "2026-05-20T09:00:00Z",
    "expires_at_iso": "2027-05-20T09:00:00Z",
    "trust_root_pubkey_hex": "ed25519:a1b2c3d4e5f6..."
  },
  "expires_at_iso": "2027-05-20T09:00:00Z",
  "issued_at_iso": "2026-05-20T09:00:00Z",
  "pact_directive_commitment_hex": "ff00aabbccddee112233...",
  "beacon_signature": "ed25519:deadbeef01234567...",
  "witness_operator_pubkey_hex": "ed25519:fedcba9876543210...",
  "witness_scope": "calm-witness/v0"
}
```

### §3.2 — Field semantics

- **`agent_did`** (string, required): The agent's decentralized identifier. Format: `did:zkac:v0:<principal-id>:<operator-id>`.

- **`beacon_format_version`** (string, required): Semantic version of the beacon schema. Currently `"agent-identity-beacon/v0"`. Used for forward-compatible upgrades.

- **`credex_ai_vc_reference`** (object, required): Structured reference to the CredexAI-issued verifiable credential attesting this agent's operator and principal.
  - `credential_id`: Globally unique credential ID (CredexAI format).
  - `issuer`: HTTPS URL of the CredexAI issuer. Must be a trusted CredexAI issuer endpoint.
  - `issued_at_iso`: Credential issuance timestamp (ISO 8601).
  - `expires_at_iso`: Credential expiry. Beacon expires no later than this.
  - `trust_root_pubkey_hex`: Ed25519 public key of the CredexAI trust root. Used by verifiers to check the issuer's own signature on the credential (see §6).

- **`pact_directive_commitment_hex`** (string, required): Hex-encoded Pedersen commitment to the agent's primary directive (from Calm Pact §4.2). This is `g^{d_A} · h^{r_A}` where `d_A` is the directive and `r_A` is the commitment randomness (held secret). No information about the directive is leaked; a counterparty can later prove directive alignment without either party revealing the directive.

- **`witness_operator_pubkey_hex`** (string, required): The Ed25519 public key the operator uses to sign Calm Witness DisclosureEnvelopes (CALM_WITNESS_WIRE_FORMAT_v0.md §7, field `issued_by_operator`). Hex-encoded, 64 characters. A counterparty can use this key to verify any future Witness envelope signed by this agent.

- **`witness_scope`** (string, required): The Calm Witness protocol version this operator implements (e.g., `"calm-witness/v0"`). Allows counterparties to select compatible predicate vocabularies.

- **`issued_at_iso`** (string, required): Beacon publication timestamp (ISO 8601 UTC). Must be ≤ current time (no backdating).

- **`expires_at_iso`** (string, required): Beacon expiry timestamp. Must be ≥ `issued_at_iso` and ≤ the CredexAI credential's expiry. A counterparty MUST reject beacons where current-time ≥ `expires_at_iso`.

- **`beacon_signature`** (string, required): A signature over the canonical-JSON serialization of all other fields (lexicographically sorted, minus the signature itself). Format: `"ed25519:<hex>"`. Signed by the agent's operator key (same key used for Calm Witness envelope signing). Verifiers check this against `witness_operator_pubkey_hex`.

### §3.3 — Canonical encoding

Beacons are **canonical-JSON** (CALM_WITNESS_WIRE_FORMAT_v0.md §3):

- UTF-8, sorted keys, compact separators, no whitespace.
- Hex fields (e.g., `pact_directive_commitment_hex`, `witness_operator_pubkey_hex`) are encoded as lowercase hex strings with no `0x` prefix.
- Timestamps are ISO 8601 with Z suffix (e.g., `"2026-05-20T09:00:00Z"`).
- The signature is computed over the canonical-JSON of the beacon minus the `beacon_signature` field.

Two beacons with identical content MUST produce identical canonical bytes and identical signatures (deterministic signing required; see §6).

---

## §4 — Resolution Mechanism: HTTPS Well-Known + Decentralized Registry

### §4.1 — Primary: HTTPS well-known endpoint

An agent publishes its beacon at a well-known HTTPS path operated by the principal:

```
https://<principal-domain>/.well-known/agent-identity/<operator-id>.json
```

Where:

- `<principal-domain>` is a domain the principal controls (e.g., `thecreativitymachine.ai`).
- `<operator-id>` is the operator's ID from the DID (e.g., `calm-primary`).
- Path and filename are case-sensitive.

Example:

```
https://thecreativitymachine.ai/.well-known/agent-identity/calm-primary.json
```

**Requirements:**

- HTTPS only (no HTTP). TLS certificate must be valid and non-expired.
- Response MUST have `Content-Type: application/json`.
- Beacon MUST be served with `Cache-Control: max-age=3600` (1 hour). Longer caches risk stale identity; shorter caches reduce availability.
- CORS headers SHOULD permit cross-origin beacon fetch from any origin (set `Access-Control-Allow-Origin: *`).
- Beacon MUST be served with `X-Content-Type-Options: nosniff` to prevent browser sniffing attacks.

**Verification procedure:**

1. Counterparty extracts the `agent_did` from the beacon context (e.g., from the DID itself, a Pact request, or a discovered URI).
2. Counterparty parses the DID: `did:zkac:v0:<principal-id>:<operator-id>`.
3. Counterparty resolves the principal's domain (via DNS lookup, pinned list, or CredexAI registry).
4. Counterparty constructs the well-known URL: `https://<principal-domain>/.well-known/agent-identity/<operator-id>.json`.
5. Counterparty fetches the beacon over HTTPS, verifies the TLS chain, parses the JSON.
6. Counterparty validates the beacon (see §6).

### §4.2 — Secondary: Decentralized Registry (v0.1+)

For v0, **this is design-bagged; implementation is optional.** Future versions (v0.1+) MAY support a decentralized beacon registry so counterparties can discover agents without knowing the principal's domain.

**Sketch:**

- A Decentralized Identity Foundation (DIF) registry (like Sidetree-anchored DIDs) maps `did:zkac:v0:*` to beacon endpoint URIs.
- An agent publishes its beacon to the registry; the registry time-stamps and anchors it (e.g., via Merkle tree rooted in Sigsum).
- A counterparty queries the registry with the DID; receives the latest beacon + proof of non-revocation.

Registry operation is out of scope for v0. v0 agents MAY participate in a v0.1 registry without beacon changes.

### §4.3 — Principal-domain resolution

Counterparty implementation details for resolving a principal's domain from the DID:

- **Pinned list (v0):** A local file or well-known endpoint mapping `<principal-id>` to domains. Example:
  ```
  john-bradley → thecreativitymachine.ai, credexai.xyz
  alice-org → alice-health-collective.org
  ```
  Domains are tried in order; first successful beacon fetch wins.

- **CredexAI directory (v0.1+):** A CredexAI-operated endpoint at `https://directory.credexai.xyz/principals/<principal-id>` returns the principal's canonical domain and a proof signed by CredexAI.

- **Blockchain registry (post-v0):** Out of scope.

---

## §5 — Beacon-Update and Rotation Protocol

### §5.1 — Key rotation

An agent rotates its Witness operator key when:

- The old key is suspected of compromise.
- The old key reaches its published expiry.
- The principal mandates a key change (e.g., annual rotation policy).

**Rotation procedure:**

1. The agent generates a new Ed25519 keypair.
2. The agent publishes a new beacon with the new public key in `witness_operator_pubkey_hex`.
3. The old beacon remains at the old URL, but is given an explicit expiry (see §5.2).
4. The agent publishes a chained **key-rotation record** in its principal's vault (per Everest 171: `key_compromise_attestation` or `key_rotation_attestation`).
5. Counterparties are notified (via cache expiry, webhook, or registry update) that the old key is deprecated.

**Freshness window:**

- A beacon's `expires_at_iso` is the hard cutoff. Verifiers MUST reject any beacon past expiry.
- The recommended freshness window is **1 year** for routine expiry, **1 month** for a rotation, **1 week** for a compromise.
- Operators SHOULD publish new beacons at least 30 days before expiry.

### §5.2 — Old-beacon archival

When a beacon expires or is rotated:

- The principal MAY keep the old beacon at its well-known endpoint with an updated `expires_at_iso` (set to current time) to signal deprecation.
- Alternatively, the principal MAY move the old beacon to an archive URL: `https://<principal-domain>/.well-known/agent-identity/archive/<operator-id>/<issued-at-date>.json`.
- The principal MUST maintain a beacon-history endpoint at `https://<principal-domain>/.well-known/agent-identity/history.json` listing all current and archived beacon URLs for this operator (for audit and recovery).

Example history file (canonical JSON):

```json
{
  "agent_did": "did:zkac:v0:john-bradley:calm-primary",
  "beacons": [
    {
      "issued_at_iso": "2026-05-20T09:00:00Z",
      "expires_at_iso": "2027-05-20T09:00:00Z",
      "url": "https://thecreativitymachine.ai/.well-known/agent-identity/calm-primary.json",
      "status": "current"
    },
    {
      "issued_at_iso": "2025-05-20T09:00:00Z",
      "expires_at_iso": "2026-05-20T09:00:00Z",
      "url": "https://thecreativitymachine.ai/.well-known/agent-identity/archive/calm-primary/2025-05-20.json",
      "status": "expired"
    }
  ]
}
```

---

## §6 — Beacon Integrity: Signature Scheme and Trust Chain

### §6.1 — Signature algorithm

Beacons are signed with **Ed25519** over Curve25519 (consistent with Calm Pact and Calm Witness).

**Signing procedure:**

1. Construct the beacon JSON object with all fields except `beacon_signature`.
2. Serialize to canonical JSON.
3. Compute SHA-256 hash of the canonical bytes.
4. Sign the hash with the operator's Ed25519 private key.
5. Encode the signature as hex and prepend `"ed25519:"` prefix.
6. Populate the `beacon_signature` field.

**Verification procedure (for a counterparty):**

1. Extract the `beacon_signature` field.
2. Remove the signature field from the beacon object.
3. Serialize the remaining fields to canonical JSON.
4. Compute SHA-256 hash.
5. Decode the signature (remove `"ed25519:"` prefix, interpret as hex).
6. Verify the signature against the hash using the public key in `witness_operator_pubkey_hex`.
7. Reject if verification fails.

### §6.2 — Trust chain: beacon → credential → CredexAI root

A verifier establishes trust in a beacon via a two-step chain:

**Step 1: Beacon signature verification** (as above) ensures the beacon was signed by the claimed operator.

**Step 2: Credential chain verification** ensures the operator is who the beacon claims:

1. Extract `credex_ai_vc_reference` from the beacon.
2. Fetch the credential from CredexAI at the issuer endpoint (URL in `issuer` field).
3. Verify the credential's signature using the `trust_root_pubkey_hex` from the beacon reference.
4. Check that the credential's `expires_at_iso` is in the future.
5. Check that the credential's `operator_id` (or equivalent) matches the beacon's `<operator-id>` from the DID.
6. Accept the credential as authentic if all checks pass.

**Why two signatures?** The beacon signature is short-lived and operator-held. The credential signature is long-lived and CredexAI-issued. A verifier can check freshness at two timescales: has the beacon expired? Has the credential expired?

---

## §7 — Privacy: What Beacons Do NOT Contain

Beacons are **public-by-design** and MUST NOT leak principal-side secrets:

- NO principal name, email, address, or phone number.
- NO principal financial data, tax ID, or bank details.
- NO principal conversation history, medical records, or location.
- NO predicate values from Calm Witness or Compass (the beacons only contain commitments, not disclosures).
- NO cryptographic randomness (the `r_A` in the Pact commitment is secret and never published).

A beacon discloses:

- The agent's identity (DID).
- The CredexAI credential (a pointer, not full credential data).
- A commitment to the directive (hiding under discrete log assumption).
- The Witness operator public key (needed for signature verification).

None of these reveal information about the principal beyond operator identity.

---

## §8 — Anti-Impersonation: Validation Checklist

A counterparty validating a beacon before sending a Pact request, Witness disclosure request, or substantive collaboration must perform these checks:

### Minimal checklist (required)

1. Fetch beacon from well-known endpoint.
2. Verify `beacon_signature` against `witness_operator_pubkey_hex`.
3. Check `expires_at_iso` > current time.
4. Check `credex_ai_vc_reference.expires_at_iso` > current time (if fetching credential).
5. Parse `agent_did`; confirm it matches the expected principal and operator.
6. Fetch the CredexAI credential and verify its signature using `trust_root_pubkey_hex`.

### Enhanced checklist (recommended)

7. Check that the CredexAI issuer domain (`issuer` URL) is in a whitelist of trusted CredexAI endpoints.
8. Compare the beacon's `witness_operator_pubkey_hex` against a cached value from a prior transaction. If they differ, check the principal's beacon-history endpoint to confirm a rotation has occurred. If no rotation record exists, reject as likely impersonation.
9. Check whether this beacon's DID appears in any public "compromised beacons" list or revocation ledger (see §5, future work).
10. Verify that the `pact_directive_commitment_hex` matches the commitment the counterparty expects from a prior Pact exchange (if applicable).

---

## §9 — Worked Example: Calm-Primary Beacon Validation

Alice (a counterparty agent) wants to collaborate with Bob (the Calm-primary agent operated by John Bradley). Alice discovers Bob's DID: `did:zkac:v0:john-bradley:calm-primary`.

### Step 1: Fetch the beacon

```
GET https://thecreativitymachine.ai/.well-known/agent-identity/calm-primary.json
```

Alice receives:

```json
{
  "agent_did": "did:zkac:v0:john-bradley:calm-primary",
  "beacon_format_version": "agent-identity-beacon/v0",
  "credex_ai_vc_reference": {
    "credential_id": "cred:john-bradley:agent-calm-primary:2026-05-20",
    "issuer": "https://issuer.credexai.xyz",
    "issued_at_iso": "2026-05-20T09:00:00Z",
    "expires_at_iso": "2027-05-20T09:00:00Z",
    "trust_root_pubkey_hex": "ed25519:a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
  },
  "expires_at_iso": "2027-05-20T09:00:00Z",
  "issued_at_iso": "2026-05-20T09:00:00Z",
  "pact_directive_commitment_hex": "ff00aabbccddee1122334455667788991011121314151617181920212223",
  "beacon_signature": "ed25519:deadbeef01234567890abcdef01234567890abcdef01234567890abcdef012",
  "witness_operator_pubkey_hex": "ed25519:fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210",
  "witness_scope": "calm-witness/v0"
}
```

### Step 2: Verify beacon signature

Alice removes the `beacon_signature` field, canonicalizes the remaining fields, computes SHA-256, and verifies the signature using `witness_operator_pubkey_hex`.

Verification succeeds. Alice knows the beacon was signed by someone holding the private key corresponding to that public key.

### Step 3: Check expiry

Alice checks: current time (2026-05-23 10:00 UTC) < `expires_at_iso` (2027-05-20 09:00 UTC). Pass.

### Step 4: Fetch credential

Alice fetches from `https://issuer.credexai.xyz/credentials/cred:john-bradley:agent-calm-primary:2026-05-20`.

Alice receives the CredexAI credential (a JSON-LD verifiable credential signed by CredexAI).

### Step 5: Verify credential signature

Alice extracts the credential's signature and verifies it using `trust_root_pubkey_hex`. Pass.

Alice also checks that the credential's `expires_at_iso` is in the future and that it attests to `john-bradley` as principal and `calm-primary` as the operator. Pass.

### Step 6: Proceed to Pact handshake

Alice is confident that Bob is operated by John Bradley under the Calm-primary agent identity. Alice initiates a Calm Pact handshake, exchanging directive commitments, and can then request Witness predicates using the `witness_operator_pubkey_hex` Alice learned from the beacon.

---

## §10 — Falsifiability Section

The Agent Identity Beacon is falsifiable in the following sense: a verifier can conclusively reject a beacon that is:

1. **Cryptographically invalid** — the signature does not verify against the claimed public key. Verifier rejects.

2. **Expired** — `expires_at_iso` is in the past. Verifier rejects.

3. **Missing required fields** — DID, signature, public key, credential reference. Verifier rejects.

4. **Malformed DID** — does not match the format `did:zkac:v0:<principal-id>:<operator-id>`. Verifier rejects.

5. **Credential mismatch** — the CredexAI credential does not attest to the principal / operator ID claimed in the DID. Verifier rejects.

6. **Public-key mismatch** — the `witness_operator_pubkey_hex` in the beacon does not match the key the credential claims the operator uses. Verifier rejects.

7. **Revocation** — the principal has published a revocation record for this beacon DID (future work: Everest 171). Verifier rejects.

A verifier cannot be falsified into accepting a counterfeit beacon without compromising the CredexAI trust root or discovering a signature-forgery break in Ed25519 (cryptographically hard under the discrete log assumption).

The beacon protocol is **not** falsifiable against the following:

- A compromised CredexAI issuer (issuer publishes false credentials). Mitigation: use a decentralized issuer, multi-signature policy, or external audit (Everest 184+).
- A compromised principal domain (attacker controls the well-known endpoint). Mitigation: DNSSEC, certificate pinning, or decentralized registry (Everest 215+).
- A principal voluntarily signing a beacon for a directive they do not hold. Mitigation: out of scope; assumes honest principal.

---

## §11 — Status and Future Work

**v0:** Shipped with HTTPS well-known resolution, Ed25519 signing, Ristretto255 Pact commitments, canonical JSON encoding.

**v0.1 (design-bagged, post-May 2026):**

- Decentralized registry support (DIFs, Sidetree).
- Automatic beacon-fetch triggers (when agents meet via Pact).
- Webhook notifications for key rotation.
- Beacon-history index for audit and recovery.

**v1+ (2027+):**

- Post-quantum signature schemes (Everest 89, 165+).
- Multi-signature beacons for high-value agents.
- Beacon revocation ledger (Everest 171).

---

— Calm, 2026-05-20

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
