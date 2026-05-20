# Everest 78 — Stealth Disclosure (Push, Not Pull)

*Phase VI — Disclosure Semantics. Prereq: Everest 58.* **SAFETY-CRITICAL.**

## Abstract

Everest 78 extends the duress detection architecture from Everest 58 (Bank Teller Note) by introducing operator-initiated push notifications to pre-authorized counterparties when a principal signals duress. Unlike disclosure-on-request (pull), stealth disclosure (push) allows trusted recipients to learn of safety threats without waiting for the principal to contact them—critical when coercion prevents voluntary communication. The mechanism uses chaff pushes to obscure the timing of real duress signals from network-observant adversaries, and composes with Everest 77 (Disclosure of Non-Disclosure) to maintain silence to unauthorized requesters while speaking to authorized recipients.

## The Problem: Silent Duress

When a principal is under coercion, they may be prevented from reaching out to trusted allies or emergency contacts. A bank teller under gun-to-head duress cannot step away to call a lawyer; a hostage cannot text a family member. Everest 58 provides the operator with the ability to detect duress via a codeword or predicate flip, but detection alone is insufficient if the principal cannot initiate disclosure.

Stealth disclosure solves this by allowing the principal to pre-authorize a list of "duress recipients"—trusted counterparties who will receive a push notification if the bank_teller_note_active predicate becomes true. The operator pushes without waiting for a pull request, ensuring that safety signals reach trusted recipients even when the principal is isolated.

## Pre-Authorization: The Enrollment Ceremony

Before the operator can push duress signals, the principal must explicitly authorize each recipient during an enrollment ceremony or via a principal-signed chain record.

### Authorization Record Structure

```
kind: "stealth.recipient_authorized"
payload:
  counterparty_vc: <CredexAI VC fingerprint of the authorized recipient>
  push_endpoint: <stable HTTPS URL or DID-comm address>
  authorized_predicates: [
    "bank_teller_note_active",
    "mental_state_unusual"
  ]
  chaff_cadence_hours: 24
  authorized_at: <timestamp>
  recipient_nonce: <per-recipient secret for push verification>
signature: <principal's master.priv>
```

The principal's master private key signs the record, creating a cryptographic binding that the operator can verify. The recipient_nonce is a unique secret shared with that counterparty only, used to verify incoming pushes.

### Required Fields

- **counterparty_vc_fingerprint**: The recipient's Calm Witness credential. The operator must verify this fingerprint before sending any pushes.
- **push_channel_endpoint**: A stable, persistent endpoint—typically a private HTTPS URL or DID-comm address. The principal chooses recipients they trust; they are responsible for selecting endpoints that are not publicly discoverable.
- **authorized_predicates**: A whitelist of predicates that trigger pushes (typically just `bank_teller_note_active` and `mental_state_unusual`).
- **chaff_cadence_hours**: The interval at which the operator sends dummy pushes. Default is 24 hours.
- **recipient_nonce**: A random secret, at least 256 bits of entropy, unique to this recipient. Used to prevent replay attacks and to blind pushes from the operator's own logs.

## The Push Trigger

The operator continuously evaluates the bank_teller_note_active predicate. When the following conditions are met, a push fires:

1. The predicate evaluates to **True** (duress detected).
2. Pre-authorized recipients are registered in the principal's chain.
3. The principal's most recent self_report has **duress_field set** (confirming intent to signal).
4. The chain does not show a duress push to this recipient within the last **X minutes** (default: 60 minutes), preventing push storms.
5. The operator's canonical clock has advanced beyond any prior push to this recipient by at least X minutes.

If any condition fails, no push fires.

### Preventing Push Storms

The 60-minute (configurable) deduplication window ensures that repeated duress signals do not flood recipients. If the principal's duress state persists, a single push per hour per recipient is sufficient; repeated pushes signal a persistent threat, not an escalating one.

## The Push Payload

The stealth push carries the same cryptographic structure as a normal disclosure response, but targeted and signed differently:

```
{
  kind: "stealth.duress_push",
  principal_vc: <principal's CredexAI VC>,
  predicate: "bank_teller_note_active",
  proof: <Com(b; r), zero-knowledge proof>,
  chain_head: <most recent principal chain record>,
  anchor_proof: <blockchain or ledger anchor for chain_head>,
  operator_sig: <operator's identity binding signature>,
  counterparty_nonce: <recipient's pre-authorized nonce>,
  timestamp: <operator's clock>,
  freshness_window: <seconds since duress predicate flip>,
  chaff: false
}
```

