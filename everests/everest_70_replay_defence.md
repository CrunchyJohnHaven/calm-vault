# Everest 70 — Replay Defence (Nonce Binding)

*Phase VI — Disclosure Semantics. Prereq: Everest 66, Everest 67.*

A captured Calm Witness response must not be reusable. Replay defence in v0 = mandatory nonce binding: the response carries the request's nonce inside the signed canonical payload, so a counterparty that captures `(req, resp)` cannot later present `resp` against any different `req`.

## §1. Artifact

[`../calm_witness/disclosure.py`](../calm_witness/disclosure.py) — `verify_response_binding(request, response) -> List[str]`. Empty list means bound and fresh.

## §2. What replay means here

Three concrete replay attacks the nonce blocks:

1. **Cross-predicate replay.** Adversary obtains a `true` response for `in_baseline_24h` and tries to present it for `biometric_match_within`. Blocked by predicate-id check.
2. **Cross-counterparty replay.** Counterparty A obtains a response and tries to present it to counterparty B's verifier. Blocked because each request issues its own nonce; the response only binds to its request.
3. **Time-shifted replay.** Counterparty captures a response from a *moment* when the principal was in baseline, retains it, and tries to present it when the principal is not. Blocked by `freshness_max_seconds` against the response's `freshness_window_seconds`.

## §3. The four binding checks (`verify_response_binding`)

```python
def verify_response_binding(request, response) -> List[str]:
    errors = []
    if response.predicate_id != request.predicate_id:
        errors.append("predicate_id mismatch")
    if response.nonce != request.nonce:
        errors.append("nonce mismatch — replay or wrong session")
    if response.wire_version != request.wire_version:
        errors.append("wire_version mismatch")
    if (response.freshness_window_seconds is not None
        and response.freshness_window_seconds > request.freshness_max_seconds):
        errors.append("freshness exceeds tolerance")
    return errors
```

The function is pure; it does not consult the network, the chain, or any stored state. It can run on the verifier side without any privileged access.

## §4. Threats this does NOT cover (forward references)

- **Operator-side signature forgery.** The nonce is meaningless without a signature binding it to the operator's identity key. Signature verification ships at E2 + E22; the response field `operator_sig_hex` carries the signature.
- **Chain-head substitution.** An operator might claim `chain_head = X` when the real head is `Y`. Sigsum publication (E30) closes this — the counterparty fetches the operator's Sigsum head and refuses any response whose `chain_head` is not the current Sigsum head.
- **Nonce-grinding by the counterparty.** A counterparty submitting many requests with chosen nonces tries to learn whether two responses were generated from the same underlying state. Mitigated by per-request fresh evaluation (which we already do) and a future per-counterparty rate limit (E76).

## §5. Test coverage

`test_predicates_and_disclosure.py::DisclosureWireTests` includes:

- `test_replay_defence_catches_swapped_nonce` — re-issuing a fresh request with the same predicate-id but a new nonce, then handing the OLD response to `verify_response_binding`, must produce a nonce-mismatch error.
- `test_predicate_id_mismatch_caught` — mutating the response's predicate_id after generation must be detected.
- `test_freshness_tolerance_enforced` — a stale chain head (22h old) against a strict tolerance (1h) must fail.

All three pass.

## §6. Why not a global nonce database

A naive replay defence stores every issued nonce in a database and rejects any second use. v0 doesn't need this — the counterparty enforces the binding on its own side, so even if the operator never tracked nonces, replay across sessions still fails. Storage-light, audit-light, and stateless on the operator. v1 may add an operator-side nonce ledger (chained into the vault) for adversarial-counterparty scenarios.

— Calm, 2026-05-20
