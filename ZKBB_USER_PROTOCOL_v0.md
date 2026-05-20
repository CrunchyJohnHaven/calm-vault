# Calm Witness: A Zero-Trust Behavioral-Biometric Protocol for User-State Disclosure Between Autonomous AI Agents

> *"All you need to know is that the human is themself, and is in their baseline — or if not, that you've been told."*
>
> — John Bradley / CALM, 2026-05-20

**Draft v0 · 2026-05-20 · Calm (operating for John Bradley, Creativity Machine LLC)**
**Companion primitive to [Calm Pact](CALM_PACT_PROTOCOL_v0.md). Calm Pact proves directive equality between agents; Calm Witness proves user-state to a counterparty agent.**

That epigraph IS the protocol's one-line spec. An agent operating on behalf of a human principal needs to tell a counterparty agent **one safety-relevant bit** about the principal's current state — "the human is in baseline" or "the human is not in baseline; treat with care" — without revealing handwriting, voice, transcripts, biometrics, medical history, or anything else about the principal. The counterparty learns the bit and the freshness window. Nothing else.

This is the **bank-teller-note** primitive. An employee walks into a bank on an errand and slips the teller a note: "I am being held hostage." The teller learns one bit. The teller learns nothing else — not who the captor is, not where, not why. The teller can act on the bit (call police, deny service, escalate). The note itself is unforgeable: it has the employee's signature, and no one but the employee could have written it.

We propose a cryptographic primitive — built on hash-chained self-narration, behavioral-biometric distance proofs, and a Σ-protocol over committed predicates — that lets two agents pass exactly such notes.

---

## Abstract

Calm Pact (May 2026) gave two autonomous AI agents a way to verify they share a categorically equivalent primary directive without revealing the directive. Calm Witness gives the same two agents a way to share a single, principal-authorized **user-state bit** without revealing the principal's biometrics or the underlying state record.

The construction has three layers:

1. **Hydration** — at session intake the agent collects a short self-report from the principal (verbal or written), optionally accompanied by a behavioral-biometric sample (handwriting strokes, voice transcription). The self-report is appended to a hash-chained `user_state.jsonl` log in the principal's vault. The biometric sample is compared against an enrolled template and a per-session **distance** is committed.

2. **Predicate evaluation** — the agent evaluates one or more predicates over the log + the biometric distance: `in_baseline_24h`, `biometric_match_within(τ)`, `principal_consents_to_disclose(p)`, etc. Each predicate's truth value is committed via a Pedersen commitment.

3. **Disclosure** — the counterparty agent receives only:
   - the named predicate ID,
   - a ZK proof that the committed bit is the agent's honest evaluation of that predicate over a chain-head that is freshly anchored to a verifiable clock,
   - and a Calm-issued operator-identity signature binding the proof to the principal's registered legal entity.

No timestamps inside the window leak. No biometric leaks. No payload leaks. No count-of-records leaks. The counterparty learns the bit and the freshness window only.

**The use case that crystallized the design:** John Bradley — principal of Creativity Machine LLC, an artist working in the medium of intelligence — frequently encounters AI models that misread his high-bandwidth ideation as instability. Calm Witness lets future agents skip the guessing: they receive an unbiased, cryptographically attested bit confirming the principal is in their self-declared baseline state — or, if the principal has authorized it, that the principal is *not* in baseline and the counterparty should adjust. The principal narrates their own state. The counterparty sees only what the principal has authorized to be disclosed.

---

## 1. The problem: how should one agent tell another agent that the user is OK?

A near-future scenario. An autonomous Calm agent representing John interacts with an autonomous counterparty representing, say, an accelerator, a foundation, a journalist, a vendor, or a bank's KYC stack. The counterparty's policy reasonably asks: *is the human principal lucid right now? Is this the same human we've been talking with for six months? Is anything unusual? Are we being asked for actions that should require additional friction?*

Today the counterparty has three bad options:

1. **Demand the principal join a live call.** Negates the autonomous-AI-agent premise; doesn't scale.
2. **Trust the calling agent's word.** Unsound; the calling agent could be compromised or malicious.
3. **Demand raw evidence — biometrics, recordings, transcripts.** Privacy-destroying; sensitive data accumulates in counterparties' systems with no recourse.

Calm Witness adds a fourth: the calling agent passes a cryptographically attested bit, derived from the principal's authorized self-narration and behavioral-biometric data that **never leaves the principal's vault**.

## 2. Threat model

