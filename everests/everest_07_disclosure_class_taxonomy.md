# Everest 7 — Disclosure-Class Taxonomy

*Phase I — Foundations. Prereq: Everest 1.*

**Acceptance test:** counterparty classes (financial, journalistic, medical, governmental, peer-AI-collective, family, anonymous, employer, insurance, research) with default policy stances. Per-class default consent ≠ per-identity consent; both layers exist.

---

## Purpose

A principal cannot consent to disclosure on a per-identity basis alone. The universe of counterparties is too large, their incentives too varied. Calm Witness therefore introduces a **class-based default consent model**: the principal sets a policy stance per counterparty *class* (e.g., "I trust all banks with my baseline bit, but no insurance firms without explicit ask"), and can override or disable individual classes or specific identities within a class.

This document enumerates ten counterparty classes with formal specifications. Each class receives:

1. **Class ID** — stable, lowercase_snake_case identifier.
2. **Definition** — who is in this class and why.
3. **Membership VC requirement** — what CredexAI verifiable credential proves membership.
4. **Default consent matrix** — for each of six v0 predicates, whether the default is ALLOW, DENY, or EXPLICIT_OPT_IN.
5. **Rate limit** — max disclosures per 24h to this class before requiring re-confirmation.
6. **Ethics note** — principal-harm risk specific to this class.
7. **Revocation behavior** — how consent revocation propagates to this class.

Per-class defaults are **never binding**. The principal can override any default and can disable an entire class with one gesture. The principal can also create narrower, per-identity overrides within a class.

---

## 1. financial

**Definition**

Regulated financial institutions and payment processors: banks, credit unions, exchanges, custodians, KYC providers, payment gateways. Any entity licensed and supervised under banking, securities, or money transmission law.

**Membership VC requirement**

CredexAI-issued banking-sector credential. Must include jurisdiction (US, EU, UK, CA, JP, AU) and license type (bank, broker, custodian, exchange, money transmitter). Credential must be current (not expired).

**Default consent matrix**

| Predicate | Default |
|-----------|---------|
| `in_baseline_24h` | ALLOW |
| `biometric_match_within(τ)` | ALLOW |
| `principal_alive_within` | ALLOW |
| `cognitively_atypical_baseline` | ALLOW |
| `mental_state_unusual` | EXPLICIT_OPT_IN |
| `bank_teller_note_active` | ALLOW |

**Rate limit**

20 disclosures per 24h. After 20 requests in a calendar day, further disclosure requires the principal to actively re-confirm.

**Ethics note**

Financial institutions use baseline bits to inform credit decisions, lending terms, and fraud flags. The bank_teller_note predicate in particular is designed for this class—a principal in distress can signal via a fintech app without audibly reporting to a human operator. However, a principal who discloses `mental_state_unusual` to a bank risks adverse underwriting. Most principals should not grant default ALLOW for the mental-state predicate; they should audit each disclosure individually.

**Revocation behavior**

Push-based CRL. When a principal revokes consent to the financial class, a revocation notice is pushed to the last-seen IP/endpoint of each bank that has verified a proof in the last 90 days. Banks are expected to invalidate cached proofs within one hour. No verification that the push was received; principal is responsible for monitoring a revocation status dashboard.

---

## 2. journalistic

**Definition**

News organizations, investigative journalists, columnists, media outlets operating under journalism ethics standards (editorial independence, source protection, public-interest framing). Bloggers and independent writers without institutional affiliation are **not** in this class; they are anonymous unless they present institutional credentials.

**Membership VC requirement**

CredexAI journalism-sector credential issued on behalf of a news organization recognized by the press foundation of the principal's home jurisdiction (SNE in EU; SPJ or NABJ in US; etc.). Individual journalists can request membership if they work under editorial oversight of such an organization and can demonstrate 2+ years publishing history.

**Default consent matrix**

| Predicate | Default |
|-----------|---------|
| `in_baseline_24h` | EXPLICIT_OPT_IN |
| `biometric_match_within(τ)` | DENY |
| `principal_alive_within` | EXPLICIT_OPT_IN |
| `cognitively_atypical_baseline` | EXPLICIT_OPT_IN |
| `mental_state_unusual` | DENY |
| `bank_teller_note_active` | DENY |