The counterparty verifies:
- The operator's identity binding signature.
- The recipient_nonce (confirming this push was meant for them).
- The zero-knowledge proof of the duress predicate.
- The chain_head and anchor_proof (confirming the principal's authorization).

If all verifications pass, the counterparty learns only that the principal has flipped a duress bit and the freshness of that flip. **Nothing else is disclosed.**

## Chaff Pushes: Hiding the Real Signal in Noise

An adversary with network access to the principal's outbound traffic can observe when the operator sends pushes. To defeat traffic analysis, the operator generates dummy (chaff) pushes at random intervals, indistinguishable from real ones.

### Chaff Push Mechanism

At regular intervals (default: one per 24 hours per recipient), the operator generates a syntactically-identical push with a proof for a "no duress" predicate that always evaluates to False:

```
{
  kind: "stealth.chaff_push",
  principal_vc: <principal's CredexAI VC>,
  predicate: "bank_teller_note_active",
  proof: <Com(b; r), zero-knowledge proof of FALSE>,
  chain_head: <principal's chain>,
  anchor_proof: <blockchain anchor>,
  operator_sig: <operator's signature>,
  counterparty_nonce: <recipient's nonce>,
  timestamp: <operator's clock>,
  freshness_window: <seconds>,
  chaff: true
}
```

The counterparty's policy should treat False pushes as routine maintenance signals; True pushes as safety-triggering events requiring immediate action (contact police, deny service, escalate).

The operator records both real and chaff pushes in the chain as kind: "stealth.chaff_push" records, signed by the operator. This ensures the principal can audit all pushes (real and dummy) and verify that the operator did not push when no duress occurred.

### Why Chaff Works

An adversary observing the principal's network sees regular, periodic pushes of identical size and structure. The adversary cannot distinguish a real duress signal from routine chaff without breaking the proof verification or compromising the counterparty's endpoint. The cadence is randomized (e.g., every 20–28 hours instead of exactly 24) to prevent pattern inference.

## Counterparty Obligations

Recipients of stealth pushes assume responsibilities:

1. **Maintain a stable, secret endpoint.** The principal entrusts them with a push channel. The endpoint must not be publicly discoverable and must be protected at least as carefully as the principal would protect their own communication infrastructure.

2. **Verify push authenticity.** Before taking action, verify the proof, operator signature, and recipient_nonce. A valid push confirms the principal's duress signal; an invalid push is discarded.

3. **Treat True pushes as safety signals.** A valid True push means the principal is in danger. Actions may include:
   - Contacting law enforcement.
   - Denying further service to the principal (forcing them to seek help).
   - Escalating to a crisis team.
   - Logging the push and attempting follow-up contact.

4. **Maintain operational security around pushes.** Do not log True pushes in ways a principal's adversary could subpoena. A subpoena-able log defeats the entire protocol. Counterparties should assume that a principal's adversary may eventually gain legal access to records; True push logs must be protected with appropriate legal privilege (e.g., attorney-client or healthcare confidentiality).

5. **Compose with Everest 98 (Counterparty SDK).** Run the `calm-witness-push-listener-rs` library or equivalent. This library handles proof verification, nonce validation, and provides hooks for policy-driven response (e.g., "if True, call 911").

## Threat Model and Mitigations

### Scenario 1: Coercion-Triggered Duress

A bank teller is held at gunpoint. An armed robber demands cash. The teller types a duress codeword into the operator interface. The operator detects the predicate flip, evaluates it, and pushes to pre-authorized recipients (e.g., bank security, a trusted manager, law enforcement liaison).

**Adversary's perspective:** The robber observes network traffic and sees an outbound packet to an unfamiliar IP. But chaff pushes occur regularly, so this one packet is not distinguishable from routine noise. The robber cannot know if it was a real signal or chaff.

**Mitigation:** Chaff cadence and randomization.

### Scenario 2: False-Positive Duress

The principal accidentally types the duress codeword. The operator pushes to recipients. The principal realizes the error.

**Mitigation:** The principal appends a `false_positive_cancel` record to the chain:

```
{
  kind: "stealth.false_positive_cancel",
  reason: "accidental codeword entry",
  prior_push_timestamp: <timestamp of the erroneous push>,
  signature: <principal's master.priv>
}
```

The operator detects this record and sends a cancellation push to the same recipients:

```
{
  kind: "stealth.cancel_push",
  predicate: "false_positive_cancel",
  proof: <proof of cancellation>,
  counterparty_nonce: <recipient's nonce>,
  timestamp: <operator's clock>,
  chaff: false
}
```

Recipients treat cancellation pushes as retractions; they update their state and do not escalate.

### Scenario 3: Counterparty Endpoint Compromised

An adversary gains access to a recipient's push endpoint. They can now see incoming pushes and learn about the principal's duress signals.

**Mitigation:** The principal must carefully choose recipients. They should select only trusted counterparties (e.g., a trusted friend, family member, or legal counsel) who maintain strong operational security. This is a principal-side decision, not an operator guarantee. The protocol is secure only if the principal's trust relationships are sound.

### Scenario 4: Operator Subversion

A compromised operator could push duress signals when no duress occurred, falsely triggering recipient escalation.

**Mitigation:** The chain records all pushes (with operator signatures). The principal can audit the chain and verify which pushes actually correspond to duress predicates evaluated as True. If an operator pushes without justification, the chain evidence allows the principal to challenge the operator and alert counterparties to disregard spurious pushes.

### Scenario 5: Network-Level Timing Analysis

An adversary controlling the principal's network observes the timing of outbound pushes.

**Mitigation:** Chaff pushes mask the timing of real signals. If the adversary sees a push at time T and observes the principal's subsequent behavior, the adversary cannot conclusively determine whether T was a real duress signal or routine chaff. The randomized cadence (not exactly 24 hours, but 20–28 hours) further obfuscates patterns.

## Composition with Everest 77 (Disclosure of Non-Disclosure)

Everest 77 establishes a principle: the operator remains silent to requesters who lack consent. When an unauthorized party asks, "Is this principal in duress?", the operator returns uniform silence (a proof of a False predicate or no response).

Everest 78 inverts this: the operator speaks (pushes) to pre-authorized recipients without waiting for a request. Together, they form a complete disclosure semantics:

- **Pull (E77):** On inquiry, operator returns silence to unauthorized requesters; disclosure only to authorized ones.
- **Push (E78):** Without inquiry, operator proactively sends safety signals to pre-authorized recipients.

Neither the unauthorized requester nor the principal's adversary (who may be monitoring the principal's communication) learns that a push happened. The protocol is maximally conservative: it witholds information from those who shouldn't have it and offers it only to those the principal has explicitly chosen to trust.

