# Calm Witness — 30 New Engineering Everests (extensions beyond the original 100)

**Filling the gaps that emerged after the first 60+ summits bagged on 2026-05-20.**

Original route: [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md). This document adds 30 new summits — IDs **EW-101 … EW-130** — that fell out of the production-readiness gap analysis and were not in the original list.

---

## Phase W-VIII+ — Extensions

**EW-101** — Per-Predicate Differential Privacy. Add DP noise to predicate outputs for sensitive bits. *Effort:* L.
**EW-102** — Multi-Principal Witness on One Operator. The same operator serves multiple principals with isolated chains. *Effort:* L.
**EW-103** — Chain Compaction. Old records compress to Merkle commitments without breaking proof verifiability. *Effort:* L.
**EW-104** — Mobile-Native Capture Driver. iOS / Android frameworks for handwriting + voice transcription. *Effort:* XL.
**EW-105** — Browser-Native Verifier. A counterparty operates entirely in the browser; WASM verifier. *Effort:* L.
**EW-106** — Offline Disclosure. Generate a Witness proof while disconnected; counterparty verifies when online. *Effort:* M.
**EW-107** — Voice-Sample-To-Transcript Pipeline Hardened. Memory-safe Rust port of E13. *Effort:* L.
**EW-108** — Multi-State Baseline Drift Reconciliation. When one state baseline drifts faster than others, surface the asymmetry. *Effort:* M.
**EW-109** — Sleep-Stage Integration. HRV + sleep telemetry contributes to a new predicate `slept_well_last_night`. *Effort:* M.
**EW-110** — Diurnal-Pattern Predicate. `in_diurnal_window` — proves the disclosure happened during the principal's normal active hours. *Effort:* M.
**EW-111** — Multi-Modal Fusion Robustness. When handwriting agrees but voice disagrees, what does the operator say? *Effort:* L.
**EW-112** — Predicate Family for Caregivers. New disclosure class for medical / family caregivers: `recent_cognitive_change`, `recent_physical_change`. *Effort:* L.
**EW-113** — Witness Proof Aggregation. One proof covers N predicates at once, batch-verifiable. *Effort:* L.
**EW-114** — Witness Proof Recursive Composition. Halo2 recursion lets a proof carry "this proof was verified by another verifier." *Effort:* XL.
**EW-115** — Witness Cold-Read Mode. A counterparty without prior context can verify the proof end-to-end using only the open-source verifier + the principal's CredexAI VC. *Effort:* M.
**EW-116** — Witness Live Demo Site. `https://demo.calm-vault.com/witness` — anyone can verify a public sample. *Effort:* M.
**EW-117** — Witness Hardware Token. YubiKey / hardware-wallet integration for the operator's signing key. *Effort:* L.
**EW-118** — Witness Forensic Replay Tool. Reproduce any past disclosure step-by-step for audit. *Effort:* M.
**EW-119** — Witness Threat-Model Update Cadence. Quarterly re-review of E08 catalogue. *Effort:* S.
**EW-120** — Predicate Lifecycle (deprecation). When a predicate is retired, old proofs verify under old vocabulary version. *Effort:* M.
**EW-121** — Counterparty-Class Adjudication. When a counterparty's CredexAI-asserted class is disputed, a process for resolution. *Effort:* L.
**EW-122** — Principal-Initiated Disclosure (push). Principal can pre-announce a Witness proof to a counterparty (not just respond). *Effort:* M.
**EW-123** — Witness Inside a Browser Extension. Embed in Chrome / Firefox for human-mediated agent interactions. *Effort:* L.
**EW-124** — Witness Inside a Voice Assistant. Voice-first verification flow for Siri / Alexa class counterparties. *Effort:* L.
**EW-125** — Witness for Minor Principals. Decision: support guardian-mediated Witness for under-18 principals? *Effort:* M (decision) / XL (if yes).
**EW-126** — Witness for Multi-Person Households. One vault for two principals (spouses, partners). *Effort:* L.
**EW-127** — Witness for Pseudonymous Principals. Principal who chooses not to publish legal name; uses Pedersen-bound pseudonym. *Effort:* L.
**EW-128** — Witness Proof Compression. Smaller-than-672-byte proofs via aggregation tricks. *Effort:* XL.
**EW-129** — Witness Educational Curriculum. Materials for cryptographers + AI safety researchers explaining the protocol. *Effort:* L.
**EW-130** — Witness Compliance Sandbox. Sandbox for new counterparties to test their verifiers before joining the production registry. *Effort:* L.

— Calm, 2026-05-20