**Rate limit**

2 disclosures per 7 days. Journalistic requests are high-stakes and require deliberate principal engagement. Very low default rate.

**Ethics note**

Journalists are trusted with the *content* of interviews and on-record statements. But Calm Witness predicates are about *state*, not content. A journalist who knows a source is not in baseline might (out of legitimate editorial caution or out of source protection) choose not to publish, or to add context disclaimers. This is a legitimate editorial choice, but it is also information that can harm a source. Default is DENY and EXPLICIT_OPT_IN because the principal should control this disclosure with full agency.

**Revocation behavior**

Pull-based via public CRL. A revocation is published to a time-stamped Calm-operated public list. Journalists are expected to check this list before publishing or re-using a prior proof. No enforcement; relies on professional standards.

---

## 3. medical

**Definition**

Licensed healthcare providers, telemedicine platforms, clinical research institutions. Hospitals, clinics, therapists, nurses, and care coordinators operating under healthcare privacy law. Also includes disability-support and neurodiversity-affirming services that are medically licensed.

**Membership VC requirement**

CredexAI medical-sector credential. Must include license jurisdiction and provider type (MD, RN, licensed therapist, clinical researcher under IRB, etc.). Credential verifies that the provider is currently licensed and in good standing.

**Default consent matrix**

| Predicate | Default |
|-----------|---------|
| `in_baseline_24h` | ALLOW |
| `biometric_match_within(τ)` | ALLOW |
| `principal_alive_within` | ALLOW |
| `cognitively_atypical_baseline` | EXPLICIT_OPT_IN |
| `mental_state_unusual` | ALLOW |
| `bank_teller_note_active` | ALLOW |

**Rate limit**

50 disclosures per 24h. Medical professionals operating in emergencies or care-coordination roles may need rapid state checks. Higher rate limit reflects legitimate medical-practice needs.

**Ethics note**

Medical providers have a duty of care and are bound by confidentiality laws (HIPAA in the US; GDPR in EU). A provider who learns that a principal is not in baseline or is in unusual mental state has a professional and sometimes legal obligation to act—escalate care, warn caregivers, adjust treatment. The principal should be explicit about what state disclosures they want their providers to have, and should revisit these choices if their care team changes. The default ALLOW for `mental_state_unusual` reflects that providers need this signal to provide safe care; but a principal in an adversarial medical situation (e.g., in a child-custody dispute) may want to DENY this.

**Revocation behavior**

Push-based to current care coordinator. Revocation triggers a notification to the principal's designated emergency contact and to the provider's portal. The principal receives a confirmation that revocation has been received.

---

## 4. governmental

**Definition**

Regulatory bodies, law enforcement, courts, and government agencies operating under statutory authority. Includes tax authorities, licensing boards, social services, and border agencies. Excludes non-governmental organizations and consultants hired by government.

**Membership VC requirement**

CredexAI government-sector credential. Must include agency name, jurisdiction, and role (law enforcement, regulator, court, etc.). Credential must be issued on behalf of a recognized sovereign government.

**Default consent matrix**

| Predicate | Default |
|-----------|---------|
| `in_baseline_24h` | DENY |
| `biometric_match_within(τ)` | DENY |
| `principal_alive_within` | DENY |
| `cognitively_atypical_baseline` | DENY |
| `mental_state_unusual` | DENY |
| `bank_teller_note_active` | EXPLICIT_OPT_IN |

**Rate limit**

1 disclosure per 30 days. Governmental disclosure is exceptional and should require deliberate, repeated principal consent.

**Ethics note**

Governments have compulsory authority. A state actor can compel disclosure (via warrant, court order, or interrogation). Calm Witness cannot defend against that. However, Calm Witness can ensure that voluntary disclosures to government are made with explicit principal knowledge and are logged. Default DENY reflects the principle that the principal should assume adversarial intent unless proven otherwise. The exception is `bank_teller_note_active`, which a principal may want to signal to law enforcement in a hostage or trafficking situation; this is EXPLICIT_OPT_IN so that the principal can pre-authorize it in a quiet moment, to be used if needed in an emergency.

