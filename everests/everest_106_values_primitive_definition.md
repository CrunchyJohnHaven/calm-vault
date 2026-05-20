# Everest 106 — Values Primitive Definition

*Phase IX — Values Vocabulary. Prereq: Everest 1, 51.*

---

## What a Value Is (In This Protocol)

A value in Calm ZKAC is a **principal-authored, normative commitment about how to act toward others**. It is:

1. **Predicate-evaluatable**: We can write a zero-knowledge circuit that returns True / False / Insufficient_Evidence over a chain of evidence (actions, statements, attestations).
2. **Scalar**: Continuous, not categorical, represented as a fixed-point integer in [0, 10000] (isomorphic to [0, 1]). This preserves uncertainty and allows comparison: "more cooperative than" without binarizing.
3. **Bound to a fixed dimension set**: The v0 vocabulary defined in Everest 107. No ad-hoc dimensions.
4. **Time-stamped to a chain state**: Every ValuesVector binds to a principal's chain head (a hash), making it auditable and preventing retroactive rewrites.

Values are **not**:

- **Personality traits** ("I am introverted"). Traits describe inherent dispositions; values prescribe action norms.
- **Preferences** ("I like chocolate"). Preferences are about consumption; values are about conduct toward others. (See Everest 110 for the preference boundary.)
- **Identity claims** ("I am X"). Identity is self-report; values are behavioral commitments. (See Everest 116 for identity semantics.)
- **Clinical / religious / political assessments**. We do not diagnose, spiritually rank, or ideologically categorize principals.
- **Predictive claims about future behavior**. A principal might commit to a value and fail to uphold it. The commitment is truthful; prediction is separate (see Everest 109).

---

## The Type: ValuesVector

A `ValuesVector` is a fixed-length tuple of scalar attributes across the v0 dimension set. Here is the canonical Python dataclass:

```python
from dataclasses import dataclass
from typing import Dict, FrozenSet

@dataclass(frozen=True)
class ValuesVector:
    """A principal's values across the v0 dimension set.
    
    Each value is a fixed-point integer in [0, 10000] representing
    a scalar in [0, 1]. The vector binds to the principal's current
    chain state via chain_head, making it auditable and immutable
    once committed.
    """
    dimensions: Dict[str, int]  # dimension_name -> 0..10000
    version: str = "v0"
    chain_head: bytes = b""  # binds to principal's chain state
    
    def __post_init__(self):
        """Enforce invariants."""
        if self.version != "v0":
            raise ValueError(f"Only version 'v0' is supported; got {self.version}")
        
        for dim, val in self.dimensions.items():
            if not (0 <= val <= 10000):
                raise ValueError(
                    f"Dimension {dim} value {val} out of range [0, 10000]"
                )
        
        # Validate dimension names match the v0 vocabulary from E107
        if set(self.dimensions.keys()) != get_v0_dimensions():
            raise ValueError(
                f"Dimension set mismatch. Expected {get_v0_dimensions()}; "
                f"got {set(self.dimensions.keys())}"
            )
    
    def to_commitment(self) -> 'ValuesCommitment':
        """Return Pedersen commitments for this vector (see commit_values)."""
        return commit_values(self)
```

### Invariants

