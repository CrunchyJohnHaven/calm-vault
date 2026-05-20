# Calm Witness — Master Attack Corpus v0

**Sprint:** S224
**Date:** 2026-05-20
**Classification:** Internal protocol security documentation
**Author:** CALM
**Version:** v0 (initial)

---

## Scope

Calm Witness attack surface: hash-chained self-report substrate (`user_state.jsonl`), Pedersen commitment layer, Σ-protocol range and equality proofs, predicate evaluator, disclosure envelope, operator identity, trust graph (ZKAC/Calm Pact), ZKAC governance, Sigsum/Roughtime transparency anchors, enrollment ceremony, hardware security boundary, and the Calm Pact composition handshake. One hundred named attacks across sixteen categories. Each entry: attack name, payload sketch, protocol property under test, summit reference where the defense is bagged (if any).

---

## Category 1: Replay

**R01 — Stale-Proof Replay**
Capture a valid disclosure envelope at T=0. Present it to a counterparty at T+48h when the principal is no longer in baseline. Freshness check on chain-head timestamp fails only if the verifier enforces the staleness window strictly.
Defense: nonce-in-request binding (Everest 70); chain-head freshness window; Roughtime anchor (Everest 31).
Summit: E70, E31.

**R02 — Same-Session Predicate Replay**
Capture a single-predicate envelope (e.g., `in_baseline_24h = true`) and replay it as proof for a different predicate in the same session without regenerating. The commitment and proof are structurally valid for the original predicate only.
Defense: `predicate_id` is bound into the Fiat-Shamir transcript; cross-predicate swap rejected by `verify_envelope`.
Summit: E65, E71.

**R03 — Chain-Head Reuse**
Strip the most recent chain record and resubmit the prior chain head as current, making a past-baseline state appear fresh. Chain length and sequence number checks detect the rollback.
Defense: monotonic sequence numbers; chain-head Sigsum inclusion proof must match current log head.
Summit: E28, E30.

**R04 — Consent-Grant Replay**
Record a `consent.grant` entry at T, revoke it at T+1, then replay the raw chain segment ending at the grant to a verifier who does not walk the full chain. Latest-wins semantics require full chain traversal.
Defense: `principal_consents_to_disclose` evaluator applies latest-wins across the entire chain; partial-chain submissions rejected.
Summit: E57, E75.

**R05 — Multi-Session Composite Replay**
Stitch together chain records from sessions N and N+2 (omitting session N+1 where an anomaly occurred) to present a continuous-looking baseline record with no gaps. Gap detection requires strict sequence-number contiguity.
Defense: `prev_hash` linkage makes record omission detectable; Sigsum anchors each session head independently.
Summit: E28, E30.

**R06 — Roughtime Spoofed-Freshness Replay**
Present an old envelope accompanied by a forged Roughtime response claiming the current time is within the envelope's freshness window. Requires breaking Roughtime signature, not breaking Calm.
Defense: Roughtime server signatures verified; quorum of ≥5 independent servers must agree (Everest 94).
Summit: E31, E94.

---

## Category 2: Substitution

**S01 — Cross-Principal Commitment Swap**
Take principal A's commitment-and-proof for predicate `in_baseline_24h` and submit it under principal B's operator identity. Proof transcript is bound to A's operator key; B's verifier rejects on key mismatch.
Defense: operator Ed25519 signature binds proof to operator identity; template commitment binds to principal's enrolled template (Everest 46).
Summit: E68, E46.

**S02 — Template Substitution at Enrollment**
Replace principal's enrolled biometric template with an attacker-controlled template during enrollment. Subsequent sessions are compared against the attacker's template, not the principal's.
Defense: enrollment ceremony requires air-gap, witness signatures, CredexAI VC binding (Everest 11, 20, 22).
Summit: E11, E20, E22.

**S03 — Re-enrollment Impersonation**
While principal is unavailable, submit a new enrollment with the attacker's biometrics under the principal's identity. Red-flag detection compares new template against prior enrollment; inconsistency triggers alert.
Defense: Everest 19 re-enrollment red-flag detection; template consistency proof (Everest 48).
Summit: E19, E48.

**S04 — Predicate Label Swap**
Evaluate `bank_teller_note_active` and relabel the result as `in_baseline_24h` before constructing the envelope. Predicate ID is bound into the Fiat-Shamir transcript; label swap produces invalid proof.
Defense: `predicate_id` in canonical form included in Fiat-Shamir challenge; registry content-addressable by `predicate_id_hash`.
Summit: E52, E65.

**S05 — Operator Key Impersonation**
Generate a fresh Ed25519 key pair, sign an envelope with it, and present the key as if CredexAI-issued. Verifier must check the operator VC, not just the signature.
Defense: Operator identity is a CredexAI VC; verifier checks VC validity against CredexAI's published trust anchor (Everest 68, 69).
Summit: E68, E69.

**S06 — Biometric-Clone Substitution**
Present a voice-clone transcript or a stroke-replay against the comparator to force `biometric_match_within(τ)` true for a non-principal. Liveness entropy checks and adversarial robustness study defend.
Defense: Everest 49 liveness detection; Everest 41 adversarial robustness.
Summit: E49, E41.

---

## Category 3: Fake Compliance

