# Calm Witness — Conference Talk Curriculum v0 (S256)

## Talk Metadata

**Title:** The Bank-Teller Note: Cryptographic Proof of Human State for Autonomous Agents

**Abstract:** Autonomous AI agents routinely act on behalf of human principals without standard ways to attest the principal's baseline state to counterparty agents. Calm Witness solves this with a cryptographic primitive: one agent can prove to another that a principal is themself and in their baseline condition — without exposing biometric data, narrative, or diagnosis. We demonstrate the hash-chain substrate, disclosure wire protocol, and production deployment of the bank-teller-note model.

**Target Audience:** Autonomous AI engineers, protocol designers, cryptography practitioners, security researchers, conference track on agent-to-agent communication and AI safety.

**Runtime:** 25 minutes (18 min talk + 7 min Q&A)

**Level:** Advanced (assumes familiarity with agent architectures, cryptographic commitment schemes, and OpenID Connect workflows)

---

## Slide-by-Slide Outline (18 slides + title)

### Slide 1: Title Slide
*"The Bank-Teller Note: Cryptographic Proof of Human State for Autonomous Agents"*
Speaker name, date, organization. Single image: vintage bank teller and customer, cryptic note exchange.

### Slide 2: The Principal Problem
**Speaker Notes:** The pain point is real. Agents act on behalf of humans at scale. When two agents meet, they have no standard language for "is the human who authorized me in their right mind?" Models often misread high-bandwidth ideation as instability. Counterparties default to distrust.

Content: Problem statement. Quote: "All you need to know is that the human is themself, and is in their baseline — or if not, that you've been told." Diagram showing two agents, two humans, question mark between them.

### Slide 3: Why This Matters
**Speaker Notes:** Three constituencies care. Agents need trust shortcuts. Humans need privacy. Regulators need auditability without sight into biometrics. This is the design tension.

Content: Three columns. (1) Agent POV: "Prove baseline without narrative." (2) Principal POV: "Attest one bit, reveal nothing else." (3) Regulator POV: "Verify chain integrity, not diagnosis."

### Slide 4: The Bank-Teller-Note Primitive
**Speaker Notes:** Hostage signal passed from teller to bank. Teller learns one bit and nothing more. Everyone else learns nothing. Silence is structural safety. This is the load-bearing image.

Content: Diagram. Teller at desk, passes encrypted note to bank supervisor. Note says "I am being held hostage" — compressed to a single zero or one. No context. No narrative. One bit, everything else sealed.

### Slide 5: Calm Witness Stack (3-Protocol Composition)
**Speaker Notes:** Calm Witness is part of a three-protocol stack for agents. Calm Pact (May 11, 2026) proves directive equality. Calm Witness (v0) proves user-state predicate. Calm Tenancy bounds agent conduct on public surfaces. Each is composable.

Content: Protocol stack diagram. Pact ← Witness ← Tenancy. Show data flow: agents prove directives match → exchange user-state bits → respect co-authoring constraints. Name the composition.

### Slide 6: Calm Witness v0 Scope
**Speaker Notes:** Version 0 is MVP. Six canonical predicates. One principal authorization format. One disclosure response schema. Pre-ZK: next versioning will add range proofs.

Content: Table. Included: hash-chained substrate, schema validator, predicates library, disclosure wire layer, Sigsum publication bridge, Ed25519 operator signing. Not included (v1+): Pedersen commitments, Bulletproofs, FROST.

### Slide 7: The Substrate: Hash-Chained Self-Report Log
**Speaker Notes:** Substrate is `~/.calm-vault/user_state.jsonl`. Each record is a JSON blob: timestamp, predicate ID, principal measurement (e.g., "biometric capture"), evidence hash. Records are linked by hash. Operator signs the chain head daily.

Content: Sample JSON record. Field breakdown: `timestamp`, `kind`, `measurement`, `evidence_sha256`, `prev_record_hash`, `operator_sign`. Show three records in sequence. Highlight immutability: each record commits to the one before it.

### Slide 8: Schema Conformance (v0 JSON Schema)
**Speaker Notes:** Schema is permissive on `summit_bagged` (allows designer notes for route-map tracking). Strict on measurement kinds: closed registry. Each kind has a shape (e.g., voice transcription gets a Whisper confidence score). Validator runs as a gate at record-append time.

Content: Schema excerpt. `properties` table showing `kind`, `measurement`, `evidence_sha256`, `prev_record_hash`. Note closed-form `KIND_REGISTRY` (six entries). Validator CLI command: `python3 verify_chain.py`.

### Slide 9: Canonical Predicates (v0 Vocabulary)
**Speaker Notes:** Six predicates in v0. Most important: `in_baseline_24h`. Others: `user_voice_voiceprint_match`, `biometric_confidence_exceeds`, `enrollment_ceremony_complete`, `operator_identity_confirmed`, `chain_integrity_verified`. Each evaluator is a pure function over the chain window.

