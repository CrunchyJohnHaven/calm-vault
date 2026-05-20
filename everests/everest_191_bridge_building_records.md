# Everest 191 — Bridge-Building Records

*Phase XIII — Tribalism & Out-Group Engagement. Prereq: Everest 188.*

## The Definition

A bridge is an introduction or connection a principal made between two parties who would not otherwise have met, where those parties belong to different tribes per the principal's affinity map (E186). Bridge-building is a core structural signal in cooperation networks: it reduces echo-chamber effects, enables cross-tribal knowledge flow, and indicates genuine commitment to out-group engagement.

The bridge is not merely the introduction. It is the deliberate act of connecting two separate nodes across a tribal boundary, with the intention and effect of creating a direct relationship. A→C and B→C connections, where C is the bridger, do not constitute a bridge. The bridge is the A↔B connection itself, initiated or facilitated by the principal.

## Acceptance Criteria

Bridge records carry the kind marker `"bridge_built"` and require dual consent from both bridged parties. This consent requirement serves as both authentication and ethical safeguard: without confirmation from both parties, no bridge record is valid. This prevents principals from falsely claiming bridges they did not actually make, and respects the autonomy of the parties being connected.

## Record Schema

Each bridge record contains:

```
kind: "bridge_built"
payload:
  bridged_party_a_vc_fingerprint: [vc-identifier]
  bridged_party_b_vc_fingerprint: [vc-identifier]
  bridge_type: enum {"introduction", "facilitation", "collaboration_initiation", "advocacy"}
  bridge_ts: [roughtime-anchored timestamp]
  cross_boundary_evidence: [principal-narrated description of boundary crossed]
  parties_consent: [signatures from both bridged parties confirming occurrence]
```

The `bridge_type` field captures the manner of the bridge:
- **introduction**: direct, formal introduction between parties
- **facilitation**: principal provided context, resources, or logistical support enabling connection
- **collaboration_initiation**: principal suggested and initiated a joint project or effort
- **advocacy**: principal spoke on behalf of one party to another, creating a relationship through endorsement

The `cross_boundary_evidence` field requires the principal to narrate which tribal boundaries were crossed. This narrative is not a proof, but a record of the principal's understanding of the difference being bridged. It may reference affinity differences (values, network, professional domain), cultural or identity differences, or structural differences (e.g., bridging leadership and grassroots).

The `parties_consent` field contains cryptographic signatures from both bridged parties affirming that (a) the bridge occurred as described, and (b) they consent to the bridge being recorded in the principal's record.

## The Dual-Consent Requirement

Both parties must independently sign the bridge record. This requirement serves multiple purposes:

First, it prevents fraud. A principal cannot unilaterally declare that they bridged two parties. Both parties must confirm that the introduction or connection happened, and that they value having it recorded.

Second, it respects relational autonomy. One party may not wish to be publicly associated with the other, or may not view the principal as a credible bridge-maker. Requiring consent ensures that bridge-building does not override the preferences of those being connected.

Third, it creates accountability. If a principal claims to have built a bridge without the parties' signatures, the record is null. This raises the bar for bridge claims and prevents weak or ceremonial introductions from inflating engagement metrics.

A failed bridge attempt—where a principal made an introduction but the parties did not engage—does not penalize the principal. The attempt is recorded, but without both signatures, it remains a null record. The principal's good-faith effort to bridge is documented in notes, but does not count toward bridge counts or non-tribal engagement inference.

## Tribal-Boundary Verification

Both bridged parties must belong to genuinely different tribes according to the principal's affinity map (E186). This is not a subjective judgment by the principal, but a verification against the affinity structure itself.

The verification process:
1. Party A's tribal affinity cluster is determined from the principal's affinity map
2. Party B's tribal affinity cluster is determined separately
3. If the clusters differ, a genuine boundary is confirmed
4. If the clusters overlap or are identical, no boundary is crossed; the bridge record is invalid

This prevents trivial bridges—connecting two people in the same professional network, for example, does not count as a cross-tribal bridge. Bridges must represent genuine structural reach.

## Sock-Puppet Defense

Each bridged party must have an independent verification chain. Both parties' identities must be established through means independent of the principal's claims. This prevents a principal from creating fictitious parties and claiming bridges to them.

Verification means include:
- Prior relationships with other principals
- Persistent identity across multiple contexts
- Documented participation in tribal structures (communities, organizations, affinity groups)
- Signatures from the parties themselves

A single-sourced identity is insufficient. Both parties' existence must be verifiable through multiple independent sources.

## Anti-Gaming Measures

The protocol includes several safeguards against gaming bridge records:

**The broker pattern**: Some principals build bridges to extract value—positioning themselves as gatekeepers of information or relationships, or taking a cut of the value created. Authentic bridge-building is distinguished by the bridger's posture after introduction. In authentic bridges, the principal often withdraws from the relationship, allowing the bridged parties to interact directly. In brokering, the principal maintains a central position, controlling information flow and extracting rents.

