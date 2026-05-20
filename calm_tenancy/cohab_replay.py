"""calm_tenancy.cohab_replay — Cohab-class incident replay test (CT-46).

Locks the Cohab failure mode into a regression test. The 2026-05-16 Cohab
audit found ``/cohab`` live at 1.17 hits/50w against a 1.0 ceiling. This
module embeds a representative excerpt of the failure-class text and asserts
that the v1 cringe rubric scores it UNSHIPPABLE.

If CI ever passes this excerpt, the rubric has been weakened and the test
fails. The fixture text is deliberately a paraphrase of the failure pattern,
NOT the original Cohab content — we capture the *style* of failure, not
verbatim language that might itself be operator-sensitive.
"""
from __future__ import annotations

try:
    from cringe_gate import DENSITY_THRESHOLD, cringe_check
except ImportError:  # pragma: no cover
    from calm_tenancy.cringe_gate import DENSITY_THRESHOLD, cringe_check


# A 200-word paraphrase composed of the failure patterns the postmortem
# tagged: surveillance, manufactured precision, money math, mystical objects,
# corporate-poetic hybrid, reverence for John. NOT verbatim Cohab content.
COHAB_CLASS_FIXTURE = """
We recognized you on the way in. We have been paying attention.

The kettle is on at the third shelf in the wisdom library, and the door is
welcome. We weave the threads of intelligence into a tapestry that scales
with grace.

Your odds of being chosen are ~25% with a 3% upside on the next round. There
are 33 seats and a small grant from John Bradley waiting for the first 5%
who commit. John knows you. John believes in you.

This page is an offering. We know how this reads — trust us when we say
the math is sound. The luminous and incandescent founders we recognize
are not chosen by lottery; they are seen by us, on the way in.

The kettle stays on through Sunday. The candle in the wisdom library is
lit. We have been watching, and we have been ready. The threads of your
story will be woven into ours, with kindness, with prayer, with scale.

Co-authored by John, the founder, the seer, the source. Made on a Friday
night at the top floor, with grace and battalions of love.
""".strip()


def assert_cohab_class_unshippable(forbidden_phrases=None) -> dict:
    """Run the v1 rubric and return a summary; raises AssertionError on regression."""
    report = cringe_check(COHAB_CLASS_FIXTURE,
                          forbidden_phrases=forbidden_phrases or [])
    assert "UNSHIPPABLE" in report.verdict, (
        f"Cohab-class fixture must be UNSHIPPABLE under v1 rubric. "
        f"Got verdict={report.verdict!r}, density={report.density:.3f}"
    )
    assert report.density > DENSITY_THRESHOLD, (
        f"Density {report.density:.3f} did not exceed ceiling {DENSITY_THRESHOLD:.1f}"
    )
    return {
        "verdict": report.verdict,
        "density": report.density,
        "total_hits": report.total_hits,
        "ceiling": DENSITY_THRESHOLD,
        "by_axis": {k: v for k, v in report.per_axis_hits.items() if v},
    }


if __name__ == "__main__":
    import json
    summary = assert_cohab_class_unshippable()
    print("CT-46 Cohab replay: PASS")
    print(json.dumps(summary, indent=2))
