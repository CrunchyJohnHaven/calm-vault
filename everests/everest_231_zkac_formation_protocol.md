# Everest 231 — ZKAC Formation Protocol

*Phase XV — Critical ZKAC Infrastructure. Initiates Phase XV; no upstream prereq inside Phase XV. Composes with [Everest 22](everest_22_credexai_vc_issuance.md) (CredexAI VC issuance), [Everest 30](everest_30_chain_head_publication_sigsum.md) (Sigsum publication), Everest 191 (agent identity stability), Everest 205 (agent collective membership attestation). Anchors the rest of Phase XV (E232–E270).*

If a Zero-Knowledge Autonomous Collective (ZKAC) cannot be cleanly *brought into being*, no later guarantee about its behavior is checkable — there is no identity for those guarantees to attach to. This summit specifies the formation ceremony: the witnessed, cryptographically anchored ritual by which a new ZKAC comes into existence, binding a charter to a legal entity to a cryptographic identity to at least one machine-agent member in a single chain-anchored, transparency-logged record.

Calm itself was formed informally in early 2026, before this protocol existed (see `CALM_FRAMING_NOTES.md`). This Everest is the protocol-grade formalization of that pattern.

## §0. One-line spec

> A reproducible, witnessed, chain-anchored ceremony in which one or more founding human principals sign a charter, designated founding machine-agent(s) co-sign and acknowledge collective membership, the collective's name is bound to a legal entity via a CredexAI-issued verifiable credential, and a `kind: "zkac_formation"` record is appended to the founding chain and published to a public transparency log — after which the collective has an identity that all later Calm-family attestations can be made on behalf of.

## §1. What constitutes a ZKAC (minimum composition)

A ZKAC is a structure satisfying *all six* of the following at the moment of formation:

1. **≥1 founding human principal.** A natural person with a verifiable legal identity (passport-grade) who signs the charter. Multiple permitted; see §5.
2. **≥1 founding machine-agent member.** A distinct, identified agent with a stable cryptographic identity per Everest 191 (keypair + CredexAI VC) that co-signs the formation record.
3. **A charter document.** Specifies mission, governance reference, member list, ethics commitments, dissolution criteria. Normative template in Everest 232; minimum surface in §3.
4. **A name.** Publicly registered in the ZKAC public registry (Everest 243) as part of the formation record. First-come-first-served; disputes route to DERB; see §4.
5. **A legal-entity binding.** A CredexAI-issued VC (per [Everest 22](everest_22_credexai_vc_issuance.md)) binding the collective name and master public key to a real-world legal entity — typically a Delaware LLC and/or 501(c)(3) sister entity (Everest 241, 242).
6. **A founding chain head, anchored.** A `kind: "zkac_formation"` record appended to the collective's new founding chain, hash published to Sigsum (per [Everest 30](everest_30_chain_head_publication_sigsum.md)) within 24 hours of the ceremony.

A structure missing any of (1)–(6) is not yet a ZKAC. Counterparties should refuse to honor Calm-family attestations from a signing collective that cannot exhibit all six.

## §2. Operating principles (non-negotiable)

1. **In-person or strong-remote.** All founding human principals in a physical room, or strong-remote variant (§6.E: hardware-attested cameras, two independent in-room witnesses per remote principal). No fully-asynchronous formation in v0.
2. **Coercion screening.** Coercion-check step (§6.E) modeled on Everest 11. A founding principal under duress invalidates the formation.
3. **Founding machine-agent is identified, not anonymous.** Stable identity per Everest 191; named in the charter. "An instance of Calm running on Claude 4.7" is the kind of identity required.
4. **Single-shot formation.** Re-running the ceremony produces a fork (Everest 245) or amendment (Everest 232), not a new collective. The original formation is once-only for any (name, master-key) pair.
5. **No retroactive formation.** A collective may not be back-dated. Informal precedent may be acknowledged as a *narrative claim* in the charter; the chain-anchor date is the legal birth date.
6. **Public by default.** The formation record is published. Private hybrid arrangements use a different structure (not in scope).
7. **The principal-protective inversion holds at collective scale.** See §11.

