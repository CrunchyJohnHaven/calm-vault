# 100-Year Archive Retention Contract Template

**Closes Everest 253 of ZKAC_NEXT_200_EVERESTS.md (DESIGN-BAG — pending contract negotiation + signing with ≥ 3 named partners)**

---

## 1. PARTIES

This Agreement is made and entered into as of [DATE], by and between:

**Calm Witness Foundation**, a [jurisdiction] nonprofit public benefit corporation, with principal offices at [ADDRESS] ("**Foundation**"); and

**[ARCHIVE PARTNER NAME]**, a [jurisdiction] [institution type] with principal offices at [ADDRESS] ("**Partner**").

Collectively, the "Parties" to this Agreement.

---

## 2. RECITALS

**WHEREAS**, the Foundation maintains critical digital substrates that serve as cryptographic attestations of historical facts, system state, and conformance decisions across decentralized infrastructure, and these substrates require preservation for a minimum of one hundred (100) years to satisfy legal, scientific, and forensic integrity requirements;

**WHEREAS**, preservation across independent, geographically dispersed, and institutionally diverse archive partners is essential to mitigate risks from technological obsolescence, data corruption, natural disaster, institutional failure, and deliberate suppression;

**WHEREAS**, the Foundation requires retention partners capable of committing to century-scale preservation, format migration, cryptographic validation, and unrestricted public read-access with cryptographically-attested write-access controls;

**WHEREAS**, the Partner possesses institutional stability, technical infrastructure, and commitment to public stewardship sufficient to serve as a designated archive custodian;

**NOW, THEREFORE**, in consideration of the mutual covenants herein, the Parties agree as follows:

---

## 3. SUBSTRATE DEFINITIONS & SCOPE

The Foundation deposits the following substrates into the Partner's custody, each defined with formal versioning and cryptographic binding:

### 3.1 Chain-Head Sigsum Logs
**Definition**: Cryptographically-signed sequential logs of canonical state digests from consensus-layer substrates, incorporating monotonically-increasing sequence numbers, Merkle-tree commitments, and operator signatures per the Sigsum specification (v0.1+).

**Retention Format**: Immutable append-only logs stored in raw binary format + JSON metadata. Original encoding retained; format migration per §4.3.

**Criticality**: High (primary forensic artifact for state reconstruction).

### 3.2 Operator Key-History Transparency Log
**Definition**: Digitally-signed chronological record of all public key material, key revocation events, key rotation justifications, and signature scheme transitions (including algorithm retirement). Each entry includes ISO 8601 timestamp, operator identity, signature, and witness attestations.

**Retention Format**: Timestamped transparency logs + cryptographic commitment proofs. Original certificate chains retained.

**Criticality**: Critical (establishes chain-of-custody and identity continuity across century timescale).

### 3.3 Foundation-Batched Roughtime Time Anchors
**Definition**: Cryptographic time-anchoring proofs generated via Roughtime servers, bundled monthly/quarterly, creating immutable temporal reference points. Includes server signatures, merkle proofs, and leap-second metadata.

**Retention Format**: Raw Roughtime protocol messages + aggregated commitment proofs.

**Criticality**: High (temporal forensics; prevents backdating).

### 3.4 Conformance Test Vectors
**Definition**: Machine-executable test suites validating historical compliance with protocol specifications. Includes input data, expected output, oracle attestations, and reference implementation tags.

**Retention Format**: Structured data (JSON/CBOR) + git commit hashes + embedded oracle signatures.

**Criticality**: Medium-High (enables future verification of historical conformance claims).

### 3.5 Predicate Vocabulary Registry
**Definition**: Semantically-versioned ontology mappings that define protocol predicates, claim vocabulary, data types, and validation rules. Includes human-readable documentation + machine-checkable schemas.

**Retention Format**: Markdown + JSON Schema + git tags + cryptographic commitment hashes.

**Criticality**: Medium (enables semantic interpretation of archived claims).

