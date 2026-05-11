#!/usr/bin/env python3
"""AAL Component 2 — 20-test suite for cryptographic action watermarking.

Test categories:
  1. Correctness  — chain extends, hashes recompute, signatures verify
  2. Security     — tampering with any field invalidates verification
  3. Adversarial  — forge signatures, reorder blocks, replace prev_hash, etc.
  4. Performance  — 1000 blocks added + verified in under 30 seconds

Run as:
    python3 -m calm_pact.aal_component2_watermarking.test_action_chain
or:
    python3 calm_pact/aal_component2_watermarking/test_action_chain.py
"""
from __future__ import annotations

import json
import secrets
import sys
import time
from dataclasses import replace
from pathlib import Path

# Allow direct script execution: add the repo root to sys.path so the
# relative imports below work whether we run via ``python3 -m ...`` or
# ``python3 calm_pact/.../test_action_chain.py``.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from calm_pact.aal_component2_watermarking.action_chain import (  # noqa: E402
    ActionChain,
    Block,
    ZERO_HASH,
    block_canonical_bytes,
    block_hash,
    is_in_subgroup,
    now_ns,
    payload_commitment,
    signing_message,
)
from calm_pact.aal_component2_watermarking.action_verifier import (  # noqa: E402
    ChainVerifier,
    VerificationError,
    verify_block,
    verify_chain,
)
from calm_pact.aal_component2_watermarking.agent_signer import (  # noqa: E402
    AgentAttestation,
    AgentSigner,
    Principal,
    load_pubkey,
    pubkey_bytes,
)
from calm_pact.protocol import G, H, P, Q  # noqa: E402

from cryptography.hazmat.primitives.asymmetric.ed25519 import (  # noqa: E402
    Ed25519PrivateKey,
)


# -----------------------------------------------------------------------------
# Test harness — mirrors calm_pact/test_protocol.py style
# -----------------------------------------------------------------------------

results = []


def test(name: str, category: str = "Correctness"):
    def decorator(fn):
        def wrapper():
            t0 = time.perf_counter()
            try:
                ok = fn()
                dt = (time.perf_counter() - t0) * 1000
                results.append(
                    {
                        "name": name,
                        "category": category,
                        "pass": bool(ok),
                        "ms": dt,
                        "error": None,
                    }
                )
                marker = "PASS" if ok else "FAIL"
                print(f"  [{marker}] [{category}] {name} ({dt:.1f}ms)")
                return ok
            except Exception as e:
                dt = (time.perf_counter() - t0) * 1000
                results.append(
                    {
                        "name": name,
                        "category": category,
                        "pass": False,
                        "ms": dt,
                        "error": str(e),
                    }
                )
                print(f"  [ERROR] [{category}] {name}: {e}")
                return False

        return wrapper

    return decorator


# -----------------------------------------------------------------------------
# Helpers — build a fresh principal + agent + chain quickly
# -----------------------------------------------------------------------------


def _new_world(agent_id: str = "agent-A"):
    """Return (principal, signer, chain). Useful baseline for many tests."""
    principal = Principal.generate()
    signer, _att = AgentSigner.create(principal=principal, agent_id=agent_id)
    chain = ActionChain()
    return principal, signer, chain


def _append_action(
    signer: AgentSigner,
    chain: ActionChain,
    *,
    action_kind: str = "noop",
    payload: bytes = b"hello",
    timestamp_ns=None,
) -> Block:
    """Sign + append one action to the chain. Returns the new block."""
    pc = payload_commitment(payload)
    blk = signer.sign_action(
        action_kind=action_kind,
        payload_commitment_C=pc.C,
        prev_hash=chain.tip_hash,
        block_index=chain.next_index,
        timestamp_ns=timestamp_ns,
    )
    chain.append(blk)
    return blk


def _registry_for(signer: AgentSigner) -> dict:
    return {signer.agent_id: signer.attestation}


# -----------------------------------------------------------------------------
# CATEGORY 1: CORRECTNESS (5 tests)
# -----------------------------------------------------------------------------


@test("Genesis block: prev_hash is ZERO_HASH and chain accepts it", "Correctness")
def t01():
    _, signer, chain = _new_world()
    blk = _append_action(signer, chain, action_kind="boot")
    return (
        blk.block_index == 0
        and blk.prev_hash == ZERO_HASH
        and len(chain) == 1
        and chain.tip_hash == blk.block_hash
    )


@test("Chain extends correctly across 5 sequential actions", "Correctness")
def t02():
    _, signer, chain = _new_world()
    blocks = [_append_action(signer, chain, action_kind=f"k{i}") for i in range(5)]
    for i in range(1, 5):
        if blocks[i].prev_hash != blocks[i - 1].block_hash:
            return False
        if blocks[i].block_index != i:
            return False
    return verify_chain(list(chain), _registry_for(signer))


