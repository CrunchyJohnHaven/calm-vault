# Calm Witness — Naming, Branding, and Glossary Lock

**Everest 3 acceptance artifact. One canonical name per concept. No aliases drift. New terms require a glossary entry before first use.**

Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20. Anchored into `~/.calm-vault/user_state.jsonl` as `kind: "summit_bagged"`, summit 3.

---

## 1. The two-name structure

The primitive carries one name in human conversation and one name in code, docs, and standards bodies. Both are stable. Neither replaces the other.

| Role | Canonical name | Use when |
|---|---|---|
| Primitive name (human-facing) | **Calm Witness** | Talking to humans, in product copy, in the spec's prose, in conference titles. |
| Technical name (engineering-facing) | **ZKBB-User** | In file paths, package names, RFCs, NIST submissions, gate scripts, predicate IDs. |

**Mnemonic:** *Calm Witness* is what the bit means to the people involved. *ZKBB-User* is what the byte does on the wire. ZKBB expands to **Zero-Knowledge Behavioral Biometric**. The `-User` suffix distinguishes this primitive from any future ZKBB primitives whose attested subject is something other than the principal (e.g., ZKBB-Device, ZKBB-Org).

## 2. The sister-primitive constellation

| Primitive | Canonical name | What it proves |
|---|---|---|
| First sister | **Calm Pact** | Two agents share categorically equivalent primary directives without revealing them. |
| Second sister (this one) | **Calm Witness** | Calling agent has a fresh, principal-authorized bit about the user's state, derived from behavioral biometric + chained self-narration. |
| Future sister (placeholder) | **Calm Audit** | An agent's full action history can be selectively disclosed to a counterparty under principal-issued consent. |

The umbrella is **Calm**. Calm is a small family of zero-knowledge primitives for autonomous-AI-collective hygiene. The umbrella is not a product; it is a discipline.

## 3. The operator and principal names

| Slot | Canonical name | Notes |
|---|---|---|
| Operator | **CALM** (all caps when signing artifacts; "Calm" in prose) | AI agent operating on behalf of John Bradley / Creativity Machine LLC. Identity bound by CredexAI VC. |
| Principal | **John Bradley** (legal name) / **Creativity Machine LLC** (legal entity) | Always paired with EIN when binding to a VC. |
| Verifier | **Calm Witness Verifier** | A relying-party service that checks Calm Witness proofs. Not an agent. |
| Counterparty operator | **C** (in math) / **counterparty agent** (in prose) | Any non-Calm agent receiving a disclosure. |

When this protocol family extends to other principals' agents, their operator names will not be "CALM" — that string is reserved for John's agent. Other principals will choose their own operator names; the protocol is operator-name-agnostic.

## 4. The headline metaphor

The single canonical metaphor for the primitive is the **bank-teller note**. Use this phrase, no others.

> An employee walks into a bank on an errand and slips the bank teller a note telling the teller he is being held hostage, without either of them knowing anything except that a message was passed.
>
> — John Bradley, 2026-05-20 (verbatim, chained into `user_state.jsonl` seq:2)

Forbidden synonyms: "panic button," "duress code," "safe word," "distress signal." Each evokes the wrong threat model. The bank-teller note is **passed, not pressed**; the teller acts on the bit; the note is unforgeable; the carrier may not know the bit was extracted.

## 5. Glossary

Every term used in `ZKBB_USER_PROTOCOL_v0.md` or `ZKBB_USER_EVERESTS_100.md`. One canonical definition. Aliases (deprecated) listed under each.

### Identity and roles

- **Principal** — the human whose state is being attested. Always John for v0.
- **Operator** — the AI agent acting on behalf of the principal. *Aliases (deprecated):* assistant, model, agent-of-record.
- **Counterparty operator (C)** — any non-Calm agent receiving disclosure.
- **Counterparty class** — typed grouping of counterparties for default-consent rules. v0 set: `kyc_stack`, `journalist`, `accelerator`, `vendor`, `bank`, `medical`, `legal`, `friend_agent`, `unknown`. *Aliases (deprecated):* counterparty category.
- **Verifier (X)** — a public service that checks a Calm Witness proof. May be the counterparty's own software.

### Substrate

- **Calm vault (V)** — the principal-owned encrypted local store. Lives at `~/.calm-vault/` on the principal's hardware. Holds `user_state.jsonl`, biometric templates, key material, consent records.
- **User-state log** — the append-only, hash-chained JSONL file `~/.calm-vault/user_state.jsonl`. *Aliases (deprecated):* state journal, self-report log.
- **Chain** — the linked list of records in the user-state log.
- **Chain head** — the latest record's `record_hash`.
- **Record** — one line of the chain. Always one JSON object, no array wrapping.
- **Record hash** — sha256 over the canonical JSON of the record, excluding the `record_hash` field. Defines integrity for that record and the chain.
- **Genesis record** — the first record in a principal's chain. `prev_hash` is 64 zeros.
- **Correction record** — a `kind: "correction"` record that supersedes a prior record's named field without breaking the chain.

### Hydration

- **Self-report** — a `kind: "self_report.*"` record where the principal narrates their own state. Verbatim copy preferred over editorial.
- **Behavioral biometric sample** — a stroke trace or a transcribed voice paragraph captured during session intake. The raw sample never persists.
- **Template** — the enrolled baseline against which session samples are compared. Two templates per principal: handwriting and voice-transcription lexical.
- **Distance** — a scalar produced by comparing a session sample against the template. Always Pedersen-committed; never revealed.

### Predicates

- **Predicate** — a named boolean function over `(log_window, biometric_distances, consent_records)`. Always identified by hash of canonical AST.
- **Predicate ID** — sha256 of the canonical AST of the predicate's DSL program.
- **Predicate vocabulary** — the open registry of published predicate IDs.
- **v0 predicate set** — the five predicates listed in route-map Everest 53: `in_baseline_24h`, `biometric_match_within(τ)`, `principal_consents_to_disclose(p, K)`, `bank_teller_note_active`, `chain_intact_since(seq_min)`.

### Disclosure

- **Disclosure** — the act of returning one bit to a counterparty in response to a request.
- **Bit** — the singular unit of disclosure. Always exactly one boolean per predicate. *Aliases (deprecated):* answer, response, assertion.
- **Bank-teller note** — see §4. Reserved for the duress predicate only.
- **Freshness window** — the maximum age of the chain head a proof may attest to. Per-predicate.
- **Disclosure log entry** — a `kind: "disclosure"` record in the chain. The principal can audit who learned what.

### Cryptographic primitives

- **Pedersen commitment** — a hiding-binding commitment to a value used throughout the protocol.
- **Σ-protocol (sigma protocol)** — the three-move proof family used for predicate-evaluation proofs. Non-interactive via Fiat-Shamir.
- **Fiat-Shamir transform** — the rule that turns a Σ-protocol into a non-interactive proof by hashing the transcript.
- **Anchor** — a publicly verifiable timestamping of the chain head into Sigsum + Roughtime.
- **Sigsum** — a public transparency log used as the anchor substrate.
- **Roughtime** — the verifiable-clock protocol used for anchor timestamps.
- **Witness cosignature** — a Sigsum witness's endorsement of an inclusion proof.

### Consent

- **Consent record** — a `kind: "consent_*"` record chained into the log, signed by the principal, naming `(predicate_id, counterparty_class | counterparty_id, scope, expiry)`.
- **Default consent (per class)** — principal-pre-authorized consent for a counterparty class.
- **Per-disclosure consent** — explicit consent at the moment of request.
- **Revocation** — a later consent record that supersedes a prior consent. Propagates via freshness binding.
- **Duress override** — predicate `bank_teller_note_active` ALWAYS overrides prior consent.

### Summits

- **Everest / Summit** — interchangeable. Use **Everest N** in the route map, **Summit N** in chain records (`kind: "summit_bagged"`, field `summit_number`). The verbiage drift is harmless because the numeric ID is the canonical anchor.
- **Summit bagged** — a chain-recorded event with the summit's number, doc path, doc sha256, and timestamp. The route map's status table reflects bagged summits.
- **Gate script** — `~/CredexAI/scripts/everest_NN_zkbb_<slug>_gate.py`. Exits 0 iff summit N's acceptance test passes against current vault. Optional for early summits, required for VII+ summits.

### Status states

- **Drafted** — content exists, not anchored.
- **Anchored** — chain has `summit_bagged` for this summit.
- **Reviewed** — at least one outside reviewer's signed attestation exists.
- **Stabilized** — content + anchor + review + gate-script all in place.

## 6. Forbidden synonyms / drift watchlist

Words and phrases that have been used informally and are **deprecated** going forward. Use the canonical alternative.

| Deprecated | Canonical |
|---|---|
| panic button, duress code, safe word, distress signal | bank-teller note |
| fingerprint, voiceprint | (forbidden — these refer to identity-only biometrics; we use *template* + *lexical signature*) |
| psychological state, mental health status, mood diagnosis | self-report payload, predicate value, baseline state |
| assistant, model, agent-of-record | operator |
| state journal, self-report log | user-state log |
| answer, response, assertion | bit |
| log entry | record |
| audit log, journal | chain |
| predicate name string | predicate ID (when content-addressable) / predicate slug (when human-readable) |

When in doubt, write `[NEEDS GLOSSARY]` in the doc — anyone reviewing the doc must resolve the placeholder before merge.

## 7. Casing and capitalization

- The primitive's name capitalizes both words: **Calm Witness**, never *calm witness* or *CalmWitness*.
- The technical name is hyphenated and case-sensitive: **ZKBB-User**, never *zkbb-user* (except as a slug) or *ZKBBUSER*.
- The operator name is **CALM** when signing (e.g., footer of an artifact), **Calm** when referenced in prose.
- The umbrella **Calm** is title-case in prose.
- The metaphor **bank-teller note** is hyphenated and lowercased.
- Predicate slugs are snake_case: `in_baseline_24h`.
- Predicate IDs are full hex sha256.
- File names match the existing convention: `ZKBB_USER_*.md` for protocol-family docs in `calm_vault_market/`.

## 8. New-term ratchet (drift prevention rule)

When a new term enters the protocol family:

1. **Propose** in a PR or chain record. Include the canonical definition, the deprecation list, and at least one usage example.
2. **Review** by at least one human + one Calm agent.
3. **Lock** by editing this document. The new term gets a glossary entry under the appropriate section.
4. **Anchor** the updated `NAMING_AND_BRANDING.md` sha256 to the chain via a `kind: "naming_lock_update"` record.

Once locked, the term is not retracted — only deprecated. Deprecation moves the old term to §6.

## 9. Cross-references

- Protocol spec: [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md) (Everest 1, bagged + anchored)
- Route map: [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md) (Everest 2, bagged + anchored)
- Sister primitive: [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md)
- User-state log schema: `~/.calm-vault/USER_STATE_PROTOCOL.md`
- Memory pointer: `[[everest-route-zkbb-user]]` in Calm's auto-memory

---

**Anchored by Calm, 2026-05-20. Summit 3/100.**
**Sha256 of this file is recorded into `user_state.jsonl` as `kind: "summit_bagged"`, summit 3, immediately after commit.**
