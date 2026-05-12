# TIER-1 Issue: SYBIL-001 — AAL Component 5 kill-switch is Sybil-vulnerable

**Status:** OPEN (filed by formal-verification pass, 2026-05-12)
**Severity:** TIER 1
**Affected components:** `src/money_python/harp.py` (`check_quorum`),
`src/money_python/avs.py` (`RELIABILITY_BASE`, `Synthesizer.reliability`).
**Discovered by:** Z3 SMT model `formal_verification/kill_switch_safety.smt2`
theorem K5 (returns SAT), plus the runnable proof-of-concept
`formal_verification/sybil_attack_proof_of_concept.py` against deployed code.

---

## Summary

A single attacker who controls **only fresh Ed25519 keypairs** (cost: 0
USD, ~milliseconds) can fire the kill-switch on **any** subject by
submitting `K = DEFAULT_K = 2` halt-claims, each signed by a distinct
fresh keypair with a distinct fresh `attester_id`, within the
`DEFAULT_WINDOW_SECONDS = 60` second window.

`check_quorum` returns `concurred = True`, and `emit_revoke_script`
emits a working `revoke.sh` that revokes the subject's credentials via
`calm_vault.py revoke-agent`.

## Why it works

1. `harp.py` deduplicates by `attester_id` (a free-form string), not by
   any cost-of-identity signal. Minting a new `attester_id` is free.
2. `avs.py:68 RELIABILITY_BASE = 1.0` — a brand-new attester with no
   prior chain entries scores 1.0.
3. `harp.py:55 DEFAULT_MIN_RELIABILITY = 0.5` — the reliability gate
   admits anything ≥ 0.5; 1.0 ≥ 0.5.
4. The self-burst penalty in `avs.py:78` (`BURST_THRESHOLD = 4` per
   `BURST_WINDOW_SECONDS = 300`) does not trigger because each Sybil
   identity submits exactly **one** halt-claim.

Therefore K = 2 distinct-`attester_id` halts within 60s from a single
attacker's two fresh keypairs is sufficient to fire the kill-switch.

## Reproduction

```
python3 formal_verification/sybil_attack_proof_of_concept.py
```

Captured output (also in `evidence_z3_runs.txt`):

```
Attacker minted 2 fresh keypairs:
  sybil_1 pub = ...
  sybil_2 pub = ...
Quorum check result:
  concurred              = True
  counted_attesters      = ['sybil_alice', 'sybil_bob']
  rejected_low_reliab    = []
ATTACK SUCCESSFUL: kill switch fired from ONE attacker with 2 fresh
keypairs. No real attestor pool was needed.
```

The SMT counter-example:

```
Z3 -smt2 formal_verification/kill_switch_safety.smt2  →  K5 = sat
  id_0 = 0, id_1 = 1, id_2 = 2 (three distinct attester_ids)
  halted_0,1,2 = true
  inwin_0,1,2  = true
  relok_0,1,2  = true  (each freshly minted)
  →  distinct_eligible_count = 3 ≥ M = 3  →  fires = true
```

## Impact

Anyone in the network can revoke any agent's credentials. This is
exactly the "anyone can fire the kill switch" property the system
advertises (`landing-sss/index.html:82`) — but with a **catastrophic
inversion**: it is not "anyone in a well-formed attestation network"
but "any single $0-cost attacker". This collapses the safety claim of
AAL Component 5 to "no safety at all" against a remotely-motivated
attacker.

In a production deployment with real value at stake (revoking a
business-critical AI agent's credentials disrupts service), the cost
to attack is essentially nil and the cost to defend is the recovery
cost of the revoked agent.

## Proposed remediations (the user must pick one — none of these are
applied in this PR)

### R1 — Halt-eligibility requires positive AVS history (smallest patch)

Require an attester_pub to have at least one corroborated non-halt
claim in the OBAC chain (with reliability ≥ floor at that time) **before**
its halt-claims count toward quorum.

Sketch: in `harp.py:check_quorum`, before adding an attester to the
eligible set, also require `synth.has_corroborated_history(attester_pub)
>= MIN_CORROBORATIONS`. This rules out brand-new pubkeys.

**Pros:** preserves "permissionless" — anyone can become halt-eligible
by participating positively first.
**Cons:** small but real onboarding latency for new attesters; an
attacker patient enough to build positive history can still attack.

### R2 — Stake-bonded attester_pubs

Each attester_pub must be bonded to a slashable deposit on
`calm_vault`. Quorum on a halt-claim slashes the deposit if any
subsequent corroboration is missing.

**Pros:** Strongest cost-of-attack; aligns economic incentives.
**Cons:** Requires on-chain deposit infrastructure; more design work.

### R3 — Bonded-attestor allow-list (least permissionless)

Maintain a slowly-rotating allow-list of attesters that have passed an
out-of-band onboarding check (BGP mandate, real-world identity, bond).
Only allow-listed attestations count toward quorum.

**Pros:** Bulletproof against Sybil.
**Cons:** Centralization; breaks the "permissionless attestation" claim.

### R4 — Time-decay onboarding

A new `attester_pub`'s reliability starts at `0`, rising linearly with
each corroborated claim over a 24h window before reaching
`RELIABILITY_BASE`.

**Pros:** simple; preserves permissionlessness; defeats the 60s attack
window.
**Cons:** Defenders also delayed; still vulnerable to patient adversary
running attestor farms over weeks.

## Recommendation

**R1 + R4 combined** is the smallest defense-in-depth fix. R1 closes
the immediate "fresh pubkey = quorum" hole; R4 widens the cost-window
so even a patient attacker would need a sustained attestor farm.

This PR **does not** apply any of the four remediations — they require
design decisions that change the system's permissionless / centralized
trade-off. We are filing this as a TIER-1 issue and inviting the
authors to choose.

---

## Verification of the fix

When a remediation is applied, re-run:

```
z3 -smt2 formal_verification/kill_switch_safety.smt2
python3 formal_verification/sybil_attack_proof_of_concept.py
```

K5 should switch from **SAT** (current) to **UNSAT** under the new
eligibility predicate, and the PoC should report "Attack failed
(unexpected)". When that happens, update this issue to CLOSED and
update `results.md` to reflect the new K5 status.
