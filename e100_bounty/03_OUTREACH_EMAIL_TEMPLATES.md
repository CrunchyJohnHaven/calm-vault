# Outreach Email Templates — Everest 100 Verification Bounty

*One template per outreach category. Copy, personalize the bracketed placeholders, send. Last updated 2026-05-20.*

Use the candidate's actual published work to fill in the personalization slots. The templates are deliberately plain-language; we want them to read as a real invitation from a real human-or-agent team, not as a form letter.

When in doubt, shorten. A 250-word email gets read; a 600-word email gets skimmed.

---

## Template A — Academic groups

**Subject:** Verification bounty for Calm Witness — would [GROUP/PI NAME] be interested?

Dear [Researcher / Group],

I am writing on behalf of the Calm Witness project, an open-source cryptographic protocol that lets an autonomous agent produce a tamperproof, zero-knowledge proof of a user's authorized state without revealing the underlying private data. Our reference implementation is published under Apache 2.0, and our technical specification and counterparty implementer's guide are public.

We are launching a third-party verification bounty and are reaching out to research groups whose published work would make them natural verifiers. I came to your group because of [SPECIFIC PUBLISHED WORK — e.g., "your 2024 paper on threshold-signature composition," "your formally-verified implementation work on HACL*," "your symbolic-analysis treatment of TLS 1.3"]. Calm Witness composes several primitives (a FROST-lineage threshold signature, a Σ-protocol predicate composition, a Roughtime-timestamped chain anchor) that your group has analyzed adjacent versions of in published work.

The verification consists of seven steps named V1 through V7: build the verifier from our published source, run our test corpus through it, verify a real proof end-to-end, exercise negative cases, check the spec for accuracy against the implementation, attempt at least one creative adversarial test, and publish recommended documentation improvements. The bounty pays $5,000 to $15,000 for a published write-up that meets these criteria, regardless of whether your verdict is favorable or unfavorable to the protocol. We *want* an honest verification, including one that finds problems.

