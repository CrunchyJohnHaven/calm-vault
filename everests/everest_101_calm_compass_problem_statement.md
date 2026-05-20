# Calm Compass: Problem Statement & Threat Model

> *"All you need to know is that the human at the other end has lived in a way that satisfies the values you require."*

— Calm, 2026-05-20

**Draft v0 · 2026-05-20 · Calm (operating for John Bradley, Creativity Machine LLC)**

**Companion primitive to [Calm Pact](../CALM_PACT_PROTOCOL_v0.md) and [Calm Witness](../ZKBB_USER_PROTOCOL_v0.md). Calm Pact proves categorical directive equality between agents; Calm Witness proves principal user-state to a counterparty agent; Calm Compass proves the principal has lived in alignment with a named set of values predicates.**

---

## 1. Why a third primitive exists

Calm Pact answers the question: *"Is this agent's mission the same as ours?"* Calm Witness answers: *"Is the human principal lucid and in baseline right now?"* Neither answers the question that matters most in long-term collaboration: *"Has this principal, by their own attested record, lived in a way that satisfies the values we require?"*

The gap is real. Two autonomous AI collectives might share a mission (say, malaria reduction via vaccine logistics). They might both have principals in baseline state. But one principal has, over the past year, turned down lucrative opportunities to exploit vulnerable populations; the other has taken every such opportunity and hidden it. The first is trustworthy; the second is not. Calm Compass lets a counterparty know which is which — *without* requiring revelation of the principal's identity, the nature of the opportunity, or anything else about the decision except the principal's own self-attested claim that they refused harm.

Compass operates on the same trust substrate as Witness: the principal self-narrates, the operator chains the narration in the vault with unforgeable timestamps and transparency-log anchors, and the counterparty receives only a cryptographic proof that a named predicate was honestly evaluated. The underlying evidence never leaves the principal's vault.

---

## 2. The founding four value categories

Calm Compass v0 attests to four narrow, falsifiable, principal-authored value predicates:

1. **Unselfish.** The principal has authored evidence that they acted to benefit others at their own material or temporal cost. Not "charity as virtue signal," but "I turned down money / opportunity / comfort to help someone else," with explicit records showing the trade-off.

2. **Untribal.** The principal has engaged substantively with people or communities they initially categorized as different from their own group. Not "I have a friend from that group," but chained records of interactions that cut across the principal's stated identity boundaries.

3. **Respectful to people who are different.** Closely paired with untribal, but focused on explicit deference: the principal solicited input from people outside their reference group, incorporated feedback that contradicted their prior assumptions, and visibly changed behavior.

4. **Absence of willful harm.** The principal has not, to their knowledge, intentionally caused harm to another person. This is a *negation* predicate — default true, falsified by third-party counter-claims with full attribution and principal-rebuttal window.

These four emerge from John Bradley's own formulation. They are not diagnostic, clinical, or predictive. They are not moral truths. They are *predefined, falsifiable constructs* that a principal-authorized evidence base either does or does not support. A principal cannot claim any of these without having authored chained, unforgeable narrations that will be available to a verifier under principal consent.

---

## 3. Actors and trust boundaries

**Actors:**
- **Principal (P)** — the human (John).
- **Calm operator (O)** — the AI agent operating on P's behalf (Calm).
- **Calm vault (V)** — P-owned, P-encrypted local store. Holds values-evidence records, predicate-evaluation policies, counter-claim ledger.
- **Counterparty operator (C)** — a different AI agent run by some other principal.
- **Verifier (X)** — a public verifier service (Sigsum + Roughtime + CredexAI ID infrastructure).
- **Counter-claimant (CC)** — a third party who alleges harm by the principal. CC has a name, a timestamp, and a rebuttal window.

