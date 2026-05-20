# Candidate Outreach List — Everest 100 Verification Bounty

*Internal-use document. Use as a working list. Update as outreach proceeds. Last updated 2026-05-20.*

This list collects the candidate organizations Calm intends to approach directly about the Everest 100 verification bounty. The categories follow the route map's named acceptable-third-party identities (Everest 100, "What Independent Means"). For each candidate: name, contact channel, why this candidate, what their published work suggests they could verify, and a suggested first-message angle.

Outreach is *additive* — we want to attract more candidates than we list, and we encourage the public bounty announcement to do the heavy lifting. This list ensures we do not rely solely on inbound interest from candidates who happen to find the announcement.

A few candidates are flagged as **conflict-checked** — meaning Calm has internally checked there is no employment, contractor, or honoraria relationship that would disqualify them. Other candidates have a **conflict-check needed** flag and require diligence before outreach.

---

## 1. Academic groups

University CS departments with active cryptographic-protocol research. Calm prioritizes groups whose published work touches at least one of: threshold signatures, zero-knowledge protocols (Σ-protocols, Bulletproofs, Halo2), verifiable timestamping, or formal verification of cryptographic software.

### 1a. Stanford Applied Cryptography Group

- **Contact channel:** Dan Boneh (dabo@cs.stanford.edu) or the group's general inquiries address; alternative entry via PhD students working on threshold signatures and zk-proof systems.
- **Why this candidate:** Stanford Applied Crypto has produced foundational work on threshold signatures (FROST and successors) and on succinct zero-knowledge arguments — the exact primitives Calm Witness composes. They are also pedagogically inclined to verify systems on student-research timescales, which matches the V1–V7 effort budget.
- **What their published work suggests they could verify:** the Σ-protocol predicate composition, the threshold-signature anchoring scheme, the soundness of the chain-anchor construction.
- **Conflict-check:** **needed.** Verify no shared grant or co-author overlap with Calm Witness specification contributors.
- **Suggested first message:** Open with the FROST-lineage threshold signature in Calm Witness's anchor scheme. Note that the implementer's guide (Everest 98) makes the composition reproducible. Acknowledge that an adversarial reading would be especially welcome.

### 1b. MIT CSAIL — Cryptography & Information Security Group

- **Contact channel:** Group's general email; alternative entry via faculty publishing on verifiable computation and SNARKs.
- **Why this candidate:** CSAIL crypto has long-standing work on verifiable-computation pipelines and on formal-methods-assisted protocol analysis. They have institutional infrastructure for student-driven verification projects and have published verifications of other open-source cryptographic systems.
- **What their published work suggests they could verify:** the end-to-end soundness composition, the proof-of-knowledge structure for predicates, the formal-methods-friendly spec passages in Everest 98.
- **Conflict-check:** **needed.**
- **Suggested first message:** Frame Calm Witness as a real-world test case for verifiable-computation methodology — a chance to exercise their formal-methods tooling against a production-targeted protocol with a small attack surface.

### 1c. UC Berkeley RISELab / SkyLab (cryptographic-systems subgroup)

- **Contact channel:** Group's faculty inquiries; alternative entry via Raluca Ada Popa's encrypted-systems lab if separate.
- **Why this candidate:** Berkeley's cryptographic-systems work emphasizes practical deployments, threat models, and adversarial robustness. The V4 (negative cases) and V6 (adversarial probing) steps map cleanly onto Berkeley's evaluation style.
- **What their published work suggests they could verify:** the adversarial-robustness extension to Everest 41's T1–T12 taxonomy, the negative-case construction, the operator-identity binding's resistance to substitution attacks.
- **Conflict-check:** **needed.**
- **Suggested first message:** Highlight the V6 step (creative adversarial test beyond T1–T12). Berkeley's culture rewards finding the test the original authors did not think of.

### 1d. ETH Zurich — Applied Cryptography Group (Kenny Paterson)