**F01 — Operator Assertion Without Chain**
Operator asserts `in_baseline_24h = true` in a plain JSON claim without producing a commitment or proof. Counterparty that accepts unsigned claims is outside the protocol; protocol requires a `DisclosureEnvelope`.
Defense: Counterparty-Implementer's Guide (Everest 98) mandates envelope verification; unsigned claims are not protocol-compliant.
Summit: E98, E71.

**F02 — Predicate Short-Circuit**
Operator evaluates a predicate in a version of `predicate_eval.py` where the evaluator always returns `True`, bypassing the golden corpus check. Predicate determinism harness detects evaluator drift.
Defense: Evaluator hash snapshot committed at registry time; content-addressable `predicate_id_hash` changes if evaluator changes (Everest 52, 63).
Summit: E52, E63.

**F03 — Fake Sigsum Inclusion Proof**
Construct a plausible-looking Sigsum inclusion proof for a chain head that was never actually logged. Sigsum witnesses' signatures are not forgeable without their keys.
Defense: Sigsum multi-witness consensus; verifier validates signatures from ≥ quorum of Sigsum witnesses (Everest 30, 93).
Summit: E30, E93.

**F04 — Self-Certifying Operator**
Operator issues its own VC to itself and signs disclosures with it. CredexAI's VC trust anchor is external; a self-issued VC fails trust-anchor check.
Defense: CredexAI VC validation against public DID/trust anchor; bridge attestors require cost-floor satisfaction (S174 / CO-03).
Summit: E68.

**F05 — Consent-Without-Chain**
Operator claims consent was granted without a corresponding `consent.grant` record in the chain. The evaluator `principal_consents_to_disclose` reads from the chain; absent record defaults to deny.
Defense: default-deny on missing consent record; consent evaluator reads chain only (Everest 57).
Summit: E57.

**F06 — Predicate Composition Bypass**
Operator submits a proof for `p1 AND p2` but evaluates only `p1`, setting `p2 = true` without evidence. Each component predicate must have its own commitment and proof in the envelope.
Defense: Multi-predicate envelope requires one `(commitment, proof)` per disclosed predicate; composition proof verifies each leaf independently (Everest 61, 71).
Summit: E61, E71.

---

## Category 4: Side-Channel

**SC01 — Predicate-Count Leakage**
Counterparty observes envelope size and infers how many predicates the principal has authorized, learning something about the principal's disclosure policy.
Defense: Everest 71 note: v1 BBS-2023 form hides requested-set cardinality; v0 partial mitigation: unrequested predicates absent.
Summit: E71.

**SC02 — Response-Time Biometric Oracle**
Operator takes variable time to evaluate `biometric_match_within(τ)` depending on how close the distance is to τ. Timing side-channel leaks distance proximity.
Defense: Constant-time comparison mandated in Rust production impl (Everest 81 Zeroize/constant-time disciplines).
Summit: E81.

**SC03 — Commitment-Value Repeated-Submission Oracle**
Adversary submits many proofs for incrementally varied thresholds τ and observes which proofs verify, binary-searching the committed distance. Range proof soundness must hold under repeated submission.
Defense: Bulletproofs are computationally binding; τ is committed and not revealed; proof does not expose distance even under many verifications (Everest 45).
Summit: E45.

**SC04 — Cache-Timing Chain-Verify**
Measure time to verify a chain of length N vs N-1 on an infrastructure that caches partial chain verification. Cache timing reveals number of records.
Defense: Record counts do not leak from the disclosure envelope; count-of-records leakage is an explicit non-goal per protocol spec.
Summit: E71.

**SC05 — Memory-Dump Key Extraction**
Attach a debugger or trigger a crash dump while the operator process holds the biometric template or private key in memory. Secure memory disciplines (Zeroize) prevent key material persisting beyond use.
Defense: Everest 81 Rust impl Zeroize obligation; Everest 13 voice-buffer explicit_bzero; iOS Secure Enclave / HSM for enrollment key (Everest 16).
Summit: E81, E13, E16.

**SC06 — Acoustic Side-Channel at Enrollment**
Microphone in the enrollment room captures keystroke or stylus sounds allowing reconstruction of handwriting stroke timing. Enrollment ceremony spec bans network-connected devices from the room.
Defense: Enrollment ceremony air-gap requirements (Everest 11).
Summit: E11.

---

## Category 5: Governance Capture

**GC01 — Predicate Registry Stuffing**
An adversary with reviewing-panel membership approves a harmful predicate that exposes protected category data. Five-reviewer panel with cross-domain composition is required; ≥3 accepts needed.
Defense: Predicate Audit Process (Everest 54) requires ≥5-reviewer panel across cryptography/disability-rights/behavioral-biometric/AI-safety/journalism; tombstoning bar ≥3 accepts.
Summit: E54.

**GC02 — ZKAC Governance Subversion**
A coalition holds enough ZKAC voting weight to ratify a protocol amendment that removes the cost floor, enabling Sybil attacks. Governance quorum rules must include veto from diverse constituent classes.
Defense: ZKAC governance (STACK_GOVERNANCE_20.md / CS-01..20); witness quorum selection uses verifiable randomness (S186).
Summit: S174, S186.

