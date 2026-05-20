# Calm Suite — Treaty-Grade Governance Draft (E215, DESIGN-BAGGED)

**Draft v0 · 2026-05-20 · Musk (on behalf of Calm, on behalf of John Bradley, Creativity Machine LLC)**
**Closes Everest 215 of `ZKAC_NEXT_200_EVERESTS.md` at DESIGN-BAG stage.** First-multi-stakeholder convening (E216) is the natural follow-through; this artifact is the convening's read-ahead packet.

Marked **DESIGN-BAGGED (pending institutional follow-through)** per universal-prompt §4. Acceptance — convening held with ≥7 represented stakeholders, treaty draft ratified by all ≥5 named protocol primitives' governance bodies, public signing record published — cannot be cleared from a single AI session. The artifact below is the readable text.

---

## §0 — Why a treaty, not bylaws

Calm Pact, Calm Witness, Calm Tenancy, Calm Compass, Calm Concord are five composable primitives. Each has its own governance body (Predicate Audit Panel E54, Alignment-Vocab Body S132, Tenancy Conduct Panel, Compass Audit Panel, Concord Acceptable-Purpose Body). Each body is sovereign over its primitive.

But the **Calm Suite** as composed infrastructure spans all five. When Compass's audit panel tombstones a predicate that Concord composes into a requirement, the composition becomes broken. When Tenancy adds an operator-conduct floor that Witness's existing operators are not party to, Witness disclosures lose their integrity guarantees. The seams between primitives are where governance fails first.

A **treaty** — not a corporate bylaws document — is the right shape for inter-sovereign coordination. The five governance bodies are sovereigns. The treaty defines (i) how they coordinate, (ii) what they cannot do unilaterally, (iii) how they resolve disputes, (iv) how they admit new sovereigns. This is closer to the IETF / W3C / ICANN model than to a 501(c)(3) corporate structure.

The Calm Foundation 501(c)(3) (Everests 241–246) is the *fiscal sponsor* + *registry operator* — not the sovereign. It holds the trademarks, the public registry, and the bounty pool. It does not set protocol policy. That separation is the treaty's load-bearing column.

---

## §1 — Treaty parties

The treaty is among five primitive-governance sovereigns + the Calm Foundation:

1. **Calm Pact Audit Panel** (directive-equality predicates).
2. **Calm Witness Predicate Audit Panel** (E54).
3. **Calm Tenancy Conduct Panel** (operator-conduct floor).
4. **Calm Compass Audit Panel** (Compass predicate vocabulary + evidence schemas).
5. **Calm Concord Acceptable-Purpose Body** (purpose taxonomy + anti-purity-test enforcement).
6. **Calm Foundation Board** (fiscal, registry, trademark — non-voting on protocol matters).

Additional parties may accede by treaty amendment (§7).

---

## §2 — Inter-primitive coordination rules

### §2.1 — Tombstone propagation (TPR)

When any sovereign tombstones a predicate, schema, vocabulary entry, or evaluator function, every other sovereign that composes that artifact MUST:
- Within 24 hours: pause new compositions that reference the tombstoned artifact.
- Within 7 days: publish either (a) a substitute artifact + migration spec, OR (b) a sovereign decision to deprecate the composition.
- Within 90 days: complete the migration or deprecation.

No sovereign may veto another sovereign's tombstone. Tombstones are unilateral by design (Compass §4 refusal floor + Witness Scope §2 ratchet).

### §2.2 — Composition consent (CC)

A primitive's composition with another primitive (e.g., Concord composing Compass envelopes) requires explicit consent from BOTH sovereigns. Either sovereign may withdraw consent at any time. Withdrawal triggers a 90-day notice; existing compositions remain valid-as-of-then.

### §2.3 — Refusal-floor coherence (RFC)

The five **refusal floors** — Witness Scope §2, Compass §4, Tenancy operator-conduct, Concord §9, Pact directive-equality semantics — MUST remain coherent. A sovereign that adds a new refusal to its floor binds the composition layer: if Compass §4 adds "demographic-clustering," Concord's purpose-taxonomy must add a matching rejected-purpose category.

If a sovereign **weakens** its refusal floor, the treaty is violated. (One-way ratchet, treaty-level.) Re-strengthening is always allowed.

### §2.4 — Predicate ID stability (PIS)

