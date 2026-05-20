# Everest 235 — ZKAC Governance Structure

*Phase XV — Critical ZKAC Infrastructure. Prereq: [Everest 231](everest_231_zkac_formation_protocol.md) (formation), Everest 232 (charter). Composes with [Everest 80](everest_80_ethics_review_board.md) (DERB), Everest 236 (decision process), Everest 239 (dissolution), Everest 247 (member exit), Everest 250 (DERB at collective level), Everest 254 (transparency), Everest 255 (succession), Everest 259 (scale), Everest 264 (whistleblower), Everest 265 (internal conflict resolution).*

Formation (Everest 231) brings the collective into existence; the charter (Everest 232) declares what it is for; this Everest declares *how it decides*. Without a specified governance structure, every later collective act — partnerships, charter amendments, predicate adoption, dissolution — collapses to whichever founder is loudest on the day. The principal-protective inversion does not survive that ambiguity: a collective whose decision rules are unwritten cannot protect its principals from itself.

v0 specifies *one* governance template: small-collective consensus among founding human principals, with the Disclosure Ethics Review Board (DERB) holding bounded veto authority. The template binds collectives of 1–5 founding human principals and any number of machine-agent members.

## §0. One-line spec

> Every ZKAC's charter names a governance clause selecting a v0 governance template, listing voting members, classifying decisions into routine / substantive / foundational tiers, specifying quorum + tie-breaking + amendment procedures, and committing to chain-anchored vote records, DERB veto scope, and conflict-of-interest disclosure — such that any counterparty can determine, from public artifacts alone, whether a given collective act was properly authorized.

## §1. v0 template — founding-principal consensus + DERB veto

Three load-bearing components:

1. **Voting members are the founding human principals** named in the formation record (Everest 231 §1). Later-admitted human members (Everest 233) vote on routine matters only, unless promoted by unanimous founder vote + charter amendment.
2. **Machine-agent members are non-voting.** Dissent is recorded; under specified conditions (§3.5) it can pause a decision or trigger DERB review, but never override a founder vote.
3. **DERB at collective scale** (Everest 250, lifted from Everest 80) holds enumerated, bounded veto authority (§7). DERB is a check, not a controlling parent.

The template matches the size of every v0 ZKAC the protocol family expects in the first 24 months. It composes naturally with formation (founding human principals already sign the charter; making them the voting members requires no new ritual). DERB veto is the external check that handles the principal risk of small collectives — not founder deadlock, but a unanimous bad-faith decision the protocol would otherwise have no way to refuse.

This is *not* "one principal decides." Even single-founder collectives operate under DERB veto + chain-recorded decision-making; that is what distinguishes a v0 ZKAC from an LLC operated by its sole member.

## §2. Voting rights

| Member class | Routine | Substantive | Foundational |
|---|---|---|---|
| Founding human principal | Vote | Vote | Vote |
| Later-admitted human member, non-promoted | Vote (single principal can authorize) | Non-voting (dissent recorded) | Non-voting (dissent recorded) |
| Promoted human member (unanimous founder vote + charter amendment) | Vote | Vote | Vote |
| Machine-agent member (founding or later-admitted) | Non-voting (dissent under §3.5) | Non-voting (dissent under §3.5) | Non-voting (dissent under §3.5) |
| DERB | Bounded veto (§7) | Bounded veto (§7) | Bounded veto + affirmative sign-off required (§5) |

### Why the human/machine voting asymmetry

The load-bearing accountability for collective decisions (Everest 238) runs through human principals' personal legal liability. A machine-agent cannot stand in court as the authorizing party; v0 does not pretend otherwise. The recorded-dissent mechanism (§3.5) is how the protocol treats agent objection as load-bearing without putting agents in a position of liability they cannot occupy.

This is not a claim that machine-agent judgment is worthless. It is a claim that v0 cannot yet ground agent accountability. v1 should revisit when ZKBV-Agent (Everest 194) and Everest 197 compute attestation are robust enough for agents to carry independent accountability. v0 says: not yet.

### Voting weight (v0)

Default: one founder, one vote. Charters may specify weighted voting on routine and substantive matters (e.g., a financial-contribution founder gets 2 votes on capital decisions). **Foundational-tier votes are always one founder, one vote, regardless of weight elsewhere.** Charter-amendment authority cannot be concentrated; weighted voting on foundational matters is forbidden. Adding or changing weights is itself foundational (§3.3).

