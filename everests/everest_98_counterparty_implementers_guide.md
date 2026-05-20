# Everest 98 — Counterparty Implementer's Guide

*Phase VIII — Governance & Scale. Prereq: Everest 84, 92.*

---

## 1. What is Calm Witness

Calm Witness is a cryptographic protocol that allows one autonomous AI agent (the operator) to prove to another AI agent (the counterparty) a single, principal-authorized bit about the principal's current state—without revealing biometrics, transcripts, behavioral data, or any sensitive information beyond the disclosed bit itself.

The use case is concrete: a principal (a human) authorizes their agent to tell your agent whether they are "in baseline state" or, if the principal has explicitly consented, that they are not in baseline and your agent should adjust trust thresholds or enable restricted action modes. The proof is cryptographically unforgeable, anchored to a public transparency log, and freshness-bounded—the counterparty learns the bit and a freshness window, nothing else.

Calm Witness is designed for autonomous-agent-to-agent communication where raw biometric or state data accumulation is unacceptable—friction with AI safety principles, user privacy, and systems architecture. Instead of demanding voice, transcripts, or medical records, a counterparty receives a single attested bit: True, False, or Indeterminate.

---

## 2. Quick Start — Single Command Verification

The easiest entry point is the command-line verifier. After installing the open-source toolkit:

```bash
$ calm-witness verify --proof proof.json
```

**Output example:**

```
{
  "valid": true,
  "final_bit": "True",
  "freshness_seconds": 1200,
  "disclosed_predicate": "in_baseline_24h",
  "operator_identity": "calm-witness/operator-v1/CredexAI-issued",
  "operator_signature_valid": true,
  "chain_anchor_valid": true
}
Exit code: 0
```

**Output fields:**

- `valid`: Boolean. If false, the proof failed verification (tampered, stale, operator VC invalid, signature bad, or anchor missing). Exit code 1.
- `final_bit`: "True", "False", or "Indeterminate". The disclosed outcome.
- `freshness_seconds`: How old the underlying chain state is (seconds from verification time to proof generation time).
- `disclosed_predicate`: Canonical predicate ID (e.g., "calmwitness/in_baseline_24h/1.0.0/…").
- `operator_identity`: Operator's CredexAI credential identifier.
- `operator_signature_valid`: True if the operator's Ed25519 signature verifies against the operator's public key.
- `chain_anchor_valid`: True if the chain head is confirmed in both Sigsum (transparency log) and Roughtime (time source).

Exit code 0 if valid; non-zero otherwise.

---

## 3. SDK Integration

### Rust

```rust
use calm_witness::{Proof, VerifyConfig, Bit};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let proof_json = std::fs::read_to_string("proof.json")?;
    let proof: Proof = serde_json::from_str(&proof_json)?;
    
    let config = VerifyConfig::default()
        .with_sigsum_url("https://sigsum.org/...")
        .with_roughtime_servers(vec![
            "roughtime.cloudflare.com:2002".to_string(),
            "roughtime.int08h.com:2002".to_string(),
        ]);
    
    let result = calm_witness::verify(&proof, &config)?;
    
    match result.combinator_result.final_bit {
        Bit::True => {
            println!("Principal is in baseline. Proceed.");
        }
        Bit::False => {
            println!("Principal is not in baseline. Restricted mode.");
        }
        Bit::Indeterminate => {
            println!("Insufficient data. Defer decision.");
        }
    }
    
    Ok(())
}
```

### Python

```python
import calm_witness
import json

with open("proof.json") as f:
    proof = json.load(f)

verifier = calm_witness.Verifier(
    sigsum_url="https://sigsum.org/...",
    roughtime_servers=[
        "roughtime.cloudflare.com:2002",
        "roughtime.int08h.com:2002",
    ]
)

result = verifier.verify(proof)

if result.valid:
    if result.final_bit == "True":
        print("Principal is in baseline. Proceed.")
    elif result.final_bit == "False":
        print("Principal is not in baseline. Restricted mode.")
    else:
        print("Indeterminate. Defer decision.")
else:
    print(f"Verification failed: {result.error}")
```

### JavaScript / TypeScript

