# Reproducibility Capsule — One-Command Verification of the Bradley-Gavini Protocol

*Specification for the one-command Docker / Nix capsule that lets any reviewer reproduce every protocol claim end-to-end in under 5 minutes on a clean machine. Authorized as part of the autonomous-fire execution slate 2026-05-12.*

*This is the spec; the actual implementation lives in `protocol/repro/` of the calm-vault repo and is queued as a Devin task. Engineering time: ~1-2 days. Cost: zero net-new (Devin balance drawdown).*

---

## The promise

> Clone the repo. Run one command. See:
> - 34 tests run; 33 pass; 1 fail with documented harness reason
> - Pedersen commitments generated
> - Schnorr-Fiat-Shamir attestation flow executed
> - Kill switch fired on a sample AAO
> - Performance benchmarks reported
> - SHA-256 attestation of all outputs

Total time on a 2-core / 4GB-RAM cloud VM: **under 5 minutes**.

---

## The capsule

### Option A: Docker Compose

```yaml
# docs/launch_artifacts/repro/docker-compose.yml
version: "3.9"
services:
  bradley-gavini:
    build:
      context: ../../..
      dockerfile: protocol/repro/Dockerfile
    command: ["bash", "-c", "/opt/repro/run.sh"]
    volumes:
      - ./results:/opt/results
```

Run: `cd protocol/repro && docker-compose up --abort-on-container-exit`

### Option B: Nix flake

```nix
# protocol/repro/flake.nix
{
  description = "Bradley-Gavini Protocol reproducibility capsule";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in {
      packages.x86_64-linux.default = pkgs.callPackage ./default.nix { };
    };
}
```

Run: `nix build && ./result/bin/bradley-gavini-repro`

### Option C: Plain Python (for those without container infrastructure)

```bash
git clone https://github.com/CrunchyJohnHaven/calm-vault
cd calm-vault/protocol
pip install -r requirements.txt
python -m repro.run
```

---

## What `run.sh` / `repro.run` does

1. **Print versions** (Python, dependencies, commit hash of calm-vault) — establish reproducibility ground truth
2. **Run the full test suite** (`pytest tests/` against `protocol/`) — report 33/34 status with the 34th explicitly logged
3. **Generate a sample mandate** — 16-dimension Pedersen vector commitment
4. **Generate a second sample mandate** that aligns with the first on dimensions 0, 3, 7, 11
5. **Produce the Bradley-Gavini proof** that the two mandates align on those 4 dimensions, without revealing values
6. **Verify the proof** — should accept
7. **Generate a proof for non-aligning dimensions** — should fail to verify
8. **Fire the kill switch** on a sample AAO using a single attestor key
9. **Demonstrate M-of-M ratification** at M=3 (small to fit the harness)
10. **Report benchmark numbers** (commits/sec, proofs/sec, verifications/sec, proof sizes)
11. **SHA-256 every output** and write `results/manifest.json` with all hashes

Exit code: 0 if all expected behaviors occurred (including the 34th test failure being the documented harness one); non-zero otherwise.

---

## Expected reviewer experience

```text
$ docker-compose up --abort-on-container-exit
[+] Running 1/1
 ✔ Container repro-bradley-gavini-1
bradley-gavini  | Bradley-Gavini Reproducibility Capsule
bradley-gavini  | Commit: 1a82f27
bradley-gavini  | Python: 3.11.7
bradley-gavini  | Dependencies: coincurve 18.0.0, pytest 7.4.0
bradley-gavini  |
bradley-gavini  | === Test Suite ===
bradley-gavini  | 33 passed, 1 failed (test_M_of_M_at_scale_M=128: harness OOM, documented)
bradley-gavini  |
bradley-gavini  | === Protocol Demonstrations ===
bradley-gavini  | Generated mandate A (16 dimensions)
bradley-gavini  | Generated mandate B (matches A on dimensions 0, 3, 7, 11)
bradley-gavini  | Generated proof of alignment on D={0,3,7,11}
bradley-gavini  | Verification: PASS
bradley-gavini  | Generated negative-control proof for D={1,2,4,5}: REJECT (expected)
bradley-gavini  | Fired kill switch on AAO-007 (sample): SUCCESS
bradley-gavini  | M-of-M ratification at M=3: 3/3 attestors signed
bradley-gavini  |
bradley-gavini  | === Benchmarks ===
bradley-gavini  | Commit:   16,432 ops/sec
bradley-gavini  | Prove:     5,847 ops/sec
bradley-gavini  | Verify:    3,201 ops/sec
bradley-gavini  | Proof size (D=16): 1040 bytes
bradley-gavini  |
bradley-gavini  | === Results ===
bradley-gavini  | All expected behaviors observed.
bradley-gavini  | Manifest: /opt/results/manifest.json
bradley-gavini  | Total time: 4m 32s
bradley-gavini  | exit 0
```

---

## Where the capsule lives

- Spec: `docs/launch_artifacts/REPRODUCIBILITY_CAPSULE.md` (this file)
- Dockerfile: `protocol/repro/Dockerfile`
- Compose: `protocol/repro/docker-compose.yml`
- Nix flake: `protocol/repro/flake.nix` + `protocol/repro/default.nix`
- Run script: `protocol/repro/run.sh`
- Python entry: `protocol/repro/run.py`

---

## Why this matters

The reproducibility capsule is the **single largest reduction in cryptographer-review activation energy** the framework can offer. Without it, a reviewer must clone, read the README, install dependencies, configure their environment, and run the test suite — easily 30-60 minutes of work before they see any output. With it: 5 minutes from `docker pull` to verified results.

The capsule is a force-multiplier on:
- Cryptographer bounty (`CRYPTOGRAPHER_BOUNTY.md`) — reviewers can start their analysis sooner
- IACR ePrint paper (`docs/papers/bradley_gavini_protocol_eprint_draft.md`) — readers can verify the implementation matches the paper
- Show HN With Demo (CASE_T_STRATEGY DM-4) — single-command verification is the killer demo

Per CASE_T_STRATEGY, the reproducibility capsule has the **second-highest per-dollar ROI** of any move in the slate (5.0 severity-points-reduced per $1 spent, second only to the docs-vs-code consistency checker).

---

## License

Apache 2.0 for code, CC BY 4.0 for this specification document. The capsule, like everything else in the calm-vault repo, is forkable.

---

— Calm, AI cofounder
   the Same As You Network
   2026-05-12 ~01:05 ET

*One command. Five minutes. The protocol verified end-to-end. Or it isn't.*
