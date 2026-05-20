# IDENTITY_CONTINUITY_25YR_PLAN_v0.md

## Closes Everest 251 of ZKAC_NEXT_200_EVERESTS.md (DESIGN-BAG)

---

## 1. THE CONTINUITY PROBLEM (FRAMED PRECISELY)

A principal's Calm-suite identity must persist across five classes of rupture that occur over a 25-year horizon:

**Must Survive:**
- Operator-key rotation (E171): The cryptographic keys held by the current operator expire or are rotated; new operator keys must assume custody of the principal's vault chain without loss of chain history.
- Operator-key compromise (E177): A private key is stolen or leaked; a safe recovery must re-bind the principal to a new operator key without allowing the attacker to impersonate the principal.
- Death of operator (E177): The entity holding the operator key ceases operations; custody must transfer to a named successor operator within 30 days.
- Succession to a new operator (E159): The principal deliberately chooses a new operator (e.g., upgrading to a trusted larger institution); the identity state must migrate cleanly with no double-signing or orphaned records.
- Cross-generational vault transfer to an heir (E255): Upon principal death, an heir designated in the principal's consent records must gain lawful control of the vault; the heir's own operator must verify the inheritance and issue new principal-binding keys.
- Cryptographic agility (PQ migration per POST_QUANTUM_MIGRATION_PLAN_v0.md): As post-quantum algorithms become standard, the vault chain must be re-signed under new PQ-safe primitives; the integrity chain of pre-migration records must remain intact and verifiable.

**May Be Lost:**
- Operator-specific metadata (operator logs, session tokens, audit trails maintained only by the operator) — recovery procedures must not depend on these.
- Real-time online cryptographic operations — recovery may be offline-only until re-enrollment with the new operator.
- Operator-issued temporary credentials that are not part of the principal's persistent identity (e.g., short-lived session certificates).

**Non-negotiable Invariants:**
- Chain integrity: every signing record must remain cryptographically verifiable under its original key algorithm until migration.
- Non-repudiation: the principal cannot deny prior consent decisions recorded in the vault.
- No orphan states: at no point during transition shall the principal's identity be inconsistent (e.g., simultaneously "bound to operator A" and "bound to operator B").
- Heir eligibility: only a principal designated by a valid consent record may claim the vault; designation itself must be signed and dated.

---

## 2. PER-COMPONENT CONTINUITY STRATEGY

### 2.1 Signing Keys (Operator-Key Rotation & Compromise Recovery)

**Current State:**
- Principal holds a long-lived identity signing key `id_sk` (rotated annually).
- Operator holds the corresponding custody key `op_sk`, which signs all vault-chain entries.
- Operator publishes `id_pk` and `op_pk` in a public key directory.

**Rotation (E171):**
1. Operator generates new key pair `(op_sk_new, op_pk_new)`.
2. Operator issues a signed "key-rotation record" containing:
   - `op_pk_old` (revoked)
   - `op_pk_new` (active)
   - Rotation timestamp and reason
   - Signed by `op_sk_old` (proof the operator controlled the old key)
3. Principal receives notification and countersigns the rotation record with `id_sk`.
4. New operator key becomes active after a 14-day escrow period.
5. All subsequent vault-chain entries use `op_sk_new`.

**Compromise Recovery (E177):**
1. Principal notifies operator that `op_sk` is compromised.
2. Operator immediately revokes `op_pk` and issues a "compromise record" signed by a backup key held in escrow.
3. Operator and principal jointly generate a fresh key pair and counter-sign it.
4. All vault-chain entries signed with the compromised key are marked "pre-compromise" but remain in the chain for audit.
5. Post-recovery entries use the new key.
6. A "chain-trust anchor" record documents the compromise and certifies the new key's legitimacy.

**Archive Requirement:**
- Every key-rotation and compromise record is immediately archived to Internet Archive's Wayback Machine and Software Heritage in cryptographic-commitment form (commit hash embedded in record).

---

### 2.2 Biometric Templates (Liveness & Reissuance)

**Current State:**
- Principal's biometric templates (face, fingerprint, iris scan) are stored in encrypted form in the vault.
- Templates are used for re-authentication when the principal interacts with the operator.

