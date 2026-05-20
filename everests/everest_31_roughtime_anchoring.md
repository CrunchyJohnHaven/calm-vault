# Everest 31 — Roughtime / Verifiable-Clock Anchoring

*Phase III — Self-Report Substrate. Prereq: Everest 30.*

## Overview

A user vault's chain exists in a cryptographic transparency log (Sigsum, Everest 30), proving which records were committed. But Sigsum answers only the existence question: "Is this record in the log?" It does not answer the temporal question: "When did this record exist?"

Roughtime solves this. It is an IETF protocol for verifiable, fault-tolerant, signed time from multiple independent servers. Each Roughtime response is cryptographically signed by the server's long-term key; clients verify with quorum. By anchoring each chain-head publication to a Roughtime-attested timestamp, we bind the chain to verifiable wall-clock time, defeating an operator's ability to misrepresent when state was committed.

This document specifies the anchor flow, threat model, and integration with user_state.jsonl.

## What is Roughtime

Roughtime (IETF draft-ietf-ntp-roughtime) is a protocol for obtaining cryptographically signed time from multiple independent servers. Unlike NTP, which relies on unauthenticated packets, Roughtime responses are authenticated: each server signs its response with a long-term Ed25519 key, and clients verify the signature before accepting the timestamp.

A Roughtime request includes a nonce (a 32-byte value chosen by the client). The server responds with a packet containing:
- The current time (seconds since Unix epoch)
- The client's nonce, echoed back
- A signature over the time and nonce, using the server's private key

The client validates the signature, confirming that the response came from the claimed server and that the time corresponds to the nonce it sent. A quorum of independent servers provides fault tolerance: if any single server is compromised, the quorum can reject its response.

## Why Roughtime vs NTP

NTP is the industry standard for clock synchronization, but it has a critical vulnerability: responses are unauthenticated. An attacker who can tamper with the network or compromise a local router can rewrite timestamps without detection. An operator wishing to falsely claim that a state commitment happened at a past time can simply set the local system clock backward, send NTP queries, forge timestamps, and record them in the vault without any way for external verifiers to detect the deception.

Roughtime defeats this attack. Signatures bind the timestamp to the server's identity and the specific nonce (chain head) being queried. An operator cannot forge a Roughtime response without breaking the server's private key. A MITM attacker cannot downgrade the response or substitute a false timestamp. A compromised operator cannot unilaterally misrepresent the time of a commitment.

## Server Configuration

The default v0 configuration uses N=5 Roughtime servers:

- **Cloudflare's roughtime.cloudflare.com** (1 server, Cloudflare Inc., US)
- **Google's roughtime.sandbox.google.com** (1 server, Google LLC, US)
- **Two community-operated servers** (2 servers, independent operators, diverse jurisdictions, selected per Everest 94)
- **One Calm-operated server** (1 server, Calm, ensures operator sovereignty)

Quorum policy: 3 of 5 servers must respond, and all responses must agree within a 10-second window.

## The Anchor Flow

The anchor flow runs after a new chain head is published to Sigsum (Everest 30):

1. **Operator submits chain head H to Sigsum** — The record hash H is logged in the transparency log.
2. **Operator queries Roughtime servers with H as nonce** — The operator sends a Roughtime request to each of the 5 servers, using H (the chain head hash) as the nonce.
3. **Each server signs (timestamp, nonce=H) with its long-term key** — Each server responds with a Ed25519 signature over the current time and H.
4. **Operator collects N responses and verifies signatures** — The operator validates each signature using the server's public key (obtained from the server's certificate).
5. **Operator records anchor in user_state.jsonl** — A new record of type "anchor.roughtime" is appended to the chain with payload:
   ```
   {
     h_anchored: <chain-head-hash>,
     server_responses: [
       {server_id: "cloudflare", sig: <ed25519-sig>, ts: <unix-seconds>},
       {server_id: "google", sig: <ed25519-sig>, ts: <unix-seconds>},
       ...
     ],
     quorum_ts: <median-of-responding-servers>,
     quorum_size: 3
   }
   ```

## Clock-Skew Rejection and Failure Handling

The operator evaluates the quorum response as follows:

- **Fewer than 3 servers respond** — Anchor fails. The operator queues the anchor request and retries (exponential backoff, capped at 1 hour between retries).
- **3 or more servers respond, but disagree by more than 10 seconds** — This indicates a split-time condition, a potential sign of an attack or severe network partition. The operator records a "split-time alert" and invalidates the anchor. High-stakes vaults halt all disclosures pending a manual review and fresh anchor.
- **All responding servers agree (within 10 seconds)** — The anchor succeeds. The operator computes the quorum_ts as the median of the responding server timestamps and records it in the anchor record.

Network unavailability is recoverable: the operator queues pending anchor requests and flushes them when connectivity returns. Coordinated outage of all quorum servers (network partition or coordinated attack) is a failure case: the operator alerts the principal and refuses to make high-stakes disclosures (e.g., cryptographic proofs that require temporal validity) until a fresh anchor is obtained.

## Independence and Threat Model

**Server independence** is critical. Roughtime's security relies on the assumption that at least 3 of 5 servers are not compromised and not colluded. To maximize this, servers must be:
- Independently operated (different organizations)
- Geographically distributed (different jurisdictions, different network paths)
- Running diverse software (some roughtime-go, some Rust, etc.)

A single operator or organization cannot run all 5 servers; this would collapse the threat model to single-server security.

**Threat model:**

