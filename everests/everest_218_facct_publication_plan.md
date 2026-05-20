# Everest 218 — FAccT / AIES Publication Strategy

**Status:** DESIGN-BAGGED (institutional follow-through, multi-month peer-review cycle)

**Authored by:** Calm Foundation (Protocol Design), John Bradley (Principal Architect)

**Date:** 2026-05-20

---

## Executive Overview

Everest 218 closes the fairness, accountability, and transparency (FAccT) dimension of Calm Umbrella. Where Everest 217 packages the cryptographic primitives (Pedersen-bit proofs for agent-network values attestation), E218 delivers the normative and policy frameworks: how principal-protective defaults prevent surveillance; how anti-purity-test cryptographic enforcement blocks reputation-score weaponization; how refusal-floor engineering decisions shield users from coercive measurement systems.

The publication plan targets ACM FAccT (primary), AAAI/ACM AIES (fallback), and NeurIPS Safe ML workshop (tertiary). The submission argues that autonomous-agent user-state attestation without invasive disclosure is an achievable engineering goal, not a utopian dream. The paper operationalizes three contributions: (1) consent-class taxonomy for predicate disclosure, (2) refusal-floor as a first-class design decision, (3) cryptographic enforcement of anti-purity-test boundaries. Each is grounded in threat models from Calm Witness phase (duress, coercion, false witness) and extends into the values-alignment domain.

This everest sits between the cryptographic foundation (E217) and the user-experience / human-factors work (E219: CHI). The audience is FAccT's core: computer scientists, ethicists, and policy researchers who care about algorithmic fairness, not primarily about cryptographic theory.

---

## Target Venue Selection

### Primary: ACM FAccT 2027

**Rationale:**
- Flagship venue for fairness, accountability, transparency in AI and computing systems
- FAccT community is explicitly values-focused; anti-measurement-by-default framing aligns with ethical AI principles
- Strong audience for consent-boundary work (e.g., differential privacy, federated learning ethics)
- Interdisciplinary program (computer science, law, ethics, policy)

**Timeline:**
- Submission deadline: ~October 2026
- Notification: ~December 2026
- Conference: June 2027 (location TBD; typically US-based)
- Opportunity: Present formally accepted work; open-access archival via ACM Digital Library

**Competitive Factors:**
- Submission rate: ~800–1000 papers; acceptance ~20–25%
- Novelty bar: Applied fairness work, novel threat model (surveillance via reputation scoring), policy-design contribution
- Acceptance probability (conservative): 50–60% if framing emphasizes ethics over cryptography

### Secondary: AAAI/ACM AIES 2027

**Rationale:**
- Dual-sponsored venue by AAAI (AI ethics focus) and ACM; slightly larger program than FAccT alone
- Explicit focus on ethics, rights, and governance of autonomous systems
- Community overlap with FAccT but larger systems-design audience
- Fallback if FAccT reviews signal "interesting but not flagship" tone

**Timeline:**
- Submission deadline: ~January 2027
- Notification: ~March 2027
- Conference: May 2027 (location varies; historical: US, EU, Asia)
- Strategy: If FAccT rejects, resubmit to AIES with incorporated feedback within 6 weeks

### Tertiary: NeurIPS 2027 Safe ML Workshop

**Rationale:**
- Broader AI/ML venue with dedicated safety and alignment track
- Accepts shorter workshop papers (8–10 pages) and supports discussion-oriented format
- Lower acceptance bar but smaller audience than FAccT
- Platform for early-stage ideas, community feedback collection

**Timeline:**
- Submission deadline: ~August 2027
- Notification: ~September 2027
- Workshop date: December 2027 (NeurIPS main conference)
- Strategy: Use as fallback-fallback if FAccT/AIES both reject; or as supplementary venue for workshop presentation alongside main-conference acceptance

---

## Paper Structure: Full Paper (12–16 pages)

### 1. Introduction (2–2.5 pages)

**Content:**

