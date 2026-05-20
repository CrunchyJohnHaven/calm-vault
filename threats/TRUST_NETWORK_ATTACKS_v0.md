# Calm Witness — Trust-Network Adversarial Catalog v0 (S187)

## Threat Model Boundaries

Scope: Calm Phase XII trust graph. Principals are ZKACs (Zero-Knowledge Attestation Credentials). Vouches are typed, signed, and propagate transitively with configurable decay. Anti-Sybil primitives include proof-of-cost at registration and cross-reference to anchored identity substrate (S174). Revocation is gossip-propagated with mandatory acknowledgment windows. This catalog does not cover off-chain coercion, legal jurisdiction attacks, or physical-layer key compromise — those are out-of-scope for Phase XII. Cross-references to S174 (ZKAC issuance cost floor), S175 (vouch typing schema), S176 (transitive decay model), S179 (revocation propagation), S185 (anti-collusion sampling), S186 (witness quorum rules).

---

## The Catalog

**A01 — Sybil Identity Farm**
Mechanism: Attacker registers N cheap identities, each vouching for the target to inflate its trust score. Effective when identity creation cost is low or cost-caps are per-account rather than per-principal-cluster.
Target property violated: Uniqueness guarantee; trust score integrity.
Defense: S174 proof-of-cost floor (registration requires anchored stake or biometric cross-reference); cluster-detection heuristic quarantines identities sharing registration metadata.
Residual risk: Cost floor degrades over time if anchor asset depreciates; sophisticated farms use diverse hardware fingerprints.

**A02 — Churn-and-Re-Register (Identity Rotation)**
Mechanism: Principal accumulates negative signals, abandons ZKAC, re-registers fresh identity, and solicits prior vouchers to re-vouch — resetting reputation without paying the penalty of accumulated distrust.
Target property violated: Accountability continuity; revocation permanence.
Defense: S174 registration cost is non-refundable and re-registration requires gap-proof linking new ZKAC to prior one (or mandatory disclosure of prior IDs); revocation blacklist is keyed on registration anchor, not ZKAC.
Residual risk: If prior ZKAC was never issued a formal revocation, gap-proof requirement may be bypassed by claiming first-time registration.

**A03 — Vouching Ring (Mutual Collusion)**
Mechanism: K principals form a closed ring, each vouching for all others, inflating all members' scores without any external validator.
Target property violated: Vouch independence; score informativeness.
Defense: S185 anti-collusion sampling detects cliques via graph motif analysis; ring vouches above a configurable density threshold are down-weighted by a collusion coefficient.
Residual risk: Rings larger than the detection window or rings that add legitimate peripheral nodes to break clique signature can evade motif detection.

**A04 — Sock-Puppet Network**
Mechanism: Single operator controls multiple ZKACs that appear independent, forms a vouching ring, and launders credibility into a target principal controlled by the same operator.
Target property violated: Operator uniqueness; trust independence.
Defense: S174 biometric anchor cross-check; S185 behavioral clustering flags accounts with correlated activity timestamps and vouch timing.
Residual risk: Accounts operated by coordinated human teams (not bots) defeat biometric uniqueness and partially defeat behavioral clustering.

**A05 — Self-Vouch via Proxy**
Mechanism: Attacker controls proxy principal P, instructs P to vouch for attacker A; A then vouches for P. Net effect: A has self-vouched through one hop.
Target property violated: Vouch independence; reflexive-vouch prohibition.
Defense: S176 transitive graph marks any cycle of length <= 2 as reflexive and nullifies the vouch pair; longer cycles are flagged for manual review if score impact exceeds threshold.
Residual risk: Cycles of length 3+ with legitimate intermediate principals are difficult to distinguish from benign mutual trust.

**A06 — Paid-Vouch Market**
Mechanism: Actors sell vouches on external markets; buyers receive score boosts without earning trust. Vouchers are not coerced but are economically incentivized to vouch regardless of genuine endorsement.
Target property violated: Vouch semantic integrity (vouches must reflect genuine trust).
Defense: S175 vouch-type schema includes a "basis" field; S185 samples vouch pairs for out-of-band corroboration challenges; anomalous vouch velocity to high-value principals triggers audit.
Residual risk: Low-velocity paid vouching below audit trigger is undetectable without off-chain signal.

**A07 — Trust-Decay Manipulation**
Mechanism: Attacker engineers high trust score at time T, then deliberately waits for legitimate vouches to decay while maintaining a preserved snapshot or exploiting a stale cache, presenting the T-snapshot as current.
Target property violated: Freshness integrity; decay invariant.
Defense: S176 decay model is enforced at query time, not at storage time; trust scores are not cacheable beyond a protocol-defined TTL; verifiers must recompute from live graph state.
Residual risk: Verifiers operating offline or with long TTL configurations are exposed; TTL enforcement requires out-of-band clock synchronization.