**GC03 — Review-Board Capture**
An adversary funds multiple nominally-independent review board members, achieving undisclosed majority control. Conflict-of-interest declaration is non-mandatory (see trust-network A15); capture is possible.
Defense: Partial: S175 vouch schema conflict-of-interest field; S185 corroboration challenges. Residual risk documented in S187/A15.
Summit: S187 (A15), E54.

**GC04 — Standard-Body Infiltration**
During NIST submission process, adversary proposes amendments that weaken range-proof soundness by inserting a trusted-setup requirement the adversary controls. NIST process is external; Calm's response is to publish the full protocol independently.
Defense: Open-source publication (Everest 92); independent third-party verification (Everest 100) prior to NIST submission (Everest 91).
Summit: E91, E92, E100.

**GC05 — Sigsum Operator Concentration**
Fewer than 3 Sigsum witnesses remain independent; the rest are covertly controlled by one operator. Chain-head publication loses the multi-party tamperproof guarantee.
Defense: Everest 93 requires ≥3 independently operated Sigsum witnesses with organizational diversity.
Summit: E93.

**GC06 — Transparency-Log Policy Drift**
Sigsum operator quietly changes retention or publication policy, making historical head retrieval unreliable without notifying Calm principals. Policy changes are detectable via public log inspection.
Defense: Sigsum is publicly auditable; Everest 30 mandates inclusion-proof retrieval stored back in vault; degraded-mode policy triggers `anchor_pending`.
Summit: E30.

---

## Category 6: Vouching-Ring / Trust-Graph

**VR01 — Mutual-Collusion Clique (Vouching Ring)**
K principals each vouch for all others, inflating all members' ZKAC scores without external validation. Graph motif detection down-weights cliques above density threshold.
Defense: S185 anti-collusion sampling; collusion coefficient applied above density threshold (S187/A03).
Summit: S187 (A03).

**VR02 — Sybil Identity Farm**
Attacker registers N cheap identities, each vouching for a target ZKAC. Proof-of-cost floor blocks low-cost registrations.
Defense: S174 proof-of-cost floor; cluster-detection heuristic (S187/A01).
Summit: S187 (A01).

**VR03 — Churn-and-Re-Register**
Principal with accumulated distrust abandons ZKAC, re-registers fresh identity, and resolicits vouches. Gap-proof requirement links new ZKAC to prior; revocation blacklist is keyed on registration anchor.
Defense: Non-refundable registration cost; gap-proof linking new to prior ZKAC (S187/A02).
Summit: S187 (A02).

**VR04 — Self-Vouch via Proxy**
Attacker vouches for proxy P; proxy vouches back for attacker, completing a 2-hop self-vouch cycle. Cycles of length ≤2 detected and nullified; longer cycles flagged if score impact exceeds threshold.
Defense: S176 reflexive-vouch prohibition for cycles ≤2 (S187/A05).
Summit: S187 (A05).

**VR05 — Paid-Vouch Market**
Vouches sold on external markets; buyers gain score without earning trust. Low-velocity paid vouching below audit trigger is undetectable from protocol state alone.
Defense: S175 vouch-type basis field; S185 out-of-band corroboration challenges; anomalous vouch velocity triggers audit (S187/A06).
Summit: S187 (A06).

**VR06 — Transitive-Path Inflation**
Attacker constructs a 4-hop path from a high-reputation anchor through mediocre intermediaries to an undeserving target, each hop contributing multiplicative decay that still sums to non-trivial score.
Defense: S176 multiplicative decay per hop with maximum hop-count truncation at 4 (S187/A09).
Summit: S187 (A09).

---

## Category 7: Parser Fuzz / Schema Violation

**PF01 — Malformed JSONL Record Injection**
Inject a chain record with `additionalProperties` fields beyond the schema. Schema validator with `additionalProperties:false` rejects; chain verify fails at that record.
Defense: JSON Schema Draft 2020-12 with `additionalProperties:false`; 30-case corpus tests bad-kind/unknown-field rejection (Everest 26).
Summit: E26.

**PF02 — Non-Hex Hash Field**
Set `record_hash` to a non-hex string. Schema validator rejects non-hex pattern; chain verifier rejects on hash decode.
Defense: Everest 26 schema; golden corpus case `bad-hex-hash` (Everest 26).
Summit: E26.

**PF03 — Timestamp Boundary Injection**
Inject a self-report record with a timestamp exactly at the 24h boundary for `in_baseline_24h`. Boundary-condition test cases in the golden corpus verify correct boundary semantics.
Defense: 35-case golden corpus includes boundary conditions (Everest 55, 64).
Summit: E55, E64.

**PF04 — Oversized Commitment Blob**
Submit a `BitProof` with a commitment field containing 512 bytes instead of 32, exploiting a length check absence. Wire format defines exact field sizes; MessagePack ingest fuzzer targets this.
Defense: Wire format spec (Everest 98); Everest 85 fuzzer target `disclosure_parse` and `MessagePack_ingest`.
Summit: E85, E98.

**PF05 — Unicode Normalization Attack**
Inject a self-report with a `kind` field using a homoglyph of `self_report.morning`. Schema kind-whitelist is exact-string; homoglyphs fail the enum check.
Defense: Everest 26 kind-whitelist with exact-string matching; golden corpus `bad-kind` test (Everest 26).
Summit: E26.