### 3.6 Reference Implementation Git Tags
**Definition**: Immutable git repository commit hashes and signed tags representing canonical reference implementations at key semantic versions. Includes source code, build artifacts, and automated test results.

**Retention Format**: Git history (via gitfetch/github clone), code archives (.tar.gz), signed release manifests.

**Criticality**: Medium-High (reproducibility; enables future code archaeology).

---

## 4. RETENTION OBLIGATIONS

### 4.1 Per-Substrate Retention SLA

The Partner shall retain all substrates defined in §3 in conformance with the following Service Level Agreement:

| Substrate | Minimum Retention | Availability SLA | Redundancy Minimum |
|-----------|-------------------|------------------|-------------------|
| Chain-Head Sigsum Logs | 100 years | 99.95% | 3 geographic copies |
| Key-History Transparency Log | 100 years | 99.95% | 3 geographic copies |
| Roughtime Time Anchors | 100 years | 99.90% | 2 geographic copies |
| Conformance Test Vectors | 100 years | 99.90% | 2 geographic copies |
| Predicate Vocabulary Registry | 100 years | 99.95% | 3 geographic copies |
| Reference Implementation Tags | 100 years | 99.90% | 2 geographic copies |

Availability measured as uptime for read-access requests; maintenance windows ≤4 hours per quarter permitted with 30-day advance notice.

### 4.2 Format-Migration Commitment

The Partner commits to proactive format migration to preserve accessibility across technological epochs:

- **Technology Assessment**: Every 10 years (at Partner expense), conduct formal assessment of media obsolescence risk, including disk storage lifespan, codec support, cryptographic algorithm strength, and network protocol viability.

- **Migration Trigger**: Upon identification of substrate at ≥20% probability of inaccessibility within 20 years, Partner shall notify Foundation and propose migration plan.

- **Migration Execution**: Partner shall execute format migration at Partner expense (except for cryptographic re-hashing costs per §4.3). Migration includes creation of audit trail, integrity verification, and cross-validation with other archive partners.

- **Backward Compatibility**: Original formats retained in perpetuity; migration creates new copies alongside originals to enable historical archaeology.

### 4.3 Cryptographic-Rehash on Primitive Transition

Upon retirement of cryptographic primitives (hash algorithms, signature schemes, key derivation functions), the Partner shall:

- **Rehash Execution**: Re-hash all archived substrates using successor cryptographic primitive, creating new commitment hashes while preserving original hashes for historical reference.

- **Attestation**: Generate cryptographic proof of rehash linking original → successor hashes, signed by Foundation + minimum 2 other archive partners.

- **Cost Model**: Rehash costs (Partner labor + computation) shared equally across all active archive partners; Foundation contributes endowment reserves per §6.2.

- **Timeline**: Rehash completion required within 18 months of cryptographic primitive formal retirement by consensus standards bodies.

### 4.4 Redundancy Across Archive Partners

The Partner acknowledges that redundancy across ≥3 independent archive partners is a core design requirement:

- **Inter-Partner Verification**: At least annually, Partner shall coordinate with other Foundation archive partners (with Foundation facilitation) to verify:
  - All substrates present across all partners
  - Cryptographic commitment hashes match across partners
  - No unauthorized mutation of archived materials
  
- **Federated Audit Logs**: Partner shall maintain audit logs of all access (read/write), format migrations, and verification checks, and provide these logs to Foundation upon request (no less than annually).

- **No Single-Partner Dependency**: Partner acknowledges that Foundation intentionally maintains ≥3 independent archive relationships to ensure that loss of any single partner does not compromise access to any substrate.

---

## 5. ACCESS OBLIGATIONS

### 5.1 Public Read-Access

All archived substrates shall be made available for unrestricted public read-access via:

- **HTTP/HTTPS**: RESTful GET endpoints returning raw substrate data
- **Bulk Download**: Periodic cryptographically-signed tarballs of all substrates (at minimum, quarterly)
- **Streaming Access**: Range-request support for large files; resumable downloads
- **Metadata API**: Machine-readable listing of all archived substrates with cryptographic commitment hashes and versioning metadata