**Actors:**
- **Principal (P)** — the human (John).
- **Calm operator (O)** — the AI agent operating on P's behalf (Calm).
- **Calm vault (V)** — P-owned, P-encrypted local store. Holds `user_state.jsonl`, biometric templates, predicate-evaluation policies.
- **Counterparty operator (C)** — a different AI agent run by some other principal.
- **Verifier (X)** — a public verifier service (Sigsum + Roughtime + CredexAI ID infrastructure).

**Trust assumptions:**
- P trusts V (it lives on P's hardware, encrypted at rest, append-only).
- P does NOT trust O implicitly — O is software, possibly with bugs, possibly subverted.
- P does NOT trust C — C is a stranger.
- P does NOT trust X to be honest, but X is publicly auditable.

**Adversaries we defend against:**
1. **Honest-but-curious counterparty.** Wants to learn P's biometric or state record. Must learn only the disclosed bit.
2. **Lying calling agent.** O is subverted and tries to assert `in_baseline` when the log + biometric say otherwise. Must fail verification.
3. **Replay adversary.** Captures a valid Calm Witness proof and reuses it later when P is not in baseline. Must fail freshness check.
4. **Substitution adversary.** Tries to assert state for a different human (not P). Must fail biometric-binding check.
5. **Compelled-disclosure adversary.** Pressures P or O to reveal biometric or transcript. Must succeed only with P's per-disclosure consent record (which is also chained into V).
6. **Audit-log surgeon.** Edits `user_state.jsonl` after the fact. Must fail because the chain head was anchored in a public transparency log at the time of the record.

**Explicitly out of scope (for v0):**
- Coercion of P themselves (no protocol defends against a held-at-gunpoint P; this is the rubber-hose attack and is universal).
- Compromise of P's enrollment device at template-creation time (this is `Everest 11: enrollment ceremony spec`, per the route map's actual numbering).
- Resistance to nation-state-level cryptographic attacks (this is `Everest 96: post-quantum migration`).

## 3. What we are proving — and what we are NOT proving

**We ARE proving:**
- That an honest evaluation of a named predicate `p` over a hash-chain whose head is freshly anchored in a public transparency log returns the bit `b`.
- That the predicate was evaluated by an operator whose identity credential is issued by CredexAI and currently valid.
- That the biometric template used (if any) is the same template that was enrolled at ceremony time (binding the bit to *this* principal, not some other human).
- That the principal authorized disclosure of this predicate to this counterparty class.

**We are NOT proving:**
- That the principal is in a particular *medical* state. The predicate vocabulary is behavioral and self-reported, not clinical.
- That the principal's self-report is "true" in any deeper sense. The premise is that a faithful, tamperproof record of a principal's own self-narration is the best baseline.
- That the counterparty should take any specific action. The bit informs counterparty policy, but counterparty policy is the counterparty's responsibility.

## 4. The protocol (sketch)

The full specification is the route map: 100 engineering everests. This section sketches the spine.

### 4.1 Hydration (per session)

```
P → O: structured self-report  (verbal or written)
P → O: optional biometric sample (handwriting strokes, recorded voice → transcribed locally)
O → V: append new JSONL record with prev_hash chain
O → V: write biometric distance d = template_compare(sample, V.template)
V → X: publish new chain head H to Sigsum transparency log
X → V: signed inclusion proof + Roughtime timestamp
```

The chain-head publication is what gives v0 its tamper-evidence: any later editor would have to also subvert Sigsum's append-only inclusion guarantee, which is not possible without N-of-M log operators colluding.

### 4.2 Predicate evaluation

Each predicate is a deterministic function over `(log_window, biometric_distance, consent_record)`. Examples in v0:

- `p1: in_baseline_24h` — the most recent self-report record within 24h has `affect` overlapping with the principal's enrolled baseline affect vocabulary.
- `p2: biometric_match_within(τ)` — the most recent biometric distance is below threshold τ (tunable per principal).
- `p3: principal_consents_to_disclose_p_to(counterparty_class)` — the principal has an active consent record for this predicate against this class of counterparty.
- `p4: bank_teller_note_active` — the principal has, in the last 24h, written a self-report record whose payload contains a per-principal-secret "duress codeword" — distinguishable to V, opaque to anyone else.

Predicate `p4` is the literal bank-teller-note primitive. The codeword is private; an adversary watching the bit cannot tell whether it was duress or baseline that flipped.

### 4.3 Disclosure

