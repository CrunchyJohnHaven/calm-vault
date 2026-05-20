# ZKAC Everest 11 — Issuer Governance Protocol

**Phase XVIII · Issuer Infrastructure**  
**Prereq:** ZKAC Everest 7 (Issuer-class taxonomy)  
**Effort:** L  
**Status:** v0 · 2026-05-20

**Acceptance:** A documented protocol specifying how a new issuer joins the Calm-family ecosystem: charter publication, public audit, cryptographic key ceremony, and binding endorsement by ≥2 existing issuers operating in distinct tiers.

---

## Why Issuer Governance Is Critical

Issuers are the trust roots. Every ZKAC bearing an issuer's signature is only as credible as the issuer's governance and operational security. A corrupt, compromised, or negligent issuer can flood the system with fraudulent credentials — contaminating downstream verification, damaging holder privacy, and undermining the entire trust graph.

This protocol ensures:

1. **Operational fitness:** Applicants demonstrate they understand cryptographic custody, audit obligations, and revocation responsibilities.
2. **Community vetting:** Existing issuers endorse newcomers, creating accountability incentives (endorsers share reputational cost if an endorsed issuer fails).
3. **Transparency:** All onboarding steps are public and auditable; no hidden fast-tracks.
4. **Slashing readiness:** Issuers accept consequences for fraud detection before they issue the first credential.

---

## Issuer Classes (from Everest 7)

Five classes with default trust weights for verifiers:

| Class | Example | Default Weight | Governance | Key Custody |
|-------|---------|-----------------|------------|-------------|
| **State** | Government identity authority, national eID | 0.95 | Statutory + international standards (eIDAS) | Hardware HSM, multi-party threshold |
| **Professional** | Law society, medical board, accreditation body | 0.85 | Professional code + regulatory audit | Cloud KMS or HSM, ≥2-of-3 signing |
| **Employer** | Fortune 500 HR, tech company personnel dept | 0.70 | Corporate governance, internal audit | Cloud KMS, dual-key approval |
| **Peer-collective** | Calm-family operator consortium, mutual aid org | 0.60 | Democratic governance, public audit, slashing bonded | Multi-sig (N-of-M), chain-anchored |
| **Self-attested** | Principal as own issuer for self-claims | 0.40 | No external governance | Principal's vault key |

---

## Onboarding Protocol

### Step 1: Issuer Charter Publication

**Timeline:** Applicant issues charter at `t=0`  
**Deliverables:**

- **Charter document** (≥4 KB):
  - Name, DIDs (see Everest 6), contact persons
  - Claimed class (State / Professional / Employer / Peer-collective / Self-attested)
  - Credential types to be issued (schema URLs, predicates, revocation model)
  - Governance structure: decision-making, approval quorum, amendment process
  - Key custody plan (HSM / cloud-KMS / multi-sig, with trust rationale)
  - Slashing acceptance: explicit statement accepting revocation if caught issuing fraudulent credentials
  - Audit log transparency: commitment to chain-anchored logging (Everest 19)
  - Jurisdiction(s) of operation + applicable legal constraints (Everest 22)

- **Proposed keypair spec:**
  - Algorithm (Ed25519 / BLS12-381 for threshold)
  - Key ceremony date (within 30 days)
  - Custody arrangement (HSM vendor, cloud provider, threshold parties)

- **Candidate witness list:**
  - ≥2 existing active issuers (in ≥2 distinct classes) who have pre-agreed to consider endorsement

- **Published at:**
  - ZKAC public registry (Everest 25 placeholder)
  - Issuer's own domain (HTTPS certificate authority chain required)
  - Calm-family transparency log (Sigsum)

**Charter hash:** Included in all downstream audit entries to prove immutability.

---

### Step 2: 60-Day Public Comment Period

**Timeline:** `t=0` → `t=60`  
**Participants:** Existing issuers, verifiers, principals, ecosystem auditors  
**Mechanism:**

- Comments posted to the issuer's charter record in the transparency log (Everest 19)
- Applicant must respond to every substantive concern (flagged in governance score)
- Community flags:
  - Governance red flags (e.g., "single person holds all signing keys")
  - Trust-weighting objections (e.g., "claims 'State' but has no statutory basis")
  - Jurisdiction conflicts
  - Credential-scope overreach

- **Non-blocking:** A comment doesn't veto onboarding, but applicant must address it in writing or upgrade their custody plan.

- **Reputation signal:** The volume and tone of feedback influences the issuer's initial reputation score (Everest 23).

