# ZKAC CredexAI Version Bridge v0

**Closes Everest 135 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Draft v0 · 2026-05-20 · Calm**

**Prereq:** Everest 121 ([`ZKAC_TYPE_SYSTEM_v0.md`](ZKAC_TYPE_SYSTEM_v0.md)).

**Acceptance test:** A vault operating under CredexAI v1 can issue ZKAC envelopes that counterparties on CredexAI v0 verify successfully within the published deprecation window. The inverse holds for v0 minters against v1 verifiers during the same window. Bridging rules are normative for version negotiation, wire layout, predicate identity, downgrade, refusal-floor inheritance, and falsifiability.

Per-primitive wire bumps (Pact, Witness, Compass) are covered in Everests 136 through 138 and in [`ZKAC_VERSION_BRIDGING_v0.md`](ZKAC_VERSION_BRIDGING_v0.md). This document is the **canonical CredexAI platform bridge**; the Everest alias lives at [`everests/everest_135_credexai_version_bridging.md`](everests/everest_135_credexai_version_bridging.md).

---

## §1 | Problem statement

CredexAI is the platform identity layer for Operators and Counterparties. When the platform bumps from `credexai/0.x` to `credexai/1.x`, vaults, Operators, and verifiers must not fracture the ZKAC graph. A Principal who migrates their vault to v1 must still collaborate with Counterparties that have not upgraded. A Counterparty on v0 must still verify envelopes from a v1 vault without accepting semantic drift, scope relaxation, or silent predicate redefinition.

Everest 135 binds platform credential semantics, envelope operator signatures, and the cross-version verifier policy that sits above primitive wire labels. The reference checker is `bridge_version_accepted` in [`~/CredexAI/calm_witness/version_bridge.py`](../../CredexAI/calm_witness/version_bridge.py).

---

## §2 | Normative definitions

| Term | Meaning |
| --- | --- |
| **CredexAI v0** | Platform release family `credexai/0.x` with VC issuance, operator attestation, and counterparty ID formats frozen at the v0 registry. |
| **CredexAI v1** | Successor platform release family `credexai/1.x`. May add optional envelope fields and dual-stack proof encodings; must not break v0 verification during the window. |
| **Deprecation window** | 180 calendar days after v1 general availability (GA). During the window, v1 verifiers accept v0 envelopes; v0 verifiers accept v1 envelopes that pass downgrade rules in §7. |
| **Platform migration record** | Principal chain record `kind: platform_migration` linking old `chain_head` to new `chain_head` after a controlled vault move. |
| **Wire version** | Top-level envelope field `wire_version` per ZKAC Type System §1 (`WireVersion`). Distinct from CredexAI platform version. |
| **Predicate ID** | Immutable string `namespace/category/predicate_name` (e.g. `cwp.v0.in_baseline_24h`). Platform bumps do not rename predicate IDs. |

---

## §3 | Version negotiation

ZKAC does **not** negotiate wire semantics at runtime the way HTTP content-types do. Version negotiation is **publish-then-verify**: each party advertises supported platform and wire labels; the minter picks an envelope label the verifier will accept; the verifier rejects anything outside its published set before parsing proofs.

### §3.1 | Disclosure request phase

When Counterparty C sends a `DisclosureRequest`, it SHOULD include optional negotiation hints:

```json
{
  "counterparty_id": "<CredexAI-issued>",
  "session_nonce": "<unique>",
  "requested_predicates": ["cwp.v0.in_baseline_24h"],
  "verifier_credexai_platform": "credexai/0.x",
  "verifier_supported_wire_versions": ["calm-stack/wire/v0", "calm-witness/wire/v0"],
  "verifier_supported_credexai_platforms": ["credexai/0.x"]
}
```

The Operator minting the response MUST read these hints (or fetch the same fields from `/.well-known/calm-operator.json` for C) before choosing `wire_version` and proof encoding. If the minter cannot produce a bit-equivalent envelope for any advertised wire label, it returns `negotiation_failed` and MUST NOT mint a misleading envelope at an unsupported label.

### §3.2 | Operator well-known as source of truth

Negotiation hints in a single request are advisory. The normative advertisement is the Operator document at `/.well-known/calm-operator.json` (§10). Counterparties cache that document with a freshness bound (recommended: 24 hours). Stale cache MUST NOT widen the supported set beyond what the Operator currently publishes.

### §3.3 | Minter selection algorithm

Given `verifier_supported_wire_versions` and `verifier_supported_credexai_platforms`:

1. If the minter's platform is `credexai/1.x` and the verifier lists only `credexai/0.x`, the minter MUST still be able to emit a downgrade-safe envelope (§7) or refuse.
2. Choose the highest wire label in the intersection of minter capability and verifier support, preferring `calm-stack/wire/v1` when dual-stack proofs are available.
3. If intersection is empty, call `bridge_version_accepted(envelope_wire, verifier_supported)` against the deprecation map; if still false, refuse with `unsupported_wire_version`.
4. Record the chosen `wire_version` and `credexai_platform` used in the envelope audit log (not in the ZK proof).

### §3.4 | No silent upgrade

Verifiers MUST NOT auto-upgrade a counterparty to v1 platform semantics because an envelope carries optional v1 fields. Upgrade requires an explicit `supported_credexai_platforms` entry and successful downgrade or native parse. This prevents a v0 counterparty from accidentally accepting scope-relaxing fields it never advertised.

### §3.5 | Negotiation and consent

Version negotiation does not bypass consent. Even when wire versions match, `principal_consents_to_disclose` gates each predicate. A platform bump MUST NOT remap consent records to broader counterparty classes.

---

## §4 | Wire version field

Every ZKAC `Envelope` MUST carry `wire_version` as the first sorted field in canonical JSON (ZKAC Type System §3). Implementations MUST reject envelopes with a missing or unknown `wire_version` unless `bridge_version_accepted` returns true for the verifier's supported set.

### §4.1 | Platform vs wire

CredexAI platform version and envelope `wire_version` are orthogonal:

- **Platform version** (`credexai/0.x` or `credexai/1.x`) governs VC schema, operator key attestation paths, and counterparty registry lookups.
- **Wire version** (`calm-stack/wire/v0`, `calm-stack/wire/v1`, or legacy `calm-witness/wire/v0`) governs JSON layout, proof tuple shape, and optional metadata slots.

A v1 vault MAY mint envelopes at `calm-stack/wire/v1` while the Counterparty verifier still advertises support for `calm-stack/wire/v0` only. Acceptance requires both platform bridging (§6) and wire bridging per the reference implementation.

### §4.2 | Verifier supported set

Each Operator MUST publish `supported_wire_versions` in `/.well-known/calm-operator.json` (see §10). The set is a frozenset of wire labels. Verification begins with:

```
bridge_version_accepted(envelope.wire_version, verifier_supported) == true
```

If false, the verifier returns `unsupported_wire_version` and MUST NOT parse disclosures.

### §4.3 | Minter default

During the deprecation window, v1 minters SHOULD default to `calm-stack/wire/v1` when all disclosures use v1-capable proof encodings. When any disclosure requires v0-only proof shape, the minter MUST emit `calm-stack/wire/v0` or a dual-encoded envelope per §7.2.

---

## §5 | Deprecation window

The deprecation window is **180 calendar days** beginning at CredexAI v1 GA (published in the operator well-known as `deprecation_window_end_iso` minus 180 days).

| Party | Obligation during window |
| --- | --- |
| v1 verifier | Accept v0-minter envelopes at `calm-stack/wire/v0`, `calm-witness/wire/v0`, and downgrade-safe v1 envelopes. |
| v0 verifier | Accept v1-minter envelopes that pass §7 downgrade; verify v1 operator signatures via cross-linked attestation. |
| v1 minter | MAY default to v1 wire; MUST provide downgrade path for v0 counterparties. |
| v0 minter | MAY remain on v0 wire only; no forced migration. |

After window end:

- v0 verifiers MAY reject `credexai/1.x` operator attestations not cross-linked in the registry.
- v1 verifiers MAY reject `calm-stack/wire/v0` unless explicitly listed for legacy partners.
- Predicate IDs in `cwp.v0.*` remain valid; only wire/platform labels sunset.

The reference implementation encodes wire succession in `DEPRECATION_WINDOWS`:

- `calm-stack/wire/v0` → `calm-stack/wire/v1` (180 days)
- `calm-witness/wire/v0` → `calm-stack/wire/v0` (180 days)

---

## §6 | CredexAI v0 / v1 interoperability

### §6.1 | Forward compatibility (v0 verifier, v1 minter)

For 180 days after v1 GA:

1. v1 vaults MAY issue envelopes signed with v1 operator credentials.
2. v0 counterparties MUST verify the operator signature using the v1 attestation document published in the CredexAI registry cross-linked to the v0 operator fingerprint.
3. v0 verifiers MUST accept envelopes whose `wire_version` passes `bridge_version_accepted` against `{calm-stack/wire/v0, calm-stack/wire/v1, calm-witness/wire/v0}`.
4. v0 verifiers MUST NOT accept envelopes that omit required v0 fields after downgrade (§7).

### §6.2 | Backward compatibility (v1 verifier, v0 minter)

For the same window:

1. v0 vaults MAY continue issuing envelopes at `calm-stack/wire/v0` or `calm-witness/wire/v0`.
2. v1 verifiers MUST accept those wire labels via `DEPRECATION_WINDOWS` in the reference implementation.
3. v1 verifiers MUST NOT require v1-only optional fields on v0 envelopes.

### §6.3 | Platform migration record

When a Principal moves a vault from CredexAI v0 to v1 (operator rotation, registry re-issuance, or hardware migration), the Operator MUST append:

```json
{
  "kind": "platform_migration",
  "from_platform": "credexai/0.x",
  "to_platform": "credexai/1.x",
  "from_chain_head": "<64-hex>",
  "to_chain_head": "<64-hex>",
  "migration_at_iso": "<ISO8601>",
  "principal_signature": "<64-hex sig over canonical record>"
}
```

Counterparties verifying post-migration envelopes MUST treat proofs bound to `from_chain_head` as stale unless `issued_at_iso` predates migration and freshness rules still hold. Proofs bound to `to_chain_head` are authoritative after migration.

### §6.4 | Counterparty ID stability

`counterparty_id` strings issued under CredexAI v0 remain valid in v1. v1 MUST NOT reissue IDs that collide with v0 IDs for a different principal. Revocation lists are unioned across platform versions during the window.

---

## §7 | Envelope downgrade rules

Downgrade is the deterministic transform that strips v1-only fields so a v0 verifier parses a bit-equivalent envelope.

### §7.1 | Allowed transforms

| v1-only field | Downgrade action |
| --- | --- |
| `attestation_fingerprint` (optional metadata) | Omit if v0 verifier schema has no slot; replay detection on v0 uses `request_digest` + `session_nonce` only. |
| `platform_version` | Omit; v0 infers platform from operator attestation lookup. |
| `proof_encoding` = `ristretto_v1` | Re-encode to `ristretto_v0` if dual-stack proof present; else reject with `downgrade_proof_missing`. |
| Extra disclosures array entries | Reject with `downgrade_extra_disclosure`; no silent drop. |

### §7.2 | Dual-stack minting

v1 minters targeting v0 counterparties SHOULD mint **dual-stack** envelopes when proof encodings differ:

- Canonical body includes both `proof` (v0 shape) and `proof_v1` (v1 shape) for each `PredicateDisclosure`.
- `wire_version` is `calm-stack/wire/v1`.
- v0 verifiers downgrade per §7.1 and verify `proof` only.
- v1 verifiers prefer `proof_v1` when present.

If dual-stack is infeasible (circuit size limits), the minter MUST set `wire_version` to `calm-stack/wire/v0` even on a v1 vault.

### §7.3 | Forbidden downgrades

Implementations MUST NOT:

- Coerce a claimed bit from 1 to 0 or 0 to 1.
- Drop `operator_signature`, `chain_head`, `request_digest`, or `session_nonce`.
- Strip `disclosures[].predicate_id` or rename predicate IDs.
- Relax freshness: `issued_at_iso` and Sigsum anchors must survive downgrade unchanged.

### §7.4 | Failure codes

| Code | Meaning |
| --- | --- |
| `unsupported_wire_version` | `bridge_version_accepted` returned false. |
| `downgrade_proof_missing` | v1 proof encoding cannot map to v0. |
| `downgrade_extra_disclosure` | Disclosure count mismatch after strip. |
| `platform_migration_stale` | `chain_head` predates migration but envelope claims v1 operator without cross-link. |
| `negotiation_failed` | No wire/platform label satisfies §3. |

---

## §8 | Predicate ID stability

Predicate IDs are **immutable** across CredexAI platform versions (ZKAC Type System §1, Everest 6, Everest 118). CredexAI v1:

1. MUST NOT rename `cwp.v0.*` or `cwp.compass.v0.*` identifiers.
2. MAY add new predicates only under new namespace versions (`cwp.v1.*`) with a separate registry ceremony.
3. MUST NOT change evaluator semantics for an existing ID without a new predicate ID and a protocol bump tracked in the audit log.

### §8.1 | Registry pinning

The public predicate registry JSON is content-addressed. v0 and v1 verifiers load the same registry hash for `cwp.v0.*` entries during the deprecation window. A v1-only registry extension MUST NOT alter hashes of v0 entries.

### §8.2 | Consent records

`ConsentRecord` objects in the vault reference `predicate_id` strings. Platform migration does not invalidate consent: the Operator re-evaluates consent against the same IDs post-migration.

### §8.3 | Composite envelopes

