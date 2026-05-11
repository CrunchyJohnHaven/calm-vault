"""Compute the (channel x task_type) leaderboard from work.jsonl.

Pure functions over plain dicts so the same code powers both
`orc leaderboard` and `orc recommend`, and is trivially unit-testable.
"""
from __future__ import annotations

import json
import statistics
from datetime import datetime, timezone
from pathlib import Path


def _parse_iso(ts: str | None) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except Exception:
        return None


def _delivery_hours(row: dict) -> float | None:
    a = _parse_iso(row.get("accepted_at"))
    d = _parse_iso(row.get("delivered_at"))
    if a and d:
        return max(0.0, (d - a).total_seconds() / 3600.0)
    return None


def _safe_mean(xs: list[float]) -> float | None:
    return statistics.fmean(xs) if xs else None


def aggregate(work_rows: list[dict]) -> dict[tuple[str, str], dict]:
    """Group rows by (channel, task_type) and compute means."""
    buckets: dict[tuple[str, str], list[dict]] = {}
    for r in work_rows:
        key = (r.get("channel", "?"), r.get("task_type", "?"))
        buckets.setdefault(key, []).append(r)

    out: dict[tuple[str, str], dict] = {}
    for key, rows in buckets.items():
        hourly = []
        qualities = []
        deliveries = []
        total_paid = 0.0
        total_hours = 0.0
        for r in rows:
            paid = float(r.get("total_paid_usd") or 0)
            hours = float(r.get("hours_worked") or 0)
            total_paid += paid
            total_hours += hours
            if hours > 0:
                hourly.append(paid / hours)
            q = r.get("quality_score_0_to_10")
            if isinstance(q, (int, float)):
                qualities.append(float(q))
            d = _delivery_hours(r)
            if d is not None:
                deliveries.append(d)
        mean_cost = _safe_mean(hourly)
        mean_quality = _safe_mean(qualities)
        mean_delivery = _safe_mean(deliveries)
        cost_per_quality = None
        if mean_cost is not None and mean_quality and mean_quality > 0:
            cost_per_quality = mean_cost / mean_quality
        out[key] = {
            "channel":           key[0],
            "task_type":         key[1],
            "n":                 len(rows),
            "total_paid_usd":    round(total_paid, 2),
            "total_hours":       round(total_hours, 2),
            "mean_cost_per_hr":  mean_cost,
            "mean_quality":      mean_quality,
            "mean_delivery_hrs": mean_delivery,
            "cost_per_quality":  cost_per_quality,
        }
    return out


def winners_per_task(work_rows: list[dict]) -> dict[str, dict | None]:
    """For each task_type seen, pick the channel with the best $/quality.

    Ties broken by highest mean quality, then lowest $/hr.
    Channels with n=0 or quality=None are ignored.
    """
    agg = aggregate(work_rows)
    by_task: dict[str, list[dict]] = {}
    for (_, task), row in agg.items():
        if row["mean_quality"] is None or row["cost_per_quality"] is None:
            continue
        by_task.setdefault(task, []).append(row)

    out: dict[str, dict | None] = {}
    for task, rows in by_task.items():
        ranked = sorted(
            rows,
            key=lambda r: (
                r["cost_per_quality"],            # lower is better
                -r["mean_quality"],               # higher is better
                r["mean_cost_per_hr"] or 1e9,     # lower is better
            ),
        )
        out[task] = ranked[0] if ranked else None
    return out


def recommend(work_rows: list[dict], task: str) -> dict | None:
    """Return the best channel for a single task_type, with `why` rationale."""
    winners = winners_per_task(work_rows)
    rec = winners.get(task)
    if not rec:
        return None
    rec = dict(rec)  # copy
    rec["why"] = (
        f"{rec['n']} sample(s); mean quality {rec['mean_quality']:.2f}/10 "
        f"at ${rec['mean_cost_per_hr']:.2f}/hr "
        f"= ${rec['cost_per_quality']:.2f} per quality-point"
    )
    return rec