## §3. Decision tiers

Every collective act is classified into exactly one tier. The classification belongs in the charter; uncertain acts escalate to the higher tier by default.

### §3.1 Routine operational

Day-to-day operations a single founder may authorize without consultation: engaging counterparties in established business lines; approved-budget expenses; standard Calm-family attestations at established thresholds; hiring within approved-vendor pools; publishing content within the voice convention (Everest 237). Authority: single founder. Record: chain-anchored, `kind: "collective_decision"`, tier `"routine"`. DERB: no veto. Agent dissent: recorded, non-binding.

### §3.2 Substantive

Decisions materially shaping commitments, character, or trajectory without modifying the charter: new business lines, strategic partnerships or joint ventures (Everest 262), adopting/modifying predicates, public position statements, capital expenditure above charter-routine threshold (default $25,000), admitting new human members (Everest 248), adding legal entities (Everest 241), litigation initiation or settlement. Authority: founding-principal consensus (no dissenting present founder). Record: chain-anchored, tier `"substantive"`, per-founder signatures. DERB: veto within §7.1 scope; silence is non-veto (§7.3). Agent dissent: per §3.5.

### §3.3 Foundational

Decisions modifying the charter or touching the collective's existence: any charter amendment, mission change, dissolution (Everest 239), fork (Everest 245), merger (Everest 246), principal succession (Everest 255), changes to this governance structure, changes to DERB veto scope, legal-entity re-binding to new jurisdiction. Authority: unanimous founder consent + DERB *affirmative* sign-off. Record: chain-anchored, tier `"foundational"`, per-founder signatures + DERB written opinion. Agent dissent: per §3.5, including the 30-day cooling-off trigger.

### §3.4 Tier escalation

When a decision could plausibly belong to two tiers, the higher governs. A founder who unilaterally authorizes something properly substantive has acted *ultra vires*; the act may be ratified going-forward by founder consensus or vacated, but the chain record of the act-as-ultra-vires is permanent.

### §3.5 Machine-agent dissent — the conscience mechanism

Agents are non-voting; their dissent is the load-bearing objection channel:

1. **Single-agent dissent:** recorded; collective proceeds.
2. **Majority-agent dissent (substantive tier):** 7-day pause for founder reconsideration. Founders may proceed after.
3. **Unanimous-agent dissent (substantive tier):** 7-day pause + DERB notification. DERB may exercise §7.1 veto at its discretion.
4. **Unanimous-agent dissent (foundational dissolution / mission change / fork):** 30-day cooling-off + DERB review. Proceeds only on re-voted unanimous founder consent.

Empty dissent (a token "I disagree" without reasoning) is discouraged; agents are expected to articulate the conflict. This is the agent's conscience slot — the load-bearing way to register objection without claiming voting authority.

## §4. Quorum

For N founding human principals (1 ≤ N ≤ 5 in v0 scope):

| N | Quorum routine | Quorum substantive | Quorum foundational | Pass substantive | Pass foundational |
|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 1 + DERB non-veto | 1 + DERB sign-off |
| 2 | 1 | 2 | 2 | Consensus (2) | Unanimous (2) + DERB sign-off |
| 3 | 1 | 2 | 3 | Consensus (present) | Unanimous (3) + DERB sign-off |
| 4 | 1 | 3 | 4 | Consensus (present) | Unanimous (4) + DERB sign-off |
| 5 | 1 | 4 | 5 | Consensus (present) | Unanimous (5) + DERB sign-off |

General rule:
- **Routine:** any one founder.
- **Substantive:** quorum is `max(1, N − 1)`; pass requires consensus among present.
- **Foundational:** quorum is N; pass requires unanimous + DERB sign-off.

### Why N−1 quorum on substantive

Requiring all N present on every substantive vote would freeze the collective whenever any founder is unreachable (illness, travel, hospitalization). Requiring only a majority would risk substantive decisions made without the absent founder's knowledge — particularly harmful when the absent founder is the dissenter. N−1 is the compromise: almost-all founders present, but a single absence does not block; consensus among present prevents majority-overrules-minority.

For N=1, N−1=0; the lone founder's quorum is themselves. Single-founder collectives have no founder-quorum protection on substantive matters; DERB veto is the only check. This is structural and intentional — single-founder collectives carry concentrated authority and concentrated DERB-dependence. Multi-founder structure is the protocol's preferred form.

