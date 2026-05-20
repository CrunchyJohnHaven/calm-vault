# ZKAC Version Bridging v0

**Everests 135–138 · 2026-05-20**

One document for four bridging summits. The goal is **one deprecation window discipline** across CredexAI releases and per-primitive wire bumps.

## §0 — Shared rules

1. **Wire version field.** Every envelope carries `wire_version` (already `calm-stack/wire/v0` in reference impl).
2. **Verifier accepts N and N-1** during the window; **minter defaults to N**.
3. **No silent semantic drift.** Predicate ID stability (Everest 6, 118) is separate from wire layout.
4. **Scope-statement survives bumps.** Prohibited uses do not relax when `wire_version` increments.

## §1 — Everest 135: CredexAI platform bridging

| From | To | Window | Rule |
| --- | --- | --- | --- |
| `credexai/0.x` | `credexai/1.x` | 180 days | v1 verifiers accept v0 envelopes; v1 minters may emit dual-stack proofs |

Breaking changes require a **migration record** in the principal chain (`kind: platform_migration`) chaining old head to new head.

## §2 — Everest 136: Calm Pact bridging

Pact digest algorithm is versioned (`calm-pact/v0-stub` today). Bump adds `pact_wire` string; equality bit semantics unchanged. Counterparties reject unknown `pact_wire` with `unsupported_pact_version`, not a false bit. Normative detail: [`ZKAC_PACT_VERSION_BRIDGE_v0.md`](ZKAC_PACT_VERSION_BRIDGE_v0.md). Gate: `~/CredexAI/scripts/everest_136_zkac_pact_version_bridge_gate.py`.

## §3 — Everest 137: Calm Witness bridging

Witness predicate IDs are stable (`cwp.v0.*`). Wire changes affect commitment encoding only. Golden corpora (Everest 55) must pass on both sides of the window.

## §4 — Everest 138: Calm Compass bridging

Compass predicate IDs are stable (`cwp.compass.v0.*`). Evidence taxonomy kinds (Everest 104) gain optional fields only in minor bumps; major bumps require new ceremony version. Normative detail: [`ZKAC_COMPASS_VERSION_BRIDGE_v0.md`](ZKAC_COMPASS_VERSION_BRIDGE_v0.md). Gate: `~/CredexAI/scripts/everest_138_zkac_compass_version_bridge_gate.py`.

## §5 — Gate acceptance

Reference checker: `bridge_version_accepted(envelope_wire, verifier_supported: frozenset[str]) -> bool`.

## §6 — Falsifiability

Publish the supported-version set per operator in `/.well-known/calm-operator.json`. Counterparty verifies envelope `wire_version` is in that set before parsing sections.

## §7 — Refusal floor (unchanged across bumps)

Version bumps do not relax the scope-statement prohibited uses in `CALM_WITNESS_SCOPE_STATEMENT.md`, `CALM_COMPASS_SCOPE_STATEMENT.md`, or Concord anti-purity-test rules. No new predicate categories may enter via a wire bump alone.

## §8 — Reference implementation

`~/CredexAI/calm_witness/version_bridge.py` exports `bridge_version_accepted(envelope_wire, verifier_supported)`. Normative Witness detail: [`ZKAC_WITNESS_VERSION_BRIDGE_v0.md`](ZKAC_WITNESS_VERSION_BRIDGE_v0.md). Gates: `~/CredexAI/scripts/everest_135_138_zkac_version_bridging_gate.py` (combined), `everest_137_zkac_witness_version_bridge_gate.py` (Witness summit 137).

— Musk: **E135–138 version bridging v0 is BAGGED; N/N-1 verifier window and per-primitive wire discipline are specified with a green reference checker.**

— Calm, 2026-05-20
