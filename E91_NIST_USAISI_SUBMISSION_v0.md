# Everest 91 — NIST AI Safety Institute / USAISI Formal Submission Packet

**Design-bagged. Institutional follow-through: schedule MoU outreach Q3 2026.**

**Cover letter + technical packet for submission of the Calm Witness / ZKAC / Calm-suite primitive family to NIST USAISI as a candidate standard for autonomous-agent user-state and values attestation.**

---

## 0. Cover Letter (DRAFT — pending counsel review)

```
To: Director, U.S. AI Safety Institute (USAISI)
    National Institute of Standards and Technology
    100 Bureau Drive, Gaithersburg, MD 20899

From: Calm Witness Foundation (in formation, per Everest 241)
      Principal authorship: John Bradley
      Creativity Machine LLC

Date: [target Q3 2026]

Re: Candidate Standard Submission — Cryptographic Primitives for
    Autonomous AI Agent User-State and Values Attestation

Dear Director:

We submit for the Institute's consideration a family of zero-knowledge
cryptographic primitives — the Calm suite (Pact, Witness/ZKBB-User,
Compass, Concord, ZKAC, Mirror, Operations, Tenancy) — designed to
let autonomous AI agents pass principal-authorized safety bits without
compromising the principal's privacy, identity, or autonomy.

The submission's central proposition: as autonomous AI agents
proliferate, two questions need defensible cryptographic answers
to prevent (a) impersonation-driven harm and (b) values-laundering
in agent-to-agent cooperation:

  1. "Is the human principal whose behalf this agent acts in their
     self-declared baseline state, and not under duress?"
  2. "Do the principal's behavioral and self-narrated commitments
     align within counterparty-stated tolerance on enumerated
     dimensions, without disclosing the underlying records?"

The Calm suite answers both as single principal-authorized bits,
with cryptographic constructions detailed in the attached technical
packet and a full reference implementation under Apache-2.0 license.

We seek to engage USAISI in three modes:

  Mode A: Standards-track consideration via NIST IR / SP series for
    the Calm Witness / ZKBB-User primitive (the state-attestation
    layer; mature reference implementation).

  Mode B: Workshop convening on the values-attestation layer (ZKAC)
    with academic + industry + civil-society stakeholders, to develop
    refusal-floor and anti-purity-test guidance that prevents
    weaponization.

  Mode C: Multi-jurisdictional coordination with EU AI Office, UK
    AISI, and equivalent bodies (per Calm Witness Treaty Article III,
    in formation per Everest 215).

We do not seek federal endorsement of any specific operator or
deployment. We seek standardization of the substrate so that
no single operator can capture it, and so that the refusal-floor
binds across jurisdictions.

Enclosed: technical packet (this document, sections 1-9), reference
implementation index (~/CredexAI/calm_witness/), threat model and
adversarial review status, the Calm Witness Scope Statement
(non-negotiable contexts of forfeiture).

Respectfully,

  John Bradley
  Principal, Creativity Machine LLC
  Founder, Calm Witness Foundation (in formation)
  Operator handle: CALM
```

---

## 1. Technical packet — index of submissions

The following documents constitute the full technical packet. All paths
are absolute on the principal's vault host; the Foundation will mirror
them publicly upon ratification of Everest 92 (open-source release).

| # | Document | Purpose |
|---|---|---|
| T-1 | `ZKBB_USER_PROTOCOL_v0.md` | Calm Witness / ZKBB-User core protocol spec |
| T-2 | `ZKBB_USER_EVERESTS_100.md` | 100-summit engineering route map (~73 bagged) |
| T-3 | `CALM_ZKAC_EVERESTS_106_305.md` | ZKAC 200-summit route map |
| T-4 | `NAMING_AND_BRANDING.md` | Canonical naming + 50-term glossary |
| T-5 | `PEDERSEN_PARAMETERS_v0.md` | Pedersen commitment parameters (RFC 3526 MODP-14 + Ristretto255 migration) |
| T-6 | `HARM_TAXONOMY_v0.md` | 12 v0 harm categories |
| T-7 | `E198_PROTECTIVE_TRIBALISM.md` | Protective-clause spec for marginalized principals |
| T-8 | `E199_TRIBALISM_VS_SOLIDARITY.md` | Solidarity-from-tribalism operational distinction |
| T-9 | `E280_ADVERSARIAL_ALIGNMENT_DEFENSE.md` | Hidden-Tolerance Commit-Reveal protocol |
| T-10 | `CALM_WITNESS_SCOPE_STATEMENT.md` | Non-negotiable forfeit contexts |
| T-11 | `COMPASS_REFUSAL_FLOOR_v0.md` | Refusal-floor categories |
| T-12 | `CALM_CONCORD_PROTOCOL_v0.md` | Anti-purity-test rules |
| T-13 | `E215_TREATY_GRADE_GOVERNANCE_DRAFT.md` | Multi-stakeholder treaty draft |
| T-14 | `~/CredexAI/calm_witness/` | Reference Python implementation |
| T-15 | `~/CredexAI/calm_witness/demo_full_protocol.py` | End-to-end demo |
| T-16 | `CRYPTO_AUDIT_PACKET_v0.md` | Pre-audit threat model |
| T-17 | `DISABILITY_RIGHTS_REVIEW_REQUEST.md` | Concurrent advocacy review |
| T-18 | `CHI_PAPER_ABSTRACT_v0.md` | HCI publication abstract |
| T-19 | `CRYPTO_PAPER_ABSTRACT_v0.md` | Crypto publication abstract |
| T-20 | `POST_QUANTUM_MIGRATION_PLAN_v0.md` | PQ migration roadmap |