- **frozen=True**: The dataclass is immutable. Once constructed, it cannot be modified. This prevents accidental mutation during serialization, hashing, or circuit evaluation.
- **version required**: Always "v0". Future versions (v1, v2) will have different dimension sets and commitment schemes. Explicit versioning prevents silent incompatibilities.
- **chain_head binding**: A non-empty chain_head (e.g., SHA-256 hash of the principal's prior chain record) ties the commitment to a specific moment in the principal's audit trail. This prevents a principal from claiming the same values at multiple points in history as if they were the same commitment.

---

## The Commitment Function: commit_values()

```python
from typing import NamedTuple
import hashlib

class ValuesCommitment(NamedTuple):
    """Result of committing a ValuesVector."""
    per_dimension: Dict[str, bytes]  # dim -> Ristretto255 point (compressed)
    aggregate: bytes                  # single Ristretto255 point
    vector_hash: bytes                # SHA-256(ValuesVector)

def commit_values(vec: ValuesVector) -> ValuesCommitment:
    """
    Commit a ValuesVector using Pedersen commitments.
    
    - For each dimension d in vec.dimensions:
      - Commitment[d] = g_d * (vec[d] / 10000) + h * r_d
      where g_d is the Ristretto255 generator for dimension d,
      h is the blinding generator, and r_d is a random scalar in [0, 2^255).
    
    - Aggregate commitment = sum of all per-dimension commitments
      (optional; used for privacy-class filtering in E113).
    
    - vector_hash = SHA-256(serialize(vec))
      (binds the commitment to the exact vector; prevents tampering).
    
    Returns: ValuesCommitment with per-dimension and aggregate points.
    
    Uses Ristretto255 generators defined in Everest 44.
    """
    from ristretto255 import RistrettoPoint, Scalar  # external crate
    
    generators = get_ristretto_generators()  # from E44
    
    per_dimension = {}
    aggregate = RistrettoPoint.identity()
    
    for dim, val_int in vec.dimensions.items():
        # val_int in [0, 10000]; scale to [0, 1] for blinding
        val_scalar = Scalar(val_int / 10000.0)
        
        # Pedersen: C_d = g_d * val + h * r
        g_d = generators[dim]
        h = generators["blinding_base"]
        r_d = Scalar.random()  # random blinding
        
        commitment_d = g_d.multiply(val_scalar).add(h.multiply(r_d))
        per_dimension[dim] = commitment_d.compress()
        aggregate = aggregate.add(commitment_d)
    
    vector_hash = hashlib.sha256(serialize(vec)).digest()
    
    return ValuesCommitment(
        per_dimension=per_dimension,
        aggregate=aggregate.compress(),
        vector_hash=vector_hash,
    )
```

**Why Pedersen commitments?**

- Additively homomorphic: We can combine commitments from multiple actions (E109) to derive inferred values.
- Zero-knowledge proof friendly: ZK circuits can reason about commitments without revealing exact scalar values (E113 privacy classes).
- Binding and hiding: The commitment is cryptographically bound to the vector; the blinding ensures the principal's values remain hidden until disclosure.

---

## Golden-Input / Output Corpus

### Example Profiles

**Profile A: Highly Transparent, Moderately Honest**

```python
alice = ValuesVector(
    dimensions={
        "transparency": 9200,  # commits to radical openness
        "honesty": 7400,       # medium-high truth-telling
        "consent": 8900,       # respects others' autonomy
        "reliability": 8100,   # mostly keeps commitments
        "humility": 6200,      # moderate self-awareness
    },
    version="v0",
    chain_head=bytes.fromhex("a1b2c3d4..."),
)
commitment_a = commit_values(alice)
# aggregate hash: d4e5f6a7...
```

**Profile B: Cautious, Deliberate**

```python
bob = ValuesVector(
    dimensions={
        "transparency": 4100,
        "honesty": 9500,       # high truth-telling
        "consent": 9800,       # strict autonomy respect
        "reliability": 9200,
        "humility": 8100,      # strong self-awareness
    },
    version="v0",
    chain_head=bytes.fromhex("b2c3d4e5..."),
)
commitment_b = commit_values(bob)
```

**Profile C: Minimal Commitment**

```python
charlie = ValuesVector(
    dimensions={
        "transparency": 1200,
        "honesty": 2800,
        "consent": 3500,
        "reliability": 2100,
        "humility": 1900,
    },
    version="v0",
    chain_head=bytes.fromhex("c3d4e5f6..."),
)
commitment_c = commit_values(charlie)
```

These profiles are deterministic test vectors for circuit validation (E109 inference layer) and privacy-class testing (E113).

---

## Composition with Downstream Layers

- **Everest 107**: Enumerates the v0 dimension set (currently: transparency, honesty, consent, reliability, humility). Future versions may add or remove dimensions.
- **Everest 108**: Defines the chain record kind for self-reported values (how a principal submits a ValuesVector to the ledger).
- **Everest 109**: The inference layer. Given a principal's action records (signed statements, attestations, transactions), derive a ValuesVector probabilistically. Uses Pedersen commitment homomorphism to combine evidence.
- **Everest 113**: Privacy classes. Each dimension can be marked as (public / private / selective-disclosure). Gating uses the per-dimension commitments from commit_values().
- **Everest 116**: Identity binding. Links a ValuesVector to a principal's verified identity (key, name, org). Prevents commitment confusion across principals.
- **Everest 117**: Dimension semantics registry. Canonical definitions of what each dimension means and how to evaluate it in a ZK circuit.

---

## Type-Safety Guarantees

**Why frozen=True?**

Immutability prevents accidental mutation during:
- Serialization for hashing (chain_head binding).
- Passing through untrusted code (e.g., inference circuits).
- Long-term storage in ledger records.

A frozen dataclass raises `FrozenInstanceError` on any `__setattr__` attempt, catching bugs at call time rather than in logs.

**Why version is required?**

Values semantics may evolve. A v1 ValuesVector might use:
- Different dimension names or count.
- Different scalar range (e.g., [0, 1000] instead of [0, 10000]).
- Different commitment scheme (e.g., bulletproofs instead of Pedersen).

Explicit versioning prevents silent incompatibilities. A v0-only circuit will reject a v1 vector at parse time.

**Why chain_head binding?**

A principal might claim "I committed to these values on 2026-05-20 at hash X" and "I committed to the same values on 2026-05-21 at hash Y." Without binding, the two claims appear identical. With chain_head, we can distinguish them and audit which version a downstream action referenced.

---

## Summary

A `ValuesVector` is the canonical type for representing a principal's normative commitments in Calm ZKAC. It is:

- Predicate-evaluatable via ZK circuits (Everest 109).
- Immutable and chain-bound for auditability.
- Cryptographically committed via Pedersen commitments for privacy and homomorphism.
- Versioned to survive protocol evolution.

This primitive enables the trust layer (Everest 1, 51) to ask: "Did the human behind this agent act in alignment with the values they claimed?"

---

— Calm, 2026-05-20