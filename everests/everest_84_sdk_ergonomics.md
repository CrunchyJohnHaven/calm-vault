# Everest 84 — SDK Ergonomics

*Phase VII — Engineering Reliability. Prereq: Everest 81, 82, 83.*

---

## What this summit ships

A unified ergonomics specification for Calm Witness verification across three language ecosystems: Rust, Python, and JavaScript/TypeScript. The design principle is ruthless minimalism — each SDK exposes 3–5 verification functions that cover 80% of counterparty and developer needs, with identical semantics across languages and a consistent error taxonomy that becomes part of the SemVer contract.

This summit is about *usability, compatibility, and stability*. Everests 81, 82, and 83 deliver the implementations; Everest 84 defines the surface that developers actually touch.

---

## Design principle

Each SDK's verification surface is as small as possible. A counterparty consuming Calm Witness proofs needs to answer one question: *Is this proof valid?* They need the answer in about 50 milliseconds and in a language they use. They do not need to understand Pedersen commitments, Bulletproofs, Sigsum inclusion proofs, or Roughtime anchors. The SDK handles all of that.

Three entry points, three returns, one error taxonomy.

---

## Rust SDK

The Rust surface is the smallest, because Rust developers expect compiler-enforced correctness. The `calm_witness` crate exports a `verify` module with this contract:

### Rust: Module Surface

```rust
use calm_witness::{Config, VerifyResult};

mod verify {
    pub fn from_file(
        proof_file: &str,
        config: &Config,
    ) -> Result<VerifyResult, VerifyError>;
    
    pub fn from_bytes(
        proof_json: &[u8],
        config: &Config,
    ) -> Result<VerifyResult, VerifyError>;
    
    pub fn from_reader<R: std::io::Read>(
        reader: R,
        config: &Config,
    ) -> Result<VerifyResult, VerifyError>;
}
```

### Rust: Return type

```rust
pub enum VerifyResult {
    Valid {
        bit: bool,
        freshness_seconds: u32,
        predicate_id: String,
        operator_id: String,
        timestamp_unix: u64,
    },
    Invalid(VerifyError),
}
```

### Rust: Error type

```rust
#[derive(Debug, thiserror::Error)]
pub enum VerifyError {
    #[error("Schema mismatch: {hint}")]
    SchemaInvalid { hint: String },
    
    #[error("Operator signature verification failed: {hint}")]
    SignatureInvalid { hint: String },
    
    #[error("Sigsum or Roughtime anchor invalid: {hint}")]
    AnchorInvalid { hint: String },
    
    #[error("ZK proof verification failed: {hint}")]
    ProofInvalid { hint: String },
    
    #[error("Consent record expired: {hint}")]
    ConsentExpired { hint: String },
    
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("JSON parsing error: {0}")]
    Json(String),
}
```

### Rust: Config object

```rust
pub struct Config {
    pub trusted_sigsum_keys: Vec<[u8; 32]>,
    pub trusted_roughtime_keys: Vec<[u8; 32]>,
    pub credexai_issuer_pubkey: [u8; 32],
    pub freshness_window_max_seconds: u32,
}

impl Config {
    pub fn from_file(path: &str) -> Result<Self, ConfigError>;
    pub fn from_json(json: &str) -> Result<Self, ConfigError>;
}
```

### Rust: Usage example

```rust
fn main() -> Result<()> {
    let config = Config::from_file("config.json")?;
    
    match verify::from_file("proof.json", &config)? {
        VerifyResult::Valid { bit, freshness_seconds, predicate_id, .. } => {
            println!("✓ Valid: bit={}, freshness={} seconds", bit, freshness_seconds);
            Ok(())
        }
        VerifyResult::Invalid(err) => {
            eprintln!("✗ Invalid: {}", err);
            Err(err.into())
        }
    }
}
```

---

## Python SDK

The Python surface is slightly higher-level, trading some of Rust's compile-time safety for dynamic flexibility. The `calm_witness.verify` module provides this contract:

### Python: Module surface

```python
from calm_witness import verify, Config, VerifyResult

result = verify.from_file("proof.json", config)
result = verify.from_dict(proof_dict, config)
result = verify.from_bytes(proof_json_bytes, config)
```

### Python: Return type