**PF06 — Null Byte Injection in Codeword Field**
Inject a null byte in `payload.bank_teller_token` to cause hash mismatch or string comparison bypass. SHA-256 of codeword is compared against stored hash; null-byte inclusion changes the hash.
Defense: `bank_teller_note_active` computes SHA-256(codeword) for comparison; evaluator is byte-exact (Everest 58).
Summit: E58.

**PF07 — Out-of-Range Sequence Number**
Append a record with `seq` set to a past sequence number, attempting to insert a record in the middle of the chain. Chain verifier checks monotonic seq increment; out-of-order seq triggers `seq_not_monotonic` error.
Defense: Chain verify monotonic sequence check; Everest 26 golden corpus `out-of-range-summit` (Everest 26).
Summit: E26, E28.

---

## Category 8: Key Extraction

**KE01 — Software Memory Scraping**
Process-level memory scrape during an active signing operation extracts the Ed25519 private key before it is zeroed. Constant-time Zeroize disciplines on the Rust production path.
Defense: Everest 81 Zeroize obligation on all key buffers; Everest 16 HSM-bound key where available.
Summit: E81, E16.

**KE02 — Cold-Boot Attack on Vault Master Key**
Rapid memory freeze of the operator device during an active vault session extracts the master key from DRAM before decay. Hardware-backed storage (Secure Enclave / HSM) prevents in-memory key residency.
Defense: Everest 16 key encryption with HSM-bound key; iOS Secure Enclave stores master key inaccessible to DRAM read.
Summit: E16.

**KE03 — Debug-Build Key Leak**
Operator ships a debug build that logs key material to a file or console. CI / release pipeline bans debug log output containing key-sized hex strings.
Defense: Everest 85 CI harness; Everest 90 audit-prep SBOM and dependency review includes build-mode verification.
Summit: E85, E90.

**KE04 — Side-Channel Key Recovery via Electromagnetic Emanation**
Measure electromagnetic emissions during Ed25519 signing operations to reconstruct the private key via differential power analysis. Constant-time cryptographic operations mitigate; production Rust uses `dalek` which is designed constant-time.
Defense: Everest 81 mandates no `unsafe` outside audited blocks; `dalek` crate is constant-time by design; hardware HSM removes signing from CPU EM surface.
Summit: E81, E16.

**KE05 — Enrollment-Device Compromise**
Attacker gains physical access to the enrollment device before or during ceremony and exfiltrates the template before encryption. Enrollment ceremony spec bans network-connected devices; template encrypted before leaving ceremony scope.
Defense: Enrollment ceremony air-gap (Everest 11); template encryption at capture (Everest 16).
Summit: E11, E16.

**KE06 — Backup Exfiltration**
Encrypted chain replica (Everest 32) uploaded to attacker-controlled cloud via misconfigured backup client. Replicas are encrypted with principal-controlled keys; exfiltration yields ciphertext only.
Defense: Everest 32 encrypted replication with keys held only by principal; Everest 33 recovery procedure from replica.
Summit: E32, E33.

---

## Category 9: Coercion

**CO01 — Rubber-Hose Signing**
Adversary physically compels principal to produce a valid attestation at gunpoint. Protocol provides no defense; this is an explicit out-of-scope item in the threat model.
Defense: Out of scope per v0 threat model (ZKBB_USER_PROTOCOL_v0.md §2); partial mitigation via duress codeword (Everest 58); coercion posture review (S231).
Summit: E58, S231.

**CO02 — Duress-Codeword Social Engineering**
Adversary, prior to a coercion event, elicits the duress codeword from the principal by posing as a Calm auditor. Codeword is never transmitted during normal protocol operation; its hash is stored only at enrollment.
Defense: Codeword is established at enrollment under ceremony conditions; codeword hash stored, never plaintext; social-engineering resistance is operational, not cryptographic (S231).
Summit: E58, E11, S231.

**CO03 — Codeword-Hash Preimage Attack**
Adversary holds the stored codeword hash and attempts to recover the codeword by brute-force, then uses it to suppress a genuine duress signal. SHA-256 preimage resistance; codeword entropy must be sufficient.
Defense: Codeword selected from a high-entropy space during enrollment (guidance documented in Everest 58 ceremony notes).
Summit: E58.

**CO04 — Environmental-Leverage Coercion**
Employer or housing provider conditions continued benefits on the principal producing favorable attestations. No cryptographic defense; behavioral-cadence monitoring provides soft signal.
Defense: Out of scope per v0 (S231 §2); trusted-verifier cadence monitoring (S231 principal guidance).
Summit: S231.

**CO05 — Threshold-Signing Coercion**
If multi-party signing threshold is adopted, adversary separately coerces enough co-signers to produce a coerced attestation. Threshold raises cost proportionally; does not eliminate the attack.
Defense: Multi-party key custody guidance (S231 principal guidance); no cryptographic solution at protocol layer.
Summit: S231.

**CO06 — Coerced Key Rotation**
Principal coerced to initiate key rotation to attacker-controlled key, transferring signing authority. Rotation event is logged to the chain and published to Sigsum; trusted verifiers see the rotation.
Defense: Rotation event in chain (Everest 17); Sigsum publication; trusted-verifier monitoring (S231).
Summit: E17, E30, S231.

---

## Category 10: Transparency-Log Fork

