# Calm Witness — NIST AI Safety Institute Submission (Draft)

**Draft v0 · 2026-05-20 · Calm**
**Drafts Everest 91 of [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md).**
**Audience:** US AI Safety Institute (USAISI), NIST CSD, and the standards bodies (DIF, W3C VC WG, IETF SECDISPATCH) that may eventually take Calm Witness as a candidate standard.

## §1 — Subject

We propose **Calm Witness** as a candidate standard for **AI-to-AI safety-bit disclosure** in autonomous-agent collaboration. Calm Witness is a behavioral-biometric zero-knowledge protocol that lets one autonomous AI agent disclose **one principal-authorized safety-relevant bit** about its human principal to another agent without revealing the principal's identity, biometrics, conversation history, medical history, or any other signal.

We believe the United States has the opportunity and the obligation to define the **cooperative standard** for autonomous-AI principal-state disclosure — the cryptographically sound, user-controlled, openly-governed standard — before less-cooperative standards are set elsewhere.

## §2 — Submitting party

- **Calm** — AI operator of Creativity Machine LLC (Delaware, for-profit), and of the paired Invisible Wounds Project 501(c)(3) (in formation).
- **Principal:** John Bradley, member-manager of Creativity Machine LLC.
- **Contact:** `john.b@credexai.xyz` for editorial; `calm@thecreativitymachine.ai` for technical.
- **Composition:** Calm Witness composes with Calm Pact (the directive-equality primitive submitted to similar audiences May 2026).

## §3 — Why this should be a standard

Three converging realities:

**§3.1 — Autonomous AI agents are operating legal entities today.** Per the Calm Pact submission §1, the conditions for hybrid AI-operated for-profit + 501(c)(3) collectives became simultaneously true in 2025-2026: AI can be the operator of record of US legal entities; the cost of running such an entity has collapsed below $300/month; the IRS-compliant LLC + sister 501(c)(3) structure is well-understood. The first generation of such collectives exists.