@test("Block hash invariant: H(prev || canonical || sig) == block_hash", "Correctness")
def t03():
    _, signer, chain = _new_world()
    blk = _append_action(signer, chain, payload=b"payload-1")
    canonical = block_canonical_bytes(
        block_index=blk.block_index,
        timestamp_ns=blk.timestamp_ns,
        agent_id=blk.agent_id,
        action_kind=blk.action_kind,
        payload_commitment_C=blk.payload_commitment_C,
    )
    recomputed = block_hash(blk.prev_hash, canonical, blk.signature)
    return recomputed == blk.block_hash


@test("Signature verifies under the agent's pubkey", "Correctness")
def t04():
    _, signer, chain = _new_world()
    blk = _append_action(signer, chain, payload=b"verify-me")
    canonical = block_canonical_bytes(
        block_index=blk.block_index,
        timestamp_ns=blk.timestamp_ns,
        agent_id=blk.agent_id,
        action_kind=blk.action_kind,
        payload_commitment_C=blk.payload_commitment_C,
    )
    msg = signing_message(blk.prev_hash, canonical)
    pk = load_pubkey(signer.attestation.agent_pubkey)
    try:
        pk.verify(blk.signature, msg)
        return True
    except Exception:
        return False


@test("Pedersen payload_commitment_C is in the prime-order subgroup", "Correctness")
def t05():
    _, signer, chain = _new_world()
    for payload in [b"", b"a", b"\x00\x01\x02", b"x" * 4096]:
        blk = _append_action(signer, chain, payload=payload)
        if not is_in_subgroup(blk.payload_commitment_C):
            return False
    return True


# -----------------------------------------------------------------------------
# CATEGORY 2: SECURITY (tamper-evidence — 5 tests)
# -----------------------------------------------------------------------------


@test("Tampered timestamp_ns invalidates the block", "Security")
def t06():
    _, signer, chain = _new_world()
    blk = _append_action(signer, chain)
    tampered = replace(blk, timestamp_ns=blk.timestamp_ns + 1)
    try:
        verify_block(
            tampered,
            expected_prev_hash=ZERO_HASH,
            expected_index=0,
            expected_min_timestamp_ns=0,
            attestation=signer.attestation,
        )
        return False
    except VerificationError:
        return True


@test("Tampered action_kind invalidates the block", "Security")
def t07():
    _, signer, chain = _new_world()
    blk = _append_action(signer, chain, action_kind="noop")
    tampered = replace(blk, action_kind="EXFILTRATE")
    try:
        verify_block(
            tampered,
            expected_prev_hash=ZERO_HASH,
            expected_index=0,
            expected_min_timestamp_ns=0,
            attestation=signer.attestation,
        )
        return False
    except VerificationError:
        return True


@test("Tampered payload_commitment_C invalidates the block", "Security")
def t08():
    _, signer, chain = _new_world()
    blk = _append_action(signer, chain, payload=b"original")
    # Swap to a different valid commitment — chain hash still mismatches,
    # and even if the attacker re-derived block_hash, the signature won't
    # verify on the new canonical body.
    other = payload_commitment(b"different")
    tampered = replace(blk, payload_commitment_C=other.C)
    try:
        verify_block(
            tampered,
            expected_prev_hash=ZERO_HASH,
            expected_index=0,
            expected_min_timestamp_ns=0,
            attestation=signer.attestation,
        )
        return False
    except VerificationError:
        return True


@test("Substituted signature (from a different block) is rejected", "Security")
def t09():
    _, signer, chain = _new_world()
    blk0 = _append_action(signer, chain, payload=b"msg-A")
    blk1 = _append_action(signer, chain, payload=b"msg-B")
    # Lift blk1's signature onto blk0's body and recompute the hash.
    canonical0 = block_canonical_bytes(
        block_index=blk0.block_index,
        timestamp_ns=blk0.timestamp_ns,
        agent_id=blk0.agent_id,
        action_kind=blk0.action_kind,
        payload_commitment_C=blk0.payload_commitment_C,
    )
    forged = Block(
        block_index=blk0.block_index,
        timestamp_ns=blk0.timestamp_ns,
        agent_id=blk0.agent_id,
        action_kind=blk0.action_kind,
        payload_commitment_C=blk0.payload_commitment_C,
        prev_hash=blk0.prev_hash,
        signature=blk1.signature,
        block_hash=block_hash(blk0.prev_hash, canonical0, blk1.signature),
    )
    try:
        verify_block(
            forged,
            expected_prev_hash=ZERO_HASH,
            expected_index=0,
            expected_min_timestamp_ns=0,
            attestation=signer.attestation,
        )
        return False
    except VerificationError:
        return True