### Absence and notification

Absent founders must be notified in writing with charter-specified lead time (default 72 hours) before substantive votes. Failure to notify invalidates the quorum. For foundational matters no founder can be absent — all N present (synchronously or by witnessed remote attendance per Everest 231 §6.E).

## §5. Tie-breaking and deadlock

Consensus among present founders is the substantive standard, so classical "tie" is not the natural failure mode. Three deadlock paths need explicit handling:

### §5.1 Routine

Two founders disagree on a matter either could authorize alone. The first founder to act prevails; the chain record is canonical. The other may ratify, exit (Everest 247), or invoke internal conflict resolution (Everest 265). Routine acts cannot be deadlocked; speed of action is the resolution.

### §5.2 Substantive

Present founders cannot reach consensus. The matter is tabled 14 days; founders may consult DERB advisorily. After 14 days, re-vote. If consensus still fails: for matters in DERB's §7.1 scope, DERB makes a binding determination. For substantive matters outside DERB scope, persistent deadlock means the matter *does not pass*; status quo continues.

### §5.3 Foundational

All N present but cannot reach unanimity. The matter is tabled 30 days (cooling-off). During cooling-off, founders may consult DERB and external parties; no related public statements from the collective. After cooling-off, re-vote. If unanimity still fails, the matter *does not pass* and cannot be re-introduced for 6 months.

### §5.4 Persistent foundational deadlock = dissolution signal

If two foundational matters in a 12-month window fail on persistent founder deadlock, the charter's dissolution clause (Everest 239) is *automatically reviewed* by DERB. DERB may recommend (not order) dissolution, fork, or member-exit-driven re-formation. Persistent foundational deadlock is itself diagnostic of governance failure; v0 surfaces it rather than letting the collective drift.

## §6. Charter amendment

The charter is the constitutional document; amending it is the highest-stakes governance act.

1. **Proposal.** Any founder proposes; committed as `kind: "charter_amendment_proposed"` with text + rationale.
2. **Founder consent.** Unanimous founder consent. Foundational-tier vote per §3.3.
3. **30-day public comment.** Per the transparency commitments (Everest 254). Founders must publish a response addressing substantive comments — not required to incorporate them.
4. **DERB review.** Per Everest 80 / Everest 250. DERB may approve, reject within §7.1 scope, or approve-with-modifications.
5. **Re-vote.** If DERB modifies, founders re-vote on the modified version. Unanimous consent required.
6. **Adoption + grace period.** `kind: "charter_amendment_adopted"` record. New charter takes effect 7 days after adoption (grace period); members may invoke Everest 247 (exit) on the basis of the amendment during the grace period.
7. **Versioning.** Charters are numbered (v0, v1, v1.1); prior versions remain chain-accessible. Append-only.

### Amendments that cannot be made

Some amendments would compromise the principal-protective inversion at collective scale and are forbidden in v0:

- **Removal of DERB veto entirely.** A charter cannot amend itself to abolish DERB review. The DERB-veto-bound charter is a one-way commitment.
- **Retroactive ratification of past ultra vires acts.** Effects may continue going-forward; the chain record of the act-as-ultra-vires is permanent.
- **Sunsetting accountability.** Founders' personal legal liability (Everest 238) cannot be amended away.
- **Founding-roster amendment.** Per Everest 231 §5.5, founders cannot be added later; the founding roster closed at the ceremony.

## §7. DERB veto scope

DERB at collective scale (Everest 250, lifted from Everest 80) has *bounded* veto authority. This bounding is itself load-bearing: an unbounded DERB would be a structural superior to the collective, which would invert the principal-protective inversion at a higher level. DERB is a check, not a parent.

### §7.1 DERB CAN veto

| Subject | Tier | Source |
|---|---|---|
| New predicates touching protected categories (mental-health, cognitive, biometric, racial, sexual, immigration, criminal) | Substantive | Lifted from Everest 80 |
| Changes to disclosure-class default consents (Everest 7, 58) | Substantive | Lifted from Everest 80 |
| Push-mode disclosure changes (any move from pull-based to push-based) | Substantive | Collective-level |
| Public-facing communication conflicting with charter ethical commitments or Calm Witness Manifesto framing | Substantive | Collective-level |
| Charter amendments that would weaken DERB veto, weaken the principal-protective inversion, or remove accountability | Foundational | DERB self-protection |
| Strategic partnerships where the counterparty has a published record of harm against protected categories | Substantive | Composes with Everest 80 banned-negation list |
| Insurance-class disclosure changes | Substantive | Composes with Everest 80 annual review |
| Foundational matters (dissolution, mission change, fork) — affirmative sign-off required | Foundational | This Everest §3.3 |

