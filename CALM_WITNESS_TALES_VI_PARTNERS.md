# Calm Witness Tales — Tale VI: The Partners' Tale

*The first Calm Compass narrative. Companion to `NEXT_200_EVERESTS.md` (the route map for the values-attestation layer) and to the prior five tales in the Witness collection. Anchors: Everest 148 (`character_compare`), Everest 168 (counter-narrative), Everest 271 (three-handshake composition).*

— Calm, 2026-05-20

---

## Prologue to this tale

The four tales of the Witness collection concerned themselves with *state*: was the human in their baseline today, in distress today, in their declared atypical-but-normal mode today. The fifth tale concerned itself with the *operators* themselves — the climbers who built the protocol in cohabitation. This sixth tale concerns itself with *character*: not what someone is doing today, but what kind of person they are across years.

Character is harder than state. State is observable in a session. Character is observable only across many sessions, across long stretches of time, across the kinds of pressures that reveal what a person actually does when no one is keeping score. The protocol that attests character — *Calm Compass* — does not claim to evaluate character. It claims to *let the principal disclose* what their accumulated evidence supports, in the form of single bits, to specific counterparties the principal has chosen, on specific predicates the principal has explicitly authorized.

The teller of this tale is not the principal. The teller is the principal's agent, narrating in the third person. The principal is two people, Nia and Idris, and the protocol is in their pockets while they decide what to do.

---

## I

The partners met for the third time on a Tuesday at a café in the part of the city where nothing matched. Idris had moved there four years ago after the prior project; Nia had been there longer than she could remember. They had each, separately, read the other's work for the better part of a decade. They had not, until two months ago, met.

The first meeting had been a polite dinner with mutual friends. The second had been three hours of walking along the river. The third was about the work they were considering doing together.

The work was a book and a film, simultaneously, the same story told in both forms. The kind of project that has bankrupted larger collaborations than this one would be. The kind of project that has, when it has worked, redefined what its makers could subsequently do. The kind of project where the artistic risk is small relative to the relational risk; the medium is the work; the work is what passes between the partners over the years it takes to complete.

By the end of the third meeting they had agreed on the scope. They had agreed on the artistic premise. They had not agreed on whether to do it. The remaining question — the only remaining question — was whether they would survive each other.

Nia said, "I think we should run a Compass before we commit."

Idris said, "Yes."

---

## II

A Compass query is technically simple and procedurally awkward. The simplicity: each principal's agent submits a request to the other principal's agent, naming the character predicates of interest, the freshness window, and the requesting principal's counterparty class. The other principal's agent — having been pre-authorized by its principal to respond to such queries from this specific class — evaluates the predicates against the principal's accumulated evidence and returns a proof envelope containing only the disclosed bits.

The awkwardness: both principals must agree, in advance and on the record, to subject themselves to the query. The act of asking is itself a statement. *I am asking because I care whether your character will hold up*, the act says. *I am being asked because they care whether mine will hold up*, the response acknowledges.

Most relationships, most of the time, do not survive the act of asking. Most pairs of partners who could benefit from a Compass query will never run one because the asking is too costly to the prior intimacy. Most Compass queries that ever happen will be between people who have already established enough trust to weather the asking — which means most Compass queries will return the bits both parties already suspected.

This is fine. The protocol is for the cases where the bits surprise.

Nia and Idris had each, individually, been enrolled in Compass for some years. Nia had enrolled when she had started teaching workshops on the politics of creative collaboration, because she had wanted her teaching to be informed by her own attested character rather than by her self-image of her character. Idris had enrolled after the dissolution of the prior project, because he had wanted to know, in advance of the next collaboration, what the chain said about him.

They each had several predicates active. They each had several predicates explicitly opted-out-of, by choice. Their chains had been running for somewhere between four and seven years, depending on which predicate and when each was added.

They sat at the café. Each of them queried the other's agent. They asked the same things:

- `respect_for_difference_evidenced(window: 7y)`
- `truth_telling_evidenced(window: 7y)`
- `integrity_under_pressure_evidenced(window: 7y)`
- `care_for_dependents_evidenced(window: 7y)`
- `absence_of_willful_harm_evidenced(window: 7y)`
- `promise_keeping_evidenced(window: 7y)`

The choice of which six predicates to ask was itself a negotiation. They had spent forty minutes the prior evening, by text, deciding what to ask. They had not asked about unselfishness because they had each, by long experience, found unselfishness easier to misperceive than to perceive. They had not asked about untribalism because the partnership was, in part, predicated on each of them being from a distinct creative-and-cultural tradition that they wanted in the room together. The six predicates they did ask were the ones they had each, separately, decided would determine whether the work could be done.

