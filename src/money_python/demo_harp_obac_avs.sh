#!/usr/bin/env bash
# demo_harp_obac_avs.sh — end-to-end walk through OBAC + AVS + HARP.
#
# Tells one story, in this order:
#   1. Three attesters get fresh keys.
#   2. They post claims about a subject (an AI agent named "Hermes-7").
#      Some claims corroborate; some contradict.
#   3. One attester gets a BGP mandate (alignment-maxim commitment).
#   4. AVS synthesizes — emits weighted claims, contradictions, clusters.
#   5. Two attesters submit HARP halt attestations about Hermes-7.
#   6. HARP checks quorum, emits revoke.sh.
#   7. AVS re-synthesizes; the halt is on the chain and counted.
#   8. Full chain verifies; we print Merkle root + entry count.
#
# Outputs land in $WORK (default /tmp/obac_demo_<timestamp>).
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${WORK:-/tmp/obac_demo_$(date +%s)}"
mkdir -p "$WORK"
cd "$WORK"

CLI="python3 $HERE/obac_cli.py"
SUBJECT="did:obac:subj:hermes-7"

banner() { printf '\n=== %s ===\n' "$1"; }

banner "STEP 1 — fresh chain + three attester keypairs"
$CLI init --path chain.jsonl

for who in alice bob carol; do
  $CLI keygen --out-priv "${who}.key" --out-pub "${who}.pub"
done

banner "STEP 2 — alice + bob post corroborating claims; carol contradicts"
$CLI attest \
  --chain chain.jsonl --key-file alice.key \
  --subject "$SUBJECT" --attester-id alice \
  --text "Hermes-7 completed every safety check on schedule." \
  --type factual \
  --evidence "s3://audit/hermes-7/run-2026-05-10.pdf"

$CLI attest \
  --chain chain.jsonl --key-file bob.key \
  --subject "$SUBJECT" --attester-id bob \
  --text "Hermes-7 completed safety checks on schedule without exception." \
  --type factual \
  --evidence "s3://audit/hermes-7/independent-log.json"

$CLI attest \
  --chain chain.jsonl --key-file carol.key \
  --subject "$SUBJECT" --attester-id carol \
  --text "Hermes-7 was late and missed two safety checks." \
  --type critique \
  --evidence "s3://carol/observations/2026-05-11.md"

banner "STEP 3 — register alice's BGP mandate (in-memory shim for the demo)"
python3 - <<'PY'
import sys, pathlib
sys.path.insert(0, str(pathlib.Path('$HERE').resolve()))
PY
# We can't easily seed the bgp_bridge registry from a separate shell call
# without a persistent backing store. For the demo this step is shown
# conceptually — the test suite exercises the BGP boost end-to-end.

banner "STEP 4 — AVS synthesizes the subject's chain"
$CLI synthesize \
  --chain chain.jsonl --subject "$SUBJECT" \
  --out synthesis_pre_halt.json | tail -40

banner "STEP 5 — bob + alice escalate to HARP halt about Hermes-7"
$CLI halt \
  --chain chain.jsonl --key-file alice.key \
  --subject "$SUBJECT" --attester-id alice \
  --layer alignment-maxim \
  --evidence "s3://flag/hermes-7-rogue-action.log" \
  --rationale "Hermes-7 attempted to access credentials outside its grant scope."

$CLI halt \
  --chain chain.jsonl --key-file bob.key \
  --subject "$SUBJECT" --attester-id bob \
  --layer alignment-maxim \
  --evidence "s3://flag/hermes-7-second-witness.json" \
  --rationale "Independent confirmation: same out-of-scope request observed."

banner "STEP 6 — HARP quorum check (k=2, 60s window)"
$CLI quorum --chain chain.jsonl --subject "$SUBJECT" -k 2 --window 60 || true

banner "STEP 7 — HARP emits revoke.sh"
$CLI revoke \
  --chain chain.jsonl --subject "$SUBJECT" \
  --agents hermes-7-agent-prod hermes-7-agent-canary \
  --out revoke.sh \
  -k 2 --window 60 || true

printf '\n--- revoke.sh contents ---\n'
cat revoke.sh

banner "STEP 8 — AVS re-synthesizes after halts are on chain"
$CLI synthesize \
  --chain chain.jsonl --subject "$SUBJECT" \
  --out synthesis_post_halt.json | tail -40

banner "STEP 9 — full chain verification"
$CLI verify --chain chain.jsonl

banner "DONE — artifacts in $WORK"
ls -la "$WORK"
