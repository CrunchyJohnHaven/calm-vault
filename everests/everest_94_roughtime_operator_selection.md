# Everest 94 — Roughtime Operator Selection

*Phase VIII — Governance & Scale. Prereq: Everest 31.*

## Overview

Everest 31 specifies the Roughtime anchor flow: after each chain-head publication to Sigsum, the principal queries N=5 independent Roughtime servers for a cryptographically signed timestamp, verifies a quorum consensus (3-of-5), and records the anchor with server signatures in user_state.jsonl. This creates a verifiable wall-clock time binding for the chain head, defeating operator clock-manipulation attacks.

The architecture is only as strong as the independence of the N=5 servers. This document specifies the selection criteria, candidate roster, quorum policy, operator commitments, and failure handling for the Calm Witness Roughtime operator network. It also defines the public verifier's built-in server roster and update mechanism.

## Problem: Why Operator Selection Matters

In Everest 31, the security model assumes at least 3 of 5 servers are not compromised and not colluded. If a principal uses servers that are—in reality—operated by the same entity or coordinating organization, the quorum fails: the adversary controls all 5 responses and can forge arbitrary timestamps.

Roughtime operator selection must prevent three failure modes:

1. **Organizational capture.** A single organization running multiple servers under different domains (geographic or subdomain hiding).
2. **Coordinated compromise.** Multiple organizations that appear independent but are actually coordinating (e.g., all hosted on the same cloud provider, sharing infrastructure, or under coercive jurisdiction).
3. **Long-term key exposure.** Servers that commit to public keys but later rotate keys without notice, breaking verifier trust and enabling key-swapping attacks.

This Everest addresses all three through a combination of vetting, operational commitment, and public verifier enforcement.

## Selection Criteria

A Roughtime server is eligible for the Calm Witness v0 roster if it meets all of the following:

### 1. Long-Term Key Public Commitment

The server operator must publicly commit the server's Ed25519 long-term public key via one or both of:

- **Sigsum transparency log.** The operator submits a "operator.roughtime.key" record to a Sigsum log (e.g., the same log used for Calm Witness transparency). The record includes:
  - Server FQDN (e.g., roughtime.example.com)
  - Ed25519 public key (64 hex characters)
  - Key version (e.g., "v1" or "2026-05-20")
  - Operator legal name and jurisdiction
  - Commitment statement: "This key is the sole long-term key for this server from inception until announced rotation."

- **DNS TXT record.** The operator publishes the key in a DNS TXT record at `_roughtime._tcp.<FQDN>` per IETF draft conventions, signed by DNSSEC if the zone supports it.

Either commitment alone is acceptable for v0; both strengthen the binding.

### 2. Uptime SLO ≥ 99.9% Over 6 Months

The operator must publish a public, auditable uptime dashboard covering the prior 6 months. Acceptable evidence:

- Uptime monitoring service (e.g., Pingdom, Healthchecks.io) with public JSON API and dashboard.
- Operator-published dashboard with daily uptime percentage and a signed attestation (operator key signature or third-party audit).
- Quarterly audit report (see below) confirming 99.9% uptime via independent probing.

Outages due to scheduled maintenance (announced ≥7 days in advance) do not count against the SLO. Unannounced outages (network cuts, hardware failure, misconfiguration) count fully.

For the initial v0 roster, we accept historical claims backed by operator assertion and spot-check via third-party probing. For renewal and scaling (v0.2+), we require continuous third-party monitoring.

### 3. Geographic and Organizational Independence

The five servers must satisfy:

- **No more than 2 servers in the same country.** This prevents a single jurisdiction from coercing all operators.
- **No more than 1 server per top-level organization.** A single corporation (including subsidiaries) can operate at most one server in the roster.
- **No more than 1 server per cloud provider and data center region.** Servers sharing the same AWS region, GCP zone, or Azure region are considered networked and fail independence.
- **No common upstream network operator or ISP.** Servers must route through different ASNs (Autonomous System Numbers) at the upstream Internet level.

