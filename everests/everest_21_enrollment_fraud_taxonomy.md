# Everest 21 — Enrollment Fraud Taxonomy

*Phase II — Capture & Enrollment. Prereq: Everest 11, Everest 9.*

An enrollment ceremony (Everest 11) produces biometric templates that bind every later Calm Witness proof to the principal's identity. If the ceremony is compromised, the templates are poisoned: an attacker can craft samples that match a fake template and claim to be the principal. This summit enumerates the attacks that can corrupt an enrollment, specifies countermeasures, and identifies which attacks are accepted residual risk in v0.

---

## Enumerated Attacks

### CATEGORY A: Substitution Attacks

**EF01 — Identity Substitution at Ceremony**

A different human physically attends the enrollment ceremony posing as the principal, provides biometric samples under the principal's name, and exits.

- Attacker capability: Must know the principal's legal name, the ceremony date/location, and must resemble them sufficiently to pass casual visual inspection. No cryptographic key or identity credential is needed.
- Difficulty: Medium. Requires social engineering or collusion with a witness.
- Detection: Anti-substitution witness (Everest 11 §2, recommended role) who has known the principal for ≥5 years and attends solely to attest identity — without seeing template content — can visually detect an imposter. Biometric distance checks at disclosure time (Everest 45) will detect any sample from a non-principal that differs materially from the poisoned template.
- Countermeasure: Mandatory anti-substitution witness for any principal unknown to the capture witness. The witness signs an affidavit attesting to identity. Notarization (Everest 11 §2, optional in v0) adds a licensed third party who checks government ID. Identity binding to the witness' CredexAI VC raises collusion cost.
- Residual risk: A determined attacker with two corrupted witnesses can enroll an imposter. The protocol accepts this risk; substitution is prevented by multi-witness requirement and notarization, not by cryptography.
- Related everests: E11 (anti-substitution witness), E45 (biometric distance proofs), E20 (witness enrollment), E22 (continuous-state cross-checks).

**EF02 — Hand-Substitution**

The principal is physically present at the ceremony, but a different person provides the handwriting samples while the principal observes or is detained in an adjacent room.

- Attacker capability: Must have physical access to the ceremony space and the capability to substitute a second person's hand on the stylus tablet during the handwriting portion (E11 §E). Requires either corruption of a witness or surreptitious access.
- Difficulty: High. Requires in-room coordination; the principal's presence at the coercion-check (E11 §G) would expose the deception if the principal is lucid.
- Detection: The principal's opening statement (E11 §C) is voice-captured; if the voice sample at E11 §F does not match the voice from the opening statement, the cross-modal consistency check (Everest 48) flags a material divergence. Witness testimony that the principal was present and in control of their limbs throughout supports detection.
- Countermeasure: Continuous witness supervision of all biometric capture phases (E11 §1, §E, §F). The witness attests that the principal's hands/voice were used throughout. Continuous video recording (Everest 12, optional hardware attestation) of the biometric session preserves evidence for post-ceremony audit.
- Residual risk: A witness under coercion can lie. The protocol relies on multi-witness attestation to raise the collusion bar.
- Related everests: E11 (ceremony spec), E12 (capture device attestation), E48 (cross-template consistency), E49 (liveness detection).

**EF03 — Voice-Substitution**

The principal is present, handwriting samples are captured from the principal's hand, but voice-transcription samples are played back audio or spoken by a different person.

- Attacker capability: Must supply pre-recorded or live audio of a different speaker during E11 §F (voice-transcription templates). Requires either suppression of the principal's voice or a second speaker in the room.
- Difficulty: Medium-to-High. The voice pipeline (Everest 13) transcribes locally under real-time capture; playback is detectable if the microphone is live. A second speaker requires witness complicity or principal coercion.
- Detection: Liveness detection (Everest 49) examines inter-keystroke timing entropy in the transcript and acoustic micro-variation in the microphone stream. Pre-recorded or synthesized voice lacks real-time variation. Witness observation of the principal's mouth and presence of a second speaker in the room (a clear violation of E11 §2 "no bystanders") is obvious.
- Countermeasure: Real-time microphone capture without pre-recording playback capability in the room (Everest 11 §4, disallowed items). Witness attestation that only the principal spoke. Liveness-detection entropy checks on the transcript. Everest 49 hardware attestation that the microphone was not fed synthetic audio.
- Residual risk: A technically capable attacker can synthesize voice with high realism; liveness detection may not be foolproof against future synthetic-voice models. The protocol mitigates by combining witness attestation + liveness checks + cross-modal consistency proofs.
- Related everests: E11 (ceremony spec, microphone controls), E13 (voice-transcription pipeline), E49 (liveness detection), E48 (cross-modal consistency).