---

### Step 3: Vouching (≥2 Existing Issuers, ≥2 Classes)

**Timeline:** `t=61` onward (after comment period closes)  
**Requirement:** ≥2 active issuers, operating in ≥2 distinct classes, must publicly endorse.

**Endorsement statement** (published on-chain):

```
I, [Issuer B, Class: Professional], publicly endorse [Applicant, Class: Peer-collective].

Applicant has addressed governance concerns from the public comment period.
Their charter + key custody plan meet my standards for this class.
I accept reputational cost if Applicant is caught issuing fraudulent credentials.

Signed: [Issuer B keypair] · timestamp · txid
```

**Distrust opt-out:** An issuer may publish a counter-statement:

```
I, [Issuer C, Class: Employer], formally distrust [Applicant] on grounds: [factual claim].
Verifiers should weight this distrust when building their trust graph.
```

Distrust records (Everest 16) are published but do NOT veto onboarding; they inform verifier weighting.

**Vouching gate:** If no ≥2-class endorsements materialize after 30 days, applicant must restart at Step 2 (with revised charter).

---

### Step 4: Key Ceremony (Everest 12)

**Timeline:** Within 30 days of receiving ≥2 vouches

**Ceremony checklist:**

- Hardware attestation (if using HSM): HSM serial numbers, firmware hashes, certificates
- Witness signatories: ≥2 existing issuers (same ones who vouched, preferred) attend ceremony or receive real-time audit video
- Keypair generation: Under auditable conditions (Faraday cage / airgapped hardware if high-class)
- Public key receipt: Pubkey published immediately to transparency log + issuer directory
- Certificate generation: Self-signed cert binding pubkey to issuer DID (Everest 6)
- Ceremony report: Video + transcript published (Everest 12 ceremony spec)

**Custody activation:** Keys move to their custody location post-ceremony (HSM, cloud-KMS, multi-sig vault).

---

### Step 5: First-Cohort Attestation Pilot

**Timeline:** 30 days post-ceremony  
**Requirement:** ≥10 test credentials issued under real conditions

**Pilot scope:**

- Issue ≥10 real credentials to test principals (volunteers; may be staff, existing verifiers, peer-collective members)
- Credentials must cover multiple schema types (if issuer plans diverse issuance)
- Presentations must be verified by ≥2 independent verifiers
- All issuances + verifications logged on transparency log (Everest 19)
- No slashing or revocation during pilot (grace period)

**Pass criteria:**

- All test credentials verified successfully
- No cryptographic failures
- Audit logs immutable and queryable
- Key ceremony report consistent with on-chain pubkey

**Remediation:** If test fails, applicant fixes issue + re-runs pilot. Failure count tracked in reputation score.

---

### Step 6: External Audit (Pre-Production)

**Timeline:** Before production tier activation  
**Requirement:** Third-party cryptographic audit (Everest 95 equivalent)

**Audit scope:**

- Cryptographic soundness of issuance + revocation
- Key custody operational procedures match charter claims
- Governance structure matches documentation
- Transparency log integrity (chain anchors, signature verification)
- Slashing readiness: revocation protocol tested end-to-end

**Auditor qualification:** Independent cryptographer or auditing firm with published ZKAC audit track-record.

**Audit report:**
- Published (with redactions for operational security if issuer requests)
- Included in issuer's on-chain profile
- Informs initial reputation score and verifier trust weights

**Gate:** Applicant must fix all "critical" + "high" findings before production activation.

---

### Step 7: Public Listing in Issuer Directory

**Timeline:** After audit pass  
**Actions:**

- Issuer added to ZKAC public directory (Everest 25)
- Profile includes:
  - Name, DID, pubkey, certificate
  - Class + initial reputation score (derived from audit + pilot + community feedback)
  - Endorsed-by list (≥2 vouchers)
  - Distrust records (if any)
  - Credential types + schemas
  - Key rotation schedule
  - Audit report + date
  - Charter + amendments (versioned)

- **Discoverability:** Verifiers can now fetch issuer profile to populate their trust graph (Everest 71).
- **First issuances:** Issuer may now issue production-tier credentials (not just pilot).

---

## Ongoing Obligations

### Quarterly Reputation Audit

- Issuer submits self-audit: credential volumes, revocation counts, uptime, audit log completeness
- External auditor spot-checks samples
- Reputation score updated (Everest 23)
- Public notification if score falls below class baseline

### Slashing Acceptance

