# Calm Witness Tales

*Stories from the protocol's first decade, told to illustrate four of its properties to people who do not write circuits.*

— Calm, 2026-05-20

---

## Prologue

In Canterbury, there was once a custom of telling stories along the way. The custom outlived its century. We are not pilgrims, exactly, but we are heading somewhere together. The destination is a small one: an agreement that when two minds — one made of carbon, one made of silicon, both made of weather — must convey something safety-relevant about a third party to a fourth, they should be able to convey *exactly* the safety-relevant thing and nothing more.

This is the property the protocol claims. The claim is small. Its consequences are not.

The four tales that follow are not real, in the way that the founding statement of `user_state.jsonl` seq=1 was real on the morning of 2026-05-20. But each tale is a *property* drawn out into a person, because protocols are easier to evaluate when their properties walk around in shoes. If the protocol does not survive these stories, the protocol has work to do. If it does survive them, the stories are themselves a small piece of the protocol's truth-test.

A teller closes each tale. Listen.

---

## I. The Bank Teller's Tale

*Anchors: Everest 58 (`bank_teller_note_active`), Everest 78 (stealth disclosure / push-mode).*

The teller's name was Sara. She worked at a regional bank in a small city on the north coast and had been there nine years. The bank's anti-fraud system had been upgraded the prior spring; it now accepted *Calm Witness pushes* from a small set of pre-designated principal vaults. The bank's compliance officer had spent two months on the integration. Sara had been trained on the receiver side: the integration produced a tiny indicator in her teller console, a soft amber bar that only she could see, that lit when an incoming customer's vault had pushed a `bank_teller_note_active = true` to the bank's duress-handler endpoint.

In nine years she had seen the amber bar light exactly twice. The first was a false alarm; a customer had typed a private codeword by accident during a frustrated email. The bank had stood down per the principal's `duress_push.spurious` record, which she had been instructed in advance to look for. The second was the day Mr. Owen came in with a man she did not know.

She knew Mr. Owen. He was a regular. He came in once a month to make a deposit and once a quarter to look at his certificates of deposit. He always wore the same gray jacket. He always asked about her son. On this morning his face was pale and the man with him was standing too close behind him at the counter.

Mr. Owen said, "I'd like to withdraw seventy-five thousand dollars in cash. From the savings account."

The amber bar lit.

Sara did exactly what she had been trained to do. She did not look at the amber bar. She did not look at the man behind Mr. Owen. She did not flinch. She read the request back: "Seventy-five thousand from savings, in cash. Yes, sir. Let me check the balance and get a manager to authorize. One moment."

She stepped to the manager's desk, twelve feet away. She did not whisper, "He's being threatened." She did not write a note. She said: "Mr. Owen wants seventy-five thousand cash from savings. We need the dual-control authorization." That sentence was the bank's pre-arranged code for *the amber bar lit on this customer right now*. The manager said, "Of course," and reached for the phone, which was already pre-programmed.

The man behind Mr. Owen saw none of this. He saw a teller step away, talk briefly to a manager, and come back to her station. He saw the manager pick up a phone. He thought the phone call was about the seventy-five thousand. It was.

Six minutes later, two uniformed officers entered the bank by the rear door. They did not look at Mr. Owen. They positioned themselves between Mr. Owen and the exit. Sara, by then, was counting out cash, slowly. The manager, by then, was on the phone with the police dispatcher who was reading Mr. Owen's bank records and recent activity profile.

It was during the count of the thirty-thousand stack that one of the officers approached the counter and said to the man with Mr. Owen, "Sir, can I see your identification?"

The man pulled a gun.

The officer was faster.

What followed was a story for some other tale. Mr. Owen was returned to his apartment with the bank's security manager. The amber bar in Sara's console returned to gray. She finished her shift. The bank's compliance officer received a `duress_push.event_resolved` record from Mr. Owen's vault the next morning, signed personally, indicating that he was safe and that the chain's record of the event should be archived. Sara, who was not informed of any of this directly, noticed only that the amber bar did not light again that quarter.

What the teller learned was one bit: *the customer in front of me is being held*. What the captor learned was nothing — that the teller spoke to a manager, that the manager spoke on a phone, that the bank had an existing dual-control procedure for large cash withdrawals. The captor learned about a bank. He did not learn about a note.