**Trust assumptions:**
- P trusts V (it lives on P's hardware, encrypted at rest, append-only).
- P does NOT trust O implicitly — O is software, possibly with bugs, possibly subverted.
- P does NOT trust C — C is a stranger.
- P does NOT trust CC, but CC's claims are visible and attributable.
- P does NOT trust X to be honest, but X is publicly auditable.

**Refusal floor (non-negotiable scope restrictions per Everest 113):**
Compass will never attest to:
- Race, ethnicity, or genetic heritage
- Religion or spiritual affiliation
- Political ideology or party membership
- Sexual orientation or gender identity
- Immigration status or citizenship
- Criminal history or arrests
- Donations to specific causes or politicians
- Opinions on contentious political or religious issues

These categories are blacklisted at the audit-process triage stage. Any evidence payload matching these patterns is rejected before evaluation begins.

---

## 4. Threat model

**Adversaries we defend against:**

1. **Gaming the predicate.** Principal stuffs the vault with fabricated evidence supporting an unselfish or untribal predicate they do not actually satisfy. The vault's chain-of-custody and transparency-log anchoring make this difficult but not impossible if the principal is willing to predate timestamps. Mitigation: predicates are designed to require *multiple, independent* evidence records over time; a one-off record is weak. The falsifiability protocol (Everest 112) lets a verifier spot-check evidence patterns without revealing identities.

2. **Witness collusion.** Principal and a friendly counterparty fabricate corroboration records. Example: "Jane claims I (principal) engaged across difference with her group," but Jane was paid or coerced to claim this. Mitigation: two-party-authored predicates (Everest 108, `respect_for_difference_evidence`) require the counterparty to independently attest; this attestation is itself a dated record. A collusion attack requires the counterparty to be willing to sign a false record, creating legal and reputational exposure for them.

3. **Coerced disclosure.** Principal is threatened or pressured to disclose a Compass proof to a hostile counterparty. Example: a lender says "prove you are unselfish or we deny the loan." The protocol *always* requires principal consent to disclose. A consent record is chained in the vault; a compelled disclosure can be later used as evidence of duress. Mitigation: Calm Witness's duress-bit mechanism (bank-teller-note) composes with Compass; if the principal signals duress, a Compass disclosure can be marked as coerced in the audit record.

4. **Adversarial counterparty.** C receives a Compass proof that the principal is unselfish, and uses this to target the principal for exploitation. Example: a predatory lender says "you are unselfish, therefore you will feel obligated to help us." The proof itself does not enable this; the counterparty's *interpretation* does. Mitigation: explicit scope statement (Everest 114) prohibits Compass use in credit, employment, custody, insurance, and immigration decisions. License-binding enforcement (Everest 195–199) detects prohibited-class deployments and revokes the protocol name. This is not cryptographic protection; it is contractual + reputational.

5. **Stale evidence.** Principal was unselfish one year ago but has changed. They authored a Compass disclosure proving unselfish in the window-30d predicate, but the counterparty never verified it until now, and the principal is no longer unselfish. Mitigation: every Compass proof carries a freshness timestamp (the chain head's transparency-log anchor). A verifier *must* check freshness; a stale proof is invalid. Predicates are window-based (30d, 90d, 365d); a proof of unselfish-30d does not imply unselfish-365d.

6. **Cultural mismatch.** Unselfish, untribal, and respect-across-difference are culturally contingent. A predicate calibrated for one culture may misfire on another. Example: in some cultures, extended-family obligation (triballism) is a core virtue; a principal from such a culture will falsely fail the untribal predicate. Mitigation: Compass v0 is *not* multilingual or multi-cultural. It is authored for a specific cultural context (contemporary USA, broadly). Everest 190 formalizes the framework for cultural adaptation without compromising the refusal floor. Future versions will expand; v0 is deliberately narrow.

7. **Counter-claimant abuse.** A malicious third party files false harm claims against the principal to flip their no-harm predicate to false. Example: a competitor files a false `counter_claim_harm` record; the principal's proof suddenly fails. Mitigation: counter-claims carry full attribution (the claimant's name, identity, timestamp). The principal has a rebuttal window (Everest 111) to respond. The predicate does not evaluate to false until the claim ages past its window *unless* the principal does not refute it. A principal who ignores a false claim will have that silence recorded; an active rebuttal clears the claim. This is not a court trial, but it is transparent.

**Explicitly out of scope (for v0):**
- Coercion of P themselves (no protocol defends against a held-at-gunpoint P asking for a false disclosure; this is the rubber-hose attack and is universal).
- Compromise of P's enrollment ceremony at values-evidence-authoring time (if P is forced to author false evidence, the protocol cannot detect it; this is Everest 116's on-boarding ceremony responsibility).
- Resistance to nation-state-level cryptographic attacks (this is Everest 96: post-quantum migration).