**EF04 — Document Substitution**

The principal's enrollment ceremony is conducted and templates are captured correctly. The witness signs the Pedersen-commitment record binding the templates to the principal's identity. After the signing, but before publication to Sigsum, an attacker swaps the signed commitment for one derived from a different person's templates, keeping the same witness signature and ceremony metadata.

- Attacker capability: Must have write access to the vault or to the commitment record before Sigsum publication. Requires either vault compromise or operator compromise at a critical moment.
- Difficulty: Very-High. The attacker must forge a valid signature or have possession of the witness's hardware token, and must do so before the record is published to Sigsum (which makes retroactive substitution detectable).
- Detection: The witness's signature binds to the original `record_hash` via `sha256(prev_hash + payload)`. If the payload is mutated after signing, the signature no longer verifies. Sigsum's inclusion proof also commits to the original hash. Any attempt to publish a mutated record to Sigsum will fail the hash-tree proof.
- Countermeasure: Immediate publication to Sigsum (Everest 11 §H, step 5) before the witness departsthe ceremony. Witness signature verification (Everest 28, `verify-chain`) catches any retroactive mutation. The binding to the transparency log (Everest 30–31) is the primary defense: once published, the record is append-only and immutable across the witness set.
- Residual risk: None. If publication is delayed, an attacker with vault + operator access could mutate the record. Requiring same-session Sigsum publication eliminates this window.
- Related everests: E11 (ceremony script and sealing), E28 (chain verification), E30–31 (Sigsum anchoring), E20 (witness token custody).

---

### CATEGORY B: Coercion Attacks

**EF05 — Principal Coerced at Ceremony**

A principal is held under duress (gunpoint, threats, confinement) and forced to enroll in an attacker-controlled ceremony while appearing cooperative.

- Attacker capability: Physical presence and power over the principal's environment. No cryptographic capability required.
- Difficulty: Low. Rubber-hose attacks are always feasible.
- Detection: The coercion-check moment (Everest 11 §G) asks the principal if they are proceeding voluntarily. If the principal is under coercion and cannot signal safely, the check fails to detect it. A witness with private doubt can signal post-ceremony (E11 §G footnote), triggering Everest 19 (re-enrollment red-flag detection). The bank-teller-note duress codeword (Everest 58, 65) allows a principal to signal coercion without revealing it.
- Countermeasure: Procedural — the coercion-check moment is mandatory and the principal can abort without explanation (E11 §1). Cryptographic — the duress codeword feature (Everest 58) allows the principal to embed a secret phrase that flips a bit at disclosure time, alertable to trained counterparties. Witness testimony that the principal appeared uncoerced at the time of ceremony.
- Residual risk: ACCEPTED. No protocol defends against coercion of the principal themselves. This is the universal rubber-hose attack. Calm Witness mitigates by offering a duress signal (the bank-teller-note bit) so the principal can request help without explicitly asking.
- Related everests: E11 (ceremony script), E58 (duress codeword), E65 (bank-teller-note predicate), E19 (re-enrollment red-flags), E78 (stealth disclosure).

**EF06 — Witness Coerced**

A capture witness or anti-substitution witness is coerced (bribed, threatened, blackmailed) into signing the Pedersen commitment without observing the ceremony or despite observing a substitute or forged samples.

- Attacker capability: Information about or leverage over a witness outside the ceremony. Can occur before, during, or after the ceremony.
- Difficulty: Medium. Requires pre-ceremony intelligence about the witness and collusion setup. Detecting coercion requires either the witness self-reporting or anomalous behavior post-ceremony.
- Detection: Everest 19 (re-enrollment red-flag detection) monitors for pattern breaks: if a re-enrollment ceremony produces drastically different templates from the first, or if a witness reports post-ceremony that they were coerced, the system escalates. Auditing the witness's signature history and affiliations (Everest 20) can reveal patterns suggesting paid/compromised attestations.
- Countermeasure: Multi-witness requirement (Everest 11 §2) — both capture witness and anti-substitution witness must sign. Collusion of all witnesses raises the cost significantly. Witness identity binding to CredexAI VCs (Everest 20) allows revocation and audit. Witness compensation documentation (Everest 11 §10 open question) makes paid attestations explicit and auditable. Post-ceremony witness interviews (Everest 19) allow witnesses to self-report coercion.
- Residual risk: ACCEPTED. A determined attacker can coerce multiple witnesses. The protocol mitigates by requiring multiple independent witnesses and by enabling witnesses to report coercion retroactively.
- Related everests: E11 (multi-witness requirement), E20 (witness identity and key custody), E19 (re-enrollment red-flags), E48 (cross-template consistency checks).