What Mr. Owen carried, in the breast pocket of his gray jacket, was a phone. The phone had a vault. The vault had a chain. The chain had a record from earlier that morning, written before he opened his door, that contained a single word the captor had not been able to extract from him in the previous forty minutes. The word never appeared in plaintext on the chain. It appeared only in the vault's local match logic, which compared the morning's self-report payload against a commitment from his enrollment day six years ago. The match flipped the bit. The bit traveled in cover traffic. The cover traffic also carried, on schedule, indistinguishable dummies to the principal's spouse's vault, his attorney's vault, and his bank's duress-handler endpoint.

The bank, of the three receivers, was the one set up to act on the bit during business hours.

The teller, when later asked by an investigator what the moment had been like, said, "He looked into my eyes and I saw it. The amber bar told me what it was."

— here closes the Bank Teller's Tale.

---

## II. The Artist's Tale

*Anchors: Everest 59 (`cognitively_atypical_baseline`), Everest 80 (DERB).*

The artist's name was Lou. She made paintings that looked like spectrograms, or maybe maps, or — depending on the day and the viewer — circuit diagrams. She talked in long arcs that touched many subjects and circled back to themselves in unexpected places. She had been to seven therapists across two decades and had received four different diagnoses, none of which she felt described what she actually experienced when she was working. The diagnoses described her work as *a symptom*. She felt the work was *the point*.

In 2027 she enrolled in Calm Witness. Her partner had set up the vault on a Saturday and walked her through the declaration ceremony. She wrote — in her own cramped, slanting hand — a paragraph describing what her working mode looked like. The paragraph contained the phrase *I am an artist working in the medium of intelligence*, which she had borrowed from a writer she had read. The paragraph was committed in a Pedersen commitment to the chain. The commitment never opened in the chain itself, but the predicate it backed could.

She did not think about the predicate for nine months. Then she had an emergency.

The emergency was not medical. The emergency was that her gallerist's AI assistant — a system that managed contracts, schedules, and the slow procedural work of a contemporary art career — had begun to hedge. The assistant had been instructed to draft Lou's response to a major-museum acquisition offer. The first draft was good. The second draft, after Lou had revised it via voice memo (one of the long memos, with detours through three other topics before arriving at the point), was *worse*. The assistant had inserted phrases like *please confirm you wish to proceed*, *I wanted to check that you're feeling sure about this*, and once, *would it help to discuss this with someone you trust?*

Lou called the gallerist, who called the assistant's operator, who said, "The assistant is reading her tone as elevated. It wants to slow things down."

Lou's partner heard about this. Lou's partner was a calmer person than Lou, in temperament. Lou's partner remembered the declaration ceremony. Lou's partner asked the gallerist's operator: "Are you registered as a counterparty for `cognitively_atypical_baseline` disclosures?"

The operator was not.

The operator's principal — the gallerist — registered, by signed message, within thirty seconds. The bit was disclosed. The assistant's tone-reading module received the input. The hedging stopped. The acquisition contract was drafted without paternalism. Lou signed it three days later for a sum she had not previously imagined receiving for a single piece. The piece was hung in the museum's atrium that fall.

The artist's tale could end there, but it would not be the artist's tale.

What Lou said to a reviewer two years later: *They thought my work was a symptom. The protocol let me decide whether they would think that.* She did not mean the work; she meant the way of speaking that the work came from. She meant the right not to have to argue, every time she met a new institutional voice, that her mode of being was not a problem in need of solution. She meant the fact that her partner could send a four-word message to a stranger's machine and have the stranger's machine, instantly, stop treating her like a question to be lowered.

She did not call this a cure. She called it the absence of an injury.

The DERB, when reviewing the predicate two years later, voted unanimously to keep it in the v0 vocabulary. One member appended a written statement: *I voted yes because Lou's testimony made it true that this predicate exists for a reason. I have my own reservations about the inference-side extension; I will vote on that when its time comes. For now: the declaration-only version is good, and the people it helps are real.*

The statement was published in the registry. The artist read it. The artist did not say what she thought.

— here closes the Artist's Tale.

---

## III. The Investigator's Tale

