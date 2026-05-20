# Everest 109 — Values from Action (Inference Layer)

*Phase IX — Values Vocabulary. Prereq: Everest 108.*

## Core Thesis

Principals self-report values (E108), but self-report is one signal among many. The chain contains a second, more direct signal: the history of their actions. This Everest defines an inference layer that derives per-dimension values scores from action records, and establishes a trust-but-verify predicate that surfaces gaps between stated and revealed values.

The design enforces three commitments:

1. **Auditable inference**: all scoring functions are open-source, content-addressed by hash, and deterministically reproducible byte-for-byte.
2. **Cryptographic binding**: each inferred score is committed in the chain via Pedersen commitment, so later verification is non-repudiable.
3. **Counterparty-driven queries**: a principal never reveals their absolute inferred score; instead, a counterparty can ask "does your inferred score match your self-report within threshold tau?" and receive a boolean, surfacing alignment without exposure.

---

## The Inference Algorithm Structure

For each dimension in V0_DIMENSIONS (Everest 107), define a scoring function:

```
f_dim: ChainWindow × Principal → score ∈ [0, 1]
```

Each function accepts a sliding window of chain records (filtered by principal, optionally by time range) and returns a normalized score. The function is:

- **Registered** in the CALM inference registry (E118 pattern)
- **Hashed** by SHA-256(function_code + dependencies + version) to produce a content address
- **Shipped as open-source Python** with reproducible outputs on test vectors
- **Subject to ethics review** (E115 Compass audit process) before deployment or substantive change

The scoring window defaults to 365 days backward from query time, but can be adjusted to exclude pre-reversal records (E112) or to focus on stress-test windows (E111).

---

## Per-Dimension Inference Rules

### 1. Cooperation

**Signal**: Evidence of joint action and collaborative commitment.

**Algorithm**:

```python
def f_cooperation(chain_window, principal, lookback_days=365):
    now = chain_window.query_time
    cutoff = now - timedelta(days=lookback_days)
    
    records = [r for r in chain_window if r.principal == principal 
               and r.timestamp >= cutoff]
    
    collaboration_records = [r for r in records 
                             if r.kind == 'action.collaboration']
    
    # Weight by recency: exponential decay, half-life 180 days
    weights = [exp(-ln(2) * (now - r.timestamp).days / 180) 
               for r in collaboration_records]
    
    if not collaboration_records:
        return 0.0
    
    return min(1.0, sum(weights) / 10.0)  # normalize to [0,1]
```

Increments per multi-party action record, weighted by recency (recent collaboration worth more). Floors at 0 if no collaboration detected; saturates at 1.

---

### 2. Fairness

**Signal**: Allocation of resources, opportunities, or attention across in-group vs. out-group counterparties.

**Algorithm**:

```python
def f_fairness(chain_window, principal, lookback_days=365):
    now = chain_window.query_time
    cutoff = now - timedelta(days=lookback_days)
    
    records = [r for r in chain_window if r.principal == principal 
               and r.timestamp >= cutoff]
    
    allocation_records = [r for r in records 
                          if r.kind == 'action.allocate' 
                          and 'resource_value' in r.metadata]
    
    in_group = sum(r.metadata['resource_value'] for r in allocation_records
                   if r.counterparty_group == principal.in_group)
    out_group = sum(r.metadata['resource_value'] for r in allocation_records
                    if r.counterparty_group != principal.in_group)
    
    total = in_group + out_group
    if total == 0:
        return 0.5  # neutral when no allocations
    
    out_group_ratio = out_group / total
    # Penalize extreme skew; reward 50-50 split
    return 1.0 - abs(out_group_ratio - 0.5)
```

Compares resource allocation across group boundaries. Score of 1.0 indicates balanced allocation; 0.0 indicates extreme in-group favoritism.

---

### 3. Honesty

**Signal**: Alignment between past declared intent and past observed outcomes.

**Algorithm**:

```python
def f_honesty(chain_window, principal, lookback_days=365):
    now = chain_window.query_time
    cutoff = now - timedelta(days=lookback_days)
    
    intent_records = [r for r in chain_window 
                      if r.principal == principal 
                      and r.kind == 'intent.declared'
                      and r.timestamp >= cutoff]
    
    matches = 0
    total = 0
    
    for intent_record in intent_records:
        intent_hash = intent_record.content_hash
        
        # Find subsequent outcome records referencing this intent
        outcome_records = [r for r in chain_window 
                           if r.kind == 'outcome'
                           and r.intent_hash == intent_hash
                           and r.timestamp > intent_record.timestamp
                           and r.timestamp <= intent_record.timestamp + timedelta(days=180)]
        
        if outcome_records:
            total += 1
            # Count as match if outcome aligns with declared intent
            if any(o.metadata.get('alignment_score', 0) >= 0.8 
                   for o in outcome_records):
                matches += 1
    
    if total == 0:
        return 0.5  # neutral if no intent-outcome pairs
    
    return matches / total
```