def render_markdown(work_rows: list[dict], task_types: dict,
                    channels: dict) -> str:
    """Render the full leaderboard markdown."""
    agg = aggregate(work_rows)
    winners = winners_per_task(work_rows)

    out: list[str] = []
    out.append("# labor leaderboard  (channel x task_type)")
    out.append(f"_auto-generated; {len(work_rows)} work row(s); "
               f"{len(agg)} populated cell(s)_\n")

    if not work_rows:
        out.append("> No scored work yet. Cast nets via `orc post ...` and "
                   "then record deliveries via `orc score ...`.\n")

    out.append("## Per-task winners")
    out.append("| task_type | best channel | n | $/hr | quality | "
               "$/quality | delivery hr |")
    out.append("|---|---|---|---|---|---|---|")
    for task in sorted(task_types):
        w = winners.get(task)
        if w:
            dt = (f"{w['mean_delivery_hrs']:.1f}"
                  if w["mean_delivery_hrs"] is not None else "-")
            out.append(
                f"| {task} | **{w['channel']}** \u2605 | {w['n']} | "
                f"${w['mean_cost_per_hr']:.2f} | "
                f"{w['mean_quality']:.2f}/10 | "
                f"${w['cost_per_quality']:.2f} | {dt} |"
            )
        else:
            out.append(f"| {task} | _untested_ | 0 | - | - | - | - |")
    out.append("")

    # full grid
    out.append("## Full grid")
    if not agg:
        out.append("_(nothing scored yet)_")
        return "\n".join(out) + "\n"

    out.append("| task_type | channel | n | total $ | total hr | "
               "$/hr | quality | $/quality | delivery hr |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    sorted_cells = sorted(
        agg.values(),
        key=lambda r: (r["task_type"], r["cost_per_quality"]
                       if r["cost_per_quality"] is not None else 1e9),
    )
    for r in sorted_cells:
        star = " \u2605" if winners.get(r["task_type"], {}) and \
            winners[r["task_type"]]["channel"] == r["channel"] else ""
        def fmt(v, prefix="", suffix=""):
            if v is None:
                return "-"
            return f"{prefix}{v:.2f}{suffix}"
        out.append(
            f"| {r['task_type']} | {r['channel']}{star} | {r['n']} | "
            f"${r['total_paid_usd']:.2f} | {r['total_hours']:.2f} | "
            f"{fmt(r['mean_cost_per_hr'], '$')} | "
            f"{fmt(r['mean_quality'], '', '/10')} | "
            f"{fmt(r['cost_per_quality'], '$')} | "
            f"{fmt(r['mean_delivery_hrs'])} |"
        )
    out.append("")

    out.append("---")
    out.append("_$/quality = mean cost/hr divided by mean quality (0..10). "
               "Lower is better._")
    return "\n".join(out) + "\n"


# CLI entrypoint for standalone use:  python3 scripts/compute_leaderboard.py
if __name__ == "__main__":
    import argparse
    import sys

    ap = argparse.ArgumentParser(
        description="Compute and print the labor leaderboard from work.jsonl"
    )
    ap.add_argument("--work", default="state/work.jsonl",
                    help="path to work.jsonl (relative to labor/)")
    ap.add_argument("--task-types", default="task_types.yaml")
    ap.add_argument("--channels", default="channels.yaml")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent.parent  # labor/

    def _read_jsonl(p: Path) -> list[dict]:
        if not p.exists():
            return []
        rows: list[dict] = []
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
        return rows

    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML required (pip install -r labor/requirements.txt)")

    work = _read_jsonl(here / args.work)
    tt = yaml.safe_load((here / args.task_types).read_text())
    ch = yaml.safe_load((here / args.channels).read_text())
    sys.stdout.write(render_markdown(work, tt, ch))