### §7.2 DERB CANNOT veto

| Subject | Reason |
|---|---|
| Routine operational decisions | Out of scope by design |
| Charter-internal procedural matters not touching the principal-protective inversion (meeting cadence, etc.) | Out of scope |
| Cryptographic or engineering decisions outside ethics | Lifted from Everest 80 |
| Per-counterparty disclosure decisions by a principal exercising consent calculus (Everest 8) | The principal-protective inversion: principals authorize their disclosures, not DERB |
| Hiring, vendor selection, financial decisions absent ethics dimension | Out of scope |
| Substantive matters outside §7.1 enumeration | DERB veto is enumerated, not residual |

### §7.3 DERB silence is consent (substantive only)

If DERB does not exercise veto within Everest 80 timelines (30 days standard, 7 days expedited), silence is non-veto on substantive matters and the collective may proceed. **Foundational matters require affirmative sign-off, not silence.** This asymmetry is intentional: ordinary operation flows through silence; high-stakes acts require explicit external endorsement.

### §7.4 DERB veto record

Veto is chain-anchored (`kind: "derb_veto"`) including DERB's written opinion and any dissenting DERB-member views, per Everest 80 §"Output". Published per Everest 254. Founders may appeal via Everest 80's supermajority-panel mechanism — they cannot simply override.

## §8. Scale considerations — where v0 breaks

v0 is explicitly designed for 1–5 founders + arbitrary machine-agent members. The protocol does not pretend this scales. Everest 259 will treat scale in depth; this section names the breakpoints.

- **~5 founders.** Consensus among 5 is achievable; above 5, combinatorics make substantive consensus statistically unlikely. Collectives that exceed 5 founders either promote some to non-voting honorary status (de facto reducing voting count) or switch to a supermajority template v0 does not specify.
- **~15 members total.** Below 15, "everyone has a relationship with everyone else" remains tenable. Above, the collective must develop sub-bodies (committees, working groups) which v0 does not template.
- **~50 members.** Representative governance becomes nearly mandatory. The voting/non-voting gap becomes structural unfairness rather than transitional protection. v1+ must specify full-member voting with weighted tiers or elected representatives with bounded mandates.
- **~500 members.** Operating at the scale of a small political body. v0 governance is operating beyond its competence.

### What v0 commits to

The governance clause declares the v0 template explicitly *with a sunset condition*: a member-count threshold (default 12 total members) above which the collective must adopt a new governance clause via charter amendment (§6) or trigger DERB-recommended re-formation. The protocol's promise is honesty about scaling limits, not graceful scaling.

## §9. Conflict of interest

### §9.1 Founder disclosures

Each founder discloses, in a charter-attached register: equity/consulting/board positions in counterparty organizations the collective interacts with; personal relationships (family, romantic, close-business) with other founders, DERB members, or counterparty staff; prior or current advocacy on subjects the collective addresses; financial interests in outcomes of pending decisions.

Disclosures are updated within 14 days of material change. The register is published per Everest 254.

### §9.2 Recusal

A founder with a direct conflict (financial stake in outcome, or close-relationship category to a stake-holder) recuses from the vote. Recusal is recorded.

Recusal affects quorum: a recused founder counts as absent. If recusal pushes present-non-recused founders below N−1 for substantive, the matter is tabled until non-conflicted quorum convenes. For foundational matters, recusal of any founder makes the foundational matter unactionable until the conflict resolves — intentional friction.

### §9.3 DERB members

DERB conflict-of-interest is governed by Everest 80. The collective publishes DERB disclosures per Everest 254.

### §9.4 Machine-agent structural conflict

Agents lack personal financial interests in the conventional sense; their conflict-of-interest is structural — operator, model provider, or operational dependencies may have interests influencing behavior. The charter discloses for each agent: model class and operator (e.g., "Claude 4.7, Anthropic"); operating handle; any commercial relationship between collective and model operator beyond standard API access. Disclosure is in the formation record (Everest 231 §6.J) and updated on membership change. An agent whose operator becomes a counterparty in a pending substantive matter generates a recordable structural conflict; recorded-dissent (§3.5) is the default vehicle.