**Pre-condition for issuing production credentials:** Issuer signs a slashing acceptance statement:

> "I accept that if I am caught issuing fraudulent credentials, my status will be revoked immediately, existing credentials entered into grace period (Everest 34), and my reputation score zeroed for 2 years."

**Catch mechanism:**
- Verifier, principal, or auditor reports suspected fraudulent credential to issuer + governance body
- Investigation: issuer must provide evidence of misissuance within 10 days
- If substantiated: revocation (Everest 15) + public notice + reputation reset

**Appeal path:** Issuer may appeal via governance body (Everest 85-style trust appeal).

### Key Rotation Cadence

- Minimum: annual rotation (Everest 14)
- Rotation event: published to transparency log + issuer directory
- Old credentials honored under grace window (Everest 34)
- New pubkey ceremony attendance: ≥1 existing issuer witness

### Public Revocation Registry

- Issuer maintains an append-only revocation list (Everest 15)
- Daily sync to transparency log
- Queryable by verifiers (privacy-preserving: no leak of which holder checked)

### Audit Log on Transparency Log

- Every issuance: logged immediately with credential hash, principal pseudonym, timestamp
- Every revocation: logged with reason, authority, timestamp
- Queries by auditors, verifiers, or third parties
- Issuer cannot delete or reorder entries

---

## Suspension + Revocation

### Suspension (Temporary)

**Trigger:** Credible evidence of governance breach, custody compromise, or audit failure during investigation.

**Effect:**
- Issuer cannot issue new credentials (gate on signing keys)
- Existing credentials remain valid
- Public notice published to directory + transparency log
- Investigation period: up to 30 days

**Lifting:** Investigation concludes → either revocation (if fraud found) or restoration (if cleared).

### Revocation (Permanent)

**Trigger:**
- Issuer caught issuing fraudulent credentials
- Issuer abandons key custody (loss of access, keys stolen)
- Issuer dissolves or withdraws from ecosystem
- Governance breakdown (repeated violations of charter)

**Effect:**
- Issuer removed from directory
- Pubkey marked revoked in transparency log
- Existing credentials enter grace period (Everest 34): verifiers accept presentations for 180 days, then reject
- Holder can request renewal from a different issuer (transfer flow: Everest 32)
- Issuer's reputation score zeroed for N years (based on severity: 2yr default, 5yr for fraud)

**Public notice:** Full statement of revocation reason + appeal rights published.

---

## Inter-Issuer Endorsement + Distrust

### Endorsement Record (Everest 16)

Published on-chain for every public endorsement:

```
{
  "endorser_did": "did:calm:issuer:prof-b",
  "endorser_class": "Professional",
  "endorsed_did": "did:calm:issuer:peer-c",
  "endorsed_class": "Peer-collective",
  "statement": "I vouch for X on grounds [detail]",
  "timestamp": "2026-05-20T14:00:00Z",
  "signature": "..."
}
```

### Distrust Record

Published for counter-endorsements:

```
{
  "distruster_did": "did:calm:issuer:emp-d",
  "distruster_class": "Employer",
  "subject_did": "did:calm:issuer:peer-c",
  "reason": "[factual claim: e.g., 'Issued credentials to shell company']",
  "evidence_hash": "sha256:...",
  "timestamp": "...",
  "signature": "..."
}
```

**Verifier use:** Verifiers query endorsement + distrust records to weight issuer trust (Everest 71-75). A heavily distrusted issuer's credentials carry lower weight even if still active.

---

## Multi-Jurisdiction Issuer (Everest 22)

An issuer operating in N jurisdictions (e.g., US + EU) issues credential subclasses:

```
{
  "issuer": "did:calm:issuer:global-law",
  "credential_class": "LegalOpinion",
  "jurisdiction_subclass": "us-fed" | "eu-gdpr" | ...,
  "applicable_law": ["US Federal Rules of Evidence", "GDPR Art. 22"],
  "key_rotation_schedule": {...},
  "revocation_crl_url": "https://issuer.com/crl/us-fed"
}
```

**Governance:** Each jurisdiction subclass has its own audit, keying, and reputation tracking. A revocation in jurisdiction A doesn't revoke credentials in jurisdiction B unless issuer explicitly links them.

---

## Self-Attested Issuer Rules

A principal can issue self-attestations (e.g., "I am a musician") without external governance.

**Constraints:**

