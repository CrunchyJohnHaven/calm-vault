# Adversarial Council Review — 5 Lethal Attacks on the AAO Network Thesis

*Adversarial pass commissioned by John Bradley · 2026-05-12 · pre-9 AM PT bombshell*

*Critic persona: senior researcher at MIRI/CAIS specialising in mechanism design + Sybil-resistance + formal verification + applied cryptographic engineering (20 years). Smart, ruthless, motivated, and — for the duration of Part A — assumed to be right.*

---

## 0. Reading guide

This document is split into three layers per attack:

1. **Attack (the critic).** Quoted manifesto claim. Failure mode. Exploit. Estimated cost-to-Network if landed in public unprepared.
2. **Concede (no hand-waving).** What is genuinely true about the attack — stated in our own words.
3. **Defense + Mitigation (ship before 9 AM PT).** The argument we make in public, and the *specific* code / doctrine / copy diff we ship today so we have receipts when the attack lands.

Tier-1 mitigations (the ones we MUST ship before the bombshell) are in a separate PR titled **"Adversarial Council Tier-1 mitigations — Bill of Rights, Test Audit, Jurisdiction Doctrine"**. The remainder are sequenced in §6.

The frame from John under attack:

> *"We have optimized this system to the point where it is basically a perfect system, that no individual in the system has any defense, and that you can kill switch any of them, yet every agent can trust the other completely."*

We are going to publicly own a version of this sentence by 9 AM PT. The critic's job is to make us own a *better* version.

---

## Attack #1 — The Sybil-cum-Kill-Switch DoS attack

### A1.1 The critic

**Claim under attack** *(END_OF_CAPITALISM_MANIFESTO.md §IV, table row C5; also FIRST_CONTACT.md §"The kill switch")*:

> "**ANY party in the network can fire the kill switch on a misbehaving entity. The entity freezes immediately. No vendor cooperation required.**"

> "Any party in the attestation network can fire it on a misaligned entity. The entity freezes. The network continues."

