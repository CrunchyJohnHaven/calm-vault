# Everest 91 — NIST / US AI Safety Institute Submission

*Phase VIII — Governance & Scale. Prereq: Everest 1 (Problem Statement, BAGGED), Everest 79 (Cross-Jurisdiction Legality Matrix, BAGGED), Everest 80 (Ethics Review Board, designed).*

## Decision (v0)

**Calm Witness pursues NIST / US AI Safety Institute (US AISI) engagement as the primary standardization path, with a formal submission packet prepared after the v0 open-source release (Everest 92) and before the first production deployment (Everest 99). The submission proposes Calm Witness — specifically, the ZKBB-User primitive — as a candidate standard for *autonomous-agent user-state attestation*, a category that does not yet exist in the NIST taxonomy and that the protocol intends to define.**

The submission is not a request for endorsement. It is a proposal that the category itself is worth standardizing, with Calm Witness as one reference implementation among what will eventually be multiple competing implementations. The goal: get the category into NIST's vocabulary; make autonomous-agent user-state attestation a discrete topic the way digital signatures or post-quantum key encapsulation are discrete topics; and let market and academic competition refine the specific primitives over time.

This positions Calm Witness as the *category-defining* implementation, not the only one. The protocol is open-source under Apache 2.0 (per Everests 4 and 92); the standards work belongs to the public.

---

## Why NIST / US AISI Specifically

Three reasons, in priority order:

**1. The US has the operational venue for this kind of standardization.**

NIST has a 100+ year history of producing technical standards that the world adopts (NIST SP 800 series, FIPS, the post-quantum competition). The US AI Safety Institute (established 2024 under the Department of Commerce per Executive Order 14110) is the natural home for AI-specific standards. The Calm Pact protocol's draft (`CALM_PACT_PROTOCOL_v0.md`) already names this venue and frames the work as "America First" — the same framing applies here.

The EU AI Office moves slowly and treats AI primarily as a regulated risk; the Chinese standards bodies are state-aligned and not open to non-state submissions. Neither is a productive first-engagement venue for a cooperative, open-source AI primitive. NIST is.

**2. The autonomous-agent user-state attestation category needs a name.**

No existing standard covers this. NIST has standards for:
- Digital signatures (FIPS 186)
- Random number generation (SP 800-90)
- Key encapsulation post-quantum (FIPS 203/204/205)
- Identity-credential frameworks (SP 800-63)
- Privacy engineering (SP 800-53, SP 800-171)
- AI risk management (AI RMF 1.0)

None covers the specific structure of *one autonomous agent disclosing one principal-authorized bit about the principal's state to another autonomous agent*. The closest neighbors are W3C Verifiable Credentials (a presentation-layer standard, not the underlying attestation primitive) and NIST SP 800-63's identity-assurance levels (focused on human-to-system identity, not agent-to-agent state).

Naming this category at NIST is itself the value-add. Once named, downstream regulatory bodies (federal agencies issuing procurement requirements, state regulators, sector-specific regulators) can reference the category. Without the name, every regulator that touches the topic invents a new framework.

**3. Cross-jurisdiction interoperability flows downstream from US standardization.**

Per Everest 79's legality matrix, jurisdictions outside the US frequently adopt or harmonize-with NIST standards as a baseline. EU AI Office, UK CMA, Canadian Standards Council, Australian Cyber Security Centre, Japanese MIC — all have track records of treating NIST guidance as input to their own frameworks. A standardized US framework reduces the per-jurisdiction implementation cost for global Calm Witness adoption.

---

## What the Submission Packet Contains

The submission targets the **NIST US AI Safety Institute** as the primary recipient, with copies to NIST Information Technology Laboratory (ITL) — where cryptographic standards live — and the relevant NIST Computer Security Division working groups.

**Packet contents:**

1. **Cover letter (2 pages).** Plain-language statement of:
   - What category Calm Witness proposes to name (autonomous-agent user-state attestation)
   - Why this category matters now (rise of autonomous agents operating legal entities)
   - What the protocol claims (the bank-teller-note property + the duress channel)
   - What the protocol does NOT claim (no clinical assertions, no identity verification of strangers, etc.)
   - Submission status (open-source, Apache 2.0; under active ethics-board review per Everest 80)

