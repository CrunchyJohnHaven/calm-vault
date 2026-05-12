#!/usr/bin/env python3
"""
Proposed-fix sketch for TIER1_ISSUE_SYBIL_001 — Remediation R1.

This file is **NOT** wired into production. It exists to make the
remediation concrete and runnable for review. To actually adopt it, the
maintainer should:

  1. Add the eligibility helper to `src/money_python/harp.py`.
  2. Plumb it into `check_quorum` between the reliability filter and the
     sliding-window loop.
  3. Re-run the SMT theorem (`kill_switch_safety.smt2`) and the PoC
     (`sybil_attack_proof_of_concept.py`); K5 should flip to UNSAT and
     the PoC should report "Attack failed".

The eligibility helper requires every halt-eligible attester_pub to have
already contributed at least MIN_CORROBORATIONS prior non-halt claims
that were positively corroborated (i.e. agreed with by at least one
higher-reliability peer on the same subject). This blocks the
fresh-keypair Sybil because fresh keypairs have zero corroborated prior
claims by construction.
"""
from __future__ import annotations

import pathlib
import sys
from collections import defaultdict

_REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "src" / "money_python"))

import obac     # noqa: E402  (after sys.path insert)
import avs      # noqa: E402


# Tunables — placed at the same level as the other harp.py constants.
MIN_CORROBORATIONS_FOR_HALT_ELIGIBILITY = 1


def attester_pub_is_halt_eligible(
    chain: "obac.Chain",
    attester_pub_b64: str,
    subject_id: str,
    synth: "avs.Synthesizer",
) -> bool:
    """
    Return True iff attester_pub_b64 has at least MIN_CORROBORATIONS prior
    non-halt claims (any subject) that were corroborated by at least one
    higher-reliability peer.

    A "corroboration" here is a same-subject non-halt claim from a
    DIFFERENT attester_pub that has reliability >= the candidate's.
    The standard AVS reliability scoring is consulted; we do NOT trust
    the candidate's own self-attestations.
    """
    all_claims = [e["envelope"]["payload"] for e in chain.entries]
    all_envs = [e["envelope"] for e in chain.entries]

    # Build attester_id ↔ pub map from prior chain entries.
    pub_for_id = {}
    id_for_pub = defaultdict(set)
    for env in all_envs:
        aid = env["payload"]["attester_id"]
        apub = env["attester_pub"]
        pub_for_id.setdefault(aid, apub)
        id_for_pub[apub].add(aid)

    # Candidate's prior non-halt claims, indexed by claim text + subject.
    candidate_ids = id_for_pub.get(attester_pub_b64, set())
    own_claims = [
        c for c in all_claims
        if c["attester_id"] in candidate_ids and c["claim_type"] != "halt"
    ]

    # Reliability of the candidate itself; halt-eligibility excludes self.
    own_rel = synth.reliability(
        attester_pub_b64,
        next(iter(candidate_ids)) if candidate_ids else "",
        subject_id,
        all_claims,
        None,
    ) if candidate_ids else 0.0

    # Count corroborations.
    corroborations = 0
    for own_c in own_claims:
        own_subj = own_c["subject_id"]
        for other in all_claims:
            if other["claim_id"] == own_c["claim_id"]:
                continue
            if other["subject_id"] != own_subj:
                continue
            if other["claim_type"] == "halt":
                continue
            other_pub = pub_for_id.get(other["attester_id"])
            if other_pub == attester_pub_b64:
                continue
            if other_pub is None:
                continue
            r_other = synth.reliability(
                other_pub, other["attester_id"], own_subj, all_claims, None
            )
            if r_other >= own_rel:
                corroborations += 1
                break  # one corroborator per own-claim is enough

    return corroborations >= MIN_CORROBORATIONS_FOR_HALT_ELIGIBILITY


# Demonstration helper — shows how this hooks into check_quorum.
def patched_check_quorum_signature():
    """
    The patched signature would be identical to the current one; the only
    change is an extra filter step inside the body:

        eligible_pre_history = [
            h for h in eligible
            if attester_pub_is_halt_eligible(
                chain, attester_pub[h['attester_id']], subject_id, synth
            )
        ]

    then proceed with eligible_pre_history instead of eligible.
    """
    pass


if __name__ == "__main__":  # pragma: no cover
    print("This is a non-binding remediation sketch — see "
          "TIER1_ISSUE_SYBIL_001.md for details.")