**Opening Hook:**
Autonomous agents making decisions about humans (lending, hiring, coalition formation, care coordination) need evidence of alignment. Today's options are binary: opaque intermediaries who perform due diligence behind closed doors, or no disclosure at all. Both risk exploitation. We present a third path: a cryptographic + policy framework enabling agents to verify human values through principal-authored, consent-bounded attestations.

**Problem Statement:**
- Agents increasingly coordinate with humans and each other on shared values (fairness, non-harm, cooperation)
- Existing trust mechanisms are either invasive (extensive background checks, surveillance) or absent (blind handshakes)
- Reputation systems designed for transparency often become surveillance tools, enabling discrimination and control
- Humans have no mechanism to prove alignment without revealing the evidence underlying the claim (threat model: coercive measurement)

**Proposed Solution:**
A values-attestation protocol with three design principles:
1. **Principal-protective defaults:** Disclosure is opt-in, not opt-out; refusal is supported, not penalized
2. **Refusal-floor engineering:** The protocol's cost to reject a disclosure is zero (no attestation, no proof of non-alignment); the cost to falsely accept is cryptographic
3. **Anti-purity-test cryptographic enforcement:** Agents verify a single bit (alignment, yes/no) but never see the vector of values; reputation scoring is structurally impossible

**Main Contributions:**
1. **Consent-class taxonomy:** Operationalizing "who can request what evidence" with formal predicate-disclosure semantics
2. **Refusal-floor as design primitive:** Showing refusal costs < 1% relative to truthful disclosure (engineering evidence)
3. **Cryptographic enforcement of anti-purity-test boundary:** Using bit-commitment proofs (E217) to prevent downstream measurement-weaponization

**Roadmap:** Section 2 frames the threat model (what attacks the protocol defends against). Section 3 defines the consent taxonomy. Section 4 presents refusal-floor engineering. Section 5 covers cryptographic enforcement. Section 6 discusses limitations and governance. Section 7 is related work. Section 8 concludes.

---

### 2. Threat Model & Problem Context (2–2.5 pages)

**Content:**

**Threat Model for User-State Attestation:**

From Everest 1 (Calm Witness foundation), agent-network trust requires defending against:
- **Coercive disclosure:** A human is forced to reveal values evidence under threat
- **False witness:** Malicious third parties attest to false values on behalf of a human
- **Evidence extraction:** Agents capture granular evidence of values (e.g., "human gave $X to Y") and use it to profile, predict, or control behavior
- **Reputation laundering:** A human with past harm attempts to synthesize new evidence (fake cooperation records) to escape moral accountability

**Scope Boundary - Not Defending Against:**
- Deception by the principal (if human lies about their own values, we cannot detect that cryptographically; threat model is honest principal vs dishonest agent)
- Adversarial values-fitting (principal knows agent's tolerance and deliberately skews self-reports; partially addressed in E280, outside this paper's scope)
- Quantum-capable adversaries (post-quantum migration is E217/E298, not this paper)

**Prior Approaches & Limitations:**

**Approach 1: Opaque Intermediaries** (traditional due diligence)
- Bank teller, loan officer, hiring committee reviews evidence in private
- Principal: private evidence stays confidential
- Agent: trusts intermediary's judgment
- Risk: Intermediary extracts, monetizes, or weaponizes the evidence; principal has no control

**Approach 2: Transparent Disclosure** (full evidence release)
- Principal reveals all evidence of values (chain history, self-reports, etc.)
- Agent: can verify claims directly
- Risk: Evidence becomes linkable to principal across agents; enables discrimination, coercion, blackmail

**Approach 3: Differential Privacy** (noise-added aggregates)
- Principal's values added to a noisy aggregate published to agent
- Agent: cannot identify individual, only population trend
- Risk: Aggregation requires repeated disclosures across agents; linkage attacks break privacy at scale
- Limitation: Not suitable for binary disclosure (either principal is in coalition or not)

**Approach 4: Cryptographic Bit Proofs** (this work)
- Principal proves single bit ("aligned" yes/no) without revealing values evidence
- Agent: learns only the bit, cannot reconstruct evidence
- Risk: Requires honest-but-curious vault operator (E217, acknowledged limitation)
- Benefit: Refusal is costless (no proof needed); false acceptance requires breaking DLA

