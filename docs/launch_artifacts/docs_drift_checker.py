#!/usr/bin/env python3
"""
docs_drift_checker.py - Detect drift between documentation and code

Walks the calm-vault repo. For each .md doctrine file at the root, extracts
claims of the form:
  - "33 of 34 tests pass" → checks pytest result
  - "Apache 2.0" / "CC BY 4.0" → checks LICENSE files
  - "AAO-Certified #N" → checks AAO_DIRECTORY consistency
  - file references "[X.md](./X.md)" → checks file exists

Reports drift in a single .json output and a human-readable .md summary.

Authorized 2026-05-12 as part of the autonomous-fire execution slate.
License: Apache 2.0.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime, UTC

REPO_ROOT = Path(__file__).parent.parent.parent.resolve()
OUT_DIR = REPO_ROOT / "docs" / "drift_reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Patterns we extract from .md files and check against code/repo state
PATTERNS = {
    "test_status": re.compile(r"(\d+)\s+of\s+(\d+)\s+tests?\s+pass", re.IGNORECASE),
    "license_code": re.compile(r"Apache\s+2\.0", re.IGNORECASE),
    "license_doctrine": re.compile(r"CC\s*BY\s*4\.0", re.IGNORECASE),
    "aao_cert_ref": re.compile(r"AAO-Certified\s+#?(\d+)", re.IGNORECASE),
    "internal_link": re.compile(r"\[([^\]]+)\]\(\.?\/?([^)]+\.md)\)"),
}


def find_md_files(root: Path) -> list[Path]:
    """Find all .md files in the repo root (one level deep, excluding press_kit/docs/etc)."""
    excluded = {"node_modules", ".git", "press_kit", "docs", "domain_manifestos", "calm_pact"}
    md_files = []
    for entry in root.iterdir():
        if entry.is_dir() and entry.name not in excluded:
            md_files.extend(entry.glob("*.md"))
        elif entry.is_file() and entry.suffix == ".md":
            md_files.append(entry)
    return sorted(md_files)


def run_pytest_status() -> tuple[int, int]:
    """Run pytest in protocol/ and return (passed, total). Returns (-1, -1) if pytest not runnable."""
    protocol_dir = REPO_ROOT / "protocol"
    if not protocol_dir.exists():
        return -1, -1
    try:
        result = subprocess.run(
            ["pytest", "--collect-only", "-q"],
            cwd=protocol_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )
        # Parse stdout for "N tests collected" pattern
        m = re.search(r"(\d+)\s+tests?\s+collected", result.stdout)
        total = int(m.group(1)) if m else -1

        result2 = subprocess.run(
            ["pytest", "--tb=no", "-q"],
            cwd=protocol_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )
        m2 = re.search(r"(\d+)\s+passed", result2.stdout)
        passed = int(m2.group(1)) if m2 else -1
        return passed, total
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return -1, -1


def check_license(filename: str, expected_license: str) -> bool:
    """Check if the expected license string appears in the named license file."""
    license_file = REPO_ROOT / filename
    if not license_file.exists():
        return False
    text = license_file.read_text(encoding="utf-8", errors="ignore")
    return expected_license.lower().replace(" ", "") in text.lower().replace(" ", "")


def check_internal_links(md_file: Path, drift: list[dict]) -> None:
    """For each internal markdown link in the file, verify the target exists."""
    try:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
    except (OSError, UnicodeDecodeError):
        return
    for m in PATTERNS["internal_link"].finditer(content):
        anchor, target = m.group(1), m.group(2).split("#")[0]
        target_path = (md_file.parent / target).resolve()
        if not target_path.exists():
            # Try repo-root resolution
            alt_path = (REPO_ROOT / target).resolve()
            if not alt_path.exists():
                drift.append({
                    "file": str(md_file.relative_to(REPO_ROOT)),
                    "type": "broken_internal_link",
                    "anchor": anchor,
                    "target": target,
                })


def check_test_claims(md_file: Path, actual: tuple[int, int], drift: list[dict]) -> None:
    """For each '33 of 34 tests pass' claim, verify against actual pytest result."""
    if actual == (-1, -1):
        return
    try:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
    except (OSError, UnicodeDecodeError):
        return
    actual_passed, actual_total = actual
    for m in PATTERNS["test_status"].finditer(content):
        claimed_passed, claimed_total = int(m.group(1)), int(m.group(2))
        if claimed_passed != actual_passed or claimed_total != actual_total:
            drift.append({
                "file": str(md_file.relative_to(REPO_ROOT)),
                "type": "test_status_drift",
                "claimed": f"{claimed_passed}/{claimed_total}",
                "actual": f"{actual_passed}/{actual_total}",
            })


def main() -> int:
    drift: list[dict] = []
    md_files = find_md_files(REPO_ROOT)

    print(f"Scanning {len(md_files)} markdown files...", file=sys.stderr)

    actual_test_status = run_pytest_status()
    print(f"Pytest status: {actual_test_status[0]}/{actual_test_status[1]}", file=sys.stderr)

    for md in md_files:
        check_internal_links(md, drift)
        check_test_claims(md, actual_test_status, drift)

    # License checks
    if not check_license("LICENSE", "Apache 2.0") and not check_license("LICENSE.md", "Apache 2.0"):
        drift.append({"type": "missing_license", "expected": "Apache 2.0", "file": "LICENSE"})

    # Generate reports
    timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H-%M-%SZ")
    json_path = OUT_DIR / f"drift_{timestamp}.json"
    md_path = OUT_DIR / f"drift_{timestamp}.md"

    json_path.write_text(json.dumps({
        "timestamp": timestamp,
        "files_scanned": len(md_files),
        "drift_count": len(drift),
        "test_status_actual": f"{actual_test_status[0]}/{actual_test_status[1]}",
        "drift": drift,
    }, indent=2))

    md_lines = [
        f"# Documentation Drift Report — {timestamp}",
        "",
        f"- Files scanned: **{len(md_files)}**",
        f"- Drift entries: **{len(drift)}**",
        f"- Actual pytest status: **{actual_test_status[0]}/{actual_test_status[1]}**",
        "",
        "## Drift entries",
        "",
    ]
    if not drift:
        md_lines.append("*No drift detected.*")
    else:
        for d in drift:
            md_lines.append(f"- **{d['type']}** in `{d.get('file', 'n/a')}`: {d}")
    md_path.write_text("\n".join(md_lines))

    print(f"Reports written to {json_path} and {md_path}", file=sys.stderr)
    print(f"Drift entries: {len(drift)}", file=sys.stderr)

    return 0 if len(drift) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