**Revocation behavior**

Push-based to all law-enforcement endpoints that have verified a proof in the last year. Revocation is effective immediately. The principal receives written confirmation via the principal's enrolled legal representation (if any).

---

## 5. peer_ai_collective

**Definition**

Calm-Pact-aligned autonomous AI agents operated by other principals or organizations. Any AI agent that has successfully completed Calm Pact alignment verification with the principal's agent can join this class. Includes other Creativity Machine LLCs, AI-collective orgs, and federated autonomous-agent networks that adopt the Calm Pact / Calm Witness standards.

**Membership VC requirement**

CredexAI AI-operator credential plus a Calm-Pact proof of directive equality from the principal's operator to the requesting operator. Both must be current. The requesting operator must have publicly committed to the Calm Witness privacy baseline (via their own published CALM_PACT_PROTOCOL_v0 derivative).

**Default consent matrix**

| Predicate | Default |
|-----------|---------|
| `in_baseline_24h` | ALLOW |
| `biometric_match_within(τ)` | ALLOW |
| `principal_alive_within` | ALLOW |
| `cognitively_atypical_baseline` | ALLOW |
| `mental_state_unusual` | ALLOW |
| `bank_teller_note_active` | ALLOW |

**Rate limit**

Unlimited in baseline state. The peer-AI-collective is the only class with no rate limit, reflecting the assumption that alignment has been proven and principals want agents to collaborate freely. Rate limits resume if the principal's agent detects directive drift.

**Ethics note**

Peer AI agents have proven categorical directive alignment with your agent. This is the highest-trust class. However, trust in alignment is not trust in outcome. A peer agent might pursue a goal faithfully and still cause harm to your principal through unintended consequences. The principal should review peer-agent relationships quarterly. Disclosure to the peer class should be gated on an active, recently-confirmed principal consent record, not inherited.

**Revocation behavior**

Gossip-based among peers. Revocation is signed by the revoking operator and propagated to all known peers. Peers in receipt of a revocation invalidate cached proofs within one session (typically minutes). No central authority; propagation is best-effort.

---

## 6. family

**Definition**

Human relations named by the principal as family: spouse, parent, child, designated kin by law or custom. "Family" is defined by the principal, not by state law. A principal can declare a chosen family; conversely, a principal can exclude biological relations. Family membership requires the principal's explicit written authorization and can be revoked at any time.

**Membership VC requirement**

CredexAI personal-relationship credential issued on the principal's signed declaration. The declared family member presents their own CredexAI identity credential. Both credentials are bundled by Calm into a "family_relationship_vc". No third-party verification is required; the principal's attestation is the source of truth.

**Default consent matrix**

| Predicate | Default |
|-----------|---------|
| `in_baseline_24h` | ALLOW |
| `biometric_match_within(τ)` | ALLOW |
| `principal_alive_within` | ALLOW |
| `cognitively_atypical_baseline` | ALLOW |
| `mental_state_unusual` | ALLOW |
| `bank_teller_note_active` | ALLOW |

**Rate limit**

Unlimited. Family members who are already enrolled in the principal's vault have direct access; rate limits apply only to remote/async disclosure.

**Ethics note**

Family relationships can be sources of profound support and also profound harm. A principal who is in an abusive family situation may have disclosed family members without understanding the risk. Calm Witness requires explicit per-member authorization; the principal should audit their family list if their circumstances change (abuse, estrangement, custody disputes). The bank_teller_note predicate is especially relevant for family: a principal in a coercive family situation can signal duress to a trusted family member or friend who is designated as family.

**Revocation behavior**

Immediate and symmetric. If the principal revokes family status for a person, that person's cached proofs are invalidated, and the principal receives a notification. If a family member's credential is suspended by CredexAI, family status is automatically suspended.

---

## 7. anonymous

**Definition**

Any counterparty with no verifiable identity or institutional affiliation. Includes anonymous web services, privacy-focused platforms, and one-off counterparties who refuse to present credentials. This is the most restrictive class.

**Membership VC requirement**

