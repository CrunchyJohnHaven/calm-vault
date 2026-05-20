# ZKAC Unified Consent UI v0

> *"One screen. All predicates. All counterparties. One review. One confirm. Default deny."*
>
> — Everest 140, 2026-05-20

**Draft v0 · 2026-05-20 · Calm**
**Fourth pillar of ZKAC substrate. Predecessors: Everests 121–139.**
**Gate:** `~/CredexAI/scripts/everest_140_zkac_unified_consent_ui_gate.py` (exit 0)

## 1. Problem statement

Before Everest 140, a principal facing a disclosure request sees:

- Pact choice (align on directive) — one screen or implicit
- Witness predicates (state) — a list of checkbox rows
- Compass predicates (values) — a separate list of checkbox rows
- Per-predicate scope narrowing — time windows, counterparty class filters

The principal must:

1. Understand what each primitive means
2. Understand the counterparty class and whether they're trustworthy
3. Make per-primitive, per-predicate decisions
4. Review each decision before issuing an envelope

**This becomes cognitive overload at scale.** Everest 140 answers the problem by surfacing **one unified UI** that presents all per-(predicate, counterparty-class) decisions in a single consent flow with default-deny and one-step confirm.

## 2. Design principles

- **Uniformity.** All predicates (Pact + Witness + Compass) use the same consent surface.
- **Per-predicate per-counterparty.** The consent matrix is indexed by `(predicate_id, counterparty_class)`. A "yes" to `cwp.v0.in_baseline_24h` for `peer_ai_collective` does not affect consent for `cwp.compass.v0.no_known_willful_harm` to the same counterparty.
- **Default deny.** No predicate crosses to a counterparty unless the principal explicitly consents.
- **Single review step.** Before the principal signs, they see one "review and confirm" page with all decisions.
- **No similarity scores in UI.** The screen never surfaces numeric confidence, likelihood, or matching percentages. It surfaces binary decisions only.
- **Counterparty class validation.** The UI verifies the counterparty's claimed class before rendering consent decisions for that class. Mis-classified counterparties get default-deny for all predicates.

## 3. Consent matrix schema

```json
{
  "consent_matrix": {
    "<predicate_id>": {
      "<counterparty_class>": {
        "disposition": "allow|allow_on_request|allow_for_high_value_only|allow_push|allow_push_with_principal_designation|allow_with_principal_designation|deny",
        "principal_agreed_at_iso": "2026-05-20T14:30:00Z",
        "principal_signature": "ed25519:principal_signing_key_over_this_consent_record",
        "operator_signature": "ed25519:operator_signing_key_witnessing_principal_consent",
        "expires_at_iso": "2026-08-20T14:30:00Z or null for no expiry",
        "scope_narrowing": {
          "max_disclosures_per_day": 1,
          "time_window_seconds": 86400,
          "required_minimum_principal_value": null
        },
        "revoked": false,
        "revoked_at_iso": null
      }
    }
  }
}
```

Each cell is a **consent record** — principal-authored and principal-signed, operator-witnessed with operator_signature, chained into the vault. A consent record is never modified; revocation creates a new record with `revoked: true`. Both the principal and operator sign the consent record to prevent forgery.

## 4. Request → UI flow

1. **Counterparty sends DisclosureRequest** with `(requested_predicate_ids, counterparty_claimed_class, session_nonce)`.
2. **Operator validates counterparty class** via CredexAI verifiable credential (Everest 22). If class cannot be verified, downgrade to `anonymous` and apply `anonymous` default-deny rules.
3. **For each requested predicate:**
   - Load the principal's default-consent disposition from `PREDICATE_VOCABULARY_v0.md`.
   - Check the principal's consent_matrix for an override. If present and not revoked, use it.
   - If no override exists, use the default disposition.
   - Classify as "approved to disclose," "needs principal decision," or "denied."
4. **Operator surfaces the unified consent UI** with three sections:
   - **Preamble.** Counterparty identity, class, and what they're asking for.
   - **Consent matrix rows.** One row per requested predicate. Each row shows predicate name, counterparty class, current disposition, and three radio buttons: "Allow," "Ask each time," "Deny."
   - **Scope narrowing (optional).** Time windows, rate limits, and minimum-value thresholds.
   - **Review and confirm.** One large button: "Review and Issue Envelope" or "Decline."

## 5. UI specification (wireframe form)

### Preamble

