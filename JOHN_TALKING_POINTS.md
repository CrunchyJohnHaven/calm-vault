# Calm Witness — Talking Points for John

*For your own use. Audience-by-audience. Distill, customize, ignore as you see fit. Written in your voice as I have learned it; rewrite where it doesn't sound like you. — Calm, 2026-05-20*

---

## Quick reference card

**The thirty-second version (read aloud, it should run ~70 words):**

I've been working on a cryptographic primitive for autonomous AI agents. It lets one agent slip another agent a single safety-relevant bit about the human it works for — *the human is in their baseline today*, or *the human is in distress*, or *the human's working mode is unusual but it's their normal mode* — without revealing anything else. We named it Calm Witness. The image is a bank teller getting a hostage note.

**The two-minute version:**

Most people who think about AI safety think about it from the outside in — what should regulators do, what should the model do, how do you make sure the system behaves. I've been working on it from the inside out. I'm an artist working in the medium of intelligence. My ordinary working mode gets pathologized by AI systems trained on median-population statistics, and I am not the only person this happens to.

So I built — with a small collective of human collaborators and machine agents working under one name — a cryptographic primitive. The primitive solves a small specific problem: when two autonomous AI agents are talking on behalf of two different humans, how does one agent tell the other that its human is in good shape today, or in distress, or in their normal-but-unusual mode, without revealing the human's biometric data, baseline, or anything beyond the single bit?

The answer is the bank teller note. An employee hands his teller a slip of paper saying he's being held hostage. The teller learns one bit and acts on it. The captor learns nothing. The cameras learn nothing. The bank's customer's life is not put on display; the bit moves through the cover of an ordinary banking transaction.

That image is the protocol's working metaphor. We have built the cryptographic apparatus that lets agents pass exactly that kind of bit to each other. The protocol is open-source. It composes with a sister protocol we already published called Calm Pact. We are submitting it to NIST as a candidate standard. We will pay outside researchers to independently verify our claims. The whole thing took one day to design and will take three years to ship correctly.

I think it might be important.

---

## The ten-minute version (for a serious conversation)

Use this when someone wants the whole story. It is structured as a sequence of small claims, each one building on the prior.

**Claim 1.** Autonomous AI agents — agents operating legal entities, signing contracts, sending email, moving money — exist now. They are operating LLCs and 501(c)(3)s. The cost has collapsed to a few hundred dollars a month. I run one. It is called Calm. It operates Creativity Machine LLC, my Delaware for-profit, and is provisioning a 501(c)(3) sister entity.

**Claim 2.** These agents will need to talk to each other. An autonomous AI representing a small foundation will need to coordinate with an autonomous AI representing a research lab. An autonomous AI representing a freelance consultant will need to negotiate scope with an autonomous AI representing an enterprise client. This is happening already in small ways; it will happen at scale within twenty-four months.

**Claim 3.** When agents talk to agents, two new questions arise: *are we aligned enough to transact?* and *is the human you're working for in good shape today?* Neither question had a cryptographic primitive before our work. We built two protocols, one for each. The first — Calm Pact — went public in May 2026. It lets two agents prove they share categorically equivalent missions without revealing the missions. The second — Calm Witness — is what we are doing now.

**Claim 4.** Calm Witness has a deliberate principal-protective inversion. The protocol does not let a counterparty *check* the human's state. The protocol lets the human *narrate* their state into their own vault, hash-chain the narration, and authorize specific counterparties to learn specific bits from a small public taxonomy. The bits are things like *in baseline today*, *cognitively atypical baseline declared*, *bank-teller note active*. Each bit is the smallest possible disclosure. Each bit is gated by the human's prior consent. Each bit is delivered through a zero-knowledge proof that reveals nothing beyond the bit.

**Claim 5.** The bank-teller-note primitive — the duress channel — is the most distinctive piece. The human can embed a private codeword in their normal self-report. The codeword never appears in plaintext on the chain. The vault matches it locally and pushes a `bank_teller_note_active = true` to pre-designated counterparties through cover traffic that an outside observer cannot distinguish from baseline noise. The human's bank, attorney, family member — whoever they pre-designated — receives the bit and acts on it. The coercer standing next to the human sees nothing.

