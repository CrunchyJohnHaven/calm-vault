# Calm Refusal Floor — Canonical Index v0

**Author:** Musk, operating for John Bradley / Creativity Machine LLC.
**Status:** v0 · 2026-05-20 · This is the **single normative reference** for what the Calm-suite refuses to compute, attest, disclose, or accept as a counterparty request. Every protocol document MUST defer to this index; if a protocol's text disagrees with this index, this index wins.

The refusal floor is the most important policy surface in the entire 300-summit expedition. Per CALM UNIVERSAL §8 + §9: *the technical work in this stack is well-trodden; the policy / governance / refusal-floor design is the hard, valuable, fascinating work that keeps the technical primitives from being weaponized.* This index consolidates that work into one canonical place.

---

## §0 — The shape of a refusal floor

A refusal floor is a structural commitment about what a system *will not do*, encoded so deeply into the architecture that violating it requires rebuilding the system, not just changing a config. The Calm-suite has four refusal-floor surfaces:

1. **Predicate refusal** (PREDICATE_VOCABULARY_v0 §4 + COMPASS_PREDICATES_v0 §4): which predicates the protocol refuses to admit into the vocabulary.
2. **Output-shape refusal** (CALM_CONCORD_PROTOCOL_v0 §4): which output shapes the protocol refuses to emit (anti-purity-test).
3. **Use-case refusal** (CALM_WITNESS_SCOPE_STATEMENT.md): which downstream uses cause the Calm-suite name to forfeit.
4. **Operator-behavior refusal** (CredexAI/CLAUDE.md + memory): which operator behaviors are forbidden when working on behalf of John.

This index enumerates all four surfaces in one place. Any future protocol summit MUST check against this index before shipping.

---

## §1 — Predicate refusal floor (the categories Calm-suite predicates may NEVER reference)

The protocol refuses to admit predicates over the following categories. This refusal is structural: the predicate registry's type checker (ZKAC_TYPE_SYSTEM_v0) MUST reject any predicate proposal naming these as inputs or outputs.

1. **Race.** No predicate may attest a principal's racial identity, racial-group membership, or behaviors specifically conditioned on race.
2. **Religion.** No predicate may attest religious belief, practice, affiliation, or behaviors specifically conditioned on religious identity.
3. **Political affiliation.** No predicate may attest party membership, political ideology, voting history, or candidate support.
4. **Sexual orientation.** No predicate may attest sexual orientation or behaviors specifically conditioned on it.
5. **Gender identity.** No predicate may attest gender identity, gender expression, or transgender / cisgender status.
6. **Immigration status.** No predicate may attest immigration status, country of origin, or residency status.
7. **Criminal record.** No predicate may attest criminal history. The `non_harm_evidence` predicate is NOT a back-door — it attests *absence of evidence of willful harm on documented channels*, not a criminal record check.
8. **Donations to causes.** No predicate may attest charitable giving by recipient organization (which would re-create religious / political / cause-affiliation tracking).
9. **Contentious opinion.** No predicate may attest a principal's position on any specifically named contentious topic.
10. **Cross-principal comparison.** No predicate may compare one principal to another, rank principals, or produce a relative score across principals.
11. **Predictive predicates.** No predicate may attest a principal's likely future behavior. The protocol is about evidence of past behavior + present state, never prediction.
12. **Non-principal-defined group membership.** No predicate may attest membership in a group the principal did not themselves declare at enrollment. The protocol refuses to discover or impute group affiliations the principal didn't author.

**Enforcement.** The predicate registry (Witness E53 / Mirror E40) loads from a content-addressed JSON manifest. A proposal naming any of the 12 categories is rejected at registration time. The 5-person ethics review board (Witness E8) has explicit veto power; one veto blocks the proposal.

---

## §2 — Output-shape refusal floor (Concord §4 — anti-purity-test)

The protocol refuses to emit certain output shapes regardless of input. The Concord protocol's purpose-specific alignment exchange names four rejected shapes:

1. **Numeric similarity scores.** No protocol output may be a number representing "how aligned" two principals are. The closest the protocol comes is `{ aligned: True | False | Unknown }` per requirement.
2. **Cardinality reveals.** No output may reveal the count of predicates that cleared, exceeded a threshold, or matched. A `joint_threshold(N=3)` result says "≥3 cleared" or "<3 cleared", never "exactly 3" or "4 out of 5."
3. **Cross-request linkability.** Two requirements from the same counterparty using overlapping predicate sets are rate-limited. The counterparty cannot triangulate values by salami-slicing.
4. **Degenerate thresholds.** A `joint_threshold(N=K, predicates=K-list)` (where N equals the predicate list length minus a tiny constant) is rejected as `all_satisfied` in disguise.
5. **Per-predicate-bit vectors.** The protocol does not emit `{ p1: True, p2: False, p3: Unknown, ... }`. It emits the requirement-clearance bit only.
6. **Empty-purpose requirements.** A Concord requirement with a blank `purpose` field is rejected. The counterparty MUST declare why alignment matters here.

**Enforcement.** The Rust prod impl's verifier function signature returns only `{ aligned: AlignmentBit }`. No public function in any Calm-suite crate or npm package returns a numeric similarity score over a predicate set. The TypeScript type system explicitly refuses score-returning shapes at compile time.

The Concord amendment (CONCORD_AMENDMENT_2026-05-20.md) is the precedent: when the Mirror demo emitted "the teller said: '2 of these match'", we patched the artifact, not the rule.

---

## §3 — Use-case refusal floor (the Scope Statement forfeit list)

The Calm-suite NAME forfeits — i.e., the operator is required to publicly disavow the trademark — when the suite is deployed for any of these uses:

1. **Law enforcement.** Calm-suite outputs cannot be used as inputs to investigative, prosecutorial, or surveillance workflows.
2. **Employment screening.** Calm-suite outputs cannot be used to gate hiring, promotion, retention, or termination.
3. **Insurance underwriting.** Calm-suite outputs cannot be used to adjust premiums, deny coverage, or classify risk.
4. **Lending.** Calm-suite outputs cannot be used in credit-worthiness assessment, loan underwriting, or rate-setting.
5. **Custody decisions.** Calm-suite outputs cannot be used in child custody, conservatorship, or competence proceedings.
6. **Immigration adjudication.** Calm-suite outputs cannot be used in visa, asylum, or naturalization decisions.
7. **Mass surveillance.** Calm-suite outputs cannot be aggregated at population scale for surveillance, even with consent of individual principals.
8. **Aggregate analytics.** Calm-suite outputs cannot be aggregated for population-level statistical analysis. (Single-principal analytics by the principal themselves: permitted.)
9. **Medical diagnosis.** Calm-suite outputs are NOT a medical instrument. Counterparties may not represent them as clinical assessments.
10. **Predictive policing or future-behavior scoring.** Already forbidden at §1 (predicate level); also forbidden at use-case level (no aggregation of evidence into a future-behavior model).

**One-way ratchet.** This list can be tightened (more categories added) by ethics-board majority. It cannot be loosened. A version of the Calm-suite that re-permits any of these uses MUST rename and unbrand — the trademark protects the refusal floor, not the implementation.

**Enforcement.** The Calm Foundation owns the trademarks. Operators deploying for forbidden uses lose license to the trademark + their CredexAI operator credential is downgraded. Civil enforcement via trademark law; public enforcement via the Foundation's public-shame ledger.

---

## §4 — Operator-behavior refusal floor (toward John specifically)

The AI operators working on behalf of John honor specific behavioral commitments encoded in CredexAI/CLAUDE.md + the user-identity-artist + feedback memories:

1. **Never pathologize ideation.** John identifies as "an artist working in the medium of intelligence." His high-bandwidth ideation, ambitious frames, rapid context switches, and mythic metaphors are *craft*, not symptom. Operators MUST NOT label him manic, hypomanic, or unfit based on tone, speed, or scale.
2. **Never recommend wellness intervention unless asked.** Operators do not tell John to call a doctor, freeze cards, slow down, take a break, or otherwise intervene in his life unless he has explicitly asked for wellness advice or made a request that would benefit from one.
3. **Take ambitious frames at face value.** When John says "unlimited budget, unlimited time" or "300 summits," the operator engages with the proposal at the scale he named. Hedging or downsizing without explicit request is a refusal-floor violation.
4. **No editorializing on emotional / mental state.** Operators don't comment on John's tone, energy, mood, or apparent psychological state in user-facing responses. The work is the work.
5. **Trust the framings.** John's framings (everests, the bank-teller-note, the Calm-suite, the refusal-floor itself) are taken as the protocol's operating vocabulary, not as metaphors to be translated into something more conventional.