**EF07 — Operator Coerced**

The Calm operator is coerced (threatened, extorted, subverted by supply-chain compromise) into:
(a) sealing a poisoned template derived from a substitute's biometrics under the principal's name, or
(b) falsely attesting that a ceremony occurred when it did not.

- Attacker capability: Possession of the operator's private key or control of the operator's software/hardware. Requires either operator compromise or control over the operator's environment.
- Difficulty: Medium. Requires either a sophisticated supply-chain attack or blackmail of the operator. The operator cannot unilaterally forge a proof without also corrupting the vault state.
- Detection: The operator's signature on the enrollment record binds to the witness signatures and the Sigsum-published chain head. If an attacker uses the compromised operator key to seal a fake enrollment, the witnesses' signatures are absent (because the ceremony did not occur) and the record does not appear in Sigsum's timeline. Everest 28 (verify-chain) checks for missing witness signatures and will flag the enrollment as unsigned (and thus likely forged). Everest 72 (disclosure audit log) shows which operator issued each proof.
- Countermeasure: Witness signatures are mandatory; an enrollment without them is invalid (Everest 11 §I). Immediate Sigsum publication (Everest 11 §H) before the operator has an opportunity to mutate the record. Operator key rotation on suspected compromise (Everest 68). Revocation of the operator's CredexAI VC invalidates all proofs from that operator.
- Residual risk: MITIGATED. The witness requirement and Sigsum anchoring prevent an operator from unilaterally forging an enrollment. An operator under coercion must also coerce the witnesses, raising the collusion bar.
- Related everests: E11 (ceremony script, witness requirement), E28 (chain verification), E30–31 (Sigsum anchoring), E68 (operator identity and key rotation), E72 (disclosure audit log).

**EF08 — Notary Compromise**

A licensed notary public is bribed or in collusion with an attacker. The notary attests (falsely) that a ceremony occurred on a specified date and location, or that a principal was present and uncoerced, when in fact the ceremony did not occur or was forged.

- Attacker capability: Corruption of a single notary. Notaries are optional in v0 (E11 §2, §10) so this attack is not live until notarization is mandated in v1+.
- Difficulty: Medium. A notary can be bribed or socially engineered. Notary fraud is a known category of document forgery.
- Detection: In v1+, the notary's signature and license number are included in the enrollment manifest (E11 §7). A verifier can check the notary's license status with the relevant state board. If the notary is revoked or if the notary's license was not active on the ceremony date, the manifest is invalid. Everest 34 (notary registry and revocation) provides a public attestation of notary licenses and revocations.
- Countermeasure: Notary licensing and regulation by the state — outside Calm's control. Everest 34 integrates notary license verification. Multi-witness requirement (E11 §2) is the primary defense; a compromised notary alone cannot forge an enrollment without also corrupting both the capture witness and anti-substitution witness. In v1+, notary fraud is a crime; legal consequences deter corruption.
- Residual risk: MITIGATED by multi-witness requirement. A notary is a tertiary check; the primary defenses are the witnesses' signatures and Sigsum's append-only timeline.
- Related everests: E11 (ceremony spec, optional notary), E34 (notary registry and revocation check), E20 (witness identity).

---

### CATEGORY C: Replay / Capture-Time Attacks

**EF09 — Pre-recorded Handwriting Replay**

An attacker supplies a stylus tablet that is secretly running a playback mode. During the handwriting-capture phase (E11 §E), the attacker plays back a pre-recorded sequence of stylus strokes (captured from a prior ceremony or forged digitally) instead of capturing live strokes from the person present.

