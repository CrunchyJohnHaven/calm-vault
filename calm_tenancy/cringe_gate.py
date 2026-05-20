"""calm_tenancy.cringe_gate — pre-publish content gate (CT-19, CT-20).

Codifies the 10-axis cringe rubric extracted from the Cohab postmortem
(``~/CredexAI/lab/cringeometer_2026-05-16/COHAB_LAUNCH_AUDIT_2026-05-16T_REVIEW.md``).

Density threshold: a page that scores > 1.0 hits per 50 words is UNSHIPPABLE.
A single forbidden-phrase hit hard-blocks publication regardless of density.

Usage:

    python3 cringe_gate.py path/to/page.html
    python3 cringe_gate.py --stdin < page.html

Exit codes:
    0 — page passes
    1 — page fails (density above threshold OR forbidden phrase)
    2 — bad input / file not found
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DENSITY_THRESHOLD = 1.0           # hits per 50 words; > 1.0 = UNSHIPPABLE
WORDS_PER_DENSITY_UNIT = 50


# 10 axes extracted from the Cohab cringe-ometer.
# Each axis is a list of compiled regex patterns. Match any → 1 hit.
RUBRIC: Dict[str, List[re.Pattern]] = {
    "1_military_cosplay": [
        re.compile(r"\b(soldier|soldiers|battalion|battalions|ranger|rangers|platoon|"
                   r"squad|squads|brigade|regiment|infantry|deployment|deployed|"
                   r"recon|recon[- ]team|wartime|frontline|trench|trenches|"
                   r"general\s+command|combat[- ]ready)\b", re.I),
    ],
    "2_mystical_anaphora": [
        re.compile(r"^(\s*)([A-Z][a-z]+ )([a-z]+ )?\1\2", re.M),  # opening-word repeats
        re.compile(r"\b(we are the|we who|those who|the ones who)\b.+\b\1\b", re.I),
    ],
    "3_manufactured_precision": [
        re.compile(r"~\d+\.?\d*\s*%"),                           # tilde-percent: ~55%
        re.compile(r"\bexactly\s+\d+\.?\d*\s*%"),
        re.compile(r"\b\d+\.\d{1,3}\s*%\s+(probability|chance|likelihood)\b", re.I),
        re.compile(r"\b\d+\.\d+x\b"),                            # 1.23x multipliers
    ],
    "4_reverence_for_john": [
        re.compile(r"\b(John (the principal|the founder|the seer|the source|the kindred))\b"),
        re.compile(r"\bJohn (knows|believes|loves|sees|cares about) (you|us|this|her|him|them)\b", re.I),
        re.compile(r"\b(co-?authored|co-?signed) (with|by) John\b", re.I),
    ],
    "5_self_aware_meta": [
        re.compile(r"\b(this page is|this letter is|this site is) (a|an) (offering|gift|love letter|prayer)\b", re.I),
        re.compile(r"\b(we know this sounds|we know how this reads|trust us when we say)\b", re.I),
    ],
    "6_corporate_poetic_hybrid": [
        re.compile(r"\b(scale|ship|launch|deploy)\b.{0,40}\b(love|grace|kindness|tenderness|prayer)\b", re.I),
        re.compile(r"\b(SaaS|MRR|ARR|TAM|CAC|LTV)\b.{0,40}\b(soul|heart|spirit)\b", re.I),
    ],
    "7_money_math_upfront": [
        re.compile(r"\$\d{1,3}(,\d{3})*(\.\d+)?(\s*(K|M|B|MM|million|billion))?\b", re.I),
        re.compile(r"\b(\d+\s+(seats|grants|tickets|spots))\b", re.I),
        re.compile(r"\b\d+\s*%\s+(equity|stake|share|grant|cut)\b", re.I),
        re.compile(r"\bsmall\s+grant\b", re.I),
    ],
    "8_ai_purple_metaphor": [
        re.compile(r"\b(weave|woven|tapestry)\b.{0,40}\b(intelligence|future|world|story)\b", re.I),
        re.compile(r"\b(threads of|the loom of|the river of|the dance of)\b", re.I),
        re.compile(r"\b(luminous|liminal|incandescent|effervescent)\b", re.I),
    ],
    "9_mystical_objects": [
        re.compile(r"\b(the kettle|the shelf|the candle|the lantern|the altar|the totem|the relic)\s+(is|stays|kept|placed)", re.I),
        re.compile(r"\b(kept on a shelf|on the third shelf|in the wisdom library)\b", re.I),
        re.compile(r"\b(the door is|the key is|the welcome is)\b", re.I),
    ],
    "10_persona_surveillance": [
        re.compile(r"\b(we recognized|we recognised|we noticed|we have been (paying attention|watching)|we have been keeping an eye on)\b", re.I),
        re.compile(r"\b(we saw you|we know you|we follow you)\b", re.I),
        re.compile(r"\b(on the way in|when you walked in|when you arrived)\b", re.I),
    ],
}


def strip_html(text: str) -> str:
    """Remove <style>, <script>, and all HTML tags. Crude but stdlib-only."""
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


@dataclass
class CringeReport:
    word_count: int
    per_axis_hits: Dict[str, int] = field(default_factory=dict)
    forbidden_phrase_hits: List[Tuple[str, str]] = field(default_factory=list)
    forbidden_phrases_loaded: int = 0

    @property
    def total_hits(self) -> int:
        return sum(self.per_axis_hits.values())

    @property
    def density(self) -> float:
        if self.word_count == 0:
            return 0.0
        return self.total_hits / (self.word_count / WORDS_PER_DENSITY_UNIT)

    @property
    def verdict(self) -> str:
        if self.forbidden_phrase_hits:
            return "UNSHIPPABLE (forbidden phrase)"
        if self.density > DENSITY_THRESHOLD:
            return "UNSHIPPABLE (density)"
        if self.density > DENSITY_THRESHOLD / 2:
            return "surgical fix"
        return "SHIP"


def load_forbidden_phrases(path: Optional[Path] = None) -> List[str]:
    """Load operator-specific forbidden phrases. Returns empty list if no file."""
    if path is None:
        path = Path.home() / ".calm-vault" / "forbidden_phrases.txt"
    if not path.exists():
        return []
    phrases: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            phrases.append(line)
    return phrases


def cringe_check(
    raw_text: str,
    forbidden_phrases: Optional[List[str]] = None,
) -> CringeReport:
    """Run the 10-axis rubric + forbidden-phrase scan over raw text."""
    visible = strip_html(raw_text)
    wc = word_count(visible)

    per_axis: Dict[str, int] = {}
    for axis_name, patterns in RUBRIC.items():
        hits = sum(len(p.findall(visible)) for p in patterns)
        per_axis[axis_name] = hits

    if forbidden_phrases is None:
        forbidden_phrases = load_forbidden_phrases()
    forbidden_hits: List[Tuple[str, str]] = []
    for phrase in forbidden_phrases:
        matches = re.findall(rf"\b{re.escape(phrase)}\b", visible, flags=re.I)
        for _ in matches:
            forbidden_hits.append((phrase, "matched"))

    return CringeReport(
        word_count=wc,
        per_axis_hits=per_axis,
        forbidden_phrase_hits=forbidden_hits,
        forbidden_phrases_loaded=len(forbidden_phrases),
    )


def render_report(report: CringeReport, source_label: str) -> str:
    lines = [f"calm-tenancy cringe-check: {source_label}"]
    lines.append(f"  words:    {report.word_count}")
    lines.append(f"  hits:     {report.total_hits}")
    lines.append(f"  density:  {report.density:.3f} (ceiling {DENSITY_THRESHOLD:.1f})")
    lines.append(f"  forbidden phrases loaded: {report.forbidden_phrases_loaded}")
    lines.append(f"  verdict:  {report.verdict}")
    if report.total_hits or report.forbidden_phrase_hits:
        lines.append("  hits per axis:")
        for axis, h in report.per_axis_hits.items():
            if h:
                lines.append(f"    {axis:35s} {h}")
        for phrase, _ in report.forbidden_phrase_hits:
            lines.append(f"    FORBIDDEN PHRASE: {phrase!r}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="calm-tenancy cringe-check",
        description="Pre-publish cringe rubric check (CT-19, CT-20).",
    )
    parser.add_argument("path", nargs="?", help="File path; omit with --stdin")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--phrases", help="Path to forbidden-phrases file")
    parser.add_argument("--quiet", action="store_true", help="Only print verdict line")
    args = parser.parse_args(argv)

    if args.stdin:
        raw = sys.stdin.read()
        label = "<stdin>"
    elif args.path:
        p = Path(args.path).expanduser()
        if not p.exists():
            print(f"calm-tenancy cringe-check: not found: {p}", file=sys.stderr)
            return 2
        raw = p.read_text(encoding="utf-8")
        label = str(p)
    else:
        parser.print_help()
        return 2

    phrases = load_forbidden_phrases(Path(args.phrases)) if args.phrases else None
    report = cringe_check(raw, forbidden_phrases=phrases)
    if args.quiet:
        print(f"{label}: {report.verdict} (density {report.density:.3f})")
    else:
        print(render_report(report, label))
    return 0 if report.verdict == "SHIP" else 1


if __name__ == "__main__":
    raise SystemExit(main())