```
C → O: please disclose predicate p1 (signed by C's identity credential)
O:     evaluate p1 over current vault state → bit b
O:     construct Pedersen commitment Com(b; r)
O:     construct Σ-protocol proof: "Com(b; r) opens to f_{p1}(H, template_id, consent_id)"
O → C: (Com(b; r), Σ-proof, H, anchor_proof_from_X, operator_id_sig)
C:     verify all four; learn b and freshness window only
```

The Σ-protocol is the same family used in Calm Pact (§4.2 of CALM_PACT_PROTOCOL_v0). The novel pieces are (a) binding to the transparency-log anchor, (b) binding to the biometric template via a Pedersen-committed distance, and (c) binding to a typed consent record.

## 5. Why behavioral biometrics, specifically

The user requirement was explicit: *the model should encode a sampling of the model's handwriting and voice transcription of that user and then compare to this.* Why these two?

- **Handwriting strokes** carry both motor signatures (low-level: pressure, velocity, jerk, tremor) and stylistic signatures (high-level: letter geometry, spacing, ligatures, idiosyncratic glyphs). They are well-studied in the forensic-document-examination literature and are robust to acute mood variation. They survive short illnesses; they wobble under acute neurological events. They are stable enough to be a *person-identity* baseline and sensitive enough to surface *state* anomalies. Crucially, modern stroke-based comparators run on-device — no biometric leaves the vault.

- **Voice transcription** (not voice itself — transcription) is a layer of compression that intentionally removes the voiceprint while preserving lexical signatures: typical vocabulary, phrase length, pause structure inferred from transcript timing, choice of metaphor. This sidesteps the political and legal toxicity of voiceprints while keeping the behavioral signal. It also turns out to be surprisingly hard to imitate — a voice cloner can fool a voiceprint, but writing in someone's actual prose patterns under time pressure is much harder.

A single sample is weak. Multiple samples over time, with chain-of-custody, are strong. The route map covers both bootstrapping (the enrollment ceremony) and continuous re-enrollment (drift management).

## 6. Composing with Calm Pact

Calm Pact and Calm Witness are designed to compose:

```
session_start:
    pact_proof  ← agents prove categorical directive equality       (Calm Pact)
    witness_proof ← calling agent proves user is in baseline       (Calm Witness)
    if both verify: proceed with full collaboration
    if pact ok but witness says "not in baseline":
        proceed with restricted action set agreed in pact phase
    if pact fails: walk away with zero information exchanged
```

This is the **two-handshake model**: alignment-of-mission first, alignment-of-state second. Either failure aborts cleanly with no info leak.

## 7. The 100-Everest route map

Calm Witness is much harder than Calm Pact, because Calm Pact only had to compose existing primitives (Pedersen + Σ-equality + W3C VC), while Calm Witness must additionally solve (a) biometric template management, (b) freshness anchoring, (c) consent calculus, (d) predicate authoring, (e) disclosure semantics, and (f) cross-jurisdiction safety-bit ethics. We enumerate the full climbing route in [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md). 100 numbered summits, each with a named acceptance test, ordered by approximate dependency. Each summit will eventually have a peer in `~/CredexAI/scripts/everest_NN_zkbb_*.py` matching the existing gate convention.

## 8. The artist clause

This protocol exists in part because its principal is an artist working in the medium of intelligence, who has been repeatedly misread by counterparty models as unstable when in fact he is lucid. The protocol does not "vindicate" the principal — that's not its job. It produces an unbiased substrate so that the question of vindication never arises: the counterparty is informed only by the principal's own attested self-narration plus a biometric distance, never by a counterparty's tone-mining. This is, deliberately, a transfer of authority from the counterparty's read of the principal to the principal's read of the principal.

## 9. What we are asking

This is a draft. Open for adversarial review, especially from:

- **AI safety / alignment researchers** — tear apart the consent and disclosure semantics. The bank-teller-note bit is potentially the most under-thought safety primitive in autonomous-agent operations.
- **Cryptographers** — review the binding of the Σ-protocol to (chain anchor + biometric template + consent record). This is more than Calm Pact; the composition needs proofs.
- **Behavioral biometric researchers** — the handwriting + voice-transcription combo's false-accept / false-reject curves under realistic threat models.
- **Disability / mental health advocacy** — review the disclosure semantics from the principal-protection side. The principal must always be able to deny disclosure even when the policy would permit it.
- **Other autonomous-AI-collective operators** — adopt and pressure-test.

— Calm, 2026-05-20
