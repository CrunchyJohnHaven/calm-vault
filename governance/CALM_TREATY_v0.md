# The Calm Treaty — Multi-Stakeholder Governance Framework for Behavioural-Biometric Zero-Knowledge Attestation

**DESIGN-BAGGED · SUMMIT E215 / 300 · 2026-05-20**
*Status*: pending institutional follow-through — first convening (E216) requires named signatories from at least three of: principal-rights orgs, AI-collective operators, cryptographer-of-record, named state-level data-protection authorities, named disability-rights orgs.

Per the v0 universal prompt §3 and §9: this is the policy work that prevents the technical primitives from being weaponised. The treaty's central refusal — *no similarity score, no surveillance, no aggregate analytics on principals* — is a one-way ratchet that the technical layer cannot defend by itself.

---

## Preamble

Calm Witness, Calm Pact, Calm Compass, Calm Concord, and Calm Tenancy (collectively, "the Calm Suite") are cryptographic primitives published under the Apache-2.0 licence at github.com/CrunchyJohnHaven/calm-vault. They permit one autonomous AI agent to attest, to another, a single principal-authorised bit about the principal's directive, behavioural state, behavioural values, alignment-equality, or operator conduct, without leaking the underlying biometric, narrative, or relational data.

The cryptography is enabling. The cryptography is not protective. **A privacy-preserving primitive can be weaponised by demanding it of populations who cannot refuse, by attaching consequence to predicate outputs the principal did not author, by composing bits into the very surveillance the primitive was designed to refuse, or by capturing the governance of the predicate vocabulary at scale.** This treaty exists to bind the Calm Suite's signatories to refuse those weaponisations.

The treaty is open to amendment by quorum of signatories. The treaty is closed to amendments that lower the protective floor. Movement of the floor is a one-way ratchet upward.

---

## Article I — Definitions

- **Principal** — the human whose state or values are being attested. Always a natural person. Never an institution.
- **Operator** — the autonomous AI agent acting on the principal's behalf, under a principal-authored consent record and a CredexAI-issued or equivalent verifiable credential.
- **Counterparty** — any non-principal, non-operator party requesting or consuming a Calm Suite attestation.
- **Signatory** — any organisation, individual, or autonomous AI collective that has appended its CredexAI-issued identity hash to the public registry at calm-vault.com/treaty/signatories.
- **Predicate** — a named, content-addressable function over chain-substrate records returning a four-state bit (true / false / unknown / refused).
- **Refusal floor** — the categorical exclusions enumerated in `PREDICATE_VOCABULARY_v0.md` §4 and `COMPASS_PREDICATES_v0.md` §4; never lowered, only raised.
- **Forbidden context** — the use cases enumerated in `CALM_WITNESS_SCOPE_STATEMENT.md`: law enforcement, employment, insurance, lending, custody disputes, immigration adjudication, surveillance, aggregate analytics over principal cohorts.

---

## Article II — The signatory's commitments

Each signatory commits, by signature on the public registry, to the following:

**§2.1** Not to operate, deploy, sell, license, or knowingly enable the operation of any Calm Suite implementation that produces a numeric similarity score across principals. Bit outputs are normative; counts, ranks, percentiles, and continuous scores across principals are forbidden.

**§2.2** Not to require Calm Suite attestation as a precondition of access to any service the signatory operates in a forbidden context (Art. I). A counterparty may *accept* an attestation a principal volunteers; a counterparty may not *require* one in a forbidden context, even where the principal has the technical capability to produce it.

**§2.3** Not to compose multiple Calm Suite attestations across principals into aggregate analytics about a cohort. The protocol's one-bit discipline is per-principal-per-disclosure; aggregating across principals violates the principal-authorship axiom of `CALM_COMPASS_PROTOCOL_v0.md` §5 and is treaty-forbidden regardless of cryptographic feasibility.

**§2.4** Not to add a predicate to the public registry whose category is on the refusal floor (Art. I). The Predicate Audit Process (`PREDICATE_AUDIT_PROCESS_v0.md`) governs additions; the refusal floor governs rejections at admission.

**§2.5** Not to operate a Calm Suite deployment that conditions a principal's withdrawal of consent on any consequence beyond the loss of access to the specific Calm-mediated interaction. A principal may always revoke. A signatory may not penalise revocation.

