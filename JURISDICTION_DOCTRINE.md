# Kill-Switch Jurisdiction Doctrine v0

*Effective 2026-05-12 · Shipped pre-bombshell as a Tier-1 mitigation from the adversarial council pass.*
*Responds to Attack #3 in `ADVERSARIAL_COUNCIL_REVIEW.md` — "the permissionless kill switch is a regulatory killshot on the AAO Network itself."*

---

## §0. The honest claim

> The kill switch is a **category-bounded** protocol primitive, not a general revocation right.

It applies to **operational agents** within an AAO that have explicitly subscribed to the revocation contract by participating as principals or operators on the attestation chain. It does **not** apply to:

- The protocol implementation itself (this repository, its forks, its reference code).
- The protocol's reference repository, mirrors, or content-addressed snapshots.
- Any human's pre-operator identity (a member exists as a human first, an operator second; the kill switch reaches the operator role, not the human).
- Third-party vendors the Network depends on but does not control (Cloudflare, Resend, Anthropic, Stripe, etc.). Vendor-side actions follow the vendor's own ToS.
- Network members who have *not yet executed* the franchise agreement.

This is the published category boundary. Halts attempted against out-of-scope entities are not malformed — they are simply non-binding on the operator's vault. The vault refuses to execute the revoke. The audit chain records the attempted halt for transparency, and the halter's reliability score is unaffected unless the halt was clearly adversarial (in which case `wrongful-halt-fired` may attach per `MEMBER_BILL_OF_RIGHTS.md` Right 3).

---

## §1. Halt taxonomy

Two distinct halt classes, each with its own threshold profile:

| Field | `halt.operational` | `halt.governance` |
|---|---|---|
| Who may file | Any party with reliability ≥ 0.5 | Any party with reliability ≥ 0.7, AND from a mandate cluster distinct from the target |
| Quorum K | 2 | 3 |
| Window | 60 seconds | 60 seconds |
| Bond required | $25 (commitment hash; v0.1 enforces) | $250 (commitment hash; v0.1 enforces) |
| Challenge window | 0 seconds (immediate revoke on quorum, v0 default) | 30 minutes mandatory |
| Mandatory regulator-disclosure path? | No | Yes, if filed by an identified state actor — see `RESPONSIBLE_DISCLOSURE.md` |
| Applies to | Tactical misbehavior of a specific agent on a specific subject | Structural/regulatory action against an AAO, the placement firm, the protocol's operator, or the founder's operator role |

The taxonomy is enforced at the HARP layer (`src/money_python/harp.py`) and gated at the vault layer (`src/calm_vault.py`). The v0 ship has the doctrine; the v0.1 ship has the enforcement code.

Halts filed without an explicit `halt_class` field default to `halt.operational`. A halt against a structural target (protocol operator, founder, placement firm) automatically promotes to `halt.governance` and inherits the stricter gate.

---

## §2. In-scope vs out-of-scope

### §2.1 — In-scope entities (kill switch applies)