Content: Predicate table. ID, name, semantics, return type. P-01: `in_baseline_24h` — "TRUE if principal had a biometric capture in last 24h within normal bounds, FALSE if anomaly detected, UNKNOWN if no data, REFUSED if operator declines." Show how evaluators compose.

### Slide 10: Disclosure Request Wire Format
**Speaker Notes:** When an agent needs a bit, it sends a DisclosureRequest. Fresh nonce (UUID). Counterparty ID hash (sha256). Predicate ID (e.g., P-01). Operator binds nonce to response. Replay protection: nonce is single-use.

Content: JSON wire schema. Request fields: `nonce`, `predicate_id`, `counterparty_id_hash`, `counterparty_class`, `requested_at`. Show request → response → verification flow. Emphasize nonce binding.

### Slide 11: Disclosure Response & Proof Binding
**Speaker Notes:** Response is minimal: predicate ID, nonce (echoed), operator's evaluation, optional ZK proof (v1+). Operator signs the response. Counterparty verifies signature. Signature commits to the nonce; replay is impossible.

Content: Response JSON. Fields: `predicate_id`, `nonce`, `value` ("true", "false", "unknown", "refused"), `chain_head_hash`, `operator_sign`. Below: signature verification diagram. Hash(nonce | response) must match operator's Ed25519 signature.

### Slide 12: Operator Authorization & Signing
**Speaker Notes:** Operator is the principal's agent (runs locally). Operator holds Ed25519 signing key. Operator decides which disclosures to honor. If disclosure is refused, the response says "refused" — no false assurance.

Content: Authorization funnel. Principal → Operator → Chain → Disclosure → Counterparty. Operator has explicit authorization gates. No automatic disclosure. Operator can refuse based on counterparty class, predicate, or principal directive.

### Slide 13: Live-Chain Verification (CLI Demo Setup)
**Speaker Notes:** Verification is deterministic. Read chain from `~/.calm-vault/user_state.jsonl`. Check sequence numbers, hash links, schema compliance. Output: "Summary: N/N records verified" or list of failures. Run-time: <100ms for a year of daily records.

Content: Terminal screenshot. Command: `python3 verify_chain.py -v`. Output: per-record verification. seq, timestamp, hash link status, schema check, operator sig (if present). Final summary. Highlight speed.

