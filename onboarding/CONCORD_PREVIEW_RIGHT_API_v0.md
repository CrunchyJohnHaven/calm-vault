# Calm Concord — Preview-Right API & UX Spec v0

**Draft v0 · 2026-05-20 · Calm**
**Companion spec to:** [CALM_CONCORD_PROTOCOL_v0.md](../CALM_CONCORD_PROTOCOL_v0.md) §5

---

## Why

The preview right exists to let a principal make an informed disclosure decision before anything crosses the wire. Without it, a principal faces a binary: either disclose predicates and invoke Concord, or decline and never know if the requirement would have cleared. That binary creates disclosure coercion — a counterparty can imply "disclose more or I won't proceed," and the principal has no way to evaluate the bluff without capitulating.

The preview breaks that coercion surface. A principal sketches their own candidate predicates and a hypothetical envelope for the counterparty, runs the simulation locally, and sees the structured outcome before any envelope is minted or any session is opened. The counterparty never learns the preview occurred. The operator runs nothing remotely. The result is a first-class AlignmentResult, structurally identical to what a live Concord invocation would return.

Secondary benefit: a principal can test multiple hypothetical disclosure sets in sequence, narrowing to the minimum disclosure that clears the requirement. This enforces data minimization without requiring the protocol to mandate it.

---

## Python API

```python
from calm_concord import (
    CompassEnvelope,
    AlignmentRequirement,
    AlignmentResult,
    preview_alignment,
)

result: AlignmentResult = preview_alignment(
    my_envelope: CompassEnvelope,
    hypothetical_their_bits: dict[str, bool | None],
    requirement: AlignmentRequirement,
) -> AlignmentResult
```

**Parameters**

- `my_envelope` — the principal's own locally-held CompassEnvelope. Must be a valid, self-signed envelope; the function will raise `EnvelopeValidationError` if it is not. The envelope is not transmitted.
- `hypothetical_their_bits` — a flat `dict` mapping predicate names to booleans or `None`. `None` means "I am sketching this as unknown / not disclosed." The dict need not be exhaustive; any predicate not present is treated as `None`. This argument substitutes for the counterparty's actual compass envelope. No signature verification is performed on it.
- `requirement` — an `AlignmentRequirement` object. The same `validate_requirement()` guards from §4 of the protocol are applied before simulation. A requirement that fails validation raises `RequirementValidationError` and no result is produced.

**Returns: AlignmentResult**

```python
@dataclass
class AlignmentResult:
    aligned: bool
    mode: str                        # one of: all_satisfied, any_satisfied, asymmetric, joint_threshold
    purpose: str                     # requirement's declared purpose, echoed back
    requirement_digest: str          # sha256 of the serialized requirement, for vault chaining
    my_role: str                     # "a" or "b" — which role this principal held
    cleared_count: int | None        # only set for joint_threshold mode; None otherwise
    threshold: int | None            # only set for joint_threshold mode; None otherwise
    sketch_warnings: list[str]       # non-fatal warnings when hypothetical_their_bits has gaps
    is_preview: bool                 # always True when returned by preview_alignment
    vault_chain_ref: str | None      # set after vault_record() is called; None before
```

**Behavior contract**

`preview_alignment` is a pure local function. It opens no sockets, writes no files, and makes no external calls. Calling it twice with the same arguments returns identical results. The function is safe to call from async context; it does not block I/O.

The `is_preview` flag is always `True` in results returned by this function. A live `compute_alignment` call sets it `False`. A downstream system that treats preview results as authoritative is a protocol violation; the `is_preview` flag is the machine-readable signal.

---

## CLI UX

**Basic invocation**

```
calm concord preview \
  --requirement ./requirements/q4_malaria_pilot.json \
  --their-bits ./sketches/counterparty_sketch.json
```

The CLI reads the principal's active vault envelope automatically from `~/.calm/vault/compass_envelope.json`. No `--my-envelope` flag is needed in the common case; it is available as an override for multi-identity setups.

**Interactive sketch mode**

```
calm concord preview --requirement ./req.json --interactive
```

Prompts the principal predicate-by-predicate through the ones named in the requirement. Accepts `y`, `n`, or Enter (unknown). Presents the result without any counterparty data.

**Output to terminal (default)**

```
Concord Preview Result
  Purpose   : co-funding the Q4 2026 malaria-vaccine logistics pilot
  Mode      : asymmetric
  My role   : a
  Would clear: YES
  Warnings  : their_bits missing predicate 'willing_to_be_corrected' — treated as unknown
  NOTE: This is a preview. Nothing was disclosed. No session was opened.
```

**Output as JSON**

```
calm concord preview --requirement ./req.json --their-bits ./sketch.json --format json
```

Returns the full serialized `AlignmentResult` to stdout.

**Future browser surface**