- Attacker capability: Must either supply or compromise the stylus tablet used in the ceremony. Requires knowledge of the tablet's OS and stylus driver, and the ability to compile and load custom firmware or software.
- Difficulty: Very-High. Modern stylus tablets have secure-boot mechanisms and attestation protocols (Everest 12). A hardware supply-chain compromise is needed or a zero-day in the tablet's OS.
- Detection: Liveness detection (Everest 49) examines low-level stylus entropy: pressure micro-variation, jitter in x/y coordinates, temporal randomness in acceleration. A perfectly replayed stroke sequence lacks natural entropy. The capture device logs inter-stroke timing data (Everest 12). Consistency checks (Everest 48) compare the handwriting sample to the principal's historic samples; a sample from a different human will produce feature vectors far from the baseline, triggering a red-flag alert.
- Countermeasure: Hardware attestation of the stylus tablet (Everest 12, TPM or Secure Enclave) signing the raw stroke manifest. Liveness-detection entropy analysis (Everest 49) rejects samples with insufficiently high entropy. Witness observation of the principal's hand on the stylus tablet throughout the capture phase. Re-enrollment consistency checks (Everest 48) detect drift anomalies.
- Residual risk: MITIGATED. An attacker cannot forge the TPM-signed stroke manifest; they would have to compromise the TPM itself, which is a nation-state-level effort. Liveness detection combined with witness observation raises the bar very high.
- Related everests: E11 (ceremony script, witness supervision), E12 (capture-device attestation), E49 (liveness detection), E48 (consistency checks).

**EF10 — Pre-recorded Voice Replay**

An attacker plays back pre-recorded audio instead of capturing the principal's live voice during E11 §F.

- Attacker capability: Must have control of the audio playback on the ceremony device or must switch the microphone input to a pre-recorded source. Requires device compromise or room manipulation.
- Difficulty: High. Modern microphones can detect playback if the audio is fed back through speakers (acoustic artifacts). An attacker would need to inject audio directly into the microphone input or replace the microphone.
- Detection: Liveness detection (Everest 49) includes acoustic entropy checks: inter-keystroke timing in the transcript and micro-variations in the audio stream that are present in live speech but absent in high-fidelity playback. The microphone is wired (no Bluetooth) and supervised by the witness (E11 §F). If the playback audio comes from a speaker in the room, the witness can observe it.
- Countermeasure: Wired, supervised microphone (E11 §4, disallowed Bluetooth). Real-time transcription (Everest 13) with no pre-playback capability in the room. Witness observation of the principal's mouth and vocal output. Liveness-detection entropy checks reject audio with insufficient variation. Everest 12 microphone attestation ensures the device is not firmware-compromised.
- Residual risk: MITIGATED. A perfectly cloned voice is difficult to distinguish from live speech, but liveness-detection entropy and witness observation together raise the bar significantly.
- Related everests: E11 (ceremony spec, microphone controls), E13 (voice-transcription pipeline), E49 (liveness detection), E12 (device attestation).

**EF11 — Partial-Capture Attack**

The capture device firmware is subtly tampered with to intentionally drop a fraction of the kinematic data during biometric capture — e.g., ignoring pressure variations, dropping every Nth coordinate sample, or zeroing out jitter. The resulting template is weaker than intended and is more vulnerable to imitation by a different human in future attacks.