Composite envelopes (Everest 122) bind multiple predicate IDs. All IDs in a composite MUST belong to registries the counterparty's verifier loaded. Mixed v0/v1 predicate namespaces in one envelope are forbidden during the window unless every ID is listed in the counterparty's `supported_predicate_namespaces` well-known field.

---

## §9 | Refusal floor inheritance

Version bumps do not relax prohibited uses in [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) or Compass scope statements. Everest 135 adds platform-level inheritance rules.

### §9.1 | Scope ratchet

§2 of the Witness scope statement is a one-way ratchet. CredexAI v1:

- MAY add prohibited uses (tightening).
- MUST NOT remove or weaken §2 entries.
- MUST NOT introduce a wire or platform flag that bypasses `principal_consents_to_disclose` or permanent-deny classes.

### §9.2 | Counterparty class preservation

Default-deny matrix entries for `governmental`, `medical`, `anonymous`, and employment-adjacent classes survive platform migration unchanged. v1 Operators MUST NOT map new counterparty classes to old IDs with looser defaults.

### §9.3 | Uniform refusal on downgrade

When downgrade would expose a refusal reason that v0 UI cannot render, the verifier returns the same uniform refusal code as v0 native (`refusal_floor`, `permanently_deny`, or `uniform_204` per suite policy). Downgrade MUST NOT leak protected-category text that v0 would have suppressed.

### §9.4 | License and trademark

Deployments that use CredexAI v1 to enable a §2 prohibited use forfeit Calm Witness naming rights per the scope statement §3.2. Platform version is visible in operator attestation; misuses are attributable to the v1 deployment fingerprint.

---

## §10 | Falsifiability

Claims about cross-version bridging must be testable by counterparties without trusting operator prose.

### §10.1 | Published supported sets

Each Operator publishes:

```json
{
  "credexai_platform": "credexai/1.x",
  "supported_wire_versions": ["calm-stack/wire/v0", "calm-stack/wire/v1"],
  "supported_credexai_platforms": ["credexai/0.x", "credexai/1.x"],
  "deprecation_window_end_iso": "2026-11-20T00:00:00Z",
  "predicate_registry_sha256": "<64-hex>"
}
```

at `/.well-known/calm-operator.json`. Counterparties reject envelopes outside the advertised sets before parsing proofs.

### §10.2 | Golden corpus

The repo maintains golden envelopes: v0-minter/v0-verifier, v1-minter/v0-verifier, v1-minter/v1-verifier, v0-minter/v1-verifier. Gate scripts and CI MUST verify all four tuples before marking Everest 135 BAGGED.

### §10.3 | Counterexample protocol

A counterparty that believes a v1 envelope misstates a predicate bit MAY file a counter-claim (Everest 112) requesting a redacted evidence sketch. Platform version MUST appear in the counter-claim metadata so auditors know which downgrade path applied.

### §10.4 | Transparency log anchor

Bridging claims bind to Sigsum anchors. A falsifying observation is: same `predicate_id`, same claimed bit, different `chain_head`, both accepted by the same verifier across platform versions without a `platform_migration` record between them.

---

## §11 | Reference implementation and gates

| Artifact | Path |
| --- | --- |
| Canonical spec (this document) | [`ZKAC_CREDEXAI_VERSION_BRIDGE_v0.md`](ZKAC_CREDEXAI_VERSION_BRIDGE_v0.md) |
| Shared bridging rules (135 to 138) | [`ZKAC_VERSION_BRIDGING_v0.md`](ZKAC_VERSION_BRIDGING_v0.md) |
| Everest alias | [`everests/everest_135_credexai_version_bridging.md`](everests/everest_135_credexai_version_bridging.md) |
| `bridge_version_accepted` | [`~/CredexAI/calm_witness/version_bridge.py`](../../CredexAI/calm_witness/version_bridge.py) |
| Everest 135 gate | [`~/CredexAI/scripts/everest_135_zkac_credexai_version_bridge_gate.py`](../../CredexAI/scripts/everest_135_zkac_credexai_version_bridge_gate.py) |
| Combined 135 to 138 gate | [`~/CredexAI/scripts/everest_135_138_zkac_version_bridging_gate.py`](../../CredexAI/scripts/everest_135_138_zkac_version_bridging_gate.py) |

---

## §12 | Acceptance checklist

1. v1 vault mints envelope; v0 counterparty verifies within 180-day deprecation window.
2. Version negotiation uses published supported sets; no silent upgrade.
3. `wire_version` present and checked via `bridge_version_accepted`.
4. Predicate IDs unchanged across platform bump.
5. Envelope downgrade rules produce bit-identical verification on v0 verifiers.
6. Witness scope §2 prohibitions unchanged; refusal floor inherited.
7. Falsifiability: well-known published sets and golden corpus pass.

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