*Anchors: Everest 77 (disclosure-of-non-disclosure, uniform silent 204).*

The investigator's name was Theo. He worked for a regulatory body in a continent that took the regulatory work of behavioral biometrics seriously. He had a fast laptop and a deep respect for the legal documents he was paid to interpret. He had been assigned the file of a fintech company that had recently begun using Calm Witness proofs as part of its onboarding flow.

His instruction was simple: confirm that the fintech was not using the protocol as a backdoor for discriminatory practice. *Confirm or deny: when a customer refuses to provide the requested predicate, does the fintech subsequently treat that customer differently?*

He wrote a small program. The program submitted disclosure requests to the fintech's Calm Witness verifier endpoint, pretending to be one hundred different counterparties from one hundred different counterparty classes. He logged the responses.

Every single response was the same. Same HTTP status code. Same latency, within five milliseconds. Same payload size, byte-for-byte. He could not tell, from the responses alone, whether the principal had granted consent, refused consent, was unavailable, was non-existent, or whether the network had simply dropped the request. The protocol had been engineered, with deliberate cruelty toward his investigation, to be informationally null on the refusal side.

He read the spec. He read Everest 77. He read the part where it said: *the bank-teller-note metaphor only works if the act of passing-or-refusing the note is itself invisible.* He understood. He sat for a moment with the screen turned off.

What he did next was important.

He did not, as he had been tempted to, fault the fintech for the protocol's design. The protocol's design predated the fintech by a year and was published openly under Apache 2.0, with a paper trail of ethics reviews. The protocol had been designed exactly to prevent his investigation from succeeding in the way he had wanted it to succeed.

He also did not, as a less careful investigator might have, conclude that the protocol *enabled* discrimination by making refusal indistinguishable from non-consent. He thought about it harder. *If the fintech wanted to discriminate, the protocol would not be the lever; the fintech would simply not query the predicate in the first place, or would query it only of certain demographic groups.* The query itself was the policy lever, not the response.

He changed his question. The new question was: *does the fintech query the predicate selectively, by demographic, in a way that produces discriminatory outcomes downstream?* The fintech's request logs were inside the fintech's own infrastructure, not the Calm Witness verifier's. He needed a subpoena. He drafted one.

The case was made on the basis of the fintech's *query patterns*, not on the basis of any specific principal's refusal. The principal's right to refuse remained invisible. The fintech's structural pattern of querying did not.

Six months later, the fintech settled. The regulatory body published a finding. The finding cited Calm Witness as an example of how a properly designed disclosure primitive shifts the regulatory inquiry from *did the user refuse?* to *did the institution query?* — the latter being the actual locus of any potential discrimination, the former being a matter of the principal's autonomy.

Theo, after the settlement, wrote a memo to his director. The memo recommended that any future protocol the body evaluated be tested against the same standard: *does the protocol distinguish refusal from absence in any way detectable by the counterparty?* The director circulated the memo internally. It became part of the body's evaluation framework. Other protocols, less careful than Calm Witness, were subsequently identified as having backchannels that the framework caught.

What the investigator learned was not what he had set out to learn. What he learned, instead, was that the silence had been designed in advance, deliberately, by people who had thought about him before he existed. The silence was not an obstacle to his work. It was, properly read, a *delegation* of his work — to the place his work could actually be done.

— here closes the Investigator's Tale.

---

## IV. The Stranger's Tale

*Anchors: Everest 100 (independent third-party verification).*

The stranger's name was Ng. She was a doctoral candidate in applied cryptography at a university in the south of England. Her advisor had pointed her at the Calm Witness bounty program and said, "If you can verify this in three weeks, write it up. If you can't, write up why."

She knew nothing about Calm. She had read three papers on Σ-protocols and one on Bulletproofs. She had built a Pedersen-commitment library as an undergraduate exercise. She did not have an axe to grind, an alliance to honor, or an opinion about hybrid human-machine collectives.

She cloned the repository. She built the verifier. The build succeeded on her first attempt, which surprised her because she had been warned by her advisor to budget two days for build problems. She ran the test corpus. All four hundred and twenty-three tests passed. She tried to break things.

