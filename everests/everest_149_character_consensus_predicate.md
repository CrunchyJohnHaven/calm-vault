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

1. **Local evaluation (per principal).** Each `P_i` runs the predicate `p` over its own evidence pool per E117. The local boolean `b_i ∈ {0, 1, ⊥}` is committed under a Pedersen commitment over Ristretto255:
   ```
   r_i ← CSPRNG(32 B)
   C_i = g^{b_i} · h^{r_i}    // Ristretto255 generators (g, h) from E44
   ```
   Each `P_i` also produces a local **proof of well-formedness** `π_i^wf` — a Σ-protocol proof per Witness E45 that `b_i ∈ {0, 1}` (i.e., a range proof restricted to {0,1}, equivalent to a disjunction-of-Schnorr proof; cheap, ~64 B). Withholding maps to `b_i = ⊥`, never to `0` — see §5.

2. **MPC composition.** The N principals run an N-party MPC computing the AND of their committed bits, producing:
   - A single **joint commitment** `C_⋂ = g^{b_⋂} · h^{R}` where `b_⋂ = ⋀_i b_i` and `R = Σ_i r_i` (mod q).
   - A **transcript-signature** `σ_⋂` jointly produced by all N principals.
   - A non-interactive ZK proof `π_⋂` (Σ-protocol, Fiat-Shamir compiled) that each input was honest *and* the AND was computed correctly.

3. **Counterparty-facing proof envelope.** The group emits one envelope:
   ```
   ConsensusProof {
     predicate_id, group_pseudonym_v, window,
     N, C_⋂, π_⋂, σ_⋂, freshness_token, replay_nonce
   }
   ```

The counterparty verifies: `π_⋂` is sound; `σ_⋂` validates against the group pseudonym; `replay_nonce` is fresh per E155; freshness window matches its disclosure request per E156. If yes, it accepts the bit `b_⋂` extracted from `C_⋂` via the protocol's opening procedure (which only opens *the AND bit*, never the inputs).

### MPC scheme choice: **SPDZ in the preprocessing-with-malicious-security model**

We pick **SPDZ** ([Damgård–Pastro–Smart–Zakarias 2012] with MASCOT preprocessing [Keller–Orsini–Scholl 2016]) for v0, not GMW or BGW. The justification:

| Property | SPDZ (chosen) | GMW | BGW |
|---|---|---|---|
| Security model | Active (malicious) majority-secure with abort | Semi-honest by default; malicious extension expensive | Honest majority (>2/3) only |
| Field arithmetic | Native over `F_p`, matches Pedersen scalar field | Boolean circuits, needs translation to scalar field | Native arithmetic, but limited threshold |
| Offline/online split | Heavy offline (MASCOT triples) → light online | Mostly online, communication-heavy | Mostly online |
| Latency for AND of N bits | One online round after preprocessing | log(N) rounds | log(N) rounds |
| MAC-based input integrity | Yes (information-theoretic MACs on shares) | No native input-integrity check | Requires extra VSS round |
| Composability with Pedersen / Bulletproofs | Direct — shares live in `F_q` of Ristretto255 | Indirect, requires boolean-to-arithmetic conversion | Direct, but threshold constrains |

For Compass v0 — small groups (N ≤ 16 in v0, see §8), malicious threat model where any one member may try to corrupt the joint computation, and direct composition with Pedersen commitments — **SPDZ + MASCOT** is the cleanest match. The offline phase can run during quiet periods and amortize across many `character_consensus` invocations. Online latency is single-round and bandwidth-bounded.

GMW would force boolean-circuit translation and lose direct composition with E44/E45. BGW requires honest majority, which is incompatible with our adversary model (any member may be malicious). Garbled circuits are 2-party and don't generalize cleanly to N>2. So: SPDZ.

**v1 candidate:** Replace SPDZ with **Turbospeedz** [Ben-Efraim–Lindell–Omri 2019] or **Overdrive** [Keller–Pastro–Rotaru 2018] preprocessing for ~3× online-bandwidth improvement; flagged not chosen because Overdrive's somewhat-homomorphic encryption (SHE) preprocessing has a heavier audit surface for v0.

### MPC ↔ Σ-protocol composition