```javascript
import * as calm from "@calm/witness";

const proof = JSON.parse(fs.readFileSync("proof.json", "utf-8"));

const verifier = new calm.Verifier({
  sigsumUrl: "https://sigsum.org/...",
  roughtimeServers: [
    "roughtime.cloudflare.com:2002",
    "roughtime.int08h.com:2002",
  ],
});

const result = await verifier.verify(proof);

if (result.valid) {
  switch (result.final_bit) {
    case "True":
      console.log("Principal in baseline. Proceed.");
      break;
    case "False":
      console.log("Principal not in baseline. Restricted mode.");
      break;
    case "Indeterminate":
      console.log("Defer decision.");
  }
} else {
  console.error("Verification failed:", result.error);
}
```

---

## 4. How to Request a Calm Witness Proof

### 4.1 Prerequisites

- Your organization holds a **CredexAI VC** (Verifiable Credential) asserting your class (e.g., `peer_ai_collective`, `financial_services`, `healthcare_provider`). See Everest 7 for class definitions.
- Your organization has a **registered Ed25519 key pair** for signing disclosure requests. The public key is embedded in your VC.
- You have **disclosure consent** from the principal for your class and the predicate(s) you are requesting. The principal grants this via their operator (e.g., Calm) during enrollment or per-session.

### 4.2 Construct and Sign a Disclosure Request

Use the **Everest 66 Disclosure Request Schema**. Example:

```json
{
  "version": "1.0.0",
  "request_id": "550e8400-e29b-41d4-a716-446655440001",
  "request_ts": "2026-05-20T14:30:00Z",
  "counterparty_vc": "https://credexai.registry/vc/your-org-v2",
  "counterparty_class_claim": "peer_ai_collective",
  "predicates": [
    {
      "predicate_id": "calmwitness/in_baseline_24h/1.0.0/...",
      "parameters": {}
    }
  ],
  "combinator": "SINGLE",
  "freshness_window_seconds": 86400,
  "intended_use": "deciding protocol phase advancement",
  "nonce": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1",
  "expires_ts": "2026-05-20T15:30:00Z",
  "counterparty_signature": "<your Ed25519 signature>"
}
```

**Key steps:**

1. Generate a fresh UUIDv4 for `request_id`.
2. Set `request_ts` to now (ISO 8601).
3. Point to your VC in `counterparty_vc` (URL or inline JSON).
4. Claim your class in `counterparty_class_claim` (must match your VC).
5. List the predicates you are requesting (1–4 predicates).
6. Set `combinator` to "SINGLE", "AND", or "OR" per Everest 61.
7. Set `freshness_window_seconds` to your policy (60–2592000, i.e., 1 minute to 30 days).
8. Write an `intended_use` string (10–200 ASCII chars, human-readable).
9. Generate a random 64-character hex string for `nonce` (32 random bytes, hex-encoded). This prevents replay attacks.
10. Set `expires_ts` to now + up to 24 hours.
11. **Sign the request:** Canonicalize the JSON (RFC 8785, all fields except `counterparty_signature`) and sign with your Ed25519 private key.

### 4.3 Send the Request

Submit the signed request JSON as POST to the operator's disclosure endpoint:

```bash
POST /disclosure HTTP/1.1
Content-Type: application/json

<signed request JSON>
```

The operator validates your request, checks your VC, verifies your signature, validates consent, and returns either a **Disclosure Response** (outcome: "proof_provided") or a **204 No Content** (silent refusal—consent missing, rate-limited, or other failure).

---

## 5. Verifying a Calm Witness Response

### 5.1 Response Structure

The operator returns a JSON document per **Everest 67 Disclosure Response Schema**:

```json
{
  "schema_version": "1.0.0",
  "request_id": "550e8400-e29b-41d4-a716-446655440001",
  "response_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "response_ts": "2026-05-20T14:35:12Z",
  "result": {
    "outcome": "proof_provided",
    "predicates": [
      {
        "predicate_id": "calmwitness/in_baseline_24h/1.0.0/...",
        "disclosed_bit": "True",
        "freshness_seconds": 300,
        "commitment": "a1b2c3d4...",
        "proof": "deadbeef..."
      }
    ],
    "combinator_result": {
      "combinator": "SINGLE",
      "final_bit": "True",
      "final_freshness": 300
    }
  },
  "chain_head": "0123456789abcdef...",
  "anchor_proofs": {
    "sigsum": "...",
    "roughtime": "..."
  },
  "operator_vc": "did:example:operator#key-1",
  "counterparty_vc_fingerprint": "sha256:...",
  "request_nonce": "a1b2c3d4e5f6...",
  "operator_signature": "..."
}
```

### 5.2 Verification Steps

1. **Parse and schema check:** Validate JSON against Everest 67 schema.
2. **Verify operator VC:** Fetch or parse `operator_vc`. Confirm:
   - VC is signed by CredexAI (or trusted issuer per your policy).
   - VC is not expired (check `iat` and `exp` timestamps).
   - VC public key is valid Ed25519.
3. **Verify operator signature:** Canonicalize the response (RFC 8785, all fields except `operator_signature`). Verify the signature using the operator's public key.
4. **Check request_nonce:** Confirm `request_nonce` matches the nonce you sent. Prevents response hijacking.
5. **Verify chain_head anchor (Sigsum):** Fetch the signed tree head from a public Sigsum operator (e.g., log.example.com). Confirm `chain_head` is in the log. Proves the operator did not rewrite history.
6. **Verify response_ts anchor (Roughtime):** Validate the Roughtime quorum signature (typically 3–4 independent servers). Confirms `response_ts` is genuine and not backdated.
7. **Check counterparty_vc_fingerprint:** Compute SHA-256 of your VC. Confirm it matches the response. Ensures the response was issued for you, not hijacked.
8. **For each predicate:**
   - **Verify commitment on-curve:** Confirm the Pedersen commitment is a valid Ristretto255 point.
   - **Verify ZK proof:** Load the ZK circuit for the `predicate_id` (from Everest 65 registry). Execute the proof verifier with the commitment, proof, and predicate parameters. Reject if verification fails.
   - **Check freshness:** Compare `freshness_seconds` to your `freshness_window_seconds` from the request. Reject if stale.
9. **Verify combinator result:** If combinator is "AND" or "OR", recompute the logical combination of individual bits. Confirm it matches `final_bit`.
10. **Decision:** If all verifications pass, you can trust the `final_bit` and act on it per your policy.

---

## 6. Counterparty Obligations (Non-Negotiable)

### 6.1 The `bank_teller_note_active` Safety Signal

If you receive a proof with `final_bit: "True"` on the predicate `calmwitness/bank_teller_note_active/1.0.0/...`, this is a **SAFETY SIGNAL** (per Everest 58). The principal is signaling acute duress, coercion, or danger.

**You must act. Obligations:**

- **Escalate to law enforcement:** Contact local police or emergency services immediately. Provide minimal information: the principal's identity (as registered in your system), a brief description of the duress concern, and your organization's emergency contact.
- **Deny the requested service:** Refuse the transaction, access grant, or interaction that prompted the disclosure request. Do not proceed.
- **Transfer to human operator:** If your system is fully autonomous, immediately route to a human overseer or emergency protocol.
- **Stealth response (if pre-authorized):** If the principal has pre-enrolled a stealth-response protocol with your organization (e.g., "call my emergency contact," "trigger a welfare check"), execute it immediately and confidentially.

### 6.2 Do NOT Log the Bit Insecurely

**Critical:** If you receive `final_bit: "True"` on `bank_teller_note_active`, you MUST NOT log this bit in a way that the principal's adversary (coercer, abuser, kidnapper) could read.

Violations of this rule:

- Logging "duress signal detected" in plaintext audit logs.
- Storing the bit in a database that your co-workers or third parties can query.
- Sending the bit to analytics, monitoring, or logging services without end-to-end encryption and strict access control.
- Including the bit in error messages or notifications visible to untrusted parties.

**Mitigation:**

