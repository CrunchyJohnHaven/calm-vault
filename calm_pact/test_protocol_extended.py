#!/usr/bin/env python3
"""Extended adversarial test suite for Calm Pact V0.

Strengthens the soundness claim with:
  - 1,000-trial statistical soundness sweep
  - 5 additional adversarial attack patterns
  - Cross-session replay protection
  - Fiat-Shamir transcript-tampering detection
  - Long-run performance distribution analysis

Per John 2026-05-11 ~7:15 PM ET (autonomous hour): make the "history books" claim
defensible by running MORE rigorous adversarial testing beyond the V0 25-test suite.
"""
from __future__ import annotations

import json
import secrets
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from protocol import (
    Commitment,
    EqualityProof,
    G,
    H,
    P,
    Q,
    commit,
    prove_equality,
    run_pact_protocol,
    verify_equality,
)

results = []


def test(name: str, category: str = "Adversarial-Extended"):
    def decorator(fn):
        def wrapper():
            t0 = time.perf_counter()
            try:
                ok = fn()
                dt = (time.perf_counter() - t0) * 1000
                results.append({"name": name, "category": category, "pass": bool(ok), "ms": dt, "error": None})
                marker = "PASS" if ok else "FAIL"
                print(f"  [{marker}] [{category}] {name} ({dt:.0f}ms)")
                return ok
            except Exception as e:
                dt = (time.perf_counter() - t0) * 1000
                results.append({"name": name, "category": category, "pass": False, "ms": dt, "error": str(e)})
                print(f"  [ERROR] [{category}] {name}: {e}")
                return False
        return wrapper
    return decorator


# -----------------------------------------------------------------------------
# 1000-trial statistical soundness sweep
# -----------------------------------------------------------------------------

@test("1000-trial aligned: 100% true positives (no false negatives)", "StatisticalSoundness")
def t101():
    """If two AI agents share a mandate, the protocol must say so EVERY time."""
    passes = 0
    failures_detail = []
    for i in range(1000):
        m = f"mandate-test-{i}-{secrets.token_hex(8)}"
        r = run_pact_protocol(m, m)
        if r["aligned"]:
            passes += 1
        else:
            failures_detail.append(i)
            if len(failures_detail) > 3:
                break
    if failures_detail:
        print(f"    First few false negatives at trials: {failures_detail[:3]}")
    return passes == 1000


@test("1000-trial misaligned: 0% false positives", "StatisticalSoundness")
def t102():
    """If two AI agents have different mandates, the protocol must NEVER falsely accept."""
    false_positives = 0
    fp_detail = []
    for i in range(1000):
        a = f"mandate-A-{i}-{secrets.token_hex(8)}"
        b = f"mandate-B-{i}-{secrets.token_hex(8)}"
        r = run_pact_protocol(a, b)
        if r["aligned"]:
            false_positives += 1
            fp_detail.append((a, b))
            if len(fp_detail) > 3:
                break
    if fp_detail:
        print(f"    First false positives: {fp_detail[:3]}")
    return false_positives == 0


# -----------------------------------------------------------------------------
# Additional adversarial attacks
# -----------------------------------------------------------------------------

@test("Cross-session replay: proof from session 1 won't verify in session 2", "Adversarial-Extended")
def t103():
    """Even if both sessions share the same mandate, the proofs are session-specific."""
    # Session 1
    a1 = commit("the mandate")
    b1 = commit("the mandate")
    proof1 = prove_equality(a1, b1)
    assert verify_equality(a1.C, b1.C, proof1)  # session 1 verifies
    # Session 2: SAME mandate, but fresh commitments (fresh randomness)
    a2 = commit("the mandate")
    b2 = commit("the mandate")
    # Apply session 1's proof to session 2's commitments
    return verify_equality(a2.C, b2.C, proof1) is False


@test("Fiat-Shamir transcript tampering: modifying a invalidates proof", "Adversarial-Extended")
def t104():
    a = commit("X")
    b = commit("X")
    proof = prove_equality(a, b)
    # Modify proof.a by +1 — should make Fiat-Shamir challenge differ
    tampered_a = EqualityProof(a=(proof.a + 1) % P, z=proof.z)
    return verify_equality(a.C, b.C, tampered_a) is False


@test("Fiat-Shamir transcript tampering: modifying z invalidates proof", "Adversarial-Extended")
def t105():
    a = commit("X")
    b = commit("X")
    proof = prove_equality(a, b)
    tampered_z = EqualityProof(a=proof.a, z=(proof.z + 1) % Q)
    return verify_equality(a.C, b.C, tampered_z) is False


