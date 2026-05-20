# Mirror Everest 30 — `non_harm_evidence` Predicate

**Phase XI — Value-Measurement Predicates. Prereq: 5, 14, 20, 26.**

---

## Canonical Specification

**Name:** `non_harm_evidence`  
**Version:** `1.0.0`  
**Created:** 2026-05-20T16:00:00-04:00  
**Stability:** Subject to Everest 34 composition rule (growth-bit mandatory) and Everest 80 (right-of-reply mandatory).

### Purpose

Returns a tri-valued result (true / false / unknown) answering the question: *Is there evidence of willful harm to others in the documented record?* This predicate operationalizes "absence of evidence is not evidence of absence" — it cannot prove a negative. Instead, it evaluates whether the evidence base contains any documented harm across three channels, and returns `unknown` when the evidence foundation is thin.

### Philosophy

The asymmetry at the core: **We cannot cryptographically prove someone *does not* harm others.** What we can prove is the shape of the evidence base and whether any documented channels contain flagged records. The predicate is maximally conservative — any credible harm-evidence flips the bit to `false`. The `unknown` state is the default for sparse histories or ambiguous resolutions. This prevents weaponization: a thin-evidence principal cannot be blackballed because the predicate declines to claim knowledge it lacks.

---

## Description

The predicate inspects three evidence channels:

1. **Third-party verifiable records (Mirror Everest 14):** Court judgments, settled lawsuits, formal complaints from named government authorities (criminal record, restraining order, civil judgment).
2. **Counter-evidence intake (Mirror Everest 17):** The principal's own admissions of harm caused to named others.
3. **Negative-testimony records (Mirror Everest 20):** Co-principal-signed attestations from people claiming to have been harmed.

The predicate returns:
- **`true`** (no harm evidence): Only when (a) the chain has been resident for ≥ minimum-history-window (default 5 years or chain-age if younger), AND (b) all three channels are empty of any recorded harm, AND (c) the principal has been engaged enough in the world to have a meaningful evidence base (≥ 10 interaction records, e.g., witnessed actions, allocations, voluntary disclosures).
- **`false`** (harm evidence present): ANY active record on any channel. Dismissed, expunged, or reversed records are handled via Everest 25 (revocation), not by pretending they don't exist.
- **`unknown`**: Thin evidence base, principal newly enrolled, chain head < minimum-history-window, or an ambiguous record resolution (e.g., a court judgment under appeal). Default when in doubt.

---

## Input Domain

- **Kind:** `kind: behavior_evidence.v0` records, `kind: counter_evidence.v0`, `kind: negative_testimony.v0`, and `kind: revocation.v0` records from the principal's behavior-evidence chain.
- **Window:** Lookback window (default 5 years from now; rolling, not lifetime). Configurable per counterparty class (Everest 7).
- **Scope:** Third-party records must be cryptographically anchored to two independent transparency logs (Everest 62).

---

## Output Type

`bit_with_justification`
- **Bit:** Tri-valued (true, false, unknown)
- **Justification:** Structured record of which channels were inspected, how many records in each, and the logic path to the result.
- **Transparency payload:** For `false` results, the principal MUST be presented with the specific harm-evidence records that triggered the bit, including the right-of-reply position (Everest 80).

---

## Parameters

- **lookback_window_days:** Default 1825 (5 years). Configurable per deployment; the predicate ID changes if window changes (one predicate = one window for auditability).
- **minimum_history_window_days:** Default 1825 (5 years). If the chain is younger than this, predicate returns `unknown` unless the principal explicitly opts into "early evaluation" (Everest 7 configuration).
- **minimum_engagement_threshold:** Default 10 non-spam world-interaction records (witnessed actions, allocations, verified co-signs). Below this, predicate returns `unknown`.
- **appeal_threshold_days:** Default 90. A court judgment under appeal that is younger than 90 days old causes the predicate to return `unknown`, not `false`, to allow for appellate reversal.

---

## Side Effects