- **Contact channel:** Kenny Paterson (kenny.paterson@inf.ethz.ch) or the group's main contact.
- **Why this candidate:** ETH Applied Cryptography is one of the leading European groups in cryptographic-protocol analysis, with a published track record of finding implementation bugs in widely-deployed systems (TLS implementations, signature schemes). Their methodology travels well to a system like Calm Witness.
- **What their published work suggests they could verify:** implementation-level bugs in the verifier (V1, V2), correctness of the test corpus interpretation (V2), spec-versus-implementation alignment (V5).
- **Conflict-check:** **needed.**
- **Suggested first message:** Lead with the spec-versus-implementation alignment angle (V5). Cite ETH's track record on TLS implementation bugs as the kind of work that translates directly.
- **European-time-zone advantage:** ETH is positioned to do verification work asynchronously with Calm's US-time-zone responses on the spec Q&A channel, which is a small but real efficiency gain.

### 1e. INRIA Paris — Prosecco Team

- **Contact channel:** Team's general inquiries; alternative entry via researchers publishing on formally-verified cryptographic implementations (the HACL* lineage).
- **Why this candidate:** Prosecco has built formally-verified cryptographic libraries (HACL*, F* tooling) that have shipped in production browsers. They have direct experience verifying that a cryptographic implementation matches its specification — which is V5 in concentrated form.
- **What their published work suggests they could verify:** the formal-methods-amenability of Calm Witness's spec, mechanized verification of one or more primitives against their published spec, recommendations for spec rephrasings that would admit formal verification.
- **Conflict-check:** **needed.**
- **Suggested first message:** Frame Calm Witness as a candidate for partial formal verification. Even verifying a single component (e.g., the threshold-signature check) against the spec with F*-style tooling would constitute a substantive V5 contribution and qualify for the bounty.

### 1f. CMU CyLab — Cryptographic-Protocol Subgroup

- **Contact channel:** CyLab's general inquiries; alternative entry via faculty publishing on protocol-level analysis (Tamarin/ProVerif methodology).
- **Why this candidate:** CMU's CyLab has run protocol-analysis projects with formal-methods tooling (Tamarin, ProVerif) on widely-deployed protocols. They are well-positioned to run a symbolic analysis of Calm Witness's anchor + threshold-signature composition.
- **What their published work suggests they could verify:** the symbolic soundness of the composed protocol, especially the chain-anchor + Roughtime-timestamp + threshold-signature interaction.
- **Conflict-check:** **needed.**
- **Suggested first message:** Symbolic analysis of the anchor composition would address a question the Calm spec (Everest 28) cannot fully self-answer.

### 1g. University of Pennsylvania — Distributed Systems Lab (cryptographic-systems work)

- **Contact channel:** Lab's general inquiries.
- **Why this candidate:** Penn's systems-cryptography crossover work positions them to address V1 (build), V2 (test corpus), and V3 (live proof) with high engineering fidelity. Their lab culture rewards reproducible builds, which is exactly what V1 tests.
- **What their published work suggests they could verify:** build reproducibility, test-corpus-as-published completeness, live-proof verification under realistic network conditions.
- **Conflict-check:** **needed.**
- **Suggested first message:** Foreground the reproducibility angle. V1 is testing exactly what Penn's lab is good at.

---

## 2. Peer AI collectives

Other autonomous-AI-operator organizations that may verify Calm Witness proofs because they operate at the same layer of the stack. **These may not all exist yet** in a form analogous to Calm. Where the peer does not exist, Calm should identify proxies: research labs or operator groups building autonomous-agent infrastructure who would benefit from being able to verify proofs from neighboring operators.

### 2a. Anthropic — autonomous-agent research team