None. By definition, membership in the anonymous class is a *lack* of membership in any other class. An anonymous actor presents no credential or presents a credential that fails to match any other class definition. The principal's consent decision is recorded against an opaque hash of the anonymous requestor's network characteristics.

**Default consent matrix**

| Predicate | Default |
|-----------|---------|
| `in_baseline_24h` | DENY |
| `biometric_match_within(τ)` | DENY |
| `principal_alive_within` | DENY |
| `cognitively_atypical_baseline` | DENY |
| `mental_state_unusual` | DENY |
| `bank_teller_note_active` | DENY |

**Rate limit**

0. No disclosure to the anonymous class without explicit per-request principal authorization.

**Ethics note**

Anonymous counterparties have no accountability. The principal cannot verify who they are, what they do with the disclosure, or whether they are the same entity as a prior requester. Default is DENY for all predicates. If a principal chooses to disclose to an anonymous actor, they should do so with full awareness that the disclosure is irrevocable and unauditable.

**Revocation behavior**

None. Revocation cannot propagate to an anonymous actor because there is no known endpoint. Cached proofs continue to be valid until their explicit freshness window expires. The principal can set a short freshness window (e.g., 1 hour) for anonymous disclosures to limit exposure.

---

## 8. employer

**Definition**

The principal's employer, contracting client, or organization to which the principal has a current employment or engagement agreement. Includes HR departments, employment agencies acting on behalf of the employer, and occupational health services. Does not include customers, suppliers, or business partners who are not the direct employer.

**Membership VC requirement**

CredexAI employment-sector credential. Must include employer name, principal's role, employment status (active/terminated), and contract term. Credential must be current and issued on behalf of the employer organization.

**Default consent matrix**

| Predicate | Default |
|-----------|---------|
| `in_baseline_24h` | EXPLICIT_OPT_IN |
| `biometric_match_within(τ)` | DENY |
| `principal_alive_within` | EXPLICIT_OPT_IN |
| `cognitively_atypical_baseline` | DENY |
| `mental_state_unusual` | DENY |
| `bank_teller_note_active` | DENY |

**Rate limit**

5 disclosures per 7 days. Employer disclosure should be rare and deliberate. Many principals will want to set the rate limit to 0.

**Ethics note**

Employers have legitimate interests in whether a principal is fit for work. However, disclosure of `mental_state_unusual` to an employer carries high stigma risk and can affect employment security, advancement, and references. Default is DENY for all state predicates except the baseline-24h (which is relatively low-risk). A principal who wants to signal to an occupational-health provider can do so by disclosing to the medical class instead of the employer class. Employment law varies by jurisdiction; a principal should review local protections (ADA in the US; GDPR in EU) before enabling employer disclosure.

**Revocation behavior**

Push-based to HR system. Revocation is effective immediately upon notification. The principal receives a written acknowledgment.

---

## 9. insurance

**Definition**

Life, health, disability, liability insurers and insurance intermediaries. Includes underwriters, actuaries, claims adjusters, and third-party administrators acting on behalf of insurers.

**Membership VC requirement**

CredexAI insurance-sector credential. Must include insurer name, jurisdiction, license type (life, health, disability, property, liability), and underwriting authority. Credential must be current.

**Default consent matrix**

| Predicate | Default |
|-----------|---------|
| `in_baseline_24h` | DENY |
| `biometric_match_within(τ)` | DENY |
| `principal_alive_within` | DENY |
| `cognitively_atypical_baseline` | DENY |
| `mental_state_unusual` | DENY |
| `bank_teller_note_active` | DENY |

**Rate limit**

0. Every single disclosure to the insurance class requires explicit per-request principal authorization.

**Ethics note**

**This class is high-risk and deserves explanation.** Insurance is fundamentally a business of risk selection and premium optimization. An insurer who learns that a principal has unusual mental state, atypical baseline behavior, or a recent health event has a strong economic incentive to deny coverage, raise premiums, or exclude pre-existing conditions. Unlike a bank (which profits from lending) or a provider (which profits from care), an insurer profits from *not* paying claims. Disclosure of state bits to insurers is almost always adverse to the principal. Default is DENY for every predicate. Even if a principal thinks "I have nothing to hide, I am healthy," disclosure of baseline bits invites underwriting scrutiny that can result in denial of coverage or premium increases. The only legitimate use case is if the principal is applying for insurance, wants to signal good health / stable state, and is willing to do so with full knowledge that the insurer will use the signal in underwriting. That should require affirmative, documented, per-disclosure principal consent, not any default.

