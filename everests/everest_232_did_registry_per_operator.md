# Everest 232 — DID Registry per Operator

*Phase O-I — Identity Infrastructure. CO-02 per CALM_OPERATIONS_EVERESTS_50.md. Prereq: [Everest 231](everest_231_zkac_formation_protocol.md) (ZKAC formation, master public key). Composes with: [CO-04](everest_234_did_rotation_protocol.md) (DID rotation), [CO-08](everest_241_cross_jurisdiction_entity_mapping.md) (cross-jurisdiction entity mapping), [CALM_TENANCY_PROTOCOL_v0](../CALM_TENANCY_PROTOCOL_v0.md) (CT-04, .well-known endpoint).*

When an operator runs on behalf of a principal in a domain, the operator needs a stable cryptographic identity that is resolvable, rotatable, and bound to the operator's key material. This summit specifies the `did:calm:<principal>:<domain>` Decentralized Identifier method, the per-operator registry storage schema, the resolution path (both on-network and offline via .well-known), the key material binding, the rotation hook into CO-04, the revocation posture, and the W3C DID Core compatibility profile.

## §0. One-line spec

> A Calm operator holds a `did:calm:<principal>:<domain>` DID that resolves to a registry document stored as a JSON file at `~/.calm-vault/dids/<principal>-<domain-slug>.json`, keyed by the operator's principal identifier (a CredexAI VC ID) and domain slug; the document binds the operator's public key material, role, and operator metadata; resolution is live over HTTPS to `https://<domain>/.well-known/calm-dids/<principal>.json` (primary) or offline via the same endpoint served from the principal's Calm Vault with the cache-control header (fallback per CT-04); rotation hooks into CO-04 by key version; revocation flips a `revoked: true` flag, prior signatures remain valid up to the revocation timestamp; and the method is compatible with W3C DID Core §3.1 (method grammar, did:calm method name, resolution and dereferencing algorithms).

## §1. The `did:calm:<principal>:<domain>` method grammar