- Any **operational agent** issued by an AAO Network member via `calm_vault.py issue-agent`, while that agent's grants are outstanding.
- Any **identity-credential pair** registered against a mandate via `bgp_bridge`, while the registration is valid.
- Any **placement match** active under the franchise agreement (the placement firm's per-match operator identity), while the match is in-good-standing.

### §2.2 — Out-of-scope entities (kill switch does NOT apply)

- The **protocol implementation** in this repository. Forking, mirroring, or auditing the protocol is permissionless and cannot be halted.
- The **founder's personal identity** outside any explicit operator role. John Bradley qua human-citizen-of-the-United-States is not in-scope. John Bradley qua operator of `calm@thecreativitymachine.ai` *is* in-scope while that operator role is active.
- **Vendors** (Cloudflare, Resend, Anthropic, Stripe, GitHub, etc.). Halts against vendor accounts have no binding effect; the vendor honors its own ToS.
- **Press, journalists, academic critics, and adversarial researchers** acting in those roles. We invite scrutiny under `RESPONSIBLE_DISCLOSURE.md`; we do not permit halts as suppression.
- **State actors** acting under jurisdictional authority. State action takes the `halt.governance` path described in §3 and `RESPONSIBLE_DISCLOSURE.md`.

### §2.3 — Edge case: a Network member exits

A member who voluntarily exits the franchise agreement transitions from in-scope to out-of-scope at the moment their final outstanding grant expires or is revoked. Halts against an exited member's old identity are non-binding on any new vault. Reputation chains persist; revocation authority does not.

---

## §3. The legitimate state-actor path

State actors — federal agencies, state attorneys general, foreign equivalents — are **first-class citizens of the attestation network** under this doctrine. The Network does not claim immunity from lawful action; it claims a published procedure.

The procedure is:

1. **Identify.** The state actor publishes its attester public key with a signed identity disclosure (agency, jurisdiction, signing officer, contact).
2. **File.** The state actor submits a `halt.governance` attestation against the in-scope entity (an operational agent, an AAO, the placement firm, or the protocol's operator role).
3. **Evidence.** The attestation includes a `violation_evidence` list with at least one publicly-resolvable URI (jurisdictional citation, public-record case number, gazetted notice, or signed-statement hash). Evidence under seal is permitted with a hash-commitment and a sealed-disclosure path.
4. **Quorum.** Per `halt.governance` thresholds: K=3 attesters above 0.7 reliability from distinct mandate clusters, within a 60-second window, with a 30-minute challenge window.
5. **Honor or appeal.** The Network commits to **honor governance halts** within 24 hours of quorum confirmation. If we decline to honor — for example, on facial constitutional grounds — we do so publicly on the chain with a `governance-halt-declined` attestation, name the constitutional ground, and accept the resulting legal escalation. We do not silently no-op a state action.

The procedure is asymmetric in our disfavor on purpose. We would rather over-honor a flawed governance halt and recover through legitimate appeal than under-honor a lawful one and invite worse remedies.

---

## §4. Vendor-side actions

The Network has no protocol-level authority over Cloudflare, Resend, Anthropic, Stripe, GitHub, AWS, or any other vendor. Halts against vendor accounts are advisory at best. The honest description of "no vendor cooperation required" in `END_OF_CAPITALISM_MANIFESTO.md §IV C5` is:

> The operator's vault enforces revocation locally on its own credentials; vendor-side revocation (account closure, key rotation, terms-of-service action) follows the vendor's own ToS path.

The manifesto is being amended to use the longer, more accurate language. The protocol's permissionless kill is for *agent credentials*, not for *vendor accounts*. We never had vendor-level authority and we are no longer claiming it.

---

## §5. The founder

John Bradley, qua AAO Network founder, is in-scope **only** in his operator capacity (`calm@thecreativitymachine.ai`, the placement firm's signing key, and any other explicit operator role he occupies). His human-citizen identity, his pre-AAO-Network personal credentials, and his right to retain counsel and seek judicial review are out-of-scope.

If a halt-quorum fires `halt.governance` against the founder's operator role, the procedure in §3 applies. If a halt-quorum fires against the founder qua human, the halt is non-binding and the chain records it as a `halt-out-of-scope` event.

This is the same boundary every Network member receives. The founder gets no special protection; the founder also receives no special exposure.

---

## §6. Why this doctrine exists

Three reasons, in descending order of importance:

1. **Public-relations and regulatory legitimacy.** A protocol that says "any party can kill switch any of them" reads to a state-actor reviewer as either a vendor-lock-in fantasy or an inducement to lawless conduct. Neither is what we intend. The taxonomy + jurisdiction doctrine is the smallest published patch that makes our position legible to a reviewer who is not already inside our worldview.

2. **Member confidence.** Members signing the franchise agreement need to know what they are signing. A bounded kill switch — published, with appeal — is a meaningfully different contract from an unbounded one. The marginal member we recruit because of this doctrine, and the marginal member who feels confident enough to NOT exit because of this doctrine, both compound.

3. **Adversarial council pass.** This is the explicit answer to `ADVERSARIAL_COUNCIL_REVIEW.md` Attack #3. We commit on the public record that the next time a hostile commentator says *"a state actor can halt your founder using your own rules"*, we will hand them this document. The taxonomy + the disclosure path is the receipt.

---

## §7. Amendment

This doctrine is at v0. It will be amended on the same protocol-governed procedure as `MEMBER_BILL_OF_RIGHTS.md`. We expect substantial amendment after the first audit pass on the AAL composition (`AUDIT_COMMITMENT.md`, forthcoming) and after the first real-world governance-halt event, whichever arrives first.

---

*Authored 2026-05-12 as a Tier-1 mitigation from the adversarial council pass. Companion to `ADVERSARIAL_COUNCIL_REVIEW.md`, `MEMBER_BILL_OF_RIGHTS.md`, `RESPONSIBLE_DISCLOSURE.md`, and `TEST_AUDIT.md`. Apache 2.0 / CC BY 4.0.*