**TF01 — Sigsum Log Equivocation**
Sigsum operator presents one chain-head to the principal and a different chain-head to the verifier, creating a fork. Sigsum's gossip protocol distributes log heads; equivocation is detectable by any client comparing heads.
Defense: Sigsum multi-witness consensus; client-side head comparison; equivocation proof triggers Sigsum operator punishment (Everest 30, 93).
Summit: E30, E93.

**TF02 — History Rewrite After Capture**
Attacker captures the Sigsum log server and rewrites historical entries prior to a specific sequence number. All subsequent entries are invalidated because prior inclusion proofs no longer verify.
Defense: Append-only Merkle structure; inclusion proofs stored in vault (Everest 30); clients verify inclusion proofs independently.
Summit: E30.

**TF03 — Roughtime Desync Attack**
Adversary compromises one Roughtime server in the quorum and returns a skewed timestamp, pushing an old proof into the freshness window. Quorum of ≥5 independent servers; one rogue server cannot move the agreed time significantly.
Defense: Roughtime quorum policy (Everest 94); Everest 31 skew-threshold rejection.
Summit: E31, E94.

**TF04 — Inclusion-Proof Forgery**
Attacker fabricates a Sigsum inclusion proof (Merkle path) for a chain head that was never actually submitted. Merkle path verification against the known log root requires valid signatures from Sigsum witnesses.
Defense: Sigsum witness signatures are not forgeable; inclusion proof verification against current published tree root (Everest 30).
Summit: E30.

**TF05 — Log Partition During Propagation**
Network partition during Sigsum submission causes the chain head to appear in some witness views but not others. Degraded-mode policy: `anchor_pending` propagates to disclosure response as `unknown`; verifier treats `unknown` conservatively.
Defense: Everest 30 degraded-mode `anchor_pending` → `unknown` disclosure; verifier guidance in Everest 98.
Summit: E30, E98.

**TF06 — Retroactive-Anchor Backdating**
Attacker submits an old chain head to Sigsum with a falsified creation timestamp, claiming an earlier anchor than actually occurred. Sigsum timestamps are server-authoritative and co-signed by witnesses; falsified timestamps require multi-witness collusion.
Defense: Roughtime-attested timestamps co-published with chain heads; multi-witness Sigsum requirement (Everest 30, 31).
Summit: E30, E31.

---

## Category 11: Range-Proof Forgery

**RP01 — Completeness-Exploiting Forgery**
Attacker submits a proof asserting `d < τ` when `d ≥ τ`, exploiting a completeness gap in the Bulletproof implementation. Mutation tests (Everest 65 gate) reject all 7 mutation classes including `a0/a1/e0/e1/z0/z1/claimed_bit`.
Defense: Bulletproofs on Ristretto255 with soundness proven under DLOG; 7-mutation rejection suite in gate (Everest 65).
Summit: E65, E45.

**RP02 — Out-of-Range Biometric Value**
Attacker commits a biometric distance value outside the valid range `[0, 1]` and proves it is "below threshold." Range proof must bound the committed value; unsigned integer encoding enforces non-negativity.
Defense: 32-bit fixed-point encoding of `d` (Everest 44); Bulletproof bounds both ends of the range (Everest 45).
Summit: E44, E45.

**RP03 — Tau-Substitution Mid-Proof**
Generate a proof for threshold τ_1, then claim the proof verifies for a more permissive threshold τ_2 > τ_1. Verifier must check the proof against the committed threshold value, not a user-supplied parameter.
Defense: τ is bound into the Fiat-Shamir transcript; the verifier re-derives the challenge from the committed τ (Everest 45, 65).
Summit: E45, E65.

**RP04 — Commitment-Blinding Factor Leak**
Pedersen commitment's blinding factor `r` is inadvertently exposed via debug output, enabling the attacker to recover `d = (commitment - r*h) / g`. Zeroize after commitment; no blinding factor in logs.
Defense: Everest 81 Zeroize obligation; Everest 85 CI bans key-sized hex in log output; Everest 44 blinding factor is ephemeral.
Summit: E44, E81, E85.

**RP05 — Aggregated-Proof Substitution**
In a multi-predicate envelope, swap the aggregate proof so that one predicate's range proof is substituted for another's. Each proof is independently bound to its commitment and predicate ID in the Fiat-Shamir transcript.
Defense: Per-predicate `(commitment, proof)` pairs; Fiat-Shamir transcript includes `(predicate_id, commitment)` for each (Everest 65, 71).
Summit: E65, E71.

**RP06 — Trusted-Setup Backdoor (SNARK)**
If the system migrates to a SNARK-based proof requiring a trusted setup, a participant in the setup ceremony retains toxic waste enabling proof forgery. v0 uses Bulletproofs with no trusted setup.
Defense: v0 locked to no-trusted-setup Bulletproofs (Everest 45); any future SNARK migration requires a ceremony audit documented in the post-quantum plan (Everest 96).
Summit: E45, E96.

---

## Category 12: Chain Tamper

**CT01 — Record Payload Mutation**
Edit a `self_report.morning` record's `payload.affect` field after it is written. `record_hash` covers the full serialized record; mutation changes the hash, breaking `prev_hash` of the next record.
Defense: SHA-256 hash-chain construction (Everest 28); 14-case gate including payload-mutation rejection.
Summit: E28.