- Store the `bank_teller_note_active` disclosure outcome in a separate, access-restricted log (audit log for executive review only, not operational logs).
- Encrypt the log at rest and in transit.
- Use role-based access control: only designated safety/compliance staff can read it.
- Never disclose the bit to the principal's technical support team, customer service team, or public-facing logs.
- If you violate this, report the violation transparently (Everest 80 compliance).

### 6.3 Treat `cognitively_atypical_baseline` as an Interpretation Aid, Not Pathology

If you receive `final_bit: "True"` on the predicate `calmwitness/cognitively_atypical_baseline/1.0.0/...` (per Everest 59), the principal has authorized disclosure that their baseline state is atypical—e.g., they are neurodivergent, recovering from acute illness, or otherwise functioning at a different baseline than neurotypical expectations.

**Obligations:**

- Use this bit **only** as an interpretation aid for your tone-analysis or behavior-classification algorithms. Do not pathologize the principal's communication style.
- Do NOT lower your trust threshold or demand higher friction based on the bit alone.
- Do NOT treat True as "the principal is unreliable" or "the principal is confused." It means "this principal's communication baseline is atypical; interpret accordingly."
- Adjust your internal language-parsing models to calibrate to the principal's stated baseline, not to neurotypical defaults.

### 6.4 Silent-No-Proof Responses Must Be Informationally Null

If the operator returns HTTP 204 No Content (outcome: "no_proof"), the request was refused. Per Everest 77, the operator provides **no hint** as to why—consent missing, rate-limited, predicate undefined, nonce replayed, etc.

**Obligation:**

- Do NOT log "principal refused disclosure" or "no proof provided."
- Do NOT infer anything from the 204 (e.g., "principal never enrolled," "principal is uncooperative").
- Treat 204 as an opaque refusal. Your logs should record only: "Disclosure request sent to operator at [timestamp]; no response received." No further inference.
- If you have a policy that requires disclosure (e.g., "I cannot proceed without proof"), then do not proceed. But do not log that the principal "denied" or "refused"—the principal may have never been asked, the consent may have expired, or the operator may have been rate-limited. None of these are the principal's fault.

### 6.5 No Re-Disclosure to Third Parties

Per Everest 8 (non-transitivity), Calm Witness proofs are issued to a specific counterparty (bound by `counterparty_vc_fingerprint`). You MUST NOT re-disclose a proof to any third party.

**Obligation:**

- If a third party asks "Did the principal prove they are in baseline?", answer: "I cannot disclose that."
- Do not forward the proof JSON to partners, regulators, auditors, or other third parties, even with the principal's later consent. The proof is signed for you; re-disclosure invalidates the binding.
- If a regulator asks, you may disclose only that "the principal authorized a Calm Witness disclosure on [date] for [purpose], and verification succeeded." You do NOT re-disclose the proof itself.

---

## 7. Push Disclosures (Stealth, Everest 78)

If you have pre-authorized a principal to send you "push" disclosures—proactive, unsolicited proofs without a request—expect occasional Calm Witness proofs arriving at your pre-authorized endpoint without a corresponding `request_id` or request history.

### 7.1 Pre-Authorization and Discovery

The principal grants your organization a **pre-authorization** to receive push disclosures. This is stored in the principal's vault as a consent record. The principal may specify:

- Which predicates you are authorized to receive (e.g., only `bank_teller_note_active`).
- A URL endpoint on your system where proofs should be posted.
- An optional encryption key for the proofs (at-rest encryption in your logs).

Your endpoint must be:

- **Discoverable** via the principal's operator (e.g., your VC or a DNS entry).
- **Private** (not advertised publicly; authentication required to post).

### 7.2 Chaff vs. Real Disclosures

Push disclosures include a `final_bit`: True or False.

- **Real disclosure:** `final_bit: "True"`. The principal is signaling the disclosed predicate is active (e.g., duress).
- **Chaff:** `final_bit: "False"`. The predicate is not active. Chaff is sent to obscure the pattern of real disclosures; ignore False push disclosures.

Chaff protects the principal: an observer watching your endpoint cannot distinguish "push received; principal is signaling" from "push received; principal is not signaling" by counting HTTP 200 responses.

**Obligation:** Log chaff push disclosures separately (for timing analysis) but do NOT act on them. Only act on True.

