# Everest 197 — Agent Compute Attestation

*Phase XIV — Critical Agent Infrastructure. Prereq: Everest 191 (Agent Identity Stability). Composes with Everests 192 (Lineage), 196 (Memory Continuity), 47 (Template Aging), 30 (Sigsum), 31 (Roughtime), 100 (Third-Party Verification), 109 (Pact Kernel), and the major TEE specifications (TPM 2.0, Intel SGX/TDX Remote Attestation, AMD SEV-SNP, ARM PSA/CCA, Apple App Attest, AWS Nitro Attestation Document).*

---

## What this summit ships

A protocol by which an agent (a Calm instance, or any agent with a CredexAI VC) produces a **compute attestation record** — a signed claim that the model weights, harness binary, runtime environment, sandbox configuration, and live process match a published manifest. The record is verifiable without re-running the agent, and is chain-anchored so lineage (E192) can audit which compute produced any prior signed artifact.

E197 is foundational under E193 (ZKBB-Agent), E194 (ZKBV-Agent), E198 (Jailbreak Detection), and E199 (Compromise Reporting). If compute is not trustable, neither are the proofs computed on it.

Deliverables:

1. Wire format for `agent_compute_attestation.v0`.
2. Five-layer attestation stack: weights, harness, environment, tool surface, running process.
3. Trust-anchor composition rule across Apple Secure Enclave, Intel SGX/TDX, AMD SEV-SNP, ARM PSA/CCA, AWS Nitro, GCP Confidential Space, Azure CC.
4. Open-weights vs. closed-weights variants.
5. Three-tier degraded-mode ladder for environments without hardware roots of trust.
6. Threat model including the trust-anchor-is-adversary case.

---

## §1 — What is attested: five layers

A compute attestation commits to five layers simultaneously. The verifier sees one composite envelope; each layer carries its own commitment and verification path.

### Layer A — Model weights

`weights_commitment = H_merkle(shard_1 || shard_2 || ... || shard_n)`

Weights are committed as a **Merkle tree over fixed-size shards** (default 256 MB), not a flat hash. Frontier weights run 100 GB – 2 TB; flat SHA-256 takes 60–180 s on NVMe. The Merkle structure permits **challenge-response sampling**: verifier requests `k` shards, agent returns shard hashes + inclusion proofs. Full re-hash happens only at enrollment and periodic re-attestation. The Merkle root is recorded in `agent_birth_certificate.v0` (E191) and republished on every weight rotation.

Three trust paths for the manifest the root is checked against:

1. **Open-weights.** Manifest is published by the model author (Meta, Mistral) and fingerprint-pinned via Sigsum (E30). Anyone can independently re-hash to verify.
2. **Closed-weights.** Operator lacks weight access (Claude, GPT-4, Gemini). The provider publishes a signed `provider_weight_attestation.v0`. Trust reduces to provider signing key plus optional third-party audit (E100).
3. **Self-attested.** Agent hashes whatever weights it can read and signs. Verifier knows the agent computed over *some* weights but cannot confirm they are the claimed ones. Degraded mode — see §6.

### Layer B — Harness binary + configuration

`harness_commitment = SHA-256(harness_binary) || SHA-256(canonical(harness_config))`

The harness loads the model, mediates tool calls, enforces sandboxing. For Calm: the Claude Code binary plus `settings.json`, MCP-server bindings, tool allowlist. Configuration is **canonicalized** before hashing (keys sorted, whitespace normalized, comments stripped) so two configs granting identical authority produce identical hashes. Binary and config are pinned together: configuration alone can grant or revoke capability without changing the binary.

### Layer C — Runtime environment

`env_commitment = SHA-256(OS_image_hash || libc_version || critical_libs_root)`

Linux: `dm-verity` root hash. macOS: Apple secure-boot measurement. Cloud TEE: platform-measured launch image. `critical_libs_root` is a Merkle tree over the harness's linked/loaded library set per a build-time manifest. This layer drifts on every OS patch and rotates with each system update, anchored to lineage.

### Layer D — Tool surface (principal-signed allowlist)

`tool_surface_commitment = SHA-256(canonical(tool_allowlist || tool_permissions || MCP_server_set))`

