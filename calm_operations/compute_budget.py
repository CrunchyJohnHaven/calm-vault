"""calm_operations.compute_budget — SUMMIT 241/300 (CO-09) LLM compute budget per operator.

Daily / weekly / monthly cost caps. Soft warning at 80%, hard fail at 100%.
Operator running over budget refuses new compute-dispatching actions until
the principal lifts the cap or the window rolls over.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional


DEFAULT_LEDGER = Path.home() / ".calm-vault" / "tenancy" / "compute_ledger.jsonl"
DEFAULT_CAPS_USD = {
    "daily":   25.0,
    "weekly":  100.0,
    "monthly": 350.0,
}
SOFT_FRACTION = 0.80


@dataclass
class ComputeEvent:
    ts_iso: str
    provider: str               # "anthropic" | "openai" | "google" | "local"
    operator_did: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    purpose: str                # short tag: "compass_proof" | "tenancy_reply" | etc.


def _now() -> datetime: return datetime.now(timezone.utc)
def _iso(dt: datetime) -> str: return dt.isoformat().replace("+00:00", "Z")
def _parse(s: str) -> datetime: return datetime.fromisoformat(s.replace("Z", "+00:00"))


def record_event(event: ComputeEvent, ledger_path: Optional[Path] = None) -> None:
    p = Path(ledger_path or DEFAULT_LEDGER).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(event), sort_keys=True, separators=(",", ":")))
        fh.write("\n")


def _load_events(ledger_path: Path) -> List[ComputeEvent]:
    if not ledger_path.exists():
        return []
    out: List[ComputeEvent] = []
    with ledger_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(ComputeEvent(**json.loads(line)))
            except (TypeError, json.JSONDecodeError):
                continue
    return out


def window_totals(now: Optional[datetime] = None,
                  ledger_path: Optional[Path] = None) -> Dict[str, float]:
    now = now or _now()
    p = Path(ledger_path or DEFAULT_LEDGER).expanduser()
    events = _load_events(p)
    cutoffs = {
        "daily":   now - timedelta(days=1),
        "weekly":  now - timedelta(days=7),
        "monthly": now - timedelta(days=30),
    }
    totals: Dict[str, float] = {k: 0.0 for k in cutoffs}
    for e in events:
        try:
            ts = _parse(e.ts_iso)
        except ValueError:
            continue
        for k, c in cutoffs.items():
            if ts >= c:
                totals[k] += e.cost_usd
    return totals


def budget_check(caps: Optional[Dict[str, float]] = None,
                 now: Optional[datetime] = None,
                 ledger_path: Optional[Path] = None) -> Dict[str, object]:
    caps = caps or DEFAULT_CAPS_USD
    totals = window_totals(now=now, ledger_path=ledger_path)
    decisions: Dict[str, str] = {}
    overall = "ok"
    for window, cap in caps.items():
        used = totals.get(window, 0.0)
        if used >= cap:
            decisions[window] = "HARD-FAIL"
            overall = "HARD-FAIL"
        elif used >= cap * SOFT_FRACTION:
            decisions[window] = "SOFT-WARN"
            if overall == "ok":
                overall = "SOFT-WARN"
        else:
            decisions[window] = "ok"
    return {
        "overall": overall,
        "totals_usd": totals,
        "caps_usd": caps,
        "per_window": decisions,
    }


def authorize_dispatch(estimated_cost_usd: float,
                       caps: Optional[Dict[str, float]] = None,
                       now: Optional[datetime] = None,
                       ledger_path: Optional[Path] = None) -> Dict[str, object]:
    """Pre-dispatch check: would this call put any window over budget?"""
    caps = caps or DEFAULT_CAPS_USD
    totals = window_totals(now=now, ledger_path=ledger_path)
    for window, cap in caps.items():
        projected = totals.get(window, 0.0) + estimated_cost_usd
        if projected >= cap:
            return {"allowed": False, "reason": f"{window}_cap_would_be_breached",
                    "projected_usd": projected, "cap_usd": cap}
    return {"allowed": True}


def main() -> int:
    p = argparse.ArgumentParser(prog="calm-operations compute-budget")
    sub = p.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("add")
    pa.add_argument("--provider", required=True)
    pa.add_argument("--operator-did", required=True)
    pa.add_argument("--model", required=True)
    pa.add_argument("--in-toks", type=int, required=True)
    pa.add_argument("--out-toks", type=int, required=True)
    pa.add_argument("--cost", type=float, required=True)
    pa.add_argument("--purpose", default="unspecified")

    pc = sub.add_parser("check")
    pa2 = sub.add_parser("authorize")
    pa2.add_argument("--estimated", type=float, required=True)

    args = p.parse_args()
    if args.cmd == "add":
        record_event(ComputeEvent(
            ts_iso=_iso(_now()), provider=args.provider,
            operator_did=args.operator_did, model=args.model,
            input_tokens=args.in_toks, output_tokens=args.out_toks,
            cost_usd=args.cost, purpose=args.purpose,
        ))
        print("ok")
        return 0
    if args.cmd == "check":
        print(json.dumps(budget_check(), indent=2))
        return 0
    if args.cmd == "authorize":
        d = authorize_dispatch(args.estimated)
        print(json.dumps(d, indent=2))
        return 0 if d["allowed"] else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
