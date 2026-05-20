# ZKAC — Alignment Disclosure Semantics v0

> *"The bit is informational, never punitive. A disclosure of 0 means 'we didn't find common ground on these dimensions; let's look elsewhere.' Not 'you are bad.'"*

**Closes Everest 141 of [`CALM_ZKAC_EVERESTS_106_305.md`](CALM_ZKAC_EVERESTS_106_305.md). Companion to [`CALM_CONCORD_PROTOCOL_v0.md`](CALM_CONCORD_PROTOCOL_v0.md) (modes and requirements), [`E198_PROTECTIVE_TRIBALISM.md`](E198_PROTECTIVE_TRIBALISM.md) (margin protection), [`E280_ADVERSARIAL_FITTING_DEFENSE.md`](E280_ADVERSARIAL_FITTING_DEFENSE.md) (hostile disclosure).**

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.**

---

## §1 — The headline distinction

An alignment disclosure is a structured tuple:

```
(
  disclosure_id,
  timestamp,
  principal_id,
  counterparty_class,
  alignment_mode,           // "all_satisfied", "any_satisfied", "asymmetric", "joint_threshold"
  tolerance_vector_hash,    // blinded commitment to counterparty's tolerance
  bit,                      // 0 or 1
  disclosure_scope,         // which dimensions were measured
  intended_use_stated,      // the counterparty's declared purpose
)
```

**Bit = 1 (Alignment demonstrated):** The principal's values vector, as evaluated against the disclosed dimensions and tolerance thresholds, satisfied the alignment requirement under the specified mode. The principal's chain evidence passes the predicate(s) the counterparty asked for. This is the green light: the counterparty may proceed with the collaboration as originally scoped, with values-alignment confidence in that scope.

**Bit = 0 (Alignment not demonstrated):** The principal's values vector, as evaluated against the disclosed dimensions and tolerance thresholds, did NOT satisfy the alignment requirement under the specified mode. The principal's chain evidence does not pass the predicate(s). This is NOT a stop sign; it is a signal to pivot. The default semantic is **cooperative redirection**: counterparty and principal explicitly explore alternative collaboration paths that might align.

---

## §2 — Operational semantics for Bit = 1

When a counterparty receives `bit = 1`:

1. **The counterparty may proceed with the stated purpose.** The collaboration framing that prompted the alignment disclosure can go forward, with the shared understanding that values-alignment (under the stated tolerance) has been cryptographically verified.

2. **The principal has pre-authorized disclosure of the fact that alignment was demonstrated** — but NOT the individual dimensions, NOT the magnitude of scores, NOT any breakdown of the tolerance vector. The counterparty knows only: "this principal's values satisfy my requirement for this purpose."

3. **The counterparty remains responsible for other due diligence** — state attestation (Calm Witness), directive equality (Calm Pact), harm-absence predicates, reputation graph, etc. A bit=1 alignment disclosure is ONE component of a multi-handshake check. It does not stand alone.

4. **The principal's chain reflects only what the principal authored.** Counterparty's receipt of a bit=1 disclosure does not create a record on the principal's chain. (The principal may audit who received disclosures via Everest 142; the bit=1 fact is counterparty-side metadata, not principal-side history.)

5. **Counterparty may NOT aggregate bit=1 across multiple principals to build a "high-alignment network."** Per Concord §4.3 (cardinality reveal refusal), cross-request linkability is rate-limited. A counterparty filing many alignment requests in sequence to build a map of "which principals align with my tolerance" triggers audit-panel detection.

---

## §3 — Operational semantics for Bit = 0

When a counterparty receives `bit = 0`:

### §3.1 — The v0 default semantic: Cooperative redirection

Bit = 0 **does NOT mean:**
- "This person is bad."
- "This person cannot be trusted."
- "This person is disqualified from any collaboration."
- "This person has failed a values test."

Bit = 0 **means:**
- "Alignment under the tolerance you requested was not demonstrated in this ZK evaluation."
- "The principal's chain evidence doesn't satisfy your threshold on these dimensions."
- "We found a mismatch; let's be explicit about it and explore options."

