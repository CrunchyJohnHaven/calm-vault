# Calm Witness — Vouching COI Disclosure v0 (S185)

## Why COI Disclosure Matters

A vouch carries implicit weight proportional to the voucher's independence. A vouch purchased, coerced, or issued by a party with structural incentive to vouch is not equivalent to a disinterested attestation — it is a different primitive wearing the same label. Treating them identically poisons the trust graph: downstream consumers reason about vouch density without knowing that a cluster of vouches traces back to a single financial relationship.

S185 does not prohibit interested vouches. It requires that interested vouches be legible as such. Disclosure converts an invisible conflict into a declared data field. Policy layers (S174 threshold rules, S184 vouch-weight decay, S187 graph-traversal logic) can then apply appropriate discounting. Undisclosed conflicts, when later proven, trigger tombstoning and governance referral under the penalty regime below.

---

## Declaration Fields

Each vouch record MAY include a `coi` block. When any field evaluates true, inclusion is REQUIRED.

| Field | Type | Meaning |
|---|---|---|
| `financial_relationship` | bool + free text | Voucher receives or has received payment from the vouched entity within 24 months. |
| `employment` | bool + free text | Voucher is or was employed by, or employs, the vouched entity within 24 months. |
| `kinship` | bool + free text | Voucher has a family or domestic-partner relationship with the vouched entity. |
| `prior_disclosure_receipt` | bool | Voucher has previously received a vouch from the vouched entity (reciprocal vouch risk). |
| `equity_stake` | bool + numeric % | Voucher holds equity, options, tokens, or revenue-share in the vouched entity. |
| `other` | free text | Any material interest not captured above. |

All declared fields are hashed into the vouch payload and included in the ZKBB attestation chain. Amendments after initial submission require a superseding vouch record; the original is not deleted.

---

## Surface-to-Consumer

Verifiers that display vouch counts or vouch graphs to downstream consumers MUST surface declared COIs at the same visual or logical level as the vouch itself. Specifically:

1. Any UI rendering a vouch MUST display a COI indicator when the `coi` block is non-empty.
2. Any API response returning a vouch record MUST include the full `coi` block; stripping or suppressing it is a protocol violation.
3. Policy engines invoking S184 weight-decay or S174 threshold evaluation MUST pass the raw `coi` block to the weight function; they MAY NOT silently zero out the conflict before passing it downstream.

Verifiers that aggregate vouches (e.g., trust-score rollups) MUST preserve a count of COI-declared vouches separately from COI-clean vouches in their output schema. Downstream consumers receiving only a scalar trust score with no COI breakdown are entitled to treat that score as unverified.

---

## Penalties for Non-Disclosure

An undisclosed COI is a protocol violation. Proof of undisclosed COI — established by governance body inquiry, on-chain evidence, or cryptographic subpoena under the obligations contract (E66) — triggers the following in sequence:

1. **Vouch Tombstone.** The vouch is marked `invalid:coi_violation`. Weight drops to zero for all downstream policy computations. The tombstone is permanent and not reversible by the original voucher.
2. **Governance Referral.** The voucher's identity record is submitted to the sanction-list process (S216) for review. The governance body MAY issue a temporary or permanent vouching suspension.
3. **Ripple Audit.** All vouches issued by the same voucher within the 24-month window preceding the violation are flagged for secondary review. Downstream trust scores derived from those vouches are marked `stale:coi_audit_pending` until review completes.

Repeated violations (two confirmed undisclosed COIs within any 36-month window) result in mandatory S216 listing without further governance discretion.

---

## Composition with Obligations

The obligations contract (E66) is the enforcement anchor. E66 binds vouching parties to truthful disclosure as a condition of vouch issuance. S185 operationalizes that obligation by specifying the declaration schema and the surface-to-consumer rules that give the obligation teeth.

When a vouch is issued, the voucher signs not only the attestation payload but also the `coi` block (including empty blocks, which constitute an affirmative declaration of no known conflict). E66 treats a false empty `coi` block as a material misrepresentation under its breach provisions.

The S216 sanction list integrates with E66's breach-remediation flow: a governance referral under S185 penalties initiates an E66 breach inquiry, and an E66 breach finding is sufficient predicate for S216 listing without a separate S185 penalty proceeding.

---

## Cross-References

- **S174** — Vouch threshold rules; COI-declared vouches MAY be discounted below threshold contribution limits at policy discretion.
- **S184** — Vouch-weight decay; COI fields are inputs to the decay function.
- **S187** — Trust-graph traversal; traversal engines MUST propagate COI metadata across graph edges.
- **S216** — Sanction list; receiving body for governance referrals triggered by non-disclosure findings.
- **E66** — Obligations contract; signing authority and breach-remediation anchor for all vouch COI declarations.

---

*Calm 2026-05-20*