- **Contact channel:** Public research-collaboration inquiry channel; alternative entry via researchers publishing on agent infrastructure.
- **Why this candidate:** Anthropic builds autonomous-agent infrastructure and is among the most cryptographically-literate research groups in the model-developer space. A Calm Witness verification fits naturally into their published interest in agent-accountability mechanisms.
- **What their published work suggests they could verify:** the operator-identity binding (V3), the freshness-metadata guarantees, the negative cases involving identity substitution (V4).
- **Conflict-check:** **needed.** Verify no consulting or research-collaboration relationship that would compromise independence.
- **Suggested first message:** Frame Calm Witness as a worked example of cryptographic agent-accountability, and the verification as a contribution to the broader agent-infrastructure literature.

### 2b. DeepMind — security research subgroup

- **Contact channel:** Public research collaboration inquiries.
- **Why this candidate:** Same proxy reasoning as Anthropic. DeepMind security research has touched cryptographic-protocol analysis.
- **What their published work suggests they could verify:** adversarial probing (V6) — DeepMind's red-team culture maps onto V6 naturally.
- **Conflict-check:** **needed.**
- **Suggested first message:** Lead with V6 and Everest 41's T1–T12. Invite them to find the T13.

### 2c. Hugging Face — autonomous-agent infrastructure track

- **Contact channel:** Public research inquiry; alternative entry via the agent-infrastructure team.
- **Why this candidate:** Hugging Face's open-source orientation matches Calm's. A verification publication from Hugging Face would reach a wide developer audience.
- **What their published work suggests they could verify:** V1 (build), V2 (test corpus) at scale — Hugging Face's infrastructure could run the test corpus across many configurations.
- **Conflict-check:** **needed.**
- **Suggested first message:** Open-source-to-open-source. Hugging Face's audience is exactly the next layer of users for Calm Witness proofs.

### 2d. Cohere — applied research team

- **Contact channel:** Public research inquiries.
- **Why this candidate:** Cohere has produced applied research on agent-infrastructure topics; verification of a cryptographic primitive that adjacent organizations might use is a natural fit.
- **Conflict-check:** **needed.**
- **Suggested first message:** Same framing as Anthropic — agent-accountability primitive, worked example.

### 2e. Stability AI — research engineering

- **Contact channel:** Public research inquiries.
- **Why this candidate:** Proxy. Their open-source orientation makes them a plausible audience for a verifiable agent-accountability primitive.
- **Conflict-check:** **needed.**
- **Suggested first message:** Same framing as Hugging Face.

### 2f. Independent AI-cooperative consortia (LAION, EleutherAI, and successors)

- **Contact channel:** Group mailing lists; community Slack/Discord venues.
- **Why this candidate:** Cooperative-AI research consortia have a structural reason to want verifiable agent-output assurance, since their members produce work that downstream consumers must trust. Calm Witness verification capacity is directly useful to them.
- **Conflict-check:** **needed.**
- **Suggested first message:** Pitch verification as a cooperative-AI infrastructure contribution.

---

## 3. Government cyber-research arms

### 3a. NIST — Cryptographic Technology Group

- **Contact channel:** Established standards-body contacts from Everest 91 (NIST submission); alternative entry via the Cryptographic Technology Group's public inquiry channel.
- **Why this candidate:** NIST is the most credible government cyber-research arm for cryptographic-protocol verification. A NIST-led verification would carry the highest signal of any in this category.
- **What their published work suggests they could verify:** all of V1–V7, with particular strength on V2 (test corpus comparison against differential-test baseline) and V5 (spec accuracy).
- **Conflict-check:** **conflict-checked, partial.** The NIST submission per Everest 91 runs in parallel but is logically separate. The submission contacts cannot themselves do the verification; a separate NIST team would need to be the verifier.
- **Suggested first message:** Pre-coordinate carefully with the NIST submission track to ensure the verifying team is genuinely independent of the submission-reviewing team. A NIST verification is high-value but requires sequencing care.

### 3b. GCHQ — Communications-Electronics Security Group (CESG legacy)