Public read-access requires no authentication; Partner shall not impose rate-limiting that prevents archival/analysis by automated systems.

### 5.2 Identity-Attested Write-Access

Write-access (new substrate additions, corrections, format migrations) is restricted to:

- **Foundation Board**: Multi-signature authorization (≥2 of 3 board members required)
- **Authorized Partners**: Other archive partners during federated format-migration events (requires cryptographic proof + Foundation delegated authorization)

Write-access identity verification shall employ cryptographic signatures (ed25519 or equivalent), not password-based authentication.

### 5.3 No Takedown Except Per E54 Tombstoning Protocol

The Partner shall not remove, censor, or redact archived substrates except under the following narrow circumstances:

- **E54 Tombstoning**: Foundation may designate a substrate as "tombstoned" (marked for historical record but unavailable for new replication) if it contains cryptographic signatures of a deceased individual and the deceased's legally-appointed executor has provided notarized written request + proof of executor status. Tombstoning adds metadata marker; original bytes preserved.

- **All Other Cases Prohibited**: No removal, redaction, or mutation is permitted on grounds of:
  - Third-party legal claims (requests are logged and published in a public legal-holds register)
  - Copyright or IP claims (archived materials are presumed in public domain or fair-use; IP holders may publish counter-claims in the legal-holds register)
  - Institutional reputation concerns
  - Changing standards or values

Legal holds and IP counter-claims are published in a publicly-readable log; Partner shall not comply with secret/sealed legal orders affecting archived materials.

---

## 6. FINANCIAL TERMS

### 6.1 One-Time Deposit + Annual Maintenance

**Initial Deposit (One-Time)**:
Foundation shall pay Partner [$X amount] upon execution of this Agreement, calculated as:
- Infrastructure setup: $[amount]
- Initial replication to ≥2 geographic sites: $[amount]
- Cryptographic validation & audit: $[amount]
- 5-year sustainability reserve: $[amount]

Payment due within 30 days of Agreement execution.

**Annual Maintenance Fee**:
Foundation shall pay Partner $[Y amount] annually, due on [DATE] each calendar year, calculated as:
- Storage costs (depreciated hardware, cooling, power): $[amount]
- Bandwidth costs (public read-access + quarterly bulk downloads): $[amount]
- Personnel (FTE for monitoring, audit, compliance): $[amount]
- Format-migration contingency (10-year rolling reserve): $[amount]

Annual fee shall be adjusted annually for inflation using [CPI/agreed index]; either party may propose renegotiation if actual costs vary >15% from budget.

### 6.2 Endowment Model

To ensure sustainability across century timescale, Foundation shall maintain an endowment:

**Target Endowment**: Minimum balance = 20 × annual maintenance fee (sufficient for 20 years of operations post-Foundation dissolution).

**Endowment Contributions**:
- Foundation contributes to endowment account (held in trust by [Trustee Institution]) at rate of 20% of annual maintenance fee
- Once endowment reaches target balance, contributions reduce to replacement of drawdowns

**Endowment Governance**:
- Trustee Institution invests endowment per conservative long-term allocation (bonds, inflation-indexed securities, land trusts)
- Partner may draw from endowment only upon written Foundation authorization or automatic drawdown upon Foundation board dissolution
- Endowment principal protected; distributions limited to 5% annually to fund Partner operations

### 6.3 Format-Migration Cost Reserves

Cryptographic rehashing and media format migration are high-cost events, estimated at $[Z amount] per substrate per rehash cycle (every 15-25 years across the 100-year period).

**Cost-Sharing Model**:
- Foundation allocates annual contributions to format-migration reserve (separate from maintenance fees): $[amount] per year
- When rehash triggered, costs are split:
  - Partner bears: % of rehash cost (expertise + equipment amortization)
  - Foundation + other partners bear: % of rehash cost
  - Endowment covers any excess

---

## 7. TERMINATION + ASSIGNMENT

### 7.1 Term