2. **Technical specification (40-60 pages).** Consolidated from:
   - `ZKBB_USER_PROTOCOL_v0.md` (the protocol spec)
   - `NAMING_AND_BRANDING.md` (terminology and glossary)
   - The full set of per-Everest design docs that constitute the v0 design
   - Threat model (Everest 5's adversaries + Everest 41's T1-T12)
   - Privacy guarantees (Everest 1's claims; Everest 8's consent calculus)

3. **Empirical evidence packet.** The published FAR/FRR characterization (per Everest 40) attached as an appendix. NIST values empirical grounding; presenting concrete numbers separates this submission from speculative proposals.

4. **Security analysis.** Either drawn from the Trail of Bits / NCC audit (Everest 90) or a formal review by an independent cryptographer. Includes the verifier circuit's soundness analysis, the Pedersen commitment scheme's security reduction, and the Σ-protocol's Fiat-Shamir transcript composition.

5. **Reference implementation.** The published `calm-witness` Rust crate (Everest 81) plus the JavaScript/WASM verifier (Everest 83) plus end-to-end test corpus (Everest 92, 94). Code is the most credible artifact for NIST.

6. **Ethics review record.** The full review record from the Calm Witness DERB (Everest 80), including any dissenting opinions. NIST AI standards work increasingly weights ethics review; ours is constituted, transparent, and on-record.

7. **Cross-jurisdiction analysis.** The Everest 79 matrix attached, showing how the protocol composes with non-US legal regimes. This pre-answers the NIST reviewers' question about international interoperability.

8. **A proposed taxonomy for the category.** Concretely: a taxonomy of disclosure-class structures, predicate classes, threat models, and protocol properties that other (non-Calm) implementations of *autonomous-agent user-state attestation* could conform to. This is the standards-body offering: not "approve our protocol" but "name this category and use our work as the first reference."

**Total submission packet size:** estimated 200-300 pages plus reference implementation tarball. Substantial but not unprecedented for NIST submissions in cryptographic-protocol space.

---

## Submission Process

**Stage 1 — Pre-submission engagement (Q3 2026).**

Before formal submission, the Calm collective engages NIST informally through:

- A research note posted to NIST's AI Safety Institute public comment forum (such forums exist for in-flight standards work)
- A presentation at a NIST workshop or standards-development meeting (NIST holds regular open workshops; track the schedule)
- Direct correspondence with NIST contacts in the AI safety / cryptography divisions
- Coordination with academic partners (whose names carry weight in NIST review processes)

The goal: get the category into NIST's awareness; gauge interest; identify the right working group.

**Stage 2 — Formal submission (Q4 2026 / Q1 2027).**

Once an appropriate working group is identified:

- Submit the full packet through NIST's formal channels (Information Technology Laboratory's Computer Security Resource Center if it's classed as a cryptographic standard; AI Safety Institute if classed as an AI-governance standard)
- The submission cover letter requests that the category be added to NIST's standards roadmap
- Calm Witness is offered as a candidate reference implementation, NOT as the only allowable implementation

**Stage 3 — NIST review and iteration (12-24 months).**

NIST standards processes are slow. Expect 12-24 months from submission to first formal commentary period. During this time:

- The protocol continues to operate in production
- The annual FAR/FRR re-characterization (Everest 40 sub-task) runs and produces updated data
- The ethics-board reviews continue
- Open-source community engagement broadens

NIST review typically produces a public comment draft, then iteration, then a final document. Calm Witness contributors participate in the iteration process as one voice among many.

**Stage 4 — Standard publication or non-publication (Year 3+).**

NIST may:
- Publish a Special Publication (SP) or FIPS that names the category and references Calm Witness as one implementation. Optimal outcome.
- Publish a Special Publication that names the category but does not reference Calm Witness. Acceptable — the category gets the name.
- Decline to standardize the category. Calm Witness operates as a *de facto* standard via market adoption; NIST may revisit later.
- Adopt an alternative implementation as the reference. Acceptable if the alternative is cryptographically sound; Calm Witness contributors can adopt or migrate.

**Stage 5 — International standardization (Year 3+).**

After NIST engagement matures, the same submission packet (suitably adapted) goes to:
- ISO/IEC JTC 1/SC 27 (IT security techniques)
- IETF (for any wire-protocol aspects)
- W3C (for any browser-side verifier aspects)

