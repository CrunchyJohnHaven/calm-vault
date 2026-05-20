# Calm Witness Predicate Language v0 — Decision

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 51 of [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md).**
**Companion to [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md).**

## §1 — The decision

**v0 ships a fixed predicate table, not a domain-specific language.**

The fixed predicate table is the catalog in [`predicates_v0.json`](../../CredexAI/calm_witness/schema/predicates_v0.json). New predicates are added by minting new IDs under the rules in [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md) §2 — not by allowing principals or counterparties to author predicates at runtime.

A DSL is deferred to v2 at the earliest. v1 may add tightly-constrained parameterization (e.g. `biometric_match_within(τ)` already takes one numeric parameter), but the universe of predicate *shapes* remains closed in v0 and v1.

## §2 — Why a fixed table (not a DSL)

Four reasons, ordered by importance.

**§2.1 — Audit surface is bounded.** A fixed table of N predicates has exactly N evaluation surfaces to audit, prove circuits for (Everest 65), and certify against the protected-category floor (Everest 6 §4). A DSL has unbounded surface; every legal expression is a new audit target. For v0, where the predicate set is six entries and the certification load matters more than expressive flexibility, the fixed table dominates.

**§2.2 — Content-addressable IDs need stable semantics.** Everest 52 makes the predicate ID a hash over canonical predicate form. A DSL would require either (a) hashing the AST (fine, but adds parser surface) or (b) hashing the source text (brittle to whitespace and rewrites). A fixed table sidesteps this — the canonical form is just `{id, type, parameters, evaluator}`, and the evaluator is a frozen pseudocode string referencing a frozen reference implementation in `~/CredexAI/calm_witness/predicate_eval.py`.

**§2.3 — Counterparty caching.** Counterparties cache predicate IDs and their semantics. A fixed table caches once and never invalidates; a DSL forces counterparty verifiers to either (a) execute received expressions (unsafe) or (b) reject unrecognized predicates (functionally a fixed table anyway, but with extra parsing).

**§2.4 — Misuse resistance.** v0's threat model includes counterparties who would like to craft predicates that look like Calm Witness predicates but exfiltrate more than a single bit. A DSL hands them the parser. A fixed table refuses the surface.

## §3 — What the fixed table looks like

Six predicates ship in v0 (full specifications in `PREDICATE_VOCABULARY_v0.md`):

| ID | Slug | Type | Parameters |
|---|---|---|---|
| `cwp.v0.in_baseline_24h` | `in_baseline_24h` | bool | (none) |
| `cwp.v0.biometric_match_within` | `biometric_match_within` | bool | `tau: float ∈ (0,1]` |
| `cwp.v0.principal_consents_to_disclose` | `principal_consents_to_disclose` | bool | `(predicate_id: str, counterparty_class: str)` |
| `cwp.v0.bank_teller_note_active` | `bank_teller_note_active` | bool | (none) |
| `cwp.v0.cognitively_atypical_baseline` | `cognitively_atypical_baseline` | bool | (none) |
| `cwp.v0.mental_state_unusual` | `mental_state_unusual` | bool | (none) |

Each is a deterministic function from `(log_window, biometric_state, consent_record)` → `bool`. The evaluator pseudocode in the catalog is the contract; the reference implementation in `~/CredexAI/calm_witness/predicate_eval.py` is the artifact every counterparty SHOULD use, and the ZK circuits to be built in Range D translate from that pseudocode.

## §4 — Forward compatibility

Adding a predicate to v0 (strictly additive) is allowed under the §7 process in `PREDICATE_VOCABULARY_v0.md`. The append-only invariant on existing IDs is enforced by the gate at `~/CredexAI/scripts/everest_6_zkbb_predicate_vocabulary_gate.py` via the snapshot at `~/CredexAI/calm_witness/schema/predicates_v0.snapshot.json`.

Changing a predicate's semantics is not a v0 operation. It requires bumping the namespace (`cwp.v1.*`) and going through the v1 release cycle. This is a feature.

## §5 — What v2 would look like

When v2 adds a DSL (estimate: 2027 at earliest), the structure will be:

- A small expression grammar over a frozen primitive set (the v0/v1 predicates and a handful of combinators: `AND`, `OR`, `NOT`, `IMPLIES`, `WITHIN(time)`).
- A canonical AST representation (already content-addressable per the v0 rules).
- A reference parser + interpreter shipped under permissive license.
- An audit harness that enumerates a representative subset of expressible predicates and asserts each respects the protected-category floor.

But v2 is not v0's problem. v0 ships the table.

— Calm, 2026-05-20