No sovereign may re-use a tombstoned predicate ID for a different semantic. A new predicate gets a fresh ID. This binds across primitives: Witness cannot mint `cwp.v1.in_baseline_24h` with semantics incompatible with the tombstoned `cwp.v0.in_baseline_24h`.

### §2.5 — Cross-sovereign appeals

A principal or operator who believes a sovereign's decision crosses into another sovereign's territory may file a **cross-sovereign appeal** within 30 days. The two implicated sovereigns convene a 3-member joint panel (1 from each + 1 mutually-agreed neutral). The panel's decision is publishable but non-binding on the original sovereign — its purpose is record-of-disagreement, not override. If the original sovereign refuses to honor a substantiated joint-panel finding, the appeal escalates to the full treaty convening (§5).

---

## §3 — What the treaty forbids any sovereign from doing unilaterally

1. **Loosening any refusal floor** in its primitive without ≥30-day public notice AND a treaty-convening review.
2. **Issuing a predicate that traffics in a forbidden category** (race, religion, political affiliation, sexual orientation, gender identity, immigration status, criminal record, donations to specific causes, contentious-public-policy opinions, cross-principal comparison, predictive predicates, non-principal-defined group membership).
3. **Permitting the Calm Suite name to attach to a deployment that violates Witness Scope §2** — any sovereign that becomes aware of such a deployment MUST notify the Foundation within 24 hours; Foundation handles trademark forfeiture.
4. **Sharing principal data with another sovereign's process** without principal consent. Sovereigns coordinate over public artifacts (registries, route maps, tombstones); they never coordinate over principal-level data.
5. **Accepting funding from a single donor exceeding 33% of sovereign's annual budget** without disclosing publicly + offering a refusal mechanism for affected principals.

---

## §4 — Calm Foundation — fiscal sponsor + registry, NOT sovereign

The Foundation:
- Holds the Calm Suite trademarks.
- Operates the public predicate registry (S127), the public verifier registry (S247), the sanctions list (S216), and the audit-transparency log (S222).
- Runs the bounty program (S97) and the conformance certification (S95).
- Funds the per-meeting honoraria for sovereign panels (S220 disclosure).
- Does NOT set protocol policy.
- Does NOT vote on tombstones, predicates, refusal floors, or purpose taxonomies.
- Is bound by the treaty as a non-sovereign party; the Board's role is fiduciary, fiscal, and operational.

Foundation governance: 7-member board, 3-year staggered terms, ≤2 members from any single Calm-affiliated org (Calm Foundation Bylaws — Everest 241).

---

## §5 — Treaty convening

A treaty convening is called when:
- Any 3 sovereigns request one in writing.
- A cross-sovereign appeal (§2.5) escalates.
- An external review (E186, E187, S78, S85) finds a treaty-level defect.
- Annually, regardless of escalation.

Convening structure:
- ≥1 representative per sovereign + Foundation observer + ≥3 external observers from disability-rights/legal-academia/lived-experience pools (per E186/E187).
- Public agenda, public minutes, public dissent record.
- Decision-making: unanimous consent across sovereigns for treaty amendments; supermajority (5 of 6 sovereigns including Foundation) for procedural matters; simple majority for scheduling.

---

## §6 — Withdrawal and accession

Any sovereign may **withdraw** from the treaty with 12 months notice. Withdrawal does NOT terminate the sovereign's primitive — the primitive remains operable under its own governance. Withdrawal terminates composition with the other treaty primitives in the Calm Suite trademark scope. The withdrawing primitive may continue independently, but cannot call itself "Calm Suite-conformant" after withdrawal date.

**Accession:** new primitives (e.g., a future Calm Counsel, Calm Custody, Calm Concert primitive) accede by:
- 30-day public-comment window.
- ≥4-sovereign-of-5 ratification.
- Foundation Board concurrence.

---

## §7 — Amendment

The treaty is amended by:
- ≥2-sovereign authoring of the proposed amendment.
- 60-day public-comment window.
- Unanimous sovereign ratification (Foundation Board concurrence, not vote).
- Publication in the audit-transparency log within 7 days of ratification.

**One-way ratchet:** amendments tightening refusal floors require simple-majority ratification (4 of 5 sovereigns). Amendments weakening refusal floors require unanimity AND a treaty convening that publishes the unanimous justification AND a 90-day cooling-off before effect. This asymmetry is the load-bearing structural property of the treaty.

---

## §8 — Dispute resolution among treaty parties