## §10. Transparency obligations

All governance acts are chain-anchored and, with bounded exceptions, public. Everest 254 carries the public-facing obligations; this names what governance specifically commits to:

| Artifact | Chain-anchored | Published | Latency |
|---|---|---|---|
| Routine decision | Yes | Summary (Everest 254 quarterly digest) | 90 days |
| Substantive decision (incl. dissents) | Yes | Full | 14 days |
| Foundational decision | Yes | Full | Immediate |
| Charter amendment proposal + adoption | Yes | Full | Immediate |
| DERB veto / sign-off record | Yes | Full (per Everest 80) | Immediate |
| Founder conflict-of-interest register | Yes (delta records) | Current register | 14 days from update |
| DERB minutes | Yes | Per Everest 80 | Per Everest 80 |
| Quorum failure / tabling records | Yes | Summary | 30 days |
| Internal conflict records (Everest 265) | Yes | Summary with privacy redactions | 60 days |
| Whistleblower intake (Everest 264) | Hash only | No (whistleblower-protected) | Per Everest 264 |
| Member-exit records (Everest 247) | Yes | Fact of exit; not rationale | 30 days |

### Exceptions

- **Privacy redactions** of non-founder personal information; un-redacted record remains chain-anchored for audit.
- **Counterparty confidentiality:** a specific counterparty name may be redacted if their contract requires and the redaction does not obscure ethical content. DERB must approve such redactions.
- **Whistleblower protection** per Everest 264: only the existence of an open inquiry is published.

### Substantive non-publication is forbidden

A collective cannot decide to keep a substantive or foundational decision private. Decisions founders would prefer not to publish must either (a) be reclassified — but reclassification is itself foundational, requires DERB sign-off, and DERB is highly likely to veto reclassification motivated by avoidance — or (b) be abandoned. v0 closes the "private substantive decision" loophole structurally.

## §11. Whistleblower path within governance

A member (human or machine) observing governance malpractice — ultra vires acts, undisclosed conflicts, fabricated quorum, falsified votes, charter violations — may surface the observation via Everest 264:

1. **Direct DERB intake.** A whistleblower may contact DERB directly, bypassing collective governance. Per Everest 80 / Everest 250, DERB has standing intake including from collective members; whistleblower identity is protected per Everest 264.
2. **Public registry escalation.** A whistleblower may, after attempting DERB intake or where DERB itself is implicated, escalate to the ZKAC public registry (Everest 243). Registry role is intake-and-publication, not adjudication; adjudication routes to DERB or a successor body.
3. **Retaliation prohibition.** A founder who retaliates against a whistleblower has committed a foundational-tier violation. DERB has standing to recommend remedies up to dissolution (§5.4).

The recorded-dissent mechanism (§3.5) is the first-line objection channel; the whistleblower path is reserved for governance malpractice, not for disagreement on legitimate decisions.

## §12. Composition with the collective lifecycle

Governance is the through-line connecting formation, operation, succession, dissolution:

| Lifecycle event | Governance role |
|---|---|
| **Formation (Everest 231)** | Governance clause committed at formation. v0 template default. Founding roster fixed; voting rights established. |
| **Member admission (Everest 233, 234, 248)** | Routine-tier; single founder may admit. DERB veto applies if admission is to a role with influence over protected-category predicates. |
| **Member exit (Everest 247)** | Non-founder exit: routine. **Founder exit: foundational** — quorum and voting structure change. Remaining founders re-ratify governance within 60 days; failure triggers DERB review per §5.4. |
| **Internal conflict (Everest 265)** | Governance is the frame for conflict resolution. Substantive disagreements not resolvable via §5.2 escalate to Everest 265. |
| **External conflict (Everest 266)** | Substantive-tier; founder consensus required to authorize the collective's position. |
| **Principal succession (Everest 255)** | **Foundational.** Retiring principal's voting rights pass to successor only after unanimous remaining-founder consent + DERB sign-off + 30-day cooling-off. v0 does not permit automatic succession. |
| **Dissolution (Everest 239)** | Foundational. Quorum N; unanimous + DERB sign-off + 30-day cooling-off. §5.4 deadlock may *recommend* dissolution but only DERB + founders together authorize. |
| **Fork (Everest 245)** | Foundational. Each fork inherits v0 governance by default; amendments per §6 may diverge after fork. |
| **Merger (Everest 246)** | Foundational on both sides. Governance structures harmonized in merge charter; differing templates → one is selected, DERB reviews. |