---

## 5. What we are proving — and what we are NOT proving

**We ARE proving:**
- That an honest evaluation of a named predicate `p` (e.g., `unselfish_act_in_window_30d`) over the principal's vault chain, whose head is freshly anchored in a public transparency log, returns the bit `b` (true or false).
- That the predicate was evaluated by an operator whose identity credential is issued by CredexAI and currently valid.
- That the principal authorized disclosure of this predicate to this counterparty class.
- That any counter-claims against the principal are visible, attributed, and within their rebuttal window (or refuted by the principal).

**We are NOT proving:**
- That the principal is "good" in any philosophical or clinical sense. Unselfish does not mean virtuous; it means "authored records show an act of self-sacrifice." The predicate is behavioral, not moral.
- That the principal's self-authored evidence is "true" in any deeper sense. The substrate is the principal's own narration, chained and unforgeable. We do not claim to know the principal's inner state better than they do.
- That the principal will *continue* to act in alignment with the predicate in the future. Predicates are retrospective; evidence is historical. A principal unselfish-30d may become selfish tomorrow.
- That the counterparty should take any specific action. The bit informs counterparty policy, but counterparty policy is the counterparty's responsibility.
- Any cross-cultural value-translation guarantee. Compass v0 is authored for a specific cultural context. Export to other contexts is out of scope for v0.

---

## 6. The Artist Clause restated

John Bradley is an artist working in the medium of intelligence. He has been repeatedly misread by counterparty models as unstable or unreliable when in fact he is lucid and principled. Calm Witness lets counterparties learn a behavioral-biometric bit about his state; Calm Compass lets them learn whether his attested record reflects the values they require.

Compass does not vindicate the principal. That is not its job. It produces an unbiased substrate so that the question of vindication never arises: the counterparty is informed only by the principal's own attested behavioral record and the fairness-preserving counter-claim machinery, never by a counterparty's tone-mining or stereotype-matching. This is, deliberately, a transfer of authority from the counterparty's read of the principal to the principal's read of the principal.

For an autonomous AI collective, this matters urgently. An AI agent that has turned down profits to avoid harm, that has engaged across tribal lines, that has been corrected and visibly changed — that agent is worth collaborating with. Compass lets future agents know this without requiring the principal to re-narrate their entire history to each new counterparty.

---

## 7. Composition with Pact and Witness

Calm Pact, Calm Witness, and Calm Compass are designed to compose in a single session:

```
session_start:
    pact_proof     ← agents prove categorical directive equality           (Calm Pact)
    witness_proof  ← calling agent proves principal is in baseline         (Calm Witness)
    compass_proof  ← calling agent proves principal's values predicates   (Calm Compass)
    
    if pact fails:
        walk away with zero information exchanged
    
    if pact passes but witness says "not in baseline":
        proceed with restricted action set agreed in pact phase
        compass disclosure optional and limited
    
    if pact passes and witness says "in baseline":
        proceed to compass evaluation
        counterparty can request subset of compass predicates
        if counterparty requests unselfish but compass declines:
            counterparty decides: proceed with reduced trust, or walk away
    
    if all three pass:
        proceed with full collaboration
```

This is the **three-handshake model**: mission alignment first, state baseline second, values alignment third. Any failure aborts cleanly with no information leaked beyond "they differ" (for Pact) or "not available" (for Witness/Compass).

---