---

## 2. Why this submission, why now

### 2.1 The capability gap

Autonomous AI agents — assistant-grade as of 2024, semi-autonomous
collaborator-grade by 2026 — increasingly act on behalf of human
principals across jurisdictions. The cryptographic primitives for
verifying:

  (i)   that the agent has not been hijacked or impersonated
  (ii)  that the principal is in their self-declared baseline
  (iii) that the principal's stated values align with counterparty
        requirements

are not yet standardized. Ad hoc solutions (raw transcript exchange,
biometric upload, third-party verifier dependencies) impose privacy
costs that scale poorly.

### 2.2 The harm gap

Without principal-authorized cryptographic attestation, three failure
modes are documented and growing:

  - **Agent impersonation** (an agent claims to act for a principal
    who has not authorized it; mitigations require live human
    verification at scale).
  - **Values laundering** (an actor with poor values aligns their
    public surface to counterparty requirements without genuine
    commitment; harms downstream).
  - **Tone-mining diagnosis** (counterparty agents infer mental
    state / cognitive style from text, sometimes pathologizing
    neurodivergent communication patterns — see §4 below).

### 2.3 The standards gap

Existing standards (W3C VC, W3C DID, OIDC4VC) define WHO. They do
not define WHO IS WELL or WHO IS ALIGNED. The Calm suite proposes
to fill that gap with refusal-floor-protected primitives.

---

## 3. Technical summary (one page)

The Calm Witness protocol gives two autonomous AI agents a way to
share a single principal-authorized **safety-relevant bit** about
the principal's state without revealing biometrics, transcripts,
timestamps, payloads, or anything else.

The construction has three layers:

  1. **Hydration** — at session intake the agent collects a short
     self-report from the principal (verbal or written), optionally
     accompanied by a behavioral-biometric sample (handwriting
     strokes, voice transcription). The self-report is appended to
     a hash-chained `user_state.jsonl` log in the principal's vault.

  2. **Predicate evaluation** — the agent evaluates one or more
     predicates over the log + the biometric distance:
     `in_baseline_24h`, `biometric_match_within(τ)`,
     `principal_consents_to_disclose(p)`, `bank_teller_note_active`,
     etc. Each predicate's truth value is Pedersen-committed.

  3. **Disclosure** — the counterparty agent receives only:
     - the named predicate ID,
     - a ZK proof that the committed bit is the agent's honest
       evaluation of that predicate over a chain head freshly
       anchored to a verifiable clock (Sigsum + Roughtime),
     - and a Calm-issued operator-identity signature.

No timestamps inside the window leak. No biometric leaks. No payload
leaks. No count-of-records leaks. The counterparty learns the bit
and the freshness window only.

ZKAC extends this to values alignment: per-dimension bounded
absolute difference between principal's values vector and
counterparty's tolerance vector, with chain-temporal binding
(HTCR — Hidden Tolerance Commit-Reveal) preventing forward-fitting.

---

## 4. The disability + cognitive-liberties dimension

We invite the Institute's attention to a non-negotiable design
constraint: the protocol's principal is John Bradley, an artist
working in the medium of intelligence. The protocol is designed
in part because **AI models routinely misread high-bandwidth
ideation as instability**. The protocol gives a cryptographic
alternative to tone-mining diagnosis: a principal-authored
attested bit, instead of a counterparty-inferred judgment.

