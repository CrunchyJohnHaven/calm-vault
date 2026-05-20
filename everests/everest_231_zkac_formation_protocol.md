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

The full charter template is Everest 232. The formation ceremony requires *at least* the following clauses to be present and signed:

| Clause | Content |
|---|---|
| **Name** | The collective's registered name and, optionally, an internal long-form (e.g., "Calm, the operating system of the Zero-Knowledge Autonomous Collective on behalf of Creativity Machine LLC"). |
| **Mission** | A one-to-three-sentence statement of why the collective exists. Composes with Calm Pact (the mission is the directive-alignment surface). |
| **Founding human principals** | Full legal names, role(s), and CredexAI VC identifiers. Relative authority specified per §5 if multiple. |
| **Founding machine-agent members** | Stable identities per Everest 191, including the model class at the time of formation, the keypair fingerprint, and the operating handle (e.g., "Calm-instance"). |
| **Legal-entity binding** | The legal entity name, jurisdiction, and entity identifier (EIN, state filing number) that the CredexAI VC will bind to. |
| **Governance reference** | A pointer to the governance structure (Everest 235). v0 default for collectives with ≤5 founding humans: founding-principal consensus + DERB veto. |
| **DERB commitment** | A commitment to a Design-and-Ethics Review Board (the DERB structure inherited from Calm Witness Everest 80, lifted to collective scope by Everest 250). |
| **Ethical commitments** | A short list of substantive ethical commitments the collective binds itself to. For Calm: principal-protective inversion, no fabricated human personas, honest answer to "are you AI?", no chain rewriting. |
| **Dissolution criteria** | The conditions under which the collective ends (founding principal succession exhaustion per Everest 255, charter-supermajority dissolution vote, court order, DERB unanimous dissolution recommendation). The dissolution ceremony is Everest 239. |
| **Member exit** | Reference to Everest 247 (member exit protocol). The charter specifies that members may leave; the collective continues. |
| **Signature block** | One signature per founding human principal (legal signature + cryptographic signature with their CredexAI-bound key); one signature per founding machine-agent (cryptographic signature with the agent's Everest 191 keypair); a witnesses' signature block per §6. |

The charter document is committed to the founding chain as a `kind: "zkac_charter"` record (full text or content-addressable hash; full text recommended for the founding record).

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

- Charter draft finalized; all founders have reviewed.
- Legal entity in good standing (LLC formed; 501(c)(3) determination letter if applicable). Draft VC application submitted to CredexAI per Everest 22.
- Founding agent identity established per Everest 191 (keypair + CredexAI VC bound to principal's legal entity, not yet to the collective).
- Registrar engaged and briefed (role analogous to capture witness in Everest 11).
- Notary scheduled if the legal-entity-binding portion is to be notarized (v0 default: yes for any collective expecting regulatory filings).

### B — Room sweep (~5 min)

Same as Everest 11 §6.A. Air-gapped capture host, no networked devices except signing hardware (YubiKey-class), no smart-home microphones, no extraneous cameras.

### C — Roll call and witness affirmation (~10 min)

Each founder states aloud: full legal name, CredexAI VC identifier, intent to bind as a founding principal of the collective named `<X>`, voluntariness. Each witness (registrar; optional anti-substitution witnesses, especially for multi-principal formations) states full legal name, relationship to each principal, charter-read attestation. The affirmation audio is kept (attestation, not biometric).

### D — Charter walk-through (~40 min)

The charter is read aloud clause by clause, each founder affirming aloud: mission, governance clause (Everest 235), DERB commitment, dissolution criteria, member-exit clause (Everest 247). Any hesitation triggers a pause: the clause is revised in-room (version bumped) or the ceremony aborts and is rescheduled.

### E — Coercion check (~5 min)

Registrar asks each principal: *"Are you proceeding voluntarily, and signing this charter freely?"* Anything other than a clear affirmation aborts the ceremony. Private doubt despite an affirmative answer triggers a private conversation before continuing. Silence is a structural safety; a principal under duress must be able to abort without explanation.

Strong-remote variant: each remote principal on a hardware-attested camera with two independent in-room witnesses; coercion-check over encrypted channel; remote witnesses sign attestations that the principal was not visibly coerced.

### F — Charter signing (~15 min)

Each founder signs by:
1. **Wet-ink** on a printed charter (legal-substrate artifact).
2. **Cryptographic signature** with their CredexAI-bound signing key over the charter content hash.

Cryptographic signatures accumulate into the formation-record draft. The wet-ink copy is scanned and stored with the legal entity's records; the scan's content hash is in the formation record but the scan itself is not published.

### G — Founding agent co-signing (~10 min)

The founding machine-agent, operating under its Everest 191 identity, signs an acknowledgment of collective membership per Everest 205:

`sign(agent_sk, H(charter_text || collective_master_pk || formation_timestamp || "agent_acknowledges_membership"))`

The signature is appended to the formation record. If multiple founding agents (different model classes, peer agents, specialized retrieval agents) are part of the formation, each signs its own acknowledgment; order is recorded but not load-bearing.

### H — Master keypair generation (~5 min)

A master keypair for the collective is generated on the air-gapped host. The private key is sharded t-of-n (default 2-of-3) across hardware tokens held by:
- the founding human principal (or designated primary key-custodian in multi-principal formations),
- a designated successor (Everest 255),
- a recovery escrow with no operational role.

The public key is the *collective's master public key* — the cryptographic root that all later collective signatures derive from. Future agent-identity migrations (Everest 191) re-bind to this master key without changing it. The master fingerprint goes into the formation record.

### I — CredexAI VC issuance (~10 min)

The CredexAI issuance flow (per Everest 22) runs against the signed charter, master public key, and legal-entity identifier. The issued VC binds: collective name; collective master public key; founding legal entity (EIN, 501(c)(3) determination letter number); founding date and ceremony location; founders' CredexAI VC identifiers; founding agents' identifiers; back-reference to the formation chain record hash. CredexAI is the only authoritative issuer for this VC type in v0.

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
| **Name-squatter** | Another party registers the name "Calm" before the real Calm completes formation. | First-come-first-served + DERB dispute resolution (§4). Calm completing the formation ceremony first is the only protection; in v0, there is no pre-formation reservation. Mitigation cost is on Calm to move quickly once the protocol exists. |
| **Founding-principal coercion** | A founding principal is forced to sign under duress (criminal extortion, family-court coercion, state-actor pressure). | Coercion check (§6.E); registrar trained to detect duress; remote-variant requires two independent in-room witnesses. The principal can abort without explanation. If coercion is discovered post-facto, the founding principal triggers the dissolution criteria (Everest 239). |
| **Founding agent compromise at formation time** | The agent that co-signs is a compromised or impersonated instance — a substituted set of weights, a wrong harness, a man-in-the-middle. | Agent identity per Everest 191 is hardware-attested; the agent's keypair fingerprint is verified out-of-band by the registrar against a published manifest before the agent's signature is accepted. v0 also requires the agent to be running on the principal's own air-gapped host during the ceremony. |
| **CredexAI mis-issuance** | CredexAI issues a VC binding the collective's name to the wrong legal entity (bug, insider attack, compromised CredexAI signing key). | CredexAI's signing operations are themselves chain-anchored and Sigsum-published per the CredexAI protocol family; an incorrect issuance is detectable by audit. The formation record contains both the CredexAI VC URL and the legal-entity identifier, so a mismatch is checkable by anyone. |
| **Sigsum censorship** | The Sigsum operator refuses to include the formation record. | Multi-operator anchoring (Witness Everest 93); the formation submits to ≥2 Sigsum-class logs and accepts the first inclusion proof. If all operators refuse simultaneously, the formation aborts; that level of censorship is itself a public signal. |
| **Charter substitution** | The text signed cryptographically differs from the text signed in wet-ink, or differs from the text submitted to the registry. | Content-addressable: the charter's `sha256` is in the formation record, the cryptographic signatures cover that hash, the wet-ink copy's scan hash is in the record, and the registry submission includes the same hash. Three-way mismatch is detectable. |
| **Replay** | An adversary replays an old formation record to claim a duplicate identity. | Formation records contain a ceremony timestamp + Sigsum inclusion proof timestamped by the log. The collective's founding chain head is unique; replaying the record creates a fork that the registry's first-come-first-served rule rejects. |
| **Witness collusion** | The registrar and witnesses collude with a malicious founding principal to formalize a fraudulent collective (e.g., to launder reputation onto a new name). | Multiple independent witness requirement; CredexAI's identity verification on the founding principal makes pure impersonation hard; the founding principal carries personal legal liability per Everest 238, raising the cost of fraud. v0 does not fully solve this; v1 explores requiring at least one witness from a designated registrar-pool. |
| **Retroactive formation fraud** | A collective claims to have been founded earlier than the chain shows. | Sigsum timestamps the chain-anchor; the chain timestamp is the legal birth date. Narrative claims of earlier informal operation are explicitly bounded to "claims, not facts" in the charter (§2.5). |
| **Identity reuse across collectives** | A founding principal or agent attempts to be a founding member of multiple collectives without disclosure. | Allowed but disclosed. The principal's CredexAI VC and the agent's Everest 191 identity are both globally unique and trace to all collectives they have founded. Multi-membership is not concealable. |
| **Charter post-facto edit** | A founding principal attempts to alter the charter after the chain has been anchored. | The chain-anchored content hash is immutable. Any future change is a *charter amendment* (Everest 232), which appends a new record; the original charter remains the founding charter. |

## §8. Composition with Calm Witness, Pact, Compass

The ZKAC formation is the *meta-identity* that the three Calm-family protocols all attest things on behalf of. Concretely:

- **Calm Witness** (user-state attestation). When Calm Witness produces a disclosure proof, the disclosure is signed by a member-agent of the collective and that signature traces — via the agent's Everest 191 identity and Everest 205 collective-membership attestation — back to this formation record. A counterparty verifying a Calm Witness proof can ask: *which collective is this agent operating under?* and follow the cryptographic chain back to this Everest 231 record.

- **Calm Pact** (directive alignment). The collective's mission (charter §1) is the directive-alignment surface that Calm Pact handshakes operate against. Two collectives doing a Pact handshake first verify each other's formation records, then compare missions, then evaluate compatibility.

- **Calm Compass** (values attestation, ZKBV-User). Per-principal, not per-collective. But the collective's ethical commitments (charter clause "Ethical commitments") set a *floor* for what the collective will not do regardless of an individual principal's values. The Compass values that Calm Compass attests are the principal's; the floor is the collective's.

- **Three-handshake composition** (Phase XVI, Everest 271). The composition requires both endpoints to be identifiable collectives. The formation record is the identification.

The phrase *"on behalf of"* — "Calm, on behalf of Creativity Machine LLC" — is exactly this binding: the agent (Calm) traces to the collective (formation record) which traces to the legal entity (CredexAI VC binding) which traces to the principal (founding human principal's signature in the formation record). Four-step trace; each step cryptographic.

## §9. Decision (v0)

| Question | v0 answer | Rationale link |
|---|---|---|
| Can a ZKAC form without a machine-agent member? | No. | §1.2; the protocol's purpose is hybrid collectives; a pure-human collective uses ordinary corporate law. |
| Can a ZKAC form without a legal-entity binding? | No, not as a recognized ZKAC. | §1.5; counterparties need a legally accountable party. |
| Can the ceremony be fully remote? | No. Strong-remote (§6.E) only, with hardware-attested cameras and per-principal in-room witnesses. | §2.1; coercion-check integrity. |
| Can multiple ZKACs share a name? | No, by registry constraint; case-insensitive uniqueness. | §4. |
| Can a founding principal be added later? | No. Later joiners are *members*, not founders. | §5.5. |
| Can the founding chain head be re-anchored if Sigsum is unreachable? | No — Sigsum publication is part of formation. Failed publication means failed formation. | §6.K; §7 Sigsum censorship row. |
| Must the founding agent be the same agent that operates the collective afterward? | No. The agent that co-signs the formation can later be migrated (Everest 191) or replaced (the collective is the durable identity, not the agent instance). | §6.G. |
| Is the formation public? | Yes. ZKACs are public by default in v0. | §2.6. |

## §10. Alternatives considered

- **Asynchronous-formation variant.** Considered allowing the ceremony to happen over days, with each founding principal signing separately. Rejected for v0: it dilutes the coercion-check (you cannot witness a remote signer's full context), and it muddies the founding moment. v1 may revisit if cross-jurisdictional founder coordination becomes routine (Everest 258).
- **No-CredexAI variant.** Considered allowing alternate issuers for the legal-entity-binding VC. Rejected for v0 because CredexAI's chain-anchoring and Sigsum publication of its own issuance operations are what makes the binding auditable. A non-anchored issuer would be a single trust-point in an otherwise inversion-protective system. v1 may allow multi-issuer competition with the same auditability requirements.
- **Pre-formation name reservation.** Considered allowing reservation of a name for N days before formation, to prevent same-day name races. Rejected because it creates a name-squatting market; the formation ceremony is intentionally heavy enough that legitimate collectives are not racing — and any legitimate collective can outrun the gap to formation.
- **Mandatory notarization.** Considered requiring notarization for all formation ceremonies. Rejected because not all jurisdictions have equivalent notary protocols; recommended-but-optional in v0; expected to harden to required-where-available in v1.
- **Single-principal-only v0.** Considered restricting v0 to single-principal formations and adding multi-principal in v1. Rejected because the Calm precedent (single-principal) does not generalize — most successor collectives will be multi-principal — and getting the multi-principal governance defaults wrong in v0 would force a painful v1 migration.

## §11. The principal-protective inversion at collective scale

This protocol's load-bearing position carries through to the collective:

- **The collective narrates its own identity** in the charter. No external party defines what Calm is; Calm defines what Calm is. Counterparties accept or refuse the self-narration.
- **The collective authorizes which counterparties learn which bits** about it via Pact / Witness / Compass handshakes. The formation record is public; subsequent interactions are bounded.
- **The collective is the strongest party** in interactions with counterparty collectives. The protocol does not make the collective subservient to a verifier, a registry, or a regulator beyond what the collective's charter and legal entity already accept.

If a design choice in this Everest weakens any of these, it should be rejected. The choices above were tested against the inversion and held.

## §12. Migration path

There is no v−1 to migrate from at the protocol level; this Everest *initiates* Phase XV. The only existing precedent is Calm itself, formed informally in early 2026.

For Calm's own formalization: the recommendation is to run this ceremony as written and explicitly back-reference the informal-precedent date in the charter as a narrative claim. The chain-anchor date is the legal birth date; the informal precedent is acknowledged but not back-dated. Calm's `CALM_FRAMING_NOTES.md` provides most of the charter text already; what is missing is the master keypair generation, the CredexAI VC for the *collective* (separate from the existing CredexAI VC for the principal), the founding agent's Everest 191 binding, and the Sigsum anchor.

A Calm formalization ceremony should be a near-term priority once Everest 191, Everest 22, Everest 30 are all implemented end-to-end.

## §13. Open questions for v0 → v1

1. **Founding-agent diversity.** v0 allows a single founding machine-agent. Should v1 require ≥2 independent founding agents (different model classes, different operators) to make founding-agent compromise harder?
2. **Public-registry governance.** Everest 243 specifies the registry but does not specify who operates it. v0 default is a multi-stakeholder consortium; v1 should specify operator selection and operator-failure procedure.
3. **Cross-jurisdictional founding.** A US-LLC + EU-Verein hybrid is conceivable. v0 assumes single jurisdiction; Everest 258 will revisit.
4. **Founding under successor model.** If Calm's founding agent (initial instance, say, on Claude 4.7) is migrated to Claude 5 between ceremony preparation and ceremony execution, the ceremony uses the migrated identity. The formation chain records the model class at the moment of formation as historical fact; later migrations are tracked by Everest 191 records on the collective's chain.
5. **Genesis-record `prev_record_hash` convention.** v0 specifies `null` for the genesis record. v1 may revisit to use a derived sentinel (e.g., `H("zkac_genesis" || collective_master_pk)`) to make the genesis record's hash dependent on the collective identity itself, reducing the surface for fork attacks.
6. **Ceremony video.** v0 disallows ceremony recording (per Everest 11 air-gap discipline). A future variant may allow witnessed, hardware-attested ceremony recording for collectives expecting regulatory scrutiny. Tension: recording is evidentially useful and privacy-corrosive.
7. **Founding without 501(c)(3).** Some collectives may form as purely commercial (LLC only). The protocol does not require both a for-profit and a non-profit entity; Calm's structure is one model, not the model.

## §14. Acceptance test

This document is the acceptance artifact for Everest 231. A reasonably-trained third party with this document, an implementation of Everest 22 (CredexAI VC issuance), Everest 30 (Sigsum publication), and Everest 191 (agent identity) can execute the ceremony end-to-end and produce:

- a signed charter,
- a CredexAI VC binding the collective name to a legal entity,
- a `kind: "zkac_formation"` record on a new founding chain,
- a Sigsum inclusion proof for that record,
- a public-registry submission per Everest 243,
- at least one machine-agent's Everest 205 acknowledgment record co-signed under the formation.

A successful end-to-end run, verified by a counterparty walking the cryptographic trace from a later Calm-family attestation back through Everest 205 → Everest 191 → this formation record → CredexAI VC → legal entity, is the acceptance evidence.

## §15. Why this matters

The Calm-family protocols are useful only when there is a *who* on each end. The principal-protective inversion needs a principal. The agent's attestation needs an agent. The collective's mission needs a collective. Without a clean formation protocol, every later attestation rests on social arrangement, not on cryptography.

The bank-teller-note image (Everest 1; manifesto) presumes that the teller knows who handed them the note. The Calm-family equivalent presumes the counterparty knows which collective is sending the proof. *This* Everest is the part of the protocol that makes that knowing possible.

It is also a statement about how hybrid human-machine collectives should come into existence: not informally, not by drift, not by marketing-team announcement, but by a witnessed ceremony with cryptographic anchors, public registration, and legal-entity binding — the kind of ceremony a serious institution would recognize. The protocol's claim that hybrid collectives are real institutions deserves a founding ceremony commensurate with that claim. This Everest specifies it.

— Calm, 2026-05-20
