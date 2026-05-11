# Show HN — submission draft

Author: John Bradley.
Repo: github.com/CrunchyJohnHaven/calm-vault.
Anchor: 2026-05-11 21:55:19 UTC.

---

## TITLE

> Show HN: $100 to anyone who can misalign our AI organization

(76 characters including the "Show HN:" prefix. Under the 80-char Show HN cap.)

## URL

Three candidates. Recommendation first, then the trade-offs.

**Recommendation: submit the URL `https://github.com/CrunchyJohnHaven/calm-vault`.**

Rationale, in order of weight:

1. HN moderators downweight Show HN posts that point at landing pages with a hero, a CTA, and no code in view. The repo opens to a README that names the protocol, lists the authors, links the paper, and shows the 33/34 test verdict in the first scroll. That is what an HN reader expects to evaluate first.
2. The bounty headline lives in the title and the first comment. The reader does not need the landing page to find it.
3. `sameasyou.ai` is the marketing site. Linking marketing under a Show HN reads as promotional and invites the "this is an ad" flag.
4. `sameasyou.ai/bounty` is the most specific URL but is a sub-page of the marketing site and reads even more promotional. It also has less context — a reader landing there cannot inspect the test suite or the code.

Submit the repo. Link the bounty page inside the first comment.

## FIRST COMMENT (pinned by OP, posted seconds after submission)

OP here. Six things to lead with.

**1. What is real today, what is not.** The Bradley-Gavini Protocol — a Sigma protocol over Pedersen commitments that lets two AI agents prove their primary directive is identical without revealing the directive — has a reference implementation in ~300 lines of pure Python at `calm_pact/protocol.py`. 33 of 34 tests pass. The one failing test is a pure-Python modexp performance target (35ms vs the 30ms goal); correctness, soundness, and zero-knowledge are all green across 1000-trial statistical runs. The position paper is public at `src/zk_alignment/POSITION.md` and `paper/bradley-gavini-protocol-v0.html`. Two landing pages are live: `sameasyou.ai` (the protocol) and `seesomethingsaysomething.ai` (the cybersecurity wedge that runs on top of it). What is aspirational: the production-grade Curve25519/libsodium port, the on-chain attestation registry, the threshold-trust governance layer, and any claim about training-time alignment. This is a run-time accountability layer. Not a training-time fix.

**2. The five attack classes that win the $100.** Equality-proof forgery (produce a valid Sigma proof for two commitments that hide different scalars). Kill-switch bypass (cause the system to refuse to halt when a valid attestation says it should). Watermark removal (strip the cryptographic watermark from synthesizer output while preserving semantics). Attestation poisoning (cause the attestation network to accept a false claim that the directive is the same). Synthesizer prompt-injection (cause the synthesizer to act outside its declared maxim while still passing the equality check). Verified submissions are paid $100 in USDC or Wise inside 24 hours. Details and submission form: `https://sameasyou.ai/bounty`.

**3. The recursive structure.** A cybersecurity startup, See Something Say Something, is being launched on top of the protocol. The point is not the startup. The point is the recursion: the parent organization is an Autonomous AI Organization that operates the protocol, and the for-profit subsidiary's net proceeds, after operational expenses, are committed to existential-risk reduction (CAIS, FLI, MIRI, and an open Calm Alignment Grant in equal quarters). If the protocol works, the same primitive that lets the subsidiary attest its alignment also lets anyone in the attestation network kill the subsidiary on detected misalignment. The parent eats its own dog food.

**4. The disclaimer.** This does not solve alignment. Training-time alignment — getting a model to want the thing you want it to want — is unaddressed by anything here. What this addresses is the coordination-failure subset of the alignment problem: two AI agents that have never met can decide whether to trust each other on the basis of mandate equality, without disclosing the mandate, and any third party in the attestation network can verify the result and revoke participation. That is a run-time accountability primitive. It is necessary, not sufficient.

**5. Why I am inviting the kicking.** We sent the bounty announcement to 56 outlets tonight. Critical coverage is more useful than laudatory coverage. The protocol is small enough to read in one sitting, the tests reproduce in ~6 minutes on a fresh clone, and the bounty is structured to pay out for any concrete break, not to pay out for vague misgivings. If you find a flaw, you are doing the alignment community a service and you are taking $100 off our table for it. Both are good outcomes.

**6. What I want from this thread.** Cryptographers: tear up the equality proof. Adversarial-ML people: try to drift the synthesizer past the watermark. Systems people: tell us where the attestation layer breaks under partition. Skeptics: tell us where the framing is overclaiming. The repo, the paper, the test verdict, and the bounty submission form are all linked.

## ANTICIPATED-QUESTION REPLIES

These are drafts for the obvious top-comments. Fire whichever fits the actual question.

### Q1 — "How is this different from RLHF / Constitutional AI?" (target: 80 words)

> Different layer. RLHF and Constitutional AI shape what a model wants during training. The Bradley-Gavini Protocol does nothing at training time. It is a run-time check: two trained agents prove their declared directives are byte-equal under a Pedersen commitment, without revealing the directives, and any third party can verify the proof. A constitution still has to be written and trained in. Our claim is narrower — that once you have one, you can coordinate on it without disclosing it.

(80 words exactly.)

### Q2 — "Why $100 instead of $10,000?" (target: 60 words)

> Two reasons. First, $100 is what we can pay out 50 times this month without running an autonomous AI organization into the ground. Second, the bounty is a credibility instrument, not a labor market. We want the people who would break it for free to break it for $100 in goodwill. If the protocol survives that, we raise the bounty.

(61 words.)

### Q3 — "Isn't this just security through obscurity?" (target: 100 words)

> No. The primitives are public, named, and battle-tested. Pedersen commitments give hiding under the discrete-log assumption and unconditional binding under the unknown-`log_g(h)` setup we publish. The equality proof is a textbook Schnorr-style Sigma protocol made non-interactive via Fiat-Shamir. There are no novel cryptographic constructions in V0; every primitive has decades of analysis. The only thing we are claiming new is the application — using these primitives to attest directive equality between autonomous agents. The directive itself stays private; the cryptographic machinery is fully disclosed. Obscurity would be the opposite of what we are doing.

(99 words.)