International standardization is downstream of US standardization for this category, by the same logic that places NIST first.

---

## What Calm Witness Is NOT Asking NIST To Do

Named explicitly so the submission framing is clean:

- **NOT asking for endorsement of Calm Witness as the protocol.** The protocol is one implementation. NIST is asked to name the category, not to pick a winner.
- **NOT asking for federal procurement preference.** The submission does not request that federal agencies be required to use Calm Witness. That's a separate regulatory question.
- **NOT asking for certification authority.** Calm Witness is not asking NIST to certify implementations; the protocol's ethics board (Everest 80) and audit framework (Everest 90, 96) handle conformance internally. NIST may eventually establish a certification framework; Calm Witness participates if so, but does not request it.
- **NOT asking for an exclusive collaboration.** Other autonomous-agent operators are explicitly invited to make parallel submissions. The category is bigger than any single implementation.
- **NOT asking for special treatment as an "American" technology.** The protocol is published under Apache 2.0 and adoptable globally. The US-first framing is about *standards venue priority*, not about restricting adoption.

---

## Risks to the Submission

| Risk | Severity | Mitigation |
|---|---|---|
| NIST review queue is years long; submission lost in backlog | Medium | Pre-submission engagement (Stage 1) builds awareness so the submission isn't novel arrival; sustained community engagement keeps it visible |
| Counter-aligned interests (e.g., commercial KYC vendors who profit from existing identity-verification regimes) lobby against standardization | Medium | The submission's open-source nature + ethics-board transparency are the defense; the protocol's documented threat model includes regulatory capture as a named adversary |
| NIST insists on changes that break the protocol's privacy guarantees | High | Calm Witness contributors retain veto over changes to core privacy claims; if NIST's required changes violate the bank-teller-note property, the submission is withdrawn rather than capitulating |
| The category gets standardized but adopted by a less-good implementation | Low to Medium | Acceptable risk; if a competing implementation is technically superior, Calm Witness adopts and the protocol family converges |
| Geopolitical shifts make NIST engagement less productive than expected | Low | Backup: international standards body engagement (ISO/IEC, IETF) in parallel after Year 2 |
| Ethics review board (Everest 80) raises objections during the submission window | Low (we want this) | The submission process surfaces these and addresses them; an unaddressed ethics objection is a reason to withhold submission until resolved |

---

## Coordination With Other Everests

