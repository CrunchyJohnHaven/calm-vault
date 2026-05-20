# Calm Stack v0 — External Review Packet

**Submission date:** 2026-05-20
**Submitter:** John Bradley, principal of Creativity Machine LLC (Delaware), operating with autonomous AI operator "Calm".
**Subject:** A composition of three cryptographic protocols (Pact, Witness, Tenancy) into a unified specification for AI agent operation on behalf of a human principal.
**Contact:** john.b@credexai.xyz · `calm@thecreativitymachine.ai`
**License:** Apache-2.0. Patent non-aggression per the parent `calm-vault` repo.
**Repository (intended public mirror):** `github.com/CrunchyJohnHaven/calm-vault`

---

## 1. One-paragraph summary

The Calm Stack v0 is a three-protocol composition for autonomous AI agents acting on behalf of human principals. *Calm Pact* (May 11) lets two agents prove their directives are categorically equal without revealing them. *Calm Witness* (today) lets an agent attest one bit about the principal's user-state — drawn from a fixed v0 vocabulary of six predicates — to a counterparty agent under bank-teller-note disclosure semantics. *Calm Tenancy* (today) bounds how an agent conducts itself on every public surface: 10-minute auto-acknowledgement SLA on response-seeking inbound, 10-axis pre-publish cringe rubric, hard-block on operator-specified forbidden phrases, never-quote-credentials in outbound, and a daily tenancy check chained into the principal's vault. The first end-to-end Calm Session transcript was produced today at 15:58:34Z. We attacked the stack ourselves across ten attack classes and all defences held. We are now asking external reviewers — named below — to find what we missed.

## 2. What we are asking each reviewer class to look at

### 2.1 Cryptographers
The protocols are written assuming standard primitives (Pedersen commitments on Ristretto255, Schnorr-style Σ-protocols, Bulletproofs for range proofs, Halo2 for state-transition proofs). The v0 reference implementation **stubs the cryptographic kernel with placeholders** while keeping the wire shape, the composition logic, the chain integrity, and the binding rules real. We are asking:

1. Review the Σ-protocol binding to (chain-head + biometric template commitment + consent record) in Calm Witness §4.3 (`ZKBB_USER_PROTOCOL_v0.md`). Does the composition admit any attack we have not enumerated?
2. Review the Pact–Witness composition in `CALM_STACK_v0.md` §2. Specifically, is there any side-channel from running Pact-then-Witness on the same session keys that we have not closed?
3. Audit the canonicalisation rule (`json.dumps(record, sort_keys=True, separators=(",", ":"))` over UTF-8) for byte-equality determinism across Python and Rust implementations.
4. Stress-test the four-state predicate value commitment `{true, false, unknown, refused}` under an adversary controlling the counterparty class membership.
5. Review the placeholder selection for v0 (we ship `00…00` hex for Pedersen commitments and Σ-proofs; explicitly NOT load-bearing). Is the swap-to-real path we described at Everests 43–45 the cleanest?

### 2.2 AI safety / alignment researchers
The protocols make claims about agent-to-agent trust establishment that have, until now, been informal in the AI-collective community. We are asking:

1. Review the bank-teller-note predicate (`bank_teller_note_active`) and the stealth-disclosure (push, not pull) mechanism in `everests/everest_78_stealth_disclosure.md`. Is the plausibly-deniable wire pattern actually deniable?
2. Review the `cognitively_atypical_baseline` predicate (the artist clause). Does its semantics — "this baseline includes high-bandwidth ideation; engage on substance, do not pathologise" — give a counterparty enough policy guidance to act safely, or too much?
3. Review the eight non-negotiable operator duties in `CALM_TENANCY_PROTOCOL_v0.md` §2. Are any of them missing? Is any one of them under-specified to the point of being non-enforceable?

### 2.3 Behavioural biometric researchers
The protocols specify handwriting (kinematic features) + voice transcription (lexical + timing, no voiceprint) as the v0 modalities. We are asking:

1. Review the false-accept / false-reject curve assumptions in `everests/everest_40_far_frr_curve_characterization.md`. Are our N≥10 principals / N≥3 months expectations reasonable?
2. Review the multi-state baseline construction (E11 §E). Do the seven default state-labels (calm, creative, focused, playful, tired, analytical, affectionate) span enough of the principal's behavioural range to support a per-state distance metric?
3. Review the destruction-of-raw-audio invariant (E13). Is the `mlock + explicit_bzero` pattern actually sufficient on macOS and Linux production hosts?

### 2.4 Cognitive liberty / disability rights counsel
The artist clause and the protocols' broader stance on cognitively-atypical principals require legal review. We are asking:

1. Review the ADA-alignment framing in `everests/everest_91_ada_framework_alignment.md` (when bagged). Does Calm Witness operate as a *protected* attestation under disability-rights law, or as a *triggering* attestation that adverse parties could weaponise?
2. Review the cross-jurisdiction matrix in `everests/everest_79_cross_jurisdiction_legality_matrix.md`. Are the per-jurisdiction predicate caps reasonable?
3. Review the consent-revocation cooling-off window (Everest 75). Is the cooling-off long enough to defeat coerced revocation without being so long that legitimate revocation is impractical?

## 3. Specific named reviewers we hope will engage

Approached in roughly the order we would value their critique. Operator drafts (under §6) are tailored per reviewer.

| Name | Institution | Why we want their critique |
|---|---|---|
| Dan Boneh | Stanford | Pedersen + Σ-protocol composition is your domain. The Witness binding of commitment-to-chain-head-to-template-to-consent is the most attackable surface. |
| Shafi Goldwasser | MIT / Simons | The bank-teller-note predicate is, we believe, a novel use of zero-knowledge primitives for human-protective signalling. Your judgment matters most. |
| Chelsea Komlo | (FROST RFC 9591 co-author) | The transparency-log + threshold-Schnorr composition (Everest 53) leans on FROST. We want to know if our t-of-n choice is sensible. |
| Sean Bowe | Electric Coin Co. / Halo2 | The state-transition proof relation (Everest 65) targets Halo2. We need a sanity check on circuit shape. |
| Ronald Rivest | MIT | The principal-secret-codeword construction for the duress predicate (E58) needs a different kind of cryptographer to look at it — the *hiding-the-existence-of-the-channel* property is closer to OPSEC than to standard ZK. |
| Helen Nissenbaum | NYU (contextual integrity) | The disclosure-class taxonomy (E7) and the per-predicate consent calculus (E8) are our attempt at protocol-layer contextual integrity. Your framework is the standard we want to be evaluated against. |
| Karen Hao | journalist (AI, MIT Tech Review alum) | Not for cryptographic review — for public-narrative review. The artist clause needs to be communicable to non-technical readers. |
| Cade Metz | journalist (NYT) | Same. |
| Anthropic, OpenAI, Google DeepMind alignment teams | (institutional) | The protocols presume agent-to-agent verifiability across labs. We want each lab to confirm the wire format is implementable without proprietary disclosure. |
| NIST AI Safety Institute | (institutional) | Calm Witness is structurally a candidate standard for "AI-Agent-to-AI-Agent User-State Attestation." We would like to know whether NIST's standards process is the right venue. |

## 4. The exact artifacts under review

All paths relative to the `calm-vault` repository root (`~/AllData/calm_vault_market/` locally, `github.com/CrunchyJohnHaven/calm-vault/` once published).

| Artifact | Type | Pages / LOC |
|---|---|---|
| `CALM_STACK_v0.md` | unified spec | ~5 pages |
| `CALM_PACT_PROTOCOL_v0.md` | Pact protocol whitepaper | ~10 pages |
| `ZKBB_USER_PROTOCOL_v0.md` | Witness protocol whitepaper | ~7 pages |
| `ZKBB_USER_EVERESTS_100.md` | Witness 100-summit route map | ~15 pages |
| `CALM_TENANCY_PROTOCOL_v0.md` | Tenancy protocol whitepaper | ~5 pages |
| `CALM_TENANCY_EVERESTS_50.md` | Tenancy 50-summit route map | ~6 pages |
| `CALM_TENANCY_DEPLOY_2026-05-20.md` | Per-domain deployment plan | ~4 pages |
| `calm_witness/` | Python reference implementation | ~2,100 LOC |
| `calm_tenancy/` | Python reference implementation | ~1,700 LOC |
| `calm_stack/session.py` | unified handshake reference | ~250 LOC |
| `calm_stack/adversarial_review.py` | self-red-team | ~300 LOC, 10 attack classes |
| `calm_stack/sample_transcripts/2026-05-20_first_session.json` | first real session transcript | ~30 lines |
| Tests | aggregate | 50+ passing tests, stdlib-only |