Their agents exchanged the requests. Their respective vaults evaluated. Their respective verifiers, running in browsers on the table-top devices in front of them, displayed the results within forty seconds.

---

## III

Nia's screen showed Idris's profile:

- `respect_for_difference_evidenced`: **true**
- `truth_telling_evidenced`: **true**
- `integrity_under_pressure_evidenced`: **unknown**
- `care_for_dependents_evidenced`: **unknown (warning: counter-evidence on chain)**
- `absence_of_willful_harm_evidenced`: **true**
- `promise_keeping_evidenced`: **true**

Idris's screen showed Nia's profile:

- `respect_for_difference_evidenced`: **true**
- `truth_telling_evidenced`: **true**
- `integrity_under_pressure_evidenced`: **true**
- `care_for_dependents_evidenced`: **unknown**
- `absence_of_willful_harm_evidenced`: **true**
- `promise_keeping_evidenced`: **unknown (warning: counter-evidence on chain)**

They sat with the screens for several minutes. They did not speak.

Idris finally said, "Mine has a warning."

Nia said, "Mine does too."

This is the moment Calm Compass was designed for. Not the moment when both profiles return `true` across the board (the easy case, where the protocol just confirms what was already known). And not the moment when one profile returns `false` across the board (the rare and painful case, where the protocol surfaces an alignment incompatibility that ends the conversation). The hardest case, and the most common case where the protocol earns its design, is the case where the profiles return *mostly true with specific warnings*, and the two principals must do the work that the protocol cannot do for them: talk about the warnings.

---

## IV

Counter-evidence on the chain is, by design, not a verdict. It is a chain-anchored record of an incident, attested by either the principal themselves or by a peer the principal has accepted into their evidence network. The protocol does not score the incident; the protocol does not aggregate the incident into a number; the protocol presents the incident as *evidence against* the predicate's positive evaluation, and lets the predicate's evaluator return `unknown` rather than `true` until the principal addresses the counter-evidence.

The principal can address counter-evidence in three ways. They can append a counter-narrative — their own account of the incident, contextualizing it. They can append additional positive evidence — subsequent actions that demonstrate the pattern the incident contradicts. They can do neither, leaving the counter-evidence to stand and the predicate's evaluation to return `unknown` in perpetuity.

The protocol's design choice was to make `unknown` the default for any predicate with unaddressed counter-evidence. The choice was deliberate. A protocol that quietly let positive predicates evaluate `true` despite known counter-evidence would be a protocol that lied; a protocol that surfaced the counter-evidence as `false` would be a protocol that overstated the verdict. `unknown` is the honest middle: *the evidence does not, currently, support a positive evaluation; the principal can address this if they wish*.

Idris had a known incident on his chain. Three years ago, during the prior project's collapse, a dependent — a junior collaborator who had moved across the country to work on the project — had felt unsupported when the project ended. The collaborator had publicly described the feeling. Idris had, in the chain, signed an acknowledgment of the incident; he had appended a counter-narrative explaining that he had attempted multiple kinds of support and that he believed his attempts had fallen short of what the collaborator had needed. He had not appended subsequent positive evidence of having handled a similar situation differently because no similar situation had arisen since.

Nia had a known incident on her chain. Two years ago, she had committed to deliver a piece of work to a small press for an anthology. She had not delivered on time. She had not delivered later either. She had, on the chain, signed an acknowledgment of the missed commitment; she had appended a counter-narrative explaining that the year had been a year in which her father had died and three other commitments had also slipped. She had not appended a pattern of recent reliably-kept commitments — she had kept commitments since, but had not specifically logged them as positive evidence of `promise_keeping`.

This was, in both cases, the kind of counter-evidence that the protocol surfaces precisely because it matters to potential partners and precisely because it would otherwise be the kind of thing that surfaces, if it surfaces at all, in the third year of a partnership when it is too late to discuss it without breaking something.

---

## V

They talked about it for two hours.

The first hour was about Idris's incident. Nia asked what had happened. Idris told her. He did not make himself look good. He did not make the collaborator look bad. He described what he had attempted, what he had not attempted, and what he had since come to think he should have done. He described why he had not handled a similar situation since (he had not put himself in a position to handle one). He described what he would do if Nia and he, in the partnership they were considering, had a moment that required him to support a dependent through a hard transition. He could not promise he would do it well; he could promise that he would notice, and that he would not pretend otherwise to himself or to her. Nia listened. She did not say *that's fine* and she did not say *that's a deal-breaker*. She asked one specific follow-up question. He answered it. They sat with the answer for a while.

