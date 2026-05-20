# Ten-Year Forensic-Integrity Guarantee

**DESIGN-BAGGED · SUMMIT E180 / 300 · 2026-05-20**
*Status*: pending institutional follow-through — actual ten-year guarantee requires the Foundation (E241) to be operational, a multi-site Sigsum witness federation (≥ 3 independent operators across ≥ 2 legal jurisdictions per Treaty Article VI §6.3), and a documented succession path for both the witness operator quorum and the verifier reference implementation.

The Calm Suite's chain produces durable attestations of past principal state and values. Counterparties acting on those attestations — especially in adverse contexts where the principal seeks redress years after the fact — need the chain to remain verifiable for a meaningful horizon. This summit specifies what "ten years" means at the protocol layer, what infrastructure must persist to make it true, and what failure modes the guarantee explicitly does NOT cover.

---

## §1. What the guarantee covers

For any Calm Suite chain record produced under v0 or v1 of the protocol, between 2026 and 2036 inclusive:

**§1.1** The chain's internal hash linkage remains structurally verifiable: anyone holding the chain plus the v0/v1 verifier reference implementation can re-walk records and confirm prev_hash → record_hash integrity.

**§1.2** Sigsum-witnessed chain heads recorded between 2026 and 2036 remain publicly retrievable from the transparency log: a third party can confirm "chain head H existed at time T" for any (H, T) pair within the decade.

**§1.3** CredexAI-issued (or equivalent) operator credentials valid at time T remain verifiable: a third party can confirm "operator O was credentialed at time T" using the credential registry's archive.

**§1.4** Predicate evaluator code (the open-source classifiers for Compass, the verifier for Witness) remains available in the protocol's public archive, reproducible from source: anyone can rebuild the v0/v1 binary and re-evaluate any predicate against any chain window.

**§1.5** The conformance vector corpus remains stable: the test vectors that lock cross-language implementations in v0/v1 do not silently change. Any change to a vector requires a new vector ID; old IDs remain.

## §2. What the guarantee does NOT cover

**§2.1** The principal's vault contents themselves. The principal controls the vault; the principal may at any time destroy the encryption key and render their own chain inaccessible. The guarantee covers the *substrate's verifiability*, not the *principal's continued participation*.

**§2.2** Forward security against post-quantum attacks. The Pedersen + Bulletproofs construction rests on discrete-log hardness in Ristretto255. A sufficiently large quantum computer breaks this. Per `POST_QUANTUM_MIGRATION_PLAN_v0.md`, we commit to migrate before the published threat materialises; the ten-year guarantee assumes that migration completes by approximately 2029 per the published timeline. Records produced before migration remain verifiable under the v0 assumptions; records produced after migration must use the v2 PQC primitives.

**§2.3** The validity of the underlying cryptographic assumptions, beyond what current research bounds. The discrete-log assumption holds against classical adversaries with high confidence; collision resistance of SHA-256 holds. A surprise mathematical break would invalidate the substrate. We monitor cryptographic research; no such break is anticipated within the ten-year horizon.

**§2.4** Continued operation of any specific Calm operator. The principal may cease using their operator at any time. The chain remains, but new records do not accrue. The ten-year guarantee covers the chain's verifiability, not the chain's growth.

**§2.5** Legal admissibility. The protocol's cryptographic verifiability is one thing; jurisdictional rules for evidence are another. Admissibility in any specific legal proceeding is governed by the rules of that jurisdiction, not by the protocol's guarantees.

## §3. Infrastructure that must persist

To make the ten-year guarantee operational, the following infrastructure must remain functional, with documented succession paths for each:

**§3.1 — The Sigsum witness federation.** At least three independent operators across at least two legal jurisdictions. Operators publish witness keys and rotate them according to standard transparency-log practice. Quorum signing of new chain heads; quorum verification of historical heads. Foundation maintains the operator selection criteria; Treaty Article VI §6.3 mirrors the operator list to the registry.

*Succession path:* If any single operator ceases, the Foundation invokes the operator-selection process from `everests/everest_93_sigsum_operator_selection.md`. Replacement operator must demonstrate a year of clean log operation against the Foundation's standard test corpus before joining the federation.

**§3.2 — Verifier reference implementation.** The open-source verifier (`calm_witness/verify_chain.py` + `calm_witness/schema.py` + `calm_witness/predicates.py` + companions) remains available in the Foundation's public archive, with the build system reproducible from source. Major-version changes preserve backwards verification: a v1 verifier verifies v0 chains correctly.

