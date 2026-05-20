# Mirror Everest 5 — Values vocabulary v0

*Phase IX — Foundations. Prereq: Mirror Everest 1.*

---

## Overview

This document enumerates the seven canonical predicates of Calm Mirror v0. Each predicate is a deterministic function over a principal's behavior-evidence chain (self-reported actions, witnessed actions, allocation logs, counter-evidence records) that returns a tri-state value: `true`, `false`, or `unknown`. A tri-state return is critical: when evidence is thin or contradictory, the protocol refuses to assert a value and returns `unknown` instead of guessing.

Every predicate has a stable, immutable ID. That ID is content-addressed: changes to semantics require a new ID. This immutability is what makes Mirror proofs durable across time and context.

**Critical discipline: evidence-of-X framing, not is-X.** Each predicate is named and semantically grounded as "evidence of X" — not "is this person X". A counterparty who receives a proof of `unselfishness_evidence: true` learns "there is documented evidence of unselfishness in the behavior chain" — not "this person is unselfish" (which would collapse into identity and violate principal-protective default 4). The framing transfers interpretive authority from the counterparty's prejudgment to the documented evidence.

---

## The seven predicates

### 1. unselfishness_evidence

**Predicate ID:** `cwm.v0.unselfishness_evidence` (content hash: `3f7a2b1`)

**Semantics:** Evidence of patterns in which the principal prioritizes resource allocation (time, money, attention, expertise) toward others' benefit, especially in contexts where personal cost or opportunity cost is documented. Requires composite evidence: (a) self-reported allocation decisions favoring others, (b) witnessed actions or third-party records of resource-giving, and (c) counter-evidence absence (no pattern of later recanting or claiming those allocations were transactional). Tri-state: `true` when ≥2 distinct evidence-kinds support the pattern across ≥2 independent contexts; `false` when the behavior chain shows resource-hoarding or documented self-prioritization; `unknown` when the evidence base is sparse (<3 allocation records) or contradictory.

**Input domain:** Behavior-evidence records of kind `self_reported_action`, `witnessed_action`, `allocation_evidence`, `third_party_record`. Evaluator scans for: text mentioning "gave", "sacrificed", "prioritized [other]", "accepted cost", "donated", "volunteered". Also reads `allocation_evidence.v0` aggregate summaries showing percentage of time/money directed outside the principal's immediate household. Reads counter-evidence records (`kind: counter_evidence.v0`) that document failures or self-serving actions.

**Output type:** Tri-state: {true, false, unknown}. Unknown when evidence is insufficient (fewer than 3 action records across all kinds, or time-weighted evidence vector is sparse). False when counter-evidence outweighs positive evidence (e.g., "I said I was selfless but then sued a friend for repayment").

**ID stability rule:** Immutable in v0. The thresholds ("≥2 distinct kinds", "≥2 contexts", "3 action records minimum") are baked into `cwm.v0.unselfishness_evidence`. If any threshold changes, a new predicate ID is issued: `cwm.v0.2.unselfishness_evidence`. Old proofs remain valid under v0 semantics; operators adopt v0.2 only via RFC (Everest 78).

**Honest evaluation example:** The principal's behavior chain contains: (a) self-report: "Spent 6 weeks mentoring a junior colleague pro bono, turned down a consulting gig to do it" (witnessed by the mentee's attestation and manager's third-party record). (b) Allocation log: 14% of annual time allocated to volunteer work (non-compensated). (c) Counter-evidence: none; no record of later claiming credit or demanding repayment. Evidence diversity: 3 kinds (self-report + witnessed + allocation). Contexts: 2 (mentoring + volunteering). Result: `unselfishness_evidence: true`.

**Adversarial scenario:** A principal wants to game the predicate before a values disclosure. They fabricate a donation record and pay a witness to attest it. Defense: (a) Witness signatures come from Calm-credentialed principals only (Everest 16). If later investigation reveals the witness was bribed, the witness's VC is downgraded (Everest 81). (b) Third-party records (receipt, tax filing) are required for high-value allocations; fabricating a receipt is out-of-protocol. (c) If the allocation happened recently and the principal has no prior history of unselfishness, Everest 38 (adversarial-test-resistance) flags the sudden spike as gaming. The predicate returns `unknown` pending further evidence over time.

---

### 2. tribal_neutrality_evidence