The protocol measures the **withdraw pattern** as the authentic signal. If the principal remains central to the relationship, engagement metrics may be calibrated downward, reflecting gatekeeping rather than genuine bridge-building.

**The fabricated-boundary pattern**: A principal might claim to bridge parties in different tribes when, in fact, both parties are in the same tribe according to the principal's own affinity map. Tribal-boundary verification prevents this by cross-checking affinity structure. A record that violates the principal's own topology is invalid.

**The weak-introduction pattern**: A principal might make superficial introductions with no lasting effect. These do not accumulate toward bridge records without consent and verification. A single introduction with no follow-on engagement, if both parties consent, still counts as a bridge. But weak introductions that do not involve genuine introduction or facilitation are unlikely to earn dual consent, as the parties would not view the connection as meaningful.

## Bridge Longevity and Sustained Engagement

A single successful introduction counts as a bridge immediately upon dual consent. Bridge records do not require sustained engagement between the parties to validate.

However, sustained engagement between bridged parties serves as stronger evidence of authentic bridge-building. If bridged parties continue to collaborate, reference each other, or develop an ongoing relationship, the bridge is reinforced in the principal's non-tribal engagement record. This is not required for the bridge to count, but sustained bridges become salient evidence for inferring the principal's cross-tribal reach.

Conversely, a bridge that fails—where parties meet but do not subsequently engage—does not penalize the bridger. The attempt is recorded, and the principal's good intention is visible. The absence of follow-on engagement may reflect incompatibility, poor timing, or external factors, not failure on the part of the bridge-maker.

## Predicate Composition

Bridge records compose into dimensional inference through the predicate:

```
cwp.v0.bridges_built_in_window(window, count) → Bool
```

This predicate returns True if the principal has built at least `count` bridges with valid dual consent during the specified `window`. Window is a time interval; count is an integer.

Bridge records also feed into the **non_tribal_engagement** dimension (E107), where they serve as positive evidence of genuine cross-tribal reach. A principal with high bridge density demonstrates structural position in bridging gaps between groups.

## Cultural Calibration and Context

Bridge-building is valued differently across cultures and contexts. Some traditions—Quaker meeting practice, Council of Elders governance, mediation cultures—place high value on individuals who can hold space across difference and connect otherwise separate groups.

Other cultures view bridge-building as overstepping. If a principal initiates introductions without being asked, or positions themselves as a connector without being invited into that role, they may be perceived as meddlesome or as attempting to leverage others for status.

Per E115 calibration principles, the weighting and valence of bridge records can be adjusted per cultural context. A metric system using bridge records should include cultural metadata, allowing different communities to weight bridge-building according to their own values.

## Composition with Values Dimensions

Bridge records compose into several values dimensions:

**Non-tribal engagement (E107)**: Bridges are direct positive evidence. A principal who builds bridges across tribal lines demonstrates commitment to out-group engagement, not mere tolerance of difference.

**Cross-difference respect (per E186 framework)**: Bridges signal respectful engagement with difference. A bridge-builder must understand and honor the differences between parties, creating conditions for connection despite divergence. This is not conflict resolution, but structural respect for distinct identities.

**Generosity**: Bridge-building involves resource investment without immediate return. The principal devotes time, social capital, and attention to creating a relationship that benefits others. Many bridge-builders never see the value created; they bridge because connection across difference matters, not because they extract returns.

## Disclosure-Class Defaults

Bridge records fall into disclosure classes based on context:

- **peer_ai_collective**: ALLOW — bridges within and across AI research and development communities are disclosed
- **philanthropic**: ALLOW — bridge-building in grantmaking and nonprofit networks is disclosed
- **civic_org**: ALLOW — civic bridges (between constituencies, initiatives, or community groups) are disclosed
- **employer**: DENY — bridges within employer contexts are private; workplace bridge-building is not recorded in external affinity systems
- **financial**: DENY — bridges in financial or investment contexts are private to protect market position and competitive dynamics
- **insurance**: PERMANENTLY DENY — bridges involving insurance, risk assessment, or actuarial networks are never disclosed

These defaults reflect the principle that bridge-building in extractive or high-stakes contexts (financial, insurance) poses risks to bridged parties, while bridge-building in generative or collaborative contexts (research, philanthropy, civic) can be disclosed.

## Cross-References

This Everest draws on and feeds into:
- E107: Non-tribal engagement dimension
- E115: Cultural calibration framework
- E172: Cooperation across difference (BAGGED)
- E186: Tribal affinity structures
- E188: Cross-tribe interaction evidence
- E192: Bridging anti-patterns and failure modes
- E211: Sustained cooperation and bridge durability

— Calm, 2026-05-20