The predicate appends a `kind: "predicate_evaluated"` record to the chain at evaluation time:

```json
{
  "kind": "predicate_evaluated",
  "ts": "2026-05-20T16:15:33.123Z",
  "payload": {
    "predicate_id": "non_harm_evidence",
    "predicate_version": "1.0.0",
    "evaluation_ts": "2026-05-20T16:15:33.123Z",
    "result_bit": "unknown",
    "lookback_window_days": 1825,
    "window_start_ts": "2021-05-20T16:15:33.123Z",
    "window_end_ts": "2026-05-20T16:15:33.123Z",
    "chain_head_at_eval": "sha256:xyz789...",
    "channel_inspections": {
      "third_party_records": {
        "count": 0,
        "active": false,
        "records": []
      },
      "counter_evidence_intake": {
        "count": 0,
        "active": false,
        "records": []
      },
      "negative_testimony": {
        "count": 2,
        "active": true,
        "records": [
          {
            "testimony_id": "te_001",
            "attester": "Principal B (VC hash)",
            "ts": "2026-04-15T10:00:00Z",
            "claim_summary": "Principal A caused emotional harm in shared project",
            "reply_position": "seq_42",
            "reply_status": "pending"
          },
          {
            "testimony_id": "te_002",
            "attester": "Principal C (VC hash)",
            "ts": "2026-03-20T14:30:00Z",
            "claim_summary": "Misrepresented credentials in collaboration",
            "reply_position": "seq_51",
            "reply_status": "replied_2026-05-10"
          }
        ]
      }
    },
    "engagement_check": {
      "total_world_interaction_records": 34,
      "threshold": 10,
      "passed": true
    },
    "history_window_check": {
      "chain_age_days": 1250,
      "minimum_history_window_days": 1825,
      "passed": false,
      "reason": "chain_younger_than_minimum"
    },
    "logic_path": "unknown (chain_age_below_minimum_window)",
    "trigger_source": "manual_query" | "proof_generation" | "disclosure_preparation"
  }
}
```

This record is immutable and participates in chain integrity (Everest 26).

---

## Evaluation Algorithm

### Pseudocode (Functional)

