# Everest 135 | ZKAC Bridging Across CredexAI Versions

**Closes Everest 135 of [`ZKAC_NEXT_200_EVERESTS.md`](../ZKAC_NEXT_200_EVERESTS.md).**

**Draft v0 · 2026-05-20 · Calm**

**Prereq:** Everest 121 ([`ZKAC_TYPE_SYSTEM_v0.md`](../ZKAC_TYPE_SYSTEM_v0.md)).

**Acceptance test:** A vault operating under CredexAI v1 can issue ZKAC envelopes that counterparties on CredexAI v0 verify successfully within the published deprecation window. The inverse holds for v0 minters against v1 verifiers during the same window. Bridging rules are normative for wire layout, predicate identity, downgrade, refusal-floor inheritance, and falsifiability.

---

## §1 | Problem statement

CredexAI is the platform identity layer for Operators and Counterparties. When the platform bumps from `credexai/0.x` to `credexai/1.x`, vaults, Operators, and verifiers must not fracture the ZKAC graph. A Principal who migrates their vault to v1 must still collaborate with Counterparties that have not upgraded. A Counterparty on v0 must still verify envelopes from a v1 vault without accepting semantic drift, scope relaxation, or silent predicate redefinition.

This Everest specifies **CredexAI platform bridging only**. Per-primitive wire bumps (Pact, Witness, Compass) are covered in Everests 136 through 138 and in [`ZKAC_VERSION_BRIDGING_v0.md`](../ZKAC_VERSION_BRIDGING_v0.md). Everest 135 binds platform credential semantics, envelope operator signatures, and the cross-version verifier policy that sits above primitive wire labels.

---

## §2 | Normative definitions

| Term | Meaning |
| --- | --- |
| **CredexAI v0** | Platform release family `credexai/0.x` with VC issuance, operator attestation, and counterparty ID formats frozen at the v0 registry. |
| **CredexAI v1** | Successor platform release family `credexai/1.x`. May add optional envelope fields and dual-stack proof encodings; must not break v0 verification during the window. |
| **Deprecation window** | 180 calendar days after v1 general availability (GA). During the window, v1 verifiers accept v0 envelopes; v0 verifiers accept v1 envelopes that pass downgrade rules in §5. |
| **Platform migration record** | Principal chain record `kind: platform_migration` linking old `chain_head` to new `chain_head` after a controlled vault move. |
| **Wire version** | Top-level envelope field `wire_version` per ZKAC Type System §1 (`WireVersion`). Distinct from CredexAI platform version. |
| **Predicate ID** | Immutable string `namespace/category/predicate_name` (e.g. `cwp.v0.in_baseline_24h`). Platform bumps do not rename predicate IDs. |

---

## §3 | Wire version field

Every ZKAC `Envelope` MUST carry `wire_version` as the first sorted field in canonical JSON (ZKAC Type System §3). Implementations MUST reject envelopes with a missing or unknown `wire_version` unless `bridge_version_accepted` returns true for the verifier's supported set.

### §3.1 | Platform vs wire

CredexAI platform version and envelope `wire_version` are orthogonal:

- **Platform version** (`credexai/0.x` or `credexai/1.x`) governs VC schema, operator key attestation paths, and counterparty registry lookups.
- **Wire version** (`calm-stack/wire/v0`, `calm-stack/wire/v1`, or legacy `calm-witness/wire/v0`) governs JSON layout, proof tuple shape, and optional metadata slots.

A v1 vault MAY mint envelopes at `calm-stack/wire/v1` while the Counterparty verifier still advertises support for `calm-stack/wire/v0` only. Acceptance requires both platform bridging (§4) and wire bridging per [`version_bridge.py`](../../CredexAI/calm_witness/version_bridge.py).

### §3.2 | Verifier supported set

Each Operator MUST publish `supported_wire_versions` in `/.well-known/calm-operator.json` (see §8). The set is a frozenset of wire labels. Verification begins with:

```
bridge_version_accepted(envelope.wire_version, verifier_supported) == true
```

If false, the verifier returns `unsupported_wire_version` and MUST NOT parse disclosures.

### §3.3 | Minter default

During the deprecation window, v1 minters SHOULD default to `calm-stack/wire/v1` when all disclosures use v1-capable proof encodings. When any disclosure requires v0-only proof shape, the minter MUST emit `calm-stack/wire/v0` or a dual-encoded envelope per §5.2.