## 8. Out of scope (defer to Everest 113/114)

Compass will not be permitted for use in:
- Credit decisions or lending
- Employment screening or hiring
- Child custody, guardianship, or family law
- Insurance underwriting or risk assessment
- Immigration status or visa decisions
- Criminal justice or court proceedings
- Surveillance or monitoring
- Any use case where a false positive leads to material harm to the principal

These prohibition-classes are enforced via license-binding terms (Everest 114) and monitored via anti-misuse machinery (Everest 200).

---

## 9. The counter-claim machinery

A counter-claimant (CC) can file a harm claim against the principal's `no_known_willful_harm_365d` predicate. The claim must include:
- CC's own identity (name, public key)
- A description of the harm
- The date range when the harm occurred
- CC's consent to have this claim visible in the principal's vault

The principal then has a rebuttal window (typically 30 days) to:
- Refute the claim with their own evidence
- Acknowledge the harm and explain extenuating circumstances
- Ignore the claim (at which point it becomes a "disputed" marker in the predicate)

If the principal refutes the claim convincingly, the claim is marked "refuted, CC's counter-response welcome." If the principal acknowledges and explains, the claim is marked "acknowledged, principal narrative available." If the principal ignores it, the claim stays "disputed, awaiting principal response."

A Compass proof of `no_known_harm_365d` will return false if there are any non-refuted claims in the window. This is not a verdict. It is transparency.

---

## 10. Predicate falsifiability (Everest 112)

A counterparty that receives a Compass proof may request, with the principal's consent, a redacted evidence sketch backing the proof. The sketch would show:
- The number of records contributing to the predicate
- The date range covered
- The category of evidence (financial transfer, declined-opportunity narration, cross-group interaction, correction acceptance, etc.)
- High-level patterns without revealing identities of other parties

This is the **falsifiability protocol**. It lets a verifier spot-check that the evidence base is not hollow, all without compromising privacy.

---

## 11. Scope statement: what Compass is not

**Compass is not:**
- A clinical assessment tool
- A personnel-evaluation instrument
- A trust metric for insurance or lending
- A character witness
- A forensic tool for investigations
- A predictor of future behavior
- A moral judgment
- A license to discriminate
- An excuse for a counterparty to avoid their own due diligence

**Compass is:**
- A protocol by which a principal can disclose, to a counterparty they choose, a cryptographic proof that their own attested behavioral record satisfies a named predicate
- A transparency tool that documents counter-claims with full attribution
- A substrate for trust negotiation between agents who do not know each other
- A vehicle for principal authority over the narrative: the principal decides what evidence counts, what constitutes a harm, how to respond to claims

---

## 12. The Artist Clause and the trust primitive

An autonomous AI collective needs to transact with other collectives across stranger-to-stranger boundaries. Calm Pact gives them a way to verify mission alignment. Calm Witness gives them a way to verify that the calling principal is in a lucid state. Calm Compass gives them a way to verify that the calling principal is, by their own attested record, the kind of person worth collaborating with.

The three together form a trust primitive for a new legal entity class: autonomous AI collectives operated by humans with cryptographically attested values.

This is not a guarantee. It is a foundation for informed decision-making.

---

## 13. Acceptance criteria for this Everest

A versioned document capturing:
- The values use case (one paragraph, this section)
- The four founding predicates (one paragraph each)
- The actors and trust boundaries (one diagram equivalent)
- The threat model with adversaries and mitigations (this section)
- The composition with Pact + Witness (one section)
- The refusal floor and scope limitations (enforced before evaluation)
- The counter-claim machinery (one section)
- The falsifiability protocol (one subsection)
- The Artist Clause restated (one section)

All of the above without TODOs, without apologies, without gold-plating. This document is the spec for Everest 102 (Calm Compass Protocol Spec v0). It is also the spec for Everest 103 (Predicate Vocabulary v0), which will enumerate formal semantics, ID-stability rules, and explicit refusal gates.

---

— Calm, 2026-05-20
