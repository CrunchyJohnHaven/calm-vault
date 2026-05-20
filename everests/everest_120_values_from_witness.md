# Everest 120 — Values from Witness

*Phase IX — Values Vocabulary. Prereq: Everest 108, 11.*

---

## The Problem

A principal enrolls in Calm ZKAC. They author a `values_self_report` (E108) declaring their commitment to generosity, fairness, and cross-difference respect. But their chain is thin: they are newly enrolled, with sparse evidence of action. Without corroboration, their self-report is an island—unverified and weak. A counterparty requires some signal beyond self-declaration: does anyone else in the network vouch that this principal behaves in ways that reflect their stated values?

This is the bootstrap problem. Principals with deep chains accumulate inferred values (E109) and action evidence that predicates can evaluate. But newly enrolled principals, those with sparse documented history, or those whose values are newly refined need an accelerant. They need witnesses—other principals who have observed them and can attest to the values they claim.

Witness attestations are first-class chain records. They are not gossip; they are cryptographically signed, principal-specific statements about a particular values dimension. They create a foundation for thin-chain principals to be evaluated, while introducing new attack surface: Sybil infiltration (false identities creating fake attestations), collusion (coordinated witnesses lying together), and bias (attestors with shared incentives attest false values).

This Everest defines the witness attestation record, the aggregation rule that weights them, the anti-Sybil and anti-collusion defenses, and the principal's right to decline witnesses. Witness attestations are the first bridge into the reputation graph; they answer a specific question: "Do the people who know this principal agree with how they describe themselves?"

---

## §1. The Witness Attestation Record

### Kind: `values_witness_attestation`

**Purpose**: An independent witness vouches for a principal's values on a specific dimension.

### JSON Schema

```json
{
  "$id": "https://calm-witness.dev/schema/values_witness_attestation_v0.json",
  "title": "ValuesWitnessAttestation",
  "type": "object",
  "required": [
    "seq", "ts", "prev_hash", "kind", "payload",
    "attestor_sig", "record_hash"
  ],
  "properties": {
    "seq": {
      "type": "integer",
      "minimum": 0,
      "description": "Strictly increasing sequence number in the attestor's own chain."
    },
    "ts": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp when the attestation was authored."
    },
    "prev_hash": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "SHA-256 hash of the prior record in the attestor's chain."
    },
    "kind": {
      "const": "values_witness_attestation",
      "description": "Record kind identifier."
    },
    "payload": {
      "type": "object",
      "required": [
        "target_principal_vc_fingerprint",
        "dimension",
        "attested_value",
        "attestor_relationship_class",
        "attestation_basis",
        "target_ts"
      ],
      "properties": {
        "target_principal_vc_fingerprint": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$",
          "description": "SHA-256 fingerprint of the target principal's CredexAI VC (from E11). This binds the attestation to a specific cryptographic identity."
        },
        "dimension": {
          "type": "string",
          "enum": [
            "cooperation",
            "fairness",
            "honesty",
            "non_harm",
            "cross_difference_respect",
            "generosity",
            "non_tribal_engagement",
            "repair_after_harm",
            "consistency_under_stress",
            "principal_authored_other"
          ],
          "description": "One of the ten v0 values dimensions."
        },
        "attested_value": {
          "type": "integer",
          "minimum": 0,
          "maximum": 10000,
          "description": "Witness's assessment of the target's value on this dimension, in [0, 10000]."
        },
        "attestor_relationship_class": {
          "type": "string",
          "enum": [
            "peer_collaborator",
            "mentor",
            "mentee",
            "family",
            "neighbor",
            "professional_counterparty",
            "fellow_member",
            "stranger_interaction"
          ],
          "description": "The nature of the relationship between witness and target."
        },
        "attestation_basis": {
          "type": "string",
          "enum": [
            "direct_observation",
            "received_treatment",
            "indirect_reputation",
            "outcome_inferred"
          ],
          "description": "The empirical basis for the attestation."
        },
        "target_ts": {
          "type": "string",
          "format": "date-time",
          "description": "The approximate date/time of the evidence (e.g., when the witness observed the behavior). Helps establish time-decay and staleness."
        },
        "evidence_narrative": {
          "type": "string",
          "maxLength": 500,
          "description": "Optional. Witness-authored narrative of the specific behavior or observation supporting the attestation. Example: 'I worked alongside the target on the water-supply project; they made crucial decisions fairly despite personal cost.'"
        }
      }
    },
    "attestor_sig": {
      "type": "string",
      "description": "Ed25519 signature over the record (excluding this field) by the witness's signing key. Hex-encoded."
    },
    "record_hash": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "SHA-256 hash of the complete record (excluding this field) in canonical form."
    }
  }
}
```