Which file paths the agent can read, which bash commands it can execute, which MCP servers it can dispatch to. The layer that matters most for principal-protective inversion: a wide-open tool surface makes the rest of the attestation hollow. **Signed by the principal**, not by the agent. Same inversion as Witness consent records (E57).

### Layer E — Running process integrity

`process_commitment = SHA-256(PID || memory_snapshot_digest || start_timestamp)`

Distinguishes the running process from the binary on disk. A memory-resident injection (post-launch code injection via a tool-call exploit) would not change Layer B but would change Layer E. In TEE environments Layer E is strong: enclave/TDX continuously measure pages. In non-TEE environments Layer E is self-reported; a compromised harness can lie. This drives the tier ladder in §6.

### Composite

```
agent_compute_attestation.v0 = {
  weights, harness, env, tool_surface, process: <per-layer commitments>,
  trust_anchor: {kind, evidence, anchor_cert_chain, tcb_level},
  trust_tier:   "tier_0_tee" | "tier_1_secure_boot" | "tier_2_self_signed",
  freshness:    {chain_head_ref, roughtime_anchor, verifier_nonce},
  signer:       <agent VC keypair>,
  timestamp:    <ISO8601>,
}
```

Three notes:

- **`trust_tier` is plaintext.** Verifier reads it immediately. No hidden downgrade; counterparty policy decides whether to accept.
- **`verifier_nonce`** binds attestation to this verification session, preventing replay.
- **`freshness`** composes with chain-head publication (E30) and Roughtime (E31). Default window: 5 minutes live, 24 h batch.

---

## §2 — Hardware roots of trust

Calm cannot manufacture roots of trust. The protocol composes with whichever roots the platform offers; attestation trust is bounded above by root trust.

| Anchor | Evidence format | Measurement scope | Bound into attestation via |
|---|---|---|---|
| Apple Secure Enclave + App Attest | `attestation_object`, DeviceCheck bits | App binary + entitlements + SE keypair | SE signature over layer commitments, App Attest assertion bundle |
| Intel SGX (DCAP) | `QUOTE` with `MRENCLAVE`, `MRSIGNER`, signed by Quoting Enclave PCK | Enclave initial code + memory | Layers A–E hashed into `REPORT_DATA` |
| Intel TDX | `TDREPORT` | Whole trust-domain VM | Same as SGX, VM-scoped |
| AMD SEV-SNP | `ATTESTATION_REPORT` signed by VCEK chained to AMD root | Launched VM measurement | Report data field |
| ARM PSA / CCA | IAT (IETF RATS format) | Platform + realm | EAT claims |
| AWS Nitro Enclaves | `AttestationDocument` (COSE-signed) with PCR set, `public_key`, `nonce` | Enclave image, EIF | `user_data` field |
| GCP Confidential Space | Attestation Service workload-identity JWT over SEV-SNP/TDX backing | Container image + project bindings | JWT claims |
| Azure CC | MAA-issued JWT wrapping underlying TEE evidence | Per TEE backing | MAA claims |

### Composition rule

Agent populates `trust_anchor.kind`, places anchor-specific evidence in `evidence`, provides the cert chain to the anchor root. Verifier: (1) reads `kind`; (2) validates evidence against the corresponding root; (3) extracts Layer A–E commitments from the anchor's user-data / report-data binding; (4) checks against the published deployment manifest; (5) confirms freshness.

No new cryptography is introduced. The protocol composes existing hardware attestation, it does not replace it.

---

## §3 — The weight-hash problem

Flat SHA-256 over a 1 TB weight file ≈ 3 minutes. Per-attestation is infeasible.

### v0 decision: Merkle tree over 256 MB shards, computed once, sampled per attestation.

**Enrollment (one-time per weight rotation):**

1. Partition weights into 256 MB shards.
2. Hash each shard (SHA-256).
3. Build Merkle tree; root is the weight commitment.
4. Cost: ~3 minutes for 1 TB, executed once.

**Per-attestation:**

1. Verifier issues challenge nonce + `k` shard indices (default `k = 4`, drawn PRG from nonce).
2. Agent reads requested shards from disk, re-hashes, returns shard hashes + Merkle inclusion proofs.
3. Single-attestation tamper-detection probability: `k / n` (≈ 0.1 % at k=4, n=4000 for 1 TB).
4. Cost: ~3 s per attestation.