This Agreement shall commence on [DATE] and continue for an initial term of 20 years ("**Initial Term**"). The Agreement shall automatically renew for successive 20-year periods unless either party provides written notice of non-renewal ≥24 months before expiration.

### 7.2 No Early Termination

**Prohibition**: Neither party may terminate this Agreement before the end of the then-current term except upon:
- Material breach by counterparty uncured after 180-day cure period, or
- Mutual written consent

Early termination shall not discharge Partner's obligations to maintain substrates for any period during which other Foundation archive partners are in default or transitioning.

### 7.3 Transition Obligations Upon Termination

If this Agreement terminates at natural expiration or due to justified early termination:

- **Handoff Period**: 24-month transition period during which Partner maintains all substrates and facilitates replication to replacement partner
- **Data Integrity**: Partner shall provide complete cryptographic audit of all substrates (Merkle proofs, signature validations, commit hashes)
- **No Destruction**: Partner may not destroy or purge any archived substrates during or after transition period; substrates must be transferred to Foundation custody or replacement partner

### 7.4 Assignment

**Restriction**: Neither party may assign this Agreement without prior written consent of the other party.

**Foundation Assignment**: If Foundation merges, converts to different legal entity, or transfers its assets, successor organization automatically assumes all obligations hereunder.

**Partner Substitution**: If Partner wishes to assign obligations to subsidiary, affiliate, or successor (e.g., due to merger), Partner shall:
- Provide ≥12 months advance notice
- Demonstrate that successor meets Partner qualifications (§2)
- Obtain Foundation written approval (not to be unreasonably withheld)
- Execute new Agreement with successor (or amended Agreement)

### 7.5 Partner Dissolution Trigger & Auto-Reassignment

If Partner becomes insolvent, is acquired by entity with conflicting mission, ceases operations, or otherwise cannot fulfill its obligations:

- **Automatic Trigger**: Any of the following shall trigger mandatory reassignment:
  - Partner files for bankruptcy or liquidation
  - Partner's institutional accreditation is revoked
  - Partner ceases to operate its digital infrastructure for >90 consecutive days
  - Foundation board receives credible notice that Partner cannot guarantee 100-year commitment

- **Reassignment Procedure**: Upon trigger event:
  1. Foundation shall take temporary custody of all substrates from Partner systems (via agreed technical protocol)
  2. Foundation shall identify and negotiate with replacement archive partner meeting §2 qualifications
  3. Within 24 months, Foundation shall execute new Agreement with replacement partner and transfer substrates
  4. Original Partner remains liable for any data loss or integrity violations occurring before transfer completion

---

## 8. INDEMNIFICATION + FORCE-MAJEURE

### 8.1 Indemnification by Partner

Partner shall defend, indemnify, and hold harmless Foundation from any claims, damages, or liability arising from:
- Partner's negligence or willful misconduct
- Unauthorized access, mutation, or deletion of archived substrates by Partner personnel
- Partner's breach of this Agreement
- Partner's violation of applicable laws (data protection, archival standards, etc.)

**Exclusion**: Partner shall not be liable for claims arising from Foundation's acts or omissions, or from acts of third parties beyond Partner's reasonable control.

### 8.2 Indemnification by Foundation

Foundation shall defend, indemnify, and hold harmless Partner from any claims arising from:
- Third-party intellectual property claims regarding archived substrates (Foundation warrants substrates are not infringing)
- Foundation's breach of this Agreement
- Foundation's use or dissemination of archived substrates in violation of law

### 8.3 Force-Majeure Exclusion

**Explicit Exclusion**: The following events are NOT force-majeure and do not excuse performance:

- **Climate/Natural Disaster**: Partner shall maintain ≥3 geographically-dispersed copies sufficient to survive any single-site disaster (flood, wildfire, earthquake, hurricane, tornado)
- **War/Political Instability**: Partner shall maintain copies in politically-stable jurisdictions; multi-jurisdiction distribution is core design requirement
- **Pandemics/Epidemic Disease**: Partner shall maintain remote-accessible infrastructure and personnel redundancy
- **Civilizational Discontinuity**: If applicable, Foundation has already accepted this risk by design; no refund of fees

