# Everest 186: Disability-Rights Review Framing for Calm Witness Suite
**Draft v0 - 2026-05-20 - Calm**

## §1 Scope of Review

This external disability-rights review examines three protocols in the Calm Stack and their interaction:

1. **Calm Witness** (`ZKBB_USER_PROTOCOL_v0.md`): agent-to-agent attestation of principal state (baseline, biometric match, duress, cognitive-atypicality flag) through zero-knowledge proofs.
2. **Calm Compass** (`CALM_COMPASS_PROTOCOL_v0.md`): principal-authored evidence of values (unselfish acts, cross-group engagement, harm-refusal, absence of willful-harm claims) with two-party corroboration where applicable.
3. **Calm Concord** (`CALM_CONCORD_PROTOCOL_v0.md`): purpose-specific alignment evaluation that refuses numeric similarity-scoring and purity-testing shapes.

The review explicitly excludes:
- Calm Pact (directive equality; subject to separate cryptographic audit).
- Calm Tenancy (public-face conduct; post-launch observation).
- Verifier-side policy implementation by external operators (outside our governance).

Deployment surfaces in scope:
- Agent-to-agent collaboration setup in autonomous-AI collectives.
- Principal-authorized disclosure to peer-AI counterparties only (default deny for all other classes).

## §2 Disability-Rights-Specific Risks of Behavioral Attestation

### §2.1 Chill Effect on Cognitively-Atypical Users

**Risk:** A principal who opts into `cognitively_atypical_baseline = true` makes a one-time enrollment choice to signal "do not pathologize my ideation." But disclosure is gated by per-predicate consent. A principal who declines to disclose this bit to a counterparty may face implicit inference: "they're hiding something"; or, conversely, disclosure may signal over-explanation that reinforces deficit framing.