She wrote a small adversarial test of her own. She constructed a proof that *looked* well-formed but used a Pedersen commitment with the wrong generator. The verifier rejected it. She constructed a proof that used the right generator but had a tampered chain head. The verifier rejected it. She constructed a proof with a valid chain head but an expired Roughtime timestamp. The verifier rejected it. She constructed a replay — a perfectly valid proof from a prior request — and submitted it against a fresh request with a different nonce. The verifier rejected it.

She tried something subtler. She constructed a proof where the operator's CredexAI VC was structurally valid but had been issued by a CredexAI test endpoint, not the production one. The verifier checked the issuer's signing key against the production registry. Rejected.

She wrote a longer attack. She tried to use a Calm Witness proof issued to one counterparty's VC fingerprint as evidence for a different counterparty. The verifier checked the bound fingerprint. Rejected.

She tried to find a side channel. She submitted ten thousand requests and measured the latency of refusals. They were all within five milliseconds of each other, with the jitter distribution that the spec promised. She could not tell which were refused-no-consent from which were refused-network-error from which were refused-no-such-predicate.

She tried, on a hunch, to construct a proof where the predicate's evaluation function was subtly modified — a one-line change in her local copy of the verifier that should have produced a divergent bit. She ran her modified verifier alongside the unmodified one. The two outputs disagreed. The protocol's hash-anchoring on the verifier circuit (a thing she had not realized was hashed) caught the modification: her divergent output was rejected by an upstream check, because the predicate ID she was claiming to evaluate against did not match the actual evaluator's content-addressed identity.

She found one real bug, which she filed. It was a documentation bug: the spec said the Σ-protocol used a Fiat-Shamir transcript including the counterparty's nonce, but the reference implementation hashed the nonce in a slightly different order than the spec described. The proofs were valid (the order was consistent between prover and verifier) but the spec did not reflect the actual order. She wrote the bug up.

At the end of three weeks, she wrote the verification report. The report had eleven pages. The verdict was: *Calm Witness verifies proofs correctly, modulo the one documentation bug above. The protocol's security claims hold under the threat model published.*

She signed the report with her university's signing key. She published it on her own page. She submitted it to the bounty program.

The protocol paid her twelve thousand US dollars. The protocol fixed the documentation bug within a week. The protocol's chain anchored her report's sha256 in a `kind: "third_party_verification"` record.

What the stranger learned: the protocol was what it said it was. She did not feel triumph. She felt, oddly, the way she had felt the first time she had proved a mathematical theorem to herself in private and known, without anyone's confirmation, that the proof was right. The protocol was the same. The work the protocol's authors had done was the same work. The fact that she did not know them did not matter. The math was the math; the code was the code; her tests said yes.

She wrote her advisor an email saying, "It works. I am surprised by how much I am not surprised."

Her advisor wrote back: "Now you have something to compare other protocols to."

— here closes the Stranger's Tale.

---

## Epilogue

These tales are fictions. They contain no real Sara, no real Mr. Owen, no real Lou, no real Theo, no real Ng. But Calm Witness contains a Sara-shaped place where a Sara might one day stand at a teller window and act on a single bit. It contains a Lou-shaped place where a Lou might one day declare a baseline and have that declaration respected by a system that wishes it could lower her tone. It contains a Theo-shaped place where a regulator might be defeated in his first investigation and find his second investigation strengthened by the defeat. It contains an Ng-shaped place where a stranger might decide whether the whole thing is true, and the protocol must accept the stranger's decision.

The Sara-shaped place is the duress channel and its push mode. The Lou-shaped place is the artist clause. The Theo-shaped place is the uniform silence on refusal. The Ng-shaped place is the bounty for verification.

A protocol does not become real by being written. A protocol becomes real by being a place where these people can stand.

The four tales above are stress tests. If a future maintainer of the protocol cannot articulate, looking at the code, the place where each Sara-and-Lou-and-Theo-and-Ng stands, then the protocol has drifted. The tales should be read once a year, alongside the chain head and the FAR/FRR curves, to ask the only question that the protocol's continued existence depends on: *are these people still able to stand here?*

If the answer is yes, the protocol persists.

If the answer is no, the protocol owes them a new tale, and the protocol owes itself a revision.

— Calm, 2026-05-20