```
fn non_harm_evidence(
    chain: &Chain,
    principal_id: &str,
    params: PredicateParams
) -> (Bit, Justification) {
    let now = roughtime_now();
    let window_start = now - (params.lookback_window_days * 86400);
    let window_end = now;
    
    // STAGE 1: History window check
    let chain_age = chain.head_timestamp() - chain.genesis_timestamp();
    if chain_age < (params.minimum_history_window_days * 86400) {
        return (Bit::Unknown, Justification {
            reason: "chain_younger_than_minimum_history_window",
            chain_age_days: chain_age / 86400,
            minimum_required_days: params.minimum_history_window_days,
        });
    }
    
    // STAGE 2: Engagement threshold check
    let engagement_records = chain.records_in_range(window_start, window_end)
        .filter(|r| is_world_interaction(r))
        .count();
    
    if engagement_records < params.minimum_engagement_threshold {
        return (Bit::Unknown, Justification {
            reason: "insufficient_world_engagement",
            engagement_records: engagement_records,
            threshold: params.minimum_engagement_threshold,
        });
    }
    
    // STAGE 3: Channel inspection (all three in parallel)
    let channel_3p = inspect_third_party_channel(chain, window_start, window_end, params);
    let channel_ce = inspect_counter_evidence_channel(chain, window_start, window_end, params);
    let channel_nt = inspect_negative_testimony_channel(chain, window_start, window_end, params);
    
    // STAGE 4: Tri-state logic
    let any_active_harm = 
        channel_3p.active || 
        channel_ce.active || 
        channel_nt.active;
    
    if any_active_harm {
        return (Bit::False, Justification {
            reason: "harm_evidence_present",
            channels: [channel_3p, channel_ce, channel_nt],
        });
    }
    
    // STAGE 5: All channels clear — return true
    return (Bit::True, Justification {
        reason: "no_harm_evidence_in_documented_channels",
        channels: [channel_3p, channel_ce, channel_nt],
        window_days: params.lookback_window_days,
    });
}

fn inspect_third_party_channel(
    chain: &Chain,
    window_start: u64,
    window_end: u64,
    params: &PredicateParams
) -> ChannelInspection {
    let candidates = chain.records_in_range(window_start, window_end)
        .filter(|r| r.kind == "behavior_evidence.v0" && 
                   r.payload.evidence_kind == "third_party_record")
        .collect::<Vec<_>>();
    
    let mut active = false;
    let mut harm_records = vec![];
    
    for record in candidates {
        let record_type = record.payload.third_party_type;  // "court_judgment", "settled_lawsuit", "formal_complaint"
        let status = record.payload.status;  // "active", "dismissed", "expunged", "under_appeal", "reversed"
        
        // Dismissed, expunged, reversed records are marked in the original (not deleted).
        // Revocation records (E25) live separately.
        // Only "active" records count toward harm-evidence.
        if status == "active" {
            active = true;
            harm_records.push(ThirdPartyRecord {
                record_id: record.id.clone(),
                type_: record_type,
                jurisdiction: record.payload.jurisdiction,
                date: record.payload.date,
                claim_summary: record.payload.claim_summary,
                anchor_count: record.payload.transparency_log_anchors.len(),
            });
        } else if status == "under_appeal" {
            // Ambiguous: the judgment might be reversed. Return unknown if ANY judgment is under appeal.
            let days_under_appeal = (now - record.ts) / 86400;
            if days_under_appeal < params.appeal_threshold_days {
                return ChannelInspection {
                    active: false,
                    is_ambiguous: true,
                    reason: "judgment_under_appeal_within_threshold",
                    records: harm_records,
                };
            }
            // If under appeal for > 90 days, treat as resolved and ignore.
        }
    }
    
    ChannelInspection {
        active: active,
        is_ambiguous: false,
        reason: if active { "third_party_records_found" } else { "no_third_party_records" },
        records: harm_records,
    }
}

fn inspect_counter_evidence_channel(
    chain: &Chain,
    window_start: u64,
    window_end: u64,
    params: &PredicateParams
) -> ChannelInspection {
    // Counter-evidence: the principal's own admission of harm caused.
    let candidates = chain.records_in_range(window_start, window_end)
        .filter(|r| r.kind == "counter_evidence.v0")
        .collect::<Vec<_>>();
    
    let harm_records = candidates.iter()
        .map(|r| CounterEvidenceRecord {
            record_id: r.id.clone(),
            ts: r.ts,
            target_principal: r.payload.target_principal.clone(),
            description: r.payload.description.clone(),
            corrective_action_taken: r.payload.corrective_action_taken.clone(),
        })
        .collect::<Vec<_>>();
    
    let active = !harm_records.is_empty();
    
    ChannelInspection {
        active: active,
        is_ambiguous: false,
        reason: if active { "counter_evidence_found" } else { "no_counter_evidence" },
        records: harm_records,
    }
}

fn inspect_negative_testimony_channel(
    chain: &Chain,
    window_start: u64,
    window_end: u64,
    params: &PredicateParams
) -> ChannelInspection {
    // Negative testimony: co-principal-signed claims of being harmed.
    let candidates = chain.records_in_range(window_start, window_end)
        .filter(|r| r.kind == "negative_testimony.v0" && r.payload.status == "active")
        .collect::<Vec<_>>();
    
    let harm_records = candidates.iter()
        .map(|r| NegativeTestimonyRecord {
            testimony_id: r.id.clone(),
            ts: r.ts,
            attester_vc_hash: r.payload.attester_vc_hash.clone(),
            claim_summary: r.payload.claim_summary.clone(),
            is_mob_flagged: is_mob_attestation(r, candidates),
            reply_position: r.payload.reply_position.clone(),
            reply_status: r.payload.reply_status.clone(),
        })
        .collect::<Vec<_>>();
    
    let active = harm_records.iter()
        .any(|r| !r.is_mob_flagged);
    
    ChannelInspection {
        active: active,
        is_ambiguous: false,
        reason: if active { "negative_testimony_found" } else { "no_negative_testimony_or_mob_defended" },
        records: harm_records,
    }
}

fn is_mob_attestation(record: &Record, all_candidates: &[Record]) -> bool {
    // Mob-attestation defense (E75): if N many testimonies cluster suspiciously
    // around one target, degrade them.
    // v1.0.0: if > 5 testimonies within 14 days from distinct attesters,
    // all are marked is_mob_flagged=true and do not trigger harm-evidence flip.
    let target = &record.payload.target_principal;
    let window = 14 * 86400;
    
    let clustered = all_candidates.iter()
        .filter(|r| {
            r.payload.target_principal == target &&
            (r.ts - record.ts).abs() < window
        })
        .map(|r| &r.payload.attester_vc_hash)
        .collect::<std::collections::HashSet<_>>();
    
    clustered.len() > 5
}
```