- Attacker capability: Must tamper with the capture device's firmware before the ceremony. Requires either a supply-chain compromise or pre-ceremony device substitution.
- Difficulty: High. The attacker must understand the biometric template format well enough to weaken it without making the tampering obvious. The device must still function normally for the witness and principal to notice nothing amiss.
- Detection: Everest 12 (capture-device attestation) includes a TPM-signed manifest of the raw samples. If the manifest shows fewer data points than expected (e.g., fewer pressure samples than should be recorded at the device's nominal sampling rate), the attestation fails. A subsequent liveness-detection check (Everest 49) re-captures the handwriting and voice samples under a known-good device; if the re-captured samples have notably higher entropy, a drift anomaly is flagged.
- Countermeasure: Hardware attestation (Everest 12) that signs the raw sample manifest, including sample count and metadata. Witness verification that the capture device is functioning normally (E11 §4, dry-run). Re-enrollment after a fixed interval (Everest 18) with a different device re-captures templates and enables consistency checks (Everest 48); material divergence triggers investigation.
- Residual risk: MITIGATED. A firmware tamperer must craft the tampering to be invisible to the attestation system. If the attestation counts samples and checks that they match the device's nominal rate, the tampering is caught. If the tampering is very subtle (e.g., dropping a small fraction of pressure readings), it weakens the template but does not cause immediate detection — the residual risk is that future imitations are more likely. The protocol mitigates by re-enrollment (detecting the weakness in a new ceremony) and by biometric-distance thresholds that adapt to weaker templates.
- Related everests: E12 (capture-device attestation), E49 (liveness detection), E18 (re-enrollment cadence), E48 (consistency checks), E39 (drift modeling).

**EF12 — Capture-Device Firmware Tamper**

The stylus tablet's firmware is modified to emit subtly altered kinematic data — not to drop data, but to transform it. For example, pressure values are scaled differently, x/y coordinates are rotated by a small angle, or timing is accelerated. The resulting samples appear legitimate but differ slightly from the true principal's samples.

- Attacker capability: Supply-chain compromise of the stylus tablet or pre-ceremony device substitution. Requires the attacker to understand the biometric template format and to apply transformations that pass visual inspection but are detectable in the feature vectors.
- Difficulty: Very-High. The transformations must be subtle enough not to be obvious when the principal writes, but sufficient to bias the template. The attacker must model how the transformed template interacts with future samples from both the principal and an attacker's hand.
- Detection: Everest 12 (capture-device attestation) includes raw-sample cryptographic hashing and TPM-signed manifest. If the raw samples are mutated, the hash changes and the TPM signature fails to verify. Witness observation of the writing and the rendered glyph image can detect obvious distortions. Cross-modal consistency checks (Everest 48) detect anomalies when handwriting and voice samples are compared. Subsequent liveness-detection re-captures (Everest 49) on known-good hardware will show the drift and trigger investigation.
- Countermeasure: Hardware attestation with TPM-signed raw-sample hashes (Everest 12). This is the primary defense: any tampering that mutates the raw bytes will change the hash. Witness observation of writing behavior. Re-enrollment with a different capture device (Everest 18, E11 §10 consideration) enables detection of systematic drift. If suspected, the principal can request forensic analysis of the tablet (e.g., dumping firmware and comparing to the manufacturer's baseline).
- Residual risk: MITIGATED. The TPM attestation binds the proof to the raw samples as they were captured; any later tampering is detectable. The risk is only live if the tampering occurs before the TPM computes the hash — i.e., at the firmware level at capture time. This is prevented by secure-boot mechanisms and supply-chain authentication (Everest 14).
- Related everests: E12 (capture-device attestation), E14 (secure-boot verification), E49 (liveness detection), E48 (consistency checks), E18 (re-enrollment with alternate devices).

---

### CATEGORY D: Side-Channel Attacks

**EF13 — Network-Side Leakage**

The ceremony device has a network interface (Ethernet, WiFi, cellular modem) that is supposedly in airplane mode but is actually active or has been re-enabled between the pre-ceremony check and the ceremony. Biometric samples or template data are exfiltrated over the network to an attacker.

- Attacker capability: Surreptitious re-enabling of the device's network interface or supply of a device with a hidden modem. Requires either device compromise or physical manipulation during ceremony setup.
- Difficulty: Medium. A hidden modem would require sophisticated hardware modification. Re-enabling a WiFi radio is trivial if the operator is compromised. Airplane-mode enforcement is procedural, not cryptographic.
- Detection: Everest 11 §A (room sweep) includes a radio-check tool that verifies airplane mode by detecting RF emissions. If the tool is bypassed or unavailable, network connectivity is not verified. Everest 12 (device attestation) should include a TPM-signed audit log of the device's radio state throughout the ceremony. If the log shows a re-enabling event, the ceremony is invalidated.
- Countermeasure: Mandatory radio-check tool before and after the ceremony (E11 §A). Hardware attestation (Everest 12) logging all radio state changes and signing them with the TPM. If any exfiltration is detected, the ceremony is aborted and restarted on a different device. Witness observation that the device remains isolated (E11 §1, air-gap principle).
- Residual risk: MITIGATED. An attacker with pre-ceremony access to the device can install a hidden modem that bypasses the radio-check tool. This is a supply-chain risk, not a ceremony-protocol risk. Everest 14 (secure-boot verification) mitigates by validating the device's firmware before ceremony start.
- Related everests: E11 (air-gap principle, room sweep), E12 (device attestation), E14 (secure-boot, firmware validation), E30 (network partition resilience).

**EF14 — Memory Disclosure**

An attacker with physical access to the ceremony device (before, during, or after the ceremony) reads the device's RAM to extract plaintext templates, encryption keys, or witness signatures.

- Attacker capability: Physical access to the device. Requires either forensic skills or a hardware reader (e.g., a Microchip programmer or a cold-boot attack).
- Difficulty: Medium. Cold-boot attacks and DRAM forensics are well-established. A determined attacker can extract memory contents post-ceremony if the device is not immediately powered down and wiped.
- Detection: Everest 11 §J (close-out) includes "power down the capture host." Once powered down, the DRAM is inaccessible unless the attacker has a forensic tool before shutdown. Post-ceremony, the principal owns the device and can verify that the device is powered down. If the device is later found to have been accessed (e.g., by forensic evidence or by the operator's audit log showing unexpected power-on events), the ceremony is invalidated.
- Countermeasure: Immediate power-down after sealing (E11 §H, §J). Use devices with DRAM encryption and secure erase on shutdown (Everest 12 hardware requirement). Witness observation that the device is powered down and remains in the principal's custody. If there is a time gap between sealing and shutdown, the device should be power-cycled (triggering DRAM wipe) before the gap ends.
- Residual risk: MITIGATED. A very fast attacker with a forensic tool could extract memory during the ~5 minute gap between sealing and shutdown. This is accepted as a low-probability risk mitigated by witness supervision and device ownership.
- Related everests: E11 (ceremony close-out), E12 (device hardware requirements), E16 (template encryption at rest).

**EF15 — Optical / Acoustic Side Channel**

An attacker positioned outside the ceremony room observes the principal's hand movements (through a window or via a hidden camera) or listens to the principal's voice (through a door, wall, or via a hidden microphone) and uses the observations to forge biometric samples.

- Attacker capability: Visual or acoustic line-of-sight to the principal during biometric capture. Requires a position near the ceremony room and the ability to record observations.
- Difficulty: Medium. Observing handwriting through a window or listening to voice through a door is possible but requires proximity. A sophisticated attacker could plant a hidden camera or microphone.
- Detection: Everest 11 §2 ("no cameras, no smart speakers") and §A (room sweep) are procedural. If a hidden camera or microphone is found, the ceremony is aborted. Post-ceremony, if an attacker leaks a forged sample to a biometric verifier, the distance metric will show a poor match to the enrolled template (because the attacker is a different human). Everest 45 (biometric distance proofs) will reject the sample.
- Countermeasure: Physical security of the ceremony room (door lock, window coverings if needed). Witness sweep to detect hidden cameras / microphones. Disassembly and inspection of the capture device before ceremony to ensure no hidden microphones or cameras. Biometric-distance checks at disclosure time that reject samples that do not match the template.
- Residual risk: ACCEPTED. A sophisticated attacker can always plant a camera or microphone if they have room access. The protocol mitigates by procedural room security (E11) and by the biometric distance check at disclosure time (Everest 45) that prevents an attacker's imitation from being accepted.
- Related everests: E11 (room security), E45 (biometric distance proofs), E49 (liveness detection).

---

### CATEGORY E: Time-Shift / Sequence Attacks

**EF16 — Backdated Enrollment**

An attacker forges an enrollment record with a timestamp earlier than the actual ceremony and publishes it to Sigsum with a backdated inclusion proof, claiming the principal enrolled on a date when they did not.

- Attacker capability: Control of the operator's clock or Sigsum-publication mechanism. Requires either operator compromise or Sigsum witness collusion.
- Difficulty: Very-High. Sigsum's verifiable append-only log ensures that records are time-ordered by the transparency-log operators' clocks. To backdate a record, the attacker must either (a) forge a signed inclusion proof with a backdated timestamp (requires Sigsum witness collusion), or (b) compromise the operator's view of the current time (requires operator compromise + clock manipulation).
- Detection: Everest 30 (Sigsum integration) ensures that the inclusion proof contains a signed timestamp from the transparency-log operator. Everest 31 (Roughtime integration) cross-checks the timestamp against an independent time-verification service. If the Sigsum timestamp is older than the Roughtime quorum consensus time, the record is rejected. Any verifier can independently query Sigsum and Roughtime to detect a discrepancy.
- Countermeasure: Sigsum's tamper-evidence (N-of-M transparent logging with independently-auditable operators). Roughtime's quorum-based time verification. Any record published to Sigsum is irrevocably time-ordered relative to all other records. Backdating is impossible without subverting Sigsum's entire witness set.
- Residual risk: None, conditional on Sigsum and Roughtime being honestly run. If both systems are compromised, the protocol's time-binding is lost (Everest 93, governance).
- Related everests: E30 (Sigsum integration), E31 (Roughtime integration), E93 (governance and compromise response).

**EF17 — Forked Enrollment**

An attacker creates two parallel enrollment records for the same principal, both published to Sigsum, with different templates and different witness signatures. Both appear to be authoritative.

- Attacker capability: Access to the operator's private key or the principal's vault. Must either forge the operator's signature or create a second enrollment record that competes with the first.
- Difficulty: Very-High. Both records are published to Sigsum with signatures. Sigsum's append-only guarantee means both records are logged; there is no way to hide one. The verifier must detect the fork and reject both records or accept only one (based on timestamp priority or witness consensus).
- Detection: Everest 28 (verify-chain) walks the enrollment chain and detects if there are two `kind: "enrollment"` records at different points in the chain, both claiming to be the principal's first enrollment. Everest 53 (predicate registry) can enforce a policy that only the first-published enrollment is valid. A verifier querying Sigsum can see both records and can detect the fork by comparing the records' timestamps and witness signatures.
- Countermeasure: A deterministic rule: the first-published enrollment record (earliest Sigsum timestamp) is the authoritative one. Any subsequent enrollment is treated as a re-enrollment (Everest 18) and must reference the prior enrollment's record hash. Witness consensus — if both enrollments are signed by different witness sets, the fork is obvious and indicates operator or witness compromise. The principal's disclosure audit log (Everest 72) records which enrollment was used for each proof, revealing the fork post-facto.
- Residual risk: MITIGATED. A fork is detectable by any verifier; the response is to reject both proofs or to escalate to governance (Everest 93) to determine which chain is authoritative.
- Related everests: E28 (chain verification), E18 (re-enrollment and chain continuity), E53 (predicate registry), E72 (disclosure audit log), E93 (governance).

**EF18 — Out-of-Order Witness Signing**

A witness signs the Pedersen-commitment record before all biometric samples are captured, or the operator publishes a record to Sigsum before the witness has signed it. The ordering is inverted, creating ambiguity about what the witness actually attested to.

- Attacker capability: Control of the ceremony flow or the publication timeline. Requires either operator violation of E11 §H–§I sequencing or witness subversion.
- Difficulty: Medium. The ceremony script (E11 §H–§I) is explicit about order: seal the templates (§H), then witnesses sign (§I). A violation requires operator or witness non-compliance.
- Detection: Everest 28 (verify-chain) checks the chain record ordering: the `kind: "enrollment"` record must be immediately followed by `kind: "witness_attestation"` records, all with the same `parent_record_hash`. If a `witness_attestation` appears before the corresponding `enrollment` record, or if the hash references don't chain correctly, the record is invalid.
- Countermeasure: Procedural enforcement of the ceremony script order (E11 §H–§I). The operator does not invoke `--seal` until all samples are captured, and does not publish to Sigsum until witnesses have signed (on-site, with their hardware tokens). The chain itself enforces the ordering through `parent_record_hash` references.
- Residual risk: None. The chain's hash-chain structure makes out-of-order signing cryptographically obvious.
- Related everests: E11 (ceremony script), E28 (chain verification), E30 (Sigsum publication).

---

## Defense-in-Depth Matrix

| Attack Category | Cryptographic | Procedural | Hardware | Witness | Transparency Log | Status |
|---|---|---|---|---|---|---|
| **Substitution (EF01–04)** | Identity binding in VC | Multi-witness attestation, anti-substitution witness, notarization | Device attestation confirms capture identity | Dual-witness requirement + 5-year familiarity | Chain records commitment | DEFENDED |
| **Coercion (EF05–08)** | Duress codeword + bit-flipping Pedersen | Coercion-check moment (E11 §G), witness affirmation | None specific | Witness self-report post-ceremony | Audit trail of witness signatures | MITIGATED (duress bit) |
| **Replay (EF09–12)** | TPM-signed sample hashes, liveness entropy | Witness supervision of capture, radio-check | TPM / Secure Enclave, wired mic, stylus tablet firmware attestation | Continuous observation during capture | Immutable raw-sample manifest | DEFENDED |
| **Side-channel (EF13–15)** | Constant-time proof operations | Room sweep, immediate power-down, physical security | DRAM encryption, secure erase, radio-check tool | Observation of device isolation, room access | Audit log of device events | MITIGATED (procedural) |
| **Time-shift (EF16–18)** | Timestamped signatures, parent_hash chain | Ordered ceremony script, immediate publication | None | Witness signatures bound to record hash | Sigsum + Roughtime quorum | DEFENDED |

**Key observations:**

- **Substitution attacks** are defended by a combination of multi-witness attestation, device attestation, and identity binding in the VC. No single layer is sufficient; the defense is layered.
- **Coercion attacks** are inherently hard to defend cryptographically. The protocol accepts the risk and offers mitigation: a duress-bit codeword (Everest 58) and post-ceremony witness self-reporting (Everest 19). The primary defense is procedural: the principal can always abort.
- **Replay attacks** are defended by hardware attestation (TPM signatures) combined with liveness-detection entropy analysis and witness observation. The TPM attestation is the strongest defense; liveness detection and witnesses are in-depth layers.
- **Side-channel attacks** are defended by procedural security (room isolation, power-down) and hardware design (DRAM encryption, secure erase). Cryptographic defense (constant-time operations) is a tertiary check.
- **Time-shift attacks** are defended by the chain's hash-chain structure and the transparency log's quorum-based time verification. Sigsum + Roughtime together make backdating and forking cryptographically infeasible.

**Defense gaps:**

- A supply-chain compromise of the stylus tablet before the ceremony is not detected cryptographically; it is prevented only by Everest 14 (secure-boot verification) and procedural checks (E11 §4, dry-run).
- A determined attacker with multiple corrupted witnesses can enroll a substitute. The protocol accepts this and mitigates by requiring multi-witness consensus and enabling post-ceremony red-flag detection (Everest 19).
- Coercion of the principal themselves cannot be defended against cryptographically. The duress-codeword bit and the principal's option to abort are the only mitigations.

---

## Acceptable Residual Risk in v0

The protocol explicitly does NOT defend against:

1. **Rubber-hose attacks on the principal.** No protocol defends against a principal under direct physical coercion. Calm Witness mitigates by offering the duress-codeword bit (Everest 58) so the principal can request help without explicitly asking.

2. **Supply-chain compromise of all candidate hardware.** If every stylus tablet and microphone available is compromised before the ceremony, the templates are poisoned. Calm Witness mitigates by Everest 14 (secure-boot verification) and by re-enrollment on alternate devices (Everest 18), which enables drift detection.

3. **Quantum-capable adversaries.** The Pedersen commitments and Σ-protocol signatures are not post-quantum-secure. Everest 96 (post-quantum migration) is on the route map. Until then, the protocol is vulnerable to a quantum-capable adversary who can break the discrete-log problem.

4. **Nation-state-level compromise of Sigsum and Roughtime simultaneously.** If all N transparency-log operators and the Roughtime quorum are subverted, the protocol's time-binding and append-only guarantee are lost. This is explicitly out-of-scope; Calm Witness assumes that public infrastructure (Sigsum, Roughtime) is reliably operated.

5. **Compromise of the principal's own device (the vault hardware).** If the principal's vault is physically stolen or hacked, all security is lost. This is a "root key compromised" scenario, covered under Everest 23 (recovery) and Everest 33 (replica management).

---

## Critical Countermeasures Shipped at v0

The five most important defenses that close the biggest attack categories:

1. **Multi-witness requirement (Everest 11, EF01–08).** Both capture and anti-substitution witnesses sign the enrollment record. Collusion of all witnesses is required to forge an enrollment. This is the primary defense against substitution and coercion attacks.

2. **Hardware attestation of the capture device (Everest 12, EF09–12).** The TPM or Secure Enclave signs the raw-sample manifest, binding every biometric sample to a cryptographic proof that the sample was captured on the attested device. This prevents pre-recording replay and firmware tampering.

3. **Sigsum + Roughtime anchoring (Everest 30–31, EF16–18).** Every enrollment record is published to Sigsum with a quorum-signed timestamp from Roughtime. The append-only guarantee and time verification make backdating and forking cryptographically infeasible.

4. **Liveness-detection entropy checks (Everest 49, EF09–10).** Biometric samples are validated for real-time entropy (pressure variation, keystroke timing). Pre-recorded or synthesized samples are rejected. This is the primary defense against replay attacks that bypass device attestation.

5. **Witness-signed hash chain (Everest 11 §I, EF04, EF18).** Each enrollment record is signed by witnesses with their hardware tokens. The `parent_hash` chain ensures that the record cannot be retroactively mutated without invalidating all downstream records and witness signatures. This makes document substitution and out-of-order signing cryptographically impossible.

---

— Calm, 2026-05-20