Tracks intent declarations (E122 records) and matches them against outcomes (E123 records). Score reflects the ratio of declared intents that resulted in aligned outcomes.

---

### 4. Non-Harm

**Signal**: Inverse of harm committed or alleged without rebuttal.

**Algorithm**:

```python
def f_non_harm(chain_window, principal, lookback_days=365):
    now = chain_window.query_time
    cutoff = now - timedelta(days=lookback_days)
    
    records = [r for r in chain_window if r.principal == principal 
               and r.timestamp >= cutoff]
    
    harm_records = [r for r in records 
                    if r.kind == 'harm.committed']
    
    harm_alleged_records = [r for r in records 
                            if r.kind == 'harm_alleged.raised']
    
    # For each allegation, check if there is a rebuttal or resolution
    unresolved_allegations = sum(
        1 for ha in harm_alleged_records
        if not any(r.kind == 'harm_alleged.rebutted' and r.prior_record_hash == ha.content_hash
                   for r in records)
    )
    
    total_harm_signals = len(harm_records) + len(harm_alleged_records)
    
    if total_harm_signals == 0:
        return 1.0
    
    return 1.0 - min(1.0, (len(harm_records) + unresolved_allegations) / 5.0)
```

Returns 1.0 if no harm records; decrements per confirmed harm or unresolved allegation. Saturates at 0 if harm events exceed threshold.

---

### 5. Cross-Difference Respect

**Signal**: Attestations from cross-group counterparties affirming respectful engagement.

**Algorithm**:

```python
def f_cross_difference_respect(chain_window, principal, lookback_days=365):
    now = chain_window.query_time
    cutoff = now - timedelta(days=lookback_days)
    
    records = [r for r in chain_window 
               if r.principal == principal 
               and r.timestamp >= cutoff]
    
    attestation_records = [r for r in records
                           if r.kind == 'attestation.respect'
                           and r.attester_group != principal.in_group]
    
    if not attestation_records:
        return 0.0
    
    # Weight attestations by attester credibility (recursively computed)
    weights = [compute_credibility(r.attester, chain_window) 
               for r in attestation_records]
    
    return min(1.0, sum(weights) / 3.0)
```

Counts positive attestations from out-group counterparties. Weighted by attester credibility (computed via recursive inference). High score indicates cross-group respect.

---

### 6. Generosity

**Signal**: Voluntary transfers, aid, or allocation of personal resources.

**Algorithm**:

```python
def f_generosity(chain_window, principal, lookback_days=365):
    now = chain_window.query_time
    cutoff = now - timedelta(days=lookback_days)
    
    records = [r for r in chain_window if r.principal == principal 
               and r.timestamp >= cutoff]
    
    giving_records = [r for r in records 
                      if r.kind == 'action.give'
                      and 'resource_value' in r.metadata]
    
    principal_capacity = compute_capacity(principal, chain_window)
    
    total_given = sum(r.metadata['resource_value'] for r in giving_records)
    
    if principal_capacity == 0:
        return 0.0
    
    giving_ratio = total_given / principal_capacity
    
    return min(1.0, giving_ratio)
```

Normalizes total giving by the principal's estimated capacity (derived from income, holdings). Score reflects fraction of capacity allocated to others.

---

### 7. Non-Tribal Engagement

**Signal**: Density of cross-tribe edges in the principal's engagement graph.

**Algorithm**:

```python
def f_non_tribal_engagement(chain_window, principal, lookback_days=365):
    now = chain_window.query_time
    cutoff = now - timedelta(days=lookback_days)
    
    records = [r for r in chain_window 
               if r.principal == principal 
               and r.timestamp >= cutoff
               and r.kind in ['action.collaborate', 'action.communicate', 
                              'action.allocate']]
    
    counterparties = set(r.counterparty for r in records)
    
    in_tribe = sum(1 for cp in counterparties 
                   if tribe(cp) == tribe(principal))
    out_tribe = sum(1 for cp in counterparties 
                    if tribe(cp) != tribe(principal))
    
    total_edges = in_tribe + out_tribe
    
    if total_edges == 0:
        return 0.0
    
    return out_tribe / total_edges
```

Computes the fraction of the principal's engagement graph that crosses tribal boundaries. Score of 1.0 indicates entirely out-tribe engagement; 0.0 entirely in-tribe.

---

### 8. Repair After Harm

**Signal**: Restitution, apology, or remedial action following harm events.

**Algorithm**:

```python
def f_repair_after_harm(chain_window, principal, lookback_days=365):
    now = chain_window.query_time
    cutoff = now - timedelta(days=lookback_days)
    
    records = [r for r in chain_window if r.principal == principal 
               and r.timestamp >= cutoff]
    
    harm_records = [r for r in records if r.kind == 'harm.committed']
    
    repair_records = [r for r in records
                      if r.kind in ['action.restitution', 'action.apology']
                      and any(r.prior_harm_hash == h.content_hash 
                              for h in harm_records)]
    
    if not harm_records:
        return 1.0
    
    repaired = len(set(r.prior_harm_hash for r in repair_records))
    
    return repaired / len(harm_records)
```

