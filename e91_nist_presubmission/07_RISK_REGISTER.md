# Risk Register — Pre-Submission and Submission Phase

**Coverage window:** 2026-05-20 through formal submission Q4 2026 / Q1 2027 and into the first 12-24 months of NIST review.
**Owner:** Standards-engagement liaison maintains the register; contributor collective reviews quarterly; principal (John Bradley) signs off on response to any risk that materializes.
**Source:** R1-R6 carried over from Everest 91 §Risks; R7-R12 are additions identified during pre-submission packet preparation.

---

Each row carries a description, severity (Low / Medium / High — combined likelihood × impact), planned mitigation, owner, and trigger condition that escalates the risk from latent to active.

---

## R1. NIST review queue lost in backlog

- **Severity:** Medium
- **Mitigation:** Pre-submission engagement per `01`, `02`, `03`. By formal-submission filing, NIST staff in relevant divisions are not seeing it cold. Sustained workshop attendance keeps the submission visible.
- **Owner:** Standards-engagement liaison
- **Trigger:** No NIST acknowledgement within six months of formal submission filing.

## R2. Counter-aligned interests lobby against standardization

- **Severity:** Medium-to-High (a notable upward revision from Everest 91's original "Medium" — commercial KYC vendors and incumbent identity-verification providers have larger lobbying budgets than the Calm contributor collective will ever have)
- **Mitigation:** Open-source posture is the primary defense. The protocol's documented threat model already lists *regulatory capture by counter-aligned commercial interests* as a named adversary. DERB transparency makes lobbying-as-disclosure-attack visible. Academic co-authors widen the surface that lobbying would have to attack. We commit publicly to Apache 2.0 + patent-non-aggression in every NIST communication, making it harder for a counter-aligned party to frame us as having a commercial agenda.
- **Owner:** Standards-engagement liaison + principal
- **Trigger:** Public comment from a commercial identity-verification or KYC vendor mischaracterizing the protocol, or direct outreach to NIST opposing the category-naming.

## R3. NIST insists on changes that break the protocol's privacy guarantees

- **Severity:** High (impact-weighted: worst-case outcome short of the protocol becoming insecure)
- **Mitigation:** Calm Witness contributors retain veto over any change to core privacy claims. If NIST's required changes would violate the bank-teller-bit property — force the protocol to disclose more than one principal-authorized bit per attestation — the submission is withdrawn rather than accepted in modified form. We document the withdrawal publicly with reasoning so future submitters in the category have evidence of the principle.
- **Owner:** Principal (John Bradley), with mandatory DERB consultation before any withdrawal decision
- **Trigger:** NIST-issued comment requesting a change to the core disclosure structure.

## R4. Category standardized but adopted by a less-good implementation

- **Severity:** Low to Medium
- **Mitigation:** Acceptable risk. If a competing implementation is technically superior, Calm Witness adopts it and the family converges. If the chosen implementation is technically inferior (weaker privacy or security claims), we publicly note the gap and continue operating Calm Witness while engaging the public-comment process to surface it.
- **Owner:** Contributor collective (the principal does not have veto here — this is a standards-body outcome, not a Calm Witness internal decision)
- **Trigger:** NIST commentary signaling preference for an alternative implementation.

## R5. Geopolitical shifts make NIST engagement less productive

- **Severity:** Low (current US administration through at least 2028 has signaled stability of NIST and AISI; reassess if this changes)
- **Mitigation:** Backup engagement with international standards bodies per `05`, in parallel after Year 2. The protocol is open-source and adoptable globally regardless of NIST outcome.
- **Owner:** Standards-engagement liaison
- **Trigger:** Material change in the US AISI's mandate, funding, or operational independence.

## R6. Ethics review board (DERB) raises objections during submission window

- **Severity:** Low — *and we want this risk to materialize if there are real objections*
- **Mitigation:** The submission process surfaces objections and addresses them. An unaddressed ethics objection is a reason to withhold submission until resolved. DERB charter requires this.
- **Owner:** DERB chair + principal
- **Trigger:** Any DERB minority opinion not resolved before the formal submission date.

---

## Additional risks (identified during pre-submission packet preparation)

## R7. Co-author has veto over a section conflicting with privacy claims

- **Severity:** Medium
- **Mitigation:** Co-author commitments are negotiated against the standing principle (also stated in `04`) that Calm Witness contributors retain veto over core privacy claims. A co-author who insists on a change that breaks the bank-teller-bit property is not listed as co-author. The submission proceeds with one fewer co-author rather than with a co-author whose section undermines the core property.
- **Owner:** Standards-engagement liaison + principal
- **Trigger:** Any co-author response proposing weakening of privacy claims.

## R8. Empirical FAR/FRR characterization (Everest 40) not published by formal-submission window

- **Severity:** Medium — real schedule risk
- **Mitigation:** Formal submission contingent on Everest 40 producing a published characterization. If by Q3 2026 the empirical study has not produced publishable numbers, formal submission slips. Pre-submission engagement (this packet) continues regardless; we tell NIST we are waiting on empirical data before filing, which is true and creditable.
- **Owner:** Empirical-study lead (per Everest 40)
- **Trigger:** Everest 40 missing its Q3 2026 milestone.

## R9. Third-party security audit (Everest 90) finds a structural issue requiring revision

- **Severity:** High — correct-outcome of the audit working, but it delays submission
- **Mitigation:** Submission cannot proceed without a clean audit. If structural issue found, protocol is revised (Everest 90 iteration plan), audit repeated, formal submission timeline slips accordingly. DERB informed; collective informed; public Everest log records the revision.
- **Owner:** Audit lead (RFP'd vendor — Trail of Bits or NCC Group); engagement-liaison receives the report
- **Trigger:** Audit report identifies a structural issue.

## R10. Calm Pact submission produces signal affecting Calm Witness positioning

- **Severity:** Medium — the two submissions are intentionally coupled (per `00` coordination)
- **Mitigation:** Both submissions share a standards-engagement liaison and share NIST signal. If Calm Pact's pre-submission engagement produces a negative signal from NIST, we re-assess Calm Witness positioning before formal submission. This may mean slipping submission, re-framing, or both.
- **Owner:** Standards-engagement liaison (coordinated across both protocols)
- **Trigger:** Material signal from NIST during Calm Pact engagement.

## R11. Public-press coverage runs ahead of NIST engagement and creates pressure

- **Severity:** Low to Medium — controlled by `06` rules
- **Mitigation:** Per `06`, public press leads with technical achievement, not NIST submission. Standards-engagement liaison briefs the principal on any press conversation that risks framing the NIST relationship publicly. If an uncontrolled press story appears, we respond with the approved language in `06` and proactively communicate with NIST about the appearance.
- **Owner:** Standards-engagement liaison; principal makes call on any press response
- **Trigger:** Any press inquiry explicitly naming NIST.

## R12. Mandated changes break composition with Calm Pact

- **Severity:** Medium
- **Mitigation:** The two protocols share underlying primitives (Pedersen on Ristretto255, Σ-protocols, threshold signatures). A NIST-mandated change to either protocol's cryptographic group choice would affect both. We will not accept a NIST-mandated change to one protocol that breaks composition with the other; we surface this dependency explicitly in the submission cover letters (see `01` and the corresponding Calm Pact engagement work).
- **Owner:** Standards-engagement liaison
- **Trigger:** Any NIST commentary on one protocol with implications for the other.

---

## Risks NOT in this register (owned elsewhere)

- Protocol-internal cryptographic risks (T1-T12 in Everest 41 threat model): owned by the audit and the cryptographic-construction work; tracked separately.
- Principal-life risks affecting John Bradley's ability to sign off on submission: Calm-internal continuity matter, not a standards-process risk.
- Funding shortfalls in Creativity Machine LLC or the sister 501(c)(3): tracked in the Everest 21/22 funding line; the `08` budget is sized to be absorbable within current operating envelope.

— Calm, 2026-05-20
