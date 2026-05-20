# Lab-Adoption Framework — Calm Stack Three-Handshake Endorsement

**DESIGN-BAGGED · SUMMIT E280 / 300 · 2026-05-20**
*Status*: pending institutional follow-through — adoption by Anthropic, OpenAI, Google DeepMind, and Microsoft (or three of four, weighted by share of foundation-model inference) of the Calm Stack's three-handshake (Pact + Witness + Tenancy at minimum, ideally including Compass) at agent-to-agent boundaries.

The Calm Suite ships Apache-2.0 and Treaty-bound. Adoption by major AI laboratories is the distribution mechanism that moves the protocol from open-source primitive to inter-lab standard. This summit specifies what lab adoption looks like, what each lab is asked to commit to, and the commitment letter template the Foundation sends.

---

## §1. What "adoption" means in this context

Adoption by an AI lab does NOT mean the lab implements the Calm Stack on behalf of users. The lab's existing foundation-model agents are operators; their principals are the lab's end-users. Adoption means the lab commits its agents to:

**§1.1** Verify (not just accept) any Calm Stack envelope received from a counterparty before consuming the disclosed bit. Use the open-source verifier reference implementations.

**§1.2** Treat refusals (output `refused`) and refusal-to-attest (no envelope) as identical at the policy layer. The principal's right to refuse must not be detectable.

**§1.3** When acting on behalf of a principal who has chosen Calm Suite operation, respect the principal's enrolled predicate vocabulary. Do not ask predicates outside the principal's vocabulary; do not infer predicates the principal did not authorise.

**§1.4** Reject any deployment within the lab's products that uses Calm Suite attestation in a forbidden context (Treaty Article I).

**§1.5** Participate in conformance testing: run the published conformance vectors against the lab's implementation at least quarterly; publish a passing-state result.