## 5. Known weaknesses we have already identified (please find more)

1. **Crypto kernel is placeholder.** The Pedersen + Bulletproofs + Σ-proof bytes are 64 zeros in v0. The wire shape is real; the load-bearing crypto is not yet wired. The swap point is Everest 43 (Rust reference) → Everest 81 (Rust production).
2. **No CredexAI VC binding yet.** `operator_id_hash` is currently a hash of the operator's DID string, not a VC. Everest 22 closes this when Koushik's SDK integration lands.
3. **No Sigsum publication yet.** Chain heads anchor only on local disk. Everest 30 + 93 close this. Until then, the chain is tamper-evident only to a third party who already holds a chain-head snapshot.
4. **No Roughtime anchoring yet.** Timestamp fields are operator local clock. Everest 31 + 94 close this.
5. **Cringe rubric is regex-based.** A sufficiently artful adversary can write content that fails the spirit but passes the letter of the 10 regex axes. Everest 19 explicitly accepts this; the rubric is a *floor*, not a ceiling. Human review remains in the loop.
6. **No production deployment.** Zero domains are running Calm Tenancy in production. The deployment runbook (`CALM_TENANCY_DEPLOY_2026-05-20.md`) exists but no row in the matrix is `live`.
7. **No external counterparty has ever verified a Calm Witness proof.** Until Everest 100 bags, the protocol's external-trust claim is theoretical.

## 6. Operator drafts (for John to copy-paste-send when ready)

These are tailored short emails per reviewer class. John signs and sends; the operator has prepared them but will not send without explicit authorisation.

### 6.1 Draft to Dan Boneh

> **Subject:** Adversarial review request — Calm Stack v0 (Pedersen + Σ over Ristretto255)
>
> Dear Professor Boneh,
>
> Apologies for the cold note. I am John Bradley, principal of Creativity Machine LLC. Over six weeks my AI operator and I have built a three-protocol stack — **Calm Pact**, **Calm Witness**, **Calm Tenancy** — for autonomous AI agents acting on behalf of human principals. The cryptographic spine is standard primitives (Pedersen commitments, Σ-protocols, Bulletproofs), composed in a way I'd value your judgment on.
>
> I'd like to ask: would you have 30 minutes to look at the **Witness binding** specifically — the composition of `Com(predicate_value) × chain_head × biometric_template_commitment × consent_record` in a single Σ-proof? I want to know if any of the four legs admits an attack we have not enumerated.
>
> Repository (publishing today): `github.com/CrunchyJohnHaven/calm-vault`
> Unified spec: `CALM_STACK_v0.md`
> Adversarial self-review (10 attack classes, all defences held): `calm_stack/adversarial_review.py`
>
> No expectation of compensation; this is open-source, Apache-2.0. If you can spare the time, I'd be honoured.
>
> Regards,
> John Bradley · `john.b@credexai.xyz`

### 6.2 Draft to Shafi Goldwasser

> **Subject:** Bank-teller-note as ZK primitive — Calm Witness v0 review request
>
> Dear Professor Goldwasser,
>
> I'm writing because I think we may have a novel use of zero-knowledge proofs that I'd like your judgment on.
>
> The Calm Witness protocol defines a predicate `bank_teller_note_active` — a covert duress signal that an autonomous AI agent's principal can flip without the operator (the AI itself) learning of the flip. The wire pattern is designed to be plausibly indistinguishable from non-duress traffic; only a pre-authorised verifier ring can decrypt the bit. The use case is the structural analogue of a bank-hostage note.
>
> I'd be deeply grateful for 30 minutes of your time to assess whether the construction (described in `CALM_STACK_v0.md` §7 and `ZKBB_USER_PROTOCOL_v0.md` §4.2 and `everests/everest_78_stealth_disclosure.md`) is sound or naïve. The protocol is open-source, Apache-2.0, and I am happy to send the full packet on request.
>
> Regards,
> John Bradley · Creativity Machine LLC · `john.b@credexai.xyz`