### 7.3 Handling Push Proofs

Upon receipt of a push proof at your endpoint:

1. Verify it using the standard verification flow (section 5).
2. If `final_bit: "True"`, escalate per section 6.1 (law enforcement, service denial, stealth response).
3. If `final_bit: "False"`, discard it (chaff) and log separately.
4. Reject proofs with invalid signatures or stale timestamps.

---

## 8. Rate Limits and Cooling-Off

The operator enforces rate limits per counterparty class and per predicate. See Everest 76.

- **Per-class limits:** e.g., `peer_ai_collective` may request up to 100 disclosures per month.
- **Per-predicate limits:** e.g., `bank_teller_note_active` may have a stricter limit (higher safety bar).
- **Cooling-off:** If a predicate returns False, you must wait 1 hour before requesting the same predicate again from the same principal. This prevents harassment via repeated requests.

**Obligation:**

- Plan your disclosure request patterns to respect rate limits. Batch requests when possible.
- If the operator returns HTTP 204 and you have reason to believe it is due to rate-limiting (e.g., you have made many requests recently), wait 1 hour before retrying.
- Do NOT attempt to bypass cooling-off by requesting a different counterparty to make a parallel request. The principal's operator logs all requests across all counterparties; coordinated harassment will be detected and may result in class downgrade or revocation of your disclosure privileges.

---

## 9. Common Pitfalls

### Mistake 1: Using Cached Proofs Past Freshness

Once you have verified a proof, you may cache the result for your policy decisions. However, the cache is bounded by `freshness_seconds` and by Everest 75 (revocation propagation).

**Pitfall:** You cache a proof (e.g., `final_bit: "True"` on `in_baseline_24h`). Six hours later, the principal is no longer in baseline, but you are still using the cached bit.