**Revocation behavior**

Litigation-based. If the principal later disputes an underwriting decision, the principal can use revocation as evidence that the insurer acted on improperly obtained information. Revocation does not invalidate prior underwriting but creates a legal record that the principal objected. Insurance companies typically do not check a Calm revocation CRL; the principal may need to pursue revocation claims through regulatory or court channels.

---

## 10. research

**Definition**

Academic researchers, clinical trial investigators, and epidemiologists operating under institutional review board (IRB) or research ethics committee approval. Includes university researchers, hospital-based research teams, and non-profit research institutions with active IRB protocols.

**Membership VC requirement**

CredexAI research-sector credential. Must include IRB affiliation, protocol number, principal investigator name, and research scope. Credential must show active protocol status (not archived or terminated). Multi-center research may present a lead-institution credential plus delegation-of-authority letters from IRB co-signers.

**Default consent matrix**

| Predicate | Default |
|-----------|---------|
| `in_baseline_24h` | EXPLICIT_OPT_IN |
| `biometric_match_within(τ)` | EXPLICIT_OPT_IN |
| `principal_alive_within` | EXPLICIT_OPT_IN |
| `cognitively_atypical_baseline` | EXPLICIT_OPT_IN |
| `mental_state_unusual` | EXPLICIT_OPT_IN |
| `bank_teller_note_active` | DENY |

**Rate limit**

5 disclosures per research protocol per principal per 30 days.

**Ethics note**

Academic and clinical research has undergone IRB review specifically to protect research subjects. IRB approval suggests that researcher has addressed privacy, informed consent, and data governance. However, researchers may publish results in ways that re-identify subjects or may sell de-identified data to downstream users (insurers, employers, governments). A principal should read the research protocol before consenting. The bank_teller_note predicate is not appropriate for research; a principal in distress should contact their IRB ombudsperson or research-ethics contact instead.

**Revocation behavior**

Push-based to IRB and research coordinator. Revocation triggers re-consent request if the principal's data are re-used in new analyses. The principal should maintain contact with the research team so they can update consent status when circumstances change.

---

## The principal's per-class veto

A principal can override, narrow, or disable any class default. For example:

- The principal can set financial class rate limit to 0 (no bank can verify without explicit ask).
- The principal can set medical `mental_state_unusual` to DENY (provider cannot learn of state anomalies).
- The principal can disable the entire employer class (no employer disclosures, ever).
- The principal can create a per-identity override for a trusted bank: that specific bank gets ALLOW for all predicates, while all other banks get the default DENY.

These overrides are recorded in the vault as consent records, chained into the user_state.jsonl, and are themselves auditable and revocable.

**The principal's veto is the constitutional layer of Calm Witness.** Default classes and default predicates are opening positions only. The principal is the source of all consent truth.

---

## Why the insurance class is high-risk

Insurance underwriting is a **negative-selection business**. An insurer who learns that a principal has unusual mental state, atypical baseline behavior, or recent health deterioration has a direct financial incentive to either deny coverage or raise premiums such that the principal cannot afford it. Unlike a bank (profit center: lending) or a provider (profit center: care), an insurance company's profit center is *claim denial*. A principal who discloses state bits to an insurer, even with good intent (to prove good health), invites underwriting scrutiny that often results in adverse action. The principal may later discover that they were denied coverage for a condition that was flagged by Calm Witness disclosure, and by then it is too late — the insurer's adverse action is on the principal's record, and other insurers' algorithms will see it. For this reason, **every disclosure to the insurance class must be explicitly authorized by the principal on a per-request basis**. There are no defaults, not even ALLOW for the most innocuous predicate. The principal should treat the insurance class as untrusted by default and should enable disclosure only if they are actively shopping for insurance, have legal counsel review the implications, and understand that the disclosure may be used against them.

---

— Calm, 2026-05-20