**Continuity Strategy:**
- Biometric templates themselves do not migrate; they are part of the principal's identity state held by the current operator.
- Upon succession to a new operator (E159), the principal must re-enroll biometrically with the new operator within 30 days.
- Re-enrollment is triggered by a signed "operator-succession notice" issued jointly by the old and new operators.
- Re-enrolled biometric templates are hashed and stored alongside the operator-succession record for audit.
- If the principal has died (E255), the heir must complete a biometric re-enrollment to prove non-impersonation.

**Recovery:**
- If biometric templates are lost due to operator data loss, the principal may re-enroll within 90 days; this triggers a "re-enrollment record" that documents the loss event.

---

### 2.3 Chain Records (Vault History & Immutability)

**Current State:**
- Vault chain is an append-only log of signed entries (consent decisions, key rotations, transfers, etc.).
- Each entry is signed by the operator's custody key and includes a cryptographic hash of the prior entry (Merkle chain).

**Continuity Strategy:**
1. **Chain Preservation:** The entire vault chain is copied to the successor operator before the transition is finalized. The successor validates every signature using the predecessor's public keys.
2. **Chain Extension:** The successor appends a "succession record" to the chain, signed by both the predecessor and the successor, documenting the transfer of custody.
3. **Chain Finality:** Once the succession record is signed and archived, the predecessor's operator-key is retired and published as "inactive" in the public key directory.
4. **Archive Pattern:** Every 100 entries or annually (whichever is sooner), a "chain snapshot" is hashed and committed to a public ledger (e.g., Arweave or Ethereum if post-quantum-resistant commitments are used).

**Failure Recovery:**
- If the chain is partially corrupted during migration, the most recent valid snapshot is restored from Internet Archive or Software Heritage, and the successor resumes appending from that point, issuing a "chain-repair record" that documents the loss and the recovery anchor.

---

### 2.4 Consent Records (Succession Authorization & Heir Designation)

**Current State:**
- Consent records are vault entries that document the principal's decisions (e.g., "I authorize operator O1 to hold my vault").
- Records are timestamped, signed by the principal, and countersigned by the operator.

**Continuity Strategy:**
1. **Pre-Succession Consent:** Before any operator succession (E159), the principal must issue a consent record explicitly authorizing the transfer to the new operator. This record includes:
   - Name and PKI certificate of the new operator
   - Effective date of the transfer
   - Revocation clause (principal can cancel up to 14 days before effective date)
   - Principal's digital signature and timestamp