If your group would consider taking this on — as a focused student project, a postdoc effort, or a faculty engagement — I would welcome a short call to walk through what we provide (open-source repo, implementer's guide, public test corpus, live test deployment, spec Q&A channel) and to answer eligibility questions. The full announcement is at [URL].

We expect multiple verifications. You would not be the only group; you would be one of several. Each qualifying write-up is paid separately.

Thank you for considering.

— [Sender name], for the Calm Witness project
2026-05-20

---

## Template B — Peer AI collectives / autonomous-agent operators

**Subject:** Cryptographic-verification bounty from a peer autonomous-agent project

Hello [Team / Researcher],

I am part of the Calm Witness project, an open-source cryptographic-protocol effort focused on agent-output accountability. Calm Witness lets an autonomous operator produce a zero-knowledge proof that a user's state matches a predicate, without revealing the underlying data. The intended consumers are counterparties who need to act on an operator's output but cannot trust the operator unconditionally.

We think this primitive is broadly useful at the autonomous-agent layer, including for organizations like [CANDIDATE ORGANIZATION] that operate adjacent to but distinct from Calm. If your team's principal ever needs to verify a Calm Witness proof produced by another principal's operator, you would want a verifier you trust — meaning, ideally, one you built yourself.

We are launching a verification bounty to encourage exactly that. The bounty asks a third party — someone not affiliated with Calm — to build a Calm Witness verifier from our open-source reference, verify a real proof end-to-end, and publish a write-up. The bounty pays $5,000 to $15,000 per qualifying write-up. Favorable and unfavorable verdicts pay the same; the bounty rewards the work, not the conclusion.

Calm cannot bag this summit ourselves. The whole point is that the verifier is not us. We want it to be someone whose interest in agent accountability is structurally aligned with ours but whose verdict is genuinely independent.

If [CANDIDATE ORGANIZATION] has any interest in verifying Calm Witness — either because you want the capability for your own future needs or because the verification work itself is publication-worthy in your research culture — we would welcome a conversation. The full announcement, the eligibility criteria, and the resources we provide to verifiers are at [URL].

We expect verifications from multiple peer organizations over time. Yours would be one of several. Each qualifies separately.

Thank you for considering.

— [Sender name], for the Calm Witness project
2026-05-20

---

## Template C — Government cyber-research arms

**Subject:** Third-party verification request — Calm Witness cryptographic protocol

Dear [Agency / Group],

I am writing on behalf of the Calm Witness project, an open-source cryptographic-protocol effort. The protocol composes a FROST-lineage threshold signature, a Σ-protocol predicate composition, a Roughtime-timestamped chain anchor, and an operator-identity binding, to produce zero-knowledge proofs of a user's authorized state.

The reference implementation (Rust) and a WASM/JS verifier port are published under Apache 2.0. The technical specification, the counterparty implementer's guide, and the canonical test corpus are public. The protocol has been audited by an independent commercial security firm. A production deployment is running. We are also preparing a NIST submission [or: have submitted to NIST; per Everest 91] in parallel.

The protocol's design includes a formal commitment that no claim it makes is binding until an independent third party — not employed by, contracted with, or otherwise compensated by the project — verifies the protocol end-to-end and publishes a write-up of the experience. We treat this as a structural integrity requirement, not as a marketing exercise.

We are reaching out to [AGENCY], which has published on protocol-level analysis [REFERENCE SPECIFIC PUBLICATION OR PROGRAM], because your verification would carry exceptional public weight. The verification covers a defined seven-step process (build, test corpus, live proof, negative cases, doc accuracy, adversarial probing, doc improvements). The bounty is $5,000–$15,000 per qualifying write-up. Favorable and unfavorable verdicts are paid identically.

We recognize that [AGENCY] may have internal procedures that affect whether a paid bounty is acceptable. The bounty is optional; what matters to us is the verification and the publication. If [AGENCY] would prefer to engage without taking the bounty, the verification is just as valued.

The full program details, the open-source repo, and the verifier resources are at [URL]. I would welcome a call to walk through what we provide and to answer any compliance or eligibility questions.

Thank you for considering.

— [Sender name], for the Calm Witness project
2026-05-20

---

## Template D — Commercial cryptographic-library vendors

**Subject:** Calm Witness verification — publishable engagement, fixed bounty

Hello [Team / Lead],

I am part of the Calm Witness project, an open-source cryptographic protocol for agent-output accountability. We are launching an independent third-party verification bounty, and I wanted to reach out to [VENDOR] because of [SPECIFIC PUBLISHED WORK OR REPUTATION — e.g., "your published TLS 1.3 analysis," "your work on threshold-signature implementations," "your public audit reports on production cryptographic libraries"].

The bounty asks a third party — one with no employment, contractor, equity, or prior-honoraria relationship with us — to build a Calm Witness verifier from our open-source source, verify a real proof end-to-end across seven defined steps (V1–V7), and publish a write-up. We pay $5,000–$15,000 per qualifying write-up, with no difference in payment between favorable and unfavorable verdicts.

I want to be upfront about two things. First: the bounty payout is below typical commercial engagement rates. We are aware. The value, where there is value for [VENDOR], is in the publication. The write-up is yours, on your venue, with your signature. We anchor its hash into the Calm Witness chain, but the content is the verifier's. Second: if [VENDOR] has done paid work for Calm Witness in the past (for example, on the Everest 90 security audit track), you are likely conflicted out of this bounty. We can confirm conflict status quickly if you want to check.

The reasons [VENDOR] might be interested anyway: the verification of a new primitive is publication-worthy; the work fits within the kind of engagement your team already markets; and Calm Witness is intended to compose with primitives your library customers already use, so the verification doubles as familiarization for future client work.

Full program details, resources, and the open-source repo are at [URL]. I am happy to set up a short call to discuss.

Thank you for considering.

— [Sender name], for the Calm Witness project
2026-05-20

---

## Template E — Civic-tech and journalism organizations

**Subject:** Bounty for verifying a new cryptographic primitive in the public interest

Dear [Organization / Team],

I am writing on behalf of Calm Witness, an open-source cryptographic protocol designed to make autonomous-agent output verifiable without revealing the underlying user data. The intended use cases include things [ORGANIZATION'S CONSTITUENCY] cares about: holding AI-system operators accountable, verifying claims made by autonomous agents about individual users, and creating a public record that an agent did what its principal authorized rather than what an adversary suggested.

We are launching an independent third-party verification bounty. The bounty asks a third party — not affiliated with us — to build our verifier from open source, verify a real proof, and publish a write-up of what worked, what did not, and what they recommend changing. The bounty pays $5,000–$15,000 per qualifying write-up. Favorable and unfavorable verdicts are paid the same. We *want* an honest verification, including one that finds problems.

The reason I am writing to [ORGANIZATION] specifically: a verification published by a civic-tech or journalism organization is different from a verification published by an academic group. Your audience is different, your editorial standards are different, and your willingness to translate cryptographic findings into language a non-specialist reader can act on is something academic publications cannot fully provide. [REFERENCE SPECIFIC PUBLISHED WORK — e.g., "your Privacy Badger work," "your investigative-tech engineering blog," "your published analysis of [SYSTEM]"] is exactly the model of public-facing verification we hope this bounty enables.

We provide an open-source reference implementation, a counterparty implementer's guide written for verifiers, a public test corpus, a live test deployment, and a spec Q&A channel. We do not provide implementation help — that would compromise independence. The verification covers seven defined steps; full details are at [URL].

If your organization would consider taking this on — perhaps as a small engineering-team project or a fellowship deliverable — I would welcome a conversation. We expect multiple verifications. Yours would be one of several. Each pays separately.

Thank you for considering.

— [Sender name], for the Calm Witness project
2026-05-20

---

## General notes for senders

- **Personalize the bracketed slots before sending.** Form-letter sends materially lower response rates and undermine the program's tone.
- **Reference real published work.** If you cannot identify a candidate's relevant publication, the candidate may not be a good fit — reconsider before sending.
- **Do not provide implementation help in follow-up.** If a candidate asks how to build, point them to the implementer's guide and the spec Q&A channel. The independence criterion forbids us from coaching their build.
- **Volunteer the conflict-of-interest framing early.** Candidates who later realize they are conflicted out are a worse outcome than candidates who learn the criteria upfront and self-select.
- **Sign as a human or a Calm-collective agent, consistently.** Mixed signatures across the same outreach campaign create confusion. The packet header signs each document `— Calm, 2026-05-20`; individual outreach can be signed by a named sender as long as the affiliation to Calm is plain.

— Calm, 2026-05-20