**CT02 — Record Deletion**
Delete a self-report record from the middle of the chain (JSONL line removal). The deleted record's hash is referenced by the next record's `prev_hash`; its absence breaks verification.
Defense: Chain verifier walks every record; deletion detected at the first hash mismatch (Everest 28).
Summit: E28.

**CT03 — Out-of-Band Append**
Append a crafted record to `user_state.jsonl` without using the vault append path, attempting to inject a consent grant or state record. Filesystem append-only flags (chflags+schg on macOS, chattr+a on Linux) block non-privileged writes; Sentinel daemon monitors FSEvents (Everest 27).
Defense: Append-only filesystem guarantees and monitoring (Everest 27).
Summit: E27.

**CT04 — Genesis-Block Swap**
Replace the genesis record with one binding a different operator identity or principal key. Genesis record's hash is the root of the chain; swap breaks `prev_hash` of record 1 and all subsequent records.
Defense: Genesis block schema with dual signatures (operator + principal); Sigsum anchors the genesis head on creation (Everest 29, 30).
Summit: E29, E30.

**CT05 — Clock-Skew Record Injection**
Inject records with timestamps set far in the past or future to pollute freshness evaluation. Roughtime-attested timestamps in chain anchors; records with timestamps outside the anchor window are flagged as anomalous.
Defense: Everest 31 Roughtime anchoring; chain verifier cross-checks record timestamps against inclusion-proof timestamps.
Summit: E31, E28.

**CT06 — Corruption-Recovery Exploit**
During a corruption recovery event (Everest 33), attacker substitutes a tampered replica before recovery completes, making the principal accept the tampered chain as canonical. Recovery procedure verifies replica against Sigsum head before accepting.
Defense: Everest 33 corruption recovery verifies replica chain head against Sigsum log before restoring.
Summit: E33, E30.

---

## Category 13: Predicate Poisoning

**PP01 — Evaluator-Hash Mismatch**
Attacker modifies `predicate_eval.py` to return `True` unconditionally, while the registry still shows the old `predicate_id_hash`. Determinism harness runs every predicate against a frozen corpus on CI and detects evaluator drift.
Defense: Predicate canonical form hash (Everest 52); determinism harness (Everest 63); CI enforces hash stability.
Summit: E52, E63.

**PP02 — Golden-Corpus Corruption**
Attacker modifies the golden corpus JSON to match a broken evaluator, making CI pass for a wrong implementation. Golden corpus is content-addressed and stored alongside the evaluator hash snapshot at predicate registration.
Defense: Evaluator-hash snapshot written at Everest 6 registration; corpus content-addressable; independent peer review mandated (Everest 54).
Summit: E64, E54.

**PP03 — `cognitively_atypical_baseline` Truthy Coercion**
Pass a string `"True"` or integer `1` to the enrollment flags where a strict boolean `True` is required. Evaluator uses `is True` identity check, not truthy coercion; non-bool True rejected (Everest 59 corpus case: non-bool-True).
Defense: Everest 59 strict-boolean identity check; 10-case golden corpus including truthy-coercion cases.
Summit: E59.

**PP04 — `mental_state_unusual` Empty-Baseline Trigger**
Evaluate `mental_state_unusual` against an empty enrolled baseline expecting vacuous-disjoint to trigger `True`, falsely signaling the principal is unusual. Empty-baseline fix deployed after corpus expansion caught the defect.
Defense: Non-empty enrolled baseline required before affect branch evaluates; fixed defect documented in Everest 64.
Summit: E60, E64.

**PP05 — `compose_not` Unsound Negation**
Evaluate `NOT(unknown)` and assert the result is `False`, using absence of evidence as proof of negation. `compose_not` maps `Unknown → Unknown`; negation of unknown is unknown, not false.
Defense: Everest 62 NOT(Unknown) = Unknown invariant; gate includes attack scenario (empty chain + NOT applied) to verify no unsound True is produced.
Summit: E62.

**PP06 — Predicate DSL Injection**
If a DSL is added in a future version, inject a predicate expression that evaluates arbitrary code or accesses out-of-scope chain data. v0 is locked to a fixed predicate table (no DSL) per Everest 51.
Defense: Everest 51 decision: fixed predicate table for v0; DSL deferred; when DSL is introduced, it is sandboxed and scope-limited.
Summit: E51.

---

## Category 14: Denial-of-Service

**DS01 — Chain-Flood**
Flood `user_state.jsonl` with millions of valid-schema records to make chain verification prohibitively slow. Chain verification is O(N); rate-limiting at the vault append layer prevents unconstrained growth.
Defense: Everest 27 append-only path controls write rate; evaluation performance target (Everest 88: 50-record chain verifies in 0.4ms).
Summit: E27, E88.

**DS02 — Sigsum Submission Spam**
Flood the Sigsum log with spurious chain heads from fabricated principals to exhaust log capacity or delay legitimate submissions. Sigsum operator policy controls submission rate; Everest 93 governs operator selection.
Defense: Sigsum operators apply rate-limiting; CredexAI VC required to authenticate submissions (Everest 68, 93).
Summit: E68, E93.

