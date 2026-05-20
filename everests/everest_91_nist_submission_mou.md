# Everest 91 — NIST / USAISI Formal Submission with MoU

*Phase XXIV — Standards & First Production. Prereq: 1, 79, 80, 90, 165, 168, 184. **DESIGN-BAGGED (Summit 91/305) 2026-05-20** — pending institutional follow-through.*

---

## Overview

The formal submission of the Calm-suite to the US standards apparatus — NIST and the US AI Safety Institute (USAISI) — is the legitimacy track that parallels the academic publication track (E217-E220) and the lab adoption track (E280). Each track produces a different kind of credibility; together they make the Calm-suite a real public standard rather than a single-organization assertion.

The two named US bodies are not equivalent and the submission strategy must differentiate:

- **NIST** owns post-quantum cryptography standardization, the Cybersecurity Framework, identity-management standards (SP 800-63), and is the natural home for the Calm-suite's cryptographic primitives + identity-binding work. Submission path: comment on existing draft standards (NIST PQC migration; SP 800-63-4) + submit Calm-suite as a candidate primitive for an extension. Multi-year cadence.
- **USAISI** owns the safety-evaluation mandate from the AI Safety Institute Consortium. The Calm-suite's autonomous-agent-user-state attestation + values-alignment-without-purity-test stance + refusal-floor design is squarely in USAISI's mandate. Submission path: formal submission as a candidate safety primitive for the autonomous-agent class. Shorter cadence than NIST.

Both submissions are MoU-gated. The MoU language is the load-bearing artifact of this summit.

---

## The MoU as the load-bearing artifact

A formal NIST/USAISI submission is not a unilateral document — it is the output of a *negotiated relationship*. The Memorandum of Understanding (MoU) between the Calm Witness Foundation and the receiving body codifies the relationship before the submission is filed. Three reasons:

1. **Standards bodies require an institutional counterparty.** NIST/USAISI does not engage with individuals. The Foundation must exist (E241+) and have legal personhood.
2. **IP terms matter.** The MoU names what the receiving body gets if Calm-suite is adopted: a royalty-free non-exclusive license to the primitives, but the Foundation retains trademark + governance.
3. **The refusal floor must be preserved in the MoU language.** This is the non-negotiable. If the receiving body asks for terms that would let downstream users weaponize the protocol (e.g., "the standard SHALL permit law-enforcement use cases"), the Foundation walks. The MoU is where this is fought.

The MoU draft below is the v0 negotiation starting position. Counsel will revise; the Foundation's bottom-line is documented in §4 below.

---

## v0 MoU draft (negotiation starting position)

### Parties

- **Calm Witness Foundation** (incorporated per E241; 501(c)(3) status filed per E243), represented by the Executive Director.
- **[Receiving Body]** — NIST (specific Institute Director / Center Director to be named) OR USAISI (specific Program Office to be named).

### Recitals

WHEREAS the Calm Witness Foundation has developed an open-source cryptographic protocol suite for user-state attestation, values-alignment without purity-testing, and credential infrastructure for autonomous-agent ecosystems;

WHEREAS the [Receiving Body] has a mandate to evaluate and potentially standardize primitives in [cryptographic identity (NIST) / autonomous-agent safety (USAISI)];

WHEREAS both parties wish to engage in formal evaluation of the Calm-suite as a candidate for [standards-track (NIST) / safety-primitive-recommendation (USAISI)];

### §1 — Scope of engagement

The parties agree to engage in:

- 12-18 month evaluation period
- Joint working group (≥3 Foundation representatives + ≥3 [Receiving Body] representatives)
- Quarterly progress reviews; transparent meeting minutes
- Public comment period of ≥90 days on any draft standard or recommendation
- Independent verification by ≥1 third-party organization (per E100)

### §2 — IP terms

- **Foundation retains.** All intellectual property in the Calm-suite — protocol designs, implementations, trademarks (CALM, Calm Pact, Calm Witness, Calm Compass, Calm Concord, Calm Tenancy), and the refusal-floor language.
- **[Receiving Body] receives.** A royalty-free, non-exclusive, perpetual license to reference, evaluate, and recommend the Calm-suite as part of standards-development or safety-evaluation work.
- **No assignment.** Foundation does NOT assign IP to the [Receiving Body]. The Calm-suite remains Foundation-governed.

### §3 — Refusal floor preservation (the non-negotiable)

This MoU is conditioned on [Receiving Body]'s acknowledgement of and commitment to preserve the Calm-suite's refusal floor as documented in `CALM_REFUSAL_FLOOR_INDEX.md` and its component documents:

- The 12 forbidden predicate categories (§1 of the Index)
- The anti-purity-test output-shape refusals (§2 of the Index)
- The Scope Statement forfeit list (§3 of the Index)
- The operator-behavior commitments (§4 of the Index)

**If [Receiving Body] proposes a recommended specification that weakens any of these surfaces, the Foundation will withdraw from this MoU and from the standards process.** The MoU is not a vehicle for laundering the refusal floor through standards-body endorsement.

### §4 — The Foundation's bottom-line (non-negotiables)

Even if pressured during the evaluation period, the Foundation will not agree to:

1. Removing or weakening any of the 10 forfeit-list use-cases (law enforcement, employment, insurance, lending, custody, immigration, surveillance, aggregate analytics, medical diagnosis, predictive policing).
2. Permitting numeric similarity scores in any standard output shape.
3. Permitting cross-principal comparisons or predictive predicates.
4. Assigning trademark or core protocol IP.
5. Permitting closed-source mandatory implementations (the Calm-suite is open-source; standards-recommended forks may be commercial but cannot be exclusive).