---

## §4 | CredexAI v0 / v1 interoperability

### §4.1 | Forward compatibility (v0 verifier, v1 minter)

For 180 days after v1 GA:

1. v1 vaults MAY issue envelopes signed with v1 operator credentials.
2. v0 counterparties MUST verify the operator signature using the v1 attestation document published in the CredexAI registry cross-linked to the v0 operator fingerprint.
3. v0 verifiers MUST accept envelopes whose `wire_version` passes `bridge_version_accepted` against `{calm-stack/wire/v0, calm-stack/wire/v1, calm-witness/wire/v0}`.
4. v0 verifiers MUST NOT accept envelopes that omit required v0 fields after downgrade (§5).

### §4.2 | Backward compatibility (v1 verifier, v0 minter)

For the same window:

1. v0 vaults MAY continue issuing envelopes at `calm-stack/wire/v0` or `calm-witness/wire/v0`.
2. v1 verifiers MUST accept those wire labels via `DEPRECATION_WINDOWS` in the reference implementation.
3. v1 verifiers MUST NOT require v1-only optional fields on v0 envelopes.

### §4.3 | Platform migration record

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

### §4.4 | Counterparty ID stability

`counterparty_id` strings issued under CredexAI v0 remain valid in v1. v1 MUST NOT reissue IDs that collide with v0 IDs for a different principal. Revocation lists are unioned across platform versions during the window.

---

## §5 | Envelope downgrade rules

Downgrade is the deterministic transform that strips v1-only fields so a v0 verifier parses a bit-equivalent envelope.

### §5.1 | Allowed transforms

| v1-only field | Downgrade action |
| --- | --- |
| `attestation_fingerprint` (optional metadata) | Omit if v0 verifier schema has no slot; replay detection on v0 uses `request_digest` + `session_nonce` only. |
| `platform_version` | Omit; v0 infers platform from operator attestation lookup. |
| `proof_encoding` = `ristretto_v1` | Re-encode to `ristretto_v0` if dual-stack proof present; else reject with `downgrade_proof_missing`. |
| Extra disclosures array entries | Reject with `downgrade_extra_disclosure`; no silent drop. |

### §5.2 | Dual-stack minting

v1 minters targeting v0 counterparties SHOULD mint **dual-stack** envelopes when proof encodings differ:

- Canonical body includes both `proof` (v0 shape) and `proof_v1` (v1 shape) for each `PredicateDisclosure`.
- `wire_version` is `calm-stack/wire/v1`.
- v0 verifiers downgrade per §5.1 and verify `proof` only.
- v1 verifiers prefer `proof_v1` when present.

If dual-stack is infeasible (circuit size limits), the minter MUST set `wire_version` to `calm-stack/wire/v0` even on a v1 vault.

### §5.3 | Forbidden downgrades

Implementations MUST NOT:

- Coerce a claimed bit from 1 to 0 or 0 to 1.
- Drop `operator_signature`, `chain_head`, `request_digest`, or `session_nonce`.
- Strip `disclosures[].predicate_id` or rename predicate IDs.
- Relax freshness: `issued_at_iso` and Sigsum anchors must survive downgrade unchanged.

### §5.4 | Failure codes

| Code | Meaning |
| --- | --- |
| `unsupported_wire_version` | `bridge_version_accepted` returned false. |
| `downgrade_proof_missing` | v1 proof encoding cannot map to v0. |
| `downgrade_extra_disclosure` | Disclosure count mismatch after strip. |
| `platform_migration_stale` | `chain_head` predates migration but envelope claims v1 operator without cross-link. |

---

## §6 | Predicate ID stability

Predicate IDs are **immutable** across CredexAI platform versions (ZKAC Type System §1, Everest 6, Everest 118). CredexAI v1:

1. MUST NOT rename `cwp.v0.*` or `cwp.compass.v0.*` identifiers.
2. MAY add new predicates only under new namespace versions (`cwp.v1.*`) with a separate registry ceremony.
3. MUST NOT change evaluator semantics for an existing ID without a new predicate ID and a protocol bump tracked in the audit log.

### §6.1 | Registry pinning

The public predicate registry JSON is content-addressed. v0 and v1 verifiers load the same registry hash for `cwp.v0.*` entries during the deprecation window. A v1-only registry extension MUST NOT alter hashes of v0 entries.

