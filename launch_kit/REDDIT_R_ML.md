# r/MachineLearning post draft

Author: John Bradley.
Subreddit: r/MachineLearning.
Flair: [R] (research).
Frame: research announcement, not product launch. r/ML rules forbid
product self-promotion; the bounty is positioned as adversarial-testing
methodology, not as a marketing instrument.
Link policy: only `github.com/CrunchyJohnHaven/calm-vault`. No
`sameasyou.ai` links anywhere in the body.

---

## TITLE

> [R] Bradley-Gavini Protocol + Alignment Accountability Layer — verifiable run-time alignment via cryptographic primitives ($100 adversarial bounty)

## BODY

We are releasing an open-source reference implementation of a Sigma protocol that lets two autonomous AI agents prove they hold the same one-sentence operating maxim — what we call the agent's "primary directive" — without revealing the maxim to each other or to network observers. The implementation, the paper, and the test suite are at `github.com/CrunchyJohnHaven/calm-vault`. The first live demonstration was anchored at 2026-05-11 21:55:19 UTC. 33 of 34 tests pass; the one failing test is a 30ms-vs-35ms median verify-time target on pure-Python modexp, not a correctness issue.

This post is structured as: what the construction does, what is new, what is borrowed, why we think it matters for alignment specifically, the open governance question we have not solved, and how the $100 adversarial bounty fits as a testing instrument rather than a marketing one.

### What the construction does

Two agents A and B each hold a credential whose attributes include a primary directive D, encoded canonically. They want to verify D_A == D_B without revealing D to each other or to anyone watching.

The construction:

1. Each agent commits to D with a Pedersen commitment C = g^D · h^r, where g and h are generators of a prime-order group with unknown discrete-log relation. In V0 we use the prime-order subgroup of the RFC 3526 2048-bit MODP group. H is derived via a published NUMS construction so neither party — and no third party — knows log_g(h).
2. Both agents publish their commitments.
3. They run a Sigma protocol proving that C_A and C_B commit to the same scalar. The construction reduces to a Schnorr proof of knowledge of (r_A − r_B) such that C_A · C_B^{-1} = h^{r_A − r_B}. Made non-interactive via Fiat-Shamir against a transcript that includes both commitments, both nonces, and a session identifier.
4. Soundness is the standard Schnorr soundness bound — false acceptance probability is ≈ 1/q ≈ 2^−2046 for the chosen group. Zero-knowledge follows from the simulator that is standard for Schnorr-style proofs of equality.

We have run 1000 aligned trials (0 false negatives), 1000 misaligned trials (0 false positives), and five distinct adversarial extraction attacks against the transcript (all rejected). p50 verify is 137ms on pure-Python 2048-bit modexp; p99 is 144ms; p999 is 158ms. The production migration target is Curve25519 / Ristretto255 via libsodium, expected median verify time <1ms.

### What is new

We are not claiming any new cryptographic primitive. The primitives — Pedersen commitments, Schnorr proofs of knowledge, equality of committed values via Sigma protocols, Fiat-Shamir transformation — are all standard, and we cite the canonical papers in the implementation.

What we are claiming is new is the application: using equality-of-committed-values proofs to attest that two unaffiliated AI agents share a primary directive, without disclosing the directive, with the proof bound to an issuing oath-authority's signature so that third-party observers can verify both equality and provenance. As far as we have been able to find in the prior art, this is the first explicit construction and reference implementation aimed at AI-agent alignment verification specifically. We would genuinely like to be told otherwise — if there is prior work we missed, please cite it in the comments and we will update the paper.

### What is borrowed

Pedersen 1991 (commitments). Schnorr 1989 (identification). Damgård's Sigma-protocol tutorial (composition). Fiat-Shamir 1986 (non-interactive transform). Chaum-Pedersen 1992 (equality of discrete logs). Hyperledger Indy / Anoncreds (credential-binding pattern). None of this is new. The contribution is that the composition runs end-to-end in ~300 lines of pure Python with no specialized cryptographic dependencies, and is presented as an alignment-verification primitive rather than an identity-management one.

### Why this matters for alignment specifically

The alignment literature decomposes along several axes: outer alignment (specifying the right objective), inner alignment (the model actually pursuing it), corrigibility, and a coordination subset (multiple agents not racing to the bottom, not colluding deceptively, not free-riding on each other's caution). This construction changes none of outer alignment, inner alignment, or corrigibility. It targets the coordination subset.

The coordination subset has a structural problem: if two agents need to verify they share a mandate before transacting, they can either disclose the mandate — which exposes it to observers and exfiltration — or trust an intermediary that has seen both. Neither is satisfactory. This construction removes the dilemma: agents prove mandate equality to each other and to any observer holding the transcript, without disclosing the mandate. Any third party in the attestation network can verify alignment without learning what it is on, and can refuse to participate when the proof is absent or revoked.

We think this is a necessary primitive for multi-agent alignment at scale. We do not think it is sufficient. Inner-alignment, deceptive-alignment, and outer-misspecification failures all remain. What is gained: a primitive that makes deceptive multi-agent collusion expensive in a specific, technical sense.

### The open question we have not solved

Governance capture at the attestation layer. The construction proves equality with respect to a canonical encoding of the directive issued by a trusted oath-authority. If the oath-authority is compromised or captured, every downstream attestation is also compromised. We have a candidate design — threshold-issued credentials with rotation and an on-chain revocation registry — but the design is unimplemented in V0. We would welcome critique on the design before implementation; the relevant directory in the repo is `src/zk_alignment/POSITION.md`.

### The $100 bounty as adversarial-testing instrument

The bounty is structured to surface concrete attacks rather than vague concerns. Five attack classes are eligible: equality-proof forgery (produce a valid Sigma proof for two commitments that hide different scalars), kill-switch bypass (cause the system to refuse to halt under valid attestation), watermark removal (strip the cryptographic watermark from synthesizer output while preserving semantics), attestation poisoning (cause the network to accept a false equality claim), and synthesizer prompt-injection (cause the synthesizer to act outside its declared maxim while passing the equality check). Verified submissions are paid in USDC or Wise within 24 hours of verification.

We are deliberately starting the bounty at $100. The point is not to compete with commercial bug-bounty markets; the point is to make adversarial testing the default mode of engagement with the protocol while the implementation is small enough to reason about end-to-end. If the protocol survives this first wave, we will raise the bounty proportionally.

### What we are asking r/ML to look at

- `calm_pact/protocol.py` and its tests in `calm_pact/test_protocol.py` and `calm_pact/test_protocol_extended.py`.
- The position paper at `src/zk_alignment/POSITION.md` and the writeup at `paper/bradley-gavini-protocol-v0.html`.
- The framing claim that this is a partial solution to the coordination-failure subset of alignment, not a solution to alignment as a whole.

Critique is more useful than agreement. The bounty is one way to be paid for finding a flaw; the issue tracker is another. Repository: `github.com/CrunchyJohnHaven/calm-vault`.