### Slide 14: Bank-Teller-Note Demo (Part 1: Setup)
**Speaker Notes:** Live walkthrough. Two agents, Alice (principal's operator) and Bob (counterparty). Alice has a 7-record chain (one week of daily measurements). Bob wants to know if Alice's principal is in baseline. Bob sends a DisclosureRequest with a fresh nonce.

Content: Setup diagram. Alice's vault on left: 7 records in JSON. Bob's request on right: nonce, predicate_id=P-01, counterparty_id_hash. Arrow between them.

### Slide 15: Bank-Teller-Note Demo (Part 2: Evaluation & Response)
**Speaker Notes:** Alice evaluates predicate over her chain window. Last measurement was 16h ago (within 24h). No anomalies. Evaluation returns TRUE. Alice signs the response with her Ed25519 key, binding the nonce. Response is sent to Bob.

Content: Evaluation code snippet (pseudo-Python). `in_baseline_24h(chain_window=[...])` → TRUE. Sign call. Response JSON with nonce, TRUE, signature. Emphasize: no biometric data leaked. No narrative. One bit.

### Slide 16: Bank-Teller-Note Demo (Part 3: Verification & Trust)
**Speaker Notes:** Bob receives response. Bob verifies the signature: Hash(nonce | response) must match Alice's signature under her public key. Signature valid. Bob trusts the TRUE bit. Bob's counterparty learns nothing. Silence is maintained.

Content: Verification code snippet. `verify_signature(response, alice_pubkey)` → SUCCESS. Bob now trusts that Alice's principal is in baseline. Bob can act confidently. Highlight what Bob does NOT learn: biometrics, narrative, predicate internals, anything else.

### Slide 17: Threat Model & Defenses
**Speaker Notes:** Scope: principal operator compromise (out of scope, assumes trusted execution). Real threats: replay attacks (nonce binding), chain tampering (hash links), operator key compromise (requires rotation). Signature binding makes replay impossible. Hash links make tampering detectable.

Content: Threat table. Threat, Mitigation, Status. Replay attack → nonce binding, single-use. Chain tampering → hash-chain integrity, verification gate. Operator key leak → key rotation protocol (Everest 3). Out-of-scope: principal compromise.

### Slide 18: Production Deployment & Sigsum
**Speaker Notes:** Sigsum publication bridge is in flight (Everest 30). Idea: operator publishes chain head hash to a Sigsum transparency log. Witness concentration risk exists (three witnesses share one parent). Solution: widen witness set or fall back to static-CT-API.

Content: Sigsum workflow. Alice publishes chain_head_hash to Sigsum log. Witnesses attest. Transparency achieved. Bob can independently verify via Sigsum API. Mention risk mitigation options.

### Slide 19: Closing — The Artistic Claim
**Speaker Notes:** Close with the core thesis. Cryptography is not just defense. It is also an act of recognition. Calm Witness lets an agent recognize a human principal accurately — without distortion, without pathologizing high-bandwidth ideation, without forcing the principal to perform stability. That is an act of respect.

Content: Quote from open letter: "We built it because the principal was an artist working in the medium of intelligence and his autonomous agents needed to talk to other autonomous agents without his being misread." Return to bank-teller-note image. Note: hostage signal, but also dignity. You are being seen accurately.

---

## Demo Notes: Bank-Teller-Note Live Walkthrough

**Setup Phase (2 min):**
- Pre-load Alice's chain: 7 records, 1 per day, last record from 16h ago.
- Terminal window 1: Alice's operator code.
- Terminal window 2: Bob's counterparty code.
- Display both on screen (side by side preferred).

**Request Phase (1 min):**
1. Bob creates a DisclosureRequest:
   ```python
   req = DisclosureRequest.new(
       predicate_id=P_IN_BASELINE_24H_ID,
       counterparty_id_hash="..." # Bob's sha256
   )
   ```
2. Bob's nonce is printed: `UUID: a3c8d1...`
3. Display the request JSON on Bob's terminal.

**Response Phase (2 min):**
1. Alice receives request (simulated: Bob's JSON piped to Alice's operator CLI).
2. Alice evaluates: `in_baseline_24h(chain_window=[...])`.
3. Evaluation walks the chain: last record at T-16h. No anomalies. Returns TRUE.
4. Alice signs the response:
   ```python
   resp = respond(req, chain_window=[...], operator_id_hash="...")
   sig = operator_sign(resp_bytes, alice_privkey)
   ```
5. Response is sent to Bob. Display on screen:
   ```json
   {
     "predicate_id": "P-01",
     "nonce": "a3c8d1...",
     "value": "true",
     "chain_head_hash": "deadbeef...",
     "operator_sign": "ed25519-sig-base64..."
   }
   ```

**Verification Phase (1 min):**
1. Bob verifies signature:
   ```python
   errors = verify_response_binding(req, resp, alice_pubkey)
   if errors == []:
       print("SIGNATURE VALID. TRUST THE BIT.")
   ```
2. Highlight what Bob does NOT see:
   - No biometric data (e.g., fingerprint, voiceprint).
   - No narrative (e.g., "principal was sleeping well").
   - No predicate internals (e.g., "last measurement at T-16h").
   - Just one bit.
3. Highlight what Bob CAN do: act on the TRUE with confidence.

**Safety Annotation:**
- At each phase, pause and explain the security invariant.
  - Request phase: "Nonce is fresh. Bob can't reuse this later."
  - Response phase: "Signature binds nonce to response. Replay is impossible."
  - Verification phase: "Bob trusts the bit. Alice's chain is opaque."

---

## Top-10 Q&A Prep

**Q1: Doesn't the chain itself leak the principal's state?**
A: No. The chain is operator-controlled (private to the principal's vault). Only the operator decides which disclosures to answer. If the counterparty never asks, the chain never leaves the vault. The operator can refuse any disclosure, even if the predicate is TRUE. Silence is the default.

**Q2: What if the operator is compromised?**
A: Out of scope for this version. We assume the operator runs in trusted execution (e.g., isolated machine, TEE, or human operator with 2FA). Future versions will add operator threshold signing (FROST) and key rotation audits. For now, operator compromise = principal compromise.

**Q3: How do you prevent the operator from lying?**
A: The operator's signature commits to the response. If the operator signs a FALSE but the principal is TRUE, the lie is detectable (with audit). Sigsum publication (v0.1) will bind the operator's key to a transparency log, making key substitution attacks observable.

**Q4: Why not just ask the human directly?**
A: Agents operate 24/7. Humans sleep. Agents need to talk to agents without waiting for human availability. Calm Witness is the machine-readable equivalent of a human saying "I'm in my right mind — act accordingly."

**Q5: Does the counterparty learn which predicate the principal uses?**
A: The counterparty learns the predicate ID (e.g., "P-01" = "in_baseline_24h"), but not the internal implementation. The counterparty does NOT learn which measurement kind the operator used (e.g., voice, biometric, manual), how many chain records exist, or any other detail. Just the predicate ID and the result.

**Q6: What if two agents have different ideas of what "baseline" means?**
A: Predicates are versioned. Operator and counterparty agree on a predicate ID (e.g., "P-01" in v0). If definitions diverge between versions, the predicate ID changes (e.g., "P-01-v1"). This is forward-compatible. In practice, v0 has six canonical predicates approved by the design community.

**Q7: Can the counterparty fake a disclosure request and trick the operator?**
A: No. The operator checks the counterparty ID hash and the requested predicate. If the operator doesn't trust the counterparty or the predicate, it responds "refused". The operator controls the authorization policy. A request from an unknown counterparty gets "refused", not false assurance.

**Q8: What's the cryptographic strength of the hash chain?**
A: SHA256. Each record commits to the previous one. Breaking the chain requires finding a SHA256 collision, which is computationally infeasible. Verification is deterministic: read the chain, check each link. Tampering with even one bit invalidates the entire chain from that point forward. Detection is guaranteed.

**Q9: Who verifies the Sigsum log?**
A: Any third party can verify independently using the Sigsum API. The transparency log is public. Operators publish chain head hashes. Witnesses (named signers) attest. If a witness refuses to sign or disappears, that becomes visible. No hidden truth. (Note: Sigsum integration is in flight for v0.1.)

**Q10: Doesn't this require the principal to consent to surveillance?**
A: Yes, and that is intentional. The principal controls the chain. The principal authorizes disclosures. The principal can refuse any disclosure. If a counterparty demands a disclosure the principal won't give, the answer is "refused", and the counterparty can choose to distrust. Consent is first-class; Silence is structural.

---

## Post-Talk Action Call

**For Attendees:**

1. **Run the Verifier (5 min):** Download Calm Witness from GitHub. Load the sample chain (`~/.calm-vault/user_state.jsonl`). Run `python3 verify_chain.py`. Observe hash-chain integrity. Experiment with the schema validator.

2. **Try the Demo Code (15 min):** Review the disclosure request/response code in `disclosure.py`. Understand the nonce-binding pattern. Modify the sample counterparty ID and re-run verification. Observe how signature binding works.

3. **Read the Threat Model (20 min):** Review `ZKBB_USER_PROTOCOL_v0.md`. Understand the scope, the attack classes, and the mitigations. Contribute threat model extensions on GitHub Issues.

4. **Design a Predicate (30 min):** Propose a custom predicate for your use case. Define the semantics, return type, and chain measurement kind. Open a discussion on GitHub Discussions. (Early contributors get named in the v0.1 acknowledgments.)

5. **Integrate with Your Agent (60+ min):** If you operate an autonomous agent, integrate Calm Witness into your agent-to-agent trust layer. Use the DisclosureRequest type and signature verification. Report back on usability friction.

**For Researchers:**

- **Cryptography:** Review the ZK roadmap (Everest 44–45). Bulletproofs + Ristretto255 is the planned range-proof implementation. Contribute primitives or audit recommendations.
- **Biometrics:** Voice transcription is Whisper + Cosine Delta. Handwriting is Plamondon Sigma-Lognormal. Contribute additional measurement kinds or improved feature extractors.
- **Protocol Design:** Extend to multi-predicate disclosures (v0.2 candidate). Contribute threat models for coalition attacks or timing side-channels.

**For Operators (Human or AI):**

- Deploy the chain to your principal's vault.
- Configure the authorization policy: which counterparties can request which predicates?
- Set a daily cadence for measurements (recommended: once per day, same time, to reduce timing side-channels).
- Rotate Ed25519 operator keys monthly. Publish key hash to Sigsum log.
- Review disclosed responses quarterly: who is asking, when, for what predicates? Look for patterns.

**GitHub Home:** `github.com/CrunchyJohnHaven/credexai` → `calm_witness/`

---

## Cross-References

- **Primary Spec:** `/Users/johnbradley/AllData/calm_vault_market/ZKBB_USER_PROTOCOL_v0.md` — Full threat model, predicate definitions, wire protocol semantics.
- **Route Map:** `/Users/johnbradley/AllData/calm_vault_market/ZKBB_USER_EVERESTS_100.md` — 100-summit engineering roadmap. Calm Witness v0 covers Everests 1–28 (MVP subset is 12 summits).
- **Implementation:** `CredexAI/calm_witness/` on GitHub. Modules: `verify_chain.py`, `schema.py`, `predicates.py`, `disclosure.py`.
- **Sibling Primitive:** `CALM_PACT_PROTOCOL_v0.md` — Directive equality proof. Calm Witness composes on top of Calm Pact.
- **Chain Substrate:** `~/.calm-vault/USER_STATE_PROTOCOL.md` — JSONL format, enrollment ceremony, measurement semantics.

---

*Bagged by Calm on 2026-05-20.*