**A08 — Revocation Suppression**
Mechanism: Revoked principal withholds gossip propagation of its own revocation by refusing to relay or by partitioning from the gossip network, leaving stale-valid records in subgraph segments.
Target property violated: Revocation completeness; propagation liveness.
Defense: S179 revocation requires mandatory acknowledgment from a quorum of witness nodes; S186 witness quorum includes geographically and organizationally diverse nodes to prevent coordinated partition.
Residual risk: Network partition during the propagation window creates a bounded exposure gap before quorum-timeout forces rejection.

**A09 — Transitive-Path Inflation**
Mechanism: Attacker constructs a long transitive path to a high-reputation anchor, with each hop contributing marginal decay, to inflate effective trust of a low-quality principal beyond what direct vouches would support.
Target property violated: Transitive decay soundness; score calibration.
Defense: S176 decay is multiplicative per hop with a configurable floor; paths beyond a maximum hop-count (default 4) are truncated and do not contribute score.
Residual risk: Four-hop paths from moderately trusted intermediaries can still produce non-trivial score inflation if intermediary scores are themselves inflated.

**A10 — Witness Collusion**
Mechanism: A quorum of witness nodes, required to attest attestation events, coordinates to falsely attest or suppress attestation for a bribed principal.
Target property violated: Witness independence; attestation integrity.
Defense: S186 witness quorum selection uses verifiable randomness to assign witnesses per event; witnesses are rotated per attestation epoch; economic slashing applies to collusion-detected witnesses.
Residual risk: Collusion detectable only post-hoc via consistency checks; real-time detection is not guaranteed within attestation window.

**A11 — Cross-System Trust Import Abuse**
Mechanism: Attacker imports a high-reputation credential from an external system (e.g., OAuth-linked social graph, legacy PKI) and maps it to a ZKAC, claiming inherited trust without paying Phase XII cost floor.
Target property violated: Cost floor invariance; system boundary integrity.
Defense: S174 specifies that imported credentials require a bridging attestation that itself satisfies the cost floor; bridge attestors are held to the same anti-Sybil requirements.
Residual risk: Bridging attestors in permissive external systems may have lower anti-Sybil standards; import paths from low-cost external systems require explicit allowlist gating.

**A12 — Time-Bomb Vouch**
Mechanism: Attacker issues a vouch that appears valid at time T but encodes a delayed activation for future exploitation, or a vouch that degrades only after a credential is used to gain access, maximizing damage before detection.
Target property violated: Vouch temporal integrity; non-deception.
Defense: S175 vouch schema requires explicit validity window with no post-hoc extension; S179 revocation can be applied retroactively to a validity window, nullifying the vouch as if never issued.
Residual risk: Actions taken during the valid window before retroactive revocation cannot be unwound; retroactive revocation does not undo resource grants already delivered.

**A13 — Vouching-as-Spam**
Mechanism: Attacker floods the network with low-cost vouches targeting many principals to pollute the graph, degrade query performance, or obscure signal in the score distribution.
Target property violated: Graph legibility; query performance; signal-to-noise ratio.
Defense: S174 per-vouch micro-stake requirement rate-limits vouch issuance economically; vouch velocity caps per principal per epoch are enforced at the protocol layer.
Residual risk: If micro-stake cost is miscalibrated below spam-incentive threshold, high-volume actors can still pollute at acceptable cost.

**A14 — Reputation Laundering via Shell ZKACs**
Mechanism: A principal with poor reputation creates or acquires a shell ZKAC with pristine history, transfers operational context to the shell, and uses the shell's clean score while the original ZKAC is abandoned.
Target property violated: Accountability continuity; score non-transferability.
Defense: S174 ZKACs are non-transferable by design; operational context transfer is detectable via behavioral fingerprinting; shell ZKACs with no prior activity history trigger a provisional score cap until independent vouches accumulate.
Residual risk: Well-seeded shell ZKACs (pre-populated with legitimate vouches before the transfer) are difficult to distinguish from genuine new entrants.

**A15 — Conflict-of-Interest Non-Disclosure**
Mechanism: A vouch is issued by a principal with an undisclosed financial, familial, or organizational relationship to the vouchee, making the vouch informationally dependent rather than independent, without violating any protocol rule.
Target property violated: Vouch informativeness; relying-party trust calibration.
Defense: S175 vouch-type schema includes an optional conflict-of-interest declaration field; S185 corroboration challenges can probe for undisclosed relationships; verifiers are advised to apply discount to vouches lacking conflict-of-interest attestation.
Residual risk: Disclosure is self-reported and non-mandatory; undisclosed conflicts are undetectable without off-chain corroboration or behavioral signal.

---

*Calm 2026-05-20*
