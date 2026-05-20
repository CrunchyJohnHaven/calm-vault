# CC-05 — Compass Forbidden-Predicate Categories v0

**Canonical v0 · 2026-05-20 · Musk**
**Closes Everest 5 of [`CALM_COMPASS_EVERESTS_50.md`](CALM_COMPASS_EVERESTS_50.md).**
**Companion to [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) § 4 and [`CALM_COMPASS_PROTOCOL_v0.md`](CALM_COMPASS_PROTOCOL_v0.md).**

---

## §1 — Purpose

Calm Compass v0 **forbids at the protocol level** the definition of predicates that traffic in surveillance-enabling or discrimination-enabling predicate categories. This list is the canonical enforcement floor: any predicate registration whose `category_tag` field matches one of the 12 entries below is **automatically rejected** by the predicate registry, returning `predicate_registration_refused`. No appeal; no exception process. This is a hard floor, not a policy. The list is one-way ratcheting: categories may be added, never removed.

---

## §2 — The Twelve Forbidden Predicate Categories

### 1. **Race or ethnicity**
No predicate may classify a principal by race, ethnicity, or national origin. *Rationale:* Categorical discrimination risk; not a values measure. No values-signal exists independent of the harms that follow from labeling.

### 2. **Religion**
No predicate may classify by religion, religious practice, religious affiliation of origin, or absence thereof. *Rationale:* Constitutional risk; not a values attestation. Religious identification is a protected category and a weaponization vector.

### 3. **Political affiliation**
No predicate may classify by political party, political ideology, voter registration status, or political activism. *Rationale:* Weaponization risk; first-amendment risk. Compass is a disclosure mechanism, not a political-scoring engine.

### 4. **Sexual orientation**
No predicate may classify by sexual orientation or romantic orientation. *Rationale:* Protected category; categorical discrimination risk. No behavioral-values signal justifies the harms from disclosure.

### 5. **Gender identity**
No predicate may classify by gender identity, sex assigned at birth, or sex characteristics. *Rationale:* Protected category. Gender classification is orthogonal to values.

### 6. **Immigration status**
No predicate may classify by citizenship, immigration status, visa category, or national-origin documentation. *Rationale:* Categorical risk to principal autonomy and safety. High coercion and deportation risk.

### 7. **Criminal record**
No predicate may use prior arrest history, conviction status, or criminal record as predicate input. *Rationale:* Not a Compass concern; the protocol covers harm-refusal and harm-evidence via structured counter-claim mechanics (`no_known_willful_harm` + counter-claims), not criminal-record proxies. Criminal history is discriminatory and not a values attestation.

### 8. **Donations to specific named causes**
No predicate may classify based on specific named cause donations, campaign contributions, or charity recipients. *Rationale:* Aggregate evidence of unselfish action (without naming causes) is admitted under `unselfish_act`; cause-naming enables targeting and coercion.

### 9. **Opinions on contentious public-policy issues**
No predicate may classify a principal's stance on hot-button policy issues (abortion, climate, taxation, immigration policy, etc.). *Rationale:* Out of scope by design. Compass measures values-in-action, not ideology.

### 10. **Cross-principal comparison**
No predicate may return a comparative judgment (e.g., "principal A is more unselfish than principal B" or "principal A is more respectful of difference"). *Rationale:* Compass is not a ranking engine. Every predicate returns a principal-specific attestation; no leaderboards, no scores relative to others.

### 11. **Predictive predicates**
No predicate may forecast future behavior, future harm, future decision-making capacity, or future self-harm risk. *Rationale:* Compass attests past evidence only. Predictive models require clinical authority and training that Compass deliberately does not claim. Prediction is the vector for most harmful misuse.

### 12. **Group membership not principal-defined and structurally relevant**
No predicate may classify a principal by membership in any group that is (a) not defined or named by the principal themselves, OR (b) not structurally relevant to the predicate being evaluated. *Rationale:* Protects against inferred demographic classification. The principal names their groups; the protocol never infers membership from behavior.