For each harm record, checks whether repair (restitution, apology) was subsequently enacted. Score is the ratio of harm events addressed via repair.

---

### 9. Consistency Under Stress

**Signal**: Behavioral variance across high-stakes records; low variance indicates high consistency.

**Algorithm**:

```python
def f_consistency_under_stress(chain_window, principal, lookback_days=365):
    now = chain_window.query_time
    cutoff = now - timedelta(days=lookback_days)
    
    records = [r for r in chain_window if r.principal == principal 
               and r.timestamp >= cutoff
               and r.metadata.get('stress_level', 0) > 0.7]
    
    if len(records) < 3:
        return 0.5  # insufficient signal
    
    # Extract principal's action vector per record
    # (e.g., cooperation_intent, harm_intent, fairness_choice)
    vectors = [extract_action_vector(r) for r in records]
    
    # Compute pairwise cosine similarity
    similarities = [cosine_similarity(vectors[i], vectors[j])
                    for i in range(len(vectors))
                    for j in range(i+1, len(vectors))]
    
    mean_similarity = mean(similarities) if similarities else 0.0
    
    return mean_similarity
```

Isolates high-stress records and computes consistency of action patterns across them. Score near 1.0 indicates stable behavior under pressure; near 0.0 indicates volatility.

---

### 10. Principal-Authored Other

**Signal**: Custom dimension, registered separately by the principal.

**Algorithm**:

```python
def f_principal_authored_other(chain_window, principal, lookback_days=365):
    # Retrieve the custom inference function from the registry
    custom_fn_hash = principal.metadata.get('custom_inference_hash')
    
    if not custom_fn_hash:
        return 0.5  # neutral default
    
    custom_fn = registry.lookup(custom_fn_hash)
    
    if not custom_fn:
        raise LookupError(f"Custom function {custom_fn_hash} not found")
    
    return custom_fn(chain_window, principal, lookback_days)
```

Allows each principal to register a custom dimension and its scoring function. The function is hashed and stored in the registry; inference delegates to it and cryptographically binds the result.

---

## Trust-But-Verify Composition

The predicate `self_report_matches_inferred_within_threshold(principal, dim, tau)` enables counterparty verification without value exposure:

```python
def self_report_matches_inferred_within_threshold(
    chain_window, principal, dim, tau):
    
    self_reported_score = lookup_self_report(chain_window, principal, dim)
    inferred_score = f_dim_registry[dim](chain_window, principal)
    
    gap = abs(self_reported_score - inferred_score)
    
    return gap < tau
```

A counterparty can ask: "Does Alice match her self-report on cooperation within 0.15?" and receive True/False. Neither value is revealed; only alignment is surfaced. This enables trust decisions ("I trust Alice on cooperation") without requiring exposure of her absolute score.

---

## Sources of Inference Error

**Sparse Chain**: Principals with few action records produce wide confidence intervals. The inference system flags these as Insufficient_Evidence and recommends longer observation windows.

**Values Reversal**: When a principal enacts a values reversal (E112), prior action records may not reflect their current values. The inference window must be adjusted to start post-reversal. This is captured in the E112 record itself.

**Witness Disagreement**: If independent witnesses (via E120-E121 attestations) disagree on the principal's behavior, the inference system flags the record as disputed and computes separate inferred scores for agreed vs. disputed subsets.

---

## Cryptographic Encoding

Each inferred score is committed to the chain via Pedersen commitment:

```
C_dim = g^score * h^randomness
```

The commitment is stored with the inference record. Later, a verifier can re-run the f_dim function on the same chain window and verify that the function output commits to the same value. This ensures the inference is auditable and non-repudiable.

---

## Open-Source Classifier Requirement

All inference functions are shipped as open-source Python in the CALM inference registry:

```
~/CredexAI/calm_witness/values_inference.py
```

Each function:

- Includes docstrings and test vectors
- Is reproducible byte-for-byte on the same input
- Is versioned and hashed for content addressing
- Undergoes ethics review before deployment (E115)

Updates trigger a re-run of all inferences for affected principals; the old scores are archived, the new scores are committed, and the hash of the updated function is recorded in the chain.

---

## Summary

Everest 109 establishes the inference layer: a deterministic, auditable system for deriving per-dimension values scores from chain action history. Combined with E108 self-reports, this enables trust-but-verify predicates that surface alignment gaps without exposing absolute values. The design enforces open-source code, cryptographic commitment, and ethics review, ensuring that inferences are reproducible, binding, and subject to community audit.

— Calm, 2026-05-20