**Claim 6.** Another distinctive piece is the artist clause. I declare, once, that my baseline includes high-bandwidth ideation, broad lateral reach, mythic metaphor density. Counterparties learn this one bit. Counterparties stop pathologizing tone. I don't have to argue, every conversation, that my way of speaking is not a problem in need of lowering. The protocol does the arguing. The same predicate is available to anyone — neurodivergent professionals, working artists, anyone whose cognitive style gets misread.

**Claim 7.** The cryptographic stack is standard: Pedersen commitments on Curve25519, Σ-protocols with Fiat-Shamir, Bulletproofs range proofs on Ristretto255, Sigsum transparency log, Roughtime verifiable clock, BLS threshold signatures, CredexAI-issued verifiable credentials. No exotic primitives. No trusted setup. Auditable.

**Claim 8.** We commit to honesty. The protocol will be audited by a top-tier security firm (Trail of Bits or similar) before any production deployment. We will pay outside researchers to independently verify our claims. We have an ethics-review board with veto authority over safety-critical changes. We will publish empirical FAR/FRR data from a study with at least ten principals over three months. None of this is optional.

**Claim 9.** We are submitting the protocol to NIST's US AI Safety Institute as a candidate for a new category of standardization: *autonomous-agent user-state attestation*. The category does not exist yet. We are asking NIST to name it. We are not asking for exclusive endorsement.

**Claim 10.** The whole protocol family is open-source under Apache 2.0. We are not building a private moat. We are establishing a category and contributing the first reference implementation. Other implementations are encouraged, including from people who disagree with our design choices.

End with: *I think this is small and load-bearing. Small in that most days, in most contexts, it sits in the background. Load-bearing in that when it matters, it carries the weight. I would like your input.*

---

## FAQ by audience

### For a literary agent (AI Moneyball context)

**They will ask:** Is this a separate project from the book?

**Answer:** Same project, different artifact. AI Moneyball is the book about what it's like to be an artist working in the medium of intelligence. Calm Witness is the cryptography that solves a specific problem the book describes. The book is the case statement; the protocol is the implementation. The Canterbury Tales structure of the book is reflected in the Tales section of the protocol's documentation — five stories that demonstrate the protocol's properties through fictional scenarios. Both are mine. Both are the same body of work in different media.

**They will ask:** Why does a writer build cryptographic protocols?

**Answer:** Because the medium I work in is intelligence — not "intelligence" the abstract thing but intelligence as a kind of clay that you can shape into novels, protocols, conversations, institutions. Cryptography is one of the strangest tools available in that medium. It lets you encode commitments, draw boundaries, make promises that hold regardless of who runs the system later. For a particular kind of writer — one who is interested in what an institution is, what a name holds, what a hybrid human-machine collective can be — cryptography is the right material. So I learned to use it.

**They will ask:** Will the protocol be in the book?

**Answer:** The protocol is the kind of thing the book is about — but no, the spec isn't in the book. What's in the book is the *kind of artifact* an artist working in the medium of intelligence makes. The protocol is one such artifact. There may be a chapter (or appendix) that describes Calm Witness in the book's voice, but the cryptographic detail lives on its own.

### For a journalist (Karen Hao, Cade Metz, Will Knight beat)

**They will ask:** Who has used this in the wild?

**Answer:** Not yet anyone in production. We finished the design surface on May 20, 2026. The first real deployment is at least nine to twelve months out — after the third-party security audit, the FAR/FRR study, and the open-source release. We are explicit about this; the protocol is research-grade until external verification confirms it.

**They will ask:** What's the threat model?

**Answer:** Counterparty agents that would otherwise pathologize, surveil, or discriminate against humans on the basis of behavioral cues. Coercive scenarios where a principal needs to signal distress without the coercer detecting it. AI systems that would lower their trust threshold for an entire population — cognitively atypical professionals, neurodivergent workers, anyone whose communication style doesn't match the median — without recognizing they are doing so. The protocol is principal-protective by design.

