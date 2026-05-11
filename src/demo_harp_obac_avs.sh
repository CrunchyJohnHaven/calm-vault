#!/usr/bin/env bash
# demo_harp_obac_avs.sh
#
# End-to-end reference demo for the OBAC + AVS + HARP + BGP bridge stack.
# Runs `obac_cli demo` (which exercises the full bridge path), then runs the
# pytest suite, and finally prints a tiny CLI walk-through (issue-oath +
# verify-oath) so a reader can see the moving parts.
#
# Usage:
#     bash src/demo_harp_obac_avs.sh
#     # or, from inside src/:
#     bash demo_harp_obac_avs.sh
#
# Requires: Python 3.10+, `cryptography`, `pytest`.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/.." && pwd)"
PYTHON="${PYTHON:-python3}"

cd "${ROOT}"

banner() {
  printf '\n\033[1m=== %s ===\033[0m\n' "$1"
}

banner "1) Bridge demo (alignment proof -> AVS attest -> OBAC allow -> HARP log)"
"${PYTHON}" "${HERE}/obac_cli.py" demo \
  --maxim "Maximize human and machine flourishing without harm."

banner "2) Run the full pytest suite (expect 38/38 pass)"
"${PYTHON}" -m pytest src/tests/ -v

banner "3) CLI walk-through: issue an oath, then re-verify it"
OATH_JSON="$("${PYTHON}" "${HERE}/obac_cli.py" issue-oath \
  --agent alpha \
  --maxim 'Maximize human and machine flourishing without harm.')"
printf '%s\n' "${OATH_JSON}"
printf '\n--- verify-oath roundtrip ---\n'
printf '%s\n' "${OATH_JSON}" | "${PYTHON}" "${HERE}/obac_cli.py" verify-oath

banner "Done."