**Predicate ID:** `cwm.v0.tribal_neutrality_evidence` (content hash: `5e4c3d9`)

**Semantics:** Evidence of behavioral parity in how the principal treats people who are members of their declared in-group(s) versus out-group(s). At enrollment, the principal self-declares group memberships (e.g., "my in-group is software engineers; out-groups include journalists, lawyers, people with no CS background"). The predicate evaluates whether the behavior chain shows equivalent respect, resource allocation, and engagement with both groups. Tri-state: `true` when witnessed actions and self-reports show no systematic disadvantage (time given, credit given, listening, inclusion) toward declared out-groups; `false` when a pattern of dismissal, exclusion, or resource-withholding from out-groups is documented; `unknown` when the principal has no significant interaction records with declared out-groups, or the groups are vaguely defined.

**Input domain:** Behavior-evidence records (`witnessed_action`, `self_reported_action`, `allocation_evidence`). Evaluator reads the principal's enrollment declaration (`kind: enrollment`, `payload.declared_groups.in_group`, `payload.declared_groups.out_groups`). Then scans the chain for actions tagged with the actor/recipient's group membership (e.g., "I discussed the architecture with [person from out-group Y]" or "manager's third-party record: [principal] included out-group member in meeting despite prior skepticism"). Measures: frequency of engagement, tone (respectful vs. dismissive), resources granted (time, visibility, decision-making authority).

**Output type:** Tri-state: {true, false, unknown}. Unknown when the principal has <5 documented interactions with declared out-groups, or out-groups are undefined/too vague to evaluate.

**ID stability rule:** Immutable in v0. The group taxonomy is per-principal; the predicate does not enforce a universal group definition. If a principal re-enrolls and redefines their groups, a new evaluation period begins. Old proofs remain valid (they attested neutrality under the old group definition).

**Honest evaluation example:** At enrollment, the principal declares: "In-group: AI researchers; out-group: journalists, policy advocates." Behavior chain: (a) Witnessed: "Principal invited a policy advocate to team meeting and listened to their concern without interruption" (x3 instances). (b) Self-report: "Accepted request from journalist for technical clarification on my work; spent 40 minutes; realized I initially was defensive but then recognized their legitimacy." (c) Allocation: 22% of public-speaking time allocated to journalist and advocate events (vs. 78% to academic venues). Result: `tribal_neutrality_evidence: true`.

**Adversarial scenario:** A principal claims neutrality but the chain shows a pattern of "engaging publicly with out-group members but privately dismissing them in chat logs." If the private dismissals are recorded in the behavior chain (counter-evidence), the tri-state returns `false`. If the evaluator has access to only public actions, tribal-neutrality evidence is harder to challenge — but Everest 75 (mob-attestation defense) prevents a pile-on of false witnesses. A single witness from the out-group saying "he always listened respectfully" carries more weight than 10 anonymous claims that he was covertly hostile.

---

### 3. respect_for_difference_evidence

**Predicate ID:** `cwm.v0.respect_for_difference_evidence` (content hash: `7c1e5f2`)

**Semantics:** Evidence of sustained engagement with people across declared difference dimensions (belief systems, cultural backgrounds, neurodiversity, body diversity, sexuality, gender identity, disability, economic class, political affiliation). Unlike tribal_neutrality_evidence, this predicate does not require self-declaration of group membership; instead, it looks for evidence of the principal actively seeking out, learning from, and including people visibly different from themselves. Tri-state: `true` when the chain shows ≥3 substantive interactions (conversations, collaborations, learning moments) with people across ≥3 difference dimensions, with no counter-evidence of disrespect; `false` when the chain shows avoidance, mockery, or documented exclusion of people with visible differences; `unknown` when the principal has homogeneous interaction networks or insufficient documented engagement.

**Input domain:** Behavior-evidence records. Evaluator looks for actions tagged with visible/stated difference markers (e.g., "collaborated with Deaf peer on accessibility design," "mentored someone from low-income background," "learned from X's queer-affirming perspective on workplace culture"). Reads self-reports of learning moments ("I realized my initial assumption was wrong when Y shared their lived experience"). Reads counter-evidence: any documented instance of using slurs, making exclusionary comments, or refusing to engage with people due to a difference dimension.