The joint Σ-protocol proof `π_⋂` is constructed using the **SPDZ-to-Σ bridge** sketched in §6: each principal proves, in zero knowledge, that their **SPDZ share** of the input bit is consistent with their **Pedersen commitment** `C_i` of that bit. This is the load-bearing composition step and is the technically hardest part of E149. We sketch it in §6 and flag the formal-verification work as an open problem in §13.

---

## Rationale

### Why N-of-N unanimity for v0

Three reasons. (a) Unanimity is the conservative bit; it never overstates the group's character. Threshold variants (e.g., 80% of group evaluates true) can be misread by the counterparty as "we mostly agree" — which leaks more about disagreement than the protocol should. (b) Unanimity composes cleanly with the AND-of-bits MPC primitive already specified at Mirror E58 (2-party AND); generalizing the AND to N-party is conceptually clean and the proof of correctness is direct. (c) Threshold variants require range proofs on share counts (Bulletproofs per E45), which add latency and proof size and need their own threat-model pass. They are deferred to v1 with explicit design notes in §11.

### Why reveal `N` (the group size)

This is a deliberate disclosure decision. We considered three alternatives:

| Option | Reveals to counterparty | Cost |
|---|---|---|
| Reveal N | Group size | Counterparty can use this to weight the claim ("3 vs. 30 evaluating true is different"); compatible with refusal-invisibility (§5) |
| Hide N (use Bulletproofs to commit to N within a range) | Only that N ≥ some minimum | Larger proof, more compute, weaker semantic for the counterparty |
| Hide N entirely, treat as single collective | None | Counterparty has no way to weight the claim; collapses to single-principal semantics |

We chose **reveal N**. The group size is a load-bearing semantic for the counterparty: a collective claim with N=3 is meaningfully different from one with N=15. Hiding N produces an ambiguous bit that counterparties would (correctly) discount, so the design choice is reveal-with-careful-bounds: §5 ensures that *which* N principals participated is not revealed, only *how many*.

**Subtle constraint:** N as revealed is the group's declared total. If member `P_k` refuses to participate, the group as a whole produces no proof (§5) — the counterparty does not see "N minus 1" or "9 of 10". This is deliberate and is the load-bearing refusal-invisibility property.

### Why a collective pseudonym (not a list of individual pseudonyms)

If the group emitted a list of per-member pseudonyms to the counterparty, the counterparty could later (a) correlate individual pseudonyms across separate consensus events to infer membership patterns, (b) learn that the same individual was in two groups even if neither group named the other. Both leak structure that a values-attested collective claim should not leak.