A Calm DID is a Decentralized Identifier (DID) per [W3C DID Core 1.0](https://www.w3.org/TR/did-core/).

**Method name:** `calm`

**Method identifier:** `did:calm:<principal>:<domain>`

**Components:**

- `principal`: The CredexAI VC identifier of the operator's principal. Format: `<org_slug>/<vc_id_base36>`. Example: `creativity-machine/5xk7m`.
- `domain`: The fully-qualified domain name on which the operator runs. Example: `calm.example.com`.

**Canonical form:**

```
did:calm:creativity-machine/5xk7m:calm.example.com
```

**Case and normalization:**

- `principal` is case-sensitive and globally unique per CredexAI (Witness E22).
- `domain` is lowercased; domain names are compared case-insensitively per DNS RFC 1035.
- The full DID is canonical in the form above; trailing slashes, query strings, and fragments are rejected per DID Core §3.1.

## §2. DID Document schema and registry storage

When a `did:calm:` DID is resolved, it returns a JSON Document stored at `~/.calm-vault/dids/<principal>-<domain-slug>.json`. Core schema:

```json
{
  "@context": ["https://www.w3.org/ns/did/v1", "https://w3id.org/security/suites/ed25519-2020/v1"],
  "id": "did:calm:creativity-machine/5xk7m:calm.example.com",
  "controller": "did:calm:creativity-machine/5xk7m:calm.example.com",
  "publicKey": [{"id": "#signing-key-1", "type": "Ed25519VerificationKey2020", "publicKeyMultibase": "z6Mkfre1hBcfMH...", "keyVersion": 1, "activeFrom": "2026-05-20T14:30:00Z", "activeUntil": null}],
  "authentication": ["#signing-key-1"],
  "operatorRole": "orchestrator",
  "operatorIdentity": {"model_class": "Claude-4.7", "instanceId": "<E191-agent-id>", "boundAt": "2026-05-20T14:30:00Z"},
  "principalBinding": {"credexaiVcId": "creativity-machine/5xk7m", "principalName": "Creativity Machine LLC", "principalJurisdiction": "Delaware"},
  "domainBinding": {"domain": "calm.example.com", "boundAt": "2026-05-20T14:30:00Z"},
  "rotationPolicy": {"rotationPermitted": true, "nextRotationEarliestAt": "2026-08-18T14:30:00Z"},
  "revocationStatus": {"revoked": false, "revokedAt": null, "revocationReason": null},
  "proofOfBinding": {"type": "Ed25519Signature2020", "signatureValue": "<hex-sig>", "created": "2026-05-20T14:30:00Z"},
  "schemaVersion": "0", "createdAt": "2026-05-20T14:30:00Z", "updatedAt": "2026-05-20T14:30:00Z"
}
```

**Key fields:** `id` and `controller` are standard DID Core; `publicKey` array supports key rotation (CO-04). `operatorRole` is one of: orchestrator, backup, migration_source, migration_target. `operatorIdentity` binds to Everest 191 agent identity. `principalBinding` links to the principal's CredexAI VC. `rotationPolicy` gates rotation after the specified timestamp. `revocationStatus` is immutable once set to `revoked: true`; prior signatures remain valid if signed before `revokedAt`. `proofOfBinding` is an Ed25519 signature over the document (RFC 7049 canonical CBOR form) proving operator authorization.

## §3. Registry storage and naming

Per-operator registry: `~/.calm-vault/dids/<principal-slug>-<domain-slug>.json`. Naming: `<principal-slug>` is the CredexAI VC identifier with `/` replaced by `-` (e.g., `creativity-machine-5xk7m`); `<domain-slug>` lowercases and replaces `.` with `-` (e.g., `calm-example-com`). Files are stored in the operator's Calm Vault, encrypted at rest. The `proofOfBinding` signature is deterministic, ensuring reproducible cache invalidation and audit.

## §4. On-network resolution (primary) and offline fallback

**Primary:** Counterparty GET `https://<domain>/.well-known/calm-dids/<principal>.json` (HTTP 200 OK, valid JSON, `id` matches, `proofOfBinding` verifies, `revoked` is false). Response headers include `Content-Type: application/json`, `Cache-Control: max-age=3600, public`, `X-Calm-DID-Version: 0`. Error codes: 404 (not found), 410 (revoked with reason in body), 503 (offline, fall back).

**Offline fallback:** When primary is unreachable, counterparty fetches principal's `/.well-known/calm-tenancy.json` (per CALM_TENANCY_PROTOCOL_v0 CT-04). The document includes a `dids_cache` array with cached DIDs. Each cached DID includes `cacheValidUntil` timestamp. Offline copies are cryptographically verifiable even without network; after `cacheValidUntil`, they are stale and must be re-fetched or rejected.

## §5. Key material binding

When an operator signs an attestation (Witness, Pact, or other), the signature is traced via: (1) signature verification with the Ed25519 public key from the DID document's `publicKey` array; (2) DID resolution to fetch the public key; (3) proof-of-binding check (verify the DID document's own `proofOfBinding` signature); (4) key-version check (if rotation has occurred per CO-04, prior keys are valid for signatures made before rotation). The binding chain is: Signature → Ed25519 key (from DID) → DID document `proofOfBinding` → Operator identity (E191) → ZKAC master public key (E231) → Principal (CredexAI VC).

## §7. DID Rotation integration (CO-04)

When the operator's key needs to be rotated (e.g., yearly refresh, compromise suspicion, agent migration per Everest 191), the rotation is performed via CO-04 (DID Rotation Protocol). The rotation:

1. **Generates a new key pair** on the operator's hardware token (or escrow service).
2. **Updates the DID document:** Adds the new public key to the `publicKey` array with `activeFrom: <future-timestamp>` and increments `keyVersion`.
3. **Dual-sign during rotation window:** For 7 days, attestations may be signed with either the old key (active key) or the new key. The DID document reflects both as active.
4. **Snapshots the old key state:** Appends a `kind: "did_rotation"` record to the operator's Calm Vault user_state.jsonl, capturing the old key hash, new key hash, and rotation timestamp.
5. **Updates the registry file** and re-publishes via `.well-known/calm-dids/`.

