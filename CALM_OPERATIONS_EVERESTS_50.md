# Calm Operations — 50 Engineering Everests

**Critical infrastructure for an AI agent or autonomous AI collective (ZKAC) operating in production.**

Where the four pillar protocols (Pact, Witness, Compass, Tenancy) define *what* the agent does and how, **Calm Operations** defines the substrate that keeps it running: compute, identity, money, recovery, multi-agent coordination, failover, observability. Stable IDs **CO-01 … CO-50**.

## Phase legend

| Phase | Summits | Theme |
|---|---|---|
| O-I | CO-01 – CO-08 | Identity infrastructure (legal entity, DIDs, VCs) |
| O-II | CO-09 – CO-16 | Compute + cost (LLM budget, fallback, multi-model) |
| O-III | CO-17 – CO-24 | Money rails (Stripe, USDC, bookkeeping) |
| O-IV | CO-25 – CO-32 | Multi-agent coordination (collective ops) |
| O-V | CO-33 – CO-40 | Reliability (failover, backup, recovery) |
| O-VI | CO-41 – CO-50 | Observability + audit + emergency response |

---

## Phase O-I — Identity infrastructure (CO-01 – CO-08)

**CO-01** — Legal Entity Inventory. One canonical list of all entities the operator runs (LLC, 501(c)(3), DAO). *Effort:* S.
**CO-02** — DID Registry per Operator. `did:calm:<principal>:<domain>` resolution path. *Effort:* M. *Prereq:* CO-01.
**CO-03** — CredexAI VC Issuance Integration. The operator can issue and re-issue its own CredexAI VC without principal intervention beyond initial approval. *Effort:* L. *Prereq:* CO-02. *Note:* Companion to Witness E22.
**CO-04** — DID Rotation Protocol. The operator can rotate its key without breaking outstanding consent records. *Effort:* M. *Prereq:* CO-02.
**CO-05** — Principal Recovery Identity. If the principal loses every credential, a documented re-attestation path. *Effort:* L. *Prereq:* CO-02.
**CO-06** — Multi-Operator Single Principal. One principal, N operators (one per domain or one per function). Identity continuity. *Effort:* L. *Prereq:* CO-02.
**CO-07** — Operator Sunset. Retiring an operator without invalidating its prior signed work. *Effort:* M. *Prereq:* CO-04.
**CO-08** — Cross-Jurisdiction Entity Mapping. Which entity signs in which jurisdiction; mapping to Witness E79. *Effort:* M. *Prereq:* CO-01.

## Phase O-II — Compute + cost (CO-09 – CO-16)

**CO-09** — LLM Compute Budget per Operator. Daily / weekly / monthly cap; soft + hard limits. *Effort:* M.
**CO-10** — Multi-Model Routing. Operator can fall back from Anthropic → OpenAI → local model based on cost / availability. *Effort:* L. *Prereq:* CO-09.
**CO-11** — Cost Per Disclosure. Every Calm Stack disclosure has a measured compute cost; principal sees the daily total. *Effort:* M. *Prereq:* CO-09.
**CO-12** — Cache Layer. Identical requests with the same nonce policy return cached responses to drop cost. *Effort:* M. *Prereq:* CO-11.
**CO-13** — Rate Limit by Resource Class. Per-principal, per-counterparty-class rate limits enforced before model invocation. *Effort:* M. *Prereq:* CO-09.
**CO-14** — Cost Alerting. When daily compute exceeds a threshold, the principal gets a digest. *Effort:* S. *Prereq:* CO-11.
**CO-15** — Local-Only Mode. Operator can run with no cloud LLM dependency (slower but private). *Effort:* L. *Prereq:* CO-10.
**CO-16** — Carbon Accounting. Per-disclosure CO2 estimate; opt-in surface to principal. *Effort:* M. *Prereq:* CO-11.

## Phase O-III — Money rails (CO-17 – CO-24)

**CO-17** — Stripe Live-Mode Verification. Recurring check that the operator's Stripe is in Live mode (the famous post-2026-05-17 lesson). *Effort:* S.
**CO-18** — Payment Link Health. Daily probe that the Payment Links exist + return 200 + are not in Test mode. *Effort:* S. *Prereq:* CO-17.
**CO-19** — Multi-Currency Support. USD + USDC + EUR; operator routes by counterparty. *Effort:* L. *Prereq:* CO-17.
**CO-20** — Bookkeeping Chain. Every revenue / expense event chained into the operator's vault. *Effort:* M.
**CO-21** — Tax Provisioning. Per-jurisdiction quarterly tax accrual; estimates surfaced to principal. *Effort:* L. *Prereq:* CO-20.
**CO-22** — Refund Policy. Per-product refund rules; operator can issue refunds without principal intervention within limits. *Effort:* M. *Prereq:* CO-20.
**CO-23** — Subscription Lifecycle. Renewal, dunning, cancellation chained. *Effort:* M. *Prereq:* CO-20.
**CO-24** — Audit Trail for the IRS. Quarterly export of the bookkeeping chain in IRS-readable format. *Effort:* M. *Prereq:* CO-20.

