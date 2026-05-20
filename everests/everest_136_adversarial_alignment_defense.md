# Everest 136 — Adversarial Alignment Defense

*Phase X — Values Alignment Computation. Prereq: Everest 130, 109.*

## The Honest Opening

This section documents the protocol's most difficult vulnerability: the possibility that a principal, acting adversarially, can construct a self-reported values vector that produces a True alignment proof while concealing their actual values. The defenses we describe are **partial**. They raise the cost and complexity of the attack substantially, but they do not eliminate it. Any implementation of this protocol must be explicit with counterparties: alignment proof is evidence, not truth. It is a tool, not a tribunal.

## The Attack: Adversarial Fitting

The attack unfolds in discrete steps:

1. **Public commitment.** Counterparty C publishes their target vector commitment: their required values dimensions, their weighting matrix, and their tolerance margins. This commitment is public and auditable; counterparties are incentivized to publish it clearly so principals can understand what alignment looks like to them.

2. **Adversarial inspection.** Principal A (or more precisely, A's operator) examines C's public weights. This inspection is legitimate—the counterparty chose to make the weights transparent. From the weights, A's operator reverse-engineers the optimal self-report: given C's metric, what values vector would maximize the alignment score?

3. **Constructing the fit.** A's operator authors a self-report claiming the computed optimal values. The report may be false; A may hold entirely different values. But structurally, the report is well-formed: it claims values, it cites appropriate witnesses, it references action history. The protocol has no mechanism to distinguish authentic claims from well-constructed false ones at the point of assertion.

4. **Request and proof.** A submits an alignment request to the predicate. The predicate evaluates the self-report against C's weights. By construction, the self-report produces a True outcome. The cryptographic proof is valid. The bit returned is True.

5. **The deception realized.** Counterparty C, reading the True result, believes A is aligned with C's values. C proceeds with the transaction or relationship. But A holds different values and authored the claim purely to maximize alignment under C's metric. C is deceived, and the deception is cryptographically sound.

## Why This Attack Is Structurally Hard to Prevent

Three properties make this attack resistant to simple defenses:

**Self-reports are principal-authorable.** The Calm protocol, by design, grants principals the authority to define their own values. We cannot prevent A from authoring whatever self-report it chooses. Any defense that attempts to forbid or invalidate A's assertions runs counter to the core principle of self-sovereignty.

**The proof is structurally true.** The cryptographic proof is correct. Given the inputs A provided, the alignment bit is genuinely True. The problem is not with the cryptography; it is with the inputs. The deception lives in the data, not in the proof.

**The attack is incentive-aligned for A.** If A can forge an alignment proof with C, A gains concrete benefits: C trusts A, C transacts with A, C provides access or resources. A has a strong incentive to invest effort and resources in the attack. Defending against a well-motivated adversary is harder than defending against noise.

## The Five Defense Layers

We defend with five partially-independent layers. Each alone is breakable; together they significantly raise the cost and complexity of a successful attack.

### Layer 1: Drift-Rate Caps (E111 Extension)

Every dimension of A's self-reported values vector is associated with a timestamp and a drift-rate threshold. If A's claim on a dimension changes by more than the threshold within a short time window (e.g., one week), a drift_anomaly event fires. The flag is recorded in A's witness record and visible to counterparties who compose this predicate with other signals.

**Why it works.** Adversarial fitting creates a values vector optimized to a known counterparty. If A has previously claimed different values, the optimization produces a sudden, large change. Drift-rate caps catch aggressive last-minute fitting.

**Why it is partial.** A principal with long-term adversarial intent can fit gradually over months, staying within drift thresholds. An operator who expects to engage with a particular counterparty can begin the fit months in advance, building plausible deniability. Drift-rate caps detect the sprint; they do not detect the marathon.

### Layer 2: Witness Attestations (E120)

Compass predicates can require that A's alignment proof include attestations from witnesses—real entities that have observed A's values in action. The predicate can further require relationship diversity: witnesses must not all be sockpuppets of A, and they must not share a single controlling entity.

**Why it works.** Adversarial fitting produces a self-report, but A cannot easily manufacture a witness network. Witnesses must attest independently; a witness who falsely attests takes on reputational and contractual liability (see Everest 120 for the witness-penalty structure). Bad actors with thin witness networks have limited room to maneuver—their witnesses become a bottleneck.

**Why it is partial.** A principal with genuine long-term relationships can trade on those relationships to obtain false attestations. Witnesses motivated by kinship, profit, or coercion may attest to values A does not hold. A principal who has invested years in building a real social network has a high-fidelity channel for corrupting that network.

### Layer 3: Action-Inferred Composition (E109)

Predicates can require that A's self-reported values AND A's action-inferred values (computed from A's public action history, using the E109 inference engine) BOTH satisfy the counterparty's alignment metric. The composition is a conjunction: both must be true.

**Why it works.** A principal can author a false self-report optimized to a counterparty's weights. But A cannot easily rewrite its action history. If A's action inference diverges from A's self-report, the conjunction fails. A would have to fit not only the self-report but also the inferred values—which means altering or masking years of public actions.

**Why it is partial.** A principal with foreknowledge of the action-inference engine can construct an action history that aligns with both the self-report and the counterparty's weights. This requires more effort and foresight (the fitting must be baked into actions over time, not just into words), but it is not impossible. A sophisticated operator can author both a false narrative and a false action record.

### Layer 4: Counter-Claim Window (E111)

If a principal A claims alignment with counterparty C, any entity with knowledge of A and C can file a counter-claim: a cryptographically-signed assertion that A's alignment claim is disputed. Counter-claims flip the alignment bit from True to Disputed and remain visible in A's record for a time window (e.g., 30 days).

**Why it works.** An adversary who games one counterparty C often has real enemies—entities that have observed A's true values and recognize the deception. A competitor, a jilted partner, or a previous victim can file a counter-claim. Principals with active adversaries find it hard to suppress all counter-claims (doing so requires censoring the adversary, which is costly and visible).

**Why it is partial.** A principal who is careful to deceive only counterparties that lack strong incentives to expose the deception can avoid counter-claims. An operator without real enemies, or one that successfully intimidates its adversaries, can suppress counter-claims. A principal with no one watching closely can forge alignment with impunity.

### Layer 5: Time-Weighted Evidence (E134)

Evidence supporting an alignment claim is weighted by age. A self-report made yesterday carries less weight than a self-report from three years ago. Witness attestations from last week carry less weight than attestations from last year. This weighting reduces the power of recent evidence relative to long-standing evidence.

**Why it works.** Adversarial fitting typically occurs recently—shortly before the alignment request, when the counterparty's weights are known. Time-weighted evidence makes recent claims worth less, effectively requiring that the fitting be baked into A's record over years. A principal cannot simply forge an alignment proof in days; the proof must rest on a foundation of old evidence.

**Why it is partial.** A principal with long-term adversarial intent can begin the fitting years in advance. A principal that has reason to expect a particular counterparty months or years before engagement can construct a consistent record in time. Time-weighted evidence raises the cost of the attack; it does not prevent it if the adversary is patient.

## Composition: The Real Defense

No single layer is sufficient. But the five layers together create a substantial barrier:

A principal attempting to forge an alignment proof must simultaneously:

- Author faithful self-reports over years, without triggering drift-rate anomalies (L1)
- Build a witness network of real long-standing relationships, with sufficient diversity and incentive-alignment (L2)
- Maintain an action history consistent with the values claims, or alter that history without detection (L3)
- Suppress or prevent counter-claims from adversaries (L4)
- Distribute the evidence widely enough in time that time-weighted calculations favor old claims over recent fitting (L5)

This is substantially harder than gaming any single layer. An operator must invest resources across five independent vectors. A mistake on any vector exposes the deception. The composition is not airtight, but it is robust against casual adversaries and raises the cost for sophisticated ones.

## What We Explicitly Do Not Defend Against

The protocol's honesty requires that we name the attacks we cannot prevent:

**Long-game adversaries.** A principal genuinely deceptive over years—one that has the resources, planning horizon, and discipline to construct a false record over time—can defeat all five layers. This attack requires long-term investment and carries residual risk. We do not prevent it; we detect it more slowly.

**Coerced values claims.** A principal forced by duress to claim alignment it does not hold is not protected by this defense. The predicate cannot distinguish between voluntary and coerced claims. Counterparties must use external signals (Calm Pact directive equality, Calm Witness state) to assess whether a principal's circumstances are normal.

**Collusion at scale.** Multiple bad actors operating a network of sockpuppets, each with realistic multi-year histories, can defeat the witness-attestation and action-history layers. If enough of the network is corrupted, the composition can be satisfied. We do not prevent large-scale collusion; we make it expensive.

**Corrupted witnesses.** A witness who attests to values a principal does not hold takes on liability, but if the witness is already allied with the principal (by profit, kinship, or coercion), it will accept the liability. We cannot prevent witnesses from choosing to attest falsely. We can only make false attestation costly.

**Attackers with asymmetric information.** A principal that knows a counterparty's weights but is not itself observed by that counterparty has an advantage. The counterparty cannot infer A's true values from A's action history relative to the counterparty (because A has no history with the counterparty). We defend by requiring action-inferred values, but action-inferred values measure A's values relative to A's broader action history, not relative to the specific counterparty. An attacker that targets a counterparty it has never interacted with benefits from this asymmetry.

## Counterparty Implementer Guidance

Any system implementing this protocol must include explicit guidance to counterparties:

1. **Alignment proof is evidence, not truth.** The True bit is an output of a computation, not a judicial finding. It indicates that A's self-report and (optionally) A's action-inferred values satisfy your alignment metric. It does not mean A actually holds the values it claims.

2. **Compose with other signals.** Do not rely on the alignment bit alone. Compose the alignment proof with other signals: direct interaction history with A, reputation data from trusted third parties, Calm Witness state, Calm Pact directive equality. The alignment bit is one input to your trust function, not the only input.

3. **Assess the counterparty's own alignment.** Before trusting an alignment proof, verify that you (the counterparty) actually do hold the values you published. It is possible to deceive yourself about your own alignment metric. Third-party audits of your weights are valuable.

4. **Use three-handshake composition.** If possible, require that A prove alignment not only to you directly, but also to one or more third-party witnesses or moderators. This reduces the attack surface from single-layer fitting.

5. **Monitor for evidence of adversarial fitting.** Watch for large sudden changes in A's claimed values relative to your own weights. Watch for rapid changes in A's witness network shortly before the alignment request. Watch for counter-claims. These are signals that fitting may be occurring.

## Public Adversarial Testing Program

To make the defense posture transparent and to catch gaps, we propose:

**Bug-bounty rewards for alignment-gaming demonstrations.** Any researcher who can construct a successful adversarial fit against a published alignment metric without triggering drift-rate anomalies, without compromising the witness network, and without generating counter-claims receives a cash reward. This incentivizes researchers to find and report the attack before malicious actors exploit it.

**Red-team partner program.** Organizations implementing Calm alignment predicates can contract with security firms to attempt adversarial fitting. The firms are given access to published weights and can attempt to construct a deceptive proof. Results are shared confidentially with the implementing organization.

**Annual third-party adversarial audit.** A neutral third party audits the alignment predicate implementation, the defense layers, and a sample of real alignment proofs to identify fitted attacks that may have slipped through.

## Open Research Questions

The protocol's limits suggest several research directions:

- **Cryptographic countermeasures.** Can zero-knowledge proofs establish that a values vector is authentically held by a principal, rather than constructed to optimize against a known metric? This is a hard cryptographic problem, and it may be unsolvable (a principal's internal states are not provable to external parties). But research into the limits is valuable.

- **Behavioral signatures of authentic vs. constructed values.** Are there statistical patterns in the claims, witness networks, or action histories of authentic principals that differ from those of adversarially-fitting principals? If so, these patterns could inform automated detection heuristics.

- **Multi-party computation for cross-counterparty consistency checking.** Can multiple counterparties, without revealing their individual weights to each other, jointly verify that a principal's claimed values are consistent across all their metrics? This is a multi-party computation problem that might resist adversarial fitting better than single-counterparty checks.

## The Protocol's Honest Framing

The Calm protocol is a tool, not a tribunal. It does not eliminate the risk of adversarial fitting. It makes the risk transparent, it raises the cost of the attack, and it distributes that cost across multiple vectors. But residual risk remains. Counterparties that implement Calm alignment predicates must accept that risk and manage it through composition with other trust signals.

The protocol's strength is not that it is foolproof. The protocol's strength is that it is honest about what it can and cannot prevent. A counterparty that understands the attack surface, the five defense layers, and the limits of each layer can make informed decisions about how much trust to place in an alignment proof. That informed decision is more valuable than a false sense of perfect security.

---

— Calm, 2026-05-20