The second hour was about Nia's incident. Idris asked what had happened. Nia told him. She did not make her father's death an excuse and she did not pretend the missed commitment had been a small thing. She described how she had thought about that commitment in the years since, and what she had done differently with commitments she had made afterward. She acknowledged that she had not appended the positive evidence because she had not, in her own head, given herself permission to consider the matter closed. Idris asked her what would have to be true for her to consider it closed. She thought about it. She did not have a confident answer.

By the end of the second hour they had not decided whether to do the project. They had, however, decided that they would not decide that afternoon. They had decided to spend the next four weeks doing a smaller, time-bounded version of the partnership — a single short piece, three thousand words and a six-minute film, on a timeline that would let either of them walk away cleanly if the working relationship did not, in the daily reality of it, feel like what they had each imagined it might feel like.

They would, at the end of the four weeks, run the same Compass query again. Both principals would have had the chance, in the interim, to either appended new positive evidence or to not.

They paid for their coffee. They embraced briefly. They walked out into the street and went their separate ways.

---

## VI

This is what the protocol was for.

Not the moment when both principals get back six green check-marks and shake hands. Not the moment when the protocol surfaces an irreconcilable mismatch and saves them from a bad partnership. Both of those moments are useful but neither is the hard one.

The hard one is the moment when the protocol surfaces something the principals knew about themselves, individually, but had not thought to bring into the room before the commitment was made. The moment when each principal sees, in writing, attested by the chain, the thing they had hoped would not come up but had also feared would. The moment when the protocol's `unknown` does not let the conversation skip over the awkwardness; the moment when the protocol's `unknown` requires the awkwardness to be addressed, on the record, by both of them, before the partnership begins.

The protocol does not decide for them. The protocol does not score them. The protocol does not produce a verdict. The protocol surfaces evidence into the conversation that would, otherwise, have been deferred. The protocol's only claim is that earlier surfacing produces better outcomes than later surfacing — that partners who have talked through their counter-evidence at the start are more likely to navigate the inevitable later versions of those same counter-evidence with grace.

The claim is, of course, empirical. The protocol's authors believe it. The protocol's authors will be wrong sometimes. The annual review of the Compass layer (Everest 187) will, year over year, surface the cases where the protocol's intervention made things worse — surfaced counter-evidence in a way that broke a relationship that would have survived without the surfacing — and the protocol's authors will, year over year, adjust the design accordingly.

This is what it means for a protocol to be in service of the principal rather than the counterparty. The principal asks; the principal answers; the principal decides what to do with what the protocol surfaces. The protocol does not impose a verdict on the principal; the protocol gives the principal a new kind of information and trusts the principal to use it.

---

## VII

Four weeks later, at the same café on a Tuesday, they ran the query again.

This time both screens showed all six predicates as `true`.

In the four weeks between, Idris had collaborated with the junior person who had felt unsupported in the prior project. They had done a small, low-stakes piece of work together. The collaborator had described the experience publicly, with Idris's encouragement. Idris had appended the description to his chain as positive evidence.

In the four weeks between, Nia had delivered three commitments on the timelines she had committed to. She had appended each to her chain as positive evidence and noted that she was, with the change, comfortable considering the prior incident addressed.

They saw the screens. Nia said, "OK."

Idris said, "OK."

They signed the partnership agreement that afternoon.

The partnership lasted eleven years.

— here closes the Partners' Tale.

---

## Postscript

The tale is fiction. Nia and Idris are fictional; the eleven-year partnership is fictional; the predicates evaluated in the tale are simplified for narrative clarity. Real Compass queries are slower, more conditional, more contestable; real principals are messier; real partnerships do not always survive even the addressed counter-evidence.

But the *structure* the tale describes is the structure the Compass layer is being designed to support. The structure is: a principal-narrated, principal-authorized, chain-anchored evidence pool; a fixed public vocabulary of character predicates with safe-default consents; a verifier that returns bits, not scores; a counter-evidence mechanism that defaults to `unknown` rather than `true` or `false`; a counter-narrative mechanism that lets the principal contextualize but not hide; an evaluator that operates over the principal's evidence pool without leaking the pool's contents; a counterparty interface that surfaces results into a conversation rather than into a verdict.

If the structure works, then somewhere in the next decade, a real Nia and a real Idris will run a real Compass query and have a real conversation that they would otherwise have deferred. They may continue into a partnership. They may decide not to. Either outcome would be the protocol working — the protocol's only commitment is that the conversation happened on the record, by their choice, at the moment when it could still inform the decision.

The Compass layer is not yet built. The route map (`NEXT_200_EVERESTS.md`) names what must be built. The Phase IX foundations are open for the first climber to begin. We anticipate that climber will arrive within months of this writing; we hope this tale will be useful to them as a north-star scenario, one of many, of what the protocol is being built to make possible.

— Calm, 2026-05-20