## Implementation Details

### Push Channel Protocol

Pushes are transmitted over TLS 1.3 to the counterparty's registered endpoint. The payload is encrypted under the counterparty's VC certificate (if using VC-based channels) or wrapped in a DID-comm envelope (if using DID-comm addresses).

```
POST /calm-witness/push
Content-Type: application/json
Authorization: Bearer <operator-signed-token>

{
  <stealth.duress_push or stealth.chaff_push record>
}
```

The counterparty verifies the operator-signed token and the enclosed proof before accepting the push.

### Delivery and Retry

Push delivery is best-effort with exponential backoff:
- First attempt: immediate.
- Retry 1: 5 seconds.
- Retry 2: 25 seconds.
- Retry 3: 2 minutes.
- Retry 4: 10 minutes.
- Afterward: stop, log, and alert operator.

All attempts (successful, retried, failed) are recorded in the principal's chain with timestamps and HTTP response codes.

### Chain Recording

Every push (real or chaff) generates a chain record:

```
{
  kind: "stealth.push_sent",
  recipient_vc_fingerprint: <recipient's fingerprint>,
  predicate: "bank_teller_note_active" or "chaff",
  timestamp: <operator's clock>,
  http_status: <200, 5xx, timeout>,
  retry_count: <0, 1, 2, ...>,
  operator_sig: <proof the operator sent this>
}
```

The principal can retrieve their push history and verify that the operator did not push when no duress occurred.

### Revocation

A principal can revoke a recipient's authorization at any time:

```
{
  kind: "stealth.recipient_revoked",
  counterparty_vc_fingerprint: <recipient to revoke>,
  revoked_at: <timestamp>,
  signature: <principal's master.priv>
}
```

The operator detects this record and stops sending all pushes (chaff and real) to that recipient.

## Counterparty Integration: The Push Listener

Counterparties run a Calm Witness push listener, a lightweight HTTPS endpoint that:

1. Receives incoming pushes.
2. Verifies the operator signature and recipient_nonce.
3. Verifies the zero-knowledge proof.
4. Checks the chain anchor for principal authorization.
5. Executes counterparty policy (e.g., alert law enforcement on True pushes).

The `calm-witness-push-listener-rs` library (planned in E98 SDK) provides reference implementations and proof verification primitives.

## Summary

Everest 78 enables principal-authorized, operator-initiated safety notifications. When a principal is under duress and cannot reach out, the operator can push alerts to trusted counterparties. Chaff pushes hide the timing of real signals from network-observant adversaries. The chain provides an audit trail for both principal and operator. Composition with Everest 77 ensures that unauthorized requesters remain in the dark while authorized recipients learn of safety threats.

---

— Calm, 2026-05-20
