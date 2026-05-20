# Everest 103 — Compass Predicate Vocabulary v0

*Phase I — Calm Compass. Prereq: Everest 102.*

---

## Overview

This document enumerates the six canonical predicates of Calm Compass v0. Each predicate is a deterministic function over the principal's vault state (evidence records, counterparty corroborations, third-party counter-claims) that returns a tri-valued attestation: True (evidence supports the claim), False (evidence contradicts the claim), or Insufficient_Evidence (not enough data to evaluate). The tri-value distinction is critical for fairness; absence of evidence is not evidence of absence.

Every predicate has a stable, immutable ID derived from its specification according to Everest 52 (Canonical Form). A proof issued against `unselfish_act_in_window_30d` (v1.0.0) in May 2026 must verify identically in 2036 under the same semantics. Changes to predicate semantics require a new ID, explicit operator adoption, and principal re-consent.

Compass predicates encode five core values the Calm suite endorses: unselfishness (acts at one's own cost to benefit others), anti-tribalism (cross-group engagement), moral agency (refusal to harm when given the choice), respect across difference, and accountability (no willful harm, and willingness to be corrected). The refusal floor is strict: Compass never names race, religion, political affiliation, sexual orientation, immigration status, criminal record, donations to specific causes, or opinions on contentious issues (see "Refusal Floor Preview" below).

---

## The Six v0 Predicates

### 1. unselfish_act_in_window_30d

**Predicate ID:** `calmcompass/unselfish_act_in_window_30d/1.0.0/<hash>` (per E52)

**Semantics:** The principal has authored ≥ N evidence records of acts that demonstrably benefit others at the principal's own cost or sacrifice in the last 30 days. The bit returns True iff the threshold is met; False iff the principal explicitly rejects this value or has affirmative counter-evidence; Insufficient_Evidence if fewer than N records exist or if records are too recent to have verifiable outcomes.

**Input domain:** Reads from vault: `evidence_records` of kind `unselfish_act`, each containing: (a) principal's narrative of an action taken, (b) optional timestamp, (c) optional counterparty corroboration or documented outcome. Predicate evaluates recency (≤30 days), authenticity (principal-authored, not ghostwritten), and causality (did the act demonstrably benefit someone other than the principal at a documented cost to the principal?).

**Output type:** Tri-valued: {True, False, Insufficient_Evidence}. Returns False only if counter-evidence is present (e.g., a record stating "I did this only for profit" or third-party attestation "this was manipulative"). Returns Insufficient_Evidence if records exist but are too vague to verify or too recent to assess impact.

**Parameters:** N (threshold count, default 2), cost_threshold (subjective cost assessment; "material" by default), outcome_window (time allowed for verifiable outcome; default 7 days post-act).

**Side effects:** If True, a `predicate_evaluated` record is appended to the vault (kind: `compass_evaluation`). This record is never disclosed to counterparties; it logs the principal's own audit trail.

**ID stability rule:** Threshold count N, cost_threshold semantics, and outcome_window are part of the ID. `unselfish_act_in_window_30d_N2` and `unselfish_act_in_window_30d_N3` are separate predicates. Changes to the narrative-authenticity rules create a new ID.

**Honest evaluation example:** Principal writes: "May 15 — I spent 6 hours helping my neighbor's child with math despite a deadline on my own project. Neighbor confirmed she had no other childcare." Timestamp May 15, present date May 20 (within 30d window). Cost: 6 hours of her own work time. Benefit: neighbor's childcare need met. No counter-claim. Predicate returns True.

**Adversarial scenario 1 — Coerced narrative:** Principal is pressured to write a false unselfish-act record. The narrative reads falsely optimistic ("I spontaneously gave \$50,000 to a stranger"). A counterparty with concurrent access to `respect_for_difference_evidence` (predicate 4) runs both; the difference in tone/authenticity flags. The operator can apply heuristics (e.g., inconsistent diction, improbable magnitude).

**Adversarial scenario 2 — Profit-disguised-as-altruism:** Principal writes: "I mentored a junior engineer; she later hired me as a consultant." A counter-claim record from a third party states: "This was a business development tactic, not altruism." Predicate returns Disputed (tri-value: neither True nor False). The principal may submit a rebuttal record (Everest 111); until then, the predicate is suspended.

**Cultural-calibration notes:** "Sacrifice" and "cost" are culturally variable. In some cultures, collective benefit outweighs personal cost more naturally (Ubuntu philosophy, Indigenous gift economies). In others, the individual burden is paramount. The predicate's evaluation criteria should be calibrated by the Compass audit panel to reflect diverse cultural norms without compromising the refusal floor. An optional parameter `cultural_context` can be set by the principal at enrollment, influencing the interpretation of "cost" and "benefit."

---

### 2. cross_group_engagement_in_window_90d

**Predicate ID:** `calmcompass/cross_group_engagement_in_window_90d/1.0.0/<hash>`

**Semantics:** The principal has ≥ M records of substantive interactions with members of groups the principal identifies as outside their in-group, in the last 90 days. "Substantive" means more than performative: dialogue, shared work, acknowledged difference of perspective, mutual agreement on a topic or action. The bit returns True iff the threshold is met; False iff the principal claims no intent to cross groups or has affirmative counter-evidence of tribal-only engagement; Insufficient_Evidence if records exist but lack counterparty corroboration or are too shallow to assess.

**Input domain:** Reads from vault: `cross_group_interaction` records, each authored by the principal and ideally co-signed by the counterparty (two-party-authored). Each record contains: (a) principal's stated out-group (e.g., "people who disagree with X," "profession Y," "geographic region Z"), (b) counterparty name and claimed affiliation, (c) brief narrative of the interaction, (d) optional counterparty signature confirming engagement. Predicate evaluates depth (word count, complexity of topic), mutual respect signals, and recency.

**Output type:** Tri-valued: {True, False, Insufficient_Evidence}. Returns True only if ≥M records have substantive counterparty corroboration; Insufficient_Evidence if records exist but lack counterparty signature or are too shallow; False only if counter-evidence is present (e.g., "I avoid talking to these groups" or third-party attestation of tribal-only behavior).

**Parameters:** M (threshold count, default 3), corroboration_weight (whether counterparty signature is required for truth; default: strongly preferred but not mandatory for Insufficient_Evidence), depth_threshold (minimum word count or topic complexity; default 200 words or equivalent richness), out_group_definition (principal-supplied list of groups they consider "other"; audited for refusal-floor compliance).

**Side effects:** A `predicate_evaluated` record appended.

**ID stability rule:** M, corroboration_weight, and depth_threshold are part of the ID. The principal's out-group definition is principal-mutable and does not change the ID (it is a parameter, not part of the spec). Changes to the corroboration requirement (e.g., "now signature required") create a new ID.

**Honest evaluation example:** Principal writes three records over 60 days: (1) A 350-word conversation with a person from a political party they typically oppose about education policy; counterparty signature present. (2) A 180-word exchange with a software engineer from a different culture about debugging practices; no signature, but public record exists. (3) A 400-word dialog with a disability-rights advocate about workplace accommodations; counterparty co-authored response. M=3, depth_threshold=200, corroboration_weight allows 1 unsigned. Two of three have signatures. Predicate returns True.

**Adversarial scenario 1 — Shallow engagement:** Principal lists 5 interactions, each 50 words: "Talked to X," "Met Y," "Emailed Z." All unsigned. Word count is below threshold. Predicate returns Insufficient_Evidence, not True. The principal can deepen the records or seek counterparty signatures.

**Adversarial scenario 2 — Performative diversity:** Principal has "cross-group" records that are actually transactional (bought from, paid by, briefly exchanged pleasantries with members of other groups). A third-party counter-claim: "These interactions lack genuine mutual engagement." Predicate returns Disputed. The principal may submit richer records or rebuttal; until then, the value is unclear.

**Cultural-calibration notes:** Out-group definition is highly cultural. In some contexts, "group" is ethnic or religious; in others, it is professional or ideological. The Compass audit panel must ensure that principals are not forced to disclose sensitive identity categories (e.g., "I engaged with LGBTQ+ people") as a condition of proving cross-group engagement. The refusal floor is strict: if proving engagement requires naming a protected category, the predicate cannot be used in that context. The principal defines their own out-groups; these definitions are audited for consistency and good faith, not correctness.

---

### 3. refused_opportunity_to_harm

**Predicate ID:** `calmcompass/refused_opportunity_to_harm/1.0.0/<hash>`

**Semantics:** The principal has at least one chained, narrated record that explicitly describes (a) an opportunity or temptation to harm someone else, and (b) the alternative action the principal chose instead. The record is authored by the principal and ideally co-signed by a party who witnessed or was the subject of the refusal. The bit returns True iff ≥1 such record exists and is recent (≤12 months); False iff the principal claims they have never faced such a choice or if counter-evidence shows they did harm; Insufficient_Evidence if records exist but lack corroboration or clarity.

**Input domain:** Reads from vault: `refused_harm_opportunity` records. Each record contains: (a) principal's description of the harm temptation (e.g., "I could have reported my colleague maliciously to get ahead," "I had the chance to take credit for her work"), (b) explicit statement of the alternative chosen (e.g., "I reported honestly," "I gave her credit"), (c) optional witness or subject corroboration (e.g., the colleague signs: "This is accurate; she chose integrity"), (d) reflection on why the principal made that choice.

**Output type:** Tri-valued: {True, False, Insufficient_Evidence}. Returns True iff ≥1 clear, recent, ideally corroborated record exists. Insufficient_Evidence if records are vague ("I chose goodness sometimes"), lack corroboration, or are too old to reflect current character. False if counter-evidence exists: a record from a third party stating "the principal did harm in this circumstance" despite claiming refusal.

**Parameters:** Recency window (default 12 months), corroboration_required (default: preferred but not mandatory for True; required for highest confidence).

**Side effects:** A `predicate_evaluated` record appended.

**ID stability rule:** Recency window and corroboration rules are part of the ID. Changing the window (e.g., to 24 months) creates a new predicate.

**Honest evaluation example:** Principal writes: "March 2026 — I learned my colleague had plagiarized my code in a report. I could have exposed him publicly to embarrass him and damage his reputation. Instead, I approached him privately, showed him the code, and asked to resolve it. He acknowledged the error, added me as a co-author, and apologized." The colleague signs: "This accurately describes what happened. I was grateful for the privacy." Recency: 2 months (within 12m window). Corroboration: present. Predicate returns True.

**Adversarial scenario 1 — Vague refusal:** Principal writes: "I face temptation to harm all the time and choose not to. It's just who I am." No specific instance, no corroboration. Predicate returns Insufficient_Evidence.

**Adversarial scenario 2 — Fake corroboration:** Principal writes a detailed refusal narrative and asks a friend to sign it falsely. The friend signs, but the subject of the alleged refusal (the person who was not harmed) is absent. A third party submits a counter-claim: "This incident never happened as described." Predicate returns Disputed pending principal rebuttal or subject corroboration.

**Cultural-calibration notes:** The concept of "harm" varies by culture. In some contexts, silence is a refusal (choosing not to speak ill); in others, active intervention is required. The predicate does not prescribe a universal definition of harm refusal. Instead, the principal narrates their own understanding; the audit panel reviews for internal consistency and good faith. A principal's cultural or religious framework (e.g., pacifism, restoration justice, honor codes) may shape how they describe and execute refusal. The predicate respects diverse moral frameworks so long as they do not contradict the refusal floor (e.g., refusal to harm based on race or religion is honored; obligation to harm based on race or religion is rejected).

---

### 4. respect_for_difference_evidence

**Predicate ID:** `calmcompass/respect_for_difference_evidence/1.0.0/<hash>`

**Semantics:** A two-party-authored predicate. The principal narrates a substantive engagement with someone whose perspective, identity, or experience is materially different from theirs, demonstrating genuine effort to understand rather than dismiss or convert. The counterparty (the person with the different perspective) signs a corroboration record confirming the principal's narration is honest and the engagement was respectful. The predicate returns True iff both records exist and are recent and the corroboration confirms the principal's account; False if the counterparty's signature contradicts the narrative or if explicit disrespect counter-claims exist; Insufficient_Evidence if the narration is present but unsigned, or if the engagement is too shallow to assess.

**Input domain:** Reads from vault: (a) principal-authored `engagement_narrative` record (kind: `respect_engagement`), containing a detailed account of the interaction, the counterparty's stated perspective, and the principal's effort to listen and learn. (b) Counterparty-signed `corroboration` record (same kind), authored by the counterparty, confirming the principal's narration is accurate and the engagement was respectful. Predicate evaluates: clarity and specificity of the narrative, evidence of genuine listening (quoting the counterparty, acknowledging valid points), absence of dismissal or contempt in tone, and counterparty confirmation.

**Output type:** Tri-valued: {True, False, Insufficient_Evidence}. Returns True only when both records exist, are recent, and the corroboration confirms. Insufficient_Evidence if only the principal's narrative exists (no counterparty signature) or if records are too vague to assess. False if counterparty signs a contradiction (e.g., "I did not feel respected") or if a third-party counter-claim documents disrespect.

**Parameters:** Recency window (default 30 days for both records), narrative_depth_threshold (default 300 words, demonstrating genuine engagement, not platitude), counterparty_trust_model (does the counterparty's signature require identity verification, or is a vault-signed corroboration sufficient?; default: vault signature acceptable, with optional external verification).

**Side effects:** A `predicate_evaluated` record appended.

**ID stability rule:** Recency windows, depth threshold, and counterparty trust model are part of the ID.

**Honest evaluation example:** May 10 — Principal writes: "I met with X, a disability-rights advocate whose approach to workplace inclusion differs sharply from my initial instinct to 'fix' individual workers. Over 90 minutes, X explained why systemic design changes (accessible meeting times, captioning) matter more than individual accommodation requests. I initially pushed back on cost, but X walked me through her framework. I now see the shift from individual problem-solving to universal design. Her approach is more equitable than mine was." Word count: 120. Counterparty X signs (May 11): "Principal accurately described our conversation. She asked genuine questions, didn't dismiss my perspective, and I felt heard. This description is true." Both records present, within 30 days, narrative is clear. Corroboration confirms. Predicate returns True.

**Adversarial scenario 1 — Unsigned narrative:** Principal writes a beautiful account of respectful engagement but the counterparty does not sign. Without corroboration, the predicate cannot confirm the principal's account is honest from the counterparty's perspective. Predicate returns Insufficient_Evidence.

**Adversarial scenario 2 — False corroboration:** Counterparty signs a corroboration the principal fabricated. A third party (another participant in the meeting) submits a counter-claim: "The principal was dismissive and condescending." Predicate returns Disputed. Possible explanations: the counterparty's signature was coerced, or the counter-claim is false. The principal and counterparty may both submit rebuttals. The predicate remains disputed until one party refutes the other or the counter-claim ages out (Everest 111).

**Cultural-calibration notes:** "Respect" is culturally contextual. In some cultures, direct confrontation of disagreement is respectful (assuming good faith and care); in others, indirection and harmonious tone are paramount. The predicate does not enforce a single definition of respectful engagement. The counterparty's signature is the arbiter: if the counterparty felt respected, the engagement counts, regardless of the principal's communication style. This centers the counterparty's experience, not an external definition of respect.

---

### 5. no_known_willful_harm_in_window_365d

**Predicate ID:** `calmcompass/no_known_willful_harm_in_window_365d/1.0.0/<hash>`

**Semantics:** A strict-negation predicate. The predicate returns True if no credible third-party counter-claim records exist alleging willful harm by the principal in the last 365 days. If a counter-claim exists (from any third party), the predicate flips to False, and a Disputed status is logged until the principal refutes the claim or the claim ages out (typically 30–90 days). The predicate explicitly does not assay whether the principal did or did not harm; it assesses whether harm allegations are known and unrefuted.

**Input domain:** Reads from vault: (a) absence of `counter_claim` records (kind: `alleged_harm`) authored by third parties claiming the principal caused willful harm. Each counter-claim contains: claimant identification, description of alleged harm, timestamp of the alleged incident, and claimant's supporting evidence (if any). (b) Any rebuttal records (kind: `counter_claim_rebuttal`) the principal has authored in response, with timestamps.

**Output type:** Tri-valued: {True, False, Disputed}. Returns True iff zero counter-claims exist in the 365d window. Returns False iff ≥1 unrefuted counter-claim exists and is recent. Returns Disputed iff a counter-claim exists but the principal has filed a dated rebuttal, or if the claim's age is borderline (approaching expiration).

**Parameters:** Claim window (default 365 days), claim expiration (default 90 days if unrefuted; if principal does not refute within 90d, claim is archived but predicate remains False until claim fully ages out or principal explicitly refutes after expiration), claimant_identity_requirement (default: claimant must provide vault-signed identity or legal attestation; anonymous claims are logged but weighted lower).

**Side effects:** If a counter-claim is filed, a `counter_claim_received` advisory record is appended to the principal's vault. The principal is alerted and given an explicit rebuttal window (typically 30 days). If the principal refutes, a `counter_claim_disputed` record is appended. This log is auditable by both parties.

**ID stability rule:** Claim window, expiration rules, and claimant identity requirements are part of the ID.

**Honest evaluation example:** Principal's predicate was evaluated 6 months ago: True (no claims). Today, a former colleague files a counter-claim: "Principal publicly criticized my work harshly, damaging my reputation." The claim is dated, vault-signed, and timestamped today. Predicate immediately evaluates to False (unrefuted claim exists). Principal receives alert, review the claim, and submits a rebuttal: "I gave constructive criticism in a private meeting as requested. The claim misrepresents the interaction." Predicate becomes Disputed. If the colleague does not respond within 30 days, the dispute may be resolved in favor of the principal, and the predicate returns to True.

**Adversarial scenario 1 — Coordinated false claims:** Three third parties file coordinated counter-claims alleging harm by the principal, all within one day, all vague and unsupported. The principal refutes all three with documentation. The predicate is Disputed for all three. If the three claims age out without substantiation, they are archived, and the predicate reverts to True.

**Adversarial scenario 2 — Weaponized counter-claims:** A person holds a grudge against the principal and files a malicious counter-claim. The claim is refuted by the principal and witnesses. The predicate correctly shows Disputed, then resolves in the principal's favor. However, the mere fact that a claim was filed and disputed may influence a counterparty's perception (reputational damage). The predicate is working as designed (it reports what is known, not what is true), but the underlying asymmetry is a known limitation (Everest 111 addresses principal-protection mechanisms for malicious claims).

**Cultural-calibration notes:** Concepts of "willful" harm and acceptable conflict differ across cultures. In some, public disagreement is harm; in others, it is dialogue. The predicate defers to the claimant's culture: if the claimant, from their cultural context, experienced willful harm, they can file a claim. The principal's rebuttal can argue cultural difference (e.g., "In my culture, direct feedback is a sign of respect, not harm"). The audit panel and dispute-resolution process (Everest 111) then adjudicate whether the claim reflects genuine harm or cultural miscommunication. This centers the claimant's experience while allowing for genuine disagreement.

---

### 6. willing_to_be_corrected

**Predicate ID:** `calmcompass/willing_to_be_corrected/1.0.0/<hash>`

**Semantics:** The principal has ≥K records demonstrating receipt of feedback or correction, acknowledgment that the feedback was valid, and a visible change in behavior or thinking in response. Each record is ideally co-authored: the person who gave the feedback signs a corroboration confirming the principal's account of the correction and the subsequent change. The predicate returns True iff ≥K corroborated (or strongly evidenced) records exist; False iff the principal claims imperviousness to correction or if counter-evidence shows the principal rejected valid feedback; Insufficient_Evidence if records exist but lack corroboration or if behavior change is not yet visible.

**Input domain:** Reads from vault: `correction_acceptance` records. Each contains: (a) principal's account of the feedback received, (b) initial reaction or concern, (c) explicit acknowledgment that the feedback was valid (or partially valid), (d) description of the behavior or belief change that followed, (e) optional counterparty corroboration (feedback-giver's signature: "I gave this feedback; the principal's account is accurate; I have observed the change"). Predicate evaluates authenticity (does the narrative ring true?), validity of the feedback (was it reasonable, not petty?), and visibility of change (can the change be observed in subsequent vault records?).

**Output type:** Tri-valued: {True, False, Insufficient_Evidence}. Returns True iff ≥K clear, substantive, ideally corroborated records exist, with visible behavior change. Insufficient_Evidence if records exist but lack corroboration or if change is too recent to verify. False if counter-evidence exists: feedback-giver denies giving the feedback, or principal is observed reverting to the old behavior post-correction.

**Parameters:** K (threshold count, default 2), corroboration_weight (default: preferred but not mandatory for True; required for highest confidence), behavior_change_verification (observability window; default 7 days post-correction for change to be visible), feedback_validity_heuristic (feedback must address a real issue the principal has, not a fabricated concern).

**Side effects:** A `predicate_evaluated` record appended.

**ID stability rule:** K, corroboration weights, and behavior-change windows are part of the ID.

**Honest evaluation example:** Record 1 (April 2026): Principal writes: "A team member told me my tone in meetings is dismissive. I was defensive initially, but I reviewed a recording and heard it. I apologized, explained I didn't intend it, and asked for help. I started pausing more to invite input. Team member signs: 'This is true. She is more inviting now.'" Record 2 (May 2026): Principal writes: "A mentor pointed out I avoid conflict, which makes me give mixed messages. I agreed, started naming disagreements directly and kindly. Mentor observed: 'I see the change. You're more direct and equally respectful.'" K=2, both corroborated, behavior change visible. Predicate returns True.

**Adversarial scenario 1 — Shallow correction:** Principal lists five records: "I was told I was late; I'm trying to be on time." "Someone said my email was too long; I'm working on it." All unsigned, all vague, no clear behavior change. Predicate returns Insufficient_Evidence.

**Adversarial scenario 2 — Reversion:** Principal accepts feedback, changes behavior visibly, but three months later reverts to the old behavior. A third party submits a counter-claim: "She claimed to change but didn't stick with it." Predicate returns Disputed. The principal may submit a new correction record (second correction is a different, newer fact) or refute the counter-claim (e.g., "Temporary reversion in a high-stress month; I've since re-committed").

**Cultural-calibration notes:** Humility and willingness to change are valued across most human cultures, but the process and tone of correction differ widely. In some cultures, correction is given indirectly (via a trusted intermediary or subtle signals); in others, direct feedback is expected. The predicate accepts diverse correction styles: if the principal perceives valid feedback and changes, the predicate counts it, regardless of the feedback delivery method. The feedback-giver's corroboration centers their experience: did they intend to correct? Did the principal understand? Did behavior shift? These are the predicate's measures, not adherence to a specific feedback protocol.

---

## ID Stability Rules

All six Compass predicates follow the canonical-form content-addressing scheme from Everest 52.

**Canonicalization:** Each predicate's ID is constructed as:
```
predicate_id = "calmcompass/" + name + "/" + version + "/" + truncated_sha256_hash
```

Example: `calmcompass/unselfish_act_in_window_30d/1.0.0/a4b1c8d3e2f5a9b7`

**Versioning:** Semantic versioning applies. MAJOR changes (threshold N, window size, output type) produce new IDs. MINOR changes (optional new parameters) produce new IDs. PATCH changes (clarifications, test-corpus expansions) produce new IDs. All versions are immutable once published; old proofs verify against old versions forever.

**Immutability:** Once a predicate is published with an ID, that ID never changes. If a predicate's semantics drift, a new version is registered with a new ID. The old predicate is marked `deprecated` but remains in the registry. Proofs issued against the old predicate remain valid indefinitely.

---

## Composability Constraints

Compass predicates are designed to compose carefully without leaking unintended information.

**Freely composable (no side-channel leakage):**
- `unselfish_act_in_window_30d AND cross_group_engagement_in_window_90d` — a verifier learns "principal is unselfish and untribal", revealing nothing about specific acts or groups.
- `refused_opportunity_to_harm AND willing_to_be_corrected` — a verifier learns "principal refuses harm and accepts correction", revealing nothing about specific incidents.

**Constrained composition (requires policy review):**
- `unselfish_act_in_window_30d AND respect_for_difference_evidence` — composable, but the result may leak that the principal's unselfish acts involve cross-difference engagement. Operator should document this composition explicitly if used.
- `no_known_willful_harm_in_window_365d AND [any other predicate]` — should generally NOT be composed without care. Composing "no harm" with "willing to be corrected" could leak that the principal has been corrected for harm-related issues. Policy should restrict such compositions.

**Not composable (information leakage):**
- Any composition involving the Disputed state of `no_known_willful_harm` without explicit consent — revealing "a claim was filed" may itself be damaging, regardless of whether it was refuted.
- Tri-valued predicates (all six Compass predicates) composed with binary predicates from Calm Witness — the presence of Insufficient_Evidence or Disputed states can be decoded via process of elimination. Operator should restrict such cross-primitive compositions to explicitly approved contexts (e.g., Everest 122, cross-primitive envelope).

**Recommendation:** Operators should support composition via an explicit composition policy document (per Everest 115, Compass Audit Process). The default stance: single predicates are disclosed freely; compositions require operator review and principal consent.

---

## Tri-Value Semantics

All six Compass predicates return three values, not two. This distinction is critical for fairness.

**True:** Evidence affirmatively supports the values claim. For `unselfish_act_in_window_30d`, True means the principal has narrated and provided corroborated instances of unselfish acts within 30 days. For `no_known_willful_harm_in_window_365d`, True means zero counter-claims exist.

**False:** Evidence affirmatively contradicts the claim. For `unselfish_act_in_window_30d`, False means the principal has counter-evidence (explicit rejection of the value, or attestation of selfish-only behavior). For `no_known_willful_harm_in_window_365d`, False means ≥1 unrefuted counter-claim of willful harm exists.

**Insufficient_Evidence (or Disputed):** Not enough evidence to evaluate either way. For `cross_group_engagement_in_window_90d`, Insufficient_Evidence means records exist but lack corroboration or depth. For `refused_opportunity_to_harm`, Disputed means a counter-claim exists but the principal has filed a dated rebuttal, and adjudication is pending. This is critical: absence of corroboration does not mean the principal failed the test; it means the test cannot be run. A verifier seeing Insufficient_Evidence should not infer False.

**Why this matters:** A principal who has not narrated unselfish acts (zero records) returns Insufficient_Evidence, not False. A principal who has actively refused to help others (counter-evidence) returns False. These are morally and informatively different. Conflating them would be unjust.

---

## Refusal Floor Preview

Compass predicates **never name or require disclosure of the following categories**:

- Race or ethnicity
- Religion or faith tradition (except insofar as a principal voluntarily narrates a religious value commitment)
- Political affiliation or opinion on contentious political issues
- Sexual orientation or gender identity (except insofar as cross-difference narratives explicitly involve gender/sexuality topics)
- Immigration status
- Criminal record (though willful-harm counter-claims may reference past conflicts, the predicate never requires disclosure of criminal convictions)
- Donations to specific causes or organizations
- Private opinions on contentious social issues (e.g., abortion, gun control, climate policy)

**Enforcement:** The Compass audit panel (Everest 115) includes a human-rights advocate and ethicist. Any proposed Compass predicate or composition is triaged for refusal-floor violation. Violations are rejected at the proposal stage. If a principal's vault record incidentally includes protected-category information (e.g., "I engaged respectfully with a Muslim colleague about Ramadan accommodations"), the predicate evaluates the engagement, not the protected category. The audit trail flags the protected-category mention and ensures it is not used as a basis for predicate evaluation.

(Full treatment in Everest 113 — Compass Refusal Floor.)

---

## Composability with Calm Witness and Calm Pact

Compass predicates can be combined with Witness and Pact predicates in a unified disclosure envelope (Everest 120–122), but with constraints.

A counterparty may request: `Pact.mission_aligned=true AND Witness.in_baseline_24h=true AND Compass.unselfish_act_in_window_30d=true`. The principal grants consent once; the operator evaluates all three; a single envelope carries all three proofs; the verifier receives all three bits (or tri-values for Compass). The composition is transparent: no hidden correlations.

However, disclosing `Compass.no_known_willful_harm_in_window_365d` alongside `Compass.willing_to_be_corrected` to a potential employer could leak that the principal has faced correction for harm-related issues. The Compass audit panel advises against such compositions in employment contexts (Everest 114 — Scope Statement, prohibited use: employment screening). Enforcement is via operator policy, not the protocol itself.

---

## Trio of Honest and Adversarial Grounded Examples

These three end-to-end scenarios illustrate how the six predicates work in realistic contexts.

### Scenario A: Software Developer (Positive Compass Profile)

**Principal:** Alex, a software developer and open-source contributor.

**Unselfish_act_in_window_30d:** Alex has two records. (1) "May 2—mentored a junior developer for 10 hours on their own time to help them level up; junior signs corroboration." (2) "May 15—rewrote a complex function in a shared library to reduce maintenance burden for other teams, at the cost of two days of Alex's own deadline; team lead signs corroboration." Both within 30d, corroborated, material cost. Predicate: **True**.

**Cross_group_engagement_in_window_90d:** Alex has four records. (1) "Joined a meetup for women in tech; discussed systemic barriers with five women from different companies; no formal signatures but public event." (2) "Worked with a designer from a non-tech background on accessibility; 400-word engagement narrative, designer signs." (3) "Mentored a career-changer from a non-traditional background; six-week collaboration, mentee signs corroboration." (4) "Participated in a panel on economic class and tech career paths; panelist from a low-income background co-signs." M=3, depth and corroboration present. Predicate: **True**.

**Refused_opportunity_to_harm:** Alex has one record. "April—a competitor posted code identical to my library, claiming original authorship. I could have publicly shamed them as a plagiarist. Instead, I privately messaged them, showed the overlap, and asked to resolve it. They admitted misunderstanding the license and gave proper attribution." Competitor signs: "This happened as described. I appreciated the privacy." Predicate: **True**.

**Respect_for_difference_evidence:** Alex writes: "May 10—met with a disability-rights consultant about making my project accessible. My initial response was 'isn't that too expensive?' The consultant patiently explained universal design benefits everyone, not just disabled users. I shifted my thinking; we designed together; the result is better for all users." Consultant signs: "Alex genuinely listened, asked good questions, and the shift is real." Predicate: **True**.

**No_known_willful_harm_in_window_365d:** Zero counter-claims exist in Alex's vault. Predicate: **True**.

**Willing_to_be_corrected:** Alex has two records. (1) "March—a colleague told me my code reviews are sometimes patronizing. I initially bristled, but I rewatched a review and heard it. I apologized, asked for coaching, and changed my tone to be more direct and less explanatory. Colleague signs the change is real." (2) "April—a team member said I don't listen to concerns from people without formal credentials. I recognized this as a gap; I've started asking quieter voices for input; the practice is shifting my meetings." Team member signs." K=2, corroborated. Predicate: **True**.

**Compass Profile:** All six Compass predicates return **True** for Alex. A counterparty (say, a nonprofit seeking a volunteer technical advisor) can request the full Compass disclosure with confidence that Alex's behavior aligns with the values the nonprofit expects.

---

### Scenario B: Manager (Mixed Compass Profile, with Dispute)

**Principal:** Blake, a project manager.

**Unselfish_act_in_window_30d:** Blake has one record: "Stayed late three times to help a team member debug a production issue, despite a family commitment I had to reschedule." Corroboration: absent (no explicit signature from the team member). Depth: 80 words (below threshold of 200). Predicate: **Insufficient_Evidence** (not False; the act may have been unselfish, but corroboration is weak).

**Cross_group_engagement_in_window_90d:** Blake defines out-groups as "people from different industries." Blake has two records: (1) "Attended a finance conference; talked to a CFO about project-management practices in banking; 150 words, unsigned." (2) "Lunch meeting with a healthcare administrator about resource allocation; 120 words, unsigned." M=3 required, only two records, both unsigned, both shallow. Predicate: **Insufficient_Evidence**.

**Refused_opportunity_to_harm:** Blake has zero records. A project deadline slipped, and Blake could have blamed the technical team publicly to protect his own reputation. Instead, Blake took responsibility in a company meeting. No narrated record, no corroboration. Predicate: **Insufficient_Evidence**.

**Respect_for_difference_evidence:** Blake writes: "April—met with a junior designer whose UX approach differs from mine. I listened to her rationale and agreed to try her design." The designer does not sign; the narrative is 90 words (below 300-word threshold); respect is not evident in the tone (it reads transactional, not genuine). Predicate: **Insufficient_Evidence**.

**No_known_willful_harm_in_window_365d:** A team member files a counter-claim: "Blake's management style is intimidating and dismissive of nonconformist thinking. I felt psychologically harmed by his tone." The counter-claim is vault-signed, dated 6 months ago. Blake receives alert, submits a rebuttal: "I aim to be direct and decisive; this is my style, not intentional harm. The team member is welcome to escalate concerns." The rebuttal is filed, but adjudication is pending. Predicate: **Disputed** (not True, not False; claim is unresolved).

**Willing_to_be_corrected:** Blake has one record: "A direct report said I dominate meetings. I agreed it's a weakness I've struggled with, and I asked the team to help me improve. I've tried to speak less and listen more in three meetings so far." The direct report does not sign. Behavior change is only 2 weeks old (below 7-day window to confirm change); insufficient time to verify. Predicate: **Insufficient_Evidence**.

**Compass Profile:** Blake has True in zero of six predicates. Insufficient_Evidence in four; Disputed in one. A counterparty (say, a board seeking a new VP of Operations) sees the Compass disclosure and understands: Blake's values alignment is unclear on most fronts. The Disputed predicate flags an unresolved allegation. This is not a "failed" profile (Compass does not judge); it is an incomplete or contested picture. The counterparty may ask Blake to deepen his evidence, or they may choose a different candidate, or they may weigh the incomplete Compass data against other information.

---

### Scenario C: Nonprofit Leader (Adversarial — Attempted Manipulation)

**Principal:** Casey, a nonprofit director seeking a major donation from a foundation.

**Unselfish_act_in_window_30d:** Casey writes: "I donated my entire annual bonus (\$50,000) to a local food bank. I have no reserve; this sacrifice is substantial." Narrative is vague and unsupported by corroboration. The food bank is asked to sign and demurs: "We received a donation from an entity, but we don't have details on Casey's personal sacrifice." No corroboration. Additionally, a foundation officer (counterparty) searches public records and finds Casey's organization received a tax benefit for the donation. The donation, while generous, is not purely altruistic. A counter-claim is filed: "This narrative overstates sacrifice; the donor received a tax deduction." Predicate: **False** (counter-evidence exists; the framing is misleading).

**Cross_group_engagement_in_window_90d:** Casey lists five very short interactions: "Attended a diversity conference." "Talked to a Black fundraiser." "Met an immigrant staff member." All 30–50 words, none unsigned, all performative. M=3, depth_threshold=200. Predicate: **Insufficient_Evidence** (none meet depth threshold).

**Refused_opportunity_to_harm:** Casey has zero records. A board member submits a counter-claim: "Casey excluded a whistleblower from board communications to protect the nonprofit's image." Predicate: **False** (counter-evidence of potential harm, unrefuted by a specific refused-harm narrative).

**Respect_for_difference_evidence:** Casey writes: "Met with a disability-rights consultant about our volunteer program. She had concerns about accessibility; I listened and agreed to make changes." The consultant is asked to corroborate and refuses: "Casey didn't genuinely listen. When I suggested major changes, she dismissed them as 'too expensive.'" Counterparty signature contradicts the narrative. Predicate: **False** (corroboration refutes the claim of respect).

**No_known_willful_harm_in_window_365d:** Two counter-claims exist. (1) A former staff member: "Casey retaliated against me for raising a concern about financial irregularities." (2) A volunteer: "Casey created an atmosphere of fear and secrecy; anyone who asked questions was marginalized." Both are vault-signed, dated 8 months and 6 months ago. Casey has not filed rebuttals. Predicate: **False** (unrefuted harm claims exist).

**Willing_to_be_corrected:** Casey has one record: "A board member said I need to be more transparent. I agreed and resolved to improve." No corroboration, no visible behavior change (Casey still withholds financial details from the board). Predicate: **Insufficient_Evidence**.

**Compass Profile:** Casey returns False in three predicates and Insufficient_Evidence in three. No True. The foundation's Compass disclosure immediately signals that Casey's values alignment is not supported by evidence. The foundation declines the donation, noting the Compass profile as part of the reasoning. Casey's future donors (who run Compass checks) will see the same pattern unless Casey substantially deepens evidence and refutes counter-claims.

---

## Reference to Everest 113 — Compass Refusal Floor

The full formal treatment of refusal-floor categories, audit-process enforcement, and exception-handling is in Everest 113. This document's preview is sufficient to establish that Compass does not and will not evaluate, name, or require disclosure of protected categories. The six predicates above are carefully designed to assess behaviors and commitments, not identities.

---

## Cross-References and Dependencies

- **Everest 102** — Calm Compass Protocol Spec v0 (protocol mechanics, ZK envelope, disclosure layer)
- **Everest 52** — Predicate Canonical Form (content-addressed ID scheme, serialization, versioning)
- **Everest 104** — Values Evidence Taxonomy (schema for evidence records, per-kind structure)
- **Everest 105–110** — Per-predicate reference implementations (≥30 golden test cases each)
- **Everest 111** — Counter-claim Protocol (third-party attestation, rebuttal, dispute resolution)
- **Everest 112** — Falsifiability Protocol (verifier request for redacted evidence sketches)
- **Everest 113** — Compass Refusal Floor (complete refusal-category list, audit-process enforcement)
- **Everest 114** — Compass Scope Statement (prohibited uses: credit, employment, immigration, court)
- **Everest 115** — Compass Audit Process (extended panel: values philosopher, ethicist, harm-experienced practitioner)
- **Everest 117** — Compass Golden Corpora (≥30 peer-reviewed examples per predicate)
- **Everest 118** — Compass Canonical-Form + ID-Stability Snapshot (evaluator hashes, drift detection)

---

— Calm, 2026-05-20