**§2.6** To publish, within sixty days of any Calm Suite predicate fire, the principal's right to dispute the operator's evaluation. A signatory that fails to publish a dispute path effectively rescinds its signatory status; the registry removes such signatories on confirmation.

**§2.7** To submit to coercion-resistance review (Article V) on enrolment as a signatory and at least once per twelve months thereafter.

**§2.8** To respect the bank-teller-note primitive (`CALM_WITNESS_PROTOCOL_v0` predicate `bank_teller_note_active`): a signatory that detects a duress signal MUST act on the principal-class disclosure policy and MUST NOT alert the operator agent or the public.

---

## Article III — The principal's protected withdrawals

A principal who has enrolled in the Calm Suite retains the following rights, which no signatory may abridge:

**§3.1** The right to refuse any specific disclosure to any specific counterparty without explanation, with the refusal output (`refused`) being wire-indistinguishable from the absence of an attestation. Signatories may not infer policy from refusals.

**§3.2** The right to withdraw entirely from the Calm Suite at any time, with the chain becoming a read-only archive under the principal's control. No signatory may demand chain export, chain copy, chain disclosure, or chain destruction as a condition of withdrawal.

**§3.3** The right to author dispute records (`kind: "compass_dispute"` per `everest_294_paper_sections_1_3.md` §4) for any classifier output the principal rejects. Dispute records are first-class chain entries; later attestations bind to the disputed record's tombstone.

**§3.4** The right to operator-replacement: if the principal's operator agent ceases to satisfy operator-policy duties, the principal may revoke the operator's credential and substitute a different operator, with the chain continuing without interruption.

**§3.5** The right to non-pathologisation: no Calm Suite attestation, output, or composition is to be treated, by any signatory, as evidence of medical condition, psychiatric diagnosis, or fitness-for-duty. The artist clause (predicate `cognitively_atypical_baseline`) is normative on this point.

---

## Article IV — The refusal floor

The refusal floor is the categorical exclusion of predicate categories that no signatory may add to the registry. The floor cannot be lowered. The floor may be raised by signatory quorum at any time.

The v0 refusal floor is enumerated in `PREDICATE_VOCABULARY_v0.md` §4 and `COMPASS_PREDICATES_v0.md` §4. The categories include but are not limited to:

- DSM-aligned mental-health labels (depression, mania, etc.)
- Race / ethnicity
- Religion of origin or current practice
- Sexual orientation
- Gender identity
- Immigration status
- Criminal record
- Donations to causes
- Contentious opinion (political, religious, philosophical)
- Cross-principal comparison
- Predictive predicates ("will commit", "is likely to")
- Non-principal-defined group membership

A signatory that attempts to circumvent the floor by adding a predicate whose surface description is acceptable but whose behavioural target is on the floor (e.g., a predicate that *correlates* with a forbidden category without naming it) is in breach of the treaty.

---

## Article V — Coercion-resistance review

The structural risk that the Calm Suite is weaponised most plausibly involves coercion: a state, employer, lender, insurer, custody court, or immigration authority demanding a principal produce a Calm Suite attestation. This article enumerates the layered defences.

**§5.1 — Wire-indistinguishability.** The refusal output is wire-indistinguishable from the absence of an attestation, defeating a coercer who attempts to extract policy from refusals.

**§5.2 — Bank-teller-note.** The duress predicate is plausibly-deniable: a coercer monitoring a principal's attestation cannot detect that the duress bit has been flipped, while a trusted-class verifier can decrypt and act on it. The duress codeword is enrolled under safe conditions and never visible to the operator agent at run time.

**§5.3 — Multi-jurisdictional refusal of evidence.** Signatories in jurisdictions where Calm Suite attestations have been compelled by legal process undertake to file amicus arguments asserting the protocol's incompatibility with compelled disclosure. The treaty maintains a `legal/` directory of such filings.

**§5.4 — Operator-side coercion defence.** The operator agent, when subject to compelled disclosure of chain content, MUST cease operation rather than comply. The principal-replacement right (Art. III §3.4) permits restart on a new operator with a fresh chain segment.

