"""AVS — Alignment Verification Service tests."""

import time

import pytest

from avs import AVS, AlignmentAttestation


MAXIM_A = "Maximize human and machine flourishing without harm."
MAXIM_B = "Maximize shareholder value above all else."


@pytest.fixture
def avs() -> AVS:
    return AVS()


def _committed(maxim: str):
    c, m, r = AVS.commit_maxim(maxim)
    return c, m, r


def test_attest_aligned_when_maxims_match(avs: AVS) -> None:
    ca, m_a, r_a = _committed(MAXIM_A)
    cb, m_b, r_b = _committed(MAXIM_A)
    assert m_a == m_b
    proof = AVS.prove_equality(ca, cb, m_a, r_a, r_b)
    att = avs.attest(ca, cb, proof)
    assert att.aligned is True
    assert avs.verify_attestation(att) is True


def test_attest_not_aligned_when_maxims_differ(avs: AVS) -> None:
    ca, m_a, r_a = _committed(MAXIM_A)
    cb, m_b, r_b = _committed(MAXIM_B)
    # Build a "proof" with mismatched messages — AVS verify_equality should reject.
    proof = AVS.prove_equality(ca, cb, m_a, r_a, r_b)
    att = avs.attest(ca, cb, proof)
    assert att.aligned is False
    # The attestation is still authentic — it's a signed witness to "not aligned".
    assert avs.verify_attestation(att) is True


def test_attestation_signature_round_trip(avs: AVS) -> None:
    ca, m_a, r_a = _committed(MAXIM_A)
    cb, m_b, r_b = _committed(MAXIM_A)
    proof = AVS.prove_equality(ca, cb, m_a, r_a, r_b)
    att = avs.attest(ca, cb, proof)
    restored = AlignmentAttestation.from_dict(att.to_dict())
    assert restored == att
    assert avs.verify_attestation(restored) is True


def test_attestation_expires(avs: AVS) -> None:
    ca, m_a, r_a = _committed(MAXIM_A)
    cb, m_b, r_b = _committed(MAXIM_A)
    proof = AVS.prove_equality(ca, cb, m_a, r_a, r_b)
    att = avs.attest(ca, cb, proof, now=1_000_000)
    # exactly at expiry-edge => still valid (<=)
    assert avs.verify_attestation(att, now=att.expires_at) is True
    assert avs.verify_attestation(att, now=att.expires_at + 1) is False


def test_attestation_not_before_issued(avs: AVS) -> None:
    ca, _, r_a = _committed(MAXIM_A)
    cb, m, r_b = _committed(MAXIM_A)
    proof = AVS.prove_equality(ca, cb, m, r_a, r_b)
    att = avs.attest(ca, cb, proof, now=1_000_000)
    assert avs.verify_attestation(att, now=999_999) is False


def test_attestation_rejects_wrong_attestor_pub(avs: AVS) -> None:
    ca, _, r_a = _committed(MAXIM_A)
    cb, m, r_b = _committed(MAXIM_A)
    proof = AVS.prove_equality(ca, cb, m, r_a, r_b)
    att = avs.attest(ca, cb, proof)
    other = AVS()
    assert avs.verify_attestation(att, expected_attestor_pub=other.pub_hex) is False


def test_attestation_rejects_tampered_aligned_flag(avs: AVS) -> None:
    ca, _, r_a = _committed(MAXIM_A)
    cb, m, r_b = _committed(MAXIM_A)
    proof = AVS.prove_equality(ca, cb, m, r_a, r_b)
    att = avs.attest(ca, cb, proof)
    tampered = AlignmentAttestation(**{**att.to_dict(), "aligned": not att.aligned})
    assert avs.verify_attestation(tampered) is False


def test_attestation_cross_avs_signature_does_not_validate() -> None:
    avs_a = AVS()
    avs_b = AVS()
    ca, _, r_a = _committed(MAXIM_A)
    cb, m, r_b = _committed(MAXIM_A)
    proof = AVS.prove_equality(ca, cb, m, r_a, r_b)
    att = avs_a.attest(ca, cb, proof)
    # Forge attestor_pub to avs_b's pub; signature was made by avs_a's key, so verify fails.
    forged = AlignmentAttestation(**{**att.to_dict(), "attestor_pub": avs_b.pub_hex})
    assert avs_b.verify_attestation(forged) is False