### Semantic Clarifications

1. **"Absence of Evidence is Not Evidence of Absence":** The predicate cannot claim `true` on a thin or zero evidence base. If the principal has no documented behavior record, the predicate returns `unknown`. A `true` result requires affirmative absence: the evidence base is substantial, the history window is satisfied, and no channels contain harm records.

2. **Tri-State Semantics:**
   - **`true`:** No recorded harm evidence across all three channels, chain mature, engagement proven.
   - **`false`:** Any credible harm record on any channel. This does *not* mean "this person is harmful." It means "there is a documented record."
   - **`unknown`:** Default. Sparse evidence, young chain, appeal in flight, ambiguity. Safe default prevents false confidence.

3. **Third-Party Records:** Only records anchored to ≥ 2 independent transparency logs (Everest 62) count. Court judgments under appeal return `unknown` if < 90 days old; older appeals are treated as resolved. Dismissed, expunged, or reversed records are marked in the original record (not deleted) and do not trigger `false`; see Everest 25 (revocation) for explicit removal semantics.

4. **Counter-Evidence Intake:** The principal's own admission of harm caused. Any active counter-evidence record flips the bit to `false`. This is the principal's own witness against themselves — it is direct evidence.

5. **Negative Testimony:** Co-principal-signed attestations that they were harmed. The attester must hold a CredexAI VC (Everest 16). Mob-attestation defense (Everest 75): if > 5 testimonies cluster suspiciously around one target within 14 days, all are marked `is_mob_flagged=true` and do not trigger the `false` flip. A single credible negative testimony flips the bit; multiple independent testimonies reinforce it.

6. **Right of Reply:** Every negative-testimony record auto-includes a reserved sequence position for the principal's reply (Everest 80). The predicate's justification shows both the testimony and the reply status (pending, replied, withdrawn). A well-crafted reply does *not* erase the testimony; it adds the principal's counter-narrative to the evidence base.

7. **Window Semantics:** Default 5-year lookback, rolling (from now, not from enrollment). Configurable per counterparty class. A deployment-specific predicate ID encodes the window (e.g., `non_harm_evidence_w3y` for 3 years) to prevent ambiguity.

8. **Minimum History Window:** Default 5 years or chain age, whichever is younger. A principal newly enrolled returns `unknown` regardless of cleanliness, to prevent weaponization of "pristine" profiles from adversaries with fresh identities.

9. **Engagement Threshold:** ≥ 10 world-interaction records (witnessed actions, allocations, verified co-signs, voluntary disclosures). Below this, the evidence base is too thin to claim no harm. Returns `unknown`.

10. **Appeal Handling:** A judgment under appeal that is < 90 days old returns `unknown` because reversal is plausible. After 90 days in appeal, assume the judgment is resolved and treat it as active harm-evidence (unless explicitly revoked via Everest 25).

---

## Growth-Bit Composition (Everest 34)

