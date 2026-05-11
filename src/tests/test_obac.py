"""OBAC — Oath-Based Access Control tests."""

import time

import pytest

from obac import (
    Decision,
    Oath,
    OathAuthority,
    Policy,
    PolicyEngine,
    verify_oath,
)


MAXIM = "Maximize human and machine flourishing without harm."
OTHER_MAXIM = "Maximize shareholder value above all else."


@pytest.fixture
def authority() -> OathAuthority:
    return OathAuthority()


@pytest.fixture
def engine(authority: OathAuthority) -> PolicyEngine:
    eng = PolicyEngine()
    eng.add_policy(Policy.for_maxim(
        resource="secret/api-key",
        action="read",
        maxim_text=MAXIM,
        authority_pub_hex=authority.pub_hex,
    ))
    return eng


def test_oath_issue_has_required_fields(authority: OathAuthority) -> None:
    oath = authority.issue("alpha", MAXIM)
    assert oath.agent_id == "alpha"
    assert oath.authority_pub == authority.pub_hex
    assert len(oath.signature) == 128  # 64 bytes hex
    assert len(oath.maxim_hash) == 64
    assert oath.issued_at > 0


def test_oath_verify_accepts_valid_signature(authority: OathAuthority) -> None:
    oath = authority.issue("alpha", MAXIM)
    assert verify_oath(oath) is True
    assert verify_oath(oath, authority_pub_hex=authority.pub_hex) is True


def test_oath_verify_rejects_substituted_authority(authority: OathAuthority) -> None:
    oath = authority.issue("alpha", MAXIM)
    other = OathAuthority()
    assert verify_oath(oath, authority_pub_hex=other.pub_hex) is False


def test_oath_verify_rejects_tampered_payload(authority: OathAuthority) -> None:
    oath = authority.issue("alpha", MAXIM)
    tampered = Oath(
        oath_id=oath.oath_id,
        agent_id="mallory",  # changed
        maxim_hash=oath.maxim_hash,
        issued_at=oath.issued_at,
        authority_pub=oath.authority_pub,
        signature=oath.signature,
    )
    assert verify_oath(tampered) is False


def test_oath_verify_rejects_corrupt_signature(authority: OathAuthority) -> None:
    oath = authority.issue("alpha", MAXIM)
    flipped = list(bytes.fromhex(oath.signature))
    flipped[0] ^= 0x01
    corrupt = Oath(**{**oath.to_dict(), "signature": bytes(flipped).hex()})
    assert verify_oath(corrupt) is False


def test_oath_rejects_empty_agent_or_maxim(authority: OathAuthority) -> None:
    with pytest.raises(ValueError):
        authority.issue("", MAXIM)
    with pytest.raises(ValueError):
        authority.issue("alpha", "")
    with pytest.raises(ValueError):
        authority.issue("alpha", "   ")


def test_decide_allows_when_oath_matches(
    authority: OathAuthority, engine: PolicyEngine,
) -> None:
    oath = authority.issue("alpha", MAXIM)
    decision = engine.decide(oath, action="read", resource="secret/api-key")
    assert decision.allowed is True
    assert decision.reason == "oath matches policy"
    assert decision.policy_id is not None
    assert decision.oath_id == oath.oath_id


def test_decide_denies_wrong_maxim(
    authority: OathAuthority, engine: PolicyEngine,
) -> None:
    oath = authority.issue("alpha", OTHER_MAXIM)
    decision = engine.decide(oath, action="read", resource="secret/api-key")
    assert decision.allowed is False
    assert "does not satisfy" in decision.reason


def test_decide_denies_no_policy_for_action(
    authority: OathAuthority, engine: PolicyEngine,
) -> None:
    oath = authority.issue("alpha", MAXIM)
    decision = engine.decide(oath, action="delete", resource="secret/api-key")
    assert decision.allowed is False
    assert "no policy covers" in decision.reason


def test_decide_honours_revocation(
    authority: OathAuthority, engine: PolicyEngine,
) -> None:
    oath = authority.issue("alpha", MAXIM)
    engine.revoke_oath(oath.oath_id)
    decision = engine.decide(oath, action="read", resource="secret/api-key")
    assert decision.allowed is False
    assert decision.reason == "oath revoked"