The preview right will surface in the Calm Dashboard as a card titled "Check Before You Disclose." The principal uploads or pastes the counterparty's public requirement file, fills in a sketch of counterparty predicates via a toggle-grid UI, and sees the structured result inline. The browser client calls the local vault agent via a localhost-only RPC; no data leaves the machine. The result panel shows the AlignmentResult fields and a plain-language sentence: "Based on your current predicates and this sketch, this requirement would [clear / not clear]." No counterparty-identifying data appears in the panel.

---

## Output Shape

The principal sees exactly `AlignmentResult` as defined above. They do not see:

- The counterparty's identity or any pseudonym
- The counterparty's disclosed bits beyond what was passed as `hypothetical_their_bits`
- Any intermediate scores, partial-match counts (except the `cleared_count` in `joint_threshold` mode, which is structural to that mode)
- Historical Concord results from other sessions involving the counterparty

The `sketch_warnings` field lists only gaps in the hypothetical input (missing predicates, conflicting entries). It does not speculate about the counterparty's actual values. Warning text is template-generated; it never embeds counterparty names or context.

---

## Audit Semantics

Preview attempts are NOT logged externally. They are not reported to the counterparty, to any operator registry, or to any audit panel. The only record is an optional append to the principal's own vault.

After calling `preview_alignment`, the principal may call `result.vault_record()` to append the result to their local vault chain. This creates an entry of the form:

```json
{
  "event": "concord_preview",
  "ts": "2026-05-20T...",
  "requirement_digest": "<sha256>",
  "aligned": true,
  "is_preview": true,
  "my_role": "a"
}
```

No predicate values are written into the vault entry — only the requirement digest and the boolean outcome. The vault entry is chained into the principal's Witness vault via the standard append-hash mechanic (Everest 64 binder). It is private to the principal and their authorized auditor only.

If the principal does not call `vault_record()`, no trace exists anywhere. The preview evaporates on process exit.

---

## Failure Modes

**F1 — Counterparty has not shared their compass-envelope-hash**

The counterparty's envelope hash is not publicly available. The principal must supply `hypothetical_their_bits` manually. The function runs on the sketch but emits a `sketch_warnings` entry: `"counterparty envelope hash unavailable — result is sketch-only, not bound to counterparty envelope."` The `aligned` field is still populated; its reliability depends entirely on the accuracy of the sketch. The principal is responsible for interpreting accordingly.

**F2 — Requirement validation fails**

`validate_requirement` returns one or more issues. `preview_alignment` raises `RequirementValidationError(issues)`. The principal must fix the requirement before proceeding. Common causes: blank purpose field, degenerate joint_threshold, unknown mode string.

**F3 — My envelope is expired or invalid**

`preview_alignment` raises `EnvelopeValidationError`. The principal must refresh their Compass envelope before running the preview.

**F4 — Predicate name not in Compass schema**

Any predicate in the requirement or in `hypothetical_their_bits` that is not in the current Compass predicate schema is rejected with `UnknownPredicateError`. The schema version is checked against the envelope's declared schema version.

**F5 — Sketch is empty**

If `hypothetical_their_bits` is an empty dict, the function succeeds but all counterparty predicates are treated as `None`. For modes that require both principals to satisfy predicates, this will typically produce `aligned = False`. The result will carry a `sketch_warnings` entry noting that the sketch contained no bits.

---

## Privacy Guarantees

1. **Counterparty learns nothing.** No network call is made during preview. The counterparty's operator cannot observe a preview attempt. The counterparty cannot discover a preview even by auditing their own logs, because nothing was written to their logs.

2. **Operator learns nothing.** The principal's own operator is not called during preview. The function is local-only.

3. **No envelope is minted.** A preview does not create a partial envelope, a draft session token, or any artifact that could leak through a side channel.

4. **Vault record is opt-in and private.** If the principal chooses to call `vault_record()`, the entry is in their own Witness vault behind their own key. Their authorized auditor can see it; no one else can.

5. **Preview results cannot be used as counterparty-facing evidence.** The `is_preview=True` flag is machine-readable. Any system that accepts a preview result as evidence of a live Concord check is violating the protocol. The Concord verifier rejects any presented result where `is_preview=True`.

6. **Multiple previews are unlinkable externally.** Because no external record is written, a principal can iterate over many sketch variants without creating a pattern visible to any external observer.

---

## Cross-References

- `CALM_CONCORD_PROTOCOL_v0.md` §5 — defines the preview right in the main protocol
- `CALM_CONCORD_PROTOCOL_v0.md` §4 — the anti-purity-test guards applied by `validate_requirement`
- `CALM_CONCORD_PROTOCOL_v0.md` §8 — reference implementation surface; `preview_alignment` is listed there
- `CALM_COMPASS_PROTOCOL_v0.md` — source of CompassEnvelope and predicate schema
- `ZKBB_USER_PROTOCOL_v0.md` — Witness vault append mechanic used by `vault_record()`
- `ALIGNMENT_EXPLAINER_v0.md` — non-technical explanation for principals new to Concord

---

*Calm Concord Preview-Right API & UX Spec v0 — 2026-05-20*

**— CALM**
John Bradley / Calm
calm_vault_market · Fifth Calm Stack Pillar
2026-05-20