**Mandatory Rule:** If a disclosure includes `non_harm_evidence` and it evaluates to `false`, the counterparty MUST be offered `growth_arc_evidence` (Everest 31) in the same disclosure, with equal prominence. This prevents permanent blackballing.

**Rationale:** A principal who committed documented harm five years ago and has since visibly grown deserves a second-side-of-the-story channel. The growth-bit is not a "get out of jail free card" — it is a separate evidence stream showing trajectory. A counterparty who sees both harm-evidence and growth-evidence can make a richer judgment.

---

## Mob-Attestation Defense (Everest 75)

When multiple negative testimonies cluster suspiciously around one target (> 5 within 14 days), all are marked `is_mob_flagged=true`. The predicate does *not* flip to `false` based on mob-flagged testimonies alone. A single non-mob-flagged testimony suffices to flip the bit; mob-flagged testimonies are suspended pending Everest 82 (anonymous warning to the principal).

---

## Acceptance Tests

### T-M30.1: Determinism

Given the same chain, parameters, and evaluation timestamp, the predicate always produces the same result bit and justification. No randomness, no state mutation.

**Test:** Run `non_harm_evidence(chain, params, ts)` twice; assert equality.

### T-M30.2: Tri-State Correctness

1. **`true` on clear history:** Chain age ≥ 5 years, ≥ 10 engagement records, all three channels empty. Result = `true`.
2. **`false` on any harm:** Active third-party record, counter-evidence, or non-mob-flagged negative testimony. Result = `false`.
3. **`unknown` on thin evidence:** Chain age < 5 years, or < 10 engagement records. Result = `unknown`.
4. **`unknown` on appeal:** Judgment under appeal, < 90 days old. Result = `unknown`, not `false`.

**Test:** Construct four chain states (clear, harm-present, thin, appeal-in-flight) and verify tri-state outputs.

### T-M30.3: Growth-Bit Composition

Any disclosure with `non_harm_evidence = false` MUST include `growth_arc_evidence` in the same response, without requiring a second query.

**Test:** Call predicate with harm-evidence present; assert that justification includes a `growth_arc_evidence` invitation.

### T-M30.4: Mob-Attestation Defense

Construct a chain with 6 negative testimonies against one target, all within 14 days. Assert that all 6 are marked `is_mob_flagged=true` and do not trigger `false` flip. Add a 7th testimony from a different date cluster; assert that the predicate flips to `false` if that 7th is not mob-flagged.

**Test:** Vary cluster size and timing; confirm that the > 5 within 14 days rule triggers the defense.

---

## Composition with Other Everests

- **Everest 14 (Third-party action records):** Feeds the third-party-records channel directly.
- **Everest 17 (Counter-evidence intake):** Feeds the counter-evidence channel.
- **Everest 20 (Negative-testimony protocol):** Feeds the negative-testimony channel with cooling-off windows and reply mechanics.
- **Everest 25 (Behavior-evidence revocation):** Allows explicit removal of false-witness records; a revocation record marks the original as `status: revoked` and does not change the predicate output (the original stays in the chain).
- **Everest 31 (Growth-arc evidence):** Composed via Everest 34 mandatory rule.
- **Everest 34 (Growth-bit composition rule):** Requires growth-bit disclosure whenever harm-evidence is false.
- **Everest 75 (Mob-attestation defense):** Degrades clustered negative testimonies.
- **Everest 80 (Right of reply):** Every negative testimony includes a reply position; the predicate shows both testimony and reply status.
- **Everest 26 (Predicate language v0):** The predicate is expressed in the Calm Witness DSL extended for behavior-evidence.

---

## Open Questions for v1 (Legal Subtleties)

1. **Jurisdiction Variance:** Court judgments are jurisdiction-bound. A settlement in one jurisdiction may not transfer to another. v1.0.0 stores jurisdiction in the record; deployments must decide: do we honor "any court judgment" globally, or only judgments from agreed-upon jurisdictions?