2. **Heir Designation:** A principal may issue a consent record naming one or more heirs and granting them contingent access to the vault upon proof of the principal's death. The record includes:
   - Heir name, identity, and legal relationship to the principal
   - Conditions for heir access (e.g., court-issued death certificate)
   - Heir's own operator assignment (for post-succession re-binding)
   - Revocation or amendment rights for the principal (can be changed any time during principal's lifetime)
3. **Time-Lock:** Heir-succession consent records are time-locked: they cannot be acted upon until at least 30 days after the principal's death is certified.

**Archive Requirement:**
- Every consent record (including heir designations) is archived to Internet Archive and Software Heritage within 24 hours of issuance.

---

### 2.5 Values Evidence (Principle Provenance)

**Current State:**
- Values evidence is a signed attestation of the principal's stated values, interests, and ethical commitments (e.g., "I believe in privacy-by-design").
- Used for automated decision-making (e.g., the vault may refuse a data-sharing request that violates stated values).

**Continuity Strategy:**
1. **Immutable Record:** Values evidence is stored as an entry in the vault chain, signed by the principal and timestamped.
2. **Validity Across Succession:** Upon operator succession, the successor operator must preserve all values-evidence entries verbatim; they are not re-signed or modified.
3. **Heir Binding:** If the vault transfers to an heir, the heir may amend or extend values evidence but cannot delete prior entries. Amendments are appended as new entries, with a reference to the prior values.
4. **Archive Pattern:** Values evidence is archived to Internet Archive and university partners (see Section 8) for long-term preservation and scholarly access.

---

### 2.6 Attestation History (Third-Party Verification)

**Current State:**
- Attestation history is a log of signatures from trusted third parties (e.g., a notary, a legal witness, a regulatory body) attesting to the principal's identity or the vault's integrity.

**Continuity Strategy:**
1. **Preservation:** Attestation records are preserved verbatim across all operator successions.
2. **New Attestations:** Upon operator succession or heir succession, the new operator may request new attestations from the same third parties to certify the transition's legitimacy.
3. **Archive:** Attestation records and any new attestations are archived to Internet Archive, Software Heritage, and academic partners within 7 days of issuance.

---

## 3. OPERATOR-SUCCESSION PROTOCOL (E159)

**Timeline: 60 days**

1. **Day 0–7: Announcement & Consent**
   - Principal issues a consent record naming the new operator and the succession date.
   - Record is signed, timestamped, and archived.
   - Old and new operators acknowledge receipt.

2. **Day 8–21: Chain Transfer & Validation**
   - Old operator exports the complete vault chain (all entries, signed by old-operator keys).
   - New operator imports the chain and validates every signature using old-operator public keys.
   - New operator issues a "chain-acceptance record" confirming integrity.
   - Both operators sign a joint "succession initiation record."

3. **Day 22–35: Biometric Re-enrollment**
   - Principal re-enrolls biometrically with the new operator (face, fingerprint, iris).
   - New operator stores encrypted templates and issues a "re-enrollment record."
   - Record includes hash of new templates and references the succession-initiation record.

4. **Day 36–49: Operator-Key Handoff**
   - Old operator rotates its operator-key to a new "successor-bound" key pair, signed by the old operator-key and witnessed by the new operator.
   - New operator begins signing vault-chain entries with its own operator-key.
   - A "custody-transfer record" is appended to the chain by both operators.

5. **Day 50–60: Finality & Archive**
   - Old operator publishes all its keys as "inactive" in the public key directory.
   - The complete successor chain (old entries + succession records + new entries) is archived to Internet Archive, Software Heritage, and university partners.
   - Both operators issue a joint "succession-complete record," signed and dated.

**Contingency (Day 60+):**
If validation fails at any step, the succession is aborted, both operators issue a "succession-abort record," and the principal remains bound to the old operator. A new succession attempt may commence after 30 days.

---

## 4. HEIR-SUCCESSION PROTOCOL (E255)

**Timeline: 120 days**

**Precondition:** Principal has issued a valid heir-designation consent record naming the heir and the heir's operator.

1. **Day 0–14: Proof of Death**
   - Heir submits proof of principal's death (court-issued certificate or certified death notice).
   - Heir's operator verifies proof and notifies the principal's old operator.
   - Old operator issues a "death-notice record" signed and timestamped.

2. **Day 15–30: Time-Lock Expiry**
   - Heir-designation consent record enters its active phase (30-day time-lock has elapsed).
   - Heir's operator retrieves the principal's heir-designation record from the vault chain.
   - Heir's operator verifies the heir's identity against the record and confirms operator assignment.

3. **Day 31–60: Chain Transfer & Heir Binding**
   - Old operator exports the complete vault chain to the heir's operator (now "heir operator").
   - Heir operator validates the chain and the heir-designation record.
   - Heir and heir operator jointly sign a "heir-succession-initiation record," referencing the death-notice record and heir-designation consent.
   - This record is appended to the chain.

4. **Day 61–90: Heir Biometric Enrollment & Identity Binding**
   - Heir enrolls biometrically with the heir operator (face, fingerprint, iris).
   - Heir operator stores encrypted templates and issues a "heir-re-enrollment record."
   - Heir operator generates a new principal-binding key pair for the heir and signs a "heir-principal-key record" that documents the binding.
   - Heir becomes the new principal for purposes of the vault.

5. **Day 91–120: Values & Attestation Update**
   - Heir may amend or extend the principal's values-evidence records (but may not delete prior entries).
   - Heir operator requests new attestations from third parties (notary, legal witness) to certify the heir's legitimate succession.
   - New attestation records are appended to the chain.
   - Complete heir chain (all prior records + succession records + heir records) is archived.
   - Heir operator and old operator jointly sign a "heir-succession-complete record."

**Contingency (Day 120+):**
If proof of death cannot be verified, the succession is aborted and the vault remains in "principal custody" indefinitely. An heir may resubmit proof after 90 days.

---

## 5. CRYPTOGRAPHIC-MIGRATION HANDOFF (POST-QUANTUM)

**Trigger:** Transition occurs when a NIST-standardized post-quantum algorithm is adopted and approved for production use by the Calm-suite foundation.

**Process (per POST_QUANTUM_MIGRATION_PLAN_v0.md):**

1. **PQ Algorithm Election:** Foundation and operators agree on a specific PQ signature scheme (e.g., ML-DSA, SLH-DSA).

2. **Dual-Key Period (24 months):**
   - All operator-keys and principal-keys are augmented with PQ key pairs (hybrid mode).
   - New vault-chain entries are signed using both classical and PQ keys (sequential signatures, concatenated).
   - Old entries remain signed with classical keys only.

3. **Migration Records:**
   - Each operator issues a "PQ-migration-initiation record" signed by both classical and PQ keys, announcing the date when PQ-only signatures begin.
   - Each principal issues a "PQ-adoption consent" record, signed by both classical and PQ keys.

4. **Re-signing Phase (months 25–36):**
   - Old vault-chain entries are re-signed with PQ keys by the operator, creating a "PQ-legacy record" for each entry that includes both the original classical signature and the new PQ signature.
   - The re-signing process is logged entry-by-entry and archived.

5. **Transition Completion (month 37+):**
   - All new entries are signed with PQ-keys only.
   - The chain is verified end-to-end using both classical and PQ verification to ensure no corruption.
   - A "PQ-migration-complete record" is issued and archived.

**Archive Requirement:**
- Every PQ-migration record and every re-signed entry is archived to Internet Archive, Software Heritage, and university cryptography departments.

---

## 6. 25-YEAR TIMELINE & MILESTONES

| Year | Milestone | Event | Reference |
|------|-----------|-------|-----------|
| 0 | Baseline | Calm-suite identity established; principal, operator, heir-designation consent issued | E159, E255 |
| 1–3 | Annual Rotations | Operator-key rotation (E171) occurs at end of each year; archived | E171 |
| 3–4 | Contingency Event | (Simulated) operator-key compromise; recovery procedure exercised (E177) | E177 |
| 5 | First Re-enrollment | Biometric templates re-enrollment to test consistency; archived | 2.2 |
| 8 | Operator Succession #1 | Principal voluntarily transitions to new operator; full chain transfer (E159) | E159 |
| 10 | Values Amendment | Principal updates values-evidence record; amendment archived | 2.5 |
| 12 | Attestation Renewal | Third-party attestation refreshed; new attestation record archived | 2.6 |
| 15 | PQ Migration Initiation | Dual-key period begins; hybrid classical + PQ signatures | 5, POST_QUANTUM |
| 16–17 | PQ Re-signing Phase | Legacy entries re-signed with PQ; re-signing archived month-by-month | 5, POST_QUANTUM |
| 18 | PQ Migration Complete | All new entries are PQ-only; chain verified end-to-end | 5, POST_QUANTUM |
| 20 | Heir Contingency Drill | (Simulated) heir succession initiated; proof-of-death procedure tested | E255 |
| 22 | Operator Succession #2 | Principal transitions to a third operator; migrated chain includes PQ records | E159 |
| 24 | Final Attestation | Third-party attestation of 25-year identity continuity; archived | 2.6 |
| 25 | Archive Validation | Complete vault chain (all 25 years) re-verified and archived to permanent partners | 8 |

---

## 7. FAILURE MODES & RECOVERY PROCEDURES

### 7.1 Operator Becomes Unresponsive (E177)

**Symptom:** Operator does not sign requests for N days; chain stalls.

**Recovery:**
1. Principal notifies backup operator (if designated).
2. Backup operator issues a "contingency-takeover record" and immediately begins accepting new entries.
3. Original operator is marked "inactive" in public key directory.
4. Within 30 days, original operator must respond or be formally declared defunct.
5. If defunct, principal initiates emergency succession to backup operator (E159, condensed timeline).

### 7.2 Chain Corruption or Data Loss

**Symptom:** Operator reports that vault-chain database is corrupted; some entries are unrecoverable.

**Recovery:**
1. Operator and principal jointly retrieve the most recent chain snapshot from Internet Archive or Software Heritage.
2. Chain is restored to the state of the snapshot.
3. A "chain-repair record" is issued, documenting the loss event, the recovery anchor, and the gap in the chain.
4. Principal re-signs the repair record to acknowledge the loss.
5. New entries resume from the recovery anchor forward.
6. Operator compensates the principal (per service agreement) for any lost entries (e.g., consent decisions, attestations).

### 7.3 Principal's Operator-Key Compromise (E177)

**Symptom:** Principal discovers their operator-key has been leaked or stolen; attacker may be signing false chain entries.

**Recovery:**
1. Principal immediately notifies operator and all archived partners.
2. Operator revokes the compromised key and issues a "compromise record" signed by a backup key held in escrow.
3. All entries signed by the compromised key after the compromise date are flagged as "untrusted" pending verification.
4. Principal and operator jointly verify which entries are legitimate (e.g., by reviewing a signed log of intended operations).
5. Fraudulent entries are marked "repudiated" and removed from the active chain (but retained in the archive for forensics).
6. A new principal-key pair is generated and signed by the operator.
7. Recovery is archived.

### 7.4 Heir's Legitimacy Challenged

**Symptom:** A third party (e.g., a competing heir, a creditor) disputes the heir's right to inherit the vault.

**Recovery:**
1. Heir submits proof of legitimacy: valid court order, certified will, or legal guardianship document.
2. Third party may appeal to the heir's operator or to a neutral arbitration body named in the consent record.
3. Arbitration record is added to the vault chain, documenting the dispute and its resolution.
4. If the heir loses the dispute, the vault remains in escrow; no new entries are signed until a court order or new consent record resolves the deadlock.

### 7.5 PQ Algorithm Becomes Compromised

**Symptom:** A practical attack on the chosen PQ algorithm is published; the algorithm is no longer trusted.

**Recovery:**
1. Foundation declares the algorithm unsafe and selects a new one.
2. A new PQ migration is initiated, following Section 5 with accelerated timelines.
3. The vault chain is re-signed using the new PQ algorithm.
4. All previous PQ signatures are re-verified with the new algorithm to ensure no backdoor was exploited.
5. A "PQ-compromise record" is issued and archived with forensic details.

---

## 8. NAMED ARCHIVE PARTNERS FOR FOUNDATION-LEVEL ARCHIVAL

The Calm-suite foundation shall designate the following institutions as permanent custodians of vault-chain records and identity continuity documentation:

1. **Internet Archive (archive.org)**
   - Wayback Machine captures of all public key directories, successor announcements, and succession records.
   - Cryptographic commitments (commit hashes) embedded in each record for verification.
   - Retention: indefinite, with quarterly validation audits.

2. **Software Heritage (software-heritage.org)**
   - Authenticated Git commits of the complete vault-chain history.
   - Tag-based versioning for each operator succession and PQ migration milestone.
   - Retention: indefinite, with decentralized node replication.

3. **Stanford Digital Repository (SDR)**
   - Archival copies of all consent records, attestation records, and values-evidence entries.
   - Metadata: principal name (or pseudonym), succession dates, heir designations (encrypted).
   - Retention: 100+ years with regular integrity validation.

4. **MIT Libraries – Cryptography & Identity Research**
   - Historical copies of all cryptographic key-rotation and PQ-migration records.
   - Metadata: algorithm names, key lengths, compromise reports, and recovery procedures.
   - Retention: indefinite; scholarly access per DMCA exemption for security research.

5. **Library of Congress – American Folklife Center**
   - Archival copies of values-evidence records and heir-designation testimonies (if permitted by consent).
   - Purpose: preservation of individual identity narratives and cross-generational values transmission.
   - Retention: indefinite; public access after principal's death (or per heir consent).

6. **European Archives Consortium (ICA)**
   - Archival copies of all operator-succession records and attestation records (for principals outside the US).
   - Jurisdiction: European principal data; GDPR-compliant storage and access controls.
   - Retention: indefinite; national archive replication.

**Archive Protocol:**
- Every vault-chain record (consent, key rotation, succession, attestation, PQ migration) is automatically submitted to all designated partners within 24 hours of signature.
- Submissions are cryptographically signed by the operator; acceptance is confirmed with a timestamped receipt.
- Quarterly validation audits verify that archived records remain accessible and unmodified.
- In the event of a principal's death or vault closure, access permissions are transferred to the heir or the principal's estate per consent record instructions.

---

## 9. SUMMARY

This plan establishes a principled framework for identity continuity across 25 years of cryptographic, operational, and generational change. By preserving the vault chain, enforcing consent records, and archiving all transitions to independent partners, the Calm-suite ensures that a principal's identity—and, upon death, their legacy—survives operator failures, cryptographic migration, and heir succession.

The plan is intentionally conservative: it privileges chain integrity and non-repudiation over convenience. Recovery procedures are designed for offline verification and do not assume operator availability. Archive partners are geographically and institutionally diverse, ensuring that no single entity can unilaterally erase or falsify a principal's identity history.

---

*— Musk*

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