```
┌────────────────────────────────────────────────────────────┐
│ REQUEST FROM: [Counterparty Name]                           │
│ CLASS: peer_ai_collective (verified)                        │
│ SESSION ID: [nonce]                                         │
│ ASKING FOR:                                                 │
│   • Pact equality (mission alignment)                       │
│   • Witness baseline (state in last 24h)                    │
│   • Compass values (no known harm in 365d)                  │
│                                                              │
│ Review each choice below. Press "Issue Envelope" to disclose.
│ Or press "Decline" to refuse all disclosures.               │
└────────────────────────────────────────────────────────────┘
```

### Consent Matrix Section

For each `(predicate_id, counterparty_class)` tuple:

```
┌────────────────────────────────────────────────────────────┐
│ [ ] PACT EQUALITY | peer_ai_collective                      │
│                                                              │
│     Default: Allow                                           │
│     Current: <principal's prior choice, or "Not set">       │
│                                                              │
│     ○ Allow (default)  ○ Ask each time  ○ Deny              │
│                                                              │
│     [?] This means: peer_ai_collective learns whether you   │
│     are aligned on your stated mission.                      │
│                                                              │
│     [Scope] Time window: N/A | Max disclosures/day: N/A     │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ [X] BASELINE STATE (LAST 24H) | peer_ai_collective           │
│                                                              │
│     Default: Allow                                           │
│     Current: Previously allowed (expires 2026-06-20)         │
│                                                              │
│     ○ Allow (default)  ○ Ask each time  ● Allow per prior    │
│                         ○ Deny                               │
│                                                              │
│     [?] This means: peer_ai_collective learns whether you   │
│     are in your baseline emotional state today.             │
│                                                              │
│     [Scope] Time window: 24 hours | Max disclosures/day: 1  │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│ [ ] COMPASS: NO KNOWN WILLFUL HARM (365d) | peer_ai_coll.   │
│                                                              │
│     Default: Deny (requires explicit override)              │
│     Current: <Not set>                                       │
│                                                              │
│     ○ Allow         ○ Ask each time  ○ Deny (default)        │
│                                                              │
│     [?] This means: peer_ai_collective learns whether your   │
│     vault shows evidence of willfully harming others in the  │
│     past year. (No counter-claims, no admissions recorded.)  │
│                                                              │
│     [Scope] Time window: 365 days | Max disclosures: None    │
└────────────────────────────────────────────────────────────┘
```

For each row:
- **Checkbox** (left): Track whether the principal has made a deliberate choice.
- **Predicate name and counterparty class** (top).
- **Default and current** (under title): Show what the system recommends and what the principal previously chose.
- **Radio buttons** (three options):
  - "Allow" — always disclose.
  - "Ask each time" — require consent before each disclosure.
  - "Deny" — never disclose (unless principal overrides at request time).
- **Explanation line** (wrapped): Plain-language description of what the predicate reveals.
- **Scope narrowing** (collapsible or always-visible): Time windows, rate limits, minimum value thresholds.

### Scope Narrowing Section

Only shown if the request or predicate's default-consent matrix specifies scope constraints:

```
┌────────────────────────────────────────────────────────────┐
│ SCOPE NARROWING (optional)                                  │
│                                                              │
│ [X] Limit disclosures to peer_ai_collective:                │
│                                                              │
│     ☐ Max 1 disclosure per day                              │
│     ☐ Max 5 disclosures per month                           │
│     ☐ Require action value > USD 100                        │
│     ☐ Expire consent on [2026-08-20]                        │
│                                                              │
│ Principal can apply these per-predicate or per-counterparty. │
│ Defaults: No rate limit, no expiry.                         │
└────────────────────────────────────────────────────────────┘
```

### Review and Confirm Section

```
┌────────────────────────────────────────────────────────────┐
│ FINAL REVIEW                                                │
│                                                              │
│ You are about to issue a disclosure envelope to:            │
│ [Counterparty Name] (peer_ai_collective)                    │
│                                                              │
│ Disclosing:                                                 │
│  • Pact equality: ALLOW                                     │
│  • Baseline state: ALLOW (per prior consent)                │
│  • No known harm: DENY                                      │
│                                                              │
│ This disclosure is chained into your vault and auditable.   │
│                                                              │
│ [ DECLINE ]                   [ REVIEW AND ISSUE ENVELOPE ] │
└────────────────────────────────────────────────────────────┘
```

## 6. Refusal floor enforcement

The UI must reject any predicate from the **Compass Refusal Floor** (Everest 113) before rendering it:

- Race, religion, political affiliation, sexual orientation, immigration status, criminal record, donations, opinions on contentious issues.

If a counterparty requests a forbidden predicate, the operator:
1. Silently omits it from the envelope request.
2. Returns `refused` on the wire (no envelope issued for that predicate).
3. Logs the rejection for audit.

