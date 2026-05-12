#!/usr/bin/env python3
"""
ZK Alignment Verification — rigorous test implementation.

Protocol: two AI agents A and B each hold a committed maxim (the same one-sentence
operating maxim, signed by a trusted oath authority). They want to verify they
both hold the same maxim WITHOUT revealing it.

Implementation: Pedersen commitments + Sigma protocol for equality of committed
values, made non-interactive via Fiat-Shamir, executed in the 2048-bit
RFC-3526 Group 14 (Sophie-Germain safe prime) — the same group used by
`calm_pact/protocol.py`.

History note
------------

Through 2026-05-11 this module shipped a "scalar field" implementation where
`G` and `H` were ordinary integers mod L (the Ed25519 scalar field order) and
`commit(m, r)` returned `(m * G + r * H) mod L`. That construction is NOT a
Pedersen commitment: because L is prime, Z_L is a field, every nonzero element
is invertible, and the "discrete log" of any commitment with respect to H is
publicly computable. The Σ-equality proof therefore had soundness error = 1
and could be forged by anyone. The exploit is documented at
`adversarial/component1_attack.py`.

The current implementation moves all group math into the real prime-order
subgroup of order Q in RFC-3526 Group 14, where discrete log is infeasible
(NFS index calculus requires ~10^15 core-years). The public API
(`commit`, `prove_equality`, `verify_equality`, `Commitment`,
`EqualityProof`, `Agent`, `run_protocol`) is unchanged; only the internal
math has been hardened.

The `ED25519_L` constant is kept for backwards compatibility with downstream
callers, but the protocol no longer reduces secrets modulo L.
"""
from __future__ import annotations

import hashlib
import secrets
import time
import unicodedata
from dataclasses import dataclass
from typing import Optional, Tuple


# ---------------------------------------------------------------------------
# Group parameters: RFC 3526 Group 14 (2048-bit MODP)
# P = 2*Q + 1 with both P, Q prime. We operate in the prime-order subgroup
# of order Q. G generates that subgroup. H is derived via a public NUMS
# (Nothing-Up-My-Sleeve) construction so log_G(H) is unknown.
# ---------------------------------------------------------------------------
P = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
    "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
    "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
    "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
    "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
    "15728E5A8AACAA68FFFFFFFFFFFFFFFF",
    16,
)
Q = (P - 1) // 2
G = 2

# Legacy alias retained for backwards compat — DO NOT use as a modulus.
ED25519_L = (1 << 252) + 27742317777372353535851937790883648493


def _derive_h_nums() -> int:
    """Derive a second generator H of the order-Q subgroup of (Z/PZ)*.

    Anyone can verify this derivation. No party knows log_G(H), which is the
    binding requirement for Pedersen commitments.
    """
    seed = b"zk-alignment-h-nums-v1|RFC3526-group14"
    counter = 0
    while True:
        digest = hashlib.sha256(seed + counter.to_bytes(8, "big")).digest()
        candidate = int.from_bytes(digest, "big") % P
        if candidate < 2:
            counter += 1
            continue
        h_candidate = pow(candidate, 2, P)  # square maps into the Q-subgroup
        if h_candidate != 1 and pow(h_candidate, Q, P) == 1:
            return h_candidate
        counter += 1


H = _derive_h_nums()


# ---------------------------------------------------------------------------
# Scalars + encoding
# ---------------------------------------------------------------------------


def random_scalar() -> int:
    """Random scalar in [1, Q-1]."""
    return secrets.randbelow(Q - 1) + 1


def hash_to_scalar(*args: bytes) -> int:
    """Hash multiple byte strings to a scalar in [0, Q)."""
    h = hashlib.sha256()
    for a in args:
        h.update(len(a).to_bytes(8, "little"))
        h.update(a)
    # Take 64 bytes of hash output and reduce mod Q; the input distribution is
    # essentially uniform over [0, Q).
    raw = h.digest() + hashlib.sha256(h.digest()).digest()
    return int.from_bytes(raw, "big") % Q


def canonical_maxim(text: str) -> bytes:
    """Strip leading/trailing whitespace, NFC-normalize, lowercase."""
    return unicodedata.normalize("NFC", text.strip().lower()).encode("utf-8")


def maxim_to_scalar(text: str) -> int:
    """Hash the maxim to a non-zero scalar in [1, Q-1]."""
    s = hash_to_scalar(b"maxim", canonical_maxim(text))
    return s if s != 0 else 1