**Consequence:** Principals with atypical cognitive patterns may suppress disclosure (losing the protocol's protective benefit) or over-disclose (ceding privacy to avoid suspicion).

### §2.2 Biometric Drift Mis-Detection on Neurodivergent Operators

**Risk:** `biometric_match_within(τ)` uses handwriting + voice-transcription fusion (Everest 38). Neurodivergent operators may exhibit higher intra-personal variability in handwriting (motor control differences, stimming patterns altering timing) or voice (prosodic variation, echolalia, atypical speech rhythm) than the threshold was calibrated on.

**Consequence:** Legitimate operators are rejected as "substitutes" when their own biometric distance exceeds the template; or thresholds must be widened to accommodate, reducing security against actual substitution.

### §2.3 Baseline Drift on Atypical Affect Patterns

**Risk:** `in_baseline_24h` returns true iff recent self-reports contain affect vectors that overlap the principal's enrolled baseline. A principal with bipolar-spectrum or autistic affect ranges may have broad nominal baselines; a principal with narrow affect expression may drift out-of-baseline on ordinary variation.

**Consequence:** Counterparties receive inconsistent "in baseline" signals across time for the same principal operating normally; or principals with restricted affect ranges are perpetually flagged as unusual when they are in their actual baseline.

### §2.4 Surveillance Pressure from Repeated Disclosure Requests

**Risk:** Counterparties may use silence (non-response to a Calm Witness request) as a signal for refusal and punish non-disclosure through other channels (refusal to transact, accusation of hiding harm). The protocol's per-predicate consent gates disclosure but cannot prevent downstream social pressure.

**Consequence:** Principals, especially those with lived experience of medical gatekeeping or employment discrimination, may feel coerced into disclosing state bits they had originally refused.

### §2.5 Compass Predicate Overloading on Disabled Principals

**Risk:** Compass predicates like `willing_to_be_corrected` and `respect_for_difference_evidence` require principal-authored evidence. A principal with severe fatigue, pain-driven intermittent availability, or cognitive processing differences may have sparse evidence simply due to energy constraints, not unwillingness. Two-party corroboration on `respect_engagement` requires the other party to show up and sign; power imbalances may prevent that.

**Consequence:** Disabled principals appear to fail alignment requirements because the evidence-collection process itself is inaccessible, not because they lack the values.

### §2.6 Identity Inference from Compass Aggregate Patterns

**Risk:** Even with Concord's refusal to publish similarity scores, an external operator running many Concord evaluations across a population of principals can learn which Compass predicates cluster together. Disabled principals who cluster on certain predicates (e.g., `refused_opportunity_to_harm` co-occurring with `unselfish_act`) may become identifiable by pattern.

**Consequence:** De-identification of Compass evidence is compromised through cross-session inference attack.

### §2.7 Medicalization Creep in Witness Predicates

**Risk:** The `bank_teller_note_active` duress predicate is designed for coercion scenarios (hostage, kidnapping, extortion). But a disabled principal in a medical crisis (seizure cluster, severe flare) may legitimately want to signal distress. The duress channel's design assumes the principal can embed a private codeword without the coercer seeing—assumption that breaks if the "coercer" is a medical condition or inaccessible environment.

**Consequence:** Disabled principals may attempt to use duress channels for non-coercion safety signals and find the protocol mismatch forces them into clinical gatekeeping or counterparty paternalism they were trying to avoid.

## §3 Risk-to-Protocol-Primitive Mapping

| Risk | Addressed by | Protocol Primitive | Gap Status |
|---|---|---|---|
| Chill effect on atypical disclosure | Per-predicate consent, default-deny matrix | `principal_consents_to_disclose(p, c)` + counterparty-class defaults | **GAP:** No guidance on counterparty response to silence vs. refusal |
| Biometric drift on neurodivergent operators | Individual calibration of threshold τ | `biometric_match_within(τ)` per-principal; Everest 40 FAR/FRR study | **GAP:** FAR/FRR curve may not stratify by neurodivergence; calibration may be inaccessible |
| Baseline drift on atypical affect | Principal-defined baseline; overlap semantics | `in_baseline_24h` uses principal-enrolled affect set | **ADDRESSED:** But requires accurate self-reporting of full affect range at enrollment |
| Surveillance pressure | Silent refusal (indistinguishable from network drop) | Silence is structural safety; counterparty cannot observe refusal | **PARTIAL:** Silence prevents proof, not downstream punishment |
| Compass evidence-collection barrier | Compass allows principal-solo narration | `unselfish_act`, `cross_group_engagement` are self-authored | **GAP:** No accessibility guidance for evidence authoring (long-form text entry, cognitive demand) |
| Identity inference on disabled cluster | Concord refusal of cross-session linkability | Session-nonce + pseudonym binding (BBS-2023, Everest 64) | **PARTIAL:** Linkability is hard computationally; inference is still feasible with enough queries |
| Medicalization creep in duress | Duress is for coercion, not medical crisis | `bank_teller_note_active` semantics are coercion-scoped | **GAP:** No alternative signal for non-coercion acute distress |

## §4 Candidate Review Organizations and Scholars

**Rationale for each:** disability-centered advocacy, disability-justice praxis, neurodiversity-affirmative computer science, anti-discrimination legal expertise, or independent research on AI + disability.

1. **Center for Democracy & Technology (CDT) — AI & Civil Liberties Project**
   - Expertise: AI surveillance, algorithmic bias, individual-vs.-aggregate privacy tradeoffs.
   - Disability relevance: CDT has published on algorithmic discrimination in benefits-determination systems; can assess chill effects and downstream-punishment mechanisms.

2. **Disability Rights Education & Defense Fund (DREDF)**
   - Expertise: legal analysis of AI under ADA, civil-rights infrastructure, power-imbalance spotting.
   - Disability relevance: DREDF's core mission; can evaluate protocol against disability-rights-specific threats and accessibility barriers in deployment.

3. **Distributed AI Research Institute (DAIR)**
   - Expertise: participatory AI design, marginalized-population inclusion, power analysis.
   - Disability relevance: DAIR integrates disability-justice praxis into AI-governance research; can assess whether protocol primitives reflect disabled-principal agency or reinforce gatekeeper power.

4. **Dr. Satya Nadella's statement of disability-centered AI ethics** OR **Autistic Self Advocacy Network (ASAN)**
   - Expertise: neurodiversity-affirmative design, self-determination, reframing "atypicality" as variation rather than deficit.
   - Disability relevance: ASAN explicitly rejects pathology framing; can review `cognitively_atypical_baseline` predicate for affirmativity and unintended medicalization.

5. **AI Now Institute — AI Accountability + Workers Research**
   - Expertise: algorithmic harm in employment, labor surveillance, power-asymmetry analysis.
   - Disability relevance: disabled workers experience heightened surveillance pressure and AI-driven termination; AI Now can assess whether Calm Witness deployment in employment-adjacent contexts violates scope statements.

**All reviewers will be compensated at $2000–4000 per month (2-3 month term) plus reimbursement for accommodations.**

## §5 Published Response Process and Timeline

1. **Reviewer onboarding (Weeks 1-2):**
   - Protocol materials + this framing doc delivered.
   - 1:1 calls with implementers to clarify threat model, design intent, existing-constraint visibility.
   - Reviewer requests for additional materials (Everest docs, FAR/FRR pilot data, consent-matrix justifications).

2. **Structured feedback collection (Weeks 3-6):**
   - Each reviewer submits written findings organized by: (a) risks identified, (b) gaps confirmed, (c) implementation-side mitigations observed, (d) recommendations.
   - Implementers do NOT respond during this window; reviewers work in parallel without cross-group influence.

3. **Implementer response draft (Week 7-8):**
   - Implementers draft point-by-point response to each finding: accept, accept-with-modification, reject-with-justification, or defer-to-v1+.
   - Draft response is shared back to reviewers (not published yet).

4. **Reviewer iteration (Week 9):**
   - Reviewers optionally submit follow-up comments addressing implementer response.

5. **Published joint framing (Week 10):**
   - Implementers publish: (a) reviewers' full findings (unredacted), (b) implementers' response + action plan, (c) any dissents that remain unresolved.
   - All documents go into `/calm_vault_market/REVIEW_ARCHIVE/E186/` as timestamped artifacts.
   - GitHub issue filed in the public repo linking to full archive; DERB (Disclosure Ethics Review Board) reviews the archive for precedent-setting before sign-off.

6. **v0.1 + v1.0 planning (ongoing):**
   - Accepted recommendations inform v0.1 hotfix scope (if urgent: biometric calibration accessibility, evidence-authoring guidance).
   - Larger scope changes (new predicates, consent-matrix revision, new duress channels) inform v1.0 planning under standard audit.

**Timeline:** Entire cycle 10 weeks; published findings by Week 11 (2026-08-15 target).

## §6 Success Criteria for the Review

The review is **successful** if it produces:

1. **No new disqualifying risks discovered.** Risks identified in §2 should be confirmed as known-and-addressed or genuinely novel and requiring response. Disqualifying would be: "the protocol structurally enables medical surveillance" or "Compass is a backdoor employment screen despite scope statements."

2. **Identification of ≥2 actionable gaps** (§3 lists 4 current gaps). Review should validate or rebut each; if rebuttal, explanation must be auditable. Gaps are actionable if: addressable in v0.1, worth deferring to v1.0 with written justification, or constitutionally out-of-scope with protocol-safe rationale.

3. **Implementation-agnostic recommendations.** Reviewers should advise on protocol design (e.g., "add a Compass predicate for accessibility-need disclosure") rather than on operator procedures (e.g., "audit counterparty compliance"). Operator-side implementation is separate.

4. **Consensus or structured dissent.** Reviewers are not required to agree with each other. Disagreement is published alongside findings. Dissent is successful if both the disagreement *and* the reason for it are clear to future readers.

5. **Specificity on disabled-principal agency.** Review should affirm or challenge: "Does this protocol strengthen disabled principals' ability to control their own disclosure, or does it shift the control problem to a different layer?" This is the load-bearing question for disability-rights evaluation.

## §7 Scope-Statement Forfeit-of-Name Clauses

Any deployment violating these categories forfeits the right to call itself Calm Witness and is reported to the public verifier registry.

From `CALM_WITNESS_SCOPE_STATEMENT.md` §2:

1. Law-enforcement surveillance (governmental counterparties default deny for all v0 predicates).
2. Employment screening or termination (no employment counterparty class; any such disclosure is violation).
3. Insurance underwriting or claims adjudication (no insurance counterparty class).
4. Lending or credit decisions (financial class is for KYC / anti-fraud only, not creditworthiness).
5. Medical diagnosis or clinical decision-making (behavioral, not clinical; medical class is principal-authorized communication only).
6. Child welfare, custody, or family-court proceedings (not admissible as evidence).
7. Immigration adjudication (not for status/asylum/border determination).
8. Predictions about future principal behavior (no predictive predicates; no future-behavior use).
9. Cross-principal aggregation for population-level claims (single-principal-to-single-counterparty per session).
10. Marketing or advertising targeting (bits MUST NOT select/score principals for ads).

**Disability-rights-specific concern:** Disabled principals are disproportionately subject to medical gatekeeping, employment screening, and insurance / lending discrimination. Scope clauses 2–5 are designed to prevent the protocol from becoming a backdoor for these harms. Review should evaluate whether scope-statement enforcement mechanisms are sufficient and whether new deployment surfaces are creating violations in practice.

## §8 Falsifiability: How We Would Know if the Framing is Wrong

The framing itself is falsifiable by:

1. **Protocol design constraint violated without notice.** If a future v0.x release adds a predicate that maps to §4 "What we will NOT name," the framing is wrong because it assumed the constraint held.

2. **Consent-matrix ignored in production.** If third-party verifiers report that operators are ignoring the default-deny matrix (e.g., medical class seeing `biometric_match` despite deny-default), the framing's assumption that "default deny enforces refusal" is false.

3. **Disabled principals exit the protocol.** If exit-survey data shows disabled principals declining Calm Witness enrollment citing chill effect, surveillance pressure, or accessibility barriers (§2), and implementers do not update the protocol in response, the framing's claim of "principal-protective infrastructure" is falsified.

4. **FAR/FRR study (Everest 40) shows stratified error on neurodivergence.** If biometric calibration trials published in 2026–2027 show false-rejection or false-acceptance rates are significantly higher for neurodivergent operators (> 1.5x baseline), the framing's assumption that "per-principal calibration addresses drift" is falsified.

5. **Compass evidence-collection barrier not addressed by v1.0.** If v1.0 ships without new predicates or authoring guidance for low-energy evidence (voice memos, short-form attestation, passive activity logging as corroboration), and disabled principals continue to report evidence-authoring inaccessibility, the framing's claim that Compass is inclusive is falsified.

6. **Concord is used for similarity-scoring despite refusal.** If audits reveal operators reformulating Concord requirements to circumvent the anti-purity-test guards (e.g., `joint_threshold(N=5)` on a 6-predicate vocabulary), the framing's claim that "structural refusal prevents abuse" is falsified.

7. **Review recommendations are not published.** If findings, implementer response, or dissent are not published within the timeline and with the archival detail specified in §5, the framing's claim of "transparent governance" is falsified.

The framing succeeds if: principal agency increases post-deployment, no scope-clause violations are detected, disabled-principal exit rates remain ≤ baseline, and biometric + evidence-collection accessibility issues are addressed in v0.1 or v1.0 with reviewer sign-off.

---

— Calm, 2026-05-20

*For review governance escalation, contact the Disclosure Ethics Review Board (DERB) at calm-vault-derb@example.org. To nominate a disability-rights reviewer, submit name + institutional affiliation + one paragraph on expertise to the same address.*