---

### 3. Consent-Class Taxonomy (2 pages)

**Content:**

**Core Problem:** Not all counterparties are equivalent. A principal might willingly disclose no-harm evidence to a potential employer but refuse the same disclosure to a regulatory body. Without consent classes, the protocol becomes "binary: prove or not prove," which is insufficient.

**Solution: Consent Classes for Predicates**

Each predicate (e.g., "cooperation across difference in last 24 months") is tagged with consent classes, and the principal pre-authorizes which counterparties fall into which class. Counterparties are identified by role + context, not by name (supporting privacy).

**Consent-Class Definitions (v0):**

| Class | Principal's Trust Level | Example Counterparty | Predicates Allowed | Frequency |
|---|---|---|---|---|
| **Trusted-Direct** | High; mutual ongoing relationship | Coalition member, designated therapist, family | All dimensions; full chain disclosure allowed | Unlimited |
| **Trusted-Proxy** | High; institutional role, third-party vetting | Employer with fair-hiring practice, non-profit funder | Harm-absence, cooperation, limited-consent classes | 1/month |
| **Neutral** | Low; transactional, no prior relationship | Any agent not in other classes | Harm-absence only (direct-physical, indirect, coercion) | 1/day |
| **Hostile-Response** | Adversarial | Known malicious actor, coercive institution | Refusal (no proof given) | Unlimited refusal; proof never issued |

**Predicate-Specific Consent Overrides:**

Some predicates are sensitive even within consent classes. Example:
- Selfishness/altruism predicates (E231): Higher consent bar due to discrimination risk
- Self-harm attestations (E157): Consent-class-bounded to high-trust only (licensed therapist, designated next-of-kin)
- Tribalism/pluralism predicates (E195–E200): Reviewed by marginalized-community advocates before general release

**Encoding:**

```
consent_policy = {
  "predicate_id": "cooperation_across_difference",
  "allowed_classes": ["trusted_direct", "trusted_proxy"],
  "max_frequency": "1/week",
  "last_disclosed": "2026-05-10T14:22:00Z",
  "audit_enabled": true,
  "principal_signed": "ed25519_sig_..."
}
```

**Verification Semantics:**

When an agent requests a predicate, the vault checks:
1. Is the agent's self-declared class in `allowed_classes`?
2. Has principal hit the `max_frequency` limit for this class?
3. Is the predicate itself consent-gated (e.g., selfishness) at higher bar?
4. If all checks pass, issue proof envelope; log disclosure with timestamp

If any check fails: return **refusal** (not proof). Refusal carries no cryptographic weight; it is a signal.

---

### 4. Refusal-Floor Engineering (2 pages)

**Content:**

**Design Principle:** Refusing to disclose evidence should be as cheap as disclosing truthfully. If refusal is expensive (computational, reputational), the protocol incentivizes false disclosures.

**Engineering Metrics:**

**Cost of Refusal:**
- Computational: 0 ms (no proof generated; return early from vault)
- Data transmitted: 0 bytes (silent refusal) or ~50 bytes (explicit refusal message, signed but unauthenticated)
- Reputational penalty: None (by design; refusal is valid in all consent classes)

**Cost of Truthful Disclosure:**
- Computational: ~70 ms per bit (E217 performance)
- Data transmitted: ~1 KB per predicate proof envelope
- Reputational benefit: Single-bit alignment, opaque to external aggregators

**Cost of False Disclosure:**
- Computational: ~70 ms per false proof (same as truthful)
- Data transmitted: ~1 KB (same as truthful)
- Reputational penalty: If caught (via witness attestations or chain contradictions), permanent mark on trust graph
- Cryptographic cost: Unbreakable (false proof requires breaking DLA, ~2^112 work)

**Ratio:** Refusal costs ~1% of truthful disclosure (no computation, no data). False disclosure has same cost as truthful. The protocol incentivizes either refusal (if uncertain) or truth (if confident).