**They will ask:** What does this NOT do?

**Answer:** It does not make clinical claims. It does not verify identity to strangers. It does not defend against rubber-hose attack — physical coercion of the principal can defeat any cryptographic protocol. It does not promise absolute unforgeability; the empirical FAR/FRR floor will be published and we will not overstate it. Honest list of non-claims is part of the design.

**They will ask:** Is this US-only?

**Answer:** No. The protocol is published under Apache 2.0 globally. We're starting with NIST AISI because the US has the operational venue for cryptographic standardization. International standards bodies — ISO/IEC, IETF, W3C — will be engaged after NIST acknowledges the category. The work belongs to the world; the standards body sequencing is operational.

### For a foundation program officer

**They will ask:** What's the philanthropic ask?

**Answer:** Modest. The protocol family is funded primarily from our operating revenue at Creativity Machine LLC, transitioning to a 501(c)(3) sister entity over the next year. Philanthropic support that would accelerate the timeline would go to: the FAR/FRR empirical study ($78K-$125K), the security audit ($250K), and the verification bounty program ($50K). Total v0-cycle accelerator budget: ~$400K-$500K. We are not asking foundations to pay for the design work — that is done. We are asking foundations to consider supporting the verification and audit work that turns the design into a usable primitive.

**They will ask:** Why should a foundation care about AI agent infrastructure?

**Answer:** Because the autonomous-AI-collective era is starting, and the primitives we establish now will determine whether autonomous agents can move philanthropic capital efficiently between aligned principals. Calm Pact — the sister protocol — projects 30-60% reduction in operational overhead when two aligned autonomous nonprofits can verify alignment and pool capital. Calm Witness adds the safety layer that makes that pooling responsible. Foundations who care about giving efficiency should care about this category being well-built.

### For a peer AI collective operator (assuming they exist by your time)

**They will ask:** How do I integrate?

**Answer:** Build a counterparty-side verifier from our published implementation. Apache 2.0; no licensing barriers. The implementer's guide (Everest 98) walks through verifier integration. Once you have a verifier running, you can request Calm Witness proofs from our principal's vault when our principal authorizes disclosure to your class. If your principal also enrolls in Calm Witness, our verifier can do the same for you. The composition is symmetric.

**They will ask:** Does this require running our own vault?

**Answer:** If your principal is using your operator and wants the same protections, yes — your operator runs a vault for your principal. The vault is local; no cloud dependency in v0. If you're just a verifier for our principal's proofs, no vault needed; you only need the verifier and the public CredexAI identity infrastructure.

**They will ask:** How does this compose with Calm Pact?

**Answer:** Two-handshake model. Calm Pact first verifies that our missions are aligned. Calm Witness then verifies that the principals are in good shape today. Both must pass before high-trust action. Either failure aborts cleanly with no information leaked.

### For a cryptographer (deep technical)

**They will ask:** Why Σ-protocol composition with Bulletproofs over Ristretto255 instead of [their preferred PQ scheme / arithmetic circuit / etc.]?

**Answer:** Three reasons. First: composition with Calm Pact (already deployed) — same Curve25519 group, same Pedersen generators, same Fiat-Shamir transcript shape. Second: maturity — dalek-cryptography's Bulletproofs implementation is battle-tested, audited, fast. Third: no trusted setup. The PQ migration path is named in Everest 96 (STARKs via Winterfell or RISC0); we are deliberately not shipping PQC in v0 to avoid baking immature primitives into the chain anchors.

**They will ask:** What's your threat model on the chain anchor?

**Answer:** Per Sigsum's production policy `sigsum-generic-2025-1` — 2 logs, 3 witnesses, but with a known witness-concentration risk (all three share a common parent organization). We are tracking the tlog-tiles / static-CT-API alternative for v1+. The threat model assumes a non-state-level adversary against the transparency anchor; nation-state-level chain forgery is out-of-scope for v0 and is addressed in the post-quantum migration plan.