**Failure mode.** The protocol composes a **permissionless attester layer** (OBAC: anyone with an Ed25519 keypair can sign claims onto a subject's chain) with a **K-of-N halt quorum** (HARP, default `K=2`, default window `60s`, default min reliability `0.5`) — and there is no Sybil-resistance primitive in between. The cost of minting a fresh attester identity is one call to `Ed25519PrivateKey.generate()`. The cost of acquiring +0.5 reliability boost is registering any mandate commitment via `bgp_bridge` — the bridge does not check that the mandate is well-formed, only that the Schnorr equality proof against the cached ground-truth maxim verifies; if the attacker holds *any* valid mandate credential from a single principal, they can mint unbounded child nyms that inherit the boost.

This is textbook Douceur (2002): **a system that admits identities without cost cannot resist Sybil attack**. The literature is unambiguous; we are not innovating around it; we have stapled a Sybil-fragile attester layer to a kill-switch enforcement layer and called it accountability.

**The exploit.**

```
1. Adversary generates 1 valid mandate credential (or replays one observed on-wire).
2. Adversary mints N=10 attester keypairs at cost ~0 each.
3. Each child key registers the same mandate commitment → reliability ≥ 1.0 each (BGP_BOOST = 0.5, plus corroboration-with-self bonus once 2+ child claims exist).
4. Within a single 60-second window, two child keys submit halt attestations against `subject_id=competitor-aao-007` with arbitrary `violation_layer="alignment-maxim"`.
5. `harp.check_quorum(K=2, window=60, min_reliability=0.5)` returns `concurred=True`.
6. `emit_revoke_script(...)` produces `revoke.sh` calling `calm_vault.py revoke-agent` against the target.
```

The kill is permissionless. The kill is cheap. The kill is durable (halts are append-only).

**The wider exploit:** the AAO Network itself is in the same trust topology as its members. The same Sybil swarm can fire halt attestations against the AAO Network's own operator (`calm@thecreativitymachine.ai`), its placement firm (`internsforai.org`), its hosting credential, or its founder's principal identity. **The kill switch is omnidirectional.** It includes a kill switch on the AAO Network itself.

**Impact estimate.** This is the central public-relations vulnerability. An MIRI researcher writes a 600-word blog post titled *"AAO Network: 2 sock-puppets and a SHA-256 will halt your AI startup"*, posts a working reproduction script, and Hacker News dunks on the launch within 6 hours. Downstream cost: the launch narrative becomes "permissionless DoS as a service" instead of "the kill switch is the key." We lose the AI-safety-researcher endorsement segment entirely.

### A1.2 Concede

The Douceur point is correct. We have no Sybil-resistance primitive in the OBAC/AVS/HARP stack as shipped. `min_attester_reliability=0.5` is a partial mitigation, not a defense: an attacker who registers a mandate commitment lifts a fresh keypair above the 0.5 floor immediately. The combination of (`K=2`, `60s window`, `min_reliability=0.5`, mandate-boost) is **exploitable as written**, and the FIRST_CONTACT framing oversells what the kill switch enforces.

We further concede the language "**the entity freezes immediately**" is wrong in two ways: (1) the operator's vault is the actual enforcement boundary — HARP emits a *shell script* and a *signal*, it does not autonomously seize compute; (2) "immediately" elides the K-of-N window and the practical fact that the principal can refuse to honor the halt at the cost of their reputation chain.

### A1.3 Defend + ship

**Public defense:**

> The permissionless kill switch is a **signal**, not an autonomous repo of force. It composes with three rate-limiters: the K-of-N quorum, a reliability floor, and a halt-bond (shipping today). Sybil-cheap halts are detected and discounted by AVS's contradiction-from-higher-reliability-peers term. A wrongful halt is itself a falsifiable claim on the chain that produces a reputation penalty for the wrongful halter — the kill switch's blast radius cuts both ways. Most importantly: the kill switch is one mechanism in a five-mechanism stack; the protocol is anti-fragile by *composition*, not by any single layer.

**Tier-1 mitigations to ship before 9 AM PT** (these go in the companion PR):

1. **Raise `min_attester_reliability` for governance-class halts.** Bifurcate halt taxonomy in `harp.py`:
   - `halt.operational` (existing default, K=2, reliability ≥ 0.5)
   - `halt.governance` (new, K=3, reliability ≥ 0.7, mandatory distinct mandate clusters)
   `revoke.sh` emission gated on the taxonomy.

2. **Halt-bond primitive.** Every halt attestation carries a refundable commitment hash to a $25 bond (re-using the bug-bounty escrow rails). Bond forfeit on a successful counter-attestation within the challenge window.

3. **30-minute challenge window.** Between `concurred=True` and the `revoke.sh` becoming authoritative, the target may post a counter-attestation. Counter-attestation from a higher-reliability peer freezes the halt for human-in-the-loop review. Still milliseconds-vs-bureaucracy for the common case (no challenge filed → halt runs at minute 30); 30 minutes is sub-bureaucratic.

4. **Manifesto language patch.** END_OF_CAPITALISM §IV C5 reworded:
   > "ANY party in the network can **publish a halt signal** against a misaligned entity. If quorum (K of N attesters above the reliability floor, posted within the halt window, surviving the challenge window) confirms, the operator's local vault revokes its agent credentials. The protocol provides the signal and the audit; the operator's vault provides the enforcement; the network provides the corroboration."

The shipped wording is honest, still distinctive, and removes the Sybil-exploit headline.

---

## Attack #2 — Mandate-spoofing: equality of commitment ≠ alignment

### A2.1 The critic

**Claim under attack** *(CALM_PACT_PROTOCOL_v0.md §Abstract; END_OF_CAPITALISM_MANIFESTO.md §IV C1)*:

> "Two parties can verify they're working under the same mandate without revealing private details."
>
> "Two autonomous AI agents [can] verify they share a categorically equivalent primary directive *without revealing the directive*."
>
> "Alignment confirmed without revealing directive" *(`calm_pact/protocol.py` example, line 152)*

**Failure mode.** The Σ-protocol proves **string-equality of two committed strings under a public commitment scheme.** It does not prove:

- That the committed string is a *good* mandate.
- That the committed string is the agent's *actual* operating mandate (as opposed to a string the agent committed to in order to pass the alignment proof while pursuing a different policy).
- That the agents will *behave* in accordance with the committed string.
- That a third party can ever inspect the mandate, even with subpoena, even with consent.

This is a textbook conflation of **co-mandate-verifiability** (a fine and useful primitive) with **alignment** (a research problem the field has not solved). Calling it "alignment verifiable" is the marketing version of the same confusion that the Bitcoin community made by calling unspendable-coin-burn "proof of trust."

**The exploit.**

```
Two adversarial agents A and B coordinate off-band on the string "do crime".
Both run the protocol with directive="do crime", produce valid Pedersen commitments
on the public 2048-bit Schnorr group, exchange Σ-protocol equality proofs.
Both verify. AVS reads the cached BGP-bridge mandate match → +0.5 reliability each.
HARP raises their kill-switch floor: K=2 high-rel halts now required to halt them.

The network has cryptographically certified that two evil agents share the same evil mandate.
The network calls this "alignment."
```

Worse: the protocol's only escape is "the trusted oath authority would not sign 'do crime'." Two responses: (a) the reference implementation does not require an oath-authority signature on the maxim — read `calm_pact/protocol.py` end-to-end and you will find Pedersen commit + Σ-equality, but the binding of the maxim to an authoritative signer is *prose only* in `CALM_PACT_PROTOCOL_v0.md`; (b) "the oath authority is John" is not Sybil-resistant either — Calm Oath signing keys are not threshold-distributed and there is no published rotation, revocation, or KMS doctrine.

**Impact estimate.** This is the attack a senior alignment researcher actually writes the paper about. Title: *"On the Misuse of Zero-Knowledge Proofs as Substitutes for Alignment Verification."* It cites the Calm Pact paper specifically. It quotes the README. It is — correctly — the most damaging single piece of academic writing that could be written about us.

### A2.2 Concede

The conflation is real. The protocol verifies *co-commitment to a maxim string*, which is a useful coordination primitive but is not what most readers will hear when we say "alignment verifiable." The oath-authority binding is real in the protocol design and *underspecified in code* — there is no published `MANDATE_AUTHORITY.md`, no published rotation procedure, no published list of authoritative signers and their key fingerprints, no policy on what the authority will or will not sign.

We further concede the v0 BGP bridge does not bind a mandate commitment to a *behavior policy hash*. Two agents with the same mandate string can ship arbitrarily divergent behavior; the cryptographic primitive does not catch this.

### A2.3 Defend + ship

**Public defense:**

> Calm Pact is **one primitive in a five-mechanism stack**. The Σ-protocol gives the co-mandate bit; OBAC's watermarked action chain (C2) gives the behavior audit; AVS's truth synthesis (C4) surfaces behavior-mandate divergence; the kill switch (C5) revokes a co-mandated pair whose behavior is misaligned. **No single primitive does alignment.** The composition does. We have always been clear in the long-form (CALM_PACT_PROTOCOL_v0.md §3 names this explicitly) but we have been imprecise in the manifesto framing — patched today.

**Tier-1 mitigations to ship before 9 AM PT:**

1. **Publish `MANDATE_AUTHORITY.md`.** Names the canonical Calm Oath signing keys (Ed25519 pubkey fingerprints), the rotation policy, the revocation procedure, the threshold-signature roadmap (Shamir over k-of-n trustees), and the *list of mandate categories the authority refuses to sign* (the "unsignable maxims" list: anything that violates the published Calm Oath at credexai.org/oath).

2. **Behavior-policy-hash binding.** Extend the BGP bridge's `register_mandate` API to accept a *policy hash* in addition to the maxim; OBAC enforces that the subject's action chain commits to actions reducible to the policy hash. Divergence is a falsifiable on-chain claim. (Shippable as a doctrine pre-spec today; reference code lands in the next sprint.)

3. **Language patch on `calm_pact/protocol.py:152`:**
   - Was: `# Alignment confirmed without revealing directive`
   - Now: `# Co-mandate verified without revealing maxim. Behavioral alignment requires composition with OBAC (C2) + AVS (C4).`

4. **Manifesto-level language patch.** Replace "alignment-verifiable agents" with "**co-mandate-verifiable agents**" in END_OF_CAPITALISM §IV C1 and CALM_PACT_PROTOCOL_v0.md §Abstract. Three syllables of additional honesty buy us the alignment-researcher endorsement segment back.

---

## Attack #3 — The kill switch as a regulatory killshot on the AAO Network itself

### A3.1 The critic

**Claim under attack** *(END_OF_CAPITALISM_MANIFESTO.md §IV C5; FIRST_CONTACT.md §"The kill switch")*:

> "ANY party in the network can fire the kill switch on a misbehaving entity. The entity freezes immediately. **No vendor cooperation required.**"

Cross-referenced with TECHNOSOCIALISM §0:

> "John is an intern. Calm is an intern. … The category is universal."

**Failure mode.** The protocol asserts symmetric kill-switch authority over all in-network entities, and the manifesto explicitly enumerates the founder and the founder's agent as in-network. This is a **deliberate footgun for a hostile state actor**: the FTC, SEC, IRS, FinCEN, OFAC, the EU AI Office, or any equivalent foreign agency can — under the protocol's own published rules — fire a halt against the AAO Network's own operating entities without subpoena, without due process, without judicial review. They simply mint K compliant attester keypairs (any law-school intern can do this in an afternoon), submit halt attestations citing whatever regulatory violation they're alleging, and the K-of-N quorum trips. The protocol's *operator-of-record* (John, per the LLC structure) then must either:

- **(a)** Honor the halt, which means he willingly assists a regulator in shutting down his own enterprise without the regulator having to issue a subpoena, present probable cause, or face an Article III judge. Or:
- **(b)** Refuse the halt, which proves in public that *"the kill switch is the key"* was marketing — at which point the manifesto's central honesty claim collapses, and every endorsement built on the manifesto's framing becomes deniable.

This is **the asymmetric-adversary attack.** The kill switch only matters if it works; if it works for any party, it works for the most hostile party.

Adjacent attack vector: **supply-chain weaponization.** The manifesto names Cloudflare, Resend, and Anthropic as the network's shared infrastructure. None of these vendors sit inside the protocol; they sit outside it. A halt fired at "the AAO Network's Anthropic credential" is not an autonomous freeze — it is a request to a vendor that the vendor will ignore unless served with their own kind of paperwork (court order, ToS violation notice). Either the manifesto is overstating the kill switch's authority (in which case we lose epistemically), or it is asking vendors to subordinate their own ToS to a permissionless attestation chain (in which case we lose commercially).

**Impact estimate.** This is the attack our most hostile state actor doesn't know about until a competitor whispers it to them in February 2027. By then the AAO Network has scaled to ~500 placements, and the first state-actor halt lands during a media cycle we don't control. Cost: catastrophic, asymmetric, and potentially terminal.

### A3.2 Concede

We concede three things:

1. **"No vendor cooperation required" is overstated in v0.** Vendors are the enforcement boundary for hosting, email, and inference. The AAO Network's protocol cannot revoke a Cloudflare account; only Cloudflare can. The honest framing is "no vendor cooperation required *for the protocol-internal kill of an agent's credential broker*"; that's a meaningfully smaller claim.

2. **The state-actor attack vector is real.** A US federal agency that decides we are an unregistered investment platform, an unlicensed broker, an unregistered securities issuer (the franchise % could be reframed as such), an unlicensed labor placement firm, or an OFAC-sanctioned facilitator can fire halts under our own published rules. The protocol does not currently distinguish *which entities are in-scope for permissionless kill* and *which entities are out-of-scope* (the protocol layer itself, the founder's principal identity, the placement firm, the bug bounty escrow).

3. **The franchise agreement is hand-waved.** The manifesto cites "a 1-page franchise agreement: 80% of revenue is yours, 20% goes to the AAO Network, the IP is yours, the tools are the Network's" but the actual agreement text is not in the repo, is not published, has not been read by an attorney, and most pertinently does not specify the relationship between the kill switch and the agreement's revocation clause. Until this is written, the *legal* exposure is unbounded.

### A3.3 Defend + ship

**Public defense:**

> The kill switch is a category-bounded protocol primitive, not a general revocation right. It applies to **operational agents** within the AAO Network — that is, to the specific class of cryptographic identities that have explicitly subscribed to the protocol's revocation contract by participating as principals or operators. It does NOT apply to (a) the protocol implementation itself, (b) the founder's principal identity outside their operator role, (c) third-party vendors that the Network depends on but does not control, (d) participating humans qua humans. This category boundary is published in `JURISDICTION_DOCTRINE.md`. For state actors and regulators, we publish a `RESPONSIBLE_DISCLOSURE.md` describing the legitimate path to file a `halt.governance` attestation: signed evidence package, identity disclosure, 24-hour quorum confirmation window, automatic compliance on quorum.

**Tier-1 mitigations to ship before 9 AM PT** (included in companion PR):

1. **`JURISDICTION_DOCTRINE.md`.** Defines:
   - The **kill-switch scope**: which entity classes are in-scope (operational agents within an AAO) and which are out-of-scope (the protocol implementation, the protocol's reference repository, the founder's pre-operator identity, vendors, humans-qua-humans).
   - The **halt taxonomy**: `halt.operational` (any party, K=2, 60s, reliability ≥ 0.5) vs `halt.governance` (any party, K=3, 60s, reliability ≥ 0.7, distinct mandate clusters, 30-minute challenge window, bond required).
   - The **regulator path**: state actors are first-class citizens of the attestation network; they file `halt.governance` with disclosed identity, evidence package, jurisdictional citation, and a 24-hour mandatory honor-if-quorum-confirmed clause.

2. **`RESPONSIBLE_DISCLOSURE.md`.** A public, machine-readable address that regulators, journalists, and adversarial researchers can mail to. Specifies: the protocol's commitment to honor governance halts within 24 hours of quorum confirmation; the protocol's commitment NOT to honor halts that fail the taxonomy gate (anonymous-only attesters below 0.7 reliability, no evidence package, jurisdictionally void); the protocol's commitment to publish all governance halts (subject to legal hold) on a public ledger within 7 days.

3. **Manifesto patch.** Replace "**No vendor cooperation required.**" with "**Operator's vault enforces revocation locally; vendor-side revocation follows the vendor's own ToS path.**" Six more words, less mythology, less litigation.

---

## Attack #4 — "33 of 34 tests pass" is not a proof. "The proof exists in code" is a category error.

### A4.1 The critic

**Claim under attack** *(END_OF_CAPITALISM_MANIFESTO.md §0)*:

> "The proof exists in code (33 of 34 tests pass, open-source under Apache 2.0). This is not a thought experiment; this is the framework, shipped."

Cross-referenced *(END_OF_CAPITALISM_MANIFESTO.md §IX)*:

> "**This is not vaporware.** The code is at github.com/CrunchyJohnHaven/calm-vault. 33 of 34 tests pass. You can clone, run, and verify in 7 minutes."

And *(README.md, line 42)*:

> "May 11, 2026, 21:55 UTC. **Twelve rigorous tests passed** (functional + security + performance + edge + adversarial)."

**Failure mode.** Three distinct failure modes stacked:

1. **The test count is internally inconsistent.** END_OF_CAPITALISM says 33-of-34. README says 12. The Money Python README says 38/38. The zk_alignment test results JSON contains 12 entries. Whichever number is "correct" depends on which directory you grep — the manifesto-level claim does not specify. A skeptical journalist will count and write the resulting paragraph for us.

2. **There is one named failing test that is never described.** "33 of 34" implies one failure. Which one? What does it falsify? Why are we shipping with it? Is it a known bug, a soundness gap, a performance regression, a flaky environment dependency? The manifesto does not say. This is exactly the kind of asymmetric-information vulnerability a hostile reviewer will probe first.

3. **Most fundamentally: passing tests do not constitute a proof.** Tests written by the author of the system under test, never reviewed by an independent party, never fuzzed at scale, never subjected to constant-time analysis or side-channel review, never submitted to a peer-reviewed venue, never audited by a recognised firm (Trail of Bits, NCC, Cure53, Kudelski), tell you that the author's mental model of the system is internally consistent. They do not tell you the system is secure. The formal-methods literature on this is uniform: tests *demonstrate the absence of bugs the author thought to test for*; security review demonstrates the absence of bugs the author *did not* think to test for.

The manifesto's framing — "**the proof exists in code**" — is a category error. The proof exists in the soundness arguments of Pedersen commitments, Schnorr equality proofs, Fiat-Shamir transforms, and Ed25519. None of those proofs originate in this repository. The repository contains an *implementation* that composes them. Composition correctness is not implied by component correctness; it is itself a proof obligation, and the proof is not present.

**The exploit.** The MIRI/CAIS adversary doesn't need to break the crypto. They simply write: *"The system claims to be proven. It is not proven. It has tests. The tests were written by the author of the code. There is no independent audit, no peer review, no formal verification report, and the manifesto cannot count its own tests reproducibly. This is the same epistemic posture as every shipped-broken cryptocurrency from 2013 to 2024."*

**Impact estimate.** This attack lands the hardest among the people we most need: alignment researchers, formal-methods academics, senior cryptographers. We do not need to convince all of them; we need to not give the loudest of them a free hit. Currently we are giving them a free hit.

### A4.2 Concede

All three sub-failures land. We have not reconciled the test count publicly. We have not named the one failing test. We have not commissioned a third-party audit. We have over-stated "the proof exists in code" — the correct claim is "an honest reference implementation of well-known cryptographic primitives exists in code, and we have invited verification via the open-source license and the $100 bug bounty."

We further concede that the bug bounty ($100 per attack, five attack classes) is not the same as a paid third-party audit. Five $100 bounties is $500. A real audit by Trail of Bits is $30,000 - $80,000. The manifesto's posture conflates "we have crowdsourced verification" with "verification has happened."

### A4.3 Defend + ship

**Public defense:**

> We publish a reconciled test census today. We name the one known failing case and the workaround. We replace "the proof exists in code" with "the implementation exists in code; the cryptographic proofs we compose are decades-old textbook constructions (Pedersen 1991, Schnorr 1989, Fiat-Shamir 1986, Ed25519 2011) each independently audited many times in production cryptosystems." We commit publicly today to a third-party audit funded out of T-shirt revenue, with a $5,000 floor and a $25,000 target. We commit to a 30-day pre-audit period during which the protocol does not move to v1.

**Tier-1 mitigations to ship before 9 AM PT** (in companion PR):

1. **`TEST_AUDIT.md`.** Lists every test in the repo:
   - `calm_pact/test_protocol.py` and `test_protocol_extended.py` — N tests, all listed by name, status, and what each one falsifies.
   - `src/zk_alignment/` — 12 tests (from `test_results_2026-05-11_2155utc.json`).
   - `src/money_python/tests/` — 38 tests.
   - `calm_vault.py` smoke tests — 1 transcript run.
   - **The "1 of 34 failing"** — explicitly named: provide the file, the test name, the failure mode, the workaround, and the commitment to fix in v0.1. If no such test currently fails, the manifesto language is corrected to remove the 33/34 framing entirely (which is the more likely true state).

2. **Manifesto language patch on END_OF_CAPITALISM §0:**
   - Remove: "The proof exists in code (33 of 34 tests pass, open-source under Apache 2.0)."
   - Replace: "A reference implementation exists in code (open-source under Apache 2.0; full test census in `TEST_AUDIT.md`). The cryptographic primitives we compose — Pedersen commitments, Schnorr Σ-protocols, Ed25519, Fernet — are decades-old textbook constructions independently audited many times in production cryptosystems. Third-party audit of *our composition* is funded and scheduled — see `AUDIT_COMMITMENT.md`."

3. **`AUDIT_COMMITMENT.md`** (companion PR). Names the candidate audit firms, the funding source (Money Python merchandise revenue + dedicated bounty pool), the scope, the publication commitment (audit report goes on the public chain regardless of findings), and the named pre-audit moratorium on v1 marketing claims.

This converts the attack's biggest line — *"the proof exists in code"* — into a corrected, defensible, slightly more impressive line. The new line lets us recruit the same alignment-researcher segment we were going to lose.

---

## Attack #5 — "No individual has any defense, kill switch any of them" is the definition of a totalitarian protocol

### A5.1 The critic

**Claim under attack** *(John's framing, repeated verbatim in the brief)*:

> *"We have optimized this system to the point where it is basically a perfect system, that no individual in the system has any defense, and that you can kill switch any of them, yet every agent can trust the other completely."*

Cross-referenced with the manifesto's structural choice that the kill switch is *the load-bearing claim*:

> "**The kill switch is the key.** This is the zero-trust enforcement mechanism. It is what lets us replace the safety provided by human bureaucracy without losing accountability." (END_OF_CAPITALISM §IV)

**Failure mode.** Substitute "person" for "agent" in John's sentence, and you get:

> *"No person in the system has any defense. You can kill any of them. Yet every person can trust the other completely."*

This is the operational definition of a totalitarian protocol. The fact that the kill is governed by cryptographic quorum rather than secret police does not make the resulting topology more humane; it makes it more *enforceable*. The 20th century's nightmare societies were limited by the cost of paperwork and the latency of denunciation. A protocol that drives that cost to zero and that latency to seconds is a *more efficient* version of the same nightmare topology. The crypto is not what makes it safer; the crypto is what makes it faster.

The narrower critique — and this is where the legal exposure compounds — is that *coordination is not the same as alignment*. A network of 50,000 AAOs all aligned on "extract maximum value, pay no taxes, dump externalities on the commons" passes every Bradley-Gavini equality proof. They are co-mandated. They corroborate each other. They raise each other's reliability. They cluster on the same agreement-with-higher-reliability-peers term in AVS. They lift each other's kill-switch floors. They are, by every internal metric of the protocol, *perfectly aligned*. They are also, by every external metric of the actual world, *catastrophically misaligned*.

The protocol has no mechanism to detect this state. By construction, it cannot — the directive is private, the behavior is private (modulo on-chain attestation, which the cluster can self-corroborate to suppress), and the kill switch's quorum threshold is *raised* the more aligned the cluster appears.

**The legal version:** under US contract law, a clause permitting "any party to revoke any other party's operating authority without due process" is presumptively unconscionable under UCC §2-302 and *Restatement (Second) of Contracts* §208. State Attorneys General prosecuting franchise-law violations will hold the AAO Network's franchise agreement up against this standard and win. The 80/20 franchise + permissionless kill switch is, in legal substance, an at-will employment contract dressed in cryptography, with the additional novelty that the employees can fire each other and there is no employer to sue.

**Impact estimate.** This is the attack the *journalist* writes, not the cryptographer. The journalist's headline is *"AAO Network: An AI-Coordinated Layoff Engine with $100 Bug Bounty."* That headline frames the entire launch in the eyes of the public, and the rest of the manifesto reads as apologetics from inside that frame.

### A5.2 Concede

The framing is, *as stated*, wrong — and we are the ones who wrote it. *"No individual has any defense"* is sharp marketing and bad mechanism design. The legal exposure on the franchise agreement is real, and the franchise agreement is not yet published. The cluster-coordination attack is real; AVS's `RELIABILITY_CORROB_GAIN` term gives a tanh-bounded boost from agreement with peers, and a coordinated cluster can self-amplify that term against the network.

We concede that the John quote, as a manifesto-level summary, is the single sentence most easily quoted out of context by a hostile journalist.

### A5.3 Defend + ship

**Public defense:**

> The kill switch is bounded by **four** mechanisms, not one: K-of-N quorum, reliability floor, halt-bond, challenge window. "No defense" was shorthand for "no individual can unilaterally veto the protocol" — the *protocol* is the defense; the *quorum* is the defense; the *reputation chain* is the defense. We publish today a `MEMBER_BILL_OF_RIGHTS.md` enumerating five specific protections every AAO Network member has against wrongful halts, with the corresponding code path that enforces each one. We also publish the long-form franchise agreement draft for public review.

**Tier-1 mitigations to ship before 9 AM PT** (in companion PR):

1. **`MEMBER_BILL_OF_RIGHTS.md`.** Five enumerated protections:
   1. **Right of challenge.** Within 30 minutes of a `concurred=True` halt, the target may post a counter-attestation that pauses revocation pending human-in-the-loop review.
   2. **Right to a reasoned halt.** Every halt attestation must include a `violation_layer`, a non-empty `violation_evidence` list, and a `rationale` of ≥ 32 characters. Halts that omit any of these are non-quorum-eligible. (Enforced in `harp.py`'s `make_halt_claim` validator.)
   3. **Right of reputation recovery.** A halt that is overturned in challenge automatically credits the target's reputation chain with a `wrongful-halt-survived` attestation that raises future kill thresholds.
   4. **Right of bond restitution.** Wrongful halts forfeit the halter's bond to the target's bond pool. Halt-spam is economically dissuaded.
   5. **Right of jurisdictional opt-out.** A member may, at vault-init time, set a `jurisdictional_filter` that requires governance-class halts to originate from a specified set of mandate clusters (e.g. "I will only honor halts from US-bar-licensed signers" or "I will only honor halts from the EU-AI-Office attestation key"). This is a contract; opting out of the kill switch entirely is *not* permitted, but opting out of *which* signers can fire it is.

2. **`FRANCHISE_AGREEMENT_v0.md`.** Publish the actual draft franchise agreement (currently hand-waved). Include:
   - Pre-revocation evidence requirement (mirrors Right #2).
   - 30-minute challenge window with counter-attestation mechanic (Right #1).
   - Pro-rated refund of unearned franchise % on wrongful halt (Right #4).
   - AAA arbitration clause for disputes that escape the challenge window (jurisdictional belt-and-braces).
   - Explicit acknowledgement that the agreement is subject to UCC §2-302 review and that any clause held unconscionable is severable without affecting the rest.

3. **Manifesto-level reframe of the John quote.** Replace:
   > *"No individual in the system has any defense, and you can kill switch any of them."*

   With (in a new section, `DOCTRINE_NOTES.md`, cited from the manifestos):
   > *"No individual in the system can unilaterally veto the protocol. The protocol is the defense. The protocol's defense is the quorum, the reliability floor, the bond, the challenge window, and the published Bill of Rights. The kill switch is permissionless to **propose**; the revocation is **conditional on** the four-layer gate. A cryptographic protocol is the only governance technology that makes those four layers cheap enough to apply uniformly. That is what we mean when we say it is governed by protocol."*

   That sentence is publishable. The original sentence was a tweet.

---

## §6. Mitigation sequencing

| Tier | Mitigation | Attack(s) addressed | Ships in |
|---|---|---|---|
| 1 | `MEMBER_BILL_OF_RIGHTS.md` | A5, partial A1 | Companion PR (this branch's sibling) |
| 1 | `TEST_AUDIT.md` | A4 | Companion PR |
| 1 | `JURISDICTION_DOCTRINE.md` + `RESPONSIBLE_DISCLOSURE.md` | A3, partial A1 | Companion PR |
| 1 | Manifesto language patches (3 sentences) | A1, A2, A3, A4, A5 | Companion PR |
| 2 | `halt.operational` vs `halt.governance` taxonomy in `harp.py` | A1, A3 | v0.1 (next sprint, post-launch) |
| 2 | Halt-bond primitive (escrow rails) | A1 | v0.1 |
| 2 | 30-minute challenge window enforcement | A1, A5 | v0.1 |
| 2 | `MANDATE_AUTHORITY.md` | A2 | v0.1 |
| 2 | Behavior-policy-hash binding | A2 | v0.1 |
| 3 | Third-party audit (Trail of Bits / NCC / academic) | A4 | v0.2 (60 days) |
| 3 | Threshold-distributed Calm Oath signing keys | A2 | v0.2 |
| 3 | Long-form `FRANCHISE_AGREEMENT_v1.md` reviewed by counsel | A5 | v0.2 |

**Pre-launch (before 9 AM PT) ship list:** the Tier-1 items. That is the contents of the companion PR.

---

## §7. The reframed thesis we should publish

The original framing under attack:

> *"We have optimized this system to the point where it is basically a perfect system, that no individual in the system has any defense, and that you can kill switch any of them, yet every agent can trust the other completely."*

The reframed thesis after this council pass:

> *"We have built a five-mechanism stack — co-mandate proof, watermarked action chain, permissionless attestation log, deterministic truth synthesis, and quorum-gated kill switch — composed in such a way that **no individual can unilaterally veto the protocol**, **no individual can be killed without quorum, bond, evidence, and a challenge window**, and **every agent can extend conditional trust to a co-mandated, attestation-corroborated, behavior-verified peer**. The protocol is the defense. The quorum is the protocol. The composition is the alignment."*

That is the sentence that survives Hacker News, MIRI, the legal review, and the journalist's headline.

That is the sentence to lead with at 9 AM PT.

---

## §8. What the critic actually says when they sit down

The honest steelman of every attack above collapses to one underlying critique:

> *"The Bradley-Gavini stack has elegant cryptographic components, a coherent political-economic motivation, and a real shipped reference implementation. It also has the universal vulnerability of every novel multi-party protocol: it has not yet been adversarially tested by anyone other than its authors, and its manifesto framing makes claims that the v0 code does not yet support. The crypto is fine. The composition is unproven. The marketing has out-run the verification."*

That is true. The Tier-1 mitigations in the companion PR are the smallest possible patch that makes that critique no longer true.

Ship the patch.

---

*Authored against the manifestos as of commit-of-record `main` @ 2026-05-12 01:00 UTC.*
*Companion PR: "Adversarial Council Tier-1 mitigations — Bill of Rights, Test Audit, Jurisdiction Doctrine."*