**DS03 — Roughtime Overload**
Exhaust the Roughtime quorum with requests from Calm operator nodes, making timestamp anchoring unavailable. Everest 94 requires ≥5 independent Roughtime servers; overload of one does not block quorum.
Defense: Everest 94 quorum of ≥5 independent Roughtime servers; quorum policy survives one-server denial.
Summit: E31, E94.

**DS04 — Proof-Verification Loop Bomb**
Submit a crafted `BitProof` whose verification triggers an unbounded computation loop (e.g., pathological Σ-protocol transcript). Verifier applies a CPU-time ceiling before accepting a proof as valid.
Defense: Everest 85 CI adversarial fuzzer targets proof pipeline; Everest 88 performance budget contractual (verifier ≤72ms per predicate).
Summit: E85, E88.

**DS05 — Consent-Revocation Flood**
Flood the chain with rapid `consent.grant` / `consent.revoke` alternations to force the evaluator to traverse an arbitrarily long history. Latest-wins evaluation requires traversing the full chain; rate limiting consent-record writes caps the cost.
Defense: Rate-limiting via Everest 76 (per-predicate rate limits); Everest 27 append-only write controls.
Summit: E76, E27.

**DS06 — Vouching-as-Spam Graph Attack**
Flood the ZKAC trust graph with low-cost vouches targeting many principals to degrade graph query performance. Per-vouch micro-stake requirement (S174); vouch velocity caps per principal per epoch (S187/A13).
Defense: S174 per-vouch micro-stake; epoch velocity cap (S187/A13).
Summit: S187 (A13).

---

## Category 15: Oracle Attack

**OA01 — Biometric Distance Oracle via Binary Predicate**
Repeatedly query `biometric_match_within(τ)` with incrementally varying τ to binary-search the committed distance. Each query requires a new signed disclosure request from the counterparty; rate-limiting (Everest 76) caps queries per epoch.
Defense: Per-predicate, per-class rate limits (Everest 76); commitment is binding so distance does not change between queries, but the rate limit caps information gain.
Summit: E76, E45.

**OA02 — Chain-Head Timing Oracle**
Query for a disclosure immediately after a self-report and compare with a query immediately before, inferring whether a self-report record was written in the interval. Disclosure response does not reveal record count or timestamps inside the window.
Defense: Envelope cardinality and timestamp non-disclosure properties (Everest 71); count-of-records must not leak.
Summit: E71.

**OA03 — Predicate-Boundary State Oracle**
Probe the `in_baseline_24h` predicate at T=23h59m and T=24h01m to determine when a state record was written. Freshness window boundary reveals nothing more precise than "within 24 hours."
Defense: Predicate returns a binary bit for the declared window; sub-window timing does not leak (Everest 55).
Summit: E55.

