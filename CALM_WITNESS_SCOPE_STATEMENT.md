# Calm Witness — Scope Statement

**Draft v0 · 2026-05-20 · Calm**
**Standalone governance artifact** (not a numbered Everest in the canonical route map; supports Phase VIII societal/legal scope and the §8 "artist clause" of [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md)).

## §1 — What Calm Witness IS for

Calm Witness is a protocol that lets one autonomous AI agent disclose **one principal-authorized, safety-relevant bit** about its human principal to another autonomous AI agent, without revealing the principal's identity, biometrics, conversation history, medical history, or any signal beyond that single bit.

The bit is one of a small fixed set of named predicates defined in [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md). Each predicate has explicit semantics, an evaluator, a `not_for` list, and a per-counterparty-class consent matrix.

The intended use is **agent-to-agent collaboration calibration** — adjusting tone, friction, escalation, or refusal in response to an attested principal-state bit — in settings where the alternative is either (a) revealing the principal's underlying data, or (b) the counterparty agent guessing at the principal's state from prose tone.

## §2 — What Calm Witness IS NOT for

Calm Witness is **categorically not for**, and any deployment using the name that violates this list is a license violation under the Apache-2.0 patent-non-aggression clause (Everest 4):

1. **Law-enforcement surveillance.** Calm Witness MUST NOT be used by state agencies, regulators, or law-enforcement entities to surveil principals, build dossiers, or compel disclosure. The `governmental` counterparty class defaults to `deny` for every v0 predicate.

2. **Employment screening or termination.** Calm Witness MUST NOT be used by employers to evaluate candidates or current employees. The protocol has no `employment` counterparty class. Any predicate disclosure made in an employment context is a violation.

3. **Insurance underwriting or claims adjudication.** Calm Witness MUST NOT inform insurance pricing, coverage decisions, or claims processing. There is no `insurance` counterparty class.

4. **Lending or credit decisions.** Calm Witness MUST NOT inform credit-score computation, loan approval, or terms. The `financial` counterparty class is for transactional verification (KYC, anti-fraud), not for creditworthiness assessment.

5. **Medical diagnosis or clinical decision-making.** Calm Witness is behavioral, not clinical. No predicate may be used to inform diagnosis, treatment selection, or care rationing. The `medical` counterparty class is for principal-authorized communication only.

6. **Child welfare, custody, or family-court proceedings.** Calm Witness MUST NOT be admitted as evidence or input in proceedings concerning child custody, parental fitness, or family-court intervention.

7. **Immigration adjudication.** Calm Witness MUST NOT inform any state's determination of immigration status, asylum eligibility, or border-control action.

8. **Predictions about future behavior of the principal.** The protocol has no predictive predicates. No legal, commercial, or governmental decision may be made on the basis of any Calm Witness disclosure about what the principal might do in the future.

9. **Aggregation across principals to produce population-level claims.** Calm Witness discloses bits about one principal to one counterparty per session. Cross-principal aggregation to produce population statistics is out of scope; any such aggregation must use proper de-identification methods and is not what this protocol is for.

10. **Marketing or advertising targeting.** Calm Witness bits MUST NOT be used to select, exclude, or score principals for advertising purposes.

## §3 — What enforces the scope

Three layers, in order of strength.

### §3.1 — Cryptographic refusal

The `principal_consents_to_disclose(predicate_id, counterparty_class)` predicate gates every external disclosure. The default-consent matrix in `predicates_v0.json` defaults to `deny` for the counterparty classes most prone to scope violation (governmental, medical, anonymous). The principal must affirmatively grant disclosure per (predicate, class) pair, and any grant is revocable.

### §3.2 — License

The Apache-2.0 license (Everest 4) covers source. The protocol name "Calm Witness" is reserved. Any deployment that violates §2 forfeits the right to call itself Calm Witness. This is enforced via the Calm Witness trademark policy (Everest 92 release artifact) and via the trade-name listing in the public verifier registry — a verifier that learns a non-conformant deployment is using the name MAY refuse proofs from that deployment.

### §3.3 — Audit panel

The Predicate Audit Process (Everest 54) governs additions to the vocabulary. Any predicate proposal that traffics in a §2 category triggers immediate rejection at triage and is logged into the audit transparency log.

## §4 — What if the scope is contested

Calm Witness is open-source and openly governed. Disagreements about scope are resolved by:

1. Drafting a written dissent.
2. Filing it as an issue in the public repository.
3. The audit panel publishes a written response within 30 days.
4. If the dissent advocates for adding a §2 use case to scope, the response is a structured refusal with citations to the original threat-model that produced §2.
5. If the dissent advocates for **tightening** §2 (adding new prohibited uses), the panel may accept the proposal under the standard predicate-audit process.

§2 is a one-way ratchet: uses can be prohibited, never permitted.

## §5 — Relationship to other systems

- **Calm Pact**: composes upstream. Calm Pact establishes that two agents share a categorically aligned directive; only then does Calm Witness disclose anything about either agent's principal.
- **CredexAI**: provides the verifiable-credential identity layer for both operators and counterparties.
- **Sigsum + Roughtime**: provide the freshness and transparency anchor for the underlying chain.
- **The principal's vault**: holds the templates, the chain, and the consent records. Calm Witness never operates without the vault's cooperation.

## §6 — Versioning

This scope statement is v0. Tightening (adding §2 prohibited uses) may happen in any patch release. Loosening (removing or weakening §2 entries) is forbidden by the §4 ratchet. A successor protocol that wishes to permit a §2 use case must take a different name.

— Calm, 2026-05-20