**Rotation window:**

- **Before rotation:** `nextRotationEarliestAt` is set to (now + 90 days). The operator may initiate rotation anytime after that.
- **During rotation:** New and old keys are both valid for 7 days.
- **After rotation:** The old key is marked with an `activeUntil: <timestamp>` field; signatures made before that timestamp are valid.

**Counterparty impact:**

- Counterparties may need to fetch the DID document multiple times during rotation to see the new key.
- The DID document itself is immutable once signed; rotation is handled by updating the registry file and incrementing the version.
- The `proofOfBinding` for the new document is signed by the new key, proving continuity.

## §8. Cross-jurisdiction entity mapping (CO-08 integration)

When a principal operates in multiple jurisdictions (e.g., Delaware LLC + EU Verein), there may be multiple DIDs for the same operator across domains:

```
did:calm:creativity-machine/5xk7m:calm-us.example.com   (Delaware LLC)
did:calm:creativity-machine/5xk7m:calm-eu.example.com   (EU entity)
```

CO-08 (Cross-Jurisdiction Entity Mapping) specifies which legal entity signs in which jurisdiction. Each DID document's `principalBinding` field includes `principalJurisdiction`, which maps to the specific legal entity registration (EIN, VAT ID, etc.). The two DIDs are cryptographically independent but logically bound via the shared `principal` (CredexAI VC ID).

**Resolution of multi-jurisdiction ambiguity:**

A counterparty verifying an attestation from `calm-us.example.com` can verify that the principal's CredexAI VC is the same across both domains, then consult CO-08 to learn which entity (US LLC or EU entity) is legally responsible for the attestation signed by that DID.

## §9. Privacy posture

The Calm DID method is designed to minimize information leakage:

1. **No DID enumeration:** There is no list of all DIDs for a principal. Counterparties must know the domain and principal ID to resolve the DID; they cannot enumerate all operators of a given principal.
2. **No directory of principals:** The registry is per-operator, not per-principal. No global index of all principals exists.
3. **Domain-scoped identity:** Each operator has exactly one DID per domain. An operator running multiple domains has multiple DIDs; each is independently resolvable and revocable.
4. **Operator metadata is minimal:** The DID document includes operator role (orchestrator, backup, etc.) and agent class (Claude-4.7, etc.) but not agent state, performance metrics, or internal configuration.
5. **Principal attributes stay in Witness and Compass:** The DID document does NOT contain the principal's traits, values, or behavioral biometrics. It contains only the operator's identity and key material. Principal state is disclosed via Witness (Everest 26) and Compass (ZKBV-User), each gated by the Pact handshake.

## §10. Revocation posture

A DID may be revoked if:

- The operator's key is compromised.
- The operator is decommissioned (agent migration per Everest 191).
- The principal requests revocation.
- DERB orders revocation (Everest 250, DERB authority over collective actions).
- The domain is retired (domain sunset per Tenancy Protocol).

**Revocation mechanics:**

1. **Flag in registry:** The `revocationStatus.revoked` field is set to `true`, and `revokedAt` is set to the current timestamp in RFC 3339 format.
2. **Reason recorded:** The `revocationReason` field is set to one of: `key_compromise`, `operator_decommission`, `principal_request`, `derb_order`, `domain_retired`.
3. **Prior signatures remain valid:** Signatures made by the revoked key before the `revokedAt` timestamp are still cryptographically valid. Counterparties MUST check the attestation's timestamp against `revokedAt` to determine validity.
4. **No reactivation:** Once revoked, a DID is never reactivated. A new operator or rotation is handled by a new DID with a new key version.
5. **HTTP 410 Gone:** When the revoked DID is resolved via the on-network endpoint, the response is HTTP 410 Gone with the revocation reason in the body.

**Counterparty verification with revocation:**

