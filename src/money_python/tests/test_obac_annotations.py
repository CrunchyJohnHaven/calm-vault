"""OBAC annotation semantics: subject can annotate; cannot delete; annotation dampens weight."""
from __future__ import annotations

import pytest

import obac
import avs


def test_subject_can_annotate_a_claim(tmp_chain_path, alice, bob, subject_id):
    """The subject's own key can append an annotation that references a prior claim."""
    chain = obac.Chain.new(tmp_chain_path)
    # Bob (subject's representative) annotates Alice's claim
    c1 = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="Acme missed the deadline.", claim_type="factual",
    )
    e1 = chain.append_claim(c1, alice["priv"])
    cid = e1["envelope"]["payload"]["claim_id"]

    annotation = obac.make_claim(
        subject_id=subject_id, attester_id=bob["id"],
        claim_text="Context: hurricane delayed delivery by federal force-majeure clause.",
        claim_type="annotation", annotates=cid,
    )
    chain.append_claim(annotation, bob["priv"])

    ann_list = chain.annotations_for(cid)
    assert len(ann_list) == 1
    assert ann_list[0]["claim_text"].startswith("Context:")
    assert ann_list[0]["annotates"] == cid


def test_subject_cannot_delete_claim(tmp_chain_path, alice, bob, subject_id):
    """The append-only chain has no delete operation; annotations are the only response."""
    chain = obac.Chain.new(tmp_chain_path)
    c = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="Acme missed the deadline.", claim_type="factual",
    )
    e = chain.append_claim(c, alice["priv"])
    cid = e["envelope"]["payload"]["claim_id"]

    # There is no public delete API on Chain. Verify the surface is append-only.
    assert not hasattr(chain, "delete")
    assert not hasattr(chain, "remove")
    assert not hasattr(chain, "redact")

    # And the claim remains discoverable.
    assert chain.find(cid) is not None
    # Bob can only add an annotation — no removal — and the original still exists.
    chain.append_claim(
        obac.make_claim(
            subject_id=subject_id, attester_id=bob["id"],
            claim_text="Disputed; see annotation.",
            claim_type="annotation", annotates=cid,
        ),
        bob["priv"],
    )
    assert chain.find(cid) is not None  # original still on chain
    assert len(chain.annotations_for(cid)) == 1


def test_annotation_lowers_disputed_claim_weight(tmp_chain_path, alice, bob, subject_id):
    """A claim with one or more annotations gets lower weight than the same claim with none."""
    # Run twice: once without annotation, once with
    chain_a = obac.Chain.new(tmp_chain_path)
    c = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="Acme missed the deadline.", claim_type="factual",
        evidence_pointers=["s3://x"],
        submitted_at="2026-05-12T00:00:00+00:00",
    )
    chain_a.append_claim(c, alice["priv"])
    synth = avs.Synthesizer(synthesizer_id="avs-test")
    out_a = synth.synthesize(chain_a, subject_id)
    weight_before = out_a["claim_weights"][0]["weight"]

    # Now build a parallel chain with the SAME claim plus an annotation
    chain_b = obac.Chain.new(tmp_chain_path.parent / "chain_b.jsonl")
    chain_b.append_claim(c, alice["priv"])
    # Bob annotates
    ann = obac.make_claim(
        subject_id=subject_id, attester_id=bob["id"],
        claim_text="Late but with force-majeure clause; contested.",
        claim_type="annotation", annotates=c["claim_id"],
    )
    chain_b.append_claim(ann, bob["priv"])
    out_b = synth.synthesize(chain_b, subject_id)
    weight_after = out_b["claim_weights"][0]["weight"]

    assert weight_after < weight_before, (
        f"annotated weight {weight_after} should be < unannotated {weight_before}"
    )