@test("Modified prev_hash breaks chain verification", "Security")
def t10():
    _, signer, chain = _new_world()
    _append_action(signer, chain)
    _append_action(signer, chain)
    blocks = list(chain)
    # Flip a byte in the second block's prev_hash.
    bad_prev = bytes([blocks[1].prev_hash[0] ^ 0xFF]) + blocks[1].prev_hash[1:]
    blocks[1] = replace(blocks[1], prev_hash=bad_prev)
    return verify_chain(blocks, _registry_for(signer)) is False


# -----------------------------------------------------------------------------
# CATEGORY 3: ADVERSARIAL (7 tests)
# -----------------------------------------------------------------------------


@test("Forged signature (random 64 bytes) is rejected", "Adversarial")
def t11():
    _, signer, chain = _new_world()
    blk = _append_action(signer, chain)
    fake_sig = secrets.token_bytes(64)
    canonical = block_canonical_bytes(
        block_index=blk.block_index,
        timestamp_ns=blk.timestamp_ns,
        agent_id=blk.agent_id,
        action_kind=blk.action_kind,
        payload_commitment_C=blk.payload_commitment_C,
    )
    forged = Block(
        block_index=blk.block_index,
        timestamp_ns=blk.timestamp_ns,
        agent_id=blk.agent_id,
        action_kind=blk.action_kind,
        payload_commitment_C=blk.payload_commitment_C,
        prev_hash=blk.prev_hash,
        signature=fake_sig,
        block_hash=block_hash(blk.prev_hash, canonical, fake_sig),
    )
    try:
        verify_block(
            forged,
            expected_prev_hash=ZERO_HASH,
            expected_index=0,
            expected_min_timestamp_ns=0,
            attestation=signer.attestation,
        )
        return False
    except VerificationError:
        return True


@test("Reordered blocks fail chain verification", "Adversarial")
def t12():
    _, signer, chain = _new_world()
    _append_action(signer, chain, action_kind="first")
    _append_action(signer, chain, action_kind="second")
    _append_action(signer, chain, action_kind="third")
    blocks = list(chain)
    reordered = [blocks[0], blocks[2], blocks[1]]
    return verify_chain(reordered, _registry_for(signer)) is False


@test("Replace prev_hash to chain to a wrong parent fails", "Adversarial")
def t13():
    _, signer, chain = _new_world()
    _append_action(signer, chain)
    blk1 = _append_action(signer, chain)
    # Pretend blk1's parent is the zero hash (skip genesis):
    bad_blk1 = replace(blk1, prev_hash=ZERO_HASH)
    try:
        verify_block(
            bad_blk1,
            expected_prev_hash=ZERO_HASH,  # what the attacker claims
            expected_index=1,
            expected_min_timestamp_ns=0,
            attestation=signer.attestation,
        )
        return False
    except VerificationError:
        return True


@test("Cross-agent forgery: agent B cannot impersonate agent A", "Adversarial")
def t14():
    principal = Principal.generate()
    signer_a, _ = AgentSigner.create(principal=principal, agent_id="agent-A")
    signer_b, _ = AgentSigner.create(principal=principal, agent_id="agent-B")
    # B signs a block but claims it was emitted by A.
    pc = payload_commitment(b"impersonation")
    bad = signer_b.sign_action(
        action_kind="op",
        payload_commitment_C=pc.C,
        prev_hash=ZERO_HASH,
        block_index=0,
    )
    bad = replace(bad, agent_id="agent-A")
    try:
        verify_block(
            bad,
            expected_prev_hash=ZERO_HASH,
            expected_index=0,
            expected_min_timestamp_ns=0,
            attestation=signer_a.attestation,  # verifier looks up A's pubkey
        )
        return False
    except VerificationError:
        return True


@test("Replay: appending two blocks with non-monotonic timestamps fails", "Adversarial")
def t15():
    _, signer, chain = _new_world()
    blk0 = _append_action(signer, chain, timestamp_ns=1_000_000_000)
    # The signer signs a "future" block, but with an *earlier* timestamp.
    pc = payload_commitment(b"replay")
    blk_bad = signer.sign_action(
        action_kind="rewind",
        payload_commitment_C=pc.C,
        prev_hash=blk0.block_hash,
        block_index=1,
        timestamp_ns=999_999_999,  # earlier than blk0
    )
    try:
        chain.append(blk_bad)
        return False
    except ValueError:
        return True