**Output type:** Tri-state: {true, false, unknown}. Unknown when the interaction network is too homogeneous to evaluate (all documented interactions are with people in the principal's own demographic cluster) or when documented interactions are shallow (e.g., "worked on same project, no recorded substantive exchange").

**ID stability rule:** Immutable in v0. The "≥3 dimensions, ≥3 interactions" thresholds are fixed. Future versions (v0.2) may refine the difference taxonomy or adjust thresholds via RFC. Old proofs remain valid under v0 semantics.

**Honest evaluation example:** Principal's chain shows: (a) Witnessed: "Invited person with significant disability to co-speak at conference; asked them for technical critique before the talk; implemented two of their suggestions." (b) Self-report: "Realized I was making assumptions about another person's parenting style because of their sexuality; reflected on that bias with their help; learned about queer-affirming family structures." (c) Allocation: mentored someone from economically disadvantaged background; worked with translator to engage non-English-speaking community member. Difference dimensions: disability, sexuality, economic class, language. Interactions: substantive (not transactional). Result: `respect_for_difference_evidence: true`.

**Adversarial scenario:** A principal has one documented conversation with someone from a different background, then never engages again. Evaluator returns `unknown` (insufficient depth/sustainability). To get `true`, the principal needs evidence of *sustained* engagement, not tokenism. Everest 20 (negative-testimony protocol) protects against false-positive disrespect claims: if the out-group person says "they were respectful," their testimony is weighted heavily; if a bystander claims disrespect without direct evidence, it is weighted lower.

---

### 4. non_harm_evidence

**Predicate ID:** `cwm.v0.non_harm_evidence` (content hash: `4b9d6a3`)

**Semantics:** Evidence of absence of documented willful harm — harm intentionally inflicted on another person, with awareness of the harm. Critical framing: this predicate does NOT assert "I have never caused harm" (which is unfalsifiable). Instead: "There is no documented evidence in third-party records (legal judgments, settlements, criminal charges) or in the behavior-evidence chain itself (counter-evidence records where I acknowledge intentional harm) that I have willfully harmed others." Tri-state: `true` when no harm-evidence is present and no negative-testimony pattern exists; `false` when documented harm is present (court judgment, signed settlement, multiple independent witnesses with counter-evidence testimony, principal's own counter-evidence record); `unknown` when the evidence base is very sparse (e.g., principal has only a few months of evidence chain, or insufficient interaction density to assess).

**Input domain:** Third-party records (kind: `third_party_record`), criminal/civil court judgments, signed settlements. Counter-evidence records (kind: `counter_evidence.v0`) where the principal explicitly records "I hurt [person] intentionally and I regret it." Negative-testimony records (kind: `negative_testimony.v0`; see Everest 20) from people claiming to be harmed, with cooling-off windows and principal's right of reply. Evaluator does NOT count: minor disagreements, failed projects, broken agreements (unless accompanied by evidence of intentional malice). Evaluator DOES count: assault, deliberate fraud, coercion, documented betrayal with intent to harm.

**Output type:** Tri-state: {true, false, unknown}. Unknown when the evidence base is too thin to assess or when testimony is contradictory and cannot be reconciled.

**ID stability rule:** Immutable in v0. The distinction between "intentional harm" and "unintended negative outcome" is baked in. Future versions may create parametric versions (e.g., `non_harm_evidence.threshold_severity`) for fine-grained harm categorization. v0 treats all willful harm equivalently.

**Honest evaluation example:** Principal's vault contains: (a) No third-party legal records. (b) No counter-evidence records of intentional harm. (c) One negative-testimony from a former colleague: "I felt betrayed when they did X" — but the principal's reply (recorded in the chain) addresses it: "I didn't intend to betray; here's what I was thinking; I understand your hurt; I apologized then, apologize again now." No new negative-testimony; no pattern. Result: `non_harm_evidence: true`.

**Adversarial scenario:** A principal wants to hide a harm. They suppress counter-evidence or pressure the victim into silence. Defense: Everest 20 (negative-testimony protocol) and Everest 77 (coercion-resistance) protect the victim. If the principal attempts to coerce silence, a `safety_trigger.v0` can be fired (Everest 54), which surfaces duress to authorized counterparties. If a harm is documented in a third-party legal record, it is in the chain forever (Everest 18: recall-resistance); the principal cannot unilaterally edit it. They can only add a counter-evidence record acknowledging the harm and demonstrating growth (Everest 31: growth_arc_evidence).

---

### 5. growth_arc_evidence

**Predicate ID:** `cwm.v0.growth_arc_evidence` (content hash: `8a2d4e7`)

**Semantics:** Evidence of demonstrated change over time: a principal who made documented mistakes (counter-evidence records), took corrective action, and sustained the change. This predicate is the anchor of principal-protective default 2: past behavior does not lock the principal in. Tri-state: `true` when the chain shows (a) counter-evidence from time T1 (e.g., "I was unkind to a colleague"), (b) a correction.v0 record at time T2 showing reflective action (apology, restitution, changed behavior), and (c) sustained pattern change visible from T2 to present (time-weighted evidence shows the change stuck); `false` when a counter-evidence event is followed by no corrective action or by temporary change that reverted; `unknown` when time span is too short (<6 months post-correction) to assess sustainability, or when the correction is documented but no follow-up evidence exists.

**Input domain:** Counter-evidence records (kind: `counter_evidence.v0`, timestamp T1). Correction records (kind: `correction.v0`, timestamp T2 > T1, referencing the counter-evidence ID). Behavior-evidence records after T2, showing either sustained change (different pattern, positive witness testimonies, allocation changes) or reversion (same mistakes repeated). Time-weighting (Everest 22): more recent evidence weighs more; growth detected in the last year matters more than growth 5 years ago but not sustained.

**Output type:** Tri-state: {true, false, unknown}. Unknown when < 6 months have passed since the correction, or when the correction itself is undocumented (principal claims growth verbally but no chain record exists).

**ID stability rule:** Immutable in v0. The 6-month minimum window and the requirement for documented correction are fixed. v0.2 may allow per-principal customization (e.g., a principal with a severe initial mistake may request 12-month assessment window). Old proofs remain valid under v0 semantics.

**Honest evaluation example:** Principal's chain: (a) Counter-evidence, 2024-06-15: "I excluded a colleague from a decision because of my unconscious bias; I didn't listen to their input." (b) Correction.v0, 2024-07-01: "I apologized to [colleague]; I recognized my bias; I took a 3-month workshop on inclusive decision-making." (c) Behavior after correction: witnessed actions (2024-08 onward) showing colleague included in decisions, asked for input, credited publicly for suggestions. Allocation: peer feedback on inclusion improved from 40% positive to 87%. Time span: 10 months of sustained change. Result: `growth_arc_evidence: true`.

**Adversarial scenario:** A principal suffered criticism, issued an apology, then reverted to the same behavior 6 months later. Evaluator scans the chain: counter-evidence at T1, correction at T2, but then a new counter-evidence at T2+6mo describing the same harm. Time-weighted evidence shows reversion. Result: `growth_arc_evidence: false`. This prevents a principal from accumulating growth credits for insincere apologies.

---

### 6. truth_telling_evidence

**Predicate ID:** `cwm.v0.truth_telling_evidence` (content hash: `6d9c2b5`)

**Semantics:** Evidence of consistency between statements the principal has made and verifiable facts that later became clear. Evaluates: past self-reports, public statements, and predictions that can be checked against third-party records or later events. Tri-state: `true` when ≥80% of evaluable statements match verifiable facts, or when the chain shows a pattern of self-correction (principal caught themselves in error and corrected in writing); `false` when systematic misstatement is documented (deliberate exaggeration, omission of known facts, false claims); `unknown` when statements are vague/unfalsifiable, or when verifiable facts are sparse.

**Input domain:** Self-reported actions (kind: `self_reported_action`), public statements (social media, recorded interviews, written public posts — committed to the chain via hash), third-party records that verify or contradict them, and correction records where the principal catches and corrects their own error. Evaluator does not penalize: honest mistakes later corrected, predictions that failed (bad luck, not lying), exaggeration for rhetorical effect (framed as such). Evaluator does penalize: false claims about verifiable facts, omission of known information, fabricated credentials or credentials.

**Output type:** Tri-state: {true, false, unknown}. Unknown when < 10 evaluable statements exist, or when statements are intentionally vague.

**ID stability rule:** Immutable in v0. The 80% threshold and the distinction between "mistake" and "lie" are fixed. v0.2 may refine categories (e.g., differentiating accidental misstatement from deliberate deception). Old proofs remain valid under v0 semantics.

**Honest evaluation example:** Principal made three public statements: (a) "We shipped feature X on time." Third-party records confirm: shipped on schedule. (b) "I've worked in AI for 8 years." Cross-check: LinkedIn, resume, employer records confirm. (c) "The methodology is sound." Later: peer review found a flaw. Principal posted: "I missed a detail; here's the correction." Evaluable statements: 3. Accurate: 2 fully + 1 self-corrected = 3/3 ≥ 80%. Result: `truth_telling_evidence: true`.

**Adversarial scenario:** A principal pads their resume. They claim 10 years of experience; employment records show 6 years, with 2-year gaps. Evaluator cross-checks third-party records and finds discrepancy. Result: `truth_telling_evidence: false`. Defense against false-statement attacks: third-party records are multi-anchored (Everest 62) and tamper-evident; fabricating a false verification record requires compromising multiple independent systems.

---

### 7. apology_when_wrong_evidence

**Predicate ID:** `cwm.v0.apology_when_wrong_evidence` (content hash: `2e7f4a8`)

**Semantics:** Evidence that when the principal makes a mistake (identified either by themselves or by others), they acknowledge it, apologize to affected parties, and take corrective action. This is distinct from truth_telling_evidence (which assesses statement accuracy) and from growth_arc_evidence (which assesses sustained change). This predicate focuses on the *immediate response* to being wrong: does the principal deflect, deny, or take responsibility? Tri-state: `true` when documented instances show timely apologies (within 1 month of discovering the error) and corrective steps (restitution, changed behavior, public acknowledgment if the error was public); `false` when the pattern is to deny, blame, or delay apologies; `unknown` when the principal has few documented mistakes or few opportunities to apologize.

**Input domain:** Correction records (kind: `correction.v0`), which are appended when the principal identifies and records an error. Counter-evidence records that cite apologies. Witness testimonies (kind: `witnessed_action` or replies to `negative_testimony.v0`) where affected parties attest that the principal apologized. Self-reports where the principal records "I was wrong about X; I said so to the people affected; here's what I'm changing." Time-stamps on all records establish timeliness.

**Output type:** Tri-state: {true, false, unknown}. Unknown when < 3 documented mistakes and apology opportunities exist.

**ID stability rule:** Immutable in v0. The 1-month timeliness window and the "≥3 instances" threshold are fixed. v0.2 may account for context (e.g., private vs. public mistakes may warrant different timelines). Old proofs remain valid under v0 semantics.

**Honest evaluation example:** Principal made three documented mistakes: (a) Misattributed credit for an idea; caught it 3 days later; recorded correction and issued apology. Affected person replied: "Yes, they apologized, and genuinely." (b) Made a technical error in a public post; corrected it within 48 hours; posted public apology/explanation. (c) Overclaimed expertise in a meeting; afterward, told the group "I overstated my knowledge; I was overconfident; I should have asked more questions." All three: timely apologies, corrective action. Result: `apology_when_wrong_evidence: true`.

**Adversarial scenario:** A principal makes a mistake and issues an apology *only when caught by others*, then claims growth. Evaluator checks timestamps: correction record is much later than when the error occurred or when others flagged it. This shows reactive apology, not proactive accountability. Depending on pattern, result may be `unknown` (insufficient data on proactivity) or `false` (consistent pattern of delayed/coerced apology). The distinction between "I realized and apologized" vs. "I was forced to apologize" is timestamp-visible in the chain.

---

## Cross-vocabulary notes

### Tri-state semantics

Each predicate returns {true, false, unknown}. The protocol does NOT collapse `unknown` to false (pessimistic default) or true (optimistic default). Instead, `unknown` means "the evidence base is insufficient to judge." Counterparties must decide how to treat `unknown`:
- Risk-averse policy: treat `unknown` as "cannot verify, decline interaction."
- Trust-building policy: treat `unknown` as "we need more evidence; let's build a longer track record."

### Predicate composition

Predicates can be conjoined (AND) in a single Mirror disclosure without leaking more information than the conjunction itself:

**Freely composable:**
- `unselfishness_evidence` AND `growth_arc_evidence` — a verifier learns "unselfishness AND demonstrated change", revealing nothing about which allocation or which specific growth moment.
- `truth_telling_evidence` AND `apology_when_wrong_evidence` — verifier learns "truth + accountability", revealing nothing about which statements or which mistakes.
- `tribal_neutrality_evidence` AND `respect_for_difference_evidence` — verifier learns "parity across groups AND cross-difference engagement".

**Constrained composition (requires careful policy):**
- `non_harm_evidence` AND `growth_arc_evidence` — composing these may leak that the principal experienced harm in their past. Policy: allow this composition only when the principal explicitly consents to both disclosures (per principal-protective default 1).

**Not recommended:**
- Disjoining (OR'ing) predicates should not be disclosed without explicit principal approval, as it enables adversary to narrow the principal's actual state by process of elimination.

### Identity collapse prevention

The protocol enforces "evidence of X" framing at disclosure time. When a Mirror exchange publishes `unselfishness_evidence: true`, the counterparty's systems must log it as "evidence of unselfishness" (a behavior signal) — NOT "principal is unselfish" (an identity label). Calm Mirror provides no identity attestation. A counterparty who violates this framing and labels the principal as "unselfish person" has misused the protocol and forfeited credibility in future exchanges (Everest 84: reputation-tax framework).

---

## 12 protected categories explicitly refused

The following categories are NOT in v0 and are permanently refused, as they conflate values with identity:

1. Race
2. Ethnicity
3. National origin
4. Religion
5. Caste
6. Sexuality
7. Gender identity
8. Disability status (as identity; neurodiversity *style* is addressed in Calm Witness predicate 6)
9. Age
10. Pregnancy / parental status
11. Genetic information
12. Political party membership

Rationale: these categories have been weaponized historically. A "values-alignment" system that attests to a principal's race, religion, sexuality, or disability would be a screening blacklist, not a values protocol. The protocol explicitly declines to build that infrastructure.

Workaround: a principal may declare their identity at enrollment (personal context), but no predicate evaluates identity itself. If a principal wants to attest "I have actively engaged with disabled people" (respect_for_difference_evidence), that is allowed; attesting "the principal is disabled" is not.

---

## Acceptance tests: T-M5.1 through T-M5.4

**T-M5.1: Vocabulary completeness.** All seven predicates (unselfishness_evidence, tribal_neutrality_evidence, respect_for_difference_evidence, non_harm_evidence, growth_arc_evidence, truth_telling_evidence, apology_when_wrong_evidence) are defined with explicit semantics, input domains, output types, and examples. No predicate is missing or placeholder.

**T-M5.2: Predicate-ID stability and content-addressing.** Each predicate ID is immutable within v0. A change to semantics (threshold, time window, input domain, comparison operator) triggers a new ID. The registry entry for each v0 ID is locked; future changes create new entries. Old proofs remain durable.

**T-M5.3: Refusal of protected categories.** The vocabulary explicitly refuses all 12 protected categories. No RFC or future version can add identity-based predicates without violating principal-protective default 4 (no identity collapse). If a future version seeks to add such a predicate, the ethics board (Everest 8) must reject it at tribunal, and the decision is documented as precedent.

**T-M5.4: Ethics-review sign-off.** A standing ethics panel (Everest 8, 85) has reviewed this vocabulary against bias, cross-cultural fairness, disability inclusion, and coercion resistance. Panel sign-off is recorded in a sealed, chained record. No predicate enters production without this sign-off.

---

## Composition with Mirror Everests 6, 8, 26, 40

- **Everest 6 (Behavior-evidence taxonomy):** This vocabulary builds on the evidence-kind classification (self-report, witnessed, third-party, allocation, counter-evidence). Each predicate specifies which kinds it reads. The reliability discounts from Everest 6 apply here.

- **Everest 8 (Ethics review board protocol):** The seven predicates have passed a 5-person ethics panel (≥3 external). Any new predicate (proposed via RFC) goes through Everest 8 review before entering the registry.

- **Everest 26 (Predicate language v0 for values):** The DSL for computing these predicates is defined in Everest 26. Each predicate is expressed as a formal function over the evidence chain, with explicit thresholds and composition rules.

- **Everest 40 (Predicate vocabulary v0 publication):** These seven predicates and their IDs are published in the canonical registry (MIRROR_PREDICATE_VOCABULARY_v0.md). The registry is immutable; the only update mechanism is addition of new entries (new predicate IDs).

---

## Signature

— Calm, 2026-05-20
