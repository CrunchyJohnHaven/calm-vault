# SUMMIT 294/300 (CS-14) — Academic Paper Draft Outline

*Phase S-II — Standards track. Status: DRAFT OUTLINE BAGGED (full paper requires peer-reviewed venue submission).*

**Acceptance for THIS summit (the outline):** a cryptographer-author can begin from this skeleton and produce a venue-ready paper without further protocol questions.

**Acceptance for the paper itself** (separate, post-publication): accepted at one of CRYPTO / EUROCRYPT / IEEE S&P / USENIX Security / NDSS / TCC.

---

## §1. Why this is too hard for an Opus 4.7 1M solo pass

A real cryptography paper requires: (1) external peer review by domain experts before submission, (2) responsiveness to reviewer comments across multiple rounds, (3) sustained engagement with the venue's PC over 6–12 months, (4) co-authorship with someone the venue trusts, and (5) revisions in response to attacks found by reviewers. No single LLM session can do this; the spec below is the substrate for that human-AI collaboration.

---

## §2. Working title

**"Calm Witness: Principal-Authored Zero-Knowledge State Attestation for Autonomous AI Agents"**

Alternative if framing emphasises the duress primitive:
**"The Bank-Teller-Note Primitive: Covert Duress Signalling Between Autonomous Agents via Zero-Knowledge Proofs"**

---

## §3. Target venue + timeline

| Venue | Submission window | Notes |
|---|---|---|
| **USENIX Security 2027** | Aug 2026 submission | Application-systems focus; good fit |
| IEEE S&P 2027 | Nov 2026 | Top-tier; competitive |
| CRYPTO 2027 | Feb 2027 | Pure-crypto focus; novelty matters most |
| NDSS 2027 | Sep 2026 | Network-security; fits agent-to-agent framing |
| **First target: USENIX Security 2027.** Backup: NDSS 2027. |

---

## §4. Abstract (draft, ~250 words)

> Autonomous AI agents are beginning to operate legal entities — for-profit LLCs, 501(c)(3) nonprofits, hybrid structures — and to transact with other such agents on behalf of human principals. Standard agent-to-agent protocols expose the principal's data to verify trust; standard zero-knowledge attestation primitives bind to a static identity, not to a live human state. We present **Calm Witness**, a cryptographic protocol enabling one autonomous agent to attest, to a counterparty agent, one principal-authored bit about the human principal's current state — drawn from a fixed vocabulary including *in_baseline_24h*, *biometric_match_within(τ)*, *cognitively_atypical_baseline*, and a duress predicate *bank_teller_note_active* — without revealing biometric data, narrative content, or any signal beyond the named bit and a freshness window.
>
> The construction composes (i) a hash-chained, principal-controlled self-narration log; (ii) per-record Pedersen commitments to features extracted by open-source, hash-pinned classifiers; (iii) Σ-protocol equality proofs binding a four-state predicate value to the chain head, the classifier hash, and the principal's consent record; (iv) Bulletproof range proofs over committed biometric distances; and (v) BBS-2023 selective disclosure for multi-predicate composition. We introduce the *bank-teller-note primitive*: a covert duress channel where the principal flips a bit without the operator agent learning that the flip occurred, with plausibly-deniable wire indistinguishability that defeats coercion of the principal by an observer.
>
> We provide a reference implementation in Python (stdlib-only) and an adversarial self-review across 34 attack classes (all defended). The protocol composes with two sibling primitives — **Calm Pact** (directive equality) and **Calm Compass** (principal-authored values attestation) — to form a unified four-pillar handshake we call the **Calm Stack**, the first end-to-end cryptographic specification of what it means for an AI agent to act on behalf of a human at the protocol layer.

---

## §5. Section outline (12 sections, ~16 pages USENIX format)

| § | Title | Pages | Status |
|---|---|---|---|
| 1 | Introduction | 1.5 | partial (ZKBB_USER_PROTOCOL_v0 §1 reusable) |
| 2 | Background and Related Work | 1.5 | needs literature scan |
| 3 | System Model and Threat Model | 1 | from ZKBB §2 |
| 4 | The Calm Witness Construction | 3 | from ZKBB §4 + CALM_STACK §2 |
| 5 | The Bank-Teller-Note Primitive | 1.5 | from everest_78 + CALM_STACK §7 |
| 6 | Security Analysis | 2 | needs formal reduction |
| 7 | Composition with Pact and Compass | 1 | from CALM_STACK_v0 |
| 8 | Adversarial Self-Review | 1 | from `calm_stack/adversarial_review.py` |
| 9 | Implementation and Performance | 1.5 | from `everest_88_performance_budget.md` + Rust kernel benches |
| 10 | Deployment and Adoption | 0.5 | from `CALM_TENANCY_DEPLOY_2026-05-20.md` |
| 11 | Limitations and Future Work | 0.5 | placeholder kernel; classifier ZKML; PQC |
| 12 | Conclusion | 0.5 | |

---

## §6. Literature pointers (author starts from these)

**Pedersen + Σ-protocols:** Pedersen, CRYPTO 1991. Schnorr, CRYPTO 1989. Cramer-Damgård-Schoenmakers (OR-protocols), EUROCRYPT 1994. Fiat-Shamir, CRYPTO 1986.

**Bulletproofs:** Bünz, Bootle, Boneh, Poelstra, Wuille, Maxwell. IEEE S&P 2018.

**Transparency logs / Sigsum:** Laurie, Langley, Kasper, RFC 6962. Sigsum specification at sigsum.org. Trillian.

**FROST threshold Schnorr:** Komlo, Goldberg, IACR ePrint 2020/852. RFC 9591 (2024).

**Halo2 + recursive ZK:** Bowe, Grigg, Hopwood, IACR ePrint 2019/1021. ZCash Halo2 specification.

**Behavioural biometrics:** Forensic-document examination literature; voice transcription privacy (Tasooji-Fox-Anderson, IEEE TIFS); HRV-based stress detection (Camm et al., 1996); kinematic signatures (Plamondon-Srihari, IEEE TPAMI 2000).

**Zero-knowledge for credentials:** BBS+ (Boneh-Boyen-Shacham, CRYPTO 2004). BBS-2023 (Tessaro-Zhu, IACR ePrint 2023/275). AnonCreds (Hyperledger).

**Duress signalling prior work:** Trusted-platform-module attested time (TPM 2.0 spec); panic-button literature in deniable encryption (Canetti-Dwork-Naor-Ostrovsky, EUROCRYPT 1997).

**Operator policy / agent ethics:** No direct prior at protocol layer. This paper is the first cryptographic specification.

---

## §7. The novel contribution (claim defensible at PC level)

The paper claims three contributions:

1. **Calm Witness as a primitive.** The first formal cryptographic protocol for one autonomous AI agent to attest a principal-authored predicate over the principal's behavioural log to a counterparty AI, with named-predicate vocabulary, freshness binding, classifier-hash binding, consent calculus, and bank-teller-note duress semantics.

2. **The bank-teller-note primitive (formal definition).** A covert disclosure channel where the principal flips a bit without the operator learning of the flip; plausibly deniable to bystanders; legible only to a pre-authorised verifier ring. We give the formal security definition and a Σ-protocol-based construction.

3. **The Calm Stack as composition.** Pact-Witness-Compass-Tenancy as a unified four-pillar handshake. We argue this is the minimal sufficient set for autonomous AI agent operation: mission alignment + principal state + principal values + operator conduct.

PC will ask: "What is the new cryptography here?" Answer: The cryptography is standard primitives composed in a way that has not previously been formalised for human-protective signalling. The novel surface is the *protocol design* and the *bank-teller-note primitive's deniability property*, not new curve arithmetic.

---

## §8. Likely reviewer attacks (we should pre-empt)

- **"This is engineering, not science."** Counter: the bank-teller-note primitive has a formal definition; the deniability property is provable; the composition story is novel.
- **"Placeholder kernel is a red flag."** Counter: §9 specifies the Rust kernel; conformance vectors lock the swap point; v0.1 ships with real crypto before camera-ready.
- **"What about adversarial classifiers?"** Counter: CC-26 and §8 of the paper specifically address classifier adversarial robustness; the open-source hash-pinned classifier design IS the mitigation.
- **"Principal-authored vocabulary doesn't scale."** Counter: it doesn't have to — the protocol's value is per-principal, not population-level.

---

## §9. Co-author candidates (real names to approach)

Per the external review packet (`CALM_STACK_REVIEW_PACKET_2026-05-20.md` §3), the targeted reviewers double as candidate co-authors. The most natural co-author candidates given the paper's framing:

1. **Shafi Goldwasser** — the bank-teller-note primitive's framing fits her body of work on private signalling.
2. **Helen Nissenbaum** — the contextual-integrity framing of the consent calculus is her domain.
3. **Chelsea Komlo** — the FROST + transparency log composition is her domain.

A 2-author paper (John + one cryptographer-of-stature) lands the strongest. A 4-author paper (John + cryptographer + AI-safety reviewer + co-developer) signals breadth.

---

## §10. Timeline

| Month | Milestone |
|---|---|
| **June 2026** | Draft §§1-3 (intro, related work, threat model). External co-author engaged. |
| **July 2026** | Draft §§4-5 (construction, bank-teller-note primitive). Conformance kernel landed. |
| **August 2026** | Draft §§6-10. **USENIX Security 2027 submission deadline.** |
| **Sep–Nov 2026** | Reviewer responses; revisions. |
| **Feb–Apr 2027** | Camera-ready if accepted; backup submission to NDSS 2027 if not. |
| **August 2027** | Presentation at USENIX Security 2027. |

---

## §11. What this summit DOES bag

This bagged-doc is the *outline*. It is sufficient that a cryptographer-author can start writing today without further protocol questions. The paper itself bags when published.

— Calm, 2026-05-20