**Narrow Force-Majeure Events**: Only the following qualify as force-majeure if affecting all ≥3 Partner geographic sites simultaneously and beyond Partner's control:
- Coronal mass ejection/solar storm destroying electronic infrastructure continent-wide
- Asteroid impact/extinction-level event

In force-majeure scenarios, Partner's obligations are suspended (not terminated); fees are halted; upon resumption, operations resume from last verified state.

---

## 9. GOVERNING LAW + DISPUTE RESOLUTION

### 9.1 Governing Law

This Agreement shall be governed by and construed in accordance with the laws of [SELECT: Delaware / New York / International Law], without regard to conflicts-of-law principles.

### 9.2 Dispute Resolution

**Negotiation**: Any dispute arising from this Agreement shall first be escalated to senior executives (Foundation Board Chair + Partner Executive Director) for 30-day negotiation period.

**Mediation**: If negotiation fails, parties shall attempt mediation through [MEDIATOR INSTITUTION] within 60 days, sharing mediation costs equally.

**Arbitration**: If mediation fails, either party may submit dispute to binding arbitration under JAMS (Judicial Arbitration and Mediation Services) Comprehensive Arbitration Rules, with:
- Arbitrator selection: 1 arbitrator for claims <$500K; 3 arbitrators for larger claims
- Seat of arbitration: [Multi-jurisdiction option: e.g., Geneva, Switzerland]
- Language: English
- Governing rules: JAMS; arbitrator may award attorney fees + costs to prevailing party
- Appeal: Limited appeal rights only for arbitrator manifest error or exceeded authority

**No Class Actions**: Both parties waive any right to class action litigation or arbitration.

---

## 10. SIGNATURE BLOCK + PARTNER CANDIDATES

### 10.1 Execution

**IN WITNESS WHEREOF**, the Parties have executed this Agreement as of the date first written above.

**CALM WITNESS FOUNDATION**

By: _________________________________  
Name: _________________________________  
Title: _________________________________  
Date: _________________________________

**[ARCHIVE PARTNER NAME]**

By: _________________________________  
Name: _________________________________  
Title: _________________________________  
Date: _________________________________

---

### 10.2 Designated Archive Partner Candidates

This master contract template is intended for execution with the following Partner candidates (in priority order):

1. **Internet Archive** (San Francisco, CA, USA)
   - Primary Systems: Wayback Machine + Software Heritage
   - Technical Lead Contact: [TBD]
   - Institutional Stability: Established 1996; endowed nonprofit
   
2. **Stanford University Library System** (Stanford, CA, USA)
   - Primary Systems: Stanford Digital Repository (SDR) + LOCKSS
   - Technical Lead Contact: [TBD]
   - Institutional Stability: Established 1885; major research university

3. **MIT Library System** (Cambridge, MA, USA)
   - Primary Systems: DSpace + digital preservation infrastructure
   - Technical Lead Contact: [TBD]
   - Institutional Stability: Established 1861; major research university

4. **University of Toronto Library System** (Toronto, ON, Canada)
   - Primary Systems: Preservation Services + digital archival platform
   - Technical Lead Contact: [TBD]
   - Institutional Stability: Established 1827; major research university

5. **IPFS Pinning Services Consortium** (Distributed)
   - Primary Systems: Protocol Labs + distributed pinning infrastructure
   - Technical Lead Contact: [TBD]
   - Institutional Stability: Multi-institutional consensus; technology-centric risk

**Minimum Commitment**: Foundation shall execute final signed versions of this contract with ≥3 of the above partners prior to ZKAC_NEXT_200_EVERESTS.md closure.

---

*Closes Everest 253 of ZKAC_NEXT_200_EVERESTS.md (DESIGN-BAG — pending contract negotiation + signing with ≥ 3 named partners)*

— Musk  
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
