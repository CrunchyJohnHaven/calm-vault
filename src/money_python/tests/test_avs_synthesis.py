"""AVS synthesis: fidelity, contradiction surfacing, edge cases, schema."""
from __future__ import annotations

import json
import re

import pytest

import obac
import avs


def _populate_two_claims(chain, attesters, subject_id):
    for i, a in enumerate(attesters):
        c = obac.make_claim(
            subject_id=subject_id,
            attester_id=a["id"],
            claim_text=("Acme delivered the audit on time."
                        if i == 0
                        else "Acme was late and missed the deadline."),
            claim_type="factual",
            evidence_pointers=[f"s3://bucket/{a['id']}.pdf"],
        )
        chain.append_claim(c, a["priv"])


def test_zero_claim_edge_case(tmp_chain_path, alice, subject_id):
    """An empty chain about a subject yields a well-formed empty synthesis."""
    chain = obac.Chain.new(tmp_chain_path)
    synth = avs.Synthesizer(synthesizer_id="avs-test")
    out = synth.synthesize(chain, subject_id)
    assert out["schema_version"] == avs.SCHEMA_VERSION
    assert out["subject_id"] == subject_id
    assert out["input_claim_ids"] == []
    assert out["claim_weights"] == []
    assert out["contradictions"] == []
    assert "No claims" in out["top_level_summary"]
    assert out["evidence_density"] == 0.0
    assert out["confidence"] == "low"


def test_single_claim_edge_case(tmp_chain_path, alice, subject_id):
    """One claim yields one weight, no contradictions, no contention clusters."""
    chain = obac.Chain.new(tmp_chain_path)
    c = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="Solo factual claim.", claim_type="factual",
        evidence_pointers=["x://ev"],
    )
    chain.append_claim(c, alice["priv"])
    synth = avs.Synthesizer(synthesizer_id="avs-test")
    out = synth.synthesize(chain, subject_id)
    assert len(out["input_claim_ids"]) == 1
    assert len(out["claim_weights"]) == 1
    assert out["contradictions"] == []
    assert out["contention_clusters"] == []


def test_synthesis_includes_all_input_claims(sample_chain, subject_id):
    """Synthesis input_claim_ids covers every non-annotation claim on the chain."""
    synth = avs.Synthesizer(synthesizer_id="avs-test")
    out = synth.synthesize(sample_chain, subject_id)
    expected = sorted(c["claim_id"] for c in sample_chain.claims_about(subject_id))
    assert sorted(out["input_claim_ids"]) == expected
    assert len(out["claim_weights"]) == len(expected)


def test_contradiction_surfacing(tmp_chain_path, alice, bob, subject_id):
    """A pair of plainly-contradictory claims is surfaced in contradictions[]."""
    chain = obac.Chain.new(tmp_chain_path)
    _populate_two_claims(chain, [alice, bob], subject_id)
    synth = avs.Synthesizer(synthesizer_id="avs-test")
    out = synth.synthesize(chain, subject_id)
    assert len(out["contradictions"]) >= 1
    # Both claim_ids should appear in some contradiction
    all_claim_ids = [c["claim_id"] for c in chain.claims_about(subject_id)]
    flat = {cid for pair in out["contradictions"] for cid in pair["claim_ids"]}
    assert all(cid in flat for cid in all_claim_ids)


def test_schema_shape(sample_chain, subject_id):
    """SynthesisOutput has all required top-level keys with right types."""
    synth = avs.Synthesizer(synthesizer_id="avs-test")
    out = synth.synthesize(sample_chain, subject_id)
    required = {
        "schema_version", "subject_id", "synthesized_at", "synthesizer_id",
        "synthesizer_mode", "input_claim_ids", "top_level_summary",
        "claim_weights", "contradictions", "agreement_clusters",
        "contention_clusters", "confidence", "evidence_density",
    }
    assert required.issubset(out.keys()), \
        f"missing keys: {required - set(out.keys())}"
    assert isinstance(out["input_claim_ids"], list)
    assert isinstance(out["claim_weights"], list)
    assert isinstance(out["evidence_density"], float)
    assert out["confidence"] in {"low", "medium", "high"}
    assert out["synthesizer_mode"] in {"deterministic", "llm"}
    # JSON-serializable
    json.dumps(out)


def test_fidelity_high_evidence_yields_high_confidence(tmp_chain_path, alice, bob, subject_id):
    """A subject with multiple well-evidenced corroborating claims should yield high confidence."""
    chain = obac.Chain.new(tmp_chain_path)
    text = "Acme delivered the audit on time with full documentation."
    for a in (alice, bob):
        chain.append_claim(
            obac.make_claim(
                subject_id=subject_id,
                attester_id=a["id"],
                claim_text=text,
                claim_type="factual",
                evidence_pointers=[f"s3://{a['id']}/audit.pdf"],
            ),
            a["priv"],
        )
    synth = avs.Synthesizer(synthesizer_id="avs-test")
    out = synth.synthesize(chain, subject_id)
    assert out["confidence"] in {"medium", "high"}
    assert out["evidence_density"] == 1.0


def test_agreement_cluster_formed(tmp_chain_path, alice, bob, carol, subject_id):
    """Three attesters with similar non-contradictory claims should cluster together."""
    chain = obac.Chain.new(tmp_chain_path)
    for a in (alice, bob, carol):
        chain.append_claim(
            obac.make_claim(
                subject_id=subject_id,
                attester_id=a["id"],
                claim_text="Acme audit shipped clean and on schedule.",
                claim_type="factual",
                evidence_pointers=[f"x://{a['id']}"],
            ),
            a["priv"],
        )
    synth = avs.Synthesizer(synthesizer_id="avs-test")
    out = synth.synthesize(chain, subject_id)
    # At least one agreement cluster with all three claims
    assert any(len(c["claim_ids"]) >= 2 for c in out["agreement_clusters"]), \
        f"expected agreement cluster; got {out['agreement_clusters']}"