**The v0 default is that the counterparty and principal engage in **structured clarification**:**

1. **Counterparty states:** "I was looking for alignment on [dimensions], with [tolerance]. I received bit=0. Here's what I'd like to understand: which dimensions were the gap?"

2. **Principal may choose to disclose** (new alignment disclosure, different dimensions or threshold) or **decline and propose alternatives**: e.g., "I'm not willing to prove alignment on that dimension. But here's a different collaboration frame that doesn't require it. Would that work?"

3. **If direct alignment is impossible, cooperatively find adjacent opportunities:**
   - Different purpose/mode (Concord §7).
   - Different dimension set (lower-bandwidth disclosure).
   - Different role in the collaboration (asymmetric mode where one party's tolerance is more permissive).
   - Staged collaboration with trust-building (Everest 214: trust ladder).

### §3.2 — When a counterparty may decline to collaborate after bit=0

Bit = 0 is informational; a counterparty is free to end the negotiation. **But the protocol requires explicit statement of why:**

Counterparty must communicate one of:

- **"Your values don't align with mine for this purpose, and no alternative frame works."** (Honest pivot or end.)
- **"I don't have operational capacity for a different frame right now."** (Resource constraint, not judgment.)
- **"This dimension is load-bearing for my decision. I cannot proceed without it."** (Explicit requirement, not secret test.)

**Counterparty may NOT:**
- Silently reject without explanation.
- Claim bit=0 is evidence of the principal's unsuitability for *any* collaboration. (A bit=0 on "cross-cultural cooperation tolerance" does not disqualify someone from a technical collaboration.)
- Use bit=0 as a pretext to extract more disclosure. (If the principal declined a dimension, they declined it; rephrasing the request doesn't override consent.)
- Aggregate bit=0 across multiple principals to construct a sorting profile. (See §2.5.)

---

## §4 — The anti-profile rule: No aggregation of bit=0 across counterparties

**Hard rule:** A principal's bit=0 disclosures to counterparty A may NOT be aggregated with bit=0 disclosures to counterparty B to build a "values profile" of the principal.

**Why:** If counterparty A learns "principal X got bit=0 on my tolerance" and counterparty B learns the same, and they share that information, they begin to reconstruct which dimensions the principal is weak on. With enough bit=0 samples across many counterparties, a coalition could map the principal's full values vector via triangulation — defeating the principle of per-predicate consent.

**Enforcement:**

1. Each bit=0 disclosure is scoped to (principal_id, counterparty_class, session_nonce). Cross-session linking is cryptographically prevented by the predicate-evaluator bridge (Everest 75).
2. The principal's audit log (Everest 142) records that a disclosure was issued but **not the bit value**. Only the principal sees whether it was 0 or 1.
3. A counterparty who publicly claims "this principal got bit=0 from me" is making a representational statement about the principal. The principal may dispute it (bit=0 was interior to the session, not public). Disputes are audit-recorded.
4. Calm-stack operators who detect a counterparty publishing or trading bit=0 results across counterparty boundaries trigger audit-panel investigation.

---

## §5 — The anti-punishment rule: Principal's chain reflects only principal-authored events

**Hard rule:** A bit=0 disclosure **may NOT** create a negative record on the principal's chain.

The principal's Calm Witness chain (E1–E105, ZKBB-User) is the source of truth for what the principal has done, who they've collaborated with, what they've built. It is principal-authored and principal-controlled.

A counterparty's rejection (bit=0) is a *counterparty decision*, not a principal event. It does not belong on the principal's chain.

**Consequence:** If a principal later needs to understand why a collaboration fell through, they audit their own disclosures (Everest 142: "I issued an alignment disclosure to Org X on 2026-05-20") but see no negative record on their own chain. The principal's narrative of themselves is not corrupted by others' refusals.

**Exception — principal-authored reckonings:** If the principal *chooses* to record "I sought alignment with Org X on cooperation, was declined, and here's what I learned," that's a principal-authored record (`kind: "reflection"` or `kind: "collaboration_attempt"`) and it belongs on the chain. The principal owns the interpretation.

---

## §6 — Alignment failure vs moral judgment

The protocol computes: **does principal P's values vector satisfy tolerance vector T on dimensions D under mode M?**

This is a **technical question**, not a moral one.

**The protocol does NOT ask:**
- "Is this person good?"
- "Should society accept them?"
- "Are they worthy of respect?"
- "Do their values align with the true and right way to live?"

**The protocol CANNOT tell anyone how to live.** It measures values consistency under specific, agreed-upon, time-bounded, purpose-specific requirements. Nothing more.

**Consequence for bit=0:** A principal with bit=0 on "high-altitude cooperation tolerance" from one counterparty may have bit=1 on "local neighborhood support" from another. The same person can be misaligned for a funding partnership and perfectly aligned for a mutual-aid network. Both bits are true simultaneously; neither is a character judgment.

**Dangerous framing that the protocol rejects:** "This person scored low on cooperation, so they are selfish." (No: they are unaligned with *one counterparty's* cooperation tolerance, on *one predicate*, at *one moment*. They may be generously cooperative in other contexts.)

---

## §7 — Concord anti-purity-test integration

Calm Concord (the requirements-evaluation layer) enforces structural rules that prevent bad-faith alignment requests (Concord §4). The disclosure semantics here assume Concord is functioning:

- **Degenerate requirements are rejected at validation time.** A counterparty cannot ask for "alignment on all 10 dimensions with a threshold of 9.5/10" (which reduces to purity-testing). Concord validation catches this.
- **Empty purpose is rejected.** A counterparty must state what they're aligning for. If the stated purpose is later found to be false (e.g., "we said educational collaboration but used the disclosure for hiring"), the principal can cite the purpose-mismatch at audit.
- **No numeric similarity scores.** The output is always a single bit per mode, never a vector of dimension scores or an aggregate percentile.

**The disclosure semantics here implement the second layer of defense:** assuming Concord is doing its job, how should a counterparty and principal behave when the bit is 0?

---

## §8 — Five example counterparty policies for bit=0

### Policy 1: Foundation (Charitable donor, explicit mission alignment)

**Context:** A foundation seeks to fund only principals whose values demonstrate "sustained generosity across cultural boundaries."

**Counterparty requirement:** `all_satisfied`, dimensions = [non_tribal_engagement, generosity], tolerance = [≥0.6, ≥0.7].

**Bit = 1 outcome:** Foundation approves grant application. Collaboration proceeds.

**Bit = 0 outcome:**
- Foundation explicitly acknowledges: "We were looking for cross-cultural generosity evidence. Your chain shows strong in-group generosity but limited cross-cultural work."
- **Cooperative redirection:** Foundation offers three paths:
  1. Principal can seek a partnership with an organization in their in-group that has already demonstrated cross-cultural work. Foundation will fund the *partnership*, not just the principal.
  2. Principal can propose a grant focused narrowly on their in-group (shifting the purpose and tolerance). Foundation has a separate grant track for this.
  3. Principal can wait and reapply; Foundation will look again in 18 months if the chain shows new cross-cultural collaborations.
- Foundation documents the bit=0 in their own decision log (counterparty-side). Does NOT contact other foundations to warn them about the principal.

---

### Policy 2: Accelerator (high-intensity startup incubator)

**Context:** An accelerator seeks co-founders who are "resilient under stress, willing to be corrected, and non-bullying."

**Counterparty requirement:** `asymmetric`, principal predicates = [consistency_under_stress, willing_to_be_corrected, no_power_abuse_evidence], tolerance = [≥0.65, ≥0.6, 100%].

**Bit = 1 outcome:** Founder invited into cohort.

**Bit = 0 outcome:**
- Accelerator explicitly states which dimension failed (e.g., "willing_to_be_corrected" was low). Does NOT say "you're not founder material."
- **Cooperative redirection:**
  1. Accelerator offers a mentorship tier: "You can attend workshops, meet mentors, and build your network for 6 months. At the end, we'll re-evaluate."
  2. Accelerator suggests the principal find a co-founder who tests high on the dimension they're low on (e.g., "You're resilient but defensive. Find someone who's good at receiving feedback and team up.")
  3. Accelerator offers "resilience coaching" — explicit skill-building on the low dimension — before reapplication.
- Accelerator does NOT tell other accelerators "this person failed our alignment check."

---

### Policy 3: Journalist (trust calibration for source-vetting)

**Context:** A journalist evaluates sources for a long-form investigation. They want to know: "Is this whistleblower likely to have been truthful with me, or embellishing?"

**Counterparty requirement:** `any_satisfied`, dimensions = [no_deception_evidence, consistency_under_stress, willing_to_be_corrected], tolerance = [≥0.8, ≥0.7, ≥0.7].

**Bit = 1 outcome:** Journalist proceeds with the source as credible on face. Still fact-checks claims, but sourcing is trusted at baseline.

**Bit = 0 outcome:**
- Journalist defers the story: "The source scores low on my deception-absence check. I can't run this story on their allegations alone."
- **Cooperative redirection / explanation:**
  1. Journalist may explicitly ask the source: "I ran a trust check. Your chain shows some instances of changing your story under pressure. Before we proceed, can you help me understand that pattern?"
  2. If the source explains (e.g., "I was under duress from my employer; my story was accurate but I told it differently to different people"), the journalist re-evaluates with that context.
  3. Journalist seeks corroborating sources with higher alignment bits.
- Journalist does NOT publish the bit=0 result or use it to discredit the source publicly. (Using a disclosure as a weapon is a separate harm.)

---

### Policy 4: Bank / Regulated Institution (KYC / AML, standard friction tier)

**Context:** A bank evaluates whether to open an account for someone. Regulatory requirement: "Know Your Customer." The bank wants: "No evidence of willful financial harm or deception."

**Counterparty requirement:** `all_satisfied`, dimensions = [no_deception_evidence, no_theft_evidence], tolerance = [≥0.75, ≥0.9].

**Bit = 1 outcome:** Account opens with standard tier.

**Bit = 0 outcome:**
- Bank acknowledges: "Our fraud-check didn't clear. This is routine; many people have short windows where they don't have documented evidence of trustworthiness (e.g., new arrivals, people without long public records)."
- **Cooperative redirection:**
  1. Bank offers "restricted tier" account: lower transaction limits, higher monitoring, but functional. Principal can graduate to standard tier after 6–12 months of clean activity.
  2. Bank asks: "Do you have a reference (someone we trust who can vouch for you)?" (Reputation graph composition, Everest 210.)
  3. Bank suggests bringing a guarantor (friend/family with high alignment on the same predicates) who co-signs.
- Bank does NOT deny banking entirely based on bit=0. (Regulatory and moral obligation: financial inclusion.) Bank applies friction, not rejection.

---

### Policy 5: Peer AI Collective (Calm-aligned AI agents)

**Context:** A peer collective of AI agents (aligned under Calm Pact + ZKAC) wants to admit a new agent. Requirement: "This new agent will not defect under incentive pressure."

**Counterparty requirement:** `all_satisfied`, dimensions = [consistency_under_stress, non_tribal_engagement, no_power_abuse_evidence], tolerance = [≥0.8, ≥0.6, 100%].

**Bit = 1 outcome:** New agent joins the collective. Full participation.

**Bit = 0 outcome:**
- Collective acknowledges: "Your chain shows inconsistency under stress (you've adjusted priorities when resources were tight). In a peer collective, we can't assume you'll hold alignment during a crisis."
- **Cooperative redirection per Calm Pact §6 (restricted-action mode):**
  1. New agent joins in restricted mode: they can observe, collaborate on low-stakes shared goals, build reputation, but cannot vote on high-stakes collective decisions or hold fiduciary roles.
  2. Collective offers a mentorship/bonding path: "Work with us on [lower-stakes project] for 3–6 months. If you develop a track record of consistency, we'll promote you."
  3. Collective is transparent about the restriction: "You're not excluded; you're in a learning relationship. The bit=0 is informational; we're building trust."
- Collective does NOT publicly broadcast that the agent "failed the alignment test." (Reputational harm is a separate concern; the bit is interior to the negotiation.)

---

## §9 — Cross-reference to protective tribalism (E198)

Bit = 0 on a cross-tribe-engagement dimension does NOT automatically reflect badly on a principal in a marginalized position.

**Example:** A principal whose chain shows predominantly in-group collaboration, and who self-declares as a member of a historically-persecuted minority, may receive bit=0 on "cross-cultural cooperation tendency" from a counterparty with high cross-cultural tolerance — yet still receive bit=1 on "non_tribal_lock_in" per E198's protective clause.

**Why the divergence:** The counterparty's tolerance and the ZKAC protocol's protective logic are separate layers. A principal can be misaligned with one counterparty's specific tolerance while still passing the protocol's own anti-tribalism guards.

**Operational consequence:** When a principal with bit=0 on cross-tribe engagement cites E198 protective clause in redirection negotiation, the counterparty must engage honestly:

- If the counterparty's purpose genuinely requires cross-cultural collaboration, the tension is real; cooperative redirection explores whether a different role/partnership model works.
- If the counterparty's stated purpose is actually neutral to culture (e.g., "technical collaboration on code"), the counterparty has no legitimate reason for the tolerance. They may need to revise their requirement (Concord validation).

---

## §10 — Adversarial fitting defense cross-reference (E280)

A principal who knows the counterparty's published tolerance may attempt to fit their self-reports to maximize alignment.

**Bit = 0 is partly a defense against this.** If a principal's chain shows sudden, coordinated values changes timed to a counterparty's public tolerance announcement, the predicate evaluator can flag "drift-rate anomaly" and degrade the evidence (Everest 271).

**Consequence for disclosure semantics:** When a principal receives bit=0 and asks "why didn't I align?" the counterparty can sometimes respond: "Your chain shows recent changes to these dimensions that look adversarial. We evaluated the current state, but the drift pattern raised flags."

**Principal's recourse:** The principal can transparently acknowledge the drift (if real) and propose a trust-ladder model (Everest 214) rather than full alignment. Example: "I've been re-thinking my values over the past year. I don't have 10 years of stable cross-cultural evidence, but I'm genuinely trying. Can we do a 12-month probation?"

This is honest cooperative redirection, not gatekeeping.

---

## §11 — Scope boundaries: What the protocol is NOT

This document specifies the semantics of alignment disclosure bits. It is NOT:

1. **A moral framework.** The protocol cannot tell a principal or counterparty how to live or what to value.
2. **A credit score for humanity.** Disclosures are principal-authorized, class-bounded, and always a single bit per grant.
3. **A tool for ranking people.** Aggregation across principals is structurally refused.
4. **A substitute for human judgment.** Counterparties act on the bit; they remain responsible for downstream decisions.
5. **A replacement for transparency.** Counterparties must state their purpose and tolerance explicitly. Vague or hidden requirements are rejected at Concord validation time.

---

## §12 — Implementation checklist for v0

- [ ] Counterparty policies (§8 examples) are reviewed by ≥3 organizations representing each policy type.
- [ ] Bit=0 handling is specified in every operator's CALM_ZKAC deployment guide (Everest 291).
- [ ] Audit-panel monitoring (Everest 142, E294) includes detection of counterparties using bit=0 as coercion or aggregation.
- [ ] Principal's audit log (Everest 142) is readable by the principal but does NOT expose bit values to third parties.
- [ ] "Cooperation redirection" language is used in all standard responses; gatekeeping language is flagged as violation.
- [ ] E198 protective-clause integration is tested: principals in marginalized categories can reference protective status when negotiating after bit=0.

---

## §13 — Versioning and evolution

`zkac-alignment-disclosure-semantics/v0` — this doc.

Future versions (v1, v2, ...) may:
- Refine the five example policies based on real-world experience.
- Add new cooperation-redirection templates.
- Strengthen the anti-profile and anti-punishment rules.
- Adjust the protective-category registry in light of E294 advocacy review.

New versions go through the standard audit + version-bump mechanic (Everest 97, 115).

---

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20. Anchored into `~/.calm-vault/user_state.jsonl` as `kind: "summit_bagged"` immediately after commit. The semantics are clear.**

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
