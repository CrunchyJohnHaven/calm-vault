# Calm Witness — Independent-Evaluator Spec v0 (S107)

## Why

Phase IX of the 200-summit route introduces values-alignment predicates: structured claims that a principal's behavioral signals meet specified alignment criteria. These predicates carry cryptographic weight. They are anchored in the ZKBB attestation chain and feed the trust ledger that governs principal access tiers.

That weight is only defensible if the evaluators producing the predicates are themselves auditable. A predicate evaluated by a closed-source model — one whose prompt, weights, or scoring thresholds are private — does not satisfy the tamperproof standard established in S104. At worst, it inverts the protocol's purpose: Calm Witness becomes the sole arbiter of whether a principal aligns with Calm Witness's own values, with no external check. Structural circularity of this kind disqualifies the attestation.

This spec defines the evaluator-independence requirement. Any values-alignment predicate introduced after ratification of S107 must comply. Predicates in production at ratification date have a 60-day remediation window.

---

## Mandatory Components

Each evaluator bound to a values-alignment predicate must supply all three of the following. Absence of any component is a blocking defect.

### (a) Public Deterministic Feature Extractor

The feature extractor transforms raw principal-state data (text, behavioral logs, interaction records) into a numeric or categorical feature vector. Requirements:

- Source code published under an OSI-approved license in the Calm Witness public repository.
- Fully deterministic: given identical input, output is bit-identical across runs and environments. No stochastic operations, no random seeds, no external API calls inside the extractor.
- Permitted extractor types: marker-vocabulary match counts, n-gram frequency vectors, stylometric features (type-token ratio, average sentence length, punctuation density, function-word profiles), lexical diversity metrics, structural parse features.
- Each predicate's extractor must declare its input schema (field names, types, units) and output schema (feature names, value ranges) in machine-readable form alongside the code.

### (b) Public Scoring Function

The scoring function maps the feature vector to a predicate outcome (pass/fail or a calibrated score). Requirements:

- Published in the same repository as the extractor. Source code or a fully specified mathematical definition (closed-form expression, decision tree, lookup table) — not a trained neural network with opaque internal weights unless model weights are also published.
- Threshold rules must be explicit numeric constants or per-principal calibration parameters derived from the reference corpus (see (c)). No threshold may be determined at inference time by a system not covered by this spec.
- If the scoring function is calibrated per-principal, the calibration procedure must be reproducible from public data alone.

### (c) Public Training / Calibration Corpus

The corpus against which the scoring function's thresholds are derived. Requirements:

- Either publicly released (permissive license, stable URI, content-addressed checksum) or, if privacy-sensitive, represented by a public calibration metadata artifact that includes: corpus size by stratum, summary statistics for all features in the extractor output schema, calibration timestamp, and the identity of the responsible curator.
- Corpus version pinned in the predicate definition. Corpus updates require predicate re-certification and a new summit bag.
- No corpus whose construction or labeling process is entirely undocumented. Labeling guidelines must be public even if labels themselves are withheld for privacy.

---

## Prohibited Patterns

The following evaluator patterns are prohibited unconditionally for values-alignment predicates:

- **Closed-source LLM judges.** Any model whose weights, architecture, or training data are not publicly disclosed.
- **Opaque proprietary scoring services.** Evaluation via API calls to services that do not expose their internal logic, regardless of vendor reputation.
- **Private-prompt evaluation.** Any setup in which the prompt or system instruction sent to an LLM is not publicly readable.
- **Undocumented human review.** Human-in-the-loop evaluation where the review rubric, reviewer selection criteria, and inter-rater reliability data are not published.
- **Post-hoc threshold tuning.** Adjusting thresholds after observing a specific principal's data without logging the adjustment, its rationale, and re-running the full calibration audit trail.

---

## Allowed LLM-Judge Usage

LLM-based evaluators are permitted for values-alignment predicates under strict conditions. All three conditions must hold simultaneously:

1. **Prompt is public.** The complete system prompt and all static user-turn templates are published in the Calm Witness repository, content-addressed, and referenced by hash in the predicate definition.
2. **Model and version are pinned and certificate-attested.** The exact model identifier (provider, model name, version string) is fixed in the predicate definition. A certificate from the model provider or an independent attestor confirms that the named model version is available for reproducible inference. Floating version aliases (e.g., "latest") are not permitted.
3. **Evaluator is third-party reproducible.** Any party holding the public prompt and access to the pinned model can reproduce the evaluation on the same input and obtain the same outcome. The predicate definition must include a reproducibility test vector: one example input with its expected output, verified at the time of predicate certification.

LLM-judge evaluators meeting the above may be used as one component of a composite evaluator but may not be the sole basis for a values-alignment predicate that triggers access-tier changes.

---

## Verification Procedure

At predicate certification time, the certifying agent (Calm or designated reviewer under E54) must:

1. Confirm all three mandatory components are present and linked by content-addressed reference.
2. Run the feature extractor and scoring function on the public calibration corpus (or its metadata equivalent) and confirm outputs match declared statistics within tolerance.
3. If an LLM-judge component is present, execute the reproducibility test vector and log the result.
4. Record a certification artifact — a structured JSON object containing predicate ID, extractor hash, scoring function hash, corpus checksum or metadata hash, certification timestamp, and certifier identity — and append it to the S127 registry.

Predicates that fail verification are suspended. Suspended predicates emit no attestation until remediated and re-certified.

---

## Cross-References

- **S104** — Tamperproof User-State Attestation Charter (establishes the cryptographic anchoring standard that predicate evaluators must satisfy).
- **S127** — Evaluator Registry (the ledger of all certified evaluators; certification artifacts defined in the Verification Procedure above are appended here).
- **S132** — Vocabulary Governance (governs the marker vocabularies used by feature extractors under component (a); vocabulary version pinning follows S132 rules).
- **E54** — Review Process (defines the designated reviewer role, review cadence, and escalation path for predicate certification disputes).

---

Calm 2026-05-20
