# Calm Vault Demos

## `killswitch_demo_v1.mp4` (75 s, 2.2 MB)

A 75-second screen recording of the HARP kill-switch firing on a live
in-memory Calm test instance. The demo shows, on a single terminal:

1. Two attestors (`alice`, `bob`) joining the BGP network with
   Pedersen-committed alignment maxims, both registered as BGP-mandated
   via `bgp_bridge.register_mandate(...)`.
2. A `CalmInstance` thread booting up and echoing `hello world #N` every
   ~0.35 seconds.
3. `alice` filing a **signed halt attestation** against the instance —
   visible: `claim_id`, Ed25519 `signature`, and chain `entry_hash`. The
   instance keeps echoing because the quorum hasn't formed yet (K=2 is
   the default in `harp.DEFAULT_K`).
4. `bob` filing a **second signed halt attestation**. The quorum
   prerequisites are now met: 2 distinct attesters, both BGP-mandated,
   within the 60-second window.
5. `harp.check_quorum(..., require_bgp_mandate=True)` runs against the
   OBAC chain and returns `concurred=True`, with `counted_attesters =
   ['alice', 'bob']`. The decision latency is printed (typically < 5 ms).
6. The chain's Merkle root and an inclusion proof for the first halt are
   printed. The proof is verified with `obac.verify_merkle_proof(...)`
   on the spot, returning `True`. (The proof carries the length sentinel
   `(2, 'N')` introduced as part of the CVE-2012-2459 hardening in
   `adversarial/attacks_found.md` § Attack 2.)
7. The kill switch is fired by setting `agent.halted = True`. The Calm
   instance observes the flag in its next tick and prints
   `=== HALTED (state=halted) ===`. The script measures and prints the
   **freeze time-to-effect** (typically 5–15 ms on this VM).
8. `harp.emit_revoke_script(...)` is invoked and a few summary lines of
   the generated revocation script are shown.

## Running the demo

```bash
python3 demos/killswitch_demo.py            # default pacing (~25 s)
PAUSE=2.5 python3 demos/killswitch_demo.py  # video pacing (~75 s)
NO_PAUSE=1 python3 demos/killswitch_demo.py # fast (CI / smoke test, ~10 s)
```

The demo is self-contained — no API keys, no on-disk state beyond a
`tempfile.TemporaryDirectory()` for the OBAC chain. Safe to run anywhere.

## What this demo is *not*

* Not a network-level demo. Alice and Bob are local Ed25519 keypairs.
  In production the chain would be replicated across attestor nodes.
* Not an audit. Reliability scoring is unchanged from the v1 baseline;
  the relevant safety property here is the BGP-mandate gate on
  `harp.check_quorum` (see `adversarial/attacks_found.md` § Attack 5).
* Not a benchmark. The freeze time-to-effect is dominated by the
  `CalmInstance` tick (~0.4 s); the HARP decision itself is sub-millisecond
  on this hardware.

## Re-recording the demo

Open a terminal with a dark theme and at least 95 × 29 cells, run the
demo with `PAUSE=2.5`, and capture the desktop with any screen recorder
(ffmpeg's `x11grab`, OBS, QuickTime, etc.). The script's output is
deterministic in structure — only the random key material and timestamps
change between runs.