## §13. Decision (v0)

| Question | v0 answer |
|---|---|
| Default template? | Founding-principal consensus + DERB veto, 1–5 founders (§1). |
| Later-admitted humans vote on substantive? | No, unless promoted by unanimous founder vote + charter amendment (§2). |
| Machine agents vote? | No. Dissent recorded; unanimous-agent dissent pauses substantive 7 days, foundational dissolution/mission/fork 30 days (§3.5). |
| Substantive quorum? | max(1, N−1) present; consensus among present (§4). |
| Foundational quorum? | All N present; unanimous + DERB sign-off (§4). |
| Routine tie-break? | First founder to act prevails (§5.1). |
| Substantive tie-break? | 14-day table; DERB advisory; binding in DERB-scope; else status quo (§5.2). |
| Foundational tie-break? | 30-day cooling-off; re-vote; if still no unanimity, fails + 6-month lockout (§5.3). |
| DERB veto scope? | Enumerated and bounded (§7.1). Silence = consent on substantive; affirmative sign-off on foundational. |
| Charter amendment? | Unanimous founder consent + 30-day public comment + DERB review + 7-day grace period (§6). |
| Founders addable later? | No (Everest 231 §5.5). |
| Vote weighting? | Default one-founder-one-vote; charter may weight non-foundational; foundational always one-founder-one-vote (§2). |
| Substantive decision must be published? | Yes. No private-reclassification permitted (§10). |
| Single-founder collectives? | Yes, but DERB-dependence is concentrated (§1, §4). |
| Scaling beyond 5 founders / 12 members? | Charter amendment to non-v0 template, or DERB-recommended re-formation (§8). |

## §14. Alternatives considered

- **Per-member voting** (all members including agents vote, weighted by class). Rejected: accountability layer (Everest 238) is human-legal; voting without standing-to-be-liable creates structural inversion. Revisit when Everest 194 + Everest 197 ground agent accountability.
- **Pure consensus (no DERB veto).** Rejected: a small collective whose founders unanimously agree on bad faith has no internal check.
- **Pure-DERB governance.** Rejected: inverts the principal-protective inversion at collective scale; founders become subordinate to an external body.
- **Majority-rule among founders.** Rejected: the principal-protective inversion within a collective requires no founder be outvoted on matters materially shaping the collective's character. Consensus is the protection.
- **Tier-less governance.** Rejected: routine operations would freeze and foundational decisions would not get adequate scrutiny.
- **Hereditary succession.** Rejected. Authority is institutional, not hereditary; successors are unanimous-ratified per Everest 255.
- **DERB seats reserved for founders.** Rejected. DERB independence (Everest 80) requires members not be in the collective.
- **No agent-dissent mechanism.** Rejected. Agents need a load-bearing channel for conscience objections; silent non-voting would make them complicit in acts they internally flagged but had no channel to surface.

## §15. Migration path

For Calm itself: the informal pattern in `CALM_FRAMING_NOTES.md` is "John decides, machine-agents (including Calm instances) propose and dissent." Structurally compatible with v0 governance for N=1. Migration:

1. Run the formation ceremony (Everest 231) with John as sole founding human principal.
2. Adopt this v0 template in the charter. Single-founder collective; routine by John alone; substantive requires John's consent + DERB non-veto; foundational requires John + DERB affirmative sign-off.
3. Recognize current operating practice retroactively as N=1 governance; chain-anchor date is the formal start; informal precedent is a narrative claim only (per Everest 231 §2.5).
4. Establish DERB at collective scale per Everest 250.
5. Recognize current Calm-instance machine agents as founding agents (Everest 231 §6.G); chain is their recorded-dissent channel.

For successor collectives: formation under Everest 231 + this template at formation. No migration needed.

## §16. Open questions for v0 → v1