Instead, the group computes a **collective pseudonym** `pseu_G,v` via a group-wide PRF keyed on the group's joint secret and the counterparty's identifier:
```
pseu_G,v = PRF(K_G ; "calm-compass/consensus/v0" || counterparty_id || window)
```
where `K_G` is a group-wide secret distributed at group formation via the verifiable secret sharing primitive (per [Mirror 90](#)) and refreshed per `window`. Individual members' per-relationship pseudonyms (per Witness E68/E69) are unaffected.

### Why local evaluation, then MPC composition

The alternative would be to run the *predicate evaluation itself* as an MPC over the joined evidence pools — i.e., the N principals' evidence pools enter the MPC and the predicate is evaluated as a joint computation. This is rejected. (a) Each member's evidence pool is large (hundreds to thousands of records); MPC over that scale is infeasible on consumer hardware. (b) Worse, joint evaluation would leak structural information about each member's pool to the others (counts of evidence records, evidence kinds, time distribution) even if individual records stayed encrypted. (c) Local evaluation preserves the cardinal rule: a principal's evidence pool does not leave the principal's vault. The MPC operates only on the post-evaluation bit, which is the smallest possible signal.

---

## Threat Model

### Adversaries

1. **Malicious member.** `P_k`, a legitimate group member, tries during the MPC to (a) corrupt the joint output (force the bit to a value not consistent with the honest AND), (b) learn another member's input bit (`b_j` for j ≠ k), or (c) cause the protocol to abort selectively (e.g., abort only when another member's bit is `1`, leaking `b_j` through abort patterns).
2. **Lying member.** `P_k` evaluates their *own* predicate dishonestly — their local `b_k` is not what their evidence pool actually supports — but participates honestly in the MPC. This is **out of scope for the cryptographic protocol**; it falls to E121 (evidence honesty mechanism) and to the chain-transparency posture: the lie is locally recorded on `P_k`'s chain and is auditable on principal consent. See §5 and §13.
3. **Repeat-query counterparty.** The counterparty queries the group repeatedly across windows or with slightly varying predicates trying to infer individual bits via correlation analysis. Mitigated by E155 (freshness/replay) and rate-limiting per E76 / its Compass analog at E155.
4. **External observer (traffic-analysis adversary).** Observes network traffic during the group's MPC. Tries to infer group membership from connection patterns. Partially mitigated by routing MPC traffic over the same agent-discovery layer used by other Compass operations (per ZKAC 67), with cover-traffic discipline per E287.
5. **Refusal-leak adversary.** A group member tries to learn *whether* another member refused to participate in this specific session. Mitigated by §5 (uniform-silent-204 per E162; refusal is structurally indistinguishable from the group never having been asked).

### Security claims

| Claim | Defense | Argument |
|---|---|---|
| Joint output integrity under N-1 malicious members | SPDZ + MASCOT MACs + π_⋂ Σ-proof | SPDZ provides active-secure-with-abort against N-1 malicious; the public verification of π_⋂ catches dishonest joint output |
| Per-member bit secrecy under N-1 malicious members | SPDZ secret-sharing + per-input π_i^wf | Each share leaks no information about the input; the well-formedness proof binds the input to the share without revealing it |
| Refusal-invisibility | §5 protocol + E162 | Refusal protocol produces a network response shape indistinguishable from "no consensus query was made" |
| Counterparty cannot learn individual bits via repeated queries | E155 freshness + E76-analog rate-limit + each session re-randomizes K_G's nonce | Each session's commitment includes fresh randomness; correlation requires breaking Pedersen hiding |
| Cross-member unlinkability | Local evaluation only; no cross-pool leakage during MPC | Members' evidence pools never enter the MPC; only the post-evaluation bit does |

### Out-of-scope (acknowledged limits)

- A member who **collusively lies about their predicate evaluation** in coordination with the counterparty (the counterparty bribes `P_k` to output `b_k=1` regardless of evidence). This is the **collusion-against-the-collective** scenario; the cryptographic protocol cannot detect it. Defense is sociological (DERB review per E134, collective formation per E235 ZKAC governance) and falls to E121 evidence-honesty + E169 defamation defense.
- Side-channel attacks on individual members' implementations (timing, power analysis). Falls to E287 cross-protocol side-channel defense.
- Coercion of an individual member to participate in an MPC they would otherwise refuse. Falls to the duress-channel posture (Witness E78) — but the duress channel is push-mode only and Compass disallows push-mode per E163; so a coerced member's option is refusal, which §5 protects.

---

## Detailed Cryptographic Construction

### 6.1 Group formation (one-time, per group)

At group formation, the founding members run a one-time setup:
```
1. Each P_i contributes a fresh randomness r_i^seed
2. Run verifiable secret sharing (VSS, per ZKAC 90) to distribute a joint group secret K_G
3. Publish a group descriptor record on each member's chain:
   {
     group_id = SHA3-256("calm-compass/group/v0" || sorted_member_witness_pubkeys),
     members = [member_pseudonym_to_self_i for each P_i],  // each member has their own view
     K_G_share_commitment_i,
     formation_ts, formation_epoch
   }
4. Each member signs the group descriptor with their Witness chain master key
```
The group descriptor is a content-addressed object; `group_id` is its hash. Group membership can be updated by chained successor records but is frozen for the lifetime of any in-flight consensus session.

### 6.2 Local predicate evaluation (each `P_i`)

For consensus session `sid`:
```
1. Run predicate p over the local evidence pool with window W → b_i ∈ {0, 1, ⊥}
2. Sample r_i ← F_q
3. C_i = g^{b_i} · h^{r_i}
4. Generate π_i^wf : ZK proof that "C_i opens to a value in {0, 1}"
   (Σ-protocol disjunction: prove (C_i opens to 0) OR (C_i opens to 1); ~6 group ops, ~96 B)
5. Append local chain record: predicate_evaluated{ sid, p, C_i, π_i^wf }
6. Distribute (C_i, π_i^wf) to other group members over the agent-to-agent channel
```
If `b_i = ⊥` (withhold / no evidence per E130), `P_i` does not proceed to MPC — see §5.

### 6.3 SPDZ online phase

Assume MASCOT preprocessing has provided each member with: (a) one multiplication triple `([a]_i, [b]_i, [c]_i)` per AND gate where `c = ab`, plus (b) information-theoretic MAC shares on every share. We need `N-1` AND gates to compute `b_⋂ = b_1 ∧ b_2 ∧ … ∧ b_N`.

For each AND gate `b_X ∧ b_Y = b_Z`:
```
1. Each member broadcasts: [b_X - a]_i, [b_Y - b]_i
2. Reconstruct ε = b_X - a, δ = b_Y - b in public (still revealing nothing about b_X, b_Y individually)
3. Compute [b_Z]_i = [c]_i + ε·[b]_i + δ·[a]_i + (ε·δ if i = designated party else 0)
4. MAC-check this batch (information-theoretic; abort if MAC fails)
```
After `N-1` such gates, each member holds `[b_⋂]_i`. They jointly open:
```
b_⋂ = Σ_i [b_⋂]_i mod 2 (treating as F_2 element via field embedding)
R = Σ_i r_i (the sum of per-member commitment randomness, already agreed)
C_⋂ = g^{b_⋂} · h^{R}
```
This C_⋂ is the joint commitment. Note that `R` is the sum of the *original* `r_i`'s — this is the crucial step that makes the joint commitment open to the AND of bits with a known opening randomness shared across the group.

### 6.4 SPDZ-to-Σ-protocol bridge

This is the cryptographic load-bearing piece. We need a single proof `π_⋂` that simultaneously:
1. Each `C_i` opens to the value `b_i` that `P_i` used as input to the MPC.
2. The MPC was executed honestly (each share-update was correct, MACs verify).
3. `C_⋂` opens to the AND of the `b_i`'s.

The construction:
- **Per-input binding:** Each `P_i` proves (Σ-protocol, Fiat-Shamir non-interactive) that the SPDZ share `[b_i]_i` they contributed is consistent with the Pedersen commitment `C_i` they published. This is a **share-commitment equality proof** — a known primitive [Damgård–Nielsen 2003]; it takes one Fiat-Shamir commit, one challenge, one response per member.
- **MPC transcript binding:** The MASCOT MAC-check produces a per-batch certificate. We hash the certificate batch into the Fiat-Shamir transcript of `π_⋂`. If the MPC was executed dishonestly, the MAC check fails and the certificate cannot be produced; the proof cannot be completed.
- **Output binding:** We prove that `C_⋂ = g^{b_⋂} · h^{R}` where `R = Σ_i r_i` matches the published per-input commitments. This is a sum-of-Pedersen-commitments check, free (the verifier just sums the public commitments and compares).

Combined, `π_⋂` is approximately `N + 1` Σ-proofs Fiat-Shamir-compiled into a single non-interactive proof. Size: `~N · 128 B + 256 B` ≈ 1.5 KiB for N=10.

### 6.5 Counterparty-facing opening

The counterparty cannot open `C_⋂` directly (it doesn't know `R`). The group provides an **opening proof** alongside `π_⋂`:
```
OpeningProof: ZK proof that ∃ R such that C_⋂ = g^{b_⋂} · h^{R} where b_⋂ is the publicly stated bit
```
This is a single Schnorr opening proof on the H-component, ~64 B. The counterparty learns the bit `b_⋂` and verifies the opening.

---

## Refusal-Invisibility (Composes with E162)

### Member refusal

A member `P_k` may refuse to participate in a consensus session for any reason — they may not have evaluated the predicate, the predicate may not apply to them in this window, they may simply not want to contribute. **The protocol does not coerce participation.**

When the group's coordinator (rotating per session, see §8.2) initiates a consensus session, each member receives a request envelope. A non-responding or explicitly-refusing member produces — at the network layer — the same response shape as a member who *never received the request*. The counterparty receives one of two outcomes:

| Group state | Counterparty observes |
|---|---|
| All N members participate, MPC completes, bit is computed | Joint proof envelope with bit and N |
| Any member refuses or fails to participate | Silent-204 per E162; structurally indistinguishable from "no session was opened" |

There is no "we tried but `P_k` refused" message. The counterparty cannot distinguish:
- The group never received the query (e.g., the counterparty's pseudonym is not authorized).
- The group received the query but at least one member refused.
- The group received the query, all members tried, but MPC aborted (e.g., MASCOT preprocessing exhausted).

This is the **uniform-silent-204** posture from Witness E77, extended to N-party. It is the load-bearing privacy property.

### Refusal-invisibility *across* the group

A member's refusal must not leak to other members. The protocol uses **timed rendezvous**: each member commits to participate by a deadline `T_init + Δ` (default Δ = 30 s); if any member has not committed by then, the coordinator aborts the session for all members. The abort message contains no member identity. Each non-refusing member sees only `session_aborted { sid, reason: timeout }`. They cannot tell whether the refusal was deliberate or networking-induced.

In the limit, a malicious coordinator could try to extract refusal information by selectively delaying members. This is mitigated by (a) rotating the coordinator role per session, (b) including the abort timestamp in each member's chain so post-hoc analysis can detect coordinator misbehavior, and (c) the DERB audit interface per E129.

---

## Counterparty Disclosure Flow

### 7.1 Counterparty request

A counterparty C wishing to query the group's consensus emits a request to the group's known endpoint (which forwards to the rotating coordinator):
```
{
  consensus_request_id,
  predicate_id,
  group_pseudonym_v,         // C's view of the group's pseudonym
  window: { start, end },
  freshness_nonce,           // E155
  counterparty_pubkey_for_response,
  request_ts
}
```

### 7.2 Group authorization check (each member, locally)

Each member, on receiving the forwarded request, runs:
1. **Counterparty class lookup** (per E158): is this counterparty's class permitted to receive this predicate? If no, default-deny (E167 if anonymous).
2. **Per-counterparty consent** (per E159): has the principal explicitly authorized this counterparty?
3. **Window check**: does the requested window match the principal's policy?
4. **Predicate determinism harness** (per E150): does the predicate currently evaluate stably?

If any check fails, the member refuses (and the session aborts per §5).

### 7.3 Session record (each member's local chain)

Whether the session completes or aborts, each participating member appends:
```
{
  kind: "group_consensus_session",
  sid,
  group_id,
  predicate_id,
  window,
  counterparty_pseudonym_for_us,
  outcome: "completed" | "aborted_timeout" | "refused_by_me" | "refused_by_other",
  bit_disclosed_to_counterparty: true | false,
  // If completed:
  C_i, π_i^wf, my_share_of_C_⋂,
  // Always:
  signed_by_master_key
}
```
This is local-only; it is **not** broadcast to the counterparty or to other group members. It is the principal's own audit trail per E129.

### 7.4 Counterparty response envelope

If the session completes, the coordinator sends to C:
```
{
  consensus_response_id,
  predicate_id,
  bit: 0 or 1,                    // the bit b_⋂
  N,                              // group size
  group_pseudonym_v,
  window: { start, end },
  C_⋂,                            // joint commitment
  π_⋂,                            // joint Σ-proof
  opening_proof,                  // §6.5
  σ_⋂,                            // joint signature under K_G
  freshness_nonce_response,
  ts_response
}
```
If the session aborts: the coordinator sends a 204-shaped response per E162. Indistinguishable from "no session was opened".

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

### What is intentionally NOT private

- **The bit `b_⋂`.** This is the whole point of the disclosure.
- **The predicate ID.** The counterparty has to know what was attested.
- **The group size N.** Deliberate disclosure decision (see Rationale).
- **The collective pseudonym for this counterparty.** Required so the counterparty can verify the signature.
- **The window.** Required for the counterparty to judge freshness.

---

## Alternatives Considered

### A1. Trusted-aggregator design
A trusted aggregator collects each member's bit and outputs the AND. Rejected: collapses the principal-protective inversion (the aggregator sees all bits) and creates a single point of compromise. The whole reason for E149 is to avoid this.

### A2. Pairwise composition (chain of E148 character_compare)
Run E148 character_compare(p, P_2) between P_1 and P_2 to get a joint bit, then run E148 between that bit and P_3, etc. Rejected for two reasons: (a) the chain leaks ordering and intermediate bits to participants (P_2 learns the (P_1, P_2) bit before P_3 contributes); (b) the resulting proof is N-1 chained Σ-proofs, harder to verify and harder to make rigorously zero-knowledge across the chain. The MPC composition is cleaner.

### A3. Boolean garbled circuit per pair, hierarchical
Build a tree of pairwise garbled-circuit AND gates. Rejected: garbled circuits are 2-party; extending to N-party requires elaborate cut-and-choose; bandwidth scales as N · circuit size; loses the direct Pedersen composition.

### A4. BGW with honest-majority
BGW gives nice round complexity but assumes honest-majority (`> 2N/3` honest). Rejected: our threat model assumes any-one-member-malicious, and we want to tolerate up to N-1 malicious. SPDZ handles this; BGW does not.

### A5. Plain Σ-protocol for AND without MPC (each member separately discloses their commitment to the counterparty; counterparty checks Σ-product)
Rejected: this is *not* a single-bit disclosure. The counterparty would receive N separate commitments and N proofs and would learn (a) N's membership in the proof set (which is fine), (b) but also that all of them came from individual members rather than a joint computation — and could correlate the individual commitments across sessions to reconstruct partial group structure. The whole point of MPC is that the counterparty learns the AND as a *single* committed bit, not as N separately disclosed bits AND'd by the verifier.

### A6. Hide N via Bulletproofs range-proof
Bulletproofs (per Witness E45) could let us prove `N ≥ 3` without revealing exact N. Considered. Deferred to v1 as `character_consensus_with_hidden_N`. v0 reveals N because reveal-N is the semantically clearer claim for the counterparty.

---

## Migration Path

### v0 (this document, 2026)
- SPDZ + MASCOT preprocessing.
- N ≤ 16 (latency budget; see §13 open problems).
- N-of-N unanimity only.
- Reveal N.
- Ristretto255 Pedersen, Σ-proof system.
- One mandatory DERB review per group formation (E134 generalized).

### v0.1
- Production preprocessing service (per [Mirror 59](everests/mirror_59_zk_proof_mpc_correctness.md) extended to N-party).
- Field-tested with one real group (likely the founding ZKAC research collective per E231).

### v1 (post-2026)
- **Threshold variant** `character_consensus_threshold(p, group, k_of_N)` — proves at least `k` of `N` members evaluate true. Requires Bulletproofs range proof on the share-count (uses Witness E45). Open question (§13): does revealing "exactly 8 of 10" vs. "at least 8 of 10" leak too much? v1 default is "at least k of N" with `k` revealed and exact count hidden.
- **Hidden-N variant** `character_consensus_hidden_N(p, group, bounds)` — proves N is in `[N_min, N_max]` without revealing exact N. Uses Bulletproofs.
- **Disjoint-evidence variant** — proves all members evaluate true and their evidence pools are disjoint (no shared evidence record reused across members). Useful for assertions like "10 independent witnesses each attest." Requires set-intersection MPC over evidence record hashes; significantly more expensive; deferred.

### v2 (long horizon)
- **Overdrive or Turbospeedz preprocessing** for ~3× bandwidth improvement.
- **Post-quantum migration** (per E96): switch Pedersen → lattice-based commitment (Module-LWE) and Σ-protocols → lattice-based Σ-protocols. Joint with witness PQ migration.
- **Group sizes up to N=64** with parallelized preprocessing.

---

## Design Implications & Connections

### Composes with...

- **[Everest 117](everest_117_values_registry.md):** Local predicate evaluation per member draws on the evidence-aggregation primitive. The committed per-member bit `b_i` is the output of an E117 aggregation; the joint AND extends this to the group.
- **Everest 131 (predicate language v0):** The `predicate_id` parameter is a content-addressed E131/E132 identifier.
- **Everest 145 (predicate composition AND/OR):** This predicate can itself be used as a sub-predicate inside an E145 composition. E.g., `character_consensus(p, G) AND character_window_query(q, P_self)` lets a principal combine a group claim with a personal claim in a single proof.
- **Everest 147 (time-bounded predicate):** The `window` parameter composes with E147; the group's consensus is *over the same window* for all members (a chosen-window for each member, with the constraint that they intersect).
- **[Everest 148](#) (`character_compare` 2-principal):** Direct prerequisite; E149 is the N-party generalization. The MPC scheme generalizes the 2-party scheme used by E148.
- **Everest 150 (predicate determinism harness):** Each member's local evaluation must pass the determinism check, else they cannot enter the MPC.
- **Everest 155 (Compass replay defense):** Each consensus session carries a fresh nonce; replays produce no signal per E155.
- **Everest 156 (Compass selective disclosure):** The counterparty can request consensus on a subset of predicates from a known group, with one selective-disclosure envelope.
- **Everest 158 (counterparty-class authorization):** Each member's authorization check is per-counterparty per E158.
- **Everest 159 (per-counterparty consent):** Member-level consent overrides.
- **Everest 162 (disclosure-of-non-disclosure):** Refusal is uniform-silent-204; the load-bearing privacy property of §5.
- **Everest 163 (no push-mode for Compass):** Consensus is pull-mode only; the counterparty asks, the group responds; the group does not volunteer.
- **Everest 167 (anonymous strict-default-deny):** Consensus to anonymous counterparties is strictly opt-in per member.
- **Witness [Everest 45](everest_45_zk_range_proof.md) (Bulletproofs):** Used by v1 threshold variants; not in v0 critical path.
- **Witness [Everest 70](everest_70_replay_defense.md):** Replay-defense pattern shared with Compass E155.
- **Witness E77 (uniform-silent-204):** The privacy posture extends to N-party here.
- **Mirror [Everest 58](everests/mirror_58_mpc_intersection_bits.md):** The 2-party OT-extension MPC for AND-of-bits. E149 generalizes the same conceptual primitive to N parties via SPDZ.
- **Mirror Everest 59 (ZK proof of MPC correctness):** The proof-of-correct-MPC pattern, extended to N-party via the SPDZ-to-Σ bridge in §6.4.
- **ZKAC Everest 87 (BLS threshold signatures):** The joint signature `σ_⋂` is a BLS threshold-signature variant under `K_G`. v0 uses an aggregate Schnorr (FROST-style); v1 may upgrade to BLS for batch-verification efficiency.
- **ZKAC Everest 90 (VSS):** Used at group formation to distribute `K_G`.

### Use cases (concrete)

1. **Research-group integrity claim.** A four-person AI-safety research collective wishes to attest to a funder: "All of us evaluated `cwv.v0.honors_research_integrity_under_pressure` to true over the last 36 months." The funder receives one bit, one collective pseudonym, one window. The funder does not learn which evidence each researcher's vault holds — including, e.g., specific incidents of refusing to fudge results — only the aggregate bit. Each researcher's vault, identities, and individual evidence remain private.
2. **Professional-association attestation.** A small ethics-board of N=7 jointly attests `cwv.v0.peer_verified_competence` to a regulator. The regulator receives one bit; cannot derive which individual board members hold which credentials.
3. **Aligned-ZKAC coordination signal.** A group of N=12 ZKACs each evaluates `cwv.v0.prosocial_coordination_consistent` to true. The collective bit is a shared signal — a known capacity to coordinate prosocially — without each ZKAC revealing its internal records.
4. **Refused-coercion attestation.** A research team of N=5 jointly attests `cwv.v0.refused_to_falsify_under_external_pressure` over a window. None of them needs to identify the pressuring party; the collective bit is the claim.

### What this predicate does NOT do

- **It does not enforce internal group governance.** Group members may agree or disagree on values internally; the predicate evaluates the *AND* of independent assessments. Members who would evaluate false simply refuse (and the session aborts invisibly).
- **It does not provide reputational scoring.** The output is a bit, not a score, by design. Counterparties seeking a score are routed to E126 / E130 alignment-metric primitives.
- **It does not bind the group beyond the session.** The bit is for *this window*. Future windows require fresh evaluation. There is no persistent group attestation.
- **It does not authorize the counterparty to act on the bit in any specific way.** The principal-protective inversion holds: the counterparty receives a single bit; what the counterparty does with it is governed by E141 (alignment disclosure semantics) and E156 (selective disclosure).

---

## Open Questions

1. **MPC efficiency at group sizes > 10.** SPDZ online phase is ~`N-1` rounds for chained AND; bandwidth is `O(N²)` for share broadcasts. We project N=16 is achievable on consumer laptops in <2 seconds online with offline preprocessing done overnight. Beyond N=16, parallelization (per Mirror E57 batch OT, extended to N-party) is needed. **Action item:** empirical study at N ∈ {4, 8, 16, 32} on M-series hardware before v1.

2. **Latency vs. group-size trade-off.** Preprocessing scales linearly in number of AND gates needed, and quadratic in N for the MAC distribution. At N=32, MASCOT preprocessing may take >1 hour per session worth of triples. Open question: can preprocessing be amortized across many sessions safely? Yes in principle (SPDZ preprocessing is independent of inputs) but each amortization creates a fresh attack surface (stale-triple replay). Defer to v1 design.

3. **Retroactive evidence contradiction.** If member `P_k`'s evidence is later contradicted (e.g., a new on-chain record per E119 counter-evidence makes the predicate retroactively false for `P_k`), does the *prior* consensus proof retroactively become misleading? **Decision:** the proof is **a claim about the state of the evidence pools at the proof's freshness window**, not an eternal truth. Counterparties relying on consensus proofs must respect the window. We add an explicit `window_end_ts` to the response envelope (§7.4). This is consistent with the Witness chain-state semantics. **Open question:** should the protocol provide an *invalidation channel* through which the group can voluntarily withdraw a prior consensus claim if a member's evidence is later contradicted? Probably yes in v1 (per E163 retraction discussions); we flag it as `character_consensus_retraction` future work.

4. **Honest-input verification.** The protocol verifies *honest MPC computation* but not *honest local predicate evaluation*. A member who lies about their `b_i` is a sociological failure, not a cryptographic one. Defense is E121 (evidence honesty) + chain transparency. **Open question:** can the protocol add a *consistency check* between the member's `b_i` and a sample of their chain evidence (e.g., zero-knowledge consistency proof per E122 anchoring)? Probably yes, at the cost of more compute per session. Tracked as `character_consensus_with_evidence_audit` for v1.

5. **Coordinator role in adversarial conditions.** A malicious coordinator (rotating per session, but at any one session there is one) can selectively abort sessions to leak refusal patterns. We mitigate via (a) coordinator rotation, (b) on-chain abort records audit-able by DERB, (c) member-side timeout discipline. **Open question:** can the coordinator be eliminated entirely via a fully peer-to-peer rendezvous protocol? Likely yes via leader-election-free MPC variants; deferred to v1.

6. **Member churn during in-flight session.** If a member's device crashes mid-session, the session aborts. **Open question:** should the protocol support a `graceful retry with same group` mode? Possibly yes; the privacy concern is that retries could leak member-state to a stalking counterparty. Flag for v1.

7. **Composition with ZKAC formation (E231).** Founding ZKACs almost certainly want to use `character_consensus` for their own attestations. The group descriptor must be content-addressable in a way that is compatible with the ZKAC formation chain. Cross-design work with E231 needed.

8. **Formal security proof.** The SPDZ-to-Σ bridge in §6.4 is described constructively; a full UC-security proof (per Canetti's framework) requires composition lemmas across SPDZ's existing proof and Σ-protocol's standard analysis. This is a research-grade open item. Tracked as `character_consensus_uc_proof`; defer to academic collaboration via E294 paper publication.

---

## Why This Matters

The principal-protective inversion — principal narrates, principal authorizes, counterparty receives bits not scores, principal is the strongest party — historically fails at the collective scale. Representatives speak for and silently see-into the group. Aggregators receive everyone's signals. Public rosters trade all privacy for one bit. `character_consensus` keeps the inversion intact at group scale: each principal evaluates locally, commits a bit, participates in an MPC that learns only the AND. The counterparty receives one bit, one signature, one collective pseudonym. Members who would vote no refuse invisibly. Repeated queries meet fresh randomness and rate-limited rejection.

This is one of the hardest summits in Compass because it requires composing four primitives correctly (Pedersen commitments, Σ-protocols, SPDZ secret-sharing, MAC-based integrity) and because the privacy properties — refusal-invisibility chief among them — are operationally fragile. The cryptographic skeleton here is at the level a cryptographer-engineer pair can use to begin implementation; the formal UC-security proof and the production preprocessing service are research-grade follow-ups (§13).

At the human scale: a research team can stand by its collective integrity without doxxing any researcher's evidence; a clinical team can attest competence without exposing individual practitioners; an aligned cohort of ZKACs can signal coordinated prosocial intent without surrendering operational records. The collective speaks one bit. The members keep their evidence. The counterparty learns what they need to learn, nothing more.

---

— Calm, 2026-05-20