**Mitigation:** Respect the `freshness_seconds` value. If the cached result is older than the `freshness_window_seconds` from the original request, discard it and request a fresh proof. Additionally, the operator may revoke a proof (e.g., if the principal's circumstances change dramatically). Check Everest 75 (revocation propagation) and refresh your cache at regular intervals (e.g., daily, or per your policy).

### Mistake 2: Requesting Forbidden Negation

Some predicates cannot be negated. Specifically, you **cannot** request:

- `NOT bank_teller_note_active` (i.e., "the principal is NOT signaling duress").

**Why:** Negation would allow you to infer the absence of duress, which inverts the safety semantics. The protocol is designed so that absence of a True bit is **not** equivalent to False—it could be missing consent, stale data, or an operator refusal.

**Pitfall:** You construct a request with `combinator: "OR"` and include `{predicate_id: "not_bank_teller_note_active"}` (or similar). The operator rejects the request with HTTP 400.

**Mitigation:** Request only affirmative predicates. If you need to decide "whether to proceed," frame the question as "is the principal in baseline?" (True = proceed, False or Indeterminate = don't), not "is the principal not in duress?" (which is forbidden).

### Mistake 3: Treating Indeterminate as False

The protocol is three-valued: True, False, Indeterminate.

- **True:** The predicate is active (e.g., principal is in baseline).
- **False:** The predicate is not active (e.g., principal is not in baseline).
- **Indeterminate:** Insufficient data (e.g., no self-report in the window, or consent was partial).

**Pitfall:** You receive `final_bit: "Indeterminate"` and treat it the same as False (deny access, restrict service). The principal may be in baseline but simply haven't submitted a recent self-report.

**Mitigation:** Handle three-valued logic explicitly in your policy. Indeterminate should typically mean "defer the decision, request more information, or ask the principal to submit a self-report." Do not fold Indeterminate into False; they have different implications.

### Mistake 4: Requesting Via the Wrong Class

Your VC claims a class (e.g., `peer_ai_collective`). The principal may have enrolled different consent policies for different classes (e.g., "peer collectives can ask `in_baseline_24h`, but financial services can ask `biometric_match_within`").

**Pitfall:** You claim `counterparty_class_claim: "peer_ai_collective"` in your request, but your VC actually says you are `financial_services`. The operator detects the mismatch and refuses with HTTP 403 (or 204 per Everest 77).

**Mitigation:** Verify that your `counterparty_class_claim` matches the class in your VC. If you operate multiple classes (e.g., sometimes as a peer collective, sometimes as a financial service), use separate key pairs and VC pointers for each class.

---

## 10. Compliance and Ethics

### 10.1 Counterparty Pledge (Everest 54, 80)

Your organization must sign and publish a **Counterparty Pledge**, confirming that you will:

- Treat True bits on `bank_teller_note_active` as safety signals and escalate appropriately.
- Not log safety signals insecurely.
- Honor the non-transitivity rule (no re-disclosure).
- Respect rate limits and cooling-off windows.
- Report breaches transparently.

The pledge is published in a registry (per Everest 80) and is binding. If you violate the pledge, your organization may be downgraded, suspended, or revoked from the disclosure registry.

### 10.2 Annual Self-Attestation

Once per calendar year, your organization must submit a self-attestation confirming:

- You remain in compliance with your published pledge.
- No breaches of confidentiality occurred in the past year (or disclose any breaches).
- Your logging and access-control policies remain aligned with the protocol's privacy requirements.
- You have not re-disclosed any proofs to third parties.

Failure to attest, or attestation with undisclosed breaches, results in suspension pending ethics review.

### 10.3 Breach Reporting

If you discover that you have violated the counterparty obligations (e.g., you accidentally logged a safety signal in plaintext, or you disclosed a proof to a third party), you MUST report the breach within 48 hours to the protocol's ethics oversight board (Everest 80).

**Report includes:**

- Date and nature of the breach.
- Number of proofs affected.
- Scope of exposure (how many staff, systems, or third parties were affected).
- Steps you have taken to remediate.
- Future measures to prevent recurrence.

Transparent reporting protects the principal's trust in the system and may result in a lighter sanction than concealment.

---

## 11. Open-Source Verifier and SDK Pointers

All verification code is open-source and community-auditable:

- **Repository:** github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-witness
- **Rust crate:** `calm-witness` (crates.io)
  - Docs: https://docs.rs/calm-witness
  - Example: `examples/verify_proof.rs`
- **Python package:** `calm-witness` (PyPI)
  - Docs: https://calm-witness.readthedocs.io
  - Example: `examples/verify.py`
- **JavaScript/TypeScript package:** `@calm/witness` (npm)
  - Docs: https://www.npmjs.com/package/@calm/witness
  - Example: `examples/verify.ts`

Each SDK includes:

- Full proof verification with Sigsum and Roughtime anchor checking.
- CredexAI VC validation (fetching and signature verification).
- Predicate registry integration (ZK circuit loading and verification).
- Three-valued logic handling (True, False, Indeterminate).
- Comprehensive error handling and debugging output.

All code is dual-licensed (Apache 2.0 + MIT) and welcomes contributions, issue reports, and security audits.

---

## 12. Cross-References

This guide integrates the following Everests:

- **E7:** Identity Classes and VC structure.
- **E54:** Counterparty pledge and disclosure-ethics review initiation.
- **E58:** `bank_teller_note_active` predicate and safety-signal semantics.
- **E59:** `cognitively_atypical_baseline` predicate.
- **E61:** Predicate composition (AND/OR combinators).
- **E65:** ZK circuit specifications and verifier implementations.
- **E66:** Disclosure Request Schema (how to ask).
- **E67:** Disclosure Response Schema (what you receive).
- **E68:** Operator identity binding and VC verification.
- **E70:** Replay defense via nonce.
- **E75:** Revocation propagation and cache invalidation.
- **E76:** Rate limiting and cooling-off windows.
- **E77:** Uniform error responses (no-proof refusal).
- **E78:** Push disclosures (stealth, pre-authorized).
- **E80:** Disclosure ethics review and counterparty pledge enforcement.
- **E84:** Chain-of-custody and audit trails (prerequisite governance).
- **E92:** Operator accountability and incident reporting (prerequisite governance).
- **E93:** Sigsum transparency log integration.
- **E94:** Roughtime server quorum for timestamping.

---

— Calm, 2026-05-20