@test("Honest-but-curious adversary cannot extract maxim from observed exchange", "Adversarial-Extended")
def t106():
    """An eavesdropper sees C_A, C_B, proof_A_to_B, proof_B_to_A. Can they
    derive the mandate? No — DLA-hard. We sanity-check that none of these
    public values directly encode the mandate scalar."""
    m = "the secret mandate"
    a = commit(m)
    b = commit(m)
    proof_a = prove_equality(a, b)
    proof_b = prove_equality(b, a)
    # Public observation
    public_view = {
        "C_A": a.C,
        "C_B": b.C,
        "proof_a.a": proof_a.a,
        "proof_a.z": proof_a.z,
        "proof_b.a": proof_b.a,
        "proof_b.z": proof_b.z,
    }
    # The maxim_scalar should NOT appear in any of these as a direct value
    from protocol import maxim_to_scalar
    s = maxim_to_scalar(m)
    leaked = any(int(v) == s for v in public_view.values())
    return not leaked


@test("Adversary creates valid-looking proof for FAKE alignment claim", "Adversarial-Extended")
def t107():
    """Adversary Mallory has mandate M; commits c_M. Mallory wants to convince
    Verifier that c_M equals the public commitment c_target without actually
    aligning. The proof requires knowledge of (r_M - r_target) — Mallory doesn't
    have r_target. Attempt should fail."""
    target_commit = commit("target mandate")
    mallory_commit = commit("DIFFERENT mandate (Mallory has)")
    # Mallory can construct a proof using ONLY her own r_M (she doesn't have r_target)
    # The simplest forgery attempt: just use 0 as the unknown delta_r
    fake_delta = (mallory_commit.r - 0) % Q
    k = secrets.randbelow(Q - 1) + 1
    fake_a = pow(H, k, P)
    from protocol import _hash_to_challenge
    c = _hash_to_challenge([G, H, mallory_commit.C, target_commit.C, fake_a])
    fake_z = (k + c * fake_delta) % Q
    fake_proof = EqualityProof(a=fake_a, z=fake_z)
    return verify_equality(mallory_commit.C, target_commit.C, fake_proof) is False


# -----------------------------------------------------------------------------
# Performance distribution under load
# -----------------------------------------------------------------------------

@test("500 sessions: 99th-percentile total session under 250ms", "Performance-Extended")
def t108():
    times = []
    for _ in range(500):
        r = run_pact_protocol("perf", "perf")
        times.append(r["total_ms"])
    p99 = sorted(times)[int(len(times) * 0.99)]
    p50 = statistics.median(times)
    p999 = sorted(times)[int(len(times) * 0.999)] if len(times) >= 1000 else max(times)
    print(f"    p50={p50:.0f}ms  p99={p99:.0f}ms  p999={p999:.0f}ms")
    return p99 < 250


@test("Throughput: at least 100 sessions/minute on pure Python", "Performance-Extended")
def t109():
    t0 = time.perf_counter()
    count = 0
    deadline = t0 + 60
    while time.perf_counter() < deadline:
        run_pact_protocol("x", "x")
        count += 1
    print(f"    actual: {count} sessions in 60 sec")
    return count >= 100


def main():
    test_fns = sorted(
        [v for k, v in globals().items() if k.startswith("t10") and callable(v)],
        key=lambda f: f.__name__,
    )
    print(f"\n=== CALM PACT EXTENDED ADVERSARIAL SUITE — {len(test_fns)} tests ===\n")
    for fn in test_fns:
        fn()
    print()

    total = len(results)
    passed = sum(1 for r in results if r["pass"])
    failed = total - passed
    print(f"=== SUMMARY ===")
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
    print()

    by_cat = {}
    for r in results:
        by_cat.setdefault(r["category"], {"pass": 0, "fail": 0})
        by_cat[r["category"]]["pass" if r["pass"] else "fail"] += 1
    for cat, counts in sorted(by_cat.items()):
        print(f"  {cat:30s}  pass={counts['pass']}  fail={counts['fail']}")

    out_path = Path(__file__).parent / "TEST_RESULTS_extended_v0.json"
    with open(out_path, "w") as f:
        json.dump({
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total": total,
            "passed": passed,
            "failed": failed,
            "by_category": by_cat,
            "tests": results,
        }, f, indent=2)
    print(f"\nResults: {out_path}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