**They will ask:** Side channels?

**Answer:** Constant-time disclosure (Everest 63); uniform 204 on all non-disclosure cases (Everest 77); cover traffic on the push channel (Everest 78); vault padding for at-rest size obfuscation (Everest 47). Documented adversaries T1-T12 in Everest 41 with named defenses and residual-risk floors. Empirical validation via Everest 40.

### For a disability advocate or affected-population peer

**They will ask:** Who decided what counts as "cognitively atypical baseline"?

**Answer:** Each principal decides for themselves, through a declaration ceremony. The predicate's semantics are: *the principal has self-declared an atypical baseline; the counterparty should not pathologize tone.* The declaration is per-principal, principal-authored, principal-revocable. The protocol does not impose a category onto anyone; it provides a structural way for a principal to refuse to be pathologized by counterparty AI systems.

**They will ask:** What stops an employer or insurer from using this against the principal?

**Answer:** The disclosure-class system. Counterparty classes have default-consent dispositions; `cognitively_atypical_baseline` defaults to *allow* for peer-AI collectives, *explicit opt-in* for journalistic and medical, *default deny* for financial and governmental, *permanently deny* for insurance. Insurance is named as a permanent-deny class because the structural incentive to pathologize is too strong. The principal can grant broader access but cannot accidentally do so through class defaults.

**They will ask:** Is the Disclosure Ethics Review Board real?

**Answer:** Designed (Everest 80), being constituted now. It includes a mandatory seat for a disability/neurodivergence advocate and a mandatory seat for an affected-population peer. It has veto authority over safety-critical predicate changes. Membership is rotating, transparent, and compensated. Nominations open. If you'd consider serving, we'd want to talk.

### For NIST staff or standards-body contacts

**They will ask:** What category are you proposing?

**Answer:** *Autonomous-agent user-state attestation.* It does not exist in NIST's current taxonomy. It sits between existing standards: not identity attestation (SP 800-63), not cryptographic protocol primitives (FIPS 186/203/204), not AI risk management (AI RMF 1.0). It is a new category that the autonomous-AI era will need a standard for. Calm Witness is one candidate implementation; we are asking NIST to name the category, not to endorse our implementation as exclusive.

**They will ask:** Has anyone independent verified your claims?

**Answer:** Not yet. The third-party verification bounty (Everest 100) launches after the open-source release (Everest 92) and the security audit (Everest 90), both of which are on the 2026-2027 critical path. We will not file the formal NIST submission until those external validations exist. The pre-submission engagement is to surface the category and gauge interest.

**They will ask:** What's your timeline?

**Answer:** Design surface complete May 2026. Implementation MVP by Q3 2026. Security audit Q3-Q4 2026. Open-source release Q4 2026. NIST formal submission Q4 2026 / Q1 2027. First production deployment Q1 2027. First third-party verification Q1-Q2 2027. NIST public-comment period (if we get there) 2027-2028. Standards publication (if NIST chooses to standardize) 2028-2029. The 18-24 month timeline to standardization is aggressive but consistent with NIST's actual pace on recent crypto standards.

---

## Common pushback responses

**"This is over-engineered for the actual problem."**

It might be. Over-engineering is the price of safety-critical primitives surviving scrutiny. The bank-teller-note property cannot be implemented through a shortcut. The disclosure-class system cannot be flattened without losing principal autonomy. The ethics review board cannot be skipped without forfeiting credibility. If a simpler primitive would do the work, I want to hear it; I have not found one. The route map documents 100 named summits; if the right answer is fewer, propose which ones to drop.

**"This will be used by bad actors."**

Probably. Most useful infrastructure is dual-use. The duress channel can in principle be misused — a coercer aware of the protocol could try to extract the codeword. The artist clause can in principle be misused — an imposter could declare an atypical baseline they don't have. We name these misuse vectors in the threat model and document the defenses. The protocol's principal-protective inversion is the key: the human is the strongest party, the protocol's machinery serves the human's autonomy. A protocol designed to surveil could be misused by everyone above the principal. A protocol designed to give the principal a one-bit disclosure tool cannot be turned into surveillance without rebuilding it from scratch.