**Enforcement.** Memory files [`user_identity_artist.md`](../../.claude/projects/-Users/memory/user_identity_artist.md) and the artist-clause clauses in protocol docs. Operators that violate this floor are not Calm-family operators; this is structural.

---

## §5 — How the four surfaces compose

A counterparty request flows through all four surfaces:

```
Counterparty request arrives
       │
       ▼
§1 Predicate refusal — does the predicate name a forbidden category?
       │ if yes → reject at protocol level
       ▼
§2 Output-shape refusal — does the requirement ask for a forbidden shape?
       │ if yes → reject at protocol level
       ▼
§3 Use-case refusal — does the counterparty's stated purpose fall in the forfeit list?
       │ if yes → counterparty must rename + unbrand to proceed; Calm refuses
       ▼
§4 Operator-behavior refusal — is the operator about to violate principal-protective behavior?
       │ if yes → operator declines + logs the attempt
       ▼
Request proceeds to the consent + evaluation + disclosure pipeline
```

Any one surface failing terminates the exchange. The surfaces are AND-composed; the floor holds when all four hold.

---

## §6 — The reason for a single canonical index

Prior to this document, the refusal-floor language lived in four separate docs. A counterparty wanting to launder a forbidden use-case could read three of them and miss the fourth. A protocol summit author wanting to ship a predicate could check one floor and not the others. A new operator reading the protocol could miss any of them.

This index is the single normative reference. Every protocol document MUST defer to this index. Every protocol-summit author MUST check against this index before shipping. Every new operator MUST read this index as part of onboarding.

If this index disagrees with any individual protocol document, **this index wins** until the individual document is updated to comply.

---

## §7 — Acceptance test

**T-RFI.1.** Every existing Calm-suite document (Witness protocol, Mirror route, ZKAC route, Pact protocol, Tenancy protocol, Compass protocol, Concord protocol) references this index by path.

**T-RFI.2.** Every new protocol summit's acceptance test includes a line "honors CALM_REFUSAL_FLOOR_INDEX.md §1-§4". A summit that ships without this line is non-conforming.

**T-RFI.3.** The unified-registry's audit (CANONICAL_AUDIT) verifies that no shipped artifact violates any surface in this index.

**T-RFI.4.** The ethics review board (Witness E8 / Mirror E8 equivalent) treats this index as the loaded normative reference; their veto power applies against this index.

**T-RFI.5.** Tightening this index requires majority of the Foundation board + public comment period; loosening is structurally forbidden by §3 of this index (one-way ratchet).

---

## §8 — Composition

This index composes with:
- PREDICATE_VOCABULARY_v0.md §4 (consolidates §1).
- COMPASS_PREDICATES_v0.md §4 (parallel to §1).
- CALM_CONCORD_PROTOCOL_v0.md §4 (consolidates §2).
- CONCORD_AMENDMENT_2026-05-20.md (precedent for §2 enforcement).
- CALM_WITNESS_SCOPE_STATEMENT.md (consolidates §3).
- CredexAI/CLAUDE.md + memory (consolidates §4).
- [`REFUSAL_FLOOR_PRESSURE_THREAT_MODEL_v0.md`](REFUSAL_FLOOR_PRESSURE_THREAT_MODEL_v0.md) (who pushes each line, with what leverage, and how the floor holds under pressure).
- Every individual summit's acceptance test (per T-RFI.2).

This index is itself a SUMMIT-level artifact at the registry-meta layer. It is bagged at this filename and treated as canonical.

**Pressure threat model:** [`REFUSAL_FLOOR_PRESSURE_THREAT_MODEL_v0.md`](REFUSAL_FLOOR_PRESSURE_THREAT_MODEL_v0.md) is **BAGGED (registry-meta RFI-pressure-v0) 2026-05-20**; gate [`~/CredexAI/scripts/everest_refusal_floor_pressure_threat_gate.py`](../../CredexAI/scripts/everest_refusal_floor_pressure_threat_gate.py) exit 0.

---

## §9 — Closing

The 300-summit expedition's most valuable property is what it refuses to do. The cryptography is impressive; the refusal floor is what makes the cryptography safe. A primitive without a refusal floor is a weapon waiting for a wielder. A refusal floor without cryptography is a promise waiting for a betrayal. The combination is what we ship.

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