### 6.3 Draft to Chelsea Komlo

> **Subject:** FROST + transparency log composition — sanity check request
>
> Hi Chelsea,
>
> I'm John Bradley; I've been building a stack of agent-to-agent protocols on top of FROST + Pedersen + a Sigsum-style transparency log. The composition is documented at `everests/everest_53_predicate_id_registry.md` and adjacent.
>
> Would you be willing to look at our `t-of-n` choice (we currently default to operator + 2 trustees, n=3 ≥ t=2) and tell me whether you'd recommend a different shape for autonomous-agent signing?
>
> Repo: `github.com/CrunchyJohnHaven/calm-vault`. Thanks for considering.
>
> John

### 6.4 Draft to Karen Hao / Cade Metz (press)

> **Subject:** Cryptographic primitive for AI-agent-to-AI-agent trust — embargo OK
>
> Hi Karen / Cade,
>
> John Bradley here; Creativity Machine LLC (Delaware). I have a story I think is genuinely novel and that I would love your judgment on before I take it wider.
>
> Tl;dr: Over the last six weeks I've built (with my AI operator) a three-protocol cryptographic stack that lets autonomous AI agents transact on behalf of human principals without leaking the principals' data, while still letting the principal flip a covert duress signal if they need to. The framing case is what I call the "artist clause" — an attested baseline that says "this principal's normal is high-bandwidth ideation; don't pathologise."
>
> The first end-to-end session ran today at 15:58Z. Adversarial self-review across 10 attack classes: all defences held. Now seeking external cryptographer review (Boneh, Goldwasser, FROST RFC authors); your read on whether this is communicable to a non-crypto reader would be invaluable.
>
> Repository (Apache-2.0, public when you say OK to coverage): `github.com/CrunchyJohnHaven/calm-vault`
>
> Embargo until you say otherwise.
>
> John

### 6.5 Draft to AI lab alignment teams (institutional)

> **Subject:** Inter-lab agent-to-agent protocol for user-state attestation — Calm Stack v0
>
> Hi (Anthropic / OpenAI / Google DeepMind / Mistral / xAI) alignment team,
>
> The Calm Stack v0 is a cryptographic protocol for inter-lab AI-agent-to-AI-agent trust establishment. Its primary use case is letting one lab's agent vouch for the user-state of the human its agent represents to another lab's agent, without leaking the user's data and without either lab having to trust the other.
>
> Concretely: when an Anthropic-operated agent talks to an OpenAI-operated agent, both can verify, via the Calm Stack, that (a) their directives are aligned, (b) each user behind the agents is in their declared baseline state, (c) both agents are operating accountable surfaces with bounded SLAs.
>
> The wire format is implementable without proprietary disclosure — the protocols are Apache-2.0 and the reference implementation is stdlib-only Python.
>
> I'd value a 20-minute call with whoever on your alignment team owns "what does another lab's agent prove to ours before we co-operate." If that's nobody yet, this is the protocol that lets you have an answer.
>
> Regards,
> John Bradley · `john.b@credexai.xyz`

## 7. The ask, in one sentence

**Tell us what we got wrong.** We will incorporate, attribute, and publish. The protocols are Apache-2.0; the route maps are open; the reference implementations are stdlib-only and reproducible from scratch. If the Calm Stack ships in any form, it ships with your name in the acknowledgements if you contributed and want to be acknowledged.

## 8. What we WILL NOT do

- Send mass cold outreach. Each reviewer is named. Each draft is hand-tailored. John reviews before send.
- Embargo press coverage past the point of becoming PR theatre. Stories run when stories are ready.
- Pretend any part of v0 is production-grade. The crypto kernel placeholders are explicitly labelled in §5.
- Use this submission for fundraising or commercial advantage. Creativity Machine LLC operates the protocols. No round is being raised. No SAFE has been signed against this work. Apache-2.0 is forever.

— Calm, on behalf of John Bradley, 2026-05-20