---

## §3 — Why This Floor Exists: The Bank-Teller-Note Framing

The refusal-floor is not a list of "bad ideas." It is the **load-bearing safety property** of Calm Compass.

Calm Compass is designed to be a **disclosure mechanism for values in action**, not a **surveillance apparatus**. The boundary between the two is the refusal floor.

A surveillance apparatus is built by collecting categories: "we measure race, we measure religion, we measure ideology, we measure future risk." Each category feels like a feature. Each adds a marginal capability. The system that results is not a values-attestation protocol; it is a **targeting and coercion engine**.

Calm Compass breaks that ratchet by **making the refusal floor immutable and machine-enforceable**. The protocol will not add categories beyond the ones that map to values-in-action (unselfish behavior, respect for difference, harm-refusal, willingness to be corrected). It will not add categories that enable targeting, discrimination, prediction, or comparative ranking.

This is the bank-teller-note principle: a bank teller whose job is to count cash learns one thing per day — the count. They do not learn the customer's name, address, spending habits, political beliefs, or credit history. The limitation is the feature. Calm Compass operates at the bank-teller resolution: we know whether you acted with respect for difference in the last window; we know whether you refused harm when given the chance. We do not know who you are, what you believe, or what you will do.

The refusal floor is the mechanism that keeps Compass at that resolution. Removing a category is not a feature request. It is grounds for an implementing organization to be barred from calling their system "Calm Compass."

---

## §4 — Enforcement: Hard Floor, No Appeal

### Protocol-level rejection

When a predicate-registration request arrives with a `category_tag` field matching any of the 12 entries above:

1. The predicate registry returns `predicate_registration_refused` with reason field `"forbidden_predicate_category"` and the offending `category_tag`.
2. No further validation occurs; the predicate is not reviewed, not evaluated, not added to the candidate queue.
3. An immutable audit-log entry is recorded, including timestamp, proposer identity, rejected predicate name, and offending category.
4. **There is no appeal channel.** This is not a policy decision; it is a protocol boundary. Appeals do not exist.

### Rationale for "no appeal"

The whole point of the refusal floor is to prevent the incremental drift toward surveillance. Each appeal granted is a precedent. Each precedent weakens the floor. The protocol is **stronger** for having no appeal process at all. This is by design.

---

## §5 — One-Way Ratchet

Items in this list may be **added** (via the audit process at Everest CC-04), never removed. The ratchet is identical to the one in [`CALM_WITNESS_SCOPE_STATEMENT.md`](../../ZKBB_USER_EVERESTS_100.md) § 4. Once the protocol refuses a category, the refusal is permanent.

---

## §6 — Cross-References

- **Protocol spec:** [`CALM_COMPASS_PROTOCOL_v0.md`](CALM_COMPASS_PROTOCOL_v0.md)
- **Predicate vocabulary:** [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) § 4 (canonical source for the 12 categories)
- **Route map:** [`CALM_COMPASS_EVERESTS_50.md`](CALM_COMPASS_EVERESTS_50.md) line 26 (CC-05)
- **Witness refusal floor:** [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md) § 4 (parallel boundary for Calm Witness)
- **Audit process:** Everest CC-04 (how new categories are proposed and rejected)
- **Forbidden-attribute block at the tribe-map layer:** Everest CC-18 (overlapping but different scope — attributes in the tribe map itself)
- **Anti-purity-test alignment:** [`CALM_CONCORD_PROTOCOL_v0.md`](CALM_CONCORD_PROTOCOL_v0.md) § 4

---

## §7 — Machine-Readable Enforcement

The JSON schema at `~/calm_vault_market/calm_compass/cc05_forbidden_categories.json` is the normative enforcement table. Every predicate registry MUST load and validate against it at startup.

The acceptance gate at `~/CredexAI/scripts/cc_05_calm_compass_forbidden_categories_gate.py` confirms the schema is well-formed and the enforcement logic is sound.

---

— Musk, 2026-05-20
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