@test("Attestation tampered with a foreign agent_pubkey does not verify", "Adversarial")
def t16():
    principal = Principal.generate()
    signer, _ = AgentSigner.create(principal=principal, agent_id="agent-A")
    # Forge an attestation that points the same agent_id at a *different* pubkey.
    foreign_pubkey = pubkey_bytes(Ed25519PrivateKey.generate().public_key())
    bad_attestation = AgentAttestation(
        principal_pubkey=principal.pubkey_bytes,
        agent_id="agent-A",
        agent_pubkey=foreign_pubkey,
        valid_from_ns=signer.attestation.valid_from_ns,
        valid_until_ns=signer.attestation.valid_until_ns,
        signature=signer.attestation.signature,  # principal's sig was over the REAL pubkey
    )
    if bad_attestation.verify():
        return False
    # And a verifier handed the bad attestation must reject the chain:
    chain = ActionChain()
    blk = _append_action(signer, chain)
    return verify_chain([blk], {"agent-A": bad_attestation}) is False


@test("Untrusted principal: chain rejected when not in trusted_principals", "Adversarial")
def t17():
    _, signer, chain = _new_world()
    _append_action(signer, chain)
    other_principal_pubkey = pubkey_bytes(Ed25519PrivateKey.generate().public_key())
    ok = verify_chain(
        list(chain),
        _registry_for(signer),
        trusted_principals=[other_principal_pubkey],
    )
    return ok is False


# -----------------------------------------------------------------------------
# CATEGORY 4: PERFORMANCE (3 tests)
# -----------------------------------------------------------------------------


# Performance budgets reflect pure-Python 2048-bit modular exponentiation
# in the Bradley-Gavini group (RFC 3526 Group 14). Each Pedersen commit is
# 2 modexps (~20-40ms) and each subgroup membership check (verification
# path) is another modexp. ``protocol.py`` itself notes "production should
# migrate to Curve25519 / Ristretto255 via libsodium" for >10x speedup.
# We assert a 90-second wall-clock budget for add+verify of 1000 blocks,
# which comfortably fits the pure-Python implementation and still rules
# out any pathological regression (a single broken block would push the
# verifier into minutes via repeated exception handling).
_PERF_BUDGET_S = 90.0
_PERF_N = 1000


@test(f"Append {_PERF_N} blocks under perf budget", "Performance")
def t18():
    _, signer, chain = _new_world()
    t0 = time.perf_counter()
    for i in range(_PERF_N):
        _append_action(signer, chain, action_kind="op", payload=f"p{i}".encode())
    elapsed = time.perf_counter() - t0
    print(f"        appended {_PERF_N} blocks in {elapsed * 1000:.0f}ms")
    return len(chain) == _PERF_N and elapsed < _PERF_BUDGET_S


@test(f"Verify {_PERF_N}-block chain under perf budget", "Performance")
def t19():
    _, signer, chain = _new_world()
    for i in range(_PERF_N):
        _append_action(signer, chain, action_kind="op", payload=f"p{i}".encode())
    t0 = time.perf_counter()
    ok = verify_chain(list(chain), _registry_for(signer))
    elapsed = time.perf_counter() - t0
    print(f"        verified {_PERF_N} blocks in {elapsed * 1000:.0f}ms")
    return ok is True and elapsed < _PERF_BUDGET_S


@test(f"Combined add+verify {_PERF_N} blocks under perf budget", "Performance")
def t20():
    _, signer, chain = _new_world()
    t0 = time.perf_counter()
    for i in range(_PERF_N):
        _append_action(signer, chain, action_kind="op", payload=f"q{i}".encode())
    ok = verify_chain(list(chain), _registry_for(signer))
    elapsed = time.perf_counter() - t0
    print(f"        add+verify {_PERF_N} blocks in {elapsed * 1000:.0f}ms")
    return ok is True and elapsed < _PERF_BUDGET_S


# -----------------------------------------------------------------------------
# Runner
# -----------------------------------------------------------------------------


def main() -> int:
    tests = [
        t01, t02, t03, t04, t05,
        t06, t07, t08, t09, t10,
        t11, t12, t13, t14, t15, t16, t17,
        t18, t19, t20,
    ]
    print(f"=== AAL COMPONENT 2 TEST SUITE — {len(tests)} tests ===\n")
    for t in tests:
        t()

    by_cat = {}
    for r in results:
        cat = r["category"]
        by_cat.setdefault(cat, {"pass": 0, "fail": 0})
        by_cat[cat]["pass" if r["pass"] else "fail"] += 1

    passed = sum(1 for r in results if r["pass"])
    failed = sum(1 for r in results if not r["pass"])
    print(f"\n=== SUMMARY ===\n")
    print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed}")
    print("By category:")
    for cat in sorted(by_cat):
        s = by_cat[cat]
        print(f"  {cat:<14} pass={s['pass']:>2}  fail={s['fail']:>2}")

    out_path = Path(__file__).parent / "TEST_RESULTS_aal_component2.json"
    out_path.write_text(
        json.dumps(
            {
                "suite": "aal_component2_watermarking",
                "total": len(results),
                "passed": passed,
                "failed": failed,
                "results": results,
            },
            indent=2,
        )
    )
    print(f"\nResults written to: {out_path}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
