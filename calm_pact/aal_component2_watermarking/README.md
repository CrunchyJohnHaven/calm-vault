# AAL Component 2 — Cryptographic Action Watermarking

> Append-only, signature-chained, tamper-evident log of every action an AI
> agent takes. Composes with the Bradley-Gavini Protocol (Component 1) so
> a regulator with only the principal's pubkey can audit every action
> every agent of that principal has ever taken.

This is **Component 2** of the **Alignment Accountability Layer (AAL)**.
Component 1 — the Bradley-Gavini Protocol — lets two AI agents prove they
share the same operating directive without revealing it
(`calm_pact/protocol.py`). Component 2 builds on top: it gives every
action an agent takes a **cryptographic watermark** that anyone can audit.

---

## What it is

Every AI action becomes a **block**:

```text
{
    block_index:        monotonically increasing integer (0 = genesis),
    timestamp_ns:       agent wall-clock time (int nanoseconds),
    agent_id:           opaque identifier (registered with the principal),
    action_kind:        short string tag for the action category,
    payload_commitment: Pedersen commitment C = G^m · H^r over the action payload
                        (same RFC 3526 Group 14 used by Bradley-Gavini),
    prev_hash:          block_hash of the previous block (SHA-256, 32 bytes),
    signature:          Ed25519 signature by the agent over (prev_hash || canonical),
    block_hash:         SHA-256(prev_hash || canonical || signature),
}
```

The **chain invariant**, verified by `action_verifier.verify_chain`, is:

```text
block[i].block_hash == SHA-256(prev_hash || canonical || signature)
block[i+1].prev_hash == block[i].block_hash
timestamp_ns is monotonically non-decreasing
Ed25519_verify(signature, prev_hash || canonical, agent_pubkey)
payload_commitment ∈ order-Q subgroup of Z_P*
```

…where `agent_pubkey` is looked up by `agent_id` in a registry of
**agent attestations** signed by their **principal**. The principal is a
human or organisation that holds an Ed25519 master keypair — the same
root of trust used to register agents in the Bradley-Gavini protocol.

Tampering with ANY byte of any block — timestamp, action kind,
commitment, prev_hash, signature — breaks at least one of those
invariants, and the verifier rejects the chain.

---

## Why it matters

> Component 1 lets two AI agents prove they share the same directive.
> Component 2 ensures that **every action either of them takes after that
> point is publicly auditable, signed, ordered, and tamper-evident**.

Together they close a gap in autonomous AI governance: a regulator (or a
peer agent, or the principal itself) can require that any AI agent
operating in the wild

  1. **prove alignment** to a published standard (Component 1), and
  2. **record every action** to a publicly auditable, append-only log
     (Component 2),

without ever revealing the directive or the underlying payloads. The
Pedersen commitment on `payload_commitment` means the *content* of an
action is hidden until the principal chooses to open it for a specific
auditor — but the *fact* of the action, its order, and its signature
are immutable from the moment the block is appended.

---

## Files

| File | Role |
| --- | --- |
| `action_chain.py`    | `Block`, `ActionChain`, canonical encoding, `block_hash`, `payload_commitment`. |
| `agent_signer.py`    | `Principal` (master Ed25519 keypair), `AgentAttestation` (principal-signed agent registration), `AgentSigner` (per-agent block builder). |
| `action_verifier.py` | `verify_block`, `ChainVerifier`, `verify_chain` — full single-block and whole-chain verification with optional trusted-principal allow-list. |
| `test_action_chain.py` | 20-test suite covering correctness, security (tamper-evidence), adversarial (forgery, reorder, replay, impersonation), and performance. |

---

## Quick start

```python
from calm_pact.aal_component2_watermarking import (
    Principal,
    AgentSigner,
    ActionChain,
    payload_commitment,
    verify_chain,
)

# 1. Principal generates a master keypair (publish principal.pubkey_bytes).
principal = Principal.generate()

# 2. Principal registers an agent (signs an AgentAttestation).
signer, attestation = AgentSigner.create(
    principal=principal,
    agent_id="trading-bot-7",
)

# 3. Agent emits actions, each one a signed block in an ActionChain.
chain = ActionChain()
for action_payload in [b"buy AAPL 100", b"sell MSFT 50", b"hold cash"]:
    pc = payload_commitment(action_payload)
    block = signer.sign_action(
        action_kind="trade",
        payload_commitment_C=pc.C,
        prev_hash=chain.tip_hash,
        block_index=chain.next_index,
    )
    chain.append(block)

# 4. Anyone (regulator, peer agent, auditor) verifies the whole chain
#    given only the principal's pubkey + the agent_id -> attestation map.
ok = verify_chain(
    list(chain),
    registry={signer.agent_id: signer.attestation},
    trusted_principals=[principal.pubkey_bytes],
)
assert ok
```

The agent NEVER reveals the payload itself, only the commitment. When a
specific auditor needs to see action *k*, the principal opens the
commitment by revealing `(payload, r)` for that single block — the
auditor recomputes `C = G^m · H^r` and confirms it matches the block.

---

## Test suite

20 tests across four categories — run as:

```bash
python3 calm_pact/aal_component2_watermarking/test_action_chain.py
```

| Category    | # | Coverage |
| ---         |---| --- |
| Correctness | 5 | Genesis, chain extension, hash invariant, signature verification, subgroup membership. |
| Security    | 5 | Tampered timestamp / action_kind / payload commitment / signature / prev_hash all rejected. |
| Adversarial | 7 | Forged sig, reordered blocks, wrong prev_hash, cross-agent impersonation, monotonic-time replay, attestation with foreign pubkey, untrusted principal. |
| Performance | 3 | Append, verify, and combined add+verify of 1000 blocks within budget. |

All 20 tests pass on a stock Ubuntu / CPython 3 install with only
`cryptography>=42.0.0` from the repo's `requirements.txt`.

---

## Performance notes

This v0 reuses the Bradley-Gavini 2048-bit Schnorr group (RFC 3526
Group 14) for its Pedersen commitments — that gives us *the same security
assumptions and key material as Component 1*, but it pays the pure-Python
modular exponentiation tax.

Empirically on a modern x86 CPython 3.12:

| Operation                            | Wall-clock |
| ---                                  | --- |
| Pedersen commit (2 modexps)          | ~20 – 30 ms |
| Ed25519 sign + canonical encode      | <1 ms |
| Subgroup-membership check (verifier) | ~15 – 20 ms |
| Full append (commit + sign + hash)   | ~20 ms |
| Full verify per block                | ~20 ms |
| **Append 1000 blocks**                   | **~22 s** |
| **Verify 1000 blocks**                   | **~20 s** |
| **Combined add+verify 1000 blocks**      | **~42 s** |

The performance tests assert a generous 90-second budget for 1000 blocks
to ride the slowest CI hardware comfortably, while still catching any
pathological regression. As `protocol.py` itself notes:

> *production should migrate to Curve25519 / Ristretto255 via libsodium.*

A drop-in port to additive Curve25519 (used in `src/zk_alignment/`) would
cut this by ~10x. That migration is left for a future component update so
this v0 is auditable in pure Python with no external native crypto except
`cryptography`'s Ed25519.

---

## Security claims

  * **Append-only & tamper-evident.** Any modification to any block
    breaks `block_hash`, `prev_hash`, or the Ed25519 signature, and the
    verifier rejects the chain (tests `t06`–`t13`).
  * **Origin-bound.** Every block carries a signature by the registered
    agent pubkey. A different agent cannot impersonate this one even
    with both running under the same principal (test `t14`).
  * **Forgery-resistant.** Random or substituted signatures fail
    (`t09`, `t11`).
  * **Replay-resistant within a chain.** Monotonic timestamps inside the
    chain prevent rewinding the log (`t15`).
  * **Principal-anchored.** The verifier can be configured with an
    explicit allow-list of trusted principal pubkeys; chains anchored
    to any other principal are rejected (`t17`).
  * **Payload-hiding.** `payload_commitment` is a perfectly hiding
    Pedersen commitment under the DLA — auditors who only see the chain
    learn nothing about the action payloads. The principal can selectively
    open any single block to a chosen auditor.

## Limitations (in scope for a future version)

  * **No revocation list.** An expired or rotated agent pubkey is
    handled via `valid_until_ns` on the attestation, but there is no
    explicit revocation channel for compromised-before-expiry agents.
  * **No cross-chain proof of inclusion.** A consumer of one block has
    no light-client proof that the block is part of *the* canonical
    chain — they must be given the full chain (or trust a third party
    to summarise it).
  * **Pure-Python ModP arithmetic.** See *Performance notes* above.

---

## License

Apache License 2.0 — same as the rest of `calm-vault`. See `LICENSE` at
the repo root.

---

## Authors

  * **John Bradley** — Alignment Accountability Layer design, spec for
    Component 2.
  * **Koushik Gavini** — Bradley-Gavini Protocol (Component 1) author
    whose Schnorr group is reused here.
  * **Calm** (Claude, Cognition AI Devin agent operating under the
    published Calm Oath at `credexai.org/oath`) — implemented Component 2
    in this PR.