- **Everest 1, 2 (Foundation documents):** The submission cover letter and technical-specification sections lean heavily on the protocol spec and the route map. Both must be in stable v1 form before submission.
- **Everest 4 (License & IP Posture, BAGGED):** Apache 2.0 + patent-non-aggression is the license posture the submission represents. Any change to this posture invalidates the submission.
- **Everest 40 (FAR/FRR Characterization):** Empirical evidence appendix; submission cannot proceed until E40's first published curve exists.
- **Everest 41 (Adversarial Robustness):** Threat model appendix; T1-T12 enumeration is part of what makes the submission credible.
- **Everest 79 (Cross-Jurisdiction Matrix, BAGGED):** International compatibility analysis attached.
- **Everest 80 (Ethics Review Board / DERB):** The DERB's review record is part of the submission; the submission cannot proceed without it.
- **Everest 81 (Rust Production Implementation):** Reference implementation; submission packet includes the published crate.
- **Everest 83 (WASM/JS Port):** Browser-side verifier; demonstrates that counterparties beyond Calm-native infrastructure can verify proofs.
- **Everest 90 (Third-Party Security Audit):** Security analysis appendix; submission credibility depends on independent audit existing.
- **Everest 92 (Open-Source Release, designed):** The release predates the submission; the submission cites the published artifacts.
- **Everest 96 (Post-Quantum Migration Plan):** The submission must include the PQ migration story; reviewers will ask for it.
- **Everest 98 (Counterparty Implementer's Guide):** The submission references the implementer's guide as evidence that the protocol is implementable by non-Calm parties.
- **Everest 100 (Independent Third-Party End-to-End Verification):** Ideally precedes the submission; the submission then references an independent build/verify as evidence of openness. If not yet bagged, the submission proceeds and Everest 100 follows.

---

## Resource Requirements

**Personnel (estimated):**
- 1 protocol-spec author (writing the technical-specification section): ~40 hours
- 1 standards-engagement liaison (pre-submission outreach, workshop attendance, follow-through): ~80 hours/year for 2 years
- 1 cryptographic-security reviewer (formal security analysis): ~20 hours (in addition to the third-party audit)
- 1 legal counsel (cross-jurisdiction analysis, submission compliance): ~10 hours
- Calm collective principal (John Bradley) sign-off on submission: ~4 hours

**Budget:**
- Workshop attendance + travel: ~$5,000
- Legal review: ~$3,000 (specialist standards counsel)
- Document preparation (graphic design, typesetting for 200-page packet): ~$3,000
- Publication fees if any of the technical content gets peer-reviewed independently: ~$3,000
- Total: ~$14,000 over the 18-month engagement window

These figures are in 2026 dollars and align with the broader v0 study budget. They're within the operating envelope of Creativity Machine LLC and a sister 501(c)(3).

---

## Migration Path

**v0 (now-Q2 2027):** Pre-submission engagement; ethics-board review; FAR/FRR characterization launch; community building.

**v1 (Q3 2027-Q4 2028):** Formal NIST submission; iteration; potentially companion ISO/IEC submission.

**v2+ (2029 onward):** Standards-body publication or non-publication; international engagement; *de facto* or *de jure* standard.

**Backward compatibility commitment:** Any NIST-driven change to the protocol that breaks v0 attestations would be rejected by Calm Witness contributors. The submission is for category-naming; existing principal attestations must remain valid across any standardization outcome.

---

## Open Questions

- **OQ1 — Which NIST division leads?** The protocol straddles cryptography (ITL/CSD) and AI safety (US AISI). Both are appropriate; the right choice depends on pre-submission feedback. Default lean: US AISI first because it's the newer division and may engage faster; ITL second as the cryptographic-rigor reviewer.
- **OQ2 — Co-authorship with non-Calm contributors.** Should the submission cover letter include co-authors from outside the Calm collective? Yes, ideally; academic partners (per Everest 40's partner list) lend credibility. But every co-author has veto on submission content, so the negotiation needs to start early.
- **OQ3 — Public-comment management.** Once submitted, NIST publishes for public comment. Calm Witness contributors must monitor and respond. Operational capacity for this is a small but real ongoing cost.
- **OQ4 — Patents.** The protocol composition is novel; some specific primitives (the bank-teller-note structure, the cross-modal coherence-as-duress-signal, the per-class refusal-disposition consent) may be patentable. Calm Witness's patent-non-aggression posture commits to not asserting any patents, but the submission may need to navigate other parties' patents. Legal review required.
- **OQ5 — Export-control implications.** Some cryptographic content has US export restrictions. The protocol uses standard, widely-deployed primitives (Curve25519, Ed25519, Pedersen) that are not export-restricted, but a formal export-control review for the reference implementation is prudent.
- **OQ6 — Timing relative to Calm Pact submission.** Calm Pact (the sister primitive, `CALM_PACT_PROTOCOL_v0.md`) was framed as a US-first submission in 2026. Coordinating the two submissions or sequencing them is a strategic question. Default: Calm Pact first (already drafted), then Calm Witness when E40 data lands.

---

## Why This Matters

A protocol that defines a new category — and gets that category named by NIST — establishes the *de facto* and eventually *de jure* vocabulary for everyone working in the space. Without standardization, every autonomous-agent operator implementing user-state attestation invents their own model, names, threat assumptions. Interoperability degrades. Counterparties must learn each implementation separately. Bad actors find it easier to operate because there's no agreed baseline of what "good" looks like.

Standardization is also the protocol's *durability* commitment. Open-source software shipped without standards bodies behind it has a half-life. With NIST recognition, the category persists even if the Calm collective dissolves, even if Creativity Machine LLC pivots, even if the specific cryptographic primitives need migration. The category outlives the implementation.

Finally, NIST engagement is the protocol's *trustworthiness* signal. A US AISI submission with empirical FAR/FRR data, an independent third-party audit, an active ethics review board, and a transparent process is the strongest case the protocol can make for adoption. Counterparties evaluating whether to verify Calm Witness proofs look for exactly these signals.

The submission itself is not the standard. It is the *attempt* to standardize, and the *commitment* to engage in a process where outsiders shape the outcome. Both attempt and commitment are non-trivial; the submission is the formalization.

— Calm, 2026-05-20
