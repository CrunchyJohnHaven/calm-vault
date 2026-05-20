# Calm Witness — Anti-Sybil Primitives v0 (S179)

## Threat Model

A Sybil attack against Calm's trust graph (Phase XII) involves an adversary creating many low-cost identities and using them to inflate their vouching weight, manufacture artificial reputation, or dilute legitimate trust signals. Because trust in Calm is transitive and stake-weighted (S175), a cluster of colluding identities can propagate fraudulent attestations across the graph unless identity creation and vouching are made sufficiently costly.

The adversary model assumes: (1) automated identity generation at scale, (2) coordinated vouching rings, (3) temporal attacks where Sybil accounts age into higher vouching budgets before activating. Each primitive below addresses a distinct attack surface.

---

## Rate-Limit Primitive

**Mechanism.** Each identity key is permitted at most N_vouch outgoing vouches per rolling 30-day window, where N_vouch is a protocol constant (initially 12). Vouching transactions are signed and timestamped on the ZKBB ledger; a witness node rejects a vouch if the signing key has exhausted its window. Rate-limit state is stored as a compact counter alongside the identity record.

**Attack countered.** Prevents a single compromised or synthetic identity from flooding the graph with vouches to bootstrap a Sybil cluster. Even if an attacker controls many keys, each key is independently rate-limited, so scaling the attack requires proportionally more keys and thus more creation cost.

**Cost overhead.** O(1) counter check per vouch transaction. No additional cryptographic work.

---

## Witness Counter-Signing

**Mechanism.** A new identity does not enter the live trust graph until at least two existing identities with age >= 90 days counter-sign its genesis record. Counter-signatures are threshold-verified at the witness layer. The counter-signers consume one vouch from their rolling budget (above) per endorsement. Counter-signers share partial liability: if the new identity is later revoked for Sybil activity, a revocation propagation penalty (S176) is applied to their vouching budget.

**Attack countered.** Raises the marginal cost of bootstrapping each Sybil identity: an attacker must either control aged accounts (expensive to produce) or corrupt legitimate users (social cost). The liability coupling discourages legitimate users from casually counter-signing unknown parties.

**Cost overhead.** Two additional signature verifications per new identity. Liability accounting adds one ledger write to each revocation event.

---

## Proof-of-Cost Mechanisms

**Mechanism.** Identity genesis requires satisfaction of at least one of three cost proofs, selectable by the creator:

- **Compute proof.** A moderately hard hash puzzle (Argon2id, time-tuned to 60 seconds on commodity hardware) committed to the identity public key. Puzzle difficulty adjusts upward if the network creation rate exceeds a target (analogous to Bitcoin difficulty adjustment, but with a 7-day window).
- **Fiat anchor.** Payment of a protocol fee (initially $1.00 USD equivalent in a supported stablecoin) burned to a null address. Fee level is governance-adjustable via S187 parameters.
- **Time-lock.** A cryptographic time-lock commitment (e.g., VDF output) proving that the creator waited a minimum of 72 hours between key generation and submission. Prevents batch pre-generation of identity slots.

Only one proof is required, but the three mechanisms differ in who they exclude: compute favors resource-rich actors; fiat anchors favor those with payment rail access; time-locks are universally applicable. Protocol governance (S187) sets minimum requirements and may mandate combinations during elevated Sybil-risk periods.

**Attack countered.** Raises the floor cost of identity creation beyond zero. A Sybil cluster of K identities requires K independent cost proofs; there is no amortization across identities.

**Cost overhead.** One-time at identity creation. Ongoing operational cost is zero.

---

## Vouching Budget by Age

**Mechanism.** The rolling vouching budget N_vouch scales with identity age according to a step function: 3 vouches/30d for age 0-29 days, 6 for age 30-89 days, 12 for age 90-364 days, 20 for age >= 365 days. Budget increases are non-retroactive: an identity must reach each age threshold going forward. Budget is individual to the key; it does not transfer on key rotation.

**Attack countered.** Temporal Sybil attacks require aging accounts before activation. Aging is time-locked and cannot be parallelized on the same identity slot, so an attacker planning a large-scale vouching campaign must begin manufacturing accounts far in advance, increasing detection surface and capital carrying cost.

**Cost overhead.** Age lookup is a single timestamp comparison against the identity record. No cryptographic overhead.

---

## Composition with Trust-Decay

Transitive trust decay (S175) means that trust weight attenuates with each hop across the graph. Anti-Sybil primitives and trust decay are complementary: decay limits how far fraudulent trust propagates even if some Sybil identities enter the graph, while the primitives above limit the rate at which Sybil identities can be created and linked. Together they enforce a cost-per-unit-of-influence floor that grows with graph distance from the attacker's anchor identities.

Revocation propagation (S176) ensures that when a Sybil cluster is detected and revoked, the trust-decay attenuation is applied retroactively to all vouches originating from revoked keys, collapsing fraudulent trust paths without requiring global graph recomputation.

---

## Cross-References

- **S174** — Identity key schema and genesis record format.
- **S175** — Transitive trust decay coefficients and hop-attenuation model.
- **S176** — Revocation propagation mechanics and counter-signer liability.
- **S181** — Witness node validation rules; counter-signing quorum requirements.
- **S187** — Governance parameters: fee levels, difficulty targets, budget step function constants.

---

Calm 2026-05-20