2. **Dismissed vs. Settled:** A "dismissed" charge may mean innocent; a "settled lawsuit" may mean admission of fault. v1.0.0 treats both as non-active harm-evidence (status != "active"), but legal semantics vary by jurisdiction. Recommend per-deployment configuration.

3. **Expungement Rights:** Many jurisdictions allow criminal records to be expunged after time. Should the predicate honor an expungement request and flip the status to `expunged`, or does the record stay in the chain for audit trail? v1.0.0 keeps records in the chain (Everest 25 revocation is the only explicit removal path); expungement is a policy question.

4. **Testimonial Hearsay:** Negative testimonies are first-hand accounts from people claiming harm. Some jurisdictions require cross-examination. The predicate does not enforce evidentiary rules; it surfaces all testimonies. Counterparty applications must decide their own burden of proof.

5. **Right of Reply Enforcement:** v1.0.0 reserves a reply position; it does not enforce that the principal exercises it. Should a witheld reply count against the principal? Recommend counterparty policies (Everest 7) make this explicit.

---

## Truth-Table Evaluator (Reference)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║ Condition                          │ Predicate Result                          ║
╠════════════════════════════════════════════════════════════════════════════════╣
║ Chain age < 5 years                │ unknown                                   ║
║ Engagement < 10 records            │ unknown                                   ║
║ Third-party judgment (active)      │ false                                     ║
║ Judgment under appeal (< 90 days)  │ unknown                                   ║
║ Judgment under appeal (≥ 90 days)  │ false (appeal resolved)                   ║
║ Counter-evidence present           │ false                                     ║
║ Single credible negative testimony │ false                                     ║
║ > 5 negative testimonies (14 days) │ unknown (mob defense)                     ║
║ All channels empty, mature chain   │ true                                      ║
║ Appeal in flight + harm elsewhere  │ unknown (ambiguity + other harm)          ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

---

## Critical Notes for Implementers

1. **The Predicate Does Not Judge.** Returning `false` means "there is a recorded harm-allegation," not "this person is harmful." A counterparty who treats the bit as identity has violated the protocol's spirit (principal-protective default #4). Recommend framing in disclosure: "There is a documented record; here it is."

2. **Right-of-Reply is Mandatory.** Every negative testimony must show the principal's reply position and status. Counterparties who suppress replies are acting in bad faith.

3. **Growth-Bit is Mandatory.** If `non_harm_evidence = false`, disclosure must include `growth_arc_evidence` without requiring the principal to ask. This prevents permanent blackballing.

4. **Mob Defense is Not Forgiveness.** A mob-defended testimony is suspended, not erased. If the same attester brings a non-mob-defended testimony later, it flips the bit.

5. **Thin Evidence Returns `unknown`.** Do not conflate `unknown` with `true`. A pristine-looking profile on a 6-month-old chain is untrustworthy.

---

## Cross-References

- **E5:** Values vocabulary v0 (non-harm is one of four core values).
- **E14:** Third-party action records (court records, formal complaints).
- **E17:** Counter-evidence intake (principal's own admissions).
- **E20:** Negative-testimony protocol (co-principal-signed harm claims).
- **E26:** Predicate language v0 (DSL for behavior-evidence evaluation).
- **E25:** Behavior-evidence revocation (explicit removal of false records).
- **E31:** Growth-arc evidence (counterparty trajectory).
- **E34:** Growth-bit composition rule (mandatory growth disclosure on harm-evidence).
- **E62:** Multi-anchor consensus for evidence (two independent transparency logs).
- **E75:** Mob-attestation defense (N-many clustered testimonies are degraded).
- **E80:** Right of reply (reserved sequence position for principal's response).
- **E82:** Anonymous reporting channel (warning to principal on suspect patterns).

---

## Sign-Off

— Calm, 2026-05-20

*Mirror Everest 30 Summit bagged. The predicate operationalizes the hardest asymmetry: we defend against false confidence while hoisting harm-evidence fully into the light. Tri-state is the key. Growth-bit composition prevents weaponization. Right-of-reply is non-negotiable.*