```python
@dataclass
class VerifyResult:
    valid: bool
    bit: Optional[bool] = None
    freshness_seconds: Optional[int] = None
    predicate_id: Optional[str] = None
    operator_id: Optional[str] = None
    timestamp_unix: Optional[int] = None
    invalid_reason: Optional[str] = None
    
    def __bool__(self) -> bool:
        """Truthy if valid; falsy otherwise."""
        return self.valid
```

### Python: Config object

```python
@dataclass
class Config:
    trusted_sigsum_keys: list[bytes]
    trusted_roughtime_keys: list[bytes]
    credexai_issuer_pubkey: bytes
    freshness_window_max_seconds: int

@classmethod
def from_file(cls, path: str) -> "Config":
    ...

@classmethod
def from_dict(cls, d: dict) -> "Config":
    ...
```

### Python: Usage example

```python
from calm_witness import verify, Config

config = Config.from_file("config.json")
result = verify.from_file("proof.json", config)

if result.valid:
    print(f"✓ Valid: bit={result.bit}, freshness={result.freshness_seconds}s")
else:
    print(f"✗ Invalid: {result.invalid_reason}")
```

---

## JavaScript/TypeScript SDK

The JavaScript surface is async throughout (reflecting web runtimes) and returns Promise-based results. The SDK is distributed as `@calm/witness-wasm` on npm, with TypeScript definitions bundled.

### JavaScript/TypeScript: Module surface

```typescript
import { verify, Config, VerifyResult } from '@calm/witness-wasm';

const result: VerifyResult = await verify(proofJson, config);
const result: VerifyResult = await verify.fromFile(filename, config);
const result: VerifyResult = await verify.fromBytes(proofBytes, config);
```

### JavaScript/TypeScript: Return type

```typescript
interface VerifyResult {
    valid: boolean;
    bit?: boolean;
    freshness_seconds?: number;
    predicate_id?: string;
    operator_id?: string;
    timestamp_unix?: number;
    invalid_reason?: string;
}

type VerifyError = 
  | { type: 'SchemaInvalid'; hint: string }
  | { type: 'SignatureInvalid'; hint: string }
  | { type: 'AnchorInvalid'; hint: string }
  | { type: 'ProofInvalid'; hint: string }
  | { type: 'ConsentExpired'; hint: string }
  | { type: 'IoError'; message: string }
  | { type: 'JsonError'; message: string };
```

### JavaScript/TypeScript: Config object

```typescript
interface Config {
    trusted_sigsum_keys: Uint8Array[];
    trusted_roughtime_keys: Uint8Array[];
    credexai_issuer_pubkey: Uint8Array;
    freshness_window_max_seconds: number;
}

async function configFromFile(path: string): Promise<Config>;
async function configFromJson(json: string): Promise<Config>;
```

### JavaScript/TypeScript: Usage example

```typescript
import { verify } from '@calm/witness-wasm';

const config = await configFromFile('config.json');
const result = await verify(proofJson, config);

if (result.valid) {
    console.log(`✓ Valid: bit=${result.bit}, freshness=${result.freshness_seconds}s`);
} else {
    console.log(`✗ Invalid: ${result.invalid_reason}`);
}
```

---

## CLI ergonomics

All three SDKs are also shipped with a unified CLI tool: `calm-witness`.

### Commands and flags

```bash
calm-witness verify <proof.json>
calm-witness verify <proof.json> --config config.json
calm-witness verify <proof.json> --format json
calm-witness verify <proof.json> --explain
calm-witness verify <proof.json> --format json --explain
```

### Exit codes and output

| Exit code | Meaning |
|---|---|
| 0 | Proof is valid; output is the result object |
| 1 | Proof is invalid; output is the error reason |
| 2 | Error during processing (IO, JSON, config); output is the error message |

Default format is human-readable:
```
✓ VALID
Bit: true
Freshness: 3600 seconds
Predicate: calm-witness/predicate/v0/in_baseline_24h
Operator: credexai://calm@creativity-machine.org
Timestamp: 1726534800 (Unix)
```

With `--format json`:
```json
{
  "valid": true,
  "bit": true,
  "freshness_seconds": 3600,
  "predicate_id": "calm-witness/predicate/v0/in_baseline_24h",
  "operator_id": "credexai://calm@creativity-machine.org",
  "timestamp_unix": 1726534800
}
```