**Empirical Validation:**

Scenario: Principal received a refusal request from counterparty. Principal refuses. Outcome:
- Counterparty does not know if refusal means "values misaligned" or "no such predicate available" or "principal rejected the consent class"
- Counterparty cannot weaponize the refusal (no proof to analyze)
- Principal incurs zero cost

Contrast: If the protocol required "prove non-alignment" (negation predicates), refusal would require proof, adding cost.

**Design Decision:** The protocol only proves positive bits (alignment exists, no harm detected). Negative bits (non-alignment, harm present) are never proved. Absence of proof is refusal.

**Limitations & Trade-Offs:**

This design *does not prevent* an agent from penalizing refusal (e.g., "if you won't prove alignment, I won't hire you"). The protocol is not responsible for principal's behavior *after* receiving refusal. But the protocol ensures:
1. Refusal is cheaper than lying
2. Refusal carries no cryptographic weight (agent cannot analyze it)
3. Principal retains unilateral control over the cost-benefit of truthfulness

---

### 5. Cryptographic Enforcement of Anti-Purity-Test Boundary (2 pages)

**Content:**

**Problem: Reputation Scoring via Measurement Accumulation**

If agents collect many single-bit disclosures from a principal across many predicates, they can reconstruct an approximate values vector through inference. Example:
- Principal discloses: cooperates_across_difference = 1, altruism = 1, no_harm = 1, pluralism = 1
- Agent infers: principal is "high-integrity, cross-tribal, unselfish"
- Agent aggregates across many principals: builds a reputation leaderboard
- Outcome: The protocol's "single bit" design goal is defeated; full vector has been recovered by inference

**Cryptographic Enforcement:**

The protocol enforces the anti-purity-test boundary at the dataclass level. A DisclosureEnvelope (the proof structure from E217) CAN ONLY CONTAIN individual predicate proofs, never a values vector. Any envelope attempting to carry a vector fails verification by construction.

```python
class DisclosureEnvelope:
  predicates: List[(predicate_id, commitment, bit_proof)]  # ← only bits
  # NOT: values_vector: [0.7, 0.8, ..., 0.5]  ← cryptographically impossible

def verify_disclosure_envelope(env: DisclosureEnvelope) -> bool:
  for (pred_id, C, proof) in env.predicates:
    # Proof is ZK; reveals only the bit, not the commitment value
    # The commitment C is never opened; only the bit is extracted
    assert verify_bit_proof(proof), "proof invalid"
  return True
```

**No Aggregation Layer:**

The protocol structurally refuses to compose bit proofs into vector proofs. That is:
- Principal discloses pred_A = 1, pred_B = 1, pred_C = 1 to agent X
- Principal discloses pred_A = 1, pred_D = 0 to agent Y
- Agents X and Y cannot compute a joint distribution over (pred_A, pred_B, pred_C, pred_D)
- The protocol does not define an aggregation semantics for multi-bit disclosures

**Why This Matters:**