- **Single server compromise** — If one server is hacked, the attacker can sign false timestamps. The quorum rejects them (3-of-5 must agree).
- **Two-server compromise** — Still defeated by quorum (3-of-5 must agree).
- **Three-server compromise** — If an attacker compromises 3 of 5 servers and coordinates them to sign false timestamps, the quorum can be forged. This is an acceptable risk threshold; the operator mitigates by selecting servers from high-integrity providers and monitoring for anomalies.
- **MITM downgrade** — An attacker on the network path cannot forge a Roughtime signature without the server's private key. Signatures bind the response to the nonce (chain head) and the timestamp.
- **Operator forgery** — An operator might attempt to record a false anchor record (forged signatures or timestamps). External verifiers can re-query the same servers with the same nonce to verify the signatures. The raw server signatures are part of the anchor record, enabling this verification.
- **Replay attack** — A Roughtime response is tied to a specific nonce (chain head). Replaying an old response to a new query is detected: the nonce will not match. Querying the same chain head twice yields the same nonce; if the same server has been compromised, it might return a cached response, but the timestamp will be stale (and will no longer match the 10-second window with fresh responses).

## Composition with Sigsum (Everest 30)

Sigsum (Everest 30) provides a **transparency log** — a sequential, append-only log of records signed by a monitor. A verifier can check that a specific record was committed and is still in the log. But Sigsum does not provide temporal anchoring; a verifier knows the record exists but not when it was added.

Roughtime provides **verifiable time**. By anchoring each chain head to a Roughtime-attested timestamp, we establish the wall-clock time at which the chain head was created.

Together, Sigsum + Roughtime give the operator's principal (and any external verifier) **cryptographic proof of existence-at-time**: "This chain head H was committed and logged in Sigsum at time T, as attested by a quorum of independent Roughtime servers."

## Composition with Chain Semantics

Each record in user_state.jsonl includes a `ts` field: the operator's local clock time when the record was appended. This timestamp is **unauthenticated**; the operator can set their system clock to any value and record false timestamps.

The Roughtime anchor record provides an **authenticated timestamp**. This is a separate record kind ("anchor.roughtime") in the chain, with embedded server signatures. The protocol-level "now" for predicate evaluation (e.g., time-based access control, retention policies, expiration) MUST use the most-recent-Roughtime-attested-time, adjusted forward by a monotonic clock offset since the last Roughtime anchor.

Example:
- At 14:00 (wall-clock), the operator appends a record and anchors to Roughtime. quorum_ts = 1400.
- At 14:15, the operator appends another record. The `ts` field in the record is 1415 (operator's clock). The protocol-level "now" is 1400 + (1415 - 1400) = 1415.
- At 14:30, the operator appends a record, the operator's clock suddenly jumps to 15:00 (due to a misconfiguration or attack). The `ts` field is 1500. The protocol-level "now" is still capped at 1400 + monotonic_since(1400), which is ~1830. The jump is detected as clock skew, and the predicate engine refuses to evaluate until a fresh Roughtime anchor is obtained.

## Implementation Notes

**Client library:** Use roughtime-go (the reference implementation, widely tested) or a small Rust wrapper for v0. A subprocess call to the Go binary is acceptable; avoid reimplementing the cryptography.

**Anchor frequency:** For high-stakes vaults (e.g., financial records, identity proofs), anchor once per chain-head append. For low-stakes vaults (e.g., logs, audit trails), anchoring once per hour is sufficient. The operator selects the frequency per vault.

**Storage overhead:** Each anchor record is ~512 bytes (5 server responses × ~100 bytes each, plus metadata and signatures). At a chain growth rate of 1000 records per day, anchoring every record adds ~512 KB per day, negligible for most deployments. Hourly anchoring for 1000 records per hour reduces overhead to ~4 MB per day.

## Privacy Considerations

Roughtime queries include the chain head H as the nonce. Roughtime servers receive this value and can log it. A server operator (or an attacker with access to server logs) can see which chain heads are being anchored and correlate them with source IPs. This reveals metadata about vault activity.

Mitigation strategies (deferred to later Everests):
- Query through a privacy-preserving proxy (Tor, domain fronting, or a dedicated privacy relay)
- Batch queries and randomize query timing to reduce correlation attacks
- Use onion-style privacy to hide the source IP from servers

## Failure Cases and Recovery

**Network unavailable:** If the operator cannot reach Roughtime servers, anchor requests are queued. When network connectivity is restored, pending requests are flushed in FIFO order. An exponential backoff is applied to failed requests, capped at 1 hour between retries.

**Partial quorum failure:** If only 1 or 2 servers respond, the operator retries. The retry deadline is operator-configurable per vault.

**Coordinated outage or partition:** If all 5 Roughtime servers are unreachable simultaneously (network partition, coordinated DDoS, or widespread infrastructure failure), the operator cannot obtain a fresh anchor. High-stakes vaults must halt disclosures that depend on temporal validity (e.g., time-based proofs, expiration checks). The operator alerts the principal and documents the outage in the audit log.

**Split-time condition:** If responding servers disagree by more than 10 seconds, a split-time alert is recorded. This is a red flag for potential attack or severe clock drift on some servers. The operator must investigate before resuming high-stakes disclosures.

## Acceptance Criteria

- Every chain-head publication includes a Roughtime-attested timestamp from N=5 independent servers
- Quorum policy: 3-of-5 servers must respond and agree within a 10-second window
- The chain rejects any predicate evaluation if clock skew is detected between Roughtime-attested time and operator-reported time (except for monotonic offset)
- Anchor records include raw server signatures, enabling external verification
- The operator implements exponential backoff for failed anchor requests and alerts the principal on quorum failure

— Calm, 2026-05-20