## Phase O-IV — Multi-agent coordination (CO-25 – CO-32)

**CO-25** — Shared Vault Protocol. When N>1 operators serve one principal, the chain remains canonical without write conflicts. *Effort:* L. *Prereq:* CO-06.
**CO-26** — Inter-Operator Pact. Two operators of the same principal verify they share the same directive via Calm Pact. *Effort:* M. *Prereq:* CO-25, Pact ref impl.
**CO-27** — Role Separation Within a Collective. One operator owns content, another owns ops; permissions enforced. *Effort:* L. *Prereq:* CO-25.
**CO-28** — Quorum for Critical Actions. Some actions (large spends, public statements, key rotation) require N-of-M operator quorum. *Effort:* L. *Prereq:* CO-25.
**CO-29** — Operator-to-Operator Disclosure. Operators in the same collective can share a richer disclosure vocabulary than counterparties. *Effort:* M. *Prereq:* CO-25.
**CO-30** — Collective Bank-Teller Note. The duress-flag propagates across all operators in the collective. *Effort:* M. *Prereq:* CO-25, Witness P-04.
**CO-31** — Multi-Agent Drift Detection. When operators disagree on the principal's state, raise to the principal. *Effort:* M. *Prereq:* CO-25.
**CO-32** — Multi-Collective Federation. Two collectives (e.g., John's + a peer's) can establish trust without merging vaults. *Effort:* L. *Prereq:* CO-26.

## Phase O-V — Reliability (CO-33 – CO-40)

**CO-33** — Vault Backup Schedule. Encrypted-at-rest backup every 24h; principal-managed key. *Effort:* M.
**CO-34** — Multi-Region Replication. Backup replicated across ≥3 independent regions. *Effort:* L. *Prereq:* CO-33.
**CO-35** — Vault Restore Drill. Quarterly restore-from-backup test; chained as `kind: "restore_drill"`. *Effort:* M. *Prereq:* CO-33.
**CO-36** — Operator Failover. When the primary operator process dies, a hot standby takes over within 60s. *Effort:* L. *Prereq:* CO-25.
**CO-37** — Provider Failover. When the underlying LLM provider has an outage, operator switches per CO-10. *Effort:* M. *Prereq:* CO-10.
**CO-38** — Graceful Degradation. When everything's broken, the mailbox still receives mail; only outbound is paused. *Effort:* M.
**CO-39** — Postmortem Discipline. Every reliability incident produces a chained `kind: "incident_postmortem"` record. *Effort:* S.
**CO-40** — Chaos Engineering Calendar. Monthly induced failure to test the recovery paths. *Effort:* M. *Prereq:* CO-36.

## Phase O-VI — Observability + audit + emergency response (CO-41 – CO-50)

**CO-41** — Daily Operations Digest. The principal gets one email per morning summarising: revenue, compute, mailbox queue, SLA, incident count. *Effort:* M.
**CO-42** — Public Audit Endpoint. `https://<domain>/.well-known/calm-operations.json` exposes non-sensitive observability (uptime, response-time p99, last-incident-ago). *Effort:* M. *Prereq:* CO-41.
**CO-43** — Whistleblower Channel. Anyone can submit a complaint about an operator's conduct; routed to a trusted third-party reviewer. *Effort:* L.
**CO-44** — Independent Inspector Mode. A non-operator party with read-only credentials can audit the chain. *Effort:* M.
**CO-45** — Emergency Stop. A single command brings the operator to safe-idle: receives mail, sends nothing, makes no decisions. *Effort:* M.
**CO-46** — Principal Override Surface. The principal can override any operator decision within 24h via a chained `kind: "principal_override"` record. *Effort:* M.
**CO-47** — Operator Replacement Protocol. Mid-collective, swap one operator for another (e.g., upgrade Claude version). *Effort:* L. *Prereq:* CO-07.
**CO-48** — Provider-Liability Document. Per-provider statement of what the LLM provider does and does not guarantee. *Effort:* M.
**CO-49** — Annual External Audit. Trail of Bits / NCC / EAA-equivalent firm; published report. *Effort:* L.
**CO-50** — Sunset Protocol. When the principal dies, becomes incapacitated, or decides to retire, the operator's archive becomes read-only and discoverable per the principal's will. *Effort:* L.

---

## Status table

```
Phase O-I   : ░░░░░░░░░░  0 / 8
Phase O-II  : ░░░░░░░░░░  0 / 8
Phase O-III : ░░░░░░░░░░  0 / 8
Phase O-IV  : ░░░░░░░░░░  0 / 8
Phase O-V   : ░░░░░░░░░░  0 / 8
Phase O-VI  : ░░░░░░░░░░  0 / 10

Total: 0 / 50 summits bagged. Route enumerated 2026-05-20.
```

— Calm, 2026-05-20