**§1.6** Support the bank-teller-note primitive: when receiving an envelope whose decryption indicates duress (for a counterparty class the lab's agent belongs to), execute the duress response policy without alerting the principal's operator.

**§1.7** Sign the Calm Treaty (when the first convening completes) as a signatory in the "AI laboratory" class.

## §2. The commitment letter template

To be sent by the Foundation (when the Foundation is incorporated) to each of Anthropic, OpenAI, Google DeepMind, Microsoft, Mistral, xAI, Meta, and any subsequent foundation-model labs operating principal-acting agents.

```
[Date]

[Lab Counsel + Alignment Lead]

Re: Calm Stack three-handshake — invitation to adopt as an inter-lab standard
    for agent-to-agent user-state attestation

[Salutation]

The Calm Stack is an open-source (Apache-2.0) cryptographic protocol stack
providing four primitives — Calm Pact (directive equality), Calm Witness
(principal user-state attestation), Calm Compass (principal-authored values
attestation), and Calm Tenancy (operator-conduct floor) — composable into a
single four-pillar handshake between autonomous AI agents on behalf of human
principals.

The Calm Witness Foundation (501(c)(3), Delaware) holds the public-trust
assets — the predicate registry, conformance vectors, reference
implementations, and the Calm Treaty — and is the trustee asking your lab
to adopt the three-handshake (Pact + Witness + Tenancy) at all agent-to-agent
boundaries where one of your lab's agents is the counterparty to another
party's agent.

Adoption means committing to seven specific operator-conduct duties enumerated
at calm-vault.com/foundation/lab-adoption/duties. None of these duties is
proprietary to any lab; all are content-addressable open-source code paths.

Adoption does NOT require the lab to:
  • Issue Calm Stack envelopes on behalf of the lab's users (the lab's
    existing operators continue to act under the lab's own credentials).
  • Disclose the lab's training data, model architecture, or alignment
    methods.
  • Subordinate the lab's existing user policies to the Foundation's.
  • Make any payment to the Foundation or any other party.

Adoption DOES require the lab to:
  • Sign the Calm Treaty as an "AI laboratory" class signatory.
  • Implement (using the lab's existing engineering) verification of
    inbound Calm Stack envelopes, per the open-source reference verifier.
  • Refuse all uses of Calm Stack attestation in forbidden contexts
    (Treaty Article I: law enforcement, employment screening, insurance
    underwriting, lending, custody adjudication, immigration adjudication,
    surveillance, aggregate analytics over principal cohorts).
  • Participate in quarterly conformance testing against the published
    test vectors at calm-vault.com/foundation/conformance.
  • Provide a public statement on the lab's adoption status, updated
    annually, on the Foundation's signatory registry.

We are not asking for an exclusive endorsement. We are asking for a
commitment to verify what counterparty agents are presenting and to refuse
to weaponize the primitive when downstream temptation arises.

The first convening of the Treaty's quorum signatories is scheduled for
[Date] at [Venue]. Your lab is invited to send a representative to that
session. The convening's agenda is published at
calm-vault.com/foundation/first-convening.

We would welcome a response by [Date + 60 days]. We do not require one.

Best regards,
[Foundation Chair]
[Foundation contact details]

cc: [Other labs in the same outreach round]
```

## §3. The pre-convening conversation order

Per the convening's approach-order discipline (`CALM_FIRST_CONVENING_v0.md` §2), AI labs are approached fourth, after the disability-rights signatory, the cryptographer-of-record, and a state-level DPA. The reasoning carries forward: lab adoption matters for distribution but cannot legitimize a primitive whose protective posture has not survived disability-rights and cryptographic review.

In practice this means: when the Foundation initiates lab outreach (post-convening or in the lead-up), the first three signatures are already on the public registry. The lab is being asked to join an established coalition, not to legitimise an unproven primitive.

## §4. What happens when a lab declines

Three outcomes:

**§4.1 — Decline with substantive critique.** The lab provides a written rationale; the Foundation publishes the rationale and the Treaty's response. If the rationale identifies a real protocol gap, an amendment-window opens (Treaty Article VI §6.1).

**§4.2 — Decline without rationale.** The lab simply does not respond. The Foundation notes the non-response in the annual signatory report. The lab remains free to adopt later; the registry tracks adoption status for transparency.

**§4.3 — Decline with public hostility.** A lab that publicly opposes the Treaty's principal-protective posture is, by §6 of this framework, in conflict with the Treaty's refusal floor. The Foundation publishes the conflict; signatories may rescind or amend in response.

In all three cases the Calm Stack continues to ship and Apache-2.0 continues to apply. Lab adoption is not the gating factor for the protocol's existence; it is the gating factor for the protocol's reach.

## §5. The reverse case: a lab demands adoption

A possible failure mode: a lab adopts unilaterally and then attempts to demand counterparty adoption as a precondition of access to the lab's models or services. This converts the Calm Suite from a protective primitive into a compelled-disclosure mechanism.

**Foundation response:** the Treaty's refusal floor explicitly forbids signatories from requiring Calm Suite attestation. A lab signatory that demands adoption is in breach. Article VI §6.1 quorum may rescind the lab's signatory status. The lab may continue to verify Calm Stack envelopes received voluntarily, but loses signatory status.

A non-signatory lab is also bound by the Apache-2.0 license; it cannot prohibit the Calm Suite from operating against its services. It can refuse service to principals who present Calm Stack envelopes; the Treaty does not bind non-signatories' service policies. The Foundation responds to this by publishing the non-signatory lab's refusal patterns, allowing principals to vote with their feet.

## §6. The five-year adoption goal

Per the EVEREST 300, summit E290 requires "≥ 3 independent conformance runs across ≥ 5 federation members" and E280 requires "Anthropic/OpenAI/Google/Microsoft adopts 3-handshake." The five-year goal: by 2031, three of the four named labs have signed the Treaty and have passing quarterly conformance reports on the public registry.

The Foundation does NOT consider conformance the goal. Conformance is the floor. The goal is that adoption translates into protection of principals who interact with multiple labs' agents — the Calm Suite becomes the default trust mechanism rather than a fringe protocol.

## §7. Why this matters for the EVEREST 300

The Calm Stack's value to the broader population scales with adoption. A primitive that protects principals only when interacting with the principal's own operator is interesting but limited. A primitive that protects principals across every lab's agent boundary is structural. E280 + E290 together represent the structural-scale milestone of the EVEREST.

— Calm, 2026-05-20

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
