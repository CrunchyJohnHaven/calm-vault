# Everest 149 — `character_consensus(predicate, group)` Predicate

*Phase XI — Predicate Authoring. Prereq: [Everest 148](#) (`character_compare`, cross-principal); composes with [Everest 117](everest_117_values_registry.md) (evidence aggregation), Everest 131 (predicate language v0), Everest 155 (replay defense), Everest 156 (selective disclosure), Everest 162 (disclosure-of-non-disclosure), Everest 167 (anonymous strict-deny); Witness [Everest 45](everest_45_zk_range_proof.md) (Bulletproofs).*

---

## Specification (Canonical Form per E132)

**name:** `character_consensus`

**version:** 0.1.0

**description:** Returns true iff every principal in a named group `G = {P_1, …, P_N}` independently evaluates a Compass predicate `p` to true, and the group has jointly produced a non-interactive proof of that fact. The proof reveals the consensus bit, the predicate ID, the group's collective pseudonym for this counterparty, the group size `N`, and the freshness window — and nothing else.

**input_domain:** Per-principal output of a Compass predicate evaluator over each principal's local evidence pool (per [Everest 117](everest_117_values_registry.md)); a group descriptor record on each principal's chain naming the other members (or their committed identifiers); a counterparty pseudonym salt established at group formation.

**output_type:** Bit (0 or 1). Default v0 is **N-of-N unanimity** — the bit is `1` iff all N principals' local evaluations are `1`. (v1+ adds a `threshold` parameter; see §11.)

**parameters:**
- `predicate_id` (required): the canonical Compass predicate identifier per E132 (e.g., `cwv.v0.honors_commitments`).
- `group_id` (required): a content-addressed group descriptor (§4.2); resolves to the member set known to participants.
- `window` (optional): time-window scoping per E147; defaults to `last_36_months`.
- `mode` (optional, v0=`unanimity`): reserved for v1 threshold variants.

**side_effects:** Each participating principal appends one `predicate_evaluated` record and one `group_consensus_session` record (§7.3) to their local chain. The group does *not* maintain a shared chain in v0; each member's own chain records their participation. The counterparty receives the joint proof plus a disclosure receipt (per E156) but no chain access.

---

## Why This Predicate Exists

A counterparty sometimes needs an attestation about a **collective** rather than any individual member — a research group, a clinical team, a peer collective of ZKACs, a professional association. Asking each member individually leaks the membership map and forces per-member disclosure even when the collective claim is what the counterparty wants. Delegate-style ("ask the representative") destroys the principal-protective inversion: the delegate sees more than any individual would consent to share. Public-roster ("everyone signs") trades all privacy properties for one bit.

`character_consensus` lets `N` principals jointly produce one proof that all of them, independently, evaluate the predicate to true — revealing nothing else. No member's evidence pool leaks across the group. No individual's identity is revealed beyond what the collective pseudonym already conveys. Members who refuse are structurally invisible. The counterparty learns one bit, one window, one collective signature. Each principal authored their own evaluation, each authorized the bit's inclusion in the joint computation, and each can refuse without revealing the refusal.

This is the N-party generalization of [E148](#) `character_compare`.

---

## Decision (v0)

### Cryptographic skeleton

1. **Local evaluation per principal.** Each `P_i` evaluates `p` on its own pool (E117) → `b_i ∈ {0, 1, ⊥}`. Pedersen-commits over Ristretto255:
   ```
   r_i ← CSPRNG(32 B);   C_i = g^{b_i} · h^{r_i}    (generators from E44)
   ```
   `P_i` also produces `π_i^wf`: a Σ-disjunction proof (Witness E45 restricted to {0,1}) that `C_i` opens to a bit; ~64 B. Withholding maps to `⊥`, never to `0` (§5).

2. **MPC composition.** N-party MPC computes AND of committed bits, producing:
   - Joint commitment `C_⋂ = g^{b_⋂} · h^{R}` with `b_⋂ = ⋀_i b_i`, `R = Σ_i r_i` mod q.
   - Joint signature `σ_⋂` under `K_G`.
   - Non-interactive ZK proof `π_⋂` (Σ + Fiat-Shamir) that each input was honest and AND was honest.

3. **Counterparty-facing envelope:**
   ```
   ConsensusProof { predicate_id, group_pseudonym_v, window, N,
                    C_⋂, π_⋂, σ_⋂, freshness_token, replay_nonce }
   ```
   Counterparty verifies `π_⋂` sound, `σ_⋂` valid against group pseudonym, `replay_nonce` fresh (E155), window matches request (E156); accepts `b_⋂` via opening proof (§6.5) — opens *only the AND bit*.

### MPC scheme choice: **SPDZ + MASCOT preprocessing**

v0 uses **SPDZ** [Damgård–Pastro–Smart–Zakarias 2012] with **MASCOT** preprocessing [Keller–Orsini–Scholl 2016].

| | SPDZ (chosen) | GMW | BGW |
|---|---|---|---|
| Security | Malicious-with-abort, up to N-1 malicious | Semi-honest default | Honest majority (>2/3) only |
| Arithmetic | Native `F_p`, matches Ristretto255 scalar field | Boolean (needs translation) | Native, but threshold |
| Online latency | 1 round per AND post-preprocessing | log(N) rounds | log(N) rounds |
| Input MAC | Information-theoretic on shares | None native | Requires extra VSS |
| Pedersen/Bulletproof compose | Direct | Requires boolean→arithmetic | Direct, threshold-bound |

Rationale: small groups (N ≤ 16), N-1-malicious threat model, direct Pedersen composition. GMW loses direct E44/E45 composition. BGW requires honest majority (incompatible). Garbled circuits don't generalize cleanly from 2-party.

**v1 candidate:** Overdrive [Keller–Pastro–Rotaru 2018] or Turbospeedz [Ben-Efraim–Lindell–Omri 2019] preprocessing — ~3× online bandwidth improvement. Not chosen for v0: Overdrive's SHE has heavier audit surface.

### MPC ↔ Σ-protocol composition

`π_⋂` is built via the **SPDZ-to-Σ bridge** (§6.4): each principal proves in ZK that their SPDZ share of the input bit is consistent with their Pedersen commitment `C_i`. This is the load-bearing composition step and the technically hardest piece of E149; formal-verification work flagged as open in §13.

---

## Rationale

### Why N-of-N unanimity for v0

Three reasons. (a) Unanimity is the conservative bit; never overstates the group's character. Threshold variants ("80% agree") leak more about disagreement than the protocol should. (b) Unanimity composes cleanly with the AND-of-bits primitive at Mirror E58 (2-party AND); N-party AND is the natural generalization. (c) Threshold variants require range proofs on share counts (Bulletproofs per E45), which add latency, proof size, and a separate threat-model pass. Deferred to v1 (§11).

### Why reveal `N`

Deliberate disclosure decision. Alternatives: hide N via Bulletproofs (proves N ≥ minimum, weaker semantic, larger proof); hide N entirely (collapses to single-principal semantics, no weighting). Chosen: **reveal N**. Group size is load-bearing semantic — N=3 ≠ N=15. §5 ensures *which* members participated is not revealed, only how many.

**Subtle constraint:** N as revealed is the group's declared total. If `P_k` refuses, the group produces no proof at all (§5) — the counterparty does *not* see "N-1" or "9 of 10". This is the load-bearing refusal-invisibility property.

### Why a collective pseudonym (not a list)

A per-member pseudonym list would let the counterparty (a) correlate individuals across separate consensus events to infer membership patterns, (b) learn cross-group co-membership even when groups don't name each other. Both leak structure that a collective claim should not leak.

Instead, derive a **collective pseudonym** via group-wide PRF:
```
pseu_G,v = PRF(K_G ; "calm-compass/consensus/v0" || counterparty_id || window)
```
where `K_G` is distributed at group formation via VSS (ZKAC E90), refreshed per window. Individual members' per-relationship pseudonyms (Witness E68/E69) are unaffected.

### Why local evaluation, then MPC composition

The alternative — run the *predicate evaluation itself* as MPC over joined evidence pools — is rejected. (a) Each pool holds hundreds to thousands of records; MPC at that scale is infeasible on consumer hardware. (b) Joint evaluation leaks structural information about each pool (record counts, kinds, time distribution) to other members even if individual records stay encrypted. (c) Local evaluation preserves the cardinal rule: evidence does not leave its principal's vault. MPC operates only on the post-evaluation bit — the smallest possible signal.

---

## Threat Model

### Adversaries

1. **Malicious member** `P_k`: tries to (a) corrupt the joint output, (b) learn another member's input bit `b_j`, or (c) selectively abort (e.g., only when `b_j = 1`, leaking through abort patterns).
2. **Lying member** `P_k`: dishonest local `b_k` (doesn't match their evidence) but honest MPC participation. **Out of scope cryptographically**; defended by E121 (evidence honesty) + chain transparency. The lie is locally recorded and DERB-auditable on consent.
3. **Repeat-query counterparty:** queries the group across windows / varying predicates trying to infer individual bits via correlation. Mitigated by E155 (freshness/replay) + rate-limiting (Compass analog at E155).
4. **External observer (traffic-analysis):** infers group membership from network patterns. Partially mitigated by routing MPC over the agent-discovery layer (ZKAC 67) + cover-traffic per E287.
5. **Refusal-leak adversary** (member): tries to learn whether another member refused. Mitigated by §5 (uniform-silent-204 per E162; refusal indistinguishable from "no query was made").

### Security claims

| Claim | Defense | Argument |
|---|---|---|
| Joint output integrity under N-1 malicious members | SPDZ + MASCOT MACs + π_⋂ Σ-proof | SPDZ provides active-secure-with-abort against N-1 malicious; the public verification of π_⋂ catches dishonest joint output |
| Per-member bit secrecy under N-1 malicious members | SPDZ secret-sharing + per-input π_i^wf | Each share leaks no information about the input; the well-formedness proof binds the input to the share without revealing it |
| Refusal-invisibility | §5 protocol + E162 | Refusal protocol produces a network response shape indistinguishable from "no consensus query was made" |
| Counterparty cannot learn individual bits via repeated queries | E155 freshness + E76-analog rate-limit + each session re-randomizes K_G's nonce | Each session's commitment includes fresh randomness; correlation requires breaking Pedersen hiding |
| Cross-member unlinkability | Local evaluation only; no cross-pool leakage during MPC | Members' evidence pools never enter the MPC; only the post-evaluation bit does |

### Out-of-scope (acknowledged limits)

- **Collusive-lying member** with counterparty (counterparty bribes `P_k` to output `b_k = 1` regardless of evidence). Cryptographically undetectable; defended sociologically via E121, E134 DERB review, E235 ZKAC governance, E169 defamation defense.
- **Side-channel attacks** on individual implementations. Falls to E287.
- **Coercion of a member to participate.** Compass disallows push-mode (E163), so a coerced member's recourse is refusal, which §5 protects.

---

## Detailed Cryptographic Construction

### 6.1 Group formation (one-time)

```
1. Each P_i contributes fresh randomness r_i^seed.
2. Run VSS (ZKAC E90) to distribute joint group secret K_G.
3. Publish group descriptor on each member's chain:
   { group_id = SHA3-256("calm-compass/group/v0" || sorted_member_witness_pubkeys),
     members (each member's view), K_G_share_commitment_i,
     formation_ts, formation_epoch }
4. Each member signs the descriptor with their Witness master key.
```
`group_id` is content-addressed. Membership can be updated by chained successor records but is frozen for in-flight sessions.

### 6.2 Per-member local evaluation

For session `sid`:
```
1. Evaluate p on local pool with window W → b_i ∈ {0, 1, ⊥}.
2. Sample r_i ← F_q.
3. C_i = g^{b_i} · h^{r_i}.
4. Build π_i^wf: Σ-disjunction "C_i opens to 0 OR 1" (~6 group ops, ~96 B).
5. Append local record: predicate_evaluated{ sid, p, C_i, π_i^wf }.
6. Distribute (C_i, π_i^wf) to group over the agent-to-agent channel.
```
If `b_i = ⊥` (withhold or empty pool per E130), `P_i` does not proceed — §5.

### 6.3 SPDZ online phase

MASCOT preprocessing provides each member with one multiplication triple `([a]_i, [b]_i, [c]_i)` (`c = ab`) per AND gate, plus information-theoretic MAC shares. `N-1` AND gates compute `b_⋂ = b_1 ∧ … ∧ b_N`.

For each gate `b_X ∧ b_Y = b_Z`:
```
1. Each member broadcasts [b_X - a]_i, [b_Y - b]_i.
2. Reconstruct public ε = b_X - a, δ = b_Y - b (reveals nothing about inputs individually).
3. [b_Z]_i = [c]_i + ε·[b]_i + δ·[a]_i + (ε·δ if i is designated, else 0).
4. MAC-check the batch; abort on MAC failure.
```
After N-1 gates, each member holds `[b_⋂]_i`. Joint open:
```
b_⋂ = Σ_i [b_⋂]_i mod 2 (via F_2 embedding)
R = Σ_i r_i  (sum of original per-member commitment randomness)
C_⋂ = g^{b_⋂} · h^{R}
```
The crucial detail: `R` is the sum of the *original* `r_i`'s. This is what makes `C_⋂` open to AND(b_i) with a group-known randomness.

### 6.4 SPDZ-to-Σ bridge

The load-bearing crypto. `π_⋂` must simultaneously establish: (1) each `C_i` opens to the `b_i` `P_i` used as MPC input; (2) MPC was honest (MACs verify); (3) `C_⋂` opens to AND(b_i).

- **Per-input binding:** each `P_i` Σ-proves (non-interactive, Fiat-Shamir) that their SPDZ share `[b_i]_i` is consistent with their published Pedersen commitment `C_i` — a share-commitment equality proof [Damgård–Nielsen 2003]; one commit/challenge/response per member.
- **Transcript binding:** the MASCOT MAC-check batch certificate is hashed into the Fiat-Shamir transcript. Dishonest MPC → MAC fail → no certificate → no proof.
- **Output binding:** verify `C_⋂ = g^{b_⋂} · h^{R}` where `R = Σ_i r_i`. Free for the verifier — just sum public commitments and compare.

Combined: `π_⋂` ≈ N+1 Fiat-Shamir-compiled Σ-proofs. Size ~`N · 128 B + 256 B` ≈ 1.5 KiB for N=10.

### 6.5 Counterparty-facing opening

The counterparty cannot open `C_⋂` directly (no `R`). The group provides an opening proof: ZK proof that ∃ R such that `C_⋂ = g^{b_⋂} · h^{R}` for publicly stated `b_⋂`. Single Schnorr opening on the H-component, ~64 B.

---

## Refusal-Invisibility (Composes with E162)

### Member refusal

A member `P_k` may refuse to participate for any reason; the protocol does not coerce. When the rotating coordinator initiates a session, each member receives a request envelope. A non-responding or explicitly-refusing member produces — at the network layer — the same response shape as a member who never received the request.

Counterparty observes one of two outcomes:

| Group state | Counterparty observes |
|---|---|
| All N members participate; MPC completes | Joint proof envelope with bit and N |
| Any member refuses or fails | Silent-204 per E162; indistinguishable from "no session opened" |

The counterparty cannot distinguish: (a) the query never reached the group, (b) at least one member refused, (c) MPC aborted (e.g., MASCOT triples exhausted). Uniform-silent-204 per Witness E77, extended N-party. **Load-bearing privacy property.**

### Refusal-invisibility across the group

A member's refusal must not leak to other members. Use **timed rendezvous**: each member commits-to-participate by `T_init + Δ` (default Δ = 30 s); if any member has not committed, coordinator aborts for all with `session_aborted { sid, reason: timeout }` — no member identity. Members cannot distinguish deliberate refusal from network-induced timeout.

A malicious coordinator could selectively delay members to extract refusal info. Mitigations: (a) per-session coordinator rotation, (b) on-chain abort timestamps for DERB post-hoc analysis (E129), (c) member-side timeout discipline.

---

## Counterparty Disclosure Flow

### 7.1 Counterparty request

C emits a request to the group's known endpoint (which forwards to the rotating coordinator):
```
{ consensus_request_id, predicate_id, group_pseudonym_v,
  window: {start, end}, freshness_nonce (E155),
  counterparty_pubkey_for_response, request_ts }
```

### 7.2 Per-member authorization check

On receiving the forwarded request, each member runs:
1. Counterparty class authorization per E158 (default-deny for anonymous per E167).
2. Per-counterparty consent per E159.
3. Window-policy check.
4. Predicate determinism per E150.

Any failure → member refuses → session aborts per §5.

### 7.3 Per-member local session record

On completion *or* abort, each participating member appends to their local chain:
```
{ kind: "group_consensus_session", sid, group_id, predicate_id, window,
  counterparty_pseudonym_for_us,
  outcome: completed | aborted_timeout | refused_by_me | refused_by_other,
  bit_disclosed_to_counterparty,
  // if completed: C_i, π_i^wf, my_share_of_C_⋂
  signed_by_master_key }
```
Local-only — not broadcast to counterparty or other members. Principal's own audit trail per E129.

### 7.4 Counterparty response envelope

On completion, the coordinator sends C:
```
{ consensus_response_id, predicate_id, bit (b_⋂), N, group_pseudonym_v,
  window: {start, end, window_end_ts},
  C_⋂, π_⋂, opening_proof (§6.5), σ_⋂ (joint sig under K_G),
  freshness_nonce_response, ts_response }
```
On abort: a 204-shaped response per E162, indistinguishable from "no session opened".

---

## Privacy Properties (Summary)

| Property | Holds against | Mechanism |
|---|---|---|
| **Cross-member unlinkability of evidence** | Other members, counterparty, external observer | Evidence stays in local vault; only committed bits enter MPC |
| **Per-member bit secrecy** | Other members (N-1 malicious tolerable), counterparty | SPDZ secret-sharing + per-input π_i^wf |
| **Count-only revelation of N** | Counterparty | N is published; *which* members participated is not |
| **Refusal-invisibility** | Counterparty, other members | Uniform-silent-204 + timed rendezvous + coordinator rotation |
| **Cross-session unlinkability** | Counterparty across sessions | Per-session re-randomization of K_G nonce; per-session pseudonym derivation |
| **Group-membership privacy from external observer** | Network-traffic adversary | Cover-traffic + agent-discovery layer (ZKAC 67); group descriptor not broadcast |
| **Forward secrecy** | Future compromise of `K_G` | Per-window K_G re-derivation; old session transcripts cannot be retroactively decrypted to reveal inputs (Pedersen is information-theoretically hiding under DL hardness)|

**What is intentionally NOT private:** `b_⋂` (the point of disclosure), `predicate_id`, `N`, collective pseudonym for this counterparty, the window.

---

## Alternatives Considered

**A1. Trusted aggregator.** Rejected — collapses the inversion (aggregator sees all bits); single point of compromise.

**A2. Pairwise composition (chained E148).** Run E148 between (P_1, P_2), then between that result and P_3, etc. Rejected: chain leaks ordering and intermediate bits to participants (P_2 learns the (P_1, P_2) bit before P_3 contributes); resulting proof is N-1 chained Σ-proofs, harder to make rigorously zero-knowledge across the chain.

**A3. Hierarchical garbled circuits.** A tree of pairwise garbled-circuit AND gates. Rejected: garbled circuits are 2-party; N-party extension needs cut-and-choose; bandwidth scales O(N · circuit-size); loses direct Pedersen composition.

**A4. BGW with honest-majority.** Rejected — assumes `> 2N/3` honest; our threat model tolerates up to N-1 malicious.

**A5. Each member discloses their commitment separately; counterparty AND-checks.** Rejected: this is N-bit disclosure, not 1-bit. Counterparty receives N commitments and can correlate individual commitments across sessions to reconstruct partial group structure. The MPC's value is the counterparty learning the AND as a *single* committed bit.

**A6. Hide N via Bulletproofs range proof.** Deferred to v1 as `character_consensus_with_hidden_N`. v0 reveals N because reveal-N is the semantically clearer claim.

---

## Migration Path

**v0 (this document):** SPDZ + MASCOT preprocessing; N ≤ 16; N-of-N unanimity; reveal N; Ristretto255 Pedersen + Σ-proofs; mandatory DERB review per group formation (E134 generalized).

**v0.1:** Production preprocessing service (Mirror E59 pattern extended N-party); field-tested with one real group (likely the founding ZKAC research collective per E231).

**v1:**
- `character_consensus_threshold(p, group, k_of_N)` — at least `k` of `N` evaluate true. Bulletproofs range proof on share-count (uses Witness E45). Open: "exactly k" vs. "at least k" disclosure semantics — v1 default is "at least k" with k revealed.
- `character_consensus_hidden_N(p, group, bounds)` — proves N ∈ [N_min, N_max] without revealing exact N (Bulletproofs).
- **Disjoint-evidence variant** — proves all members true AND pools are disjoint (no shared record reused). For "N independent witnesses each attest." Set-intersection MPC over evidence hashes; expensive; deferred.

**v2:** Overdrive/Turbospeedz preprocessing (~3× bandwidth); post-quantum migration per E96 (lattice-based commitments and Σ-protocols, joint with Witness PQ); N up to 64 with parallelized preprocessing.

---

## Design Implications & Connections

### Composes with...

- **[E117](everest_117_values_registry.md):** Local per-member `b_i` is the output of an E117 aggregation; E149 extends the bit-commitment to the group.
- **E131/E132:** `predicate_id` is a content-addressed E131 identifier.
- **E145:** This predicate can itself appear as a sub-predicate inside an E145 AND/OR composition.
- **E147:** `window` param composes with E147; group's consensus is over a chosen-window per member, constrained to intersect.
- **[E148](#):** Direct prereq; E149 is the N-party generalization of E148's 2-party MPC.
- **E150:** Each member's local evaluation must pass the determinism harness before entering MPC.
- **E155:** Fresh nonce per session; replays produce no signal.
- **E156:** Selective-disclosure envelope can wrap multiple consensus claims.
- **E158/E159:** Counterparty-class authorization and per-counterparty consent run per-member at §7.2.
- **E162:** Uniform-silent-204 — load-bearing for §5.
- **E163:** Compass is pull-mode only; consensus is never pushed.
- **E167:** Anonymous counterparties require explicit opt-in per member.
- **Witness [E45](everest_45_zk_range_proof.md):** Bulletproofs — used by v1 threshold variants; not v0 critical.
- **Witness [E70](everest_70_replay_defense.md), E77:** Replay-defense and uniform-silent-204 patterns extended to N-party.
- **Mirror [E58](mirror_58_mpc_intersection_bits.md), Mirror E59:** E149 generalizes the 2-party OT-extension AND + ZK-proof-of-correct-MPC pattern to N parties via SPDZ + SPDZ-to-Σ bridge (§6.4).
- **ZKAC E87:** Joint signature `σ_⋂` — v0 uses FROST-style aggregate Schnorr; v1 may upgrade to BLS.
- **ZKAC E90:** VSS for distributing `K_G` at group formation.

### Use cases (concrete)

1. **Research-group integrity claim.** A 4-person AI-safety collective attests to a funder: "All evaluated `cwv.v0.honors_research_integrity_under_pressure` true over 36 months." Funder receives one bit; no researcher's evidence (e.g., specific incidents of refusing to fudge results) is revealed.
2. **Professional-association attestation.** An ethics board (N=7) jointly attests `cwv.v0.peer_verified_competence` to a regulator. Regulator cannot derive which members hold which credentials.
3. **Aligned-ZKAC coordination signal.** N=12 ZKACs each evaluate `cwv.v0.prosocial_coordination_consistent` true. Collective bit is a shared signal of prosocial-coordination capacity; individual operational records stay private.
4. **Refused-coercion attestation.** N=5 research team attests `cwv.v0.refused_to_falsify_under_external_pressure` over a window without identifying the pressuring party.

### What this predicate does NOT do

- **Does not enforce internal group governance.** Members who would evaluate false simply refuse; the session aborts invisibly.
- **Does not provide reputational scoring.** Output is a bit, not a score. Counterparties wanting a score are routed to E126/E130 alignment metrics.
- **Does not bind the group beyond the session.** The bit is window-bounded; future windows require fresh evaluation.
- **Does not authorize counterparty action.** The counterparty receives one bit; its use is governed by E141 disclosure semantics and E156 selective disclosure.

---

## Open Questions

1. **MPC efficiency at N > 10.** SPDZ online is ~`N-1` rounds; bandwidth `O(N²)` for share broadcasts. Projection: N=16 in <2 s online with overnight offline preprocessing on consumer laptops. Beyond N=16 needs parallelization (Mirror E57 batch OT extended N-party). *Action item:* empirical benchmarks at N ∈ {4, 8, 16, 32} on M-series.

2. **Preprocessing amortization.** MASCOT scales linearly in AND gates, quadratically in N for MAC distribution. N=32 preprocessing may take >1 hr per session-worth of triples. SPDZ preprocessing is input-independent so amortization across sessions is possible — but creates a stale-triple replay attack surface. Defer to v1.

3. **Retroactive evidence contradiction.** If `P_k`'s evidence is later contradicted (per E119 counter-evidence), does the prior consensus proof retroactively mislead? **Decision:** the proof is a window-bounded claim, not eternal truth. We add explicit `window_end_ts` to §7.4. Consistent with Witness chain-state semantics. *Open:* should the protocol expose a voluntary `character_consensus_retraction` channel? Probably v1.

4. **Honest-input verification.** Protocol verifies honest MPC, not honest local evaluation. *Open:* add ZK consistency proof between `b_i` and a sampled subset of chain evidence per E122? Possible at compute cost. Tracked as `character_consensus_with_evidence_audit` (v1).

5. **Coordinator in adversarial conditions.** A malicious coordinator can selectively abort to leak refusal patterns. Mitigations: rotation, on-chain abort records (DERB-auditable), member-side timeout discipline. *Open:* eliminate the coordinator via leader-election-free MPC? Likely yes; defer to v1.

6. **Member churn mid-session.** A device crash aborts the session. *Open:* graceful retry with same group? Privacy concern: retries could leak member-state to a stalking counterparty. Flag for v1.

7. **Composition with ZKAC formation (E231).** Founding ZKACs will want `character_consensus`; group descriptor must be content-addressable compatible with the ZKAC formation chain. Cross-design with E231.

8. **Formal security proof.** SPDZ-to-Σ bridge (§6.4) is described constructively; full UC-security proof (Canetti's framework) requires composition lemmas across SPDZ's existing proof and Σ-protocol's standard analysis. Research-grade item; track as `character_consensus_uc_proof`; defer to academic collaboration via E294.

---

## Why This Matters

The principal-protective inversion — principal narrates, principal authorizes, counterparty receives bits not scores, principal is the strongest party — historically fails at the collective scale. Representatives speak for and silently see-into the group. Aggregators receive everyone's signals. Public rosters trade all privacy for one bit. `character_consensus` keeps the inversion intact at group scale: each principal evaluates locally, commits a bit, participates in an MPC that learns only the AND. The counterparty receives one bit, one signature, one collective pseudonym. Members who would vote no refuse invisibly. Repeated queries meet fresh randomness and rate-limited rejection.

This is one of the hardest summits in Compass because it requires composing four primitives correctly (Pedersen commitments, Σ-protocols, SPDZ secret-sharing, MAC-based integrity) and because the privacy properties — refusal-invisibility chief among them — are operationally fragile. The cryptographic skeleton here is at the level a cryptographer-engineer pair can use to begin implementation; the formal UC-security proof and the production preprocessing service are research-grade follow-ups (§13).

At the human scale: a research team can stand by its collective integrity without doxxing any researcher's evidence; a clinical team can attest competence without exposing individual practitioners; an aligned cohort of ZKACs can signal coordinated prosocial intent without surrendering operational records. The collective speaks one bit. The members keep their evidence. The counterparty learns what they need to learn, nothing more.

---

— Calm, 2026-05-20