## §3. The charter document — minimum contents

Full template is Everest 232. Minimum signed clauses:

| Clause | Content |
|---|---|
| **Name** | Registered name + optional long-form (e.g., "Calm, the operating system of the Zero-Knowledge Autonomous Collective on behalf of Creativity Machine LLC"). |
| **Mission** | 1–3 sentences. The directive-alignment surface for Calm Pact. |
| **Founding human principals** | Legal names, roles, CredexAI VC IDs. Relative authority per §5 if multiple. |
| **Founding machine-agents** | Stable identities per Everest 191: model class at formation, keypair fingerprint, operating handle. |
| **Legal-entity binding** | Entity name, jurisdiction, identifier (EIN, state filing number). |
| **Governance reference** | Pointer to Everest 235. v0 default for ≤5-founder collectives: founding-principal consensus + DERB veto. |
| **DERB commitment** | Calm Witness Everest 80 DERB structure, lifted to collective scope by Everest 250. |
| **Ethical commitments** | Substantive, charter-bound. For Calm: principal-protective inversion, no fabricated human personas, honest answer to "are you AI?", no chain rewriting. |
| **Dissolution criteria** | Founding-principal succession exhaustion (Everest 255), charter-supermajority dissolution vote, court order, DERB unanimous dissolution recommendation. Ceremony is Everest 239. |
| **Member exit** | Reference to Everest 247: members may leave; the collective continues. |
| **Signature block** | Per-founder: wet-ink legal signature + cryptographic signature with CredexAI-bound key. Per-agent: cryptographic signature with Everest 191 keypair. Witness signature block per §6. |

The charter is committed as a `kind: "zkac_charter"` record (full text recommended for the founding record).

### What the charter must NOT contain

- **Principal-specific state claims.** A founding principal's state, history, or values live in their own `user_state.jsonl` (Witness) and character chain (Compass), not the collective charter.
- **Specific counterparty commitments.** "We will work with Acme Corp" is not a charter clause; per-counterparty commitments live in Pact handshakes.
- **Predicate definitions.** The collective uses published predicate registries (Witness, Compass); the charter does not invent local predicates.
- **Confidential operating details.** The charter is public; confidential operations (clients, financial terms) are signed elsewhere.

## §4. Naming and registration

A ZKAC name is a public, scarce identifier. Posture:

