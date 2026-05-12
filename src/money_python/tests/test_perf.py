"""Performance: synthesis throughput targets.

100 claims  <  500ms
1000 claims < 5s

These are deterministic-mode targets. Slack added to absorb CI jitter.
"""
from __future__ import annotations

import time

import pytest

import obac
import avs


def _build_chain(tmp_chain_path, n_claims: int, n_attesters: int = 5):
    """Make a chain with `n_claims` claims spread across `n_attesters` keypairs."""
    chain = obac.Chain.new(tmp_chain_path)
    attesters = []
    for i in range(n_attesters):
        priv, _ = obac.gen_keypair()
        attesters.append({"id": f"att{i}", "priv": priv})
    subject = obac.make_subject_id("perf-subject")
    for i in range(n_claims):
        a = attesters[i % n_attesters]
        chain.append_claim(
            obac.make_claim(
                subject_id=subject,
                attester_id=a["id"],
                claim_text=f"Observation number {i} from {a['id']}.",
                claim_type="factual",
                evidence_pointers=[f"x://obs/{i}"] if i % 2 == 0 else [],
                submitted_at="2026-05-12T00:00:00+00:00",
                nonce=obac.random_nonce(),
            ),
            a["priv"],
        )
    return chain, subject


def test_perf_100_claims_under_500ms(tmp_chain_path):
    chain, subject = _build_chain(tmp_chain_path, n_claims=100)
    synth = avs.Synthesizer(synthesizer_id="avs-perf")
    t0 = time.perf_counter()
    out = synth.synthesize(chain, subject)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert len(out["input_claim_ids"]) == 100
    assert elapsed_ms < 500, f"100-claim synthesis took {elapsed_ms:.1f}ms (>500ms)"


def test_perf_1000_claims_under_5s(tmp_chain_path):
    chain, subject = _build_chain(tmp_chain_path, n_claims=1000)
    synth = avs.Synthesizer(synthesizer_id="avs-perf")
    t0 = time.perf_counter()
    out = synth.synthesize(chain, subject)
    elapsed_s = time.perf_counter() - t0
    assert len(out["input_claim_ids"]) == 1000
    assert elapsed_s < 5.0, f"1000-claim synthesis took {elapsed_s:.2f}s (>5s)"