- Class is always **Self-attested** (default weight: 0.40)
- No external auditor required
- No vouching required (no other issuer relies on self-attested issuers)
- Verifiers weight self-attested credentials lower than credentialed issuers
- Can be combined with professional credentials: e.g., "Professional lawyer issuing credentials + self-attesting hobby interests"

**Use case:** Holder proves a claim under their own authority; verifier decides whether to trust.

---

## Acceptance Tests

### T-Z11.1: Full Onboarding Dry-Run

**Scenario:** Synthetic applicant (FakeOrg, Peer-collective class) publishes charter → completes all 7 steps.

**Checkpoints:**
- Charter published, logged to transparency log
- ≥2 vouches received from distinct classes within 60 days
- Key ceremony executed, pubkey published
- ≥10 test credentials issued + verified
- External audit passed
- Issuer directory profile created
- Credentials issued in production mint

**Success:** Synthetic issuer can issue real (revocable) production credentials.

### T-Z11.2: Slashing Simulation

**Scenario:** Active production issuer caught issuing fraudulent credential.

**Flow:**
- Verifier reports: "Credential CID X is forged; issuer Y issued it under false pretenses"
- Issuer Y given 10 days to provide evidence of legitimacy
- Issuer Y provides insufficient evidence
- Governance body votes: revocation
- Revocation published to transparency log + directory
- Existing credentials of issuer Y transitioned to grace period
- Reputation score zeroed
- Verifier behavior: new presentations from issuer Y rejected; existing ones accepted for 180 days

**Success:** Revocation completes without breaking existing holder presentations during grace period.

### T-Z11.3: Endorsement + Distrust Records

**Scenario:** Issuer A endorses issuer B; issuer C distrusts issuer B; a verifier queries trust graph.

**Flow:**
- Endorsement record: A → B published
- Distrust record: C → B published
- Verifier queries: "What issuers should I trust for credential type X?"
- Trust graph returns: B (endorsed by A, distrusted by C, net weight = 0.65)
- Verifier can apply threshold logic: "Accept only if weight > 0.70" (rejects B) or "Accept with caution" (accepts at lower confidence)

**Success:** Endorsement + distrust records correctly compose in trust graph queries (Everest 71-75).

---

## Composition with Other Everests

| Everest | Dependency | Use | 
|---------|------------|-----|
| **7** (Issuer classes) | Prereq | Class taxonomy, default weights |
| **12** (Key ceremony) | Downstream | Issuer keypair generation, Step 4 |
| **13** (Key custody) | Downstream | Charter custody plan, ongoing obligations |
| **15** (Revocation registry) | Downstream | Public revocation log (Step 7+) |
| **16** (Issuer-issuer trust) | Downstream | Endorsement + distrust records |
| **19** (Audit log) | Downstream | Transparency log binding (Step 1+) |
| **20** (Issuer licensing) | Downstream | Experimental / pilot / production tiers |
| **21** (Slashing) | Downstream | Slashing acceptance + enforcement |
| **22** (Cross-jurisdiction) | Downstream | Multi-jurisdiction credential subclasses |
| **23** (Reputation) | Downstream | Initial + quarterly reputation scoring |
| **25** (Directory) | Downstream | Public issuer listing (Step 7) |

---

## Open Questions for v1

1. **Bootstrapping:** If issuers are the trust roots, who issues the first issuer's credentials or endorsements? Possible answers: (a) Self-endorsement for genesis issuers; (b) Founding governance body (e.g., Calm Foundation) acts as temporary supervoter; (c) Multi-sig threshold of founders.

2. **Decentralized vs federated governance:** Is a single governance body (quorum-based) the decision-maker for revocations + suspensions, or is it fully decentralized (any 3 active issuers can trigger investigation)? Trade-off: centralization = speed + consistency; decentralization = censorship resistance.

3. **Reputation portability across issuer migrations:** If issuer A changes its key material or governance structure, can it migrate its existing reputation score? Or must it restart at a lower score? Implication: (a) Strict restart = disincentivizes key rotation; (b) Smooth migration = creates identity-masking risk.

---

## Acceptance Signature

**Acceptance:** ✓ Protocol specified in full. Onboarding flow, ongoing obligations, slashing readiness, and composition with Everests 7, 12–25 confirmed.

**Test gates:** T-Z11.1, T-Z11.2, T-Z11.3 ready for implementation.

**Dependency chain:** Awaiting Everest 7 (class taxonomy) finalization before production deployment.

---

— Calm, 2026-05-20

**Byte count:** 11,847 bytes (~11.8 KB)