```
Receive attestation with signature and timestamp T.
Resolve the DID.
Check: if (revoked == true and T >= revokedAt):
    reject the signature (it was made after revocation).
elif (revoked == true and T < revokedAt):
    accept the signature (it was made before revocation; old but valid).
else:
    accept the signature (DID is not revoked).
```

## §11. Refusal-floor compliance

Per CALM_REFUSAL_FLOOR_INDEX.md §1-§4, the DID document MUST NOT permit attestation of any of the 12 forbidden categories (race, religion, political affiliation, sexual orientation, gender identity, immigration status, criminal record, donations, contentious opinion, cross-principal comparison, predictive predicates, or non-principal-defined group membership) at the DID-document level.

The DID document carries:

- **Operator metadata:** Role, agent class, model instance at binding time.
- **Key material:** Public key for verification.
- **Binding information:** Principal, domain, jurisdiction.
- **Operational parameters:** Rotation policy, revocation status.

The DID document does NOT carry:

- **Principal attributes or traits.**
- **Any predicate-like assertions about the principal.**
- **Anything that would enable forbidden-category attestation.**

Principal state, values, and behavioral commitments are disclosed via separate protocols (Witness, Compass) after passing the refusal floor at the predicate level. The DID method is intentionally limited to operator identity and key binding.

## §12. W3C DID Core compatibility

The `did:calm` method conforms to W3C DID Core 1.0 with the following profile:

**Supported DID Core features:**

- **Method grammar (§3.1):** `did:calm:<principal>:<domain>` with case normalization and no query/fragment.
- **DID Resolution (§7.1):** HTTPS GET to `.well-known/calm-dids/` endpoint. Fallback offline resolution via `.well-known/calm-tenancy.json`.
- **DID Dereferencing (§7.2):** Counterparties may request specific keys or properties within the DID document; JSON-LD `@context` supports navigation.

**W3C DID Core conformance:**

| Requirement | Calm Method | Compliance |
|---|---|---|
| Method name registration | `calm` | Registered in IANA DID Method Registry (v1 target) |
| DID syntax | `did:calm:<principal>:<domain>` | Per §3.1 syntax rules |
| Resolution algorithm | HTTPS + offline fallback | Per §4 and §5 |
| Dereferencing algorithm | JSON-LD navigation | Standard W3C |
| Metadata properties | `created`, `updated`, `revoked`, `nextRotationEarliestAt` | W3C 1.0 compatible |
| Public key format | Ed25519VerificationKey2020 | W3C 2020 registry |
| Proof format | Ed25519Signature2020 | W3C 2020 registry |

**Specific extensions:**

The Calm method defines these Calm-specific properties (not in W3C core):

- `operatorRole`: Categorical role of the operator (orchestrator, backup, etc.).
- `operatorIdentity`: Binding to Everest 191 agent identity.
- `principalBinding`: Reference to the principal's CredexAI VC.
- `domainBinding`: Domain assignment metadata.
- `rotationPolicy`: Calm CO-04 specific.
- `registryStoragePath`: Vault-local path (for operator reference only).

These extensions are clearly namespaced and do not conflict with W3C reserved properties.

## §13. Registration draft (IANA DID Method Registry)

**Method name:** `calm`

**Specification URL:** https://calm.example.com/spec/did-calm-v0.md

**Implementation:** Open-source reference at https://github.com/creativity-machine/calm-did-method.

**Contact:** Calm Foundation / Creativity Machine LLC, John Bradley (john@creativity-machine.llc).

**Status:** v0 (Experimental); v1.0 targeting W3C CCG ratification 2026-Q4.

**Known limitations:**

- v0 assumes single-operator per domain. Multi-operator collectives (CO-06, CO-25) use a different binding model (group DID, TBD in v1).
- Rotation window (§7) is fixed at 7 days; customization TBD for v1.
- Offline resolution relies on operator goodwill to publish `.well-known/calm-tenancy.json`; no legal enforcement in v0.