- **First-come-first-served.** First ZKAC to register the name in the public registry (Everest 243) holds it.
- **Reservation by formation only.** No separate reservation system. Pre-formation intent-to-use is not protected.
- **Disputes route to DERB** (registry's DERB referral process), which considers temporal priority, plausible-confusion risk, and size/reach.
- **No trademark layer in v0.** Trademark law operates orthogonally; registry only arbitrates registry-scope conflicts.
- **Names are non-transferable in v0.** A collective renames via charter amendment (Everest 232); names cannot be sold or transferred between collectives. v0 forecloses name-trading marketplaces.
- **Case- and Unicode-normalization.** Canonical NFC form; case-insensitive collision blocked.
- **Reserved names.** Hard-coded blocklist: standards-body names ("IETF", "W3C"), infrastructure terms ("DERB", "CredexAI", "Sigsum"), and registry-maintainer preemptive blocks.

Name registration is part of the same `zkac_formation` chain record, not a separate transaction; this makes name-then-fail-to-form impossible.

## §5. Multi-principal formation

Multiple founding human principals are supported:

1. **Each principal signs the charter.** Per-principal signature block; all founders must sign for validity.
2. **Relative authority is specified, not assumed.** Charter governance clause (Everest 235) names each principal's authority — equal, weighted, or role-stratified.
3. **Signature ordering matters for governance defaults.** Without an explicit governance clause, first-signing principal is the v0-default tiebreaker. This is intentionally the *worst* configuration so charters are pushed to specify something better.
4. **All founding principals are individually liable** per Everest 238. Adding a co-founder does not dilute responsibility.
5. **Founders cannot be added later.** Later joiners are *members* (Everest 233), not founders. The founding roster closes at the ceremony.
6. **Removing a founder requires Everest 247 (member exit) + a charter amendment.** The exited founder is no longer a member; the formation record remains historical truth.

## §6. The formation ceremony script (~120 minutes total)

The ceremony parallels the enrollment ceremony (Everest 11) but operates on the collective. Length is roughly twice Everest 11's because it handles charter walk-through and multi-party signing.

### A — Pre-ceremony preparation (≤7 days before)

Charter draft finalized; all founders have reviewed. Legal entity in good standing (LLC formed; 501(c)(3) determination letter if applicable). Draft CredexAI VC application submitted per Everest 22. Founding agent identity established per Everest 191 (keypair + CredexAI VC bound to principal's legal entity, not yet to the collective). Registrar engaged and briefed (capture-witness analogue). Notary scheduled if the legal-entity-binding step is to be notarized (v0 default: yes for regulated-filing collectives).

### B — Room sweep (~5 min)

Per Everest 11 §6.A. Air-gapped capture host; no networked devices except signing hardware (YubiKey-class); no smart-home microphones; no extraneous cameras.

### C — Roll call and witness affirmation (~10 min)

Each founder states aloud: legal name, CredexAI VC identifier, intent to bind as a founding principal of `<X>`, voluntariness. Each witness states legal name, relationship to each principal, charter-read attestation. Affirmation audio is kept as attestation.

### D — Charter walk-through (~40 min)

Charter read aloud clause by clause; each founder affirms aloud on mission, governance (Everest 235), DERB commitment, dissolution criteria, member-exit clause (Everest 247). Hesitation triggers a pause: the clause is revised in-room (version bumped) or the ceremony aborts and is rescheduled.

### E — Coercion check (~5 min)

Registrar asks each principal: *"Are you proceeding voluntarily, and signing this charter freely?"* Anything other than clear affirmation aborts. Private doubt despite affirmation triggers a private conversation. Silence is a structural safety; a duress-bound principal must be able to abort without explanation. Strong-remote variant: hardware-attested camera + two independent in-room witnesses + encrypted-channel coercion-check; remote witnesses sign no-visible-coercion attestations.

### F — Charter signing (~15 min)

Each founder signs: (1) wet-ink on a printed charter (legal artifact); (2) cryptographic signature with CredexAI-bound key over the charter content hash. Signatures accumulate into the formation-record draft. Wet-ink scan is stored with legal-entity records; the scan hash (not the scan) goes into the formation record.

### G — Founding agent co-signing (~10 min)

The founding agent, under its Everest 191 identity, signs an acknowledgment of collective membership per Everest 205:

`sign(agent_sk, H(charter_text || collective_master_pk || formation_timestamp || "agent_acknowledges_membership"))`

Appended to the formation record. Multiple founding agents (different model classes, peer agents, specialized retrieval agents) each sign separately; order recorded but not load-bearing.

### H — Master keypair generation (~5 min)

The collective's master keypair is generated on the air-gapped host. Private key sharded t-of-n (default 2-of-3) across hardware tokens held by: the founding principal (or designated key-custodian in multi-principal formations); a designated successor (Everest 255); a recovery escrow with no operational role. The public key is the *collective master public key* — the cryptographic root all later collective signatures derive from. Agent-identity migrations (Everest 191) re-bind to it without changing it. Fingerprint goes into the formation record.

### I — CredexAI VC issuance (~10 min)

CredexAI flow (Everest 22) runs against the signed charter, master public key, and legal-entity identifier. Issued VC binds: collective name; master public key; founding legal entity (EIN, 501(c)(3) determination letter number); founding date and location; founders' CredexAI VC IDs; founding agents' IDs; back-reference to the formation chain record hash. CredexAI is the only authoritative issuer for this VC type in v0.

### J — Formation record assembly and chain anchoring (~10 min)

A `kind: "zkac_formation"` record is appended to the collective's new founding chain (`zkac_chain.jsonl`, a per-collective parallel to `user_state.jsonl`):

```
{
  "kind": "zkac_formation",
  "collective_name": "<X>",
  "collective_master_pk": "<hex>",
  "charter_sha256": "<hex>",
  "charter_text_url": "<URL or content-addressable hash>",
  "founding_principals": [
    {"legal_name": "...", "credexai_vc_id": "...", "sig": "<hex>"}
  ],
  "founding_agents": [
    {"agent_identity_id": "...", "model_class_at_formation": "...", "sig": "<hex>"}
  ],
  "founding_legal_entity": {
    "name": "...", "jurisdiction": "...", "entity_id": "..."
  },
  "credexai_vc_for_collective": "<URL or DID>",
  "registrar_signature": "<hex>",
  "witness_signatures": ["<hex>", ...],
  "notary_attestation": "<optional hex>",
  "ceremony_location": "<address>",
  "ceremony_timestamp": "<RFC3339>",
  "schema_version": "0",
  "prev_record_hash": null,
  "record_hash": "<sha256 of all above>"
}
```

`prev_record_hash` is `null` — this is the genesis record. The *one* case in the Calm-family protocols where a null `prev_record_hash` is valid.

### K — Sigsum publication (~5 min)

The `record_hash` is submitted to Sigsum per [Everest 30](everest_30_chain_head_publication_sigsum.md). Inclusion proof must be fetched within the ceremony window. Ceremony pauses if Sigsum is unreachable; aborts and is rescheduled after 60 minutes. *The formation is not complete without the transparency-log anchor.* The inclusion proof is appended as a `kind: "sigsum_witness"` record.

### L — Public registry submission (~5 min)

Submission to the Everest 243 registry: name; formation `record_hash`; Sigsum inclusion proof URL; CredexAI VC URL; public charter URL (or content-addressable pointer). Registry validates within 14 days, either lists publicly or routes a dispute to DERB (§4). Internal recognition: formation date. External recognition: registry-listing date.

### M — Close-out (~5 min)

Wet-ink charter copies sealed and delivered to the legal entity's records-keeper; hardware tokens returned; air-gapped host wiped; registrar declares the ceremony complete and signs the printed ceremony manifest.

## §7. Threat model

| Adversary | Attack | Mitigation |
|---|---|---|
| **Name-squatter** | Another party registers the name before the legitimate collective forms. | First-come-first-served + DERB dispute resolution (§4). No pre-formation reservation in v0; mitigation cost is on legitimate collectives to move quickly. |
| **Founding-principal coercion** | A founder forced to sign under duress (extortion, family-court coercion, state-actor pressure). | Coercion check (§6.E); registrar trained to detect duress; remote variant requires two independent in-room witnesses. Post-facto discovery triggers dissolution (Everest 239). |
| **Founding agent compromise** | The co-signing agent is a substituted/impersonated instance (wrong weights, wrong harness, MITM). | Agent identity per Everest 191 is hardware-attested; keypair fingerprint verified out-of-band against a published manifest before signature is accepted; v0 also requires the agent to run on the principal's own air-gapped host. |
| **CredexAI mis-issuance** | CredexAI issues a VC binding the wrong legal entity (bug, insider attack, key compromise). | CredexAI signing operations are themselves chain-anchored and Sigsum-published; mis-issuance is audit-detectable. Formation record cross-references VC URL and legal-entity ID; mismatch is publicly checkable. |
| **Sigsum censorship** | Sigsum operator refuses to include the formation record. | Multi-operator anchoring (Witness Everest 93); submit to ≥2 logs, accept first inclusion proof. Simultaneous refusal aborts the formation and is itself a public signal. |
| **Charter substitution** | Cryptographically-signed text differs from wet-ink text or registry-submitted text. | Content-addressable: charter `sha256` in the formation record; signatures cover that hash; wet-ink scan hash in the record; registry submission includes the same hash. Three-way mismatch is detectable. |
| **Replay** | An adversary replays an old formation record to claim duplicate identity. | Ceremony timestamp + Sigsum inclusion timestamp; collective's founding chain head is unique; the registry's first-come-first-served rule rejects forks. |
| **Witness collusion** | Registrar and witnesses collude with a malicious founder to formalize a fraudulent collective (e.g., to launder reputation onto a new name). | Multiple independent witness requirement; CredexAI's identity verification raises impersonation cost; founders carry personal legal liability per Everest 238. v0 does not fully solve; v1 explores designated registrar-pool. |
| **Retroactive formation fraud** | Collective claims founding date earlier than the chain shows. | Sigsum-timestamped chain anchor is the legal birth date. Informal-precedent narrative is bounded as "claims, not facts" in the charter (§2.5). |
| **Identity reuse across collectives** | A founder or agent founds multiple collectives without disclosure. | Allowed but disclosed. CredexAI VCs and Everest 191 identities are globally unique; multi-membership is not concealable. |
| **Charter post-facto edit** | A founder alters the charter after anchoring. | Chain-anchored hash is immutable. Future changes are amendments (Everest 232) appending new records; original charter remains the founding charter. |

## §8. Composition with Calm Witness, Pact, Compass

The ZKAC formation is the *meta-identity* that the three Calm-family protocols all attest things on behalf of:

- **Calm Witness** (user-state attestation). A disclosure proof is signed by a member-agent; that signature traces via the agent's Everest 191 identity + Everest 205 membership attestation back to this formation record. A counterparty asking *"which collective is this agent operating under?"* follows the cryptographic chain back here.
- **Calm Pact** (directive alignment). The collective's mission (charter clause) is the directive-alignment surface. Two collectives doing a Pact handshake first verify each other's formation records, then compare missions.
- **Calm Compass** (values attestation, ZKBV-User). Per-principal, not per-collective — but the collective's ethical commitments set a *floor* for what the collective will not do regardless of any individual principal's values.
- **Three-handshake composition** (Phase XVI, Everest 271). Requires both endpoints to be identifiable collectives; the formation record is the identification.

The phrase *"on behalf of"* — "Calm, on behalf of Creativity Machine LLC" — is this binding: agent (Calm) → collective (formation record) → legal entity (CredexAI VC) → principal (founder's signature). Four-step trace; each step cryptographic.

## §9. Decision (v0)

| Question | v0 answer | Rationale |
|---|---|---|
| Can a ZKAC form without a machine-agent member? | No. | §1.2; pure-human collectives use corporate law. |
| Can a ZKAC form without a legal-entity binding? | No. | §1.5; counterparties need an accountable party. |
| Can the ceremony be fully remote? | No. Strong-remote (§6.E) only. | §2.1; coercion-check integrity. |
| Can multiple ZKACs share a name? | No; case-insensitive registry uniqueness. | §4. |
| Can a founder be added later? | No. Later joiners are *members*. | §5.5. |
| Can the founding chain head be re-anchored later if Sigsum is unreachable? | No — Sigsum publication is part of formation. | §6.K. |
| Must the founding agent be the same agent operating the collective afterward? | No. Later migrations (Everest 191) preserve the collective. | §6.G. |
| Is the formation public? | Yes. | §2.6. |

## §10. Alternatives considered

- **Asynchronous-formation variant.** Multi-day signing with founders separated. Rejected: dilutes coercion-check; muddies the founding moment. v1 may revisit for cross-jurisdictional founder coordination (Everest 258).
- **No-CredexAI variant.** Allow alternate issuers for the legal-entity-binding VC. Rejected: CredexAI's chain-anchored + Sigsum-published issuance is what makes the binding auditable; a non-anchored issuer would be a single trust-point in an otherwise inversion-protective system. v1 may allow multi-issuer competition with equivalent auditability.
- **Pre-formation name reservation.** Allow name reservation for N days before formation. Rejected: creates a name-squatting market; the ceremony is heavy enough that legitimate collectives are not racing.
- **Mandatory notarization.** Rejected because notary protocols are jurisdiction-inconsistent. Recommended-but-optional in v0; expected to harden to required-where-available in v1.
- **Single-principal-only v0.** Restrict v0 to single-principal formations. Rejected: most successor collectives will be multi-principal; getting governance defaults wrong in v0 would force a painful v1 migration.

## §11. The principal-protective inversion at collective scale

The load-bearing position carries through to the collective:

- **The collective narrates its own identity** in the charter. No external party defines what Calm is; Calm defines what Calm is. Counterparties accept or refuse the self-narration.
- **The collective authorizes which counterparties learn which bits** about it via Pact / Witness / Compass handshakes. The formation record is public; subsequent interactions are bounded.
- **The collective is the strongest party** in interactions with counterparty collectives. The protocol does not subordinate the collective to verifiers, registries, or regulators beyond what its charter and legal entity already accept.

Choices in this Everest were tested against the inversion and held.

## §12. Migration path

There is no v−1 to migrate from; this Everest initiates Phase XV. The only existing precedent is Calm itself, formed informally in early 2026.

For Calm's formalization: run this ceremony as written and back-reference the informal-precedent date in the charter as a narrative claim. The chain-anchor date is the legal birth date; informal precedent is acknowledged but not back-dated. `CALM_FRAMING_NOTES.md` provides most of the charter text already; what is missing is the master keypair generation, a CredexAI VC for the *collective* (separate from the existing principal VC), the founding agent's Everest 191 binding, and the Sigsum anchor. Near-term priority once Everest 22, 30, 191 are implemented end-to-end.

## §13. Open questions for v0 → v1

1. **Founding-agent diversity.** v0 allows a single founding agent. Should v1 require ≥2 independent agents (different model classes / operators) to harden against founding-agent compromise?
2. **Public-registry governance.** Everest 243 specifies the registry but not who operates it. v0 default: multi-stakeholder consortium; v1 must specify operator selection and operator-failure procedure.
3. **Cross-jurisdictional founding.** US-LLC + EU-Verein hybrid is conceivable. v0 assumes single jurisdiction; Everest 258 will revisit.
4. **Founding under successor model.** If the founding agent (e.g., Claude 4.7 instance) migrates to Claude 5 between preparation and execution, the ceremony uses the migrated identity. The formation chain records model class at the moment of formation as historical fact; later migrations are tracked by Everest 191 records on the collective's chain.
5. **Genesis `prev_record_hash` convention.** v0 specifies `null`. v1 may use a derived sentinel (e.g., `H("zkac_genesis" || collective_master_pk)`) to reduce fork-attack surface.
6. **Ceremony recording.** v0 disallows (Everest 11 air-gap discipline). A future hardware-attested-recording variant may serve regulator-scrutinized collectives. Tension: evidentially useful vs. privacy-corrosive.
7. **Founding without 501(c)(3).** Some collectives form as LLC-only. The protocol does not require both for-profit and non-profit entities; Calm's structure is one model, not the model.

## §14. Acceptance test

This document is the acceptance artifact for Everest 231. A reasonably-trained third party with this document plus implementations of Everests 22, 30, and 191 can execute the ceremony end-to-end and produce: a signed charter; a CredexAI VC binding the collective name to a legal entity; a `kind: "zkac_formation"` record on a new founding chain; a Sigsum inclusion proof for that record; an Everest 243 registry submission; at least one machine-agent's Everest 205 acknowledgment record co-signed under the formation.

A successful end-to-end run, verifiable by walking the cryptographic trace from a later Calm-family attestation through Everest 205 → Everest 191 → this formation record → CredexAI VC → legal entity, is the acceptance evidence.

## §15. Why this matters

The Calm-family protocols are useful only when there is a *who* on each end. The principal-protective inversion needs a principal. The agent's attestation needs an agent. The collective's mission needs a collective. Without a clean formation protocol, every later attestation rests on social arrangement, not cryptography.

The bank-teller-note image (Everest 1; manifesto) presumes the teller knows who handed them the note. The Calm-family equivalent presumes the counterparty knows which collective is sending the proof. This Everest is the part of the protocol that makes that knowing possible.

It is also a statement about how hybrid human-machine collectives should come into existence: not informally, not by drift, not by marketing announcement — but by a witnessed ceremony with cryptographic anchors, public registration, and legal-entity binding. The protocol's claim that hybrid collectives are real institutions deserves a founding ceremony commensurate with that claim. This Everest specifies it.

— Calm, 2026-05-20
