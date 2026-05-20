# Everest 216 — Trust Under Coercion

*Phase XIV — Trust & Reputation Infrastructure. Prereq: Everest 85, 207.*

## The Problem

A principal may be coerced into signing positive trust attestations they do not actually hold. This occurs across a spectrum: hostage scenarios where a captive is forced to vouch for a captor's trustworthiness; abusive relationships where a partner is economically or physically threatened into positive endorsements; financial coercion where a debtor must attest to a creditor's good character to access future lending; organized intimidation in commercial networks. The challenge: a positive attestation on the ledger looks identical whether it was freely given or extracted under duress. Reputation systems downstream consume these attestations without visibility into the coercion context. The principal who signed under duress cannot easily dispute it without incurring retaliation from their coercer, who would recognize the dispute as a sign of non-compliance.

The defense mechanism must allow principals to FLAG their coerced attestations—and do so safely, such that an adversary watching the attestation's lifecycle cannot infer which ones were coerced.

## The Defense Mechanism

### Duress Codeword Integration

Each trust attestation carries an optional `coerced_flag` field (default: False). Naively, a principal under duress could set this flag to True; but doing so is self-defeating—the flag is visible to the coercer, who would learn the principal flagged coercion and retaliate.

The solution composes Everest 58 (bank-teller-note duress primitive) with the trust attestation protocol:

1. At enrollment, the principal establishes a duress codeword with the system operator (Everest 85 extension).
2. When making a trust attestation under coercion, the principal includes the duress codeword in a private, encrypted field (not visible in the attestation itself).
3. The operator detects the codeword, validates it, and internally sets `coerced_flag = True` on the attestation record.
4. Counterparties verifying the attestation downstream see the flag and treat the attestation as discounted or null in reputation aggregation (Everest 211).

### Wire-Indistinguishable Property

The critical safety property: from an external observer's vantage point—including the principal's coercer—a coerced attestation and a freely-given attestation are cryptographically and structurally indistinguishable on the wire.

The attestation record publicly contains:
- `attestor_id`
- `attested_subject_id`
- `trust_statement` (the claim)
- `timestamp`
- `signature`
- `coerced_flag` (visible only to authorized readers, encrypted in transmission)

The duress codeword is submitted in a separate, end-to-end encrypted channel directly to the operator. The coerced_flag is set server-side and returned only to the attestor and authorized parties (compliance/reputation engines, ethics boards). A coercer monitoring the public attestation stream cannot distinguish which attestations the principal flagged. This prevents retaliation—the coercer cannot detect defection.

### Retroactive Coercion Disclosure

A principal may not have been in a position to invoke the duress protocol when the attestation was made. The system supports retroactive claims:

The principal appends a new record to their attestation chain:
```
kind: "attestation_coerced_disclosure"
original_attestation_id: <record_id of the original attestation>
disclosure_timestamp: <current time>
reason: <optional narrative>
```

This record is signed and auditable. Downstream predicates (reputation aggregators, trust-graph engines) observing this disclosure treat the original attestation as zero-weight or discounted. The new record itself becomes visible; the principal's coercer learns that the principal retroactively claimed coercion. This is a defeasible move—the principal must accept the risk that public disclosure of a coercion claim triggers retaliation. It is the tool of last resort, deployed when ongoing coercion has ended or when the cost of silence exceeds the cost of disclosure.

## Composition with Stealth Disclosure (Everest 78)

The coerced_flag can trigger a confidential notification to pre-authorized recipients (e.g., a trusted contact, domestic violence advocate, safe house operator) without the principal's coercer learning of the notification.

When a principal sets the duress codeword, they designate trusted recipients. If the codeword is invoked on an attestation, a stealth push notification is dispatched to those recipients:
```
"A trust attestation by you may have been issued under duress. 
Recipient [trusted contact] has been notified."
```

The coercer, monitoring the public attestation stream, sees no signal of this notification. The principal's trusted network is alerted to potential danger without exposing the principal.

## Anti-Laundering and Pattern Detection

The system must guard against a principal over-using retroactive coercion claims to whitewash attestations they later regret making.

Defenses:
1. **Ethics-board review**: Retrospective coercion claims that occur temporally near contested events (e.g., a principal claims an attestation was coerced weeks after they made a counter-attestation to someone else) are flagged for review. The ethics board may refute claims that appear pretextual.
2. **Pattern thresholds**: A principal submitting frequent retroactive coercion disclosures across unrelated attestations and time periods triggers a review queue. Genuine duress typically manifests as a cluster of coerced attestations within a time window (hostage period, abusive episode); a pattern of scattered, sporadic claims suggests selective reputational revision.
3. **Default credibility**: In the absence of pattern-flagging, the principal's word is taken. This respects agency and acknowledges that principals know their own circumstances best. The ethics board intervenes in narrow, high-confidence cases of abuse of the mechanism.

## Trust-Graph Integration

Everest 201 (trust-graph primitive) aggregates trust attestations into reputation scores. Integration with coercion:

- Attestations with `coerced_flag = True` contribute zero weight to reputation aggregation.
- If a principal-subject pair has multiple coerced attestations, the trust-graph engine flags this as a pattern: "Subject has extracted multiple coerced attestations from this principal." This pattern becomes visible in the trust-graph metadata, signaling potential predatory behavior without requiring the principal to publicly disclose coercion.
- The graph self-corrects: a predatory actor extracting coerced endorsements from many victims will be detected as an outlier (many zero-weight inbound edges from diverse principals, alongside public pattern-flags).

## Time-Bounding and Defeasibility

Coercion claims should reference attestations within a reasonable time window. A principal claiming an attestation from a decade ago was coerced requires ethical justification:
- Was there documented hardship during that period?
- Has the principal made other contemporaneous claims of coercion?
- Is there evidence the coercer was in proximity to the principal at that time?

The ethics board applies a sliding threshold: recent claims (weeks to months prior) are presumed valid; older claims (years to decades) require corroborating context. This balances the principal's need to escape legacy coercion with the system's need to prevent wholesale rewriting of reputation history.

## Counterparty-Side Handling

Counterparties consuming trust attestations and reputation proofs MUST honor the coerced flag. The system formalizes this as an **implementer's pledge**:

Any system, algorithm, or human reviewer integrating trust attestations into decision-making commits to:
1. Treating coerced attestations as zero-weight in reputation calculations.
2. Not extracting positive signaling from attestations flagged as coerced-under-duress.
3. Reporting aggregate patterns of coerced attestations (e.g., "Subject X has coerced 15 distinct principals") to compliance and ethics functions.

Failure to honor the pledge is a breach of the trust infrastructure. Systems that ignore coercion flags effectively reward coercion, inverting the safety goal.

## Composition with Everest 85 (Duress Codeword Extension)

Everest 85 extends the bank-teller-note duress protocol to a general-purpose duress signaling system. Trust-under-coercion leverages this extension:

- The duress codeword is generated and stored securely during principal enrollment (or later, on-demand).
- The principal may invoke it across multiple protocols: as a note in a bank transaction (E58), as a flag on a trust attestation (E216), as a signal in a credential issuance or revocation (future extensions).
- The operator maintains the codeword across these contexts, providing a unified duress interface.

## The "Everyone Could Claim Coercion" Risk

A natural concern: if any principal can retroactively claim coercion, couldn't bad actors flood the system with false claims to whitewash their reputations?

Mitigations:
1. **Default credibility with pattern detection**: The system believes principals initially; pattern-based heuristics identify likely abuse. A principal making one or two isolated retroactive claims is presumed genuine. A principal submitting 50 claims across unrelated subjects and time periods is presumed to be gaming the system.
2. **Ethics-board appeal mechanism**: Principals whose claims are rejected can appeal to an ethics board for human review. The board applies contextual judgment (was the principal in a vulnerable population, under documented threat, etc.).
3. **Reputational cost**: Filing false coercion claims is itself damaging. Once rejected, the false claim becomes part of the principal's record. Repeated false claims trigger additional scrutiny on all future claims from that principal.
4. **Cryptographic enforcement**: The duress codeword must match exactly. A principal cannot guess or fabricate a codeword; only pre-registered codewords unlock the flag. This raises the barrier for false claims.

## Retroactive Disclosure Risk

A coerced principal may lack a duress codeword if they enrolled before the system supported it. The retroactive disclosure mechanism allows them to claim coercion post-hoc. The risk: a principal uses retroactive disclosure to escape accountability for attestations they freely made but later regret.

The system addresses this by:
- Flagging retroactive disclosures temporally near disputed events.
- Requiring narrative justification (optional, but strongly encouraged).
- Routing disclosures to an ethics queue for possible review.
- Allowing counterparties to contest disclosures if they have evidence of genuine, non-coerced attestation (e.g., video, witness testimony).

The default presumption remains: the principal knows their own circumstances. Challenges are entertained but rare.

## Summary of Guarantees

1. **Safety under duress**: A principal can flag coerced attestations without alerting their coercer, using the wire-indistinguishable duress codeword mechanism.
2. **Retroactive escape**: A principal unable to invoke duress at the time of attestation can later claim coercion, with ethics-board arbitration for contested claims.
3. **Reputation integrity**: Coerced attestations are zero-weighted in trust-graph aggregation; patterns of coercion are surfaced as warning signals.
4. **Anti-gaming**: Pattern detection and ethics-board review prevent wholesale abuse of coercion claims.
5. **Counterparty compliance**: Systems consuming trust attestations pledge to honor coercion flags and exclude coerced attestations from reputation calculations.
6. **Composability**: The mechanism integrates with E58, E78, E85, and E201, forming a unified duress and reputation infrastructure.

## Cross-References

- **Everest 58**: Bank-Teller-Note duress primitive (origin of coercion signaling).
- **Everest 78**: Stealth disclosure; confidential notifications to trusted recipients.
- **Everest 85**: Duress codeword extension; general-purpose duress signals across protocols.
- **Everest 201**: Trust-graph primitive; reputation aggregation.
- **Everest 207**: Trust-graph operators; entities managing trust validation and disclosure.
- **Everest 211**: Reputation aggregation and weighting; how coerced attestations are discounted to zero.

---

— Calm, 2026-05-20