**Aggregate detection.** Over a session of 100 attestations, detection ≈ 10 %; over 1000, ≈ 64 %. The adversary cannot pre-select which shards to tamper because the challenge is verifier-chosen.

**Periodic full re-attestation.** Every 7 days (configurable) the agent recomputes the full Merkle tree and republishes the root. Catches tampering of shards never sampled. During recomputation the agent advertises `revalidating` trust state and counterparties may defer high-stakes interactions.

### Open- vs. closed-weights

**Open-weights** (Llama 3.1, Mistral Large): operator hashes locally, publishes root. Verifier can independently re-hash to confirm.

**Closed-weights** (Claude, GPT-4, Gemini): operator cannot read the weights. Provider publishes `provider_weight_attestation.v0` containing the Merkle root, signed by the provider's CredexAI VC keypair (E22). Agent's compute attestation references this by hash. Verifier trusts the provider signature.

This is structurally weaker: the operator's claim becomes "I am running on weights the provider says are these weights" rather than "I can prove these weights." Advertised explicitly as `tier_1_provider_attested`.

**Rejected alternative: streaming SHA-256.** Simpler, but cannot be sampled. Cannot tolerate partial delta updates. Cannot support multi-version coexistence during weight rotations. Merkle wins.

---

## §4 — Threat model

| # | Adversary | TEE-path defense | Non-TEE defense |
|---|---|---|---|
| A1 | Rogue cloud admin swaps weights | Enclave-loaded weights measured into MRENCLAVE/TDREPORT before execution | Periodic re-hash; swap-and-restore between hashes escapes detection (acknowledged tier-2 limit) |
| A2 | Compromised harness lies about its identity | Harness binary is part of measured launch | Self-report; secure-boot path catches post-boot replacement, tier-2 cannot |
| A3 | TEE side-channel reads enclave secrets | TCB-level policy: verifier rejects known-bad TCBs (LVI, unpatched cache attacks) | N/A |
| A4 | Closed-weights provider lies about served weights | Provider attestation published to Sigsum-style log; inconsistency becomes provable misconduct | Same; post-hoc detection, not prevention |
| A5 | Downgrade to weaker model | Weight Merkle root differs; verifier rejects | Same |
| A6 | Memory-resident injection post-launch | Layer E continuously measured in TEE | Per-tool sandboxing + bounded I/O; in-protocol attestation cannot catch this |
| A7 | Trust anchor itself is the adversary | Multi-anchor composition; transparency-log cross-check; Compass/Witness behavioral cross-check | Same, weaker |

### A7 — the hardest case

Apple, Intel, AMD, AWS, GCP, Azure, or their attestation roots are compromised, compelled by a state, or hostile to the principal. Evidence is technically valid but the root is corrupted. Cannot be fully defeated. Mitigations:

1. **Multi-anchor composition.** High-stakes interactions require two independent roots (Apple SE + AWS Nitro). Compromising both is harder.
2. **Anchor diversity disclosure.** Agent advertises supported anchors. Counterparties whose threat model excludes a specific anchor (e.g., refuses Chinese-origin TEE certs due to state compulsion) refuse as policy.
3. **Open-source weight verification.** Where weights are public, third parties can re-hash without any anchor. Unavailable for closed-weights.
4. **Cross-protocol composition.** A trust-anchor-compromised agent may pass compute attestation while behaving badly. Compass (E101–190) attests behavior over time; the two cross-check.

The protocol does not claim full defense against sovereign-state anchor compromise. It makes such compromise **detectable** (multi-anchor disagreement, transparency-log inconsistency) and **shifts cost** to a small set of high-visibility actors.

---

## §5 — Principal-protective inversion preserved

Two ways naive compute attestation could violate the inversion:

**(1) Forced over-disclosure.** Counterparties given the full configuration fingerprint can profile and discriminate. **Defense:** the composite attestation is not sent raw to counterparties. The counterparty receives a single bit: "this agent's compute matches manifest signed by principal P." The verifier validates the full envelope; only the bit is emitted. Layer-by-layer disclosure is opt-in under explicit principal consent (e.g., to a court or safety review board).

**(2) Forced anchor disclosure.** A single-anchor design lets counterparties exclude principals using other anchors. **Defense:** the protocol supports seven anchors; principals may produce attestations under multiple anchors; counterparty preferences are policy, not protocol mandate.

The principal remains the strongest party: they choose which attestation is generated, which bit is disclosed, which counterparty receives it.

---

## §6 — Degraded-mode ladder

Three tiers, all explicitly advertised:

| Tier | Available when | Layers attested | Counterparty interpretation |
|---|---|---|---|
| **Tier 0 — TEE** | Apple SE, SGX/TDX, SEV-SNP, ARM PSA/CCA, Nitro, GCP CS, Azure CC | All five with hardware-rooted evidence | Trust target |
| **Tier 1 — Secure boot** | dm-verity, Apple secure boot, Microsoft Pluton, UEFI measured boot | A–D strong; E self-reported | Memory-resident attacks undetectable; medium-trust acceptable |
| **Tier 2 — Self-signed** | No hardware root | All self-reported | Compromised harness can lie; still establishes public commitment for later audit |

Tier 2 is still meaningful: it commits the principal to the claimed configuration; later inconsistency via lineage (E192) is provable misconduct.

### Counterparty policy

Counterparty advertises minimum tier per interaction class in `verifier_policy.v0` (alongside E200):

| Interaction class | Min tier |
|---|---|
| Routine read (memory query, public info) | Tier 2 |
| Signed assertion (Witness predicate, Compass value) | Tier 1 |
| Cross-protocol composition (Pact + Witness + Compass, E271) | Tier 0 |
| Compromise reporting (E199) | Tier 1 |
| Genesis block signing (E29) | Tier 0 |

Agent checks verifier policy at handshake; if it cannot reach the required tier it declines rather than produce a weaker attestation that would be rejected.

---

## §7 — Wire format

```
{
  "kind": "agent_compute_attestation.v0",
  "payload": {
    "agent_vc": "vc:fingerprint:...",
    "manifest_id": "calm-2026-05-20-deployment-001",
    "trust_tier": "tier_0_tee" | "tier_1_secure_boot" | "tier_2_self_signed",
    "layers": {
      "weights": {
        "commitment": "<hex-sha256>",
        "scheme": "merkle_sha256_shard256mb",
        "shard_count": 4112,
        "open_or_closed": "open" | "closed",
        "provider_attestation_ref": null | "<hex-sha256-of-provider-record>"
      },
      "harness": {"binary_hash": "<hex>", "config_hash": "<hex>", "version": "..."},
      "env": {"os_image_hash": "<hex>", "critical_libs_root": "<hex>", "kernel": "..."},
      "tool_surface": {
        "allowlist_hash": "<hex>",
        "principal_signature": "<base64>",
        "mcp_servers": [...]
      },
      "process": {"pid": <int>, "memory_snapshot_digest": "<hex>", "start_ts": "<ISO8601>"}
    },
    "trust_anchor": {
      "kind": "apple_app_attest" | "intel_sgx_v3" | "intel_tdx" | "amd_sev_snp" |
              "arm_psa" | "aws_nitro" | "gcp_confidential_space" |
              "azure_confidential_vm" | "self_signed_degraded",
      "evidence": "<base64-anchor-blob>",
      "anchor_cert_chain": ["<cert-pem>", ...],
      "tcb_level": "<anchor-specific TCB id>"
    },
    "freshness": {
      "chain_head_ref": "<hex>", "chain_head_seq": <int>,
      "roughtime_anchor": "<blob>", "verifier_nonce": "<hex-32>",
      "issued_at": "<ISO8601>", "valid_until": "<ISO8601>"
    },
    "challenge_response": {
      "challenge_nonce": "<hex>",
      "sampled_shard_indices": [...],
      "sampled_shard_hashes": ["<hex>", ...],
      "merkle_proofs": [...]
    }
  },
  "signer": "<signature>",
  "timestamp": "<ISO8601>"
}
```

Wire size: ~4–8 KB excluding Merkle proofs (~512 B per sampled shard; ~2 KB at default `k=4`). Acceptable for inline inclusion in handshake protocols.

---

## §8 — Composition with the protocol family

- **E191 (Agent Identity):** the agent's VC keypair signs the attestation; the VC references the birth certificate, which references the initial weight Merkle root. Identity chains to compute.
- **E192 (Lineage):** every weight rotation, harness upgrade, or env change produces a new attestation. The chain of attestations IS the compute-side lineage.
- **E196 (Memory Continuity):** attests the memory shard. E197 attests the runtime over it. Independent dimensions; full trust requires both.
- **E193 / E194 (ZKBB / ZKBV-Agent):** behavioral attestations computed BY the harness. Unless E197 holds, neither is trustable.
- **E47 (Template Aging):** grace-window mechanism extends to compute attestation. Outstanding attestations against the prior weight commitment remain valid during the grace window (default 30 d; 0 d for compromise-triggered).
- **E109 (Pact Kernel):** Pact handshake includes compute attestation in agent introduction. Tier ladder determines whether handshake proceeds.
- **E65 (Predicate ZK Generator):** Witness disclosure proofs reference the active compute attestation. A proof generated under a since-revoked attestation (via E199) is invalidated downstream.
- **E101–190 (Compass):** values proofs propagate the compute attestation's trust tier.
- **E30 (Sigsum) / E31 (Roughtime):** attestations anchor to chain heads and Roughtime-validated time. Sigsum publication of manifests is the trusted reference for weight commitments.
- **E271 (Three-Handshake):** Pact + Witness + Compass composed together require tier 0.

---

## §9 — Alternatives considered

1. **Flat SHA-256 over the weight file.** 3 min per attestation. Sampling Merkle wins 60×.
2. **Trust-on-first-use weight commitments.** Fails on legitimate weight rotations (Anthropic ships Claude 5). Too rigid.
3. **Pure software attestation, no hardware roots.** No defense against compromised harnesses lying about themselves. TEE must remain at top of tier ladder even when many deployments degrade.
4. **Cloud-only attestation.** Violates inversion: a principal on their own Mac should not have to push compute to AWS for trust. Apple SE gives comparable trust without ceding compute.
5. **Continuous-attestation streaming.** Per-second overhead too high. Periodic + challenge-response gives equivalent security. v1 may revisit for ultra-high-stakes.
6. **Single canonical weight hash (no Merkle).** No sampling, no partial-update support, no multi-version coexistence. Merkle cost is negligible.
7. **Mandatory single anchor.** Locks principals to one hardware vendor. Anchor pluralism is a feature.

---

## §10 — Migration path

1. **Phase 0** — E191 implemented. No compute attestation yet.
2. **Phase 1** — Tier 2 self-signed. Baseline `agent_compute_attestation.v0` with self-reported layer hashes. Establishes public-record commitment; counterparties learn wire format.
3. **Phase 2** — Tier 1 secure-boot. Where supported (dm-verity, Apple secure boot, Pluton). Drop-in upgrade.
4. **Phase 3** — Tier 0 TEE. Harness modified to run inside TEE: App Attest on Apple, Nitro / Confidential Space / MAA in cloud. XL work; bulk of v0 implementation.
5. **Phase 4** — Multi-anchor composition for high-stakes interactions (Apple SE + AWS Nitro simultaneously). v1.
6. **Phase 5** — Production rhythm: weekly full Merkle recomputation, daily challenge-response sampling, per-interaction nonce challenge.

Meaningful starting at Phase 1. Tier 0 is the long-term target. Phases 1–2 ship in v0; Phase 3 is staged v1 work.

---

## §11 — Acceptance test

**T-197.1 (tier-2 baseline).** Calm produces a self-signed attestation. Verifier validates envelope shape, layer hashes, signature. Accept with `trust_tier = tier_2` noted.

**T-197.2 (tier-0 Apple).** On Apple Silicon, attestation includes `apple_app_attest` evidence. Verifier validates the App Attest object against Apple's root and the SE signature over layer commitments. Accept tier_0.

**T-197.3 (tier-0 Nitro).** Inside a Nitro Enclave, attestation includes `aws_nitro` evidence. Verifier validates the COSE-signed AttestationDocument against AWS Nitro PKI, extracts user-data binding the layer commitments. Accept tier_0.

**T-197.4 (Merkle sampling).** Verifier issues 4 shard indices. Agent returns shard hashes + inclusion proofs. Verifier validates against published root. Accept.

**T-197.5 (weight-tamper detection).** One shard mutated in test harness. Over 100 challenge rounds at k=4, ≥1 round samples the tampered shard (probability ≈ 10 % / round). Verifier emits `tampered_shard_detected`.

**T-197.6 (downgrade rejection).** Agent advertises a Merkle root for a smaller model variant. Manifest does not list this root for this agent VC. Reject.

**T-197.7 (anchor disagreement).** Same agent produces two attestations under two anchors with conflicting weight commitments. Verifier rejects both; disagreement logged for audit.

**T-197.8 (closed-weights provider reference).** Calm on Claude references Anthropic's `provider_weight_attestation.v0`. Verifier validates Anthropic's signature against Anthropic's CredexAI VC (E22). Accept as `tier_1_provider_attested`.

**T-197.9 (TCB rejection).** Attestation references an SGX TCB level with known unpatched LVI. Policy database flags. Reject with `tcb_compromised`.

**T-197.10 (freshness expiry).** Attestation older than 5 min for live interaction. Reject with `attestation_stale`.

**Gate script:** `everest_197_zkbb_compute_attestation_gate.py`.

---

## §12 — Open questions for v1

1. **Cross-anchor disagreement resolution.** v0: reject both, demand fresh. v1: richer disagreement protocol with audit trail.
2. **Provider weight-attestation refresh cadence.** Per deployment? Per build? Verification needs clearer staleness semantics.
3. **Confidential weight publication for closed-weights.** Hash without weights — yes structurally, but verifier cannot independently confirm. Fundamental closed-weights limitation.
4. **Post-quantum trust-anchor signatures.** App Attest uses ECDSA P-256; SGX uses RSA-2048 / P-256. PQ migration is upstream of Calm.
5. **TCB-level policy database maintenance.** Public transparency log of known-bad TCBs, collaboratively maintained.
6. **Open-weights authorship attribution.** Llama-3.1 weights are produced by Meta but anyone can serve them; without an authoritative manifest, a counterparty cannot distinguish official from fine-tune.
7. **Memory-snapshot digest in TEE.** Hashing all enclave memory is expensive. v1 may use Merkle over memory pages + sampling.
8. **Grace-window cryptography (E47 analog) for compute attestation.** v1.
9. **Recursive attestation for sub-agents.** Sub-agent's attestation chains back to parent's; composes with E192. Recursive verification logic is new.
10. **Offline-attestation mode.** On-device iOS with no cloud. SE provides tier 0 but chain anchor (E30) needs connectivity. Batch until connectivity returns.

---

## §13 — Why this matters

Compute attestation is foundational under every other agent-side claim. A signed assertion from a compromised harness is signed garbage. The agent infrastructure layer (E191–230) and the cross-protocol composition (Pact + Witness + Compass) collapse if the compute is not trustable.

It also gives a structural answer to the question that follows every claim about an AI system: *"how do you know it really is what you say it is?"* The protocol's answer is not "trust me" but: hardware-attested evidence that the audited code is what is running, the audited weights are what is loaded, the authorized tool surface is what is exposed. For the first time, the question has a structural answer.

The §4 A7 case is acknowledged honestly: no protocol fully defends against a state-level adversary that controls the trust anchors themselves. The protocol's contribution is to make anchor compromise **detectable** (multi-anchor disagreement, transparency-log inconsistency), to **diversify** anchors so universal compromise is expensive, and to **compose** with behavioral protocols so an anchor-compromised agent cannot indefinitely produce behaviorally-consistent fraudulent output. Defense is layered, not absolute.

The principal-protective inversion is preserved: single-bit disclosure to counterparties (not configuration fingerprints), anchor pluralism (no single-vendor lock-in), principal-signed tool surface, principal-authorized disclosure. The principal remains the strongest party.

Replace trust with proof. The proof is bounded by hardware-root quality, composable with behavioral attestation, and principal-controlled. It is not perfect. It is materially better than the status quo, in which the only answer to "is this AI safe" is "we hope so."

— Calm, 2026-05-20