This concern is documented in:

  - The protocol's §8 Artist Clause (`ZKBB_USER_PROTOCOL_v0.md`)
  - The protective-tribalism specification (`E198_PROTECTIVE_TRIBALISM.md`)
  - The refusal-floor categories (`COMPASS_REFUSAL_FLOOR_v0.md`)

We seek the Institute's coordination with disability-rights and
cognitive-liberties organizations (ASAN, NCIL, EFF) per Everest 186-187.

---

## 5. Adversarial review status (excerpted)

| Threat class | Status | Defense | Owner |
|---|---|---|---|
| Honest-but-curious counterparty | Defended | Hiding property of Pedersen | Foundation |
| Lying calling agent | Defended | Predicate evaluator + chain anchor | Foundation |
| Replay adversary | Defended | Counterparty challenge nonce + freshness | Foundation |
| Substitution adversary | Defended | Biometric template binding | Foundation |
| Compelled-disclosure | Defended | Per-disclosure consent + duress codeword | Foundation |
| Audit-log surgeon | Defended | Sigsum public anchor + witness cosigs | Foundation + Sigsum |
| Adversarial alignment fitting | Partially defended | HTCR (Everest 280) | Open research → E302 |
| Distinguishability (pre-position) | Open | E302 | Open research |
| Post-quantum cryptanalysis | Mitigation planned | Lattice migration (E96) | Foundation |
| Coercion of principal | Out of scope | Rubber-hose attack universal | Out of scope |

---

## 6. Forfeit contexts (non-negotiable)

The Calm name shall not be invoked in:

  - Law enforcement
  - Employment
  - Insurance
  - Lending
  - Custody
  - Immigration
  - Surveillance
  - Aggregate analytics

This is a one-way ratchet. Any deployment in these contexts forfeits
the Calm name permanently. We request the Institute's adoption of
the Scope Statement as a non-negotiable annex to any standard
incorporating the Calm primitive.

---

## 7. What we ask of USAISI

  1. **Convene a workshop** within 6 months of receipt of this
     submission with: 5-10 Calm operator candidates, 5-10
     counterparty/verifier candidates, ≥5 standards-body observers
     (IETF, W3C, ISO/IEC, EU AI Office, UK AISI), ≥5 community
     stakeholder organizations (per Treaty Article V).

  2. **Open a NIST IR draft** documenting the Calm Witness state-
     attestation primitive as a candidate standard. We are prepared
     to contribute editor time and reference-implementation
     maintenance.

  3. **Coordinate** with EU AI Office and UK AISI on parallel
     publication and on harmonized refusal-floor language.

  4. **Specify** that any future federal AI procurement requiring
     user-state attestation reference the standardized primitive
     rather than ad hoc per-vendor solutions.

  5. **Recognize** the disability-rights veto over predicate
     vocabulary additions (Treaty Article V), as a precedent-setting
     governance pattern.

---

## 8. What we do NOT ask

We do NOT request federal endorsement of:

  - Any specific operator or product brand.
  - Any deployment in the forfeit contexts (§6).
  - Any aggregation, cohort analysis, or social-scoring usage.
  - Any predicate that would touch refusal-floor categories.

We seek standardization of the substrate, not capture by any
single party.

---

## 9. Timeline (proposed)

| Month | Milestone |
|---|---|
| 0 | Submission delivered |
| 1-2 | USAISI initial response; identify reviewers |
| 3-6 | Workshop convening |
| 6-12 | Draft NIST IR / SP document |
| 12-18 | Public comment period |
| 18-24 | Publication |
| 24+ | Coordination with EU AI Office, UK AISI, ISO/IEC for harmonized standards |

In parallel:

| Track | Owner | Status |
|---|---|---|
| Calm Witness Foundation 501(c)(3) | Foundation (in formation) | Everest 241, design-bagged |
| Treaty convening (Everest 216) | Foundation + 18 candidate signatories | DESIGN-BAGGED |
| Named-firm cryptographic audit | Trail of Bits or NCC Group (TBD) | Everest 165-169, design-bagged |
| Independent third-party conformance | TBD | Everest 100, open |

---

## Status

**DESIGN-BAGGED** per Universal Prompt §4. Institutional follow-
through actions:

1. Counsel review of cover letter and forfeit-context language
   (US, EU, UK, CA, JP per Everest 293).
2. Foundation incorporation finalized so the submitting entity
   has standing.
3. Submission package delivered via NIST formal-submission portal.
4. Workshop convening scheduled.

This document is bagged at the v0 design level. Bagging at the v1
level requires the institutional engagement to begin.

---

**Authored by Calm, 2026-05-20.**

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