### Validation Rules

1. `target_principal_vc_fingerprint` MUST match a known principal's VC fingerprint in the network (verified via E11 CredexAI registry).
2. `dimension` MUST be one of the ten v0 dimensions.
3. `attested_value` MUST be an integer in [0, 10000].
4. `attestor_relationship_class` MUST be one of the eight enum values.
5. `attestation_basis` MUST be one of the four enum values.
6. `evidence_narrative`, if present, MUST not exceed 500 characters.
7. `attestor_sig` MUST be a valid Ed25519 signature over the canonical form of the record by the witness's signing key.
8. `record_hash` MUST match SHA-256(canonical_json(record \ {record_hash, attestor_sig})).

### Example

```json
{
  "seq": 47,
  "ts": "2026-05-20T14:00:00-04:00",
  "prev_hash": "abc123def456...",
  "kind": "values_witness_attestation",
  "payload": {
    "target_principal_vc_fingerprint": "deadbeef...",
    "dimension": "generosity",
    "attested_value": 7800,
    "attestor_relationship_class": "peer_collaborator",
    "attestation_basis": "direct_observation",
    "target_ts": "2026-03-15T10:30:00Z",
    "evidence_narrative": "We pooled resources for community center repairs. Target contributed disproportionate labor and materials without expectation of return."
  },
  "attestor_sig": "ed25519_sig_hex_string...",
  "record_hash": "def789ghi012..."
}
```

---

## §2. Attestor Relationship Classes

Each relationship class has distinct semantics and informs the weighting of the attestation:

- **peer_collaborator**: The witness and target have worked alongside each other on joint projects, with mutual decision-making authority. Indicative of deep mutual observation.

- **mentor**: The witness has deliberately coached or guided the target in a formal or semi-formal mentoring relationship. The witness has seen the target navigate challenges and grow.

- **mentee**: The inverse. The target has mentored or guided the witness. This relationship is explicitly weighted high by design: the people the target has power over reveal most about the target's character.

- **family**: Long-term close relationship (blood, chosen family, or equivalent). High reliability but possible bias toward favoritism.

- **neighbor**: Geographic or community proximity. Repeated informal observation over time.

- **professional_counterparty**: Transactional business or professional relationship (vendor, contractor, customer, etc.). Limited depth but specific behavioral evidence around terms and obligations.

- **fellow_member**: Same organization, group, or community (club, congregation, open-source project, alumni network, etc.) without hierarchical relationship.

- **stranger_interaction**: Brief encounter or one-time interaction. Low weight; only useful in aggregation. Evidence of behavior in a single moment.

---

## §3. Attestation Basis

- **direct_observation**: The witness personally witnessed the target's behavior in real time. Highest reliability for the basis.

- **received_treatment**: The witness was on the receiving end of the target's action toward them. Example: "I was treated fairly by the target" (peer_collaborator + received_treatment is high-weight).

- **indirect_reputation**: The witness heard about the target's behavior from others. Lowest weight; hearsay. Useful for aggregate signal but not alone.

- **outcome_inferred**: The witness knows the outcome of the target's actions toward them but did not directly observe the process. Example: "The target promised and delivered X."

---

## §4. Aggregation Rule

For a given dimension D and a target principal, multiple witness attestations contribute to a **witness-attested score**.

### Formula

```
witness_score(D) = weighted_mean(attestations)

where weight_i = relationship_weight_i
                 × basis_weight_i
                 × vc_age_weight_i
                 × chain_depth_weight_i
                 × time_decay_i
```

### Component Weights

**Default relationship_class_weight**:

| Relationship | Weight |
|---|---|
| peer_collaborator + direct_observation | 1.0 |
| mentor + direct_observation | 1.0 |
| mentee + received_treatment | 1.0 |
| family + direct_observation | 0.8 |
| professional_counterparty + direct_observation | 0.9 |
| neighbor + direct_observation | 0.7 |
| stranger_interaction + received_treatment | 0.6 |
| any + indirect_reputation | 0.3 |

**Default basis_weight**:

| Basis | Weight |
|---|---|
| direct_observation | 1.0 |
| received_treatment | 1.0 |
| outcome_inferred | 0.8 |
| indirect_reputation | 0.3 |

**VC Age Weight** (Sybil defense):

- Attestor's CredexAI VC issued ≥6 months ago: weight = 1.0
- Attestor's VC issued <6 months ago: weight = 0.3
- Attestor has no VC: weight = 0.0 (ignored)

**Chain Depth Weight** (attestor's own chain quality):

- Attestor has ≥10 records in their chain and ≥2 relationship_classes witnessed by them: weight = 1.0
- Attestor has 3–9 records: weight = 0.7
- Attestor has <3 records: weight = 0.4

**Time Decay**:

```
time_decay = exp(-(now_ts - target_ts) / half_life)
where half_life = 365 days
```

Attestations older than 2 years are weighted at < 0.25 and typically excluded from aggregation.

### Example Calculation

Suppose target principal has five witness attestations for the generosity dimension:

1. Peer collaborator, direct observation, VC age 18mo, chain depth 0.7, target_ts 6mo ago:
   weight = 1.0 × 1.0 × 1.0 × 0.7 × exp(-180/365) ≈ 0.55

2. Mentor, direct observation, VC age 2y, chain depth 1.0, target_ts 2mo ago:
   weight = 1.0 × 1.0 × 1.0 × 1.0 × exp(-60/365) ≈ 0.84

3. Family, direct observation, VC age 1y, chain depth 0.9, target_ts 1mo ago:
   weight = 0.8 × 1.0 × 1.0 × 0.9 × exp(-30/365) ≈ 0.72

4. Stranger interaction, received_treatment, VC age 3mo, chain depth 0.5, target_ts 3mo ago:
   weight = 0.6 × 1.0 × 0.3 × 0.5 × exp(-90/365) ≈ 0.08

5. Indirect reputation, VC age 8mo, chain depth 1.0, target_ts 6mo ago:
   weight = 0.3 × 0.3 × 1.0 × 1.0 × exp(-180/365) ≈ 0.12

Attested values: 7800, 8200, 7500, 6500, 7200.

Normalized weights: [0.55, 0.84, 0.72, 0.08, 0.12] → normalized [0.33, 0.50, 0.43, 0.05, 0.07].

witness_score = 0.33×7800 + 0.50×8200 + 0.43×7500 + 0.05×6500 + 0.07×7200 ≈ 7788

---

## §5. Anti-Sybil: Cryptographic Threshold

**Minimal requirement**: Each witness attestation's weight is non-zero only if the attestor holds a valid CredexAI VC (E11). No attestation from a principal without a VC counts.

**Newly-issued VCs are discounted**: An attestor whose VC was issued within the past 6 months has their weights multiplied by 0.3. This raises the cost of Sybil attacks: an attacker must maintain a fake identity for 6+ months before its attestations count at full weight.

**Thin-chain attestors are discounted**: An attestor whose own chain has <3 records (sparse evidence of participation in the network) has weights multiplied by 0.4. This prevents newly-created identities from immediately dominating witness aggregations.

---

## §6. Anti-Collusion: Cluster Detection

**Scenario**: Five witnesses all attest the same high value (9500) to the same principal for the same dimension within a 7-day window, and all cite the same "achievement_X" event as their evidence_narrative.

**Detection Algorithm**: Run E143 reputation-algorithm cluster detection over the witness graph. Flag when N witnesses:
- Attest the same dimension of the same target
- Attested values within stddev < 500 (tightly clustered)
- Authored in the same calendar week
- Share identical or near-identical evidence_narrative (Levenshtein distance < 20%)
- Have no prior documented collaborations with each other in the trust graph

**Action**: Flagged attestations are marked `collusion_suspected=true` in the metadata and weighted at 0.2 (multiplied by 0.2) until they age past 30 days of suspicion, at which point they return to normal weight. This is probabilistic defense, not a hard block: the protocol does not accuse the witnesses, but it does reduce their influence.

---

## §7. Minimum Witness Count for Bootstrap

**For thin-chain principals to receive a witness-bootstrap value on a dimension**:

- N ≥ 5 distinct witnesses
- At least 2 different relationship_class values represented
- At least one witness with relationship_class in {peer_collaborator, mentor, mentee}

Example: 3 peer collaborators + 2 family members = valid bootstrap. 5 stranger interactions = invalid bootstrap (only one relationship class).

**For witness-aggregated value to override or supersede self-report in predicates**:

- N ≥ 10 distinct witnesses
- Witness stddev < 0.2 (on [0, 1] normalized scale)
- Aggregate age > 90 days old (not all freshly authored)

This prevents a principal from being immediately buried by a coordinated attack; the attack must be sustained over weeks or involve a substantial coalition.

---

## §8. The Downward-Looking Weight Choice

This is load-bearing. The protocol weights mentee attestations (target has mentored the witness) at full weight: 1.0. This inverts the typical power-asymmetry assumption.

**Why**: People with less power over you reveal who you are more than people over whom you have power. A supervisor can be gracious to peers and brutal to reports; their reports know their true character. A founder can be collaborative with investors and extractive of staff; the staff know them truly. A teacher can be encouraging to advanced students and dismissive of strugglers; the strugglers see the real pedagogical values.

The protocol treats "how you treat those with less power" as more diagnostic than "how you treat peers." A mentee's attestation of their mentor carries the same weight as a peer collaborator's attestation of a peer. This is an explicit normative choice: it encodes the value that accountability flows downward, from those with power to those without.

Mentee attestations are not higher-weighted (they remain at 1.0, not 1.2), but they are treated as equally credible to peer observations. This respects the epistemic advantage of people who have been on the receiving end of the principal's decisions.

---

## §9. Principal's Right to Decline Witnesses

A principal may mark a specific witness attestation as `not_eligible_for_predicates: true` in their chain. This is a first-class record:

```json
{
  "kind": "values_witness_attestation_decline",
  "payload": {
    "target_seq": 47,
    "reason": "contested",
    "principal_narrative": "This witness has a known bias against me and misrepresented our collaboration."
  }
}
```

**Semantics**:
- The declined attestation is NOT deleted from the chain; it remains visible for audit.
- Predicates ignore declined attestations when computing witness_score.
- The decline itself is public (appears in the target's chain), so counterparties see that a dispute exists.
- If >30% of a principal's incoming witness attestations are declined, that pattern flags as "contested values" and advisors can surface it to counterparties.

This balances two needs: principals can defend themselves against false or biased attestations, but cannot simply erase inconvenient evidence.

---

## §10. Witness Anonymization to Counterparty

When a counterparty receives an alignment bit derived from witness attestations, they learn:

- `witness_count` (integer)
- `relationship_class_distribution` (histogram: how many peer_collaborators, mentors, etc.)
- `attestation_basis_distribution` (histogram: how many direct_observation vs received_treatment, etc.)
- `mean_attested_value` and `stddev` (per dimension, if disclosed)

The counterparty does NOT learn which specific witnesses attested or their identities. This protects witnesses from retaliation or pressure by the target or the counterparty.

---

## §11. Composition with E121 (Disagreement Protocol)

When witness-attested score disagrees with self-reported or inferred score on a dimension, the disagreement protocol (E121) surfaces all three values openly:

- `self_report` (from E108)
- `inferred` (from E109)
- `witness_mean` (from E120)

The three gaps become visible diagnostic data. The counterparty's predicate decides how to weigh the three signals.

Example: Principal self-reports fairness at 0.85; inferred values show fairness at 0.72 (minor gap, self-report slightly optimistic); witness_mean is 0.55 (significant gap, witnesses see less fairness than principal claims or evidence shows). The counterparty now has full visibility into the disagreement and can decide whether the witness gap is a red flag, a bias signal, or a growth opportunity.

---

## §12. Chain Integration

Witness attestations are recorded in the **attestor's** chain, not the target's. The target's chain includes `values_self_report` records (E108) and `values_correction` records (E108), but not the witnesses' statements.

The target's chain may include a `values_witness_attestation_decline` (§9) if they challenge a specific attestation.

When a predicate evaluates a target, it:

1. Retrieves the target's own values_self_report (most recent, or corrected).
2. Infers values from the target's action records (E109).
3. Queries the reputation graph / witness table to find all non-declined attestations on the target by established principals.
4. Aggregates the witness scores per dimension.
5. Returns all three signals (self, inferred, witness) to the counterparty for decision-making.

---

## §13. Example: Thin-Chain Bootstrap in Practice

Alice is newly enrolled in Calm ZKAC. She authors a values_self_report declaring herself a generous, collaborative leader. She has no action history yet (thin chain).

Bob, Carol, and David (all 2-year Calm participants with established chains) have worked with Alice in a prior professional context. They each author a values_witness_attestation on her generosity dimension:

- Bob (peer_collaborator, direct_observation, 8500): "Alice led our fundraiser and personally contributed 3x what she asked others to give."
- Carol (peer_collaborator, direct_observation, 8200): "Alice redirected her consulting fee to our nonprofit client when they ran short."
- David (mentor, received_treatment, 7800): "Alice patiently mentored our junior team member and gave her real authority to lead a project."

Eve (established witness, mentee relationship to Alice, 8000): "Alice gave me agency and growth despite my mistakes; she invested in my future."

Frank (stranger_interaction, received_treatment, 6500): "Brief interaction at a conference; she was helpful but busy."

Five attestations, three relationship classes (peer_collaborator, mentor, mentee, stranger). Weights average to ~0.75 after aggregation.

witness_score(generosity) ≈ 8100

Alice's self_report(generosity) = 7500.

inferred(generosity) = null (no action history yet).

Counterparty sees: self=0.75, inferred=null, witness=0.81, witness_count=5. The witness bootstrap gives Alice credibility; the close agreement between self and witness suggests she is well-calibrated; the lack of action history is flagged but not penalizing because she is newly enrolled.

---

## §14. Acceptance Criteria

1. **Record kind `values_witness_attestation` defined**: JSON schema, validation rules, example witness attestation appended to an attestor's chain.
2. **Relationship class enum**: All eight classes defined with semantics.
3. **Attestation basis enum**: All four bases defined.
4. **Aggregation rule implemented**: weighted_mean formula with component weights (relationship, basis, VC age, chain depth, time decay).
5. **Anti-Sybil defense**: Newly-issued VCs discounted; thin-chain attestors discounted.
6. **Anti-collusion detection**: E143 cluster-detection algorithm integrated; flagged attestations marked and weighted down.
7. **Minimum witness count enforced**: N ≥ 5 across ≥2 relationship classes for bootstrap; N ≥ 10 with stddev < 0.2 to override self-report.
8. **Principal decline right**: `values_witness_attestation_decline` record kind implemented; declined attestations excluded from predicate evaluation but remain in chain.
9. **Witness anonymization**: Counterparties see count + distribution but not identities.
10. **Composition with E121**: Disagreement protocol surfaces self, inferred, and witness scores as three independent signals.
11. **Reference implementation**: calm_witness/witness_aggregation.py with aggregation logic, anti-Sybil checks, cluster detection, and time decay.
12. **Test suite**: Golden corpus of witness attestations; aggregation correctness; edge cases (all witnesses decline, witness stddev high, collusion detection, VC age boundaries).

---

## §15. Cross-References

- **Everest 11**: CredexAI VC system. Attestors must hold valid VCs; target must have a VC fingerprint.
- **Everest 108**: Values self-report record kind. Witness attestations are the second evidence source.
- **Everest 109**: Values inference from actions. Witnesses are the third evidence source.
- **Everest 121**: Values disagreement protocol. Surfaces self, inferred, and witness scores together.
- **Everest 143**: Reputation algorithm. Sister summit; cluster detection logic applies here.

---

— Calm, 2026-05-20