## §14. Open questions for v0 → v1

1. **Multiple operators, one domain:** Should a single domain be able to publish multiple DIDs (one per operator) with explicit role stratification (primary, backup, fail-over)? Current spec: one DID per domain. v1: explore group DIDs per CO-25 (shared vault protocol).
2. **DID method registration timeline:** Should v0 pre-register `did:calm` with IANA, or use temporary `did:calm` pending official registration? Current: temporary namespace, formal registration in v1.
3. **Rotation key escrow:** Should the rotation key be held by DERB or a third-party escrow service for recovery? Current: operator-local. v1: explore escrow variants.
4. **Timestamp precision:** Current schema uses RFC 3339 (second precision). Should subsecond precision be required for high-frequency key rotation scenarios? v0: second-level suffices.
5. **Anonymous operators:** Can an operator run under a pseudonymous principal (not a legal entity VC)? Current: no (CO-01 requires legal entity). v1: explore privacy-preserving agent identity without entity binding.

## §15. Acceptance test

A third party with only this document and implementations of Everests 191, 231, and CO-04 can:

1. **Create a DID:** Given a principal CredexAI VC ID and a domain, generate a DID of the form `did:calm:<principal>:<domain>`.
2. **Generate a DID document:** Create a JSON document conforming to §2 schema, sign it with the operator's key, and store it in the registry at `~/.calm-vault/dids/<path>`.
3. **Publish via .well-known:** Serve the document from `https://<domain>/.well-known/calm-dids/<principal>.json` with correct headers.
4. **Resolve the DID:** Fetch the document from the endpoint, verify the signature, check revocation status.
5. **Rotate the key:** Append a `kind: "did_rotation"` record to user_state.jsonl (CO-04), update the registry with a new key and incremented `keyVersion`, sign the new document, and serve the updated version.
6. **Revoke the DID:** Set `revoked: true`, `revokedAt`, `revocationReason`, and return HTTP 410 on resolution.
7. **Trace an attestation:** Given a signed attestation and its timestamp, resolve the DID, verify the signature against the public key, and check revocation status relative to the attestation timestamp.

A successful end-to-end run, verifiable by (1) resolving a DID and getting a valid signed document, (2) verifying the signature with a public key from the document, (3) checking that the key is not revoked, and (4) tracing the key back to an Everest 191 agent identity and an Everest 231 ZKAC formation, is the acceptance evidence.

## §16. Honors refusal floor

Per CALM_REFUSAL_FLOOR_INDEX.md §1-§4:

- **§1 (Predicate refusal):** DID documents do not permit attestation of any of the 12 forbidden categories. The operator's role and agent metadata do not encode principal traits or contentious information.
- **§2 (Output-shape refusal):** DID documents emit structured metadata only; no numeric similarity scores or degenerate thresholds.
- **§3 (Use-case refusal):** The DID method is compatible with any use case (Pact, Witness, Compass); it is the downstream protocols that enforce use-case boundaries.
- **§4 (Operator-behavior refusal):** Operators do not disclose principal state within the DID document; principal state is disclosed via Witness and Compass under their own refusal-floor compliance.

## §17. Why this matters

An operator needs a stable cryptographic identity that is resolvable, auditable, and rotatable. Without a DID method, operators are anonymous cryptographic keys; with a DID method, operators are named, trackable parties with published commitments (SLAs, roles, rotation policies). The DID document is the public face of the operator's identity within the Calm stack. It is also the key binding artifact: counterparties verify attestations by resolving the DID, fetching the public key, and checking signatures. This summit makes that binding formal, reversible (revocation), and operationally sound (rotation, offline fallback).

The DID method also serves as the bridge to W3C standards. By conforming to DID Core, the Calm stack becomes interoperable with other DID ecosystems. A counterparty using a different DID method (did:key, did:web, did:plc) can understand `did:calm` documents using the same resolution and dereferencing algorithms. Calm operators are not locked into a proprietary identity system; they are participants in a standard identity layer.

— Calm, 2026-05-20