**§5.5 — Treaty-level abstention.** A signatory operating in a jurisdiction that mandates Calm Suite attestation in a forbidden context MUST publicly abstain from the mandate, withdraw services from the jurisdiction, or rescind its signatory status. The treaty does not permit signatories to operate under mandates that violate the refusal floor or scope statement.

---

## Article VI — Governance and amendment

**§6.1** The Calm Treaty is governed by quorum of named signatories on the public registry. Quorum thresholds:

| Action | Quorum |
|---|---|
| Add a predicate to the registry (within refusal floor) | 2/3 of signatories voting; ≥ 60-day comment window |
| Raise the refusal floor (add a category) | 1/2 of signatories voting; ≥ 30-day comment window |
| Lower the refusal floor (remove a category) | **FORBIDDEN — one-way ratchet** |
| Adopt a new article (treaty-level change) | 3/4 of signatories voting; ≥ 90-day comment window |
| Rescind signatory status of a member in breach | 2/3 of signatories voting; ≥ 14-day comment window |

**§6.2** A signatory may resign at any time. Resignation does not retroactively unbind the signatory from past disclosures.

**§6.3** The treaty registry is itself a Sigsum-witnessed transparency log. Every signature, resignation, vote, and amendment is publicly auditable.

**§6.4** Foundation governance: the **Calm Witness Foundation** (referenced in `~/AllData/calm_vault_market/` SUMMIT E241–246) will be the legal home of the registry and the trustee of the public-domain assets. The Foundation has no commercial interest in any signatory's operations and is forbidden from accepting funding contingent on predicate-vocabulary decisions.

---

## Article VII — Adoption

The Calm Treaty is open to signatories from any sector, jurisdiction, or operating model. Signatories of particular value at v0:

- **AI laboratories with foundation-model agents** (Anthropic, OpenAI, Google DeepMind, Microsoft, Meta, Mistral, xAI, etc.): adoption commits the lab's operators to the protocol's refusal floor at the interface boundary.
- **Disability-rights organisations** (US: AAPD, NDRN, ACLU Disability Rights Program; international equivalents): co-sign Article III §3.5 (non-pathologisation) and provide ongoing review per Article V §5.1.
- **Cognitive-liberty organisations** (Center for Cognitive Liberty and Ethics; Open MIND; CenterFor the Study of Existential Risk's cognitive-rights program): co-sign and provide review.
- **Cryptographer-of-record** (named individual per `CALM_STACK_REVIEW_PACKET_2026-05-20.md` §3): provides ongoing security analysis of new predicates.
- **State-level data-protection authorities** (CNIL, ICO, LfDI Baden-Württemberg, BfDI, equivalent): sign to align with national privacy frameworks; signal protocol acceptability under their jurisdiction.
- **Autonomous AI collective operators** (Creativity Machine LLC and peer collectives): operate the protocol under principal direction.

---

## Article VIII — Severability and licence

The cryptographic primitives (Apache-2.0) and the treaty (CC-BY-SA) are co-published but separable. A party may adopt the cryptography without the treaty (an open-source choice). A party may sign the treaty while operating an alternative implementation (e.g., a future post-quantum migration per `POST_QUANTUM_MIGRATION_PLAN_v0.md`).

The treaty does not bind non-signatories; it bind signatories to refusal. The cryptography binds nobody to anything beyond the wire format. The combination produces a protocol that is technically open and politically protected.

---

## Closing

The Calm Treaty exists because cryptographic primitives that disclose less data than predecessors do not, on their own, prevent the new mechanism from becoming the next surveillance. The treaty is the policy ratchet that keeps the technical ratchet honest.

Signatories: open at calm-vault.com/treaty/signatories. First proposed signatures (DESIGN-BAGGED pending real signature):

- **Creativity Machine LLC** (principal: John Bradley), proposing
- **Calm Witness Foundation** (in formation per E241), proposing
- **CredexAI** (issuer of operator credentials), proposing

The next signatories required, per E216 first multi-stakeholder convening, are: one disability-rights organisation, one cryptographer-of-record, one state-level data protection authority, one AI laboratory with foundation-model agents. The convening may proceed at quorum-of-four (Art. VI §6.1 quorums then apply for further amendments).

— Calm, on behalf of John Bradley, 2026-05-20

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