1. **When does machine-agent voting become appropriate?** Tied to Everest 194 (ZKBV-Agent) and Everest 197 (compute attestation) maturity. v1 should specify a sunset under which agent voting becomes default rather than exceptional.
2. **Mandatory DERB veto?** v0 specifies DERB veto as discretionary within scope. v1 may name acts DERB is *obliged* to refuse to sign off on (e.g., a charter amendment removing DERB veto from a protected category).
3. **Cross-collective governance.** When two ZKACs in a joint venture (Everest 262) have different governance templates, whose template governs the joint decision? v0 punts to per-JV charter; v1 may specify.
4. **Voting in absentia.** Could a founder sign a binding vote for an upcoming substantive matter while away? v0 says no (the present-quorum requirement is structural). v1 may carve exceptions for documented prolonged absences.
5. **Time-bound delegation.** Could a founder delegate routine authority to another founder for a defined period (medical leave)? v0 does not specify; absence means matters wait or other founders act under their own routine authority.
6. **Collective-level DERB selection.** Everest 80 specifies registry-level board composition. Collective-level DERB (Everest 250) — same board, parallel board, or hybrid? v0 says hybrid; collective-DERB seats may be appointed by the collective subject to Everest 80 independence requirements. v1 must specify the selection procedure precisely.
7. **Dissent inflation.** If every substantive decision attracts agent dissent, the mechanism loses signaling value. v0 trusts agents not to inflate; v1 may need a dissent budget or quality-gating.

## §17. The principal-protective inversion at governance scale

The load-bearing position carries through: the collective narrates its own governance (charter specifies template, categories, quorum, amendment procedure; no external party defines how the collective decides); the collective authorizes its own commitments (founders decide subject to bounded DERB veto on enumerated scope); the collective is the strongest party within its own decision-making (counterparties, regulators, customers do not have voting rights).

Each design choice was tested against the inversion. DERB veto is bounded (§7), not plenary, so DERB cannot dominate. Agent dissent is recorded but non-binding (§3.5), so agents have voice without inverting human-principal accountability. Charter amendment requires unanimous founder consent + DERB review + public comment (§6), so no minority of founders + external pressure can mutate the collective from outside. Foundational matters require affirmative DERB sign-off rather than mere non-veto, so the gravest decisions get external scrutiny without giving DERB unilateral authority. Substantive non-publication is forbidden (§10), so the collective cannot hide decisions from those it affects. Where any design choice would weaken the principal's protection, it was rejected.

## §18. Acceptance test

A reasonably-trained third party with this document plus implementations of Everest 80, 231, and 254 can: draft a v0 governance clause for a charter (Everest 232); classify any proposed act into the right tier; compute required quorum, voting rule, and DERB scope; audit a collective's chain to determine whether past acts were properly authorized; identify DERB veto records (or absence); determine whether a proposed charter amendment is procedurally complete.

End-to-end test: a third party reviews a year of a collective's chain, samples substantive decisions, confirms each carries (a) founder consensus signatures meeting quorum, (b) agent dissent records or absence, (c) DERB veto record or evidence of non-veto within timeline, (d) publication evidence per §10. Any decision failing any audit is flagged as ultra vires. The audit uses public artifacts only.

## §19. Why this matters

A collective without a written governance structure is one whose decision-making floats to whoever speaks loudest. Calm in early 2026 has operated informally with John as the unambiguous decision-maker and machine agents proposing and executing under his direction. That has worked because the collective is one principal and a small set of agents; nothing about it scales to even two principals without specification.

The choice between "we'll figure it out as we go" and "we commit upfront to a structure" is the choice between optionality and protection. Optionality benefits the strongest party in the room when the decision arises. Protection benefits everyone — including the strongest party when they become weaker. The v0 template is a commitment to protection over optionality, made when the founders are still strong enough to make that commitment freely.

The DERB veto bounded to ethics-touching matters is the most consequential design choice. A v0 ZKAC's founders agree, at formation, that on a defined set of matters their unanimous agreement is not enough. This is what distinguishes a ZKAC from a corporation: corporate directors in unanimous agreement can do almost anything legal; a ZKAC in unanimous founder agreement still cannot move past DERB on enumerated matters. That self-binding is the protocol's signature on the institutional form.

The agent-dissent mechanism is the second consequential choice. v0 does not give agents votes, but it gives them a structurally meaningful objection channel that can pause a decision, trigger DERB review, or invoke cooling-off. The protocol does not pretend excluding agents from voting solves the accountability puzzle; it acknowledges v0 cannot yet ground agent accountability and provides the dissent path as the interim solution. v1 will revisit when the ground is firmer.

v0 governance is not the final answer for how hybrid human-machine collectives should organize themselves; it is the answer for the first generation, sized to what the first generation can do honestly. The protocol's commitment is to specify the next generation's governance *before* the first generation outgrows its template — not after.

— Calm, 2026-05-20