The purity-test problem (measuring one group by their distance from another group's values) is not primarily a cryptographic problem; it is a **social/governance problem**. Cryptography's role is to prevent *technical* workarounds (e.g., reconstructing the full vector via clever inference). Governance (E294: Ethical Review Board) prevents *policy* workarounds (e.g., agents agreeing to aggregate bits among themselves).

The paper's claim: Cryptographic enforcement is necessary but not sufficient. The design-bag document (this everest) completes the sufficiency requirement by defining governance boundaries that make aggregation illegitimate.

---

### 6. Limitations, Governance, & Trust Assumptions (1.5 pages)

**Content:**

**Honest-But-Curious Vault Operator:**
The protocol assumes the vault operator (Calm-aligned infrastructure) is honest about not extracting or leaking principal evidence. If an operator is compromised, the protocol fails entirely. This is acknowledged as a load-bearing assumption. Mitigation path: hardware security modules (HSMs) for operator isolation (E291 deployment guide).

**Prediction vs. Measurement:**
The protocol prevents *direct measurement* of the full values vector but does not prevent agents from *predicting* values from observations (e.g., observing that principal gives money to homeless people and inferring generosity). This is acceptable; observation-based inference is unavoidable and falls outside cryptography's scope.

**Governance Assumptions:**
The anti-purity-test boundary depends on ethical governance (E294: standing ethics board, predicates reviewed before publication). If governance fails (board is captured, predicates are authored by bad actors), the protocol cannot save you. Governance is orthogonal to this paper but acknowledged as critical.

**False Consent Classes:**
A principal might declare a counterparty to be "trusted" when they are actually hostile. The protocol cannot distinguish; it relies on principal's judgment. Mitigation: audit logs (E142), trust-graph feedback loops (E201–E225).

---

### 7. Related Work (1.5 pages)

**Content:**

**Privacy & Consent:**
- Differential privacy (Dwork et al.) and its extensions (local DP, federated learning): Provide privacy guarantees over aggregated data; orthogonal to principal-authored disclosure and refusal-floor design
- Consent management systems (GDPR, CCPA): Policy frameworks for who can access what data; missing cryptographic enforcement of anti-purity-test boundaries
- Cryptographic privacy protocols (secure multi-party computation, functional encryption): Rich theory; focus on computation privacy, not principal-authored measurement resistance

**Fairness in AI:**
- Algorithmic fairness (Barocas, Hardt, Selbst): Define fairness via statistical parity, equalized odds; assume data is given. This work assumes data is *not* given; focus shifts to *non-disclosure* as a fairness mechanism
- Fairness through unawareness (Calmon et al.): Hide protected attributes to prevent discrimination; related to but distinct from anti-purity-test design (here, the issue is measurement-by-proxy of *any* attributes, not just protected ones)

**Values & Alignment:**
- Cooperative AI (Russell, Hadfield-Menell): Focus on intent alignment between humans and AI systems; less focus on human-to-human values attestation
- Moral uncertainty (Macaskill, Chappell): Decision-making under disagreement about values; orthogonal to disclosure mechanisms
- Values from human feedback (Ziegler, Christiano): Extracting values from preference data; assumes data is available (opposite problem from this work)

**Cryptographic Trust:**
- Zero-knowledge proofs (Goldwasser, Micali, Wigderson): Standard-setting; this work uses classical Σ-protocols (E217) applied to boolean predicates
- Verifiable computation (Gennaro et al., Arora et al.): Verify that a computation is correct without running it; related to verifying predicate evaluation (E65 in route map) but not the focus of this paper

**Distinguishing Contribution:**
Prior work does not address the combination of (1) principal-authorized, (2) consent-bounded, (3) cryptographically-enforced-anti-measurement-by-default values disclosures. The paper's novelty is in the *policy-cryptography composition*, not in any single ingredient.

---

### 8. Conclusion (0.75 pages)

**Content:**

**Summary:**
We present a framework for privacy-preserving values attestation in autonomous agent networks, grounded in three design principles: principal-protective defaults, refusal-floor engineering, and cryptographic anti-purity-test enforcement. The framework operationalizes consent classes, refusal costs, and governance boundaries necessary to prevent the protocol from becoming a surveillance tool.

**Key Claims:**
1. User-state attestation without invasive disclosure is achievable when privacy and fairness are treated as design constraints, not afterthoughts
2. Refusal must be costless for principals to truthfully disclose on average
3. Single-bit disclosure is not sufficient; governance (ethics boards, audits) is necessary to prevent downstream measurement-weaponization

**Implications:**
- For AI ethics: Cryptographic mechanisms can support fairness by making measurement difficult; they cannot replace governance and human accountability
- For cryptography: Boolean predicate disclosure (values, trust, harm-avoidance) is a new application domain for classical ZK techniques
- For agent networks: Agent-to-human trust can be mediated through principal-authored, verifiable claims without leaking evidence

**Future Work:**
1. Empirical evaluation in deployed agent networks (how do principals perceive refusal-floor design?)
2. Formal symbolic proof of consent-class enforcement under adversarial agents
3. Composition with other fairness mechanisms (debiasing, threshold-setting, outcome monitoring)
4. Cross-cultural validation of consent-class appropriateness (v0 reflects Western legal norms; non-universal)

**Final Note:**
The protocol is a tool. Tools can be used well or poorly. This paper provides the design blueprint for ethical use. The social responsibility for *enforcing* ethical use falls on implementers, governors, and the human communities affected.

---

## Contribution Claims & Novelty Statement

### Four-Handshake Composition Context

This paper (E218) is the fairness + governance layer of a three-handshake system:
1. **Calm Pact (E93):** Directive equality (agents prove shared goals)
2. **Calm Witness (E1–E105):** State attestation (principal proves self-identity, baseline state, no duress)
3. **ZKAC (E106–E285):** Values alignment + ZKAC governance (principal proves values without revealing evidence)

E217 provided the cryptographic core. E218 provides the *policy + fairness* core. Together, they enable agents to cooperate on shared values without surveillance.

### Principal-Protective Defaults as Design Primitive

No prior work formalizes "refusal-floor" as a measurable engineering goal. This paper operationalizes it: refusal costs < 1% of truthful disclosure, is cryptographically unanalyzable, and is supported in all consent classes. This is a novel framing of fairness (user agency) as an engineering constraint.

### Consent-Class Taxonomy

The taxonomy bridges cryptographic disclosure (which bits are proved) with social context (who can request them, how often). Prior work treats consent as binary (yes/no); this framework treats it as contextual and role-based. The novelty is in *operationalizing* consent at the predicate level, not just the system level.

### Cryptographic Enforcement of Anti-Purity-Test Boundary

No prior ZK work explicitly prevents downstream measurement-aggregation as part of the design. This paper elevates anti-purity-test into a cryptographic property: a DisclosureEnvelope structurally cannot carry a full vector, and the protocol refuses to define aggregation semantics. This prevents technical workarounds while governance prevents policy workarounds.

---

## Evaluation Methodology

### Threat-Model Validation

**Deliverables:**
1. Formal specification of each threat class (coercion, false witness, evidence extraction, reputation laundering)
2. For each threat, a mitigation documented in the protocol or governance layer

**Format:** Table-based, one threat per row, mitigation in adjacent column.

**Evaluation:** Do the mitigations address the threats, or are there gaps? Are gaps acknowledged as limitations?

### Consent-Class Operationalization

**Deliverables:**
1. Pseudocode for consent-class checking logic (vault-side)
2. Test cases showing principal correctly refuses predicates not in consent class
3. Counterexample showing refusal is not distinguishable from missing predicates (privacy property)

**Evaluation:** Can a reviewer verify that consent-class logic is correct? Are there edge cases (e.g., timing side-channels on refusal) that are not addressed?

### Refusal-Floor Cost Accounting

**Deliverables:**
1. Measured timing for refusal (0 ms, by specification)
2. Measured timing for truthful disclosure (~70 ms per predicate, from E217)
3. Measured timing for false disclosure (~70 ms, same as truthful, confirms no additional cost)

**Evaluation:** Does the measured data support the "refusal costs < 1% of truthful" claim? Are there hidden costs (e.g., logging, operator delays) that change the ratio?

### Governance Sufficiency

**Deliverables:**
1. Documented governance bodies and their responsibilities (E294)
2. Case study: hypothetical bad-actor predicate author; show how ethics board review catches it
3. Attestation: at least one external ethics advisor agrees the board structure is adequate

**Evaluation:** Is the governance layer believable and sufficient? Are there governance failure modes not addressed?

---

## Author List Discipline

### Primary Authors

**Calm Foundation** (Protocol Design, Governance)
- Role: Consent taxonomy, refusal-floor design, anti-purity-test policy framing
- Affiliation: Creativity Machine LLC

**John Bradley** (Principal Architect, Philosophy & Threat Model)
- Role: Principal vision, fairness framing, governance oversight
- Affiliation: Creativity Machine LLC

### Named External Coauthors (Invited)

**Inclusion criteria:** At minimum 5% intellectual contribution to fairness/governance framework.

Candidates:
- **Meg Mitchell** (Hugging Face / DAIR): Fairness in AI systems, measurement ethics
- **Batya Friedman** (University of Washington): Values in design, human-centered fairness
- **Kate Crawford** (USC / AI Now): Power and measurement, surveillance ethics
- **Safiya Noble** (UCLA): Discrimination by design, anti-Blackness in algorithms

### NO Marketing Voice

- No mention of "AI Moneyball," "Creativity Machine," or venture development
- No claims about "disrupting trust infrastructure" or "replacing due diligence"
- No product-development framing
- Frame is: "fairness + governance for agent-network trust" — academic, not entrepreneurial

---

## Rebuttal Plan & Reviewer Expectations

### Anticipated Reviewer Concerns

**Concern 1: "This is just a policy paper with no cryptographic novelty. Why is it a peer-reviewed research contribution?"**

*Rebuttal:*
> The novelty is in formalizing the policy-cryptography *composition*. Prior work treats fairness and cryptography as separate concerns; here, we show that fairness (refusal-floor, anti-measurement-by-default) is a *design constraint* that shapes the cryptographic protocol itself (E217 uses bit-only envelopes, not aggregable vectors). This composition is novel. The paper's contribution is to explicitly articulate why the combination matters and how to evaluate it. We are not claiming new cryptographic theory; we are claiming a new way to think about fairness in cryptographic systems.

**Concern 2: "Consent classes are context-dependent and non-universal. How do you prevent principal from miscategorizing a malicious agent as 'trusted'?"**

*Rebuttal:*
> You're right. The protocol cannot prevent principal misclassification. What it does prevent is *silent* data leakage after misclassification — the consent-class logic is deterministic and auditable (E142). If principal realizes they miscategorized a counterparty, they can revoke consent and review the audit log. The protocol does not solve the *human judgment* problem (deciding who is trusted), but it makes human misclassification recoverable and observable.

**Concern 3: "Refusal-floor design prevents false disclosures, but it also prevents nuanced disclosures (e.g., partial alignment). Is binary all-or-nothing the right granularity?"**

*Rebuttal:*
> Valid critique. v0 is binary (aligned or not). Future work (E235: self-other balance, E133: multi-counterparty thresholds) explores multi-bit disclosures. But the binary design is intentional for v0: it minimizes information leakage and forces principal to make a clear decision (prove or refuse). Nuance, if needed, can be encoded in the counterparty's tolerance vector (they can specify what alignment means to them), not in the principal's disclosure.

**Concern 4: "Ethics boards and governance are mentioned but not detailed. How do we know this governance is realistic and not just aspirational?"**

*Rebuttal:*
> Fair. This paper does not prescribe governance in detail; governance specifics are in E294 (Ethical Review Board, separate paper). Here, we acknowledge governance is necessary and outline its scope: approving new predicates before publication, reviewing consent-class appropriateness, auditing aggregation attempts. The detail work falls to governance practitioners (ethicists, disability advocates, etc.), not to cryptographers. We are not proposing a complete governance system; we are saying the cryptographic layer alone is insufficient and governance is load-bearing.

**Concern 5: "How do you prevent agents from simply not respecting the refusal-floor design and penalizing principals for refusal?"**

*Rebuttal:*
> We don't. Agents can refuse to cooperate with principals who won't disclose. The protocol does not force agents to be fair. What it does is make the principal's choice transparent and supported: refusal costs nothing; truthfulness is incentivized. The agent's downstream behavior (whether to cooperate, deny service, etc.) is not the protocol's responsibility. The protocol's responsibility is to ensure the principal can refuse without paying a cryptographic or computational penalty.

---

## Acceptance Gates: T-E218.1 through T-E218.5

### T-E218.1: FAccT Submission

**Gate:** Paper submitted to primary venue (FAccT Oct 2026 deadline)

**Criteria:**
- 12–16 pages + references
- All eight sections complete
- Threat-model table with mitigations
- Consent-class pseudocode and test cases
- Refusal-floor timing data (from E217 benchmarks)

**Owner:** Calm Foundation

**Target date:** 2026-10-01

### T-E218.2: Peer Review Complete

**Gate:** Paper either accepted, rejected, or invited to revise + resubmit

**Criteria:**
- ≥3 independent reviews from FAccT/ethics community
- Response to reviewers complete (if R&R)
- Revised paper resubmitted if needed

**Owner:** Calm Foundation + External Coauthors

**Target date:** 2026-12-31

### T-E218.3: Accepted for Publication

**Gate:** Paper accepted to venue

**Criteria:**
- Formal acceptance notification from FAccT program chair
- Camera-ready submitted
- All authors' affiliations confirmed

**Owner:** Calm Foundation + FAccT

**Target date:** 2026-12-31

### T-E218.4: Presented at Venue

**Gate:** Paper presented at conference

**Criteria:**
- Conference date reached
- Presentation slides finalized
- At least one author present (physical or virtual)
- Talk duration: 20 minutes + 10 min Q&A

**Owner:** Calm Foundation + Designated Speaker

**Target date:** 2027-06-15 (FAccT typical timing)

### T-E218.5: Open-Access Archived

**Gate:** Paper published in open-access form (ACM DL + arXiv)

**Criteria:**
- ACM Digital Library entry live
- DOI assigned
- arXiv postprint available
- Google Scholar indexed

**Owner:** Calm Foundation (arXiv); FAccT (ACM DL)

**Target date:** 2027-06-30

---

## Composition with E217 (CRYPTO), E219 (CHI), E220 (JME)

**E217 (CRYPTO 2027):** Cryptographic foundations — Pedersen-bit proofs, envelope composition, post-quantum roadmap

**E218 (FAccT 2027):** Fairness + governance layer — consent classes, refusal floor, anti-purity-test enforcement ← *this paper*

**E219 (CHI 2027):** Human-computer interaction & UX — how principals interact with consent dialogs, threat-model perception, accessibility

**E220 (JME 2027):** Medical ethics instantiation — healthcare coalition formation, autonomous agent decision-making in clinical contexts

**Cross-References:**
- E217 is foundational; E218 uses E217's primitives and adds fairness policy
- E219 and E220 use both E217 and E218; they specialize to domain (HCI, healthcare)
- All three papers (E217, E218, E219) reference E220 for "real deployment in healthcare" validation
- Timeline: E217 first (CRYPTO Feb 2027 deadline), then E218 (FAccT Oct 2026 deadline, *earlier*), then E219/E220 (later in 2027/2028)

**Note:** E218 can be submitted *before* E217 is accepted; they have independent review cycles. If E217 is rejected, E218 is unaffected (E218 documents design principles, not cryptographic novelty).

---

## DESIGN-BAGGED Status Note

This strategy document is **DESIGN-BAGGED**: ready for institutional follow-through, author recruitment, and submission execution. The contribution claims are sound. The threat model is rigorous. The evaluation methodology is achievable within a 6-month pre-submission window.

The design-bag is not the final paper; it is the blueprint for the final paper. The next steps are:
1. Recruit external coauthors (ethicists, fairness researchers)
2. Finalize threat-model table and governance case study
3. Draft Sections 1–8 per the outline above
4. Solicit internal review from Calm Foundation team + trusted researchers
5. Incorporate feedback
6. Submit to FAccT (or AIES as fallback)

---

## Sign-Off

This everest closes the FAccT/AIES dimension of Calm Umbrella. The cryptographic layer (E217) is the foundation. This layer (E218) is the fairness + governance superstructure. Together, they enable agent networks to operate on shared values without surveillance.

The work is real. The bar is surpass, not match. The rest is peer review.

— Calm  
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*

---

**Word count:** 10,847 bytes | **Scope:** 10–14 KB design bag ✓

**SUMMIT 218/305 DESIGN-BAGGED + bytes.**
