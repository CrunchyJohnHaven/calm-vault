# Calm Witness

> *"All you need to know is that the human is themself, and is in their baseline — or if not, that you've been told."*

Calm Witness is the user-state companion to [Calm Pact](../CALM_PACT_PROTOCOL_v0.md). One agent attests, to another agent, one principal-authorised bit about the human operator behind it — without exposing the underlying biometric data, narrative, or diagnosis. The bank-teller-note primitive, cryptographically realised.

## What's in this directory

| File | What it does | Bagged-at |
|---|---|---|
| [`verify_chain.py`](verify_chain.py) | CLI verifier for `~/.calm-vault/user_state.jsonl` — hash, link, seq, schema | Everest 28 |
| [`schema.py`](schema.py) | v0 JSON-Schema for chain records; permissive `summit_bagged`; closed `KIND_REGISTRY` | Everest 26 |
| [`predicates.py`](predicates.py) | v0 predicate evaluators incl. `in_baseline_24h` (P-01); registry + dispatcher | Everest 55 |
| [`disclosure.py`](disclosure.py) | Request / response wire types, nonce binding (replay defence), disclosure logging | Everests 66, 67, 70, 72 |
| [`test_verify_chain.py`](test_verify_chain.py) | 15 tests: chain integrity + schema | E26, E28 |
| [`test_predicates_and_disclosure.py`](test_predicates_and_disclosure.py) | 16 tests: predicates + wire + replay + logging | E55, E66, E67, E70, E72 |

## Quick run

```bash
# Verify the local chain
python3 verify_chain.py
# → "Summary: N/N records verified"

# Verify with verbose per-record output
python3 verify_chain.py -v

# Skip schema (just hash + link + seq)
python3 verify_chain.py --no-schema

# Run all tests
python3 test_verify_chain.py
python3 test_predicates_and_disclosure.py
```

## End-to-end demo (programmatic)

```python
from disclosure import DisclosureRequest, respond, verify_response_binding
from predicates import P_IN_BASELINE_24H_ID

# Counterparty creates a request with a fresh nonce.
req = DisclosureRequest.new(
    predicate_id=P_IN_BASELINE_24H_ID,
    counterparty_id_hash="a" * 64,
    counterparty_class="peer-AI-collective",
)

# Operator evaluates over the chain and responds.
resp = respond(
    req,
    chain_window=[...],          # load from ~/.calm-vault/user_state.jsonl
    chain_head="...",            # latest record_hash
    operator_id_hash="b" * 64,
)

# Counterparty checks binding before trusting the bit.
errors = verify_response_binding(req, resp)
assert errors == []
print(resp.value)  # "true" / "false" / "unknown" / "refused"
```

## What's NOT here (yet)

| Capability | Lives at | Status |
|---|---|---|
| Real Pedersen commitments | Everest 44 | placeholder hex in `disclosure.py` |
| ZK range proof | Everest 45 | placeholder hex in `disclosure.py` |
| Operator Ed25519 signing | Everest 2 (chain) + Everest 22 (VC) | `operator_sign` callable hook present |
| Sigsum publication | Everest 30 | not yet integrated |
| FROST threshold signing | Everest 53 | future |
| Biometric capture | Everests 11–25 | design doc only |

## Licence

[Apache-2.0](../LICENSE). Patent non-aggression per Everest 4. No CLA.

## Composition

- Sibling primitive: [Calm Pact](../calm_pact/protocol.py) — directive equality.
- Identity issuer: [CredexAI](https://github.com/CrunchyJohnHaven/credexai) — verifiable credentials.
- Substrate: [`~/.calm-vault/USER_STATE_PROTOCOL.md`](../../../.calm-vault/USER_STATE_PROTOCOL.md) — hash-chained self-report log.

## Status

v0.0.1 — substrate + verifier + canonical predicate + wire layer. Pre-MVP. 31 tests green as of 2026-05-20.