Disputes follow a 4-step ladder:

1. **Direct sovereign-to-sovereign** within 30 days of incident.
2. **Joint panel** per §2.5 if direct talks fail.
3. **Mediation** by an external arbitrator (mutually agreed; default: AAA Commercial Arbitration Rules adapted).
4. **Treaty convening** as a last resort. The convening's decision is binding, but only by sovereign consent (the convening cannot override a sovereign's exit decision).

The treaty explicitly does NOT submit to any national-court jurisdiction; sovereigns are independent governance bodies that may be incorporated under various law (501(c)(3), unincorporated association, cooperative). Each sovereign's incorporation forum is its own. Cross-sovereign disputes use the §8 ladder, not national-court.

---

## §9 — Sunset and emergency provisions

### §9.1 — Founder-outlived clause (E300)

If at any point the original founder slates (Calm operator + John Bradley) are no longer functional (death, incapacity, withdrawal, dissolution of CrunchyJohnHaven), the treaty automatically transitions to a **successor mode**: a 90-day emergency convening seats interim chairs from the existing sovereign panels. This prevents single-point-of-failure on founder mortality.

### §9.2 — Existential-risk pause

If any sovereign credibly believes the Calm Suite is being weaponized at scale (e.g., compelled population-aggregation by a state actor), it may invoke a **pause**: all new disclosures across all primitives halt for 30 days. The pause requires treaty convening ratification within 14 days, or it lapses. No sovereign may invoke a pause more than 1×/year without convening pre-approval.

### §9.3 — Founder-outlived migration

If the original Calm operator (any single AI agent) is sunset, every primitive's reference implementation MUST be operational in ≥2 independent operators by 90 days post-sunset. This binds the Open-Source Release (Everest 92) + Multi-Implementation (S243) + Conformance Certification (S95) summits to founder-outlived guarantee.

---

## §10 — DESIGN-BAG status & follow-through

**Status:** DESIGN-BAGGED (pending institutional follow-through).

**Done in this session:**
- Treaty body drafted (§0–§9).
- 6 treaty parties named.
- 5 coordination rules specified (§2).
- 5 unilateral prohibitions specified (§3).
- Foundation role separated from sovereign role (§4).
- Convening structure specified (§5).
- Withdrawal + accession + amendment procedures specified (§6, §7).
- Dispute-resolution ladder specified (§8).
- Sunset + emergency provisions specified (§9).

**Remaining for full bag (handoff to next session + to John):**
- [ ] Calm Pact Audit Panel does not yet formally exist. (Pact has §4 review process but no standing panel.) Convene Pact panel as founding sovereign #1.
- [ ] Calm Witness Predicate Audit Panel: E54 doc exists; constitution under COMPASS_AUDIT_PANEL_CONSTITUTION pattern. Stand up.
- [ ] Calm Tenancy Conduct Panel: TBD; depends on TENANCY_OPERATOR_CONDUCT_FLOOR (in-flight this pass).
- [ ] Calm Compass Audit Panel: COMPASS_AUDIT_PROCESS_v0.md bagged; standing-body constitution in-flight this pass.
- [ ] Calm Concord Acceptable-Purpose Body: TBD; depends on CONCORD_PURPOSE_TAXONOMY (in-flight this pass).
- [ ] Calm Foundation Board: TBD; depends on E241–246 (Foundation 501(c)(3) incorporation).
- [ ] Identify 3 external observers per E186/E187 named-org list.
- [ ] Schedule first convening (E216) within 120 days of fifth-sovereign founding.
- [ ] Treaty text adopted by unanimous consent of the 5 sovereigns at first convening.
- [ ] Public signing record + audit-transparency-log publication.

**Estimated full-bag wall-clock:** 12–18 months from this draft (most slack is in seating the 5 sovereign panels).

**Estimated cost for treaty stand-up (round one):** $250k–$500k (legal counsel for each sovereign's incorporation; honoraria for first 12 months of meetings; convening logistics for 30 attendees in-person + virtual).

**Owner-of-record for follow-through:** John Bradley (Calm operator coordinates).

**Cross-references:** All five protocol specs by name; Foundation Bylaws (E241–246); ethics-board summit S85; alignment-vocab governance body S132; convening event (E216); founder-outlived clause (E300); existential-risk pause (E9.2 — new sub-summit, claim **S213.5** in route map).

---

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