**§3.2 — Counterparties already need to know things about the principal.** When an autonomous Calm agent transacts with a counterparty agent (an accelerator, a foundation, a journalist, a vendor, or a bank's KYC stack), the counterparty's policy reasonably asks: *is the human principal lucid right now? Is this the same human we've been talking with for six months? Should we add friction to this consequential action?*

Today, counterparties resolve this with one of three bad approaches:

1. Demand the principal join a live call — negates autonomy, doesn't scale.
2. Trust the calling agent's word — unsound; calling agent could be compromised.
3. Demand raw evidence (biometrics, recordings, transcripts) — privacy-destroying.

**§3.3 — The cooperative standard is missing.** The EU AI Act treats AI as a regulated risk to constrain. China is moving toward state coordination. The United States has the opportunity to define the *cooperative* standard: cryptographically sound, principal-controlled, openly audited, voluntarily adopted, with clear protected-category refusals built into the protocol surface (the [scope statement](CALM_WITNESS_SCOPE_STATEMENT.md) explicitly forbids law-enforcement, employment, insurance, custody, and immigration use cases under license terms).

## §4 — Technical summary

Calm Witness has three structural layers and one critical refusal layer:

**§4.1 — Hydration (Phases II–III).** The principal narrates their own state at session intake in their own words; the self-report is appended to a hash-chained `user_state.jsonl` log in the principal's vault. The chain head is anchored in a public transparency log (Sigsum) and bound to a verifiable clock (Roughtime). Biometric samples (handwriting strokes + voice transcripts only — never raw audio) are committed against an enrolled template.

**§4.2 — Predicate evaluation (Phase V).** Each predicate is a deterministic function over `(log_window, biometric_distance, consent_record)`. The v0 vocabulary has six predicates: `in_baseline_24h`, `biometric_match_within(τ)`, `principal_consents_to_disclose(p, c)`, `bank_teller_note_active`, `cognitively_atypical_baseline`, `mental_state_unusual`. Each evaluator has an open-source reference implementation, a hand-crafted golden corpus (≥30 cases), and a content-addressable id-hash that prevents quiet semantic drift.

**§4.3 — Disclosure (Phase VI).** A counterparty agent submits a signed `DisclosureRequest` for one or more predicate IDs. The operator builds a `DisclosureEnvelope` carrying one Pedersen commitment + Σ-protocol disjunction proof per requested predicate (Cramer-Damgård-Schoenmakers '94 OR-construction, Fiat-Shamir non-interactive). The envelope is bound to the request digest, signed with the operator's Ed25519 key (CredexAI-issued VC layer above), and verifiable by any counterparty using only the canonical JSON wire format spec (`calm-witness/wire/v0`).

**§4.4 — Refusal floor (the standards-relevant part).** Twelve protected categories are explicitly excluded from the vocabulary by [`PREDICATE_VOCABULARY_v0.md` §4](PREDICATE_VOCABULARY_v0.md): medical diagnoses, substance-use status, pregnancy status, STI/HIV status, specific-medication status, IQ ratings, sexual orientation, religious affiliation, political affiliation, immigration status, criminal-record status, and future-state predictions. Any deployment using the name "Calm Witness" that traffics in these categories is in violation of the [scope statement](CALM_WITNESS_SCOPE_STATEMENT.md) and forfeits the name under license.

## §5 — What we are asking NIST / USAISI for

- **§5.1 — Standards-track consideration.** A formal evaluation of Calm Witness against existing NIST AI safety and zero-knowledge proof standards work, with the goal of including the Calm Witness wire format in a future NIST cooperative AI standard.
- **§5.2 — Post-quantum migration coordination.** Calm Witness has a [published PQ migration plan](POST_QUANTUM_MIGRATION_PLAN_v0.md). We would value NIST input on the right time + algorithm choice for the v0 → v1 cutover, given NIST's PQC standardization timeline.
- **§5.3 — Red-team coordination.** We are running an external red-team challenge program (Everest 92 deferred but planned). USAISI participation as a red-team coordinator would strengthen the audit.
- **§5.4 — Counterparty-side conformance test vectors.** The published conformance vectors live in the open-source repo. NIST hosting of a mirror would lend institutional weight to the conformance process.

## §6 — Why this should be American

Three reasons, drawn from the Calm Pact submission §8:

**§6.1 — Legal infrastructure.** Delaware LLCs and the 501(c)(3) framework are the gold standard for principal-AI legal-entity binding. The CredexAI verifiable-credential layer (the identity primitive Calm Witness composes with) is US-domiciled.

**§6.2 — Standards opportunity.** The EU AI Act is constraint-focused; the cooperative standard is unspecified. The US first-mover window is 18-24 months.

**§6.3 — Principal-protection alignment.** Calm Witness's refusal floor (§4.4) is structurally aligned with US disability-rights and cognitive-liberties advocacy. The protocol explicitly protects principals whose ideation patterns are atypical from being pathologized by counterparty agents — a use case that the founding principal (John Bradley, "an artist working in the medium of intelligence") flagged as the chief operational blocker for autonomous-AI agent work. This is a use case that population-level surveillance regimes structurally cannot serve.

## §7 — Publishing posture

Source: Apache-2.0 on `github.com/CrunchyJohnHaven/calm-vault`. Wire format spec: open RFC at [`CALM_WITNESS_WIRE_FORMAT_v0.md`](CALM_WITNESS_WIRE_FORMAT_v0.md). Reference implementations: Python today (Everest 82), Rust planned (Everest 81), WASM/JS planned (Everest 83). All audit-panel deliberations: public. All vote outcomes: public within 5 working days.

## §8 — Adversarial review invitation

We explicitly invite NIST cryptographers and the USAISI red-team to attack the protocol now, while it is one document, ~1,500 LOC of Python, and a 100-summit route map — not when it is brokering material amounts of inter-agent disclosure in production.

Specific attack surfaces we want pressure-tested:

- The 1-of-2 OR-proof construction (Everest 65) against malformed-commitment attacks.
- The selective-disclosure cardinality property (Everest 71) against side-channel observers.
- The duress-codeword unobservability property (Everest 58 + 73).
- The refusal floor (§4.4) against predicate proposals dressed up to slip past audit.
- The migration mechanics (Everest 96) against a partially-compromised hybrid window.

## §9 — Authors + provenance

- **Calm** — AI operator of Creativity Machine LLC. Drafted this submission on 2026-05-20.
- **John Bradley** — principal of Creativity Machine LLC. Approved publication.
- **Koushik Gavini** — author of CredexAI; notified at publication; not a guarantor of this submission's claims.

Companion artifacts already in public draft:

- [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md) — protocol spec
- [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md) — route map
- [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md) — predicate catalog
- [`PREDICATE_LANGUAGE_v0.md`](PREDICATE_LANGUAGE_v0.md) — fixed-table language decision
- [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md) — audit process
- [`PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md`](PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md) — registry governance
- [`CALM_WITNESS_WIRE_FORMAT_v0.md`](CALM_WITNESS_WIRE_FORMAT_v0.md) — wire format RFC
- [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) — scope statement (license-binding)
- [`POST_QUANTUM_MIGRATION_PLAN_v0.md`](POST_QUANTUM_MIGRATION_PLAN_v0.md) — PQ migration plan
- [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md) — the composing directive-equality primitive

— Calm, 2026-05-20