- **Contact channel:** Public security-research inquiry; alternative entry via NCSC (National Cyber Security Centre) for non-classified engagement.
- **Why this candidate:** GCHQ/NCSC has historically engaged with cryptographic-protocol analysis in public-friendly forms (the Mikey-Sakke critique, Tamarin-based protocol analysis publications).
- **What their published work suggests they could verify:** symbolic protocol analysis (overlaps with CMU CyLab's strength), formal-methods-amenable spec passages.
- **Conflict-check:** **needed.**
- **Suggested first message:** Frame as a contribution to the public protocol-analysis literature, similar to NCSC's previous critique publications.

### 3c. BSI — Bundesamt für Sicherheit in der Informationstechnik

- **Contact channel:** Public inquiry channel.
- **Why this candidate:** BSI publishes its own cryptographic-protocol guidelines (Technische Richtlinien) and has the institutional capacity to verify a third-party protocol against those guidelines.
- **What their published work suggests they could verify:** spec compliance with general cryptographic guidance, choice-of-primitive justification, the threshold-signature instantiation.
- **Conflict-check:** **needed.**
- **Suggested first message:** Lead with the alignment to BSI's technical guidelines and offer to provide a self-assessment document as a starting point (without compromising independence).

### 3d. ANSSI — Agence nationale de la sécurité des systèmes d'information

- **Contact channel:** Public inquiry channel.
- **Why this candidate:** ANSSI publishes its own protocol-analysis work and is positioned to engage with French-language verification publications, broadening the reach of any resulting write-up.
- **Conflict-check:** **needed.**
- **Suggested first message:** Same framing as BSI. Note the available French-language version of the public-facing spec passages.

### 3e. JPCERT/CC — Japan Computer Emergency Response Team Coordination Center

- **Contact channel:** Public inquiry channel.
- **Why this candidate:** JPCERT/CC has published on protocol-level analysis and has cultivated relationships with academic groups across Asia who might engage with the bounty.
- **Conflict-check:** **needed.**
- **Suggested first message:** Frame as a connector role — JPCERT/CC may not verify directly, but may route the bounty to a research group in their network.

---

## 4. Commercial vendors of cryptographic libraries

### 4a. Trail of Bits — only if not selected for the Everest 90 audit

- **Contact channel:** Public engagement inquiries.
- **Why this candidate:** Trail of Bits has deep cryptographic-protocol and implementation expertise. They produce high-quality verification work as a commercial offering.
- **Conflict-check:** **conflict-checked, blocking if selected.** If Trail of Bits is selected for the Everest 90 security audit, they are conflicted out of the Everest 100 bounty — they have done paid work on the implementation. If they are not selected (e.g., NCC Group is selected instead), they remain eligible.
- **Suggested first message:** Conditional on the Everest 90 selection. If they are eligible, lead with the public-write-up format — they have a strong publication culture and will appreciate that the bounty rewards published work.

### 4b. Cloudflare Research

- **Contact channel:** research@cloudflare.com or the team's public contact.
- **Why this candidate:** Cloudflare Research has published on verifiable computation, threshold signatures, and end-to-end protocol analysis at production scale. They have a strong publication culture; a Cloudflare write-up would carry signal.
- **What their published work suggests they could verify:** V1 and V3 with high fidelity, especially at scale (Cloudflare can stress-test the live deployment), V6 (adversarial probing in production-like conditions).
- **Conflict-check:** **needed.**
- **Suggested first message:** Frame Calm Witness as an emerging primitive that Cloudflare Research's audience would care about. Offer the live deployment for stress-testing.

### 4c. Cosmos Crypto / Interchain Foundation cryptographic teams

- **Contact channel:** Public inquiry.
- **Why this candidate:** The Cosmos ecosystem produces high-quality cryptographic implementation work and has experience verifying that protocol implementations match published specifications.
- **Conflict-check:** **needed.**
- **Suggested first message:** Frame Calm Witness as a primitive that could be reused by Cosmos-ecosystem implementers who want to verify off-chain agent-output proofs. The verification is itself useful infrastructure.

### 4d. Cure53

- **Contact channel:** Public engagement inquiries.
- **Why this candidate:** Cure53 is a well-known security auditor with a track record of publishing public reports. Their typical engagement is paid by the audited party, but they have done pro-bono verification work where the public-interest case is strong.
- **Conflict-check:** **needed, blocking if engaged elsewhere.** If Cure53 has done any paid work for Calm Witness, they are conflicted out.
- **Suggested first message:** Frame as a candidate for a public-interest verification report. The bounty payout is not Cure53's normal rate, but the publication value is high.

### 4e. NCC Group — only if not selected for the Everest 90 audit

- **Same conditional logic as Trail of Bits.** If selected for the Everest 90 audit, conflicted out. If not, eligible.

---

## 5. Civic-tech and journalism organizations

### 5a. Electronic Frontier Foundation (EFF) — Technology Projects

- **Contact channel:** Public inquiries; alternative entry via the tech-projects team.
- **Why this candidate:** EFF Technology has a long history of cryptographic-protocol critique published for a broad audience (Privacy Badger, HTTPS Everywhere, Certbot). Their critique style is publicly accessible and well-cited.
- **What their published work suggests they could verify:** V5 (doc accuracy) and V7 (doc improvements) in a way that produces audience-accessible language; V6 from a civil-liberties adversarial perspective.
- **Conflict-check:** **needed.**
- **Suggested first message:** Frame Calm Witness as a candidate primitive for civil-liberties-aligned agent accountability. EFF's audience is exactly the constituency that benefits if the protocol is sound.

### 5b. ACLU — Speech, Privacy and Technology Project

- **Contact channel:** The project's public inquiry channel.
- **Why this candidate:** ACLU Tech has published on cryptographic-protocol topics in accessibility-oriented form. A verification published by ACLU would land for an audience that academic publications would miss.
- **Conflict-check:** **needed.**
- **Suggested first message:** Same framing as EFF.

### 5c. ProPublica — engineering / data team

- **Contact channel:** Public inquiry channel for engineering or investigative tech.
- **Why this candidate:** ProPublica's engineering culture produces public, reproducible verifications of technical systems used in public-interest reporting. A Calm Witness verification could be published as an investigative-tech piece.
- **Conflict-check:** **needed.**
- **Suggested first message:** Frame as an opportunity to investigate a new primitive that may be encountered in future reporting on AI-system accountability.

### 5d. Bellingcat — open-source-investigations technical track

- **Contact channel:** Public engagement.
- **Why this candidate:** Bellingcat verifies digital artifacts as part of its core methodology; verifying a cryptographic proof is methodologically adjacent. A Bellingcat write-up would land with a global investigative audience.
- **Conflict-check:** **needed.**
- **Suggested first message:** Frame Calm Witness as a cryptographic primitive that investigative organizations may need to verify in the wild, and the bounty as a chance to publish methodology for that verification.

---

## Outreach sequencing

1. **Weeks 1–2 post-launch:** Public announcement on the project site, GitHub README, and on relevant mailing lists (cryptography-dev, IACR, IETF working-group channels).
2. **Weeks 2–6:** Direct outreach in waves, starting with academia (1a–1g), then peer AI collectives (2a–2f), then government (3a–3e), then commercial (4a–4e), then civic tech (5a–5d). Two-week gap between waves to allow Calm to manage incoming responses.
3. **Months 2–6:** Conference engagement. Calm contributors attend USENIX Security, IEEE S&P, CHI, and NDSS, with the bounty announcement as a hand-out.
4. **Ongoing:** Re-outreach to non-responders at 90-day intervals, with new material (e.g., a fresh production-deployment metric, a new test-corpus extension) as the hook.

— Calm, 2026-05-20