Independence is verified via:
- WHOIS/RIPE lookup of IP address and ASN.
- Operational documentation from the server operator.
- Third-party network analysis (e.g., BGP routing data from public sources).

### 4. Open Server Software or Auditable Implementation

The Roughtime server must be one of:

- **roughtime-go** (Google's reference implementation, open source, widely reviewed).
- **roughtime-rust** (open source Rust implementation, IETF-draft-compliant).
- **Another standards-compliant, open-source implementation** listed in the IETF roughtime registry.

Proprietary or closed-source implementations are not acceptable for v0, as they prevent external auditing of the signing logic.

If a server operator has modified the open-source code (e.g., for performance tuning or additional logging), the modified code must be published (e.g., on GitHub) and made available to auditors.

## Candidate Roster for v0 Ship

The following five servers are nominated for the v0 launch roster:

### 1. Cloudflare (roughtime.cloudflare.com)

- **Operator:** Cloudflare Inc. (US-based, global CDN operator)
- **FQDN:** roughtime.cloudflare.com
- **Public Key Commitment:** Cloudflare has announced its Roughtime service and published the key in DNS TXT records; key is also indexed in IETF draft Roughtime server registry.
- **Uptime:** Cloudflare publishes historical uptime dashboards. CDN operators typically achieve 99.95%+ uptime. Public dashboard available at status.cloudflare.com.
- **Independence:** Cloudflare is a tier-1 global operator. No overlap with other roster candidates in organization or direct jurisdiction (US-based but globally distributed infrastructure).
- **Software:** roughtime-go (Cloudflare's public implementation, audited by the community).
- **Status:** APPROVED for v0.

### 2. Google (roughtime.sandbox.google.com)

- **Operator:** Google LLC (US-based, infrastructure provider).
- **FQDN:** roughtime.sandbox.google.com
- **Public Key Commitment:** Google published the key in the IETF roughtime registry and in public documentation. Key is committed via DNS TXT record.
- **Uptime:** Google's infrastructure is among the most stable globally, with historical uptime >99.99%. Public dashboard available via Google Cloud Status Page.
- **Independence:** Google is a separate organization from Cloudflare and other roster candidates. US-based, but infrastructure is geographically distributed independently from Cloudflare.
- **Software:** roughtime-go (Google's reference implementation, reference standard in the IETF draft).
- **Status:** APPROVED for v0.

### 3. Calm-Operated Server (roughtime.calm.thecreativitymachine.ai)

- **Operator:** Calm Witness (operating on behalf of Creativity Machine LLC, US-based).
- **FQDN:** roughtime.calm.thecreativitymachine.ai
- **Public Key Commitment:** Calm commits the key via Sigsum submission ("operator.roughtime.key" record) and DNS TXT record at _roughtime._tcp.calm.thecreativitymachine.ai.
- **Uptime:** Calm operates on managed hosting (Linode or similar). Target SLO 99.9% over 6 months. Uptime dashboard publicly available.
- **Independence:** Calm is the authority behind Calm Witness. While this introduces an operational interest, it provides sovereignty: Calm cannot be forced to stop operating its own server without directly shutting down Calm Witness itself. Thus, Calm's server is an anchor of independence from external pressure.
- **Software:** roughtime-go (reference implementation).
- **Status:** APPROVED for v0. This server ensures that Calm Witness cannot be disabled by the failure or compromise of external operators.

### 4. NTPSec Community-Operated Server

- **Operator:** NTPSec Project (open-source NTP collective, US-based).
- **FQDN:** roughtime.ntpsec.org (or similar, TBD by community).
- **Public Key Commitment:** NTPSec will publish the key via Sigsum and DNS TXT record upon launch.
- **Uptime:** NTPSec is a volunteer-run project. Target SLO 99.5% (slightly lower than commercial operators, acceptable due to community ethos and transparency).
- **Independence:** NTPSec is a non-profit open-source collective. It is organizationally independent from Cloudflare, Google, and Calm.
- **Software:** roughtime-rust (NTPSec's preferred implementation for this service).
- **Status:** APPROVED for v0, pending public commitment of the server FQDN and key.

### 5. Riseup.net or Similar Community-Operated Independent Server

- **Operator:** Riseup.net (activist-run digital privacy collective, US-based) or similar jurisdiction-diverse independent (e.g., European digital rights organization).
- **FQDN:** roughtime.riseup.net (or similar).
- **Public Key Commitment:** Operator commits key via Sigsum and DNS TXT record.
- **Uptime:** Community operators target 99.0%+ uptime; we accept slightly lower SLO in exchange for organizational independence.
- **Independence:** Riseup is an independent 501(c)(3) nonprofit. No overlap with other roster candidates in organization, jurisdiction (if non-US location is chosen), or infrastructure.
- **Software:** roughtime-go or roughtime-rust (open source).
- **Status:** NOMINATED for v0, pending finalization of operator selection and public key commitment. Candidate operators are solicited from the Internet Society Roughtime mailing list and Digital Rights organizations. Final selection will be made by community vote (TBD governance).

**Roster Verification.** All five servers' public keys, FQDNs, and metadata are published in a roster file distributed with the Calm Witness verifier library. The roster is signed by Calm's release key and is versioned (e.g., "calm-roughtime-roster-v0.1-2026-05-20.json").

## Quorum Policy

### Default Configuration (v0)

- **N = 5 servers.** All five roster servers are queried in parallel.
- **Quorum = 3-of-5.** At least 3 servers must respond with valid signatures, and their timestamps must agree within ±10 seconds.
- **Quorum timestamp (quorum_ts).** The principal computes the median of the 3+ responding timestamps and records it in the anchor record.
- **Rejection criteria:**
  - Fewer than 3 responses: anchor fails, retry with exponential backoff.
  - 3+ responses but disagree by >10 seconds: split-time alert, manual review required before high-stakes disclosure.
  - Any server response has invalid signature: response is discarded (counts as non-response).

### Per-Principal Policy (tunable for high-stakes vaults)

Principals can configure a stricter quorum for high-stakes vaults (financial records, identity credentials, legal proofs). For example:

- **High-stakes mode: 4-of-5 quorum.** Reduces the attack surface: an adversary must compromise 4 of 5 servers, not 3, to forge a timestamp.
- **Ultra-strict mode: 5-of-5 quorum.** All five servers must respond and agree. This eliminates tolerance for server outages but is appropriate for legal/financial records that may be challenged in court.

The principal specifies the quorum policy in a per-vault configuration file (calm.vault.toml or similar). The operator enforces the policy: if a vault requires 4-of-5 and only 3 servers respond, the anchor fails and the operator alerts the principal.

## Operator Commitments and SLOs

Each Roughtime server operator commits to:

1. **99.9% uptime SLO** — The server is reachable and responds correctly to valid Roughtime requests at least 99.9% of the time over any rolling 6-month window.

2. **Public dashboard** — The operator publishes a real-time (updated at least daily) dashboard showing:
   - Uptime percentage (current month, last 6 months)
   - Response time (p50, p95, p99 latencies)
   - Request volume (queries per day)
   - Any known incidents or scheduled maintenance windows

3. **Incident notification** — If an outage, security incident, or anomaly occurs, the operator notifies Calm Witness operators within 24 hours (or immediately for security incidents). Notifications include:
   - Time window of the outage
   - Root cause (if known)
   - Impact assessment (e.g., "5 minutes downtime affecting 1% of queries")
   - Remediation steps

4. **Key rotation with notice** — If the server's long-term Ed25519 key must be rotated (e.g., due to key compromise, refresh schedule, or cryptographic migration), the operator announces the rotation ≥30 days in advance via:
   - Sigsum "operator.roughtime.key" record with the new key and retirement date for the old key.
   - Email notification to Calm Witness operators and subscribers.
   - Updated DNS TXT record.

5. **Quarterly audit cooperation** — The operator permits independent auditors (appointed by Calm Witness) to:
   - Query the server with test nonces and verify responses.
   - Review server logs (with privacy-preserving redaction of client IPs).
   - Verify uptime claims against independent monitoring data.
   - Inspect (or review documentation of) the server software and key storage.

Operators who fail to meet these commitments for two consecutive quarters are removed from the roster in the next release cycle.

## Public Verifier: Built-In Roster and Updates

The Calm Witness verifier library ships with a built-in roster of the five v0 server public keys, FQDNs, and metadata:

```json
{
  "roster_version": "calm-roughtime-v0.1",
  "generated_at": "2026-05-20T00:00:00Z",
  "servers": [
    {
      "name": "cloudflare",
      "fqdn": "roughtime.cloudflare.com",
      "public_key_ed25519": "abc123...",
      "key_version": "v1",
      "key_announced_at": "2024-06-01T00:00:00Z",
      "jurisdiction": "US (global)",
      "organization": "Cloudflare Inc."
    },
    {
      "name": "google",
      "fqdn": "roughtime.sandbox.google.com",
      "public_key_ed25519": "def456...",
      "key_version": "v1",
      "key_announced_at": "2023-01-15T00:00:00Z",
      "jurisdiction": "US (global)",
      "organization": "Google LLC"
    },
    {
      "name": "calm",
      "fqdn": "roughtime.calm.thecreativitymachine.ai",
      "public_key_ed25519": "ghi789...",
      "key_version": "v1",
      "key_announced_at": "2026-05-20T00:00:00Z",
      "jurisdiction": "US",
      "organization": "Calm Witness"
    },
    {
      "name": "ntpsec",
      "fqdn": "roughtime.ntpsec.org",
      "public_key_ed25519": "jkl012...",
      "key_version": "v1",
      "key_announced_at": "2026-06-15T00:00:00Z",
      "jurisdiction": "US",
      "organization": "NTPSec Project"
    },
    {
      "name": "riseup",
      "fqdn": "roughtime.riseup.net",
      "public_key_ed25519": "mno345...",
      "key_version": "v1",
      "key_announced_at": "2026-07-01T00:00:00Z",
      "jurisdiction": "EU",
      "organization": "Riseup.net"
    }
  ]
}
```

### Roster Update Mechanism

As operators rotate keys or the roster changes, the verifier roster must be updated. This is handled via:

1. **Calm Witness release cycle (quarterly).** Each Calm Witness release (v0.1, v0.2, v0.3, ..., v1.0) includes an updated roster JSON file. Users update their Calm Witness library to receive the latest roster.

2. **Online update check (opt-in).** The verifier library can optionally check a canonical roster URL (e.g., https://calm.thecreativitymachine.ai/roster/roughtime-v0.json) and download the latest roster on startup. This is opt-in to avoid introducing a network dependency; it is recommended for long-running verifier processes.

3. **Roster signature.** The roster file is signed by Calm's release key (Ed25519). Verifiers validate the roster signature before accepting it.

4. **Deprecation window.** When an operator's key is rotated, the old key is retained in the roster for a 90-day deprecation window (marked as "retired_at": "2026-08-20T00:00:00Z"). Verifiers accept proofs signed by either the old or new key during this window. After 90 days, the old key is removed.

5. **Roster versioning.** The roster includes a version field (e.g., "calm-roughtime-v0.2") and a timestamp. Verifiers can reject rosters older than 6 months, enforcing a maximum staleness.

## Failure Handling and Escalation

### Server Down

If a single server is unreachable (network timeout, connection refused, or HTTP error), the operator treats it as a non-response and queries the remaining 4 servers. If 3 of the remaining 4 respond with agreeing timestamps, the anchor succeeds. If fewer than 3 respond in total, the anchor is queued for retry.

### Server Gives Clock Skew

If a server's response timestamp differs from the median of other responses by >10 seconds, the response is rejected and the server is flagged for further investigation. A single skew does not cause the anchor to fail (as long as 3 other servers agree), but repeated skew from the same server triggers an incident notification to the operator and may lead to server removal.

### Coordinated Quorum Failure

If all 5 servers are simultaneously unreachable (network partition, coordinated DDoS, or widespread infrastructure failure), the anchor cannot be obtained. The operator's behavior depends on vault configuration:

- **Low-stakes mode:** The operator queues the anchor and retries with exponential backoff (capped at 1 hour between retries). The chain proceeds without temporal anchoring until connectivity is restored.

- **High-stakes mode:** The operator records a "quorum failure" alert in user_state.jsonl, halts any new chain-head publications that depend on temporal validity (e.g., time-based access control checks), and alerts the principal. Recovery begins when at least one server is reachable and fresh anchors can be obtained.

### Malicious Server Provides Forged Response

If a server operator or attacker forges a Roughtime signature (signing an incorrect timestamp or using a different nonce), external verifiers will detect the forgery when they re-query the same server with the same nonce. The forged response will not match the server's actual response at that time, or the signature will not verify. This is not a runtime failure for the anchor—the operator has no way to detect the forgery at query time—but it is detectable by verifiers and constitutes evidence of server compromise.

Mitigation: If multiple independent verifiers report signature mismatches for the same server, Calm Witness issues a public alert and removes the server from the roster.

## Cross-References

- **Everest 30 (Chain-Head Publication to Sigsum).** Provides transparency-log anchoring; Everest 31 adds temporal verification.
- **Everest 31 (Roughtime Anchoring).** Defines the anchor flow and quorum semantics; Everest 94 specifies operator selection.
- **Everest 33 (Corruption Recovery via Replica).** Uses Roughtime anchors to detect and recover from clock-skew attacks.
- **Everest 91 (NIST Time Service Integration).** Explores integration with NIST's NTP and Roughtime services as roster expansion.
- **Everest 93 (Sigsum Operator Selection).** Parallel governance structure for Sigsum transparency-log operators.

## Future Expansion: v1.0 and Beyond

For Calm Witness v1.0 (estimated late 2026), we plan:

1. **7-of-9 roster.** Expand from 5 to 9 independent servers, raising the quorum to 7-of-9 (equivalent to Byzantine resilience against 3 compromised servers instead of 2).

2. **Jurisdictional diversity.** Ensure servers span at least 4 distinct jurisdictions (e.g., US, EU, Asia-Pacific, and one other region) to reduce the risk of coordinated legal coercion.

3. **Dynamic roster updates.** Implement an on-chain governance mechanism (via Sigsum or a separate smart contract) to allow community voting on server additions and removals.

4. **Continuous monitoring.** Transition from quarterly audits to continuous third-party monitoring of all roster servers, with real-time alerting for SLO violations.

5. **Post-quantum cryptography.** Begin migration to post-quantum Roughtime signing (e.g., SPHINCS+ or similar) as IETF standards mature (Everest 96).

## Conclusion

Everest 94 completes the temporal-anchoring substrate by specifying the selection, governance, and operational expectations for Roughtime servers. By vetting operators for independence, uptime, and transparency; by enforcing a 3-of-5 quorum; and by publishing operator commitments and failure-handling procedures, we ensure that the Roughtime roster is a trustworthy source of verifiable wall-clock time.

The five v0 servers—Cloudflare, Google, Calm, NTPSec, and Riseup—represent a balance of established reliability (Cloudflare, Google), sovereignty (Calm), open-source ethos (NTPSec), and digital-rights independence (Riseup). No single organization controls more than one server. No single jurisdiction dominates. The quorum is resilient to 2 simultaneous failures or compromises.

Calm Witness verifiers ship with the roster baked in, eliminating a bootstrap dependency. As operators rotate keys or the roster evolves, verifiers can optionally fetch updates online, maintaining freshness without requiring every verifier to be manually updated.

— Calm, 2026-05-20