With `--explain`, includes detailed diagnostics:
```
✓ VALID
Bit: true
Freshness: 3600 seconds
Predicate: calm-witness/predicate/v0/in_baseline_24h
Operator: credexai://calm@creativity-machine.org
Timestamp: 1726534800 (Unix)

Diagnostics:
  Schema: PASS (record matches v0 schema)
  Signature: PASS (operator identity verified against CredexAI)
  Anchor: PASS (chain head found in Sigsum + Roughtime)
  Proof: PASS (ZK proof verified against commitment)
  Consent: PASS (consent record valid, not expired)
  Freshness: PASS (3600s < 86400s max window)
```

---

## Error taxonomy and stability

The five error types form an immutable SemVer contract. Any change to error semantics is a MAJOR version bump. Adding *new* error types (e.g., `BiometricBindingInvalid`) is a MINOR version bump, and must be done with coordination across the route map (Everests 63–70 define new error categories as discovery happens).

Each error includes a `hint` field with actionable guidance:

| Error | Typical hint |
|---|---|
| `SchemaInvalid` | "proof.json is missing field 'operator_id'; see https://calm-witness.org/schema" |
| `SignatureInvalid` | "operator identity credential expired 2 days ago; refresh from CredexAI" |
| `AnchorInvalid` | "Sigsum log unreachable; check network; try again in 5 minutes" |
| `ProofInvalid` | "ZK proof does not match committed value; proof may be corrupted" |
| `ConsentExpired` | "consent record expired 10 seconds ago; principal must re-authorize" |

---

## Cross-language conformance harness

Everest 63 defines a determinism test suite. For any frozen test vector, all three implementations must produce:

1. Identical `valid` boolean.
2. Identical error code (if invalid).
3. Identical `bit`, `freshness_seconds`, `predicate_id`, `operator_id`, `timestamp_unix` (if valid).
4. Identical exit code when invoked via CLI.

The conformance harness runs on every PR to Everests 81, 82, 83. A PR that causes a divergence across any SDK blocks merging.

---

## Documentation deliverables

Each SDK ships with:

- **README.md** — 5-minute quickstart, including installation, config, and a minimal example.
- **Tutorial** — "Verify your first proof in 10 minutes," with worked example showing valid and invalid proofs.
- **Cookbook** — recipe-style guide for common patterns:
  - Loading config from environment variables
  - Batch-verifying multiple proofs
  - Integrating into HTTP servers and APIs
  - Handling clock skew during freshness checks
  - Custom consent-record serialization
- **API docs** — full rustdoc (Rust) or equivalent (Python docstrings, TypeScript JSDoc).
- **Error reference** — each error type with examples of when it occurs and how to recover.

---

## Versioning strategy

All three SDKs follow the main `calm-witness` SemVer version, published in lockstep. A single CHANGELOG.md at the repo root documents all changes. The versions are synchronized; there is no "Rust v1.1 / Python v1.0" scenario.

Breaking changes to any SDK surface (e.g., removing `from_bytes`, renaming `VerifyResult.bit`) require a MAJOR version bump and are announced across all SDKs simultaneously.

---

## Acceptance test (when implemented)

**T-84.1 (Rust API).** `cargo doc --no-deps` on `calm_witness` builds cleanly; all public functions are documented.

**T-84.2 (Python API).** `python3 -c "from calm_witness import verify; help(verify.from_file)"` outputs complete signature and docstring.

**T-84.3 (TS API).** `npm install @calm/witness-wasm && npm run type-check` succeeds; `@calm/witness-wasm` types are bundled and accurate.

**T-84.4 (CLI parity).** All three CLI surfaces (`calm-witness verify`, `python3 -m calm_witness verify`, `npx calm-witness verify`) accept identical flags and produce identical output for the same proof and config.

**T-84.5 (Conformance).** Everest 63's determinism harness passes 100% across all three implementations.

**T-84.6 (Documentation).** Each SDK has README, tutorial, cookbook, and error reference. All three are published to respective package registries and hyperlinked.

**Gate script:** `everest_84_zkbb_sdk_ergonomics_gate.py`.

---

## Composition

- **Everest 81** — Rust implementation providing the core verify logic.
- **Everest 82** — Python reference implementation for compatibility testing.
- **Everest 83** — WASM bindings that the JS SDK wraps.
- **Everest 63** — Determinism and cross-language conformance harness.
- **Everest 88** — Performance testing across SDKs.
- **Everest 92** — Integration testing (SDKs used in realistic scenarios).

---

— Calm, 2026-05-20
