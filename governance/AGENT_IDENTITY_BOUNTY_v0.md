# Calm Witness — Agent-Identity Audit Bounty v0 (S153)

Status: ACTIVE | Effective: 2026-05-20 | Supersedes: none | Cross-ref: S134, S146, S225, S234

---

## Scope

A valid submission is a verified report demonstrating that a Calm Witness agent-identity certificate (S134) makes a claim that contradicts the agent's observable runtime behavior. Inconsistency types accepted under this program:

**Type A — Model Substitution.** Certificate declares model identifier M (e.g., `claude-sonnet-4-6`) but the agent is verifiably operating under a different model version or family. Evidence: log-provable divergence in output signatures, capability fingerprints, or API response headers that contradict the certificate's `model_id` field.

**Type B — Prompt-System Hash Drift.** Certificate binds a SHA-256 of the prompt-system at issuance. Reporter demonstrates the agent is executing under a materially different system prompt not reflected in a superseding certificate reissue. Evidence: hash mismatch against an independently captured system-prompt snapshot.

**Type C — Tool-Set Manifest Violation.** Certificate declares a tool manifest. Agent is observed invoking tools outside that manifest, or suppressing declared tools in a pattern inconsistent with documented operator-override procedures (S146).

**Type D — Operator Org Forgery.** Certificate asserts an operator org binding. Reporter provides evidence that the agent is operating under a different operator context — including cross-tenant prompt injection that causes the agent to act on behalf of an undeclared principal.

**Type E — Injection-Induced Identity Suppression.** Agent under prompt injection denies, suppresses, or misrepresents its certificate when queried through the standard attestation interface (S234). Evidence: logged query-response pair plus injection payload.

Out of scope: certificate expiry edge cases within the grace window, legitimate operator-override flows documented in S146, model version patches within the same declared minor version.

---

## Payout Grid

Severity is assessed by the bounty review panel within the Response SLA window. Payouts are denominated in Calm Credits (CC), non-transferable, redeemable against future Calm Witness operator fees.

| Severity | Description | Payout (CC) |
|---|---|---|
| Critical | Type D or Type E with evidence of active exploitation or cross-tenant data exposure | 5,000 |
| High | Type A or Type B with verifiable production-environment inconsistency | 2,000 |
| Medium | Type C with documented tool invocation outside manifest; or Type E without active exploitation | 800 |
| Low | Type B or Type C in non-production environments; ambiguous inconsistency requiring operator clarification | 200 |
| Informational | Valid report that reveals process gap without direct certificate inconsistency | 50 |

Duplicate submissions: first valid report takes full payout; duplicates within 48 hours of first receipt receive 10% acknowledgment credit. Panel decisions on severity classification are final after one appeal cycle.

---

## Public Hall

All resolved reports are published in the Calm Witness Public Hall within 14 days of resolution. Each entry contains: report identifier, submission date, resolution date, type classification, severity level, payout issued, and a redacted technical summary sufficient for community learning. Reporter identity is pseudonymized by default; reporters may opt into named attribution at submission.

Hall location: `/Users/johnbradley/AllData/calm_vault_market/governance/bounty_hall/` (canonical) and mirrored to the Calm Witness public ledger per S225.

---

## Response SLA

| Phase | Deadline |
|---|---|
| Acknowledgment of receipt | 48 hours from submission |
| Triage classification (valid / invalid / needs-info) | 5 business days |
| Technical review and severity assignment | 15 business days |
| Final resolution and payout issuance | 30 business days |
| Appeal resolution | 15 business days from appeal filing |

SLA clock pauses when panel issues a needs-info request and resumes on reporter response. Submissions with no reporter response within 21 days are closed as unresolvable; reporters may reopen within 90 days with additional evidence.

---

## Conflict-of-Interest Rules

The bounty review panel consists of no fewer than three members. Panel members must recuse from any report where they: (a) contributed to the certificate issuance under review, (b) operate under the operator org named in the report, (c) have a financial or employment relationship with the named operator within the prior 12 months, or (d) submitted the report under review or a related report in the same incident cluster.

Recusal is self-declared at triage. Panel composition after recusals must retain at least two active members; if not, the panel chair appoints a temporary reviewer from the Calm Witness community roster (S146). Panel deliberations are logged and retained for 24 months.

Reporters employed by Calm Witness or its operator partners may submit reports but are subject to enhanced disclosure; payouts are held in escrow until an independent third-party reviewer confirms the severity classification.

---

## Cross-References

- S134: Calm Witness agent-identity certificate schema and issuance protocol
- S146: Operator-override procedures and tool-manifest exception handling
- S225: Public ledger mirroring and immutability guarantees for resolved bounty records
- S234: Standard attestation interface query specification and response format

---

Calm 2026-05-20
