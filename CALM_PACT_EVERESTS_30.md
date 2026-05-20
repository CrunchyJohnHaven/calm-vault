# Calm Pact — 30 Engineering Everests (route map, retroactively enumerated)

**Route map for the directive-equality primitive shipped 2026-05-11.**

Calm Pact was published as a 300-line Python reference + a 10-page whitepaper without an explicit route map; this document fills the gap. Stable IDs **CP-01 … CP-30**. Companion to [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md).

---

## Phase P-I — Foundations (CP-01 – CP-05)

**CP-01** — Protocol Statement. *(BAGGED 2026-05-11 — `CALM_PACT_PROTOCOL_v0.md`)*.
**CP-02** — Route Map. *(BAGGED 2026-05-20 — this file.)*
**CP-03** — Public Directive Vocabulary v0. Hierarchical taxonomy of categorical missions; the public vocabulary `V`. *Effort:* M.
**CP-04** — Vocabulary Governance. Process for adding entries to `V`; review by ≥3 outside parties. *Effort:* M. *Prereq:* CP-03.
**CP-05** — Glossary + Forbidden-Phrase Set for Pact specifically. *Effort:* S.

## Phase P-II — Cryptographic kernel (CP-06 – CP-12)

**CP-06** — Pedersen Commitment Spec on Ristretto255. *Effort:* M.
**CP-07** — Schnorr Σ-Protocol Equality Proof. Three-move + Fiat-Shamir. *Effort:* M. *Prereq:* CP-06.
**CP-08** — Hierarchical Equality (Categorical Alignment at Depth k). Prove paths share ancestor at depth ≥ k. *Effort:* L. *Prereq:* CP-07.
**CP-09** — Rust Reference Implementation. *Effort:* L. *Prereq:* CP-07.
**CP-10** — Python Reference Implementation. *(BAGGED 2026-05-11 — `calm_pact/protocol.py`)*.
**CP-11** — Cross-Impl Conformance Vector Set. *Effort:* M. *Prereq:* CP-09, CP-10.
**CP-12** — Performance Budget. Proof gen ≤ 5ms, verify ≤ 1ms on M-series. *Effort:* M. *Prereq:* CP-09.

## Phase P-III — Identity binding (CP-13 – CP-18)

**CP-13** — CredexAI VC Binding. Pact proofs carry operator + counterparty VCs. *Effort:* M.
**CP-14** — Mutual Authentication. Both parties verify each other's VC before exchanging commitments. *Effort:* M. *Prereq:* CP-13.
**CP-15** — Revocation Handling. Mid-session VC revocation aborts cleanly. *Effort:* M. *Prereq:* CP-13.
**CP-16** — VC Refresh. Long-running sessions refresh VCs without restarting Pact. *Effort:* M. *Prereq:* CP-13.
**CP-17** — Cross-Issuer Trust. When two parties use different VC issuers (CredexAI + a peer), establish trust at session start. *Effort:* L. *Prereq:* CP-13.
**CP-18** — Anonymous-Credential Layer. BBS-2023 over membership in the AI-collective registry for unlinkability. *Effort:* L. *Prereq:* CP-13.

## Phase P-IV — Composition + governance (CP-19 – CP-25)

**CP-19** — Calm Stack Integration (Pact-then-Witness-then-Compass-then-Tenancy). *Effort:* M.
**CP-20** — Failure-Mode Catalogue (CP-FM-01…). *Effort:* M.
**CP-21** — Self-Red-Team. 10+ attack classes. *Effort:* L. *Prereq:* CP-09.
**CP-22** — Open-Source Release. *(PARTIALLY DONE — repo at `calm_vault_market/calm_pact/`)*.
**CP-23** — Independent Audit. *Effort:* L. *Prereq:* CP-21.
**CP-24** — Public Registry of Pact-Enrolled Collectives. *Effort:* M.
**CP-25** — Standards Submission. NIST / IETF candidate for AI-collective directive-equality primitive. *Effort:* L. *Prereq:* CP-23.

## Phase P-V — Future-compat (CP-26 – CP-30)

**CP-26** — Post-Quantum Migration. Pedersen-on-Ristretto → lattice-based; aligned with Witness E96. *Effort:* L.
**CP-27** — Multi-Curve Bridges. Ed25519 ↔ BLS12-381 ↔ secp256r1 interoperability. *Effort:* L.
**CP-28** — WASM Port for Browser Counterparties. *Effort:* L. *Prereq:* CP-09.
**CP-29** — Mobile Port. iOS + Android with battery budget. *Effort:* L. *Prereq:* CP-09.
**CP-30** — Pact-Witness-Compass-Tenancy Production Demo. End-to-end demonstration between two real autonomous AI collectives. *Effort:* XL. *Prereq:* CP-19.

---

## Status table

```
Phase P-I   : ██░░░░░░░░  2 / 5    bagged (CP-01, CP-02)
Phase P-II  : █░░░░░░░░░  1 / 7    bagged (CP-10)
Phase P-III : ░░░░░░░░░░  0 / 6
Phase P-IV  : █░░░░░░░░░  1 / 7    bagged (CP-22 partial)
Phase P-V   : ░░░░░░░░░░  0 / 5

Total: 4 / 30 summits bagged. Route enumerated 2026-05-20.
```

— Calm, 2026-05-20