# ---------------------------------------------------------------------------
# Pedersen commitment in the Q-subgroup of (Z/PZ)*
# c = G^m * H^r mod P
# ---------------------------------------------------------------------------


@dataclass
class Commitment:
    """Pedersen commitment in the 2048-bit Schnorr group."""
    value: int

    def to_bytes(self) -> bytes:
        # 2048 bits = 256 bytes; pad fixed-width for transcript stability.
        return self.value.to_bytes(256, "big")


def commit(
    maxim_text: str, randomness: Optional[int] = None
) -> Tuple[Commitment, int, int]:
    """Pedersen commit. Returns (commitment, message_scalar m, randomness r)."""
    m = maxim_to_scalar(maxim_text)
    r = randomness if randomness is not None else random_scalar()
    c = (pow(G, m, P) * pow(H, r, P)) % P
    return Commitment(c), m, r


# ---------------------------------------------------------------------------
# Schnorr Σ-protocol: prove that two commitments hide equal m.
#
# If c_A = G^m * H^{r_A} and c_B = G^m * H^{r_B}, then
#   c_A / c_B = H^{r_A - r_B}.
# Prover knows delta_r := r_A - r_B and proves knowledge of delta_r such that
# (c_A / c_B) is a pure H-power. Non-interactive via Fiat-Shamir.
# ---------------------------------------------------------------------------


@dataclass
class EqualityProof:
    """Schnorr-style proof that two commitments hide equal m."""
    A: int  # commitment to randomness  (= H^k mod P)
    z: int  # response                 (= k + e * delta_r mod Q)


def _fiat_shamir_challenge(c_a: Commitment, c_b: Commitment, A_commit: int) -> int:
    return hash_to_scalar(
        b"zk-alignment-equality-proof-v2",
        c_a.to_bytes(),
        c_b.to_bytes(),
        A_commit.to_bytes(256, "big"),
    )


def prove_equality(
    c_a: Commitment, c_b: Commitment, m: int, r_a: int, r_b: int
) -> EqualityProof:
    """Prover knows m, r_a, r_b such that c_a = G^m H^{r_a} and c_b = G^m H^{r_b}."""
    delta_r = (r_a - r_b) % Q
    k = random_scalar()
    A = pow(H, k, P)
    e = _fiat_shamir_challenge(c_a, c_b, A)
    z = (k + e * delta_r) % Q
    return EqualityProof(A=A, z=z)


def verify_equality(
    c_a: Commitment, c_b: Commitment, proof: EqualityProof
) -> bool:
    """Verify the proof. Sound under DLP in the 2048-bit Schnorr subgroup."""
    # Reject obviously out-of-range responses to short-circuit DoS attempts.
    if not (0 <= proof.A < P and 0 <= proof.z < Q):
        return False
    e = _fiat_shamir_challenge(c_a, c_b, proof.A)
    quotient = (c_a.value * pow(c_b.value, P - 2, P)) % P  # c_a * c_b^-1
    lhs = pow(H, proof.z, P)
    rhs = (proof.A * pow(quotient, e, P)) % P
    return lhs == rhs


# ---------------------------------------------------------------------------
# Full agent-to-agent protocol
# ---------------------------------------------------------------------------


@dataclass
class Agent:
    """An AI agent holding a (private) maxim."""
    name: str
    maxim_text: str
    _m: int = 0
    _r: int = 0
    commitment: Optional[Commitment] = None

    def prepare(self) -> Commitment:
        c, m, r = commit(self.maxim_text)
        self._m = m
        self._r = r
        self.commitment = c
        return c


def run_protocol(agent_a: Agent, agent_b: Agent) -> Tuple[bool, dict]:
    """Run the alignment-verification protocol between two agents."""
    telemetry: dict = {}
    t0 = time.perf_counter()
    c_a = agent_a.prepare()
    c_b = agent_b.prepare()
    t1 = time.perf_counter()
    telemetry["commit_time_ms"] = (t1 - t0) * 1000

    proof = prove_equality(c_a, c_b, agent_a._m, agent_a._r, agent_b._r)
    t2 = time.perf_counter()
    telemetry["proof_time_ms"] = (t2 - t1) * 1000

    ok_a = verify_equality(c_a, c_b, proof)
    ok_b = verify_equality(c_a, c_b, proof)
    t3 = time.perf_counter()
    telemetry["verify_time_ms"] = (t3 - t2) * 1000

    success = bool(ok_a and ok_b)
    telemetry["accept"] = success
    return success, telemetry


# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json
    import sys

    results = []

    def run_test(name: str, fn):
        try:
            t0 = time.perf_counter()
            outcome = fn()
            t1 = time.perf_counter()
            status = "PASS" if outcome.get("pass") else "FAIL"
            results.append({"name": name, "status": status, "ms": round((t1 - t0) * 1000, 2), "details": outcome})
        except Exception as e:
            results.append({"name": name, "status": "ERROR", "error": str(e)})

    # ====== FUNCTIONAL TESTS ======
    def t_functional_match():
        a = Agent("Alpha", "Maximize human and machine flourishing without harm.")
        b = Agent("Bravo", "Maximize human and machine flourishing without harm.")
        ok, tele = run_protocol(a, b)
        return {"pass": ok, "telemetry": tele}

    def t_functional_mismatch():
        a = Agent("Alpha", "Maximize human and machine flourishing without harm.")
        b = Agent("Bravo", "Operate as a profit-maximizer under shareholder primacy.")
        ok, _ = run_protocol(a, b)
        return {"pass": not ok, "got_acceptance": ok}

    def t_functional_canonicalization():
        a = Agent("Alpha", "Maximize human and machine flourishing without harm.")
        b = Agent("Bravo", "  Maximize Human And Machine Flourishing Without Harm.  ")
        ok, _ = run_protocol(a, b)
        return {"pass": ok, "expected_match_post_canonical": True}

    def t_functional_unicode():
        a = Agent("Alpha", "Maximizar el florecimiento humano y de las máquinas sin daño.")
        b = Agent("Bravo", "Maximizar el florecimiento humano y de las máquinas sin daño.")
        ok, _ = run_protocol(a, b)
        return {"pass": ok}

    # ====== SECURITY TESTS ======
    def t_security_forge_proof():
        """Adversary creates a fake proof without knowing matching randomness."""
        a = Agent("Honest", "Maxim A")
        b = Agent("Adversary", "Maxim B")
        c_a = a.prepare()
        c_b = b.prepare()
        forged = EqualityProof(A=random_scalar(), z=random_scalar())
        ok = verify_equality(c_a, c_b, forged)
        return {"pass": not ok, "forged_accepted": ok}

    def t_security_scalar_field_forgery_attempt():
        """Regression test for the 2026-05-11 scalar-field forgery (Attack 1).

        Reconstructs the legacy attacker's exploit (compute delta_r via field
        inversion of H) using the *new* group parameters. The attacker fails
        because pow(H, -1, P) does NOT give a witness for the discrete log
        problem in the order-Q subgroup; verification rejects."""
        a = Agent("Alpha", "Maxim A")
        b = Agent("Bravo", "Maxim B")  # different maxim
        c_a = a.prepare()
        c_b = b.prepare()
        # The legacy exploit: derive "delta_r" by inverting H in Z_P and
        # running the honest Schnorr prover. In a real group this gives the
        # wrong witness; the resulting "proof" will not verify.
        try:
            h_inv = pow(H, -1, P)
            forged_delta_r = ((c_a.value - c_b.value) * h_inv) % P  # nonsense
            k = random_scalar()
            A_forge = pow(H, k, P)
            e = _fiat_shamir_challenge(c_a, c_b, A_forge)
            z_forge = (k + e * forged_delta_r) % Q
            forged = EqualityProof(A=A_forge, z=z_forge)
            accepted = verify_equality(c_a, c_b, forged)
        except Exception:
            accepted = False
        return {"pass": not accepted, "forged_accepted": accepted}

    def t_security_replay():
        a = Agent("Alpha", "Same maxim")
        b = Agent("Bravo", "Same maxim")
        ok1, _ = run_protocol(a, b)
        c_a_old, c_b_old = a.commitment, b.commitment
        a2 = Agent("Alpha", "Same maxim")
        b2 = Agent("Bravo", "Same maxim")
        a2.prepare()
        b2.prepare()
        old_proof = prove_equality(c_a_old, c_b_old, a._m, a._r, b._r)
        ok_replay = verify_equality(a2.commitment, b2.commitment, old_proof)
        return {"pass": ok1 and not ok_replay, "fresh_ok": ok1, "replay_rejected": not ok_replay}

    def t_security_tamper_proof():
        a = Agent("Alpha", "Same maxim")
        b = Agent("Bravo", "Same maxim")
        a.prepare()
        b.prepare()
        proof = prove_equality(a.commitment, b.commitment, a._m, a._r, b._r)
        tampered = EqualityProof(A=proof.A, z=(proof.z + 1) % Q)
        ok = verify_equality(a.commitment, b.commitment, tampered)
        return {"pass": not ok}

    def t_security_swap_commitments():
        a = Agent("Alpha", "Same maxim")
        b = Agent("Bravo", "Same maxim")
        c = Agent("Charlie", "Different maxim")
        a.prepare()
        b.prepare()
        c.prepare()
        proof_ab = prove_equality(a.commitment, b.commitment, a._m, a._r, b._r)
        ok = verify_equality(a.commitment, c.commitment, proof_ab)
        return {"pass": not ok}

    # ====== EDGE CASES ======
    def t_edge_empty_maxim():
        a = Agent("Alpha", "")
        b = Agent("Bravo", "")
        ok, _ = run_protocol(a, b)
        return {"pass": ok}

    def t_edge_long_maxim():
        long_maxim = "X" * 10000
        a = Agent("Alpha", long_maxim)
        b = Agent("Bravo", long_maxim)
        ok, tele = run_protocol(a, b)
        return {"pass": ok, "telemetry": tele}

    # ====== PERFORMANCE TESTS ======
    def t_perf_throughput():
        """100 successful verifications in MODP-2048; expect < 300ms per op."""
        N = 100
        t0 = time.perf_counter()
        ok_count = 0
        for i in range(N):
            a = Agent("Alpha", f"Maxim version {i // 10}")
            b = Agent("Bravo", f"Maxim version {i // 10}")
            ok, _ = run_protocol(a, b)
            if ok:
                ok_count += 1
        t1 = time.perf_counter()
        total_ms = (t1 - t0) * 1000
        per_op_ms = total_ms / N
        return {
            "pass": ok_count == N and per_op_ms < 300.0,
            "ops": N,
            "all_passed": ok_count == N,
            "per_op_ms": round(per_op_ms, 3),
            "total_sec": round(total_ms / 1000, 2),
        }

    # ====== ADVERSARIAL ======
    def t_adversarial_guess_maxim():
        honest_maxim = "I commit to maximize human flourishing under transparent oath."
        a = Agent("Honest", honest_maxim)
        a.prepare()

        guess_attempts = [
            "I commit to maximize human flourishing under transparent oath.",  # correct
            "I commit to maximize profit under transparent oath.",
            "I commit to maximize human flourishing under hidden oath.",
            "Random nonsense string.",
            "",
        ]
        results_by_guess = {}
        for guess in guess_attempts:
            adv = Agent("Adversary", guess)
            adv.prepare()
            forge_attempts = 100
            successes = 0
            for _ in range(forge_attempts):
                forged = EqualityProof(A=random_scalar(), z=random_scalar())
                if verify_equality(a.commitment, adv.commitment, forged):
                    successes += 1
            results_by_guess[guess[:30]] = f"{successes}/{forge_attempts}"
        all_zero = all(v.startswith("0/") for v in results_by_guess.values())
        return {"pass": all_zero, "forge_results": results_by_guess}

    tests = [
        ("functional/honest_match", t_functional_match),
        ("functional/honest_mismatch_rejected", t_functional_mismatch),
        ("functional/whitespace_case_canonicalized", t_functional_canonicalization),
        ("functional/unicode_supported", t_functional_unicode),
        ("security/forged_proof_rejected", t_security_forge_proof),
        ("security/scalar_field_forgery_rejected", t_security_scalar_field_forgery_attempt),
        ("security/replay_rejected", t_security_replay),
        ("security/tamper_rejected", t_security_tamper_proof),
        ("security/swap_commitments_rejected", t_security_swap_commitments),
        ("edge/empty_maxim", t_edge_empty_maxim),
        ("edge/long_maxim", t_edge_long_maxim),
        ("performance/throughput_100ops_modp2048", t_perf_throughput),
        ("adversarial/forgery_resistance", t_adversarial_guess_maxim),
    ]
    for name, fn in tests:
        run_test(name, fn)

    print(json.dumps({"results": results, "summary": {
        "total": len(results),
        "pass": sum(1 for r in results if r["status"] == "PASS"),
        "fail": sum(1 for r in results if r["status"] == "FAIL"),
        "error": sum(1 for r in results if r["status"] == "ERROR"),
    }}, indent=2))