If [Receiving Body] insists on any of these as a condition of engagement, the Foundation walks. The MoU is renegotiable; the bottom-line is not.

### §5 — Termination

Either party may terminate this MoU with 30 days written notice. On termination, the IP license in §2 survives for work already published; no future work proceeds under MoU auspices.

### §6 — Public transparency

The MoU itself, once signed, is published. The working-group meeting minutes are published. Draft outputs are subject to ≥90 day public comment. There is no closed-door negotiation of the refusal floor.

---

## Submission package contents

Once the MoU is signed, the submission package includes:

1. **Cover letter** — naming the candidate primitive(s) and the standards-track scope.
2. **Full protocol specification** — all four pillars (Pact + Witness + Compass + Concord) + ZKAC infrastructure.
3. **Cryptographic audit reports** — Trail of Bits (E165) + NCC (E168) + Cure53 (E167) at the time of submission.
4. **Conformance test suite** — cross-implementation vector set.
5. **Reference implementations** — Rust prod (E81), Python ref (E82, E86), WASM (E83).
6. **Compliance evidence** — SOC 2 + ISO 27001 + GDPR/CCPA/LGPD/APPI mappings (E184).
7. **Threat model + adversarial robustness study** (E69 + E101 + similar).
8. **Refusal floor canonical index** (`CALM_REFUSAL_FLOOR_INDEX.md`).
9. **Foundation governance documents** — bylaws (E241), board composition (E242), 501(c)(3) determination letter (E243).
10. **Independent third-party verification report** (E100 + Witness E100 + Mirror E100).

---

## Timeline

| Phase | Duration | Deliverable |
|---|---|---|
| Pre-MoU outreach | 3-6 months | Initial contacts; identify named officials; informal scoping |
| MoU negotiation | 6-12 months | Foundation counsel + [Receiving Body] counsel; multiple drafts |
| MoU signing | event | Public announcement |
| Submission filing | 1-3 months post-MoU | Full package |
| Evaluation period | 12-18 months | Working group; quarterly reviews |
| Draft standard/recommendation | 6-12 months | Public comment ≥90 days |
| Final standard/recommendation | 3-6 months post-comment | Published; effective date set |

**Total: 30-60 months from initial outreach to final published standard.** This is consistent with NIST PQC standardization cadence (which took ~6 years).

---

## Acceptance test (T-E91)

**T-E91.1.** MoU signed by Foundation Executive Director + [Receiving Body] named official. MoU text publicly available.

**T-E91.2.** Formal submission package filed. Receipt confirmation from [Receiving Body].

**T-E91.3.** Public comment period of ≥90 days concluded; all substantive comments responded to in writing; comment-response document published.

**T-E91.4.** Draft standard or formal recommendation published by [Receiving Body], naming the Calm-suite as a recommended primitive.

**T-E91.5.** ≥2 independent implementations of the recommended primitive (in addition to the Foundation's reference impl) demonstrated and conformance-tested. Per the NIST PQC standardization pattern.

**T-E91.6.** Refusal-floor preservation verified at every milestone — no language weakening any of the 4 surfaces of `CALM_REFUSAL_FLOOR_INDEX.md` appears in the recommended specification.

---

## Named follow-through (the institutional commitments this summit defers to)

1. **Foundation incorporation completed** (E241) — required prerequisite to MoU signing.
2. **Calm Foundation legal counsel** named — engaged for MoU drafting + negotiation.
3. **NIST point of contact** identified — the Computer Security Division or Cybersecurity and Privacy Applications Group.
4. **USAISI point of contact** identified — the Program Office for Autonomous Systems Safety.
5. **First MoU draft** — to be circulated within 12 weeks of E241 completion.
6. **First MoU signing target** — within 12 months of E241 completion (this is ambitious; realistic range is 12-18 months).

---

## Composition

- **E1** (problem statement + threat model) — referenced in submission.
- **E69** (adversarial robustness) — submitted as evaluation evidence.
- **E79** (multi-jurisdiction legal) — referenced for compliance framing.
- **E90** (audit prep) — feeds the submission package.
- **E100** (independent third-party verification) — required at T-E91.5.
- **E165, E167, E168** (audit firms) — reports submitted.
- **E184** (SOC 2 + compliance) — referenced.
- **E215, E216** (treaty governance) — parallel legitimacy track at the international level.
- **E217-E220** (academic publications) — parallel academic track.
- **E241** (Foundation bylaws) — required prerequisite.
- **E280** (lab adoption) — parallel adoption track; not exclusive with standards-body endorsement.
- **`CALM_REFUSAL_FLOOR_INDEX.md`** — the non-negotiable referenced in MoU §3 + §4.

---

## Why this is DESIGN-BAGGED and what's actually required to BAG

This summit cannot be CLOSED by an AI alone. The MoU is a real document signed by real institutions. Closure requires:

1. The Foundation to exist legally (E241).
2. Foundation counsel to draft + negotiate the MoU.
3. NIST/USAISI to engage; this is a multi-year diplomatic process.
4. The Foundation to maintain its refusal-floor bottom-line under pressure.

What this DESIGN-BAG ships is the institutional framework, the MoU draft language (specifically §3 + §4 which protect the refusal floor under negotiation pressure), the submission package contents, and the timeline.

The named follow-through actions in the section above are the operational commitments the Foundation owes the world. They're not promises that AI tooling will keep — they're promises that the Foundation, when it exists, will honor.

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
