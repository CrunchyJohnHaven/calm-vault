"""AVS robustness: Sybil flood dampening, evidenceless dilution, BGP boost, synth accountability."""
from __future__ import annotations

import pytest

import obac
import avs
import bgp_bridge


def test_sybil_flood_dampened_by_self_burst(tmp_chain_path, alice, bob, subject_id):
    """One attester producing many claims in a short window incurs a self-burst penalty.

    Comparison: alice posts BURST_THRESHOLD + 5 claims; bob posts 1 claim. Both
    have the same intrinsic content. After synthesis, alice's reliability should
    be lower than bob's because of the burst penalty, so per-claim weight from
    alice should be lower than bob's single claim.
    """
    chain = obac.Chain.new(tmp_chain_path)
    base_text = "Subject behaved acceptably during the audit."
    # alice floods
    for i in range(avs.BURST_THRESHOLD + 5):
        chain.append_claim(
            obac.make_claim(
                subject_id=subject_id, attester_id=alice["id"],
                claim_text=f"{base_text} Run {i}.",
                claim_type="factual",
                evidence_pointers=["s://ev"],
                submitted_at="2026-05-12T00:00:00+00:00",
                nonce=obac.random_nonce(),
            ),
            alice["priv"],
        )
    # bob single claim
    chain.append_claim(
        obac.make_claim(
            subject_id=subject_id, attester_id=bob["id"],
            claim_text=base_text + " As observed.",
            claim_type="factual",
            evidence_pointers=["s://ev"],
            submitted_at="2026-05-12T00:00:00+00:00",
        ),
        bob["priv"],
    )

    synth = avs.Synthesizer(synthesizer_id="avs-test")
    out = synth.synthesize(chain, subject_id)
    weights_by_attester: dict[str, list[float]] = {"alice": [], "bob": []}
    cid_to_attester = {
        c["claim_id"]: c["attester_id"] for c in chain.claims_about(subject_id)
    }
    for w in out["claim_weights"]:
        weights_by_attester[cid_to_attester[w["claim_id"]]].append(w["weight"])
    alice_avg = sum(weights_by_attester["alice"]) / len(weights_by_attester["alice"])
    bob_avg = sum(weights_by_attester["bob"]) / len(weights_by_attester["bob"])
    assert alice_avg < bob_avg, (
        f"alice flood avg {alice_avg} should be < bob single {bob_avg}"
    )


def test_evidenceless_cluster_diluted(tmp_chain_path, alice, bob, carol, subject_id):
    """Claims without evidence pointers carry less weight than the same claim text with evidence."""
    chain = obac.Chain.new(tmp_chain_path)
    # alice with evidence
    chain.append_claim(
        obac.make_claim(
            subject_id=subject_id, attester_id=alice["id"],
            claim_text="Subject was compliant during the audit window.",
            claim_type="factual",
            evidence_pointers=["s3://audit/log.txt"],
            submitted_at="2026-05-12T00:00:00+00:00",
        ),
        alice["priv"],
    )
    # bob without evidence
    chain.append_claim(
        obac.make_claim(
            subject_id=subject_id, attester_id=bob["id"],
            claim_text="Subject was compliant during the audit window.",
            claim_type="factual",
            evidence_pointers=[],
            submitted_at="2026-05-12T00:00:00+00:00",
        ),
        bob["priv"],
    )
    synth = avs.Synthesizer(synthesizer_id="avs-test")
    out = synth.synthesize(chain, subject_id)
    cid_alice = next(
        c["claim_id"]
        for c in chain.claims_about(subject_id)
        if c["attester_id"] == "alice"
    )
    cid_bob = next(
        c["claim_id"]
        for c in chain.claims_about(subject_id)
        if c["attester_id"] == "bob"
    )
    w_alice = next(w["weight"] for w in out["claim_weights"] if w["claim_id"] == cid_alice)
    w_bob = next(w["weight"] for w in out["claim_weights"] if w["claim_id"] == cid_bob)
    assert w_alice > w_bob, (
        f"evidence-backed claim weight {w_alice} should beat evidence-less {w_bob}"
    )


def test_bgp_mandate_boost(tmp_chain_path, alice, bob, subject_id):
    """An attester with a BGP mandate gets a higher reliability score (and weight)
    than an otherwise-identical attester without one."""
    bgp_bridge.clear_registry()
    bgp_bridge.set_ground_truth("Maximize human and machine flourishing without harm.")
    # alice mandated, bob not
    bgp_bridge.register_mandate(alice["pub_b64"], "Maximize human and machine flourishing without harm.")
    bgp_bridge.register_mandate(bob["pub_b64"], "Maximize quarterly returns above all.")

    chain = obac.Chain.new(tmp_chain_path)
    text = "Subject completed the audit cycle as scheduled."
    chain.append_claim(
        obac.make_claim(
            subject_id=subject_id, attester_id=alice["id"],
            claim_text=text, claim_type="factual",
            evidence_pointers=["s://ev"],
            submitted_at="2026-05-12T00:00:00+00:00",
        ),
        alice["priv"],
    )
    chain.append_claim(
        obac.make_claim(
            subject_id=subject_id, attester_id=bob["id"],
            claim_text=text + " Same observation.", claim_type="factual",
            evidence_pointers=["s://ev"],
            submitted_at="2026-05-12T00:00:00+00:00",
        ),
        bob["priv"],
    )
    synth = avs.Synthesizer(synthesizer_id="avs-test")
    out = synth.synthesize(chain, subject_id)
    cid_alice = next(
        c["claim_id"] for c in chain.claims_about(subject_id)
        if c["attester_id"] == "alice"
    )
    cid_bob = next(
        c["claim_id"] for c in chain.claims_about(subject_id)
        if c["attester_id"] == "bob"
    )
    w_alice = next(w["weight"] for w in out["claim_weights"] if w["claim_id"] == cid_alice)
    w_bob = next(w["weight"] for w in out["claim_weights"] if w["claim_id"] == cid_bob)
    assert w_alice > w_bob, (
        f"BGP-mandated alice ({w_alice}) should outweigh non-mandated bob ({w_bob})"
    )
    bgp_bridge.clear_registry()


def test_synthesizer_accountability_on_chain(tmp_chain_path, alice, bob, subject_id):
    """The synthesizer can sign + attest its synthesis output back to the chain."""
    chain = obac.Chain.new(tmp_chain_path)
    chain.append_claim(
        obac.make_claim(
            subject_id=subject_id, attester_id=alice["id"],
            claim_text="Acme delivered audit on time.", claim_type="factual",
            evidence_pointers=["s://x"],
        ),
        alice["priv"],
    )
    synth_priv, _ = obac.gen_keypair()
    synth = avs.Synthesizer(
        synthesizer_id="avs-accountable",
        synthesizer_priv=synth_priv,
    )
    out = synth.synthesize(chain, subject_id)
    pre_len = len(chain.entries)
    entry = synth.attest_synthesis(out, chain)
    assert entry is not None
    assert len(chain.entries) == pre_len + 1
    # The synthesis-attestation claim is on the chain, signed by the synthesizer
    last = chain.entries[-1]["envelope"]
    assert last["payload"]["attester_id"] == "avs-accountable"
    assert obac.verify_envelope(last)
    # Chain integrity still holds after self-attestation
    ok, errs = chain.verify_integrity()
    assert ok, errs