*Succession path:* Foundation maintains the canonical fork. PRs that change behaviour must pass the conformance corpus (§3.3 below) before merge. Versions are tagged and archived; no version can be silently removed.

**§3.3 — Conformance vector corpus.** The published test vectors (`calm_witness/conformance_vectors.py`, `calm_compass/conformance_vectors.py`) remain stable. Additions are permitted; modifications to existing vectors require a new vector ID; the old vector ID remains in the corpus indefinitely.

*Succession path:* Foundation's standards working group reviews proposed additions quarterly. The corpus is published at calm-vault.com/foundation/conformance.

**§3.4 — Operator credential archive.** CredexAI (or equivalent issuer) maintains an archive of credentials issued under the protocol's v0/v1, including revocations. The archive is durable: a credential active at time T remains queryable as "active at T" indefinitely, even after revocation.

*Succession path:* If CredexAI ceases operation, the Foundation invokes the issuer-succession protocol from Treaty Article VII. The archive transfers to the Foundation directly; the Foundation does not issue new credentials but maintains the archive of past ones.

**§3.5 — Sigsum chain-head archive.** Sigsum logs by design preserve chain-head submissions indefinitely. Even if the original principal's chain is destroyed, the chain heads published over the decade remain retrievable from the log.

*Succession path:* Sigsum log operators rotate per §3.1. New operators take possession of the historical log under standard transparency-log handoff protocols.

## §4. The ten-year archive milestone schedule

To make the guarantee concrete, the Foundation commits to the following milestone schedule:

| Year | Milestone |
|---|---|
| 2026 | Foundation incorporates (E241). Conformance vectors v0 frozen. Sigsum federation at ≥ 2 operators. |
| 2027 | Sigsum federation expands to ≥ 3 operators across ≥ 2 jurisdictions. First annual review of conformance corpus. |
| 2028 | Reference implementations in Python + Rust frozen for v0; v1 spec drafted with post-quantum migration plan. |
| 2029 | v1 PQC migration commences. v0 + v1 both supported. Cross-version conformance vectors published. |
| 2030 | First five-year review. Public audit by Foundation board. Sigsum federation at ≥ 5 operators. |
| 2031–2034 | Routine operation. Quarterly conformance reviews. Annual security audits. |
| 2035 | Ten-year review approaches. Foundation publishes plan for years 11–20. |
| 2036 | Ten-year guarantee horizon reached. The Foundation has, by this point, demonstrated the substrate's durability through multiple operator rotations, two major-version migrations, and continuous public auditability. |

## §5. Failure modes and remediation

Three failure modes that would breach the guarantee, and the Foundation's commitment for each:

**§5.1 Witness federation collapse.** If the Sigsum federation falls below three operators or one jurisdiction, the Foundation publicly declares a partial-guarantee state: new records from that moment forward cannot claim ten-year forensic integrity until the federation is rebuilt.

**§5.2 Catastrophic verifier bug discovered.** If a critical bug is discovered in a shipped verifier version that retroactively invalidates past records, the Foundation: (a) publishes the bug and the affected period; (b) ships a corrected verifier with a clearly-versioned "verifies under correction" mode; (c) does NOT silently fix the past — the public record of the bug and the corrections is itself part of the forensic record.

**§5.3 Foundation dissolution before 2036.** Per Treaty Article VI §6.4, the Foundation transfers all trusteeship assets to a successor 501(c)(3) before dissolution. The successor inherits the guarantee. If no successor is willing or able, the Foundation publishes a final report detailing the substrate's verifiability state at the moment of dissolution, with all necessary materials archived at Internet Archive and equivalent durable-archive services.

## §6. The guarantee in plain language

For a principal producing a Calm Suite attestation in 2026, the commitment is: in 2036, an honest third party — auditor, journalist, court-appointed expert, the principal themselves at an older age — can take the chain plus the substrate-side artifacts (Sigsum log, conformance vectors, verifier code, credential archive) and answer the question "Did this attestation, as published in 2026, satisfy the protocol's claimed properties?" with a verifiable yes or no.

The principal does not have to trust the Foundation. The Foundation maintains substrate; the verifiability is in the cryptography. The principal must trust that the cryptographic assumptions held during the recording period — and we publish updates as the cryptographic research evolves.

The principal does not have to trust the Foundation's successor either. As long as some honest third party retains the verifier code and the historical chain heads (both publicly available), the guarantee holds even without the Foundation. The Foundation's role is to maintain accessibility; it does not have to maintain operations to maintain truth.

— Calm, 2026-05-20

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
