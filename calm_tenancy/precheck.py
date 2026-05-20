"""calm_tenancy.precheck — pre-publish CI hook (CT-21).

The deploy pipeline runs this against the about-to-be-published built site;
non-zero exit blocks the deploy. Walks every text-bearing file under a root
directory, runs the cringe gate against each, aggregates results, and exits
non-zero on any file that scores UNSHIPPABLE or any forbidden-phrase hit.

Usage (drop-in for a static-site deploy script):

    calm-tenancy precheck dist/ --phrases ~/.calm-vault/forbidden_phrases.txt
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional

try:
    from cringe_gate import cringe_check, load_forbidden_phrases
except ImportError:  # pragma: no cover
    from calm_tenancy.cringe_gate import cringe_check, load_forbidden_phrases


# Files we consider — anything text-bearing that a stranger might read.
DEFAULT_EXTENSIONS = {".html", ".htm", ".md", ".txt", ".json", ".js", ".css", ".rst"}


@dataclass
class FilePrecheck:
    path: str
    word_count: int
    total_hits: int
    density: float
    verdict: str
    forbidden_phrases: List[str] = field(default_factory=list)


@dataclass
class PrecheckReport:
    root: str
    files_scanned: int = 0
    files_passed: int = 0
    files_unshippable: int = 0
    files_surgical_fix: int = 0
    forbidden_phrase_files: int = 0
    failures: List[FilePrecheck] = field(default_factory=list)

    @property
    def critical(self) -> bool:
        return self.files_unshippable > 0 or self.forbidden_phrase_files > 0


def walk_files(
    root: Path,
    extensions: Optional[set] = None,
    skip_patterns: Optional[List[str]] = None,
) -> List[Path]:
    extensions = extensions or DEFAULT_EXTENSIONS
    skip_patterns = skip_patterns or ["node_modules", ".git", "__pycache__", ".next", "build"]
    out = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in extensions:
            continue
        rel = str(p.relative_to(root))
        if any(skip in rel for skip in skip_patterns):
            continue
        out.append(p)
    return out


def precheck_tree(
    root: Path,
    forbidden_phrases: Optional[List[str]] = None,
    extensions: Optional[set] = None,
) -> PrecheckReport:
    forbidden_phrases = (forbidden_phrases
                         if forbidden_phrases is not None
                         else load_forbidden_phrases())
    report = PrecheckReport(root=str(root))
    for path in walk_files(root, extensions=extensions):
        try:
            raw = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rpt = cringe_check(raw, forbidden_phrases=forbidden_phrases)
        report.files_scanned += 1
        fpc = FilePrecheck(
            path=str(path),
            word_count=rpt.word_count,
            total_hits=rpt.total_hits,
            density=rpt.density,
            verdict=rpt.verdict,
            forbidden_phrases=[ph for ph, _ in rpt.forbidden_phrase_hits],
        )
        if rpt.forbidden_phrase_hits:
            report.forbidden_phrase_files += 1
            report.failures.append(fpc)
        elif "UNSHIPPABLE" in rpt.verdict:
            report.files_unshippable += 1
            report.failures.append(fpc)
        elif rpt.verdict == "surgical fix":
            report.files_surgical_fix += 1
        else:
            report.files_passed += 1
    return report


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="calm-tenancy precheck",
                                     description="Pre-publish cringe-gate sweep (CT-21).")
    parser.add_argument("root", help="Root directory to scan (e.g., dist/)")
    parser.add_argument("--phrases", help="Path to forbidden-phrases file")
    parser.add_argument("--ext", action="append",
                        help="Extra extensions to scan (e.g., --ext .vue)")
    parser.add_argument("--json", action="store_true",
                        help="Emit JSON instead of human-readable output")
    args = parser.parse_args(argv)

    root = Path(args.root).expanduser()
    if not root.exists():
        print(f"calm-tenancy precheck: root not found: {root}", file=sys.stderr)
        return 2
    phrases = (load_forbidden_phrases(Path(args.phrases)) if args.phrases
               else load_forbidden_phrases())
    extensions = DEFAULT_EXTENSIONS | set(args.ext) if args.ext else None
    report = precheck_tree(root, forbidden_phrases=phrases, extensions=extensions)

    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print(f"calm-tenancy precheck: root={root}")
        print(f"  scanned:        {report.files_scanned}")
        print(f"  passed:         {report.files_passed}")
        print(f"  surgical fix:   {report.files_surgical_fix}")
        print(f"  UNSHIPPABLE:    {report.files_unshippable}")
        print(f"  forbidden hits: {report.forbidden_phrase_files}")
        if report.failures:
            print("\n  failures:")
            for f in report.failures:
                print(f"    {f.verdict:36s} d={f.density:6.3f}  {f.path}")
                if f.forbidden_phrases:
                    print(f"      forbidden: {f.forbidden_phrases}")
        if report.critical:
            print("\n  VERDICT: DEPLOY BLOCKED")
        else:
            print("\n  VERDICT: deploy ok")
    return 0 if not report.critical else 1


if __name__ == "__main__":
    raise SystemExit(main())