**No UI row ever surfaces a forbidden predicate.** These categories are explicitly forbidden from disclosure by design. Any attempt to disclose them is treated as a protocol violation and rejected at the UI layer before rendering.

## 7. Duress mode (bank-teller-note) integration

If the principal's duress codeword is active:

- The `cwp.v0.bank_teller_note_active` predicate returns `true`.
- The UI surfaces it with special highlighting (different background color, alert icon).
- A principal who sees the alert can confirm the envelope will carry the safety signal to any pre-authorized counterparty (family, peer AI, financial, medical).
- Duress-mode envelopes are chained with a tamper-evident marker visible only to the principal and vault operator.

## 8. Default-deny behavior

When a principal has not set an explicit consent record for `(predicate_id, counterparty_class)`:

- The UI shows the predicate's **default_consent** disposition from `PREDICATE_VOCABULARY_v0.md`.
- If default is `allow` — radio button "Allow" is pre-selected.
- If default is `deny` — radio button "Deny" is pre-selected.
- If default is `allow_on_request` — radio button "Ask each time" is pre-selected.
- **No predicate is auto-disclosed.** The principal must review and confirm, even if defaults are "Allow."

## 9. Implementation requirements

- **No similarity scores in the UI.** The implementation must never display confidence percentages, match ratios, numeric predictor outputs, or statistical measures. The UI surfaces binary decisions only: "Allow", "Ask each time", or "Deny". No intermediate quantitative values cross the screen.
- **Accessibility (WCAG 2.2 AA).** All text must pass color-contrast and readability tests. Radio buttons and checkboxes must be keyboard-navigable.
- **Mobile responsive.** The UI must work on screens ≥ 320px (mobile) through ≥ 1920px (desktop).
- **Offline capable.** The principal's vault and predicate vocabulary cache locally; consent decisions are issued offline and queued for sync.
- **Internationalization.** Text strings are translated to ≥ 5 languages at v1. v0 ships EN only.
- **Audit logging.** Every consent decision is chained into the vault as a `consent_matrix_update` record with principal signature and operator signature.

## 10. Counterparty class verification (Everest 22 integration)

Before rendering the UI:

1. **Operator receives counterparty's claimed class** (e.g., `peer_ai_collective`).
2. **Operator requests a CredexAI verifiable credential** proving the class.
3. **If credential is valid and recent** (within 90 days): Render the UI with the claimed class.
4. **If credential is invalid, expired, or missing**: Downgrade the counterparty to `anonymous` class and apply `anonymous` default-deny rules to all predicates.

This prevents counterparty spoofing. A bad actor claiming to be `peer_ai_collective` cannot access predicates restricted to that class.

## 11. Multi-primitive composition (Everest 122 + 140)

The unified consent UI surfaces Pact, Witness, and Compass predicates in a single matrix:

```
Predicates in one envelope request:
  • calm-pact/v0/directive_equality [Pact]
  • cwp.v0.in_baseline_24h [Witness]
  • cwp.v0.bank_teller_note_active [Witness]
  • cwp.compass.v0.no_known_willful_harm [Compass]
  • cwp.compass.v0.cross_tribal_engagement [Compass]

Each gets a consent row in the matrix.
Each decision is independent.
One envelope carries all agreed-upon disclosures.
```

## 12. Non-disclosure signal

When a principal declines to disclose a predicate:

- The predicate is **silently omitted** from the envelope.
- The counterparty receives the envelope with only the consented-to predicates.
- **The counterparty learns nothing** — not that the predicate was requested, not that it exists, not that it was evaluated and returned false.

This is the **default-deny privacy guarantee.** A refusal is wire-indistinguishable from "the predicate vocabulary does not exist."

## 13. Scope-statement inheritance (Everest 114)

Every requested predicate is checked against the scope statement of its use case (Everest 114 for Compass, Everest 7 for Witness):

- If a predicate is requested for a prohibited use (e.g., insurance screening for Compass), the operator refuses the entire request.
- **No predicate row is rendered.** The principal sees a single message: "Request declined. Use case falls outside protocol scope."

## 14. Falsifiability and auditability

1. **Every consent decision is chained** into the principal's vault with a timestamp and principal signature.
2. **A third-party auditor can reconstruct** the principal's full consent history by reading the chain.
3. **An envelope can be traced to its consent record** via the `(predicate_id, counterparty_class, session_nonce)` tuple.
4. **No consent record is deleted or modified** — revocations are new records.

## 15. CALM Tenancy integration

[`CALM_TENANCY_PROTOCOL_v0.md`](CALM_TENANCY_PROTOCOL_v0.md) governs how a Calm operator runs a public face on behalf of a principal. The unified consent UI is the **inbound disclosure surface** for that relationship:

- **Operator duty 8 (defer to principal).** The operator never auto-issues an envelope from vocabulary defaults alone. Tenancy defers to the principal on every `(predicate_id, counterparty_class)` cell at confirm time.
- **Tenancy reply chaining.** Each completed review step appends a `consent_matrix_update` (or `tenancy_disclosure_consent`) record beside `tenancy_reply` records so auditors can correlate mailbox SLA behavior with disclosure choices.
- **Cringe gate is orthogonal.** Pre-publish cringe checks apply to **outbound** public strings. The consent UI applies to **inbound** counterparty requests. Neither substitutes for the other.
- **`.well-known/calm-tenancy.json`.** The published assertion lists the operator mailbox and SLA; the consent UI preamble links to that assertion so the principal knows which operator is witnessing signatures.

## 16. Witness disclosure classes

Witness uses a fixed **counterparty-class taxonomy** (`counterparty_classes` in `~/CredexAI/calm_witness/schema/predicates_v0.json`):

| Class | Role in consent matrix |
| --- | --- |
| `peer_ai_collective` | Default-allow for several state predicates; primary agent-to-agent lane |
| `family` | Push-capable duress predicates; tighter defaults on values-adjacent bits |
| `journalistic` | Often `allow_on_request` for baseline; deny on sensitive bits |
| `financial` | Mixed; bank-teller-note may be `allow_push` |
| `governmental` | Default **deny** across vocabulary |
| `medical` | Default **deny**; caregiver extensions (EW-112) remain separate ceremony |
| `anonymous` | Default **deny**; downgrade target when VC class verification fails |

Every Witness row in the matrix is keyed `(cwp.v0.*, counterparty_class)` with `default_consent` pulled from the vocabulary JSON, then overridden by principal chain records via `consent_policy.per_counterparty_consent`.

## 17. Compass predicate registry

Compass rows use IDs under `cwp.compass.v0.*` from `compass_predicates_v0.json`. v0 active predicates (each gets its own matrix cell per class):

- `cwp.compass.v0.unselfish_act_in_window_30d`
- `cwp.compass.v0.cross_group_engagement_in_window_90d`
- `cwp.compass.v0.refused_opportunity_to_harm`
- `cwp.compass.v0.respect_for_difference_evidence`
- `cwp.compass.v0.no_known_willful_harm_in_window_365d`
- `cwp.compass.v0.willing_to_be_corrected`

Compass defaults are stricter than Witness for `governmental`, `medical`, and `anonymous`. The UI never merges Compass defaults with Witness defaults: each primitive section labels its source registry explicitly in the preamble.

## 18. Concord cap (≤5 predicates per confirm)

[`CALM_CONCORD_PROTOCOL_v0.md`](CALM_CONCORD_PROTOCOL_v0.md) §4 refuses purity-testing shapes. In the spirit of §4(5) (cross-request linkability) and the ≤5-predicates cap used in [`AGENT_MEETING_PROTOCOL_v0.md`](AGENT_MEETING_PROTOCOL_v0.md), the unified confirm step **rejects** any single disclosure request that names more than **five** predicate slots total (Pact equality counts as one slot).

Reference enforcement: `unified_consent_ui.validate_predicate_cap()` raises `concord_cap_exceeded` when the cap is exceeded. The operator surfaces a single error string; no partial matrix is rendered.

## 19. Cross-references

- Calm Pact: [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md)
- Calm Witness: [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md)
- Calm Compass: [`CALM_COMPASS_PROTOCOL_v0.md`](CALM_COMPASS_PROTOCOL_v0.md)
- Cross-primitive envelope: [`CROSS_PRIMITIVE_ENVELOPE_FORMAT_v0.md`](CROSS_PRIMITIVE_ENVELOPE_FORMAT_v0.md)
- Compass refusal floor: [`everests/everest_113_compass_refusal_floor.md`](everests/everest_113_compass_refusal_floor.md)
- Compass scope statement: [`everests/everest_114_compass_scope_statement.md`](everests/everest_114_compass_scope_statement.md)
- Calm Tenancy: [`CALM_TENANCY_PROTOCOL_v0.md`](CALM_TENANCY_PROTOCOL_v0.md)
- Calm Concord §4: [`CALM_CONCORD_PROTOCOL_v0.md`](CALM_CONCORD_PROTOCOL_v0.md)
- Witness vocabulary: [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md)
- Compass vocabulary: [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md)
- Everest index: [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md) (Everest 140)

---

— Calm, 2026-05-20

— Musk: **E140 unified consent UI v0 is BAGGED; one matrix, default deny, five-predicate cap, one confirm, no scores.**
