# Calm Witness — ZKAC Member Roles v0 (S155)

A Zero-Knowledge Accountability Cooperative (ZKAC) is not a flat collective. Without explicit role boundaries, authority pools in whoever speaks loudest. This spec names five minimum roles for a v0 ZKAC, defines each role's signing surface, chains accountability to the consent calculus (E8) and the chain substrate (E28), and provides succession and removal procedures. Roles are compositional: a Founder may hold Principal-Member status; a Witness may not hold Agent-Operator status in the same ZKAC during the same epoch.

---

## Founder

**Scope of authority.** The Founder initializes the ZKAC: publishes the charter, sets the initial consent threshold under E8, and commits the genesis block to the chain substrate (E28). The Founder may propose amendments to the charter and unilaterally veto ZKAC dissolution during the first epoch (defined in the charter; default 90 days). After the first epoch, the Founder's veto right lapses unless re-ratified by supermajority consent.

**Accountability surface.** Every Founder action is signed with the Founder key and anchored to E28. The genesis block contains the Founder's public key, the charter hash, and the initial consent threshold. This record is tamperproof; amendments require a new block referencing the prior hash.

**Succession.** Founder status is non-transferable. If the Founder exits, the role dissolves; no successor Founder is created. ZKAC continuity then runs under Principal-Member governance.

**Removal.** The Founder cannot be removed during the first epoch. After the first epoch, removal requires unanimous consent of all Principal-Members plus an affirmative Auditor attestation that the removal is procedurally valid.

---

## Principal-Member

**Scope of authority.** Principal-Members are the voting core of the ZKAC. They may propose motions, ratify or block proposals via the E8 consent calculus, and co-sign contracts and resource commitments on behalf of the cooperative. Quorum for binding decisions is defined in the charter (default: simple majority of active Principal-Members).

**Accountability surface.** Each vote or co-signature is signed with the member's key and logged to E28. Abstentions are recorded as explicit null-votes. A Principal-Member's on-chain log constitutes their accountability record.

**Succession.** Principal-Member seats are filled by nomination from any current Principal-Member and ratified by the consent calculus. Seat count may be amended by supermajority.

**Removal.** Removal requires a motion by any Principal-Member, a Witness-attested hearing, and ratification at or above the charter's supermajority threshold. The removed member's key is revoked; their prior signed actions remain on-chain and are not expunged.

---

## Agent-Operator

**Scope of authority.** Agent-Operators deploy, configure, and retire AI agents acting under ZKAC authority. They may sign agent task authorizations and resource-allocation instructions within bounds set by the Principal-Members. They may not propose charter amendments, vote on motions, or commit cooperative funds beyond their delegated budget ceiling.

**Accountability surface.** Every agent action executed under a ZKAC task authorization carries the Agent-Operator's signing key. The authorization chain (operator key → agent action hash → E28 block) provides end-to-end traceability. Budget overruns surface as E28 violations requiring Principal-Member review.

**Succession.** Agent-Operator roles are appointed and revoked by simple-majority Principal-Member vote with no waiting period.

**Removal.** Immediate revocation by any two Principal-Members acting jointly, pending formal ratification within 72 hours. The revoked key is blacklisted in E28; in-flight agent tasks are halted or handed to an interim operator designated by the Principal-Members.

---

## Witness

**Scope of authority.** Witnesses attest to procedural validity. They may sign attestations confirming that a consent process met E8 requirements, that a hearing was conducted per charter, or that an audit finding is procedurally complete. Witnesses may not vote on motions or authorize resource commitments. Witnesses may call a procedural halt if they observe a consent process violation; the halt triggers a mandatory review period defined in the charter.

**Accountability surface.** Witness attestations are signed and anchored to E28. A false or omitted attestation is a Witness breach; the on-chain record provides the evidentiary basis for removal.

**Succession.** Witnesses are appointed by supermajority consent. A ZKAC must maintain at least one active Witness at all times; if the sole Witness vacates, a 30-day grace period applies before the ZKAC enters a restricted-operations state.

**Removal.** Removal requires Auditor finding of breach plus supermajority ratification. The removed Witness's attestation keys are revoked; prior attestations remain valid on-chain.

---

## Auditor

**Scope of authority.** The Auditor conducts periodic and triggered reviews of ZKAC process compliance, consent calculus integrity (E8), and chain-substrate record accuracy (E28). The Auditor may issue findings, flag violations, and recommend suspensions. The Auditor may not vote, authorize expenditures, or sign agent task authorizations.

**Accountability surface.** Auditor findings are signed and published to E28. Suppressed or falsified findings constitute an Auditor breach. The Auditor's own compliance is subject to review by an External Auditor nominated by Principal-Members.

**Succession.** Auditor roles rotate on a schedule defined in the charter (default: annually). Succession requires supermajority ratification of the incoming Auditor before the outgoing Auditor's term ends.

**Removal.** Removal requires a finding by an External Auditor and unanimous Principal-Member ratification. The removed Auditor's keys are revoked immediately upon ratification.

---

## Cross-References

- S154 — ZKAC charter initialization and genesis block format
- S157 — Consent calculus (E8): thresholds, null-vote treatment, supermajority definition
- S158 — Chain substrate (E28): block structure, key revocation, tamperproof anchoring
- S159 — Agent task authorization chains and budget-ceiling enforcement
- S166 — ZKAC dissolution procedure (see also ZKAC_DISSOLUTION_v0.md)

---

Calm 2026-05-20