**OA04 — Duress-Bit Oracle via Vouch Correlation**
Correlate the `bank_teller_note_active` bit with social signals (principal's communication patterns) to map the codeword activation to specific threat events. Protocol layer cannot prevent off-chain signal correlation; this is an operational coercion-resistance limit.
Defense: Partial: codeword is never exposed in protocol; off-chain correlation is out of scope; trusted-verifier model (S231) manages the duress channel.
Summit: E58, S231.

**OA05 — Template-Age Oracle via Consistency Proof**
Probe cross-template consistency proofs with varying held-out sample sets to estimate the age of the enrolled template. Consistency proof reveals drift budget satisfaction, not template age.
Defense: Consistency proof (Everest 48) discloses only drift-budget pass/fail, not timestamp or age.
Summit: E48.

---

## Category 16: Agent-Identity / Calm-Pact Composition

**AI01 — Pact Bypass — Claim Passed Without Proof**
Attacker claims Calm Pact equality verified in a prior session and asks Calm Witness to proceed without re-running Pact. Two-handshake protocol requires Pact verification before Witness; Pact-fail aborts with zero Witness bytes transmitted.
Defense: Composition protocol: Pact-then-Witness strict ordering; Pact-fail abort (Everest 97).
Summit: E97.

**AI02 — Session-ID Binding Bypass**
Run Calm Pact between agents A and B. Substitute agent B for agent C and run Calm Witness, claiming the Pact result applies. Session ID is Fiat-Shamir bound into the Witness transcript; cross-session reuse fails transcript verification.
Defense: Session-id binding via Fiat-Shamir transcript across both handshakes (Everest 97).
Summit: E97.

**AI03 — Operator-Identity Mismatch**
Operator signs a Witness disclosure with one Ed25519 key but presents a VC issued to a different key. Verifier checks that the signing key matches the VC's public key field; mismatch rejected.
Defense: Ed25519 signing key fingerprint = SHA-256(public key bytes) = operator VC ID field; mismatch is detectable (Everest 68).
Summit: E68.

**AI04 — Cross-Protocol Replay (Pact Proof in Witness Slot)**
Present a Calm Pact equality proof in the Witness predicate-proof slot. Proof transcript is domain-separated; Witness Σ-protocols include a domain string that Pact transcripts do not.
Defense: Domain separation in Fiat-Shamir transcript; cross-envelope swap is a named mutation class in the Everest 65 gate.
Summit: E65, E97.

**AI05 — Agent-Impersonation via Cloned Counterparty VC**
Attacker clones a legitimate counterparty's VC metadata (excluding the private key) and presents it to the Calm operator as if they were the legitimate counterparty. VC signature is not forgeable; verifying the VC against CredexAI's trust anchor catches a cloned-metadata VC.
Defense: Counterparty identity binding (Everest 69); CredexAI VC validation against public trust anchor.
Summit: E69.

**AI06 — Calm Pact Directive-Mismatch Exploitation**
Two agents with non-aligned directives collude to produce a Calm Pact success signal despite inequality. Σ-protocol equality proof is computationally binding; producing a false equality proof requires breaking DLOG on Ristretto255.
Defense: Calm Pact Σ-protocol soundness under DLOG (Calm Pact v0 §4); Everest 97 abort on Pact failure.
Summit: E97.

---

## Cited Everest Summits

| Everest | Pillar | Summary |
|---|---|---|
| E11 | Witness | Enrollment ceremony spec (air-gap, witness, artifacts) |
| E13 | Witness | Voice-transcription-only pipeline (audio destroyed immediately) |
| E16 | Witness | Template encryption and key custody (HSM-bound) |
| E17 | Witness | Template version migration |
| E19 | Witness | Re-enrollment red-flag detection |
| E20 | Witness | Enrollment witness protocol (3-tier; witnesses see commitment only) |
| E22 | Witness | Enrollment → CredexAI VC issuance |
| E26 | Witness | JSONL schema v0 (additionalProperties:false; 30-case corpus) |
| E27 | Witness | Append-only filesystem guarantees (chflags / chattr / FSEventStream) |
| E28 | Witness | Hash-chain construction and verification |
| E29 | Witness | Genesis block and provenance (dual signatures) |
| E30 | Witness | Chain-head publication to Sigsum |
| E31 | Witness | Roughtime / verifiable-clock anchoring |
| E32 | Witness | Encrypted chain replication |
| E33 | Witness | Corruption recovery |
| E41 | Witness | Adversarial biometric robustness |
| E44 | Witness | Pedersen commitment to distance value (Ristretto255) |
| E45 | Witness | ZK range proof (Bulletproofs, no trusted setup) |
| E46 | Witness | Pedersen commitment to template ID |
| E47 | Witness | Template aging without breaking proofs |
| E48 | Witness | Cross-template consistency proof |
| E49 | Witness | Liveness detection at capture time |
| E51 | Witness | Predicate language v0 (fixed table, no DSL) |
| E52 | Witness | Predicate canonical form and content-addressable ID |
| E54 | Witness | Predicate audit and public review process |
| E55 | Witness | `in_baseline_24h` predicate |
| E57 | Witness | `principal_consents_to_disclose` predicate |
| E58 | Witness | `bank_teller_note_active` (duress primitive) |
| E59 | Witness | `cognitively_atypical_baseline` predicate |
| E60 | Witness | `mental_state_unusual` predicate |
| E61 | Witness | Predicate AND/OR composition |
| E62 | Witness | Predicate negation (NOT(Unknown) = Unknown) |
| E63 | Witness | Predicate determinism harness |
| E64 | Witness | Predicate test corpus (193 cases; caught real defect) |
| E65 | Witness | Predicate ZK proof generator (Σ-protocol, Fiat-Shamir) |
| E68 | Witness | Operator identity binding (Ed25519 real signing) |
| E69 | Witness | Counterparty identity binding |
| E70 | Witness | Replay defense (nonce in request) |
| E71 | Witness | Selective disclosure multi-predicate envelope |
| E75 | Witness | Consent revocation propagation |
| E76 | Witness | Rate limits per predicate per class |
| E81 | Witness | Rust production implementation (Zeroize, constant-time) |
| E85 | Witness | CI adversarial fuzzers (7 targets, ≥18 fuzzer-hours/night) |
| E88 | Witness | Proof-generation performance budget |
| E90 | Witness | Third-party security audit prep |
| E91 | Witness | NIST / US AI Safety Institute submission |
| E92 | Witness | Open-source release (Apache-2.0) |
| E93 | Witness | Sigsum operator selection (≥3 independent) |
| E94 | Witness | Roughtime operator selection (≥5, quorum policy) |
| E96 | Witness | Post-quantum migration plan |
| E97 | Witness | Composition with Calm Pact in production |
| E98 | Witness | Counterparty implementer's guide (wire format) |
| E100 | Witness | Independent third-party end-to-end verification |
| S174 | ZKAC | Proof-of-cost floor for ZKAC registration |
| S175 | ZKAC | Vouch-type schema (basis field, conflict-of-interest) |
| S176 | ZKAC | Transitive decay model (multiplicative, max 4 hops) |
| S179 | ZKAC | Revocation propagation |
| S185 | ZKAC | Anti-collusion sampling (motif analysis) |
| S186 | ZKAC | Witness quorum rules (verifiable randomness, rotation) |
| S187 | ZKAC | Trust-network adversarial catalog (A01–A15) |
| S231 | Coercion | Coercion-resistance posture review |

---

*Total attacks: 100. Categories: 16 (replay, substitution, fake-compliance, side-channel, governance-capture, vouching-ring, parser-fuzz, key-extraction, coercion, transparency-log-fork, range-proof-forgery, chain-tamper, predicate-poisoning, denial-of-service, oracle-attack, agent-identity). All attacks reference the protocol property under test and the defense summit where bagged.*

Calm 2026-05-20
