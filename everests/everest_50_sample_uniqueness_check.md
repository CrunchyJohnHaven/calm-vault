# Everest 50 — Sample Uniqueness Check

*Phase IV — Biometric Distance Machinery. Prereq: Everest 28, 49.*

## Threat

An attacker obtains a record of the operator's biometric sample from a prior session—either by capturing the raw stroke data, the embedding, or the committed sample record—and attempts to replay it as a fresh sample in a subsequent session. Liveness detection (Everest 49) prevents replay attacks at capture time from external sources; this everest prevents replay of already-captured samples *across sessions within the operator's own vault*.

The attack is subtle because the vault stores committed samples in the chain, and if an attacker can extract or reconstruct those samples and inject them at a later session, the biometric matcher may accept them as authentic. Worse, the attacker need not understand the vault's internal mechanics; they simply record "what worked before" and replay it.

## Defense Architecture

Every biometric sample committed to the chain is bound to a unique session context and labeled by a deterministic cryptographic hash that prevents silent re-use. The defense layers are:

1. **Per-sample uniqueness binding** via a content-addressed identifier (`sample_id`)
2. **Session-scoped freshness** via a per-session random nonce
3. **Historical index** to detect replay within a sliding window
4. **Kinematic sensitivity** so even minor modifications break the biometric match

Together, these make it cryptographically and operationally infeasible to replay a sample without detection.

## Mechanism

### Sample ID Computation

Each biometric capture is assigned a `sample_id` computed as:

```
sample_id = sha256(stroke_or_word_data || session_id || timestamp_ns || principal_master_pub)
```

This hash includes:
- **stroke_or_word_data**: The canonical serialization of the raw biometric events (keystroke timings, pen pressure, speech frames, etc.)
- **session_id**: A unique identifier for the current session
- **timestamp_ns**: Nanosecond timestamp of the capture, preventing duplicate captures at the exact instant
- **principal_master_pub**: The operator's public master key, binding the sample to the operator's identity

The `sample_id` is deterministic: the same operator, same stroke, same session, same timestamp always produces the same hash. Critically, *any* change to the input (different session, different nonce, different timestamp, or different stroke) produces a different `sample_id`.

### Chain Commitment

When a sample is accepted by the biometric matcher, a record is appended to the chain:

```
kind: "biometric.sample_committed"
payload:
  sample_id: <sha256 hash>
  distance_to_template: <Pedersen commitment (E44)>
  capture_modality: "hw" | "voice"
  session_id: <session identifier>
  freshness_nonce: <32-byte random bound to session>
```

The `distance_to_template` commitment cryptographically binds the acceptance decision to this specific sample, making cross-session reuse detectable (see below).

### Session Freshness Nonce

At the start of each session, the operator generates a 32-byte random `freshness_nonce`. This nonce is:
- Signed by the operator's `master.priv` key
- Included in every sample_id computation for that session
- Committed to the chain at session start

The nonce ensures that even if an attacker obtains the raw stroke data from session N, they cannot compute the same `sample_id` in session N+1 (the nonce is different). This provides defense-in-depth: the attacker must capture not just the stroke, but also the nonce, which is signed and session-specific.

### Sample ID Index

The vault maintains a content-addressed index at `~/.calm-vault/sample_ids.idx`:

```
sample_id_1 -> {timestamp, session_id, stroke_data_hash, modality}
sample_id_2 -> {timestamp, session_id, stroke_data_hash, modality}
...
```

More critically, the index also maps stroke data hashes to their first occurrence:

```
stroke_data_hash_1 -> [session_N, session_M, ...]  (history of sessions using this stroke)
stroke_data_hash_2 -> [session_K, ...]
```

This is the core anti-replay mechanism. On every new capture:

1. Compute `sample_id` with the current session's freshness_nonce
2. Compute `stroke_data_hash = sha256(canonical_stroke_serialization)`
3. Query the index: has this `stroke_data_hash` been seen before?
4. If found within the **sliding window** (default: last 30 days), **REJECT** the sample as a duplicate
5. Otherwise, append `biometric.sample_committed` to the chain and update the index

The sliding window is crucial: we don't forbid *all* reuse of a stroke indefinitely (a user might naturally make the same handwriting stroke repeatedly), but we forbid reuse *within a short time window*, catching active replay attacks while permitting legitimate recaptures.

### Distance Commitment Binding

Everest 44 introduces Pedersen commitments to the distance from the operator's biometric template. Each `biometric.sample_committed` record includes:

```
distance_to_template: Pedersen(distance, randomness)
```

This binding prevents "disguised replay": if an attacker replays a stroke and the biometric matcher computes a distance, that distance must match the commitment. If the stroke was genuinely replayed (identical input), the distance will be identical, and the commitment will match—but the sample_id index already rejected it. If the attacker modifies the stroke to evade the index, the distance shifts, the commitment mismatches, and the matcher rejects it.

### Rebuildability

The index is not a source of truth; it is a cache. Any process can rebuild `sample_ids.idx` by walking the chain:

```
index := {}
for record in chain:
  if record.kind == "biometric.sample_committed":
    stroke_hash := sha256(record.stroke_data)
    index[stroke_hash] := append(index[stroke_hash], record.session_id)
```

This property ensures the index cannot be the vector for attack (an attacker cannot corrupt the index without corrupting the chain, which is cryptographically auditable).

## Worked Attack Scenarios

### Scenario 1: Direct Replay

An attacker captures the raw `stroke_data` from session N. In session N+1, they replay the identical bytes.

- Liveness detection (E49) may pass if the attack is sophisticated (replaying recorded sensor events).
- The vault computes `stroke_data_hash` and queries the index.
- The hash matches an entry within the sliding window (session N was 3 days ago).
- The capture is **REJECTED**.

**Outcome**: Liveness provides the first line of defense; the sample index is the second line. Both must pass.

### Scenario 2: Minor Modification

The attacker modifies the stroke data by 1 byte (e.g., adding jitter to one pen pressure value) to evade the hash index.

- The modified stroke generates a different `stroke_data_hash`.
- The index lookup passes (no prior match).
- The biometric matcher evaluates the distance to template.
- The 1-byte change perturbs the kinematic features (timing, pressure curves, etc.), shifting the distance beyond the threshold τ.
- The `biometric_match_within(τ)` check **fails**.

**Outcome**: Layered defense. The index catches exact replays; the biometric matcher catches subtle tampering.

### Scenario 3: Captured Embedding

The attacker obtains the operator's embedding (the template-relative vector) from a prior session and tries to inject it directly.

- This attack fails because embeddings are not stored in the chain; only raw events and their commitment are.
- The embedding is recomputed at evaluation time from the fresh `stroke_data`.
- The attacker cannot inject a pre-computed embedding; they must provide the raw events that generate it.
- If they provide the same raw events, the stroke hash is detected (Scenario 1).
- If they provide modified raw events, the embedding differs and the matcher rejects it (Scenario 2).

**Outcome**: Embeddings are ephemeral; only raw events are persisted, and those are covered by the index.

### Scenario 4: Nonce Substitution

The attacker captures the stroke and nonce from session N (perhaps by extracting the `freshness_nonce` from the chain or a vault backup). In session N+1, they try to replay both.

- The vault compares the nonce against the current session's nonce.
- They do not match (the current session has a fresh random nonce).
- The capture is rejected due to nonce mismatch before it reaches the biometric matcher.

**Outcome**: The freshness_nonce mechanism provides defense-in-depth: even if raw data is captured, the session nonce changes every session.

## Index Retention and Garbage Collection

The index grows over time as samples accumulate. To prevent unbounded storage, retention is time-bounded:

- **Retention window**: 30 days (configurable per policy)
- **Policy**: Stroke data hashes older than 30 days are removed from the active index
- **Chain records**: `biometric.sample_committed` records remain in the chain indefinitely for audit trails

The 30-day window is chosen based on the operational threat model: replay of a sample captured 30+ days ago is considered low-risk because the operator's biometric template evolves over time, environmental conditions change, and the attack window is narrow.

**Index footprint**: Each sample consumes ~30 bytes (hash + metadata). At ~100 samples/month over 30 days, the index is <40KB/year. Storage is trivial; the bottleneck is policy, not capacity.

## Performance Characteristics

- **Index lookup**: <1ms per check (hash table in-memory)
- **Index update**: O(1) append
- **Chain append**: Consistent with other chain operations (E28)
- **Rebuild cost**: O(N) where N is the number of `biometric.sample_committed` records in the last 30 days (~100 records/month)

The index is kept in-process or backed by a fast KV store (e.g., RocksDB) and does not block sample evaluation.

## Integration Points

This everest depends on:
- **Everest 28 (Chain Verifier)**: The chain is the source of truth for all committed samples and their metadata.
- **Everest 49 (Liveness Detection)**: Prevents replay at capture time; this everest prevents replay across sessions.
- **Everest 44 (Distance Commitment)**: Binds acceptance decisions to specific samples, enabling tamper detection.

This everest feeds forward to:
- **Everest 36, 37** (Distance Thresholding): The index ensures only fresh samples reach the distance checker.
- **Everest 45** (Multimodal Binding): When multiple modalities are used, each modality's sample_id is independently indexed and checked.
- **Everest 58** (Vault Integrity): The sample index can be rebuilt from the chain, enabling integrity verification of the index itself.

## Summary

Sample Uniqueness Check is the session-level replay defense. By binding each sample to a cryptographic hash that includes the session context, maintaining a sliding-window index of historical hashes, and leveraging the chain as an immutable audit trail, the vault prevents re-use of biometric samples within a short operational window while remaining computationally efficient and fully auditable.

The defense is layered: the freshness_nonce provides defense-in-depth against nonce substitution, the index catches exact replays, the biometric matcher rejects tampered samples, and the distance commitment makes all acceptance decisions cryptographically binding. No single layer is a silver bullet; the combination is resilient.

— Calm, 2026-05-20