### §6.2 | Consent records

`ConsentRecord` objects in the vault reference `predicate_id` strings. Platform migration does not invalidate consent: the Operator re-evaluates consent against the same IDs post-migration.

### §6.3 | Composite envelopes

Composite envelopes (Everest 122) bind multiple predicate IDs. All IDs in a composite MUST belong to registries the counterparty's verifier loaded. Mixed v0/v1 predicate namespaces in one envelope are forbidden during the window unless every ID is listed in the counterparty's `supported_predicate_namespaces` well-known field.

---

## §7 | Refusal floor inheritance

Version bumps do not relax prohibited uses in [`CALM_WITNESS_SCOPE_STATEMENT.md`](../CALM_WITNESS_SCOPE_STATEMENT.md) or Compass scope statements. Everest 135 adds platform-level inheritance rules.

### §7.1 | Scope ratchet

§2 of the Witness scope statement is a one-way ratchet. CredexAI v1:

- MAY add prohibited uses (tightening).
- MUST NOT remove or weaken §2 entries.
- MUST NOT introduce a wire or platform flag that bypasses `principal_consents_to_disclose` or permanent-deny classes.

### §7.2 | Counterparty class preservation

Default-deny matrix entries for `governmental`, `medical`, `anonymous`, and employment-adjacent classes survive platform migration unchanged. v1 Operators MUST NOT map new counterparty classes to old IDs with looser defaults.

### §7.3 | Uniform refusal on downgrade

When downgrade would expose a refusal reason that v0 UI cannot render, the verifier returns the same uniform refusal code as v0 native (`refusal_floor`, `permanently_deny`, or `uniform_204` per suite policy). Downgrade MUST NOT leak protected-category text that v0 would have suppressed.

### §7.4 | License and trademark

Deployments that use CredexAI v1 to enable a §2 prohibited use forfeit Calm Witness naming rights per the scope statement §3.2. Platform version is visible in operator attestation; misuses are attributable to the v1 deployment fingerprint.

---

## §8 | Falsifiability

Claims about cross-version bridging must be testable by counterparties without trusting operator prose.

### §8.1 | Published supported sets

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

### §8.2 | Golden corpus

The repo maintains golden envelopes: v0-minter/v0-verifier, v1-minter/v0-verifier, v1-minter/v1-verifier, v0-minter/v1-verifier. Gate scripts and CI MUST verify all four tuples before marking Everest 135 BAGGED.

### §8.3 | Counterexample protocol

A counterparty that believes a v1 envelope misstates a predicate bit MAY file a counter-claim (Everest 112) requesting a redacted evidence sketch. Platform version MUST appear in the counter-claim metadata so auditors know which downgrade path applied.

### §8.4 | Transparency log anchor

Bridging claims bind to Sigsum anchors. A falsifying observation is: same `predicate_id`, same claimed bit, different `chain_head`, both accepted by the same verifier across platform versions without a `platform_migration` record between them.

---

## §9 | Reference implementation and gates

| Artifact | Path |
| --- | --- |
| Shared bridging rules (135 to 138) | [`ZKAC_VERSION_BRIDGING_v0.md`](../ZKAC_VERSION_BRIDGING_v0.md) |
| This Everest (135 only) | [`everest_135_credexai_version_bridging.md`](everest_135_credexai_version_bridging.md) |
| `bridge_version_accepted` | [`~/CredexAI/calm_witness/version_bridge.py`](../../CredexAI/calm_witness/version_bridge.py) |
| Everest 135 gate | [`~/CredexAI/scripts/everest_135_zkac_credexai_version_bridging_gate.py`](../../CredexAI/scripts/everest_135_zkac_credexai_version_bridging_gate.py) |
| Combined 135 to 138 gate | [`~/CredexAI/scripts/everest_135_138_zkac_version_bridging_gate.py`](../../CredexAI/scripts/everest_135_138_zkac_version_bridging_gate.py) |

---

## §10 | Acceptance checklist

1. v1 vault mints envelope; v0 counterparty verifies within 180-day window.
2. `wire_version` present and checked via `bridge_version_accepted`.
3. Predicate IDs unchanged across platform bump.
4. Downgrade rules produce bit-identical verification on v0 verifiers.
5. Witness scope §2 prohibitions unchanged; refusal floor inherited.
6. Falsifiability: well-known published sets and golden corpus pass.

---

Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