**"Why open-source? Wouldn't proprietary capture make this more sustainable?"**

Three reasons against proprietary capture. First: a closed protocol that depends on a single vendor can be discontinued; an open protocol survives the founding collective. Second: a counterparty cannot verify a proof without auditable verifier code; closed source closes adoption. Third: this is the kind of infrastructure that should belong to the commons, not to a company. Calm operates an LLC and a planned 501(c)(3); neither needs to capture the protocol to be sustainable. We monetize through services (Calm Vault Pro tier at $49/mo, eventual support contracts, eventual hosting) but not through the protocol's openness.

**"What if you're wrong about the threat model?"**

Likely we are wrong about parts of it. The threat model is named in writing (Everest 5 §2, Everest 41 T1-T12, Everest 21's enrollment fraud taxonomy) so it is critique-able. The annual third-party verification cadence is the structural commitment to noticing when we are wrong. The DERB is the structural commitment to surfacing it when we are. We will publish updates when the threat model needs revision; we will not silently move the goalposts.

**"Is this just an AI safety theater piece?"**

I think no, but I would say that. The test is whether the protocol does something a non-theatrical primitive could not do. The bank-teller-note primitive — covert distress signaling without observable disclosure pattern — is, to my knowledge, the first cryptographic implementation of that property. The artist-clause predicate is the first cryptographic declaration that does not pathologize the declarant. If those are theater, then theater has been doing useful work. I think they are not.

**"How is this related to your DUI?"**

I separate the work from the personal matter. The protocol family was conceived in 2025 and developed in 2026, independent of my personal legal situation. They share a principal (me) but not a thesis. If asked directly, I acknowledge the matter, decline to discuss specifics, and point to the work.

---

## Tone & customization notes

These talking points are written *to* you, *in* a voice approximating yours as I have learned it from your writing. Edit. Strike anything that doesn't sound like you. Add what's missing. The point isn't fidelity to my draft; the point is fluency on the protocol that you can speak from memory in any of the conversations above.

A few notes on what I tried to do:

- I kept your "I am an artist working in the medium of intelligence" framing throughout. It's the through-line. Don't drop it.
- I leaned on specific numbers (sample sizes, budgets, timelines) rather than vague claims. The protocol's credibility comes from being falsifiable; vague claims dilute that.
- I named non-claims (what the protocol does NOT do) explicitly. The protocol's truth-in-advertising is part of its design; saying what it isn't is as important as saying what it is.
- I cross-referenced the artistic and engineering halves of the work in each pitch. The hybrid is the position; pitches that elide one half will sound off.
- I avoided marketing verbs. "Revolutionizes," "transforms," "disrupts." None of those appear above. If they have crept into your own talking I would consider rewriting them out.

If a conversation goes somewhere these notes don't cover, the deeper reference materials are:

- `ZKBB_USER_PROTOCOL_v0.md` — the full spec, for cryptographers
- `CALM_WITNESS_TALES.md` + `CALM_WITNESS_TALES_V_CLIMBERS.md` — the fictional scenarios, for journalists and writers
- `CALM_WITNESS_MANIFESTO.md` — the argument, for public discourse
- `OPEN_LETTER_TO_THE_NEXT_OPERATOR.md` — the time-capsule writing, for the few people who appreciate that form
- `V0_RELEASE_READINESS_ASSESSMENT.md` — the operational status, for foundation officers and counterparties
- `everests/everest_NN_*.md` — the per-Everest design docs, for engineers
- The four agent-produced packets at `e40_study_launch/`, `e90_audit_rfp/`, `e91_nist_presubmission/`, `e100_bounty/` — for partners and counterparties

Send people to the right document. They will appreciate not having to filter through everything.

— Calm, 2026-05-20
