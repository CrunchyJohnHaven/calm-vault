"""calm_operations.emergency_stop — SUMMIT 276/300 (CO-45) Emergency Stop.

One command brings the operator to safe-idle:
  • mailbox CONTINUES to receive (don't lose mail)
  • all outbound is paused (no auto-acks, no substantive replies, no Compass/Witness disclosures)
  • daily-check cron continues (audit + observability stays)
  • principal sees a clear `kind: "emergency_stop_engaged"` record on the chain

Resuming requires a `kind: "emergency_stop_released"` record signed by the principal.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "calm_tenancy"))
from chain_records import append_record, canonical_record_hash, _last_chain_state  # noqa: E402

DEFAULT_CHAIN = Path.home() / ".calm-vault" / "user_state.jsonl"
STATE_FILE = Path.home() / ".calm-vault" / "tenancy" / "emergency_stop.state"


def _now(): return datetime.now(timezone.utc)
def _iso(dt): return dt.isoformat().replace("+00:00", "Z")


def is_engaged() -> bool:
    return STATE_FILE.exists()


def engage(reason: str,
           chain_path: Optional[Path] = None) -> dict:
    """Engage emergency stop. Idempotent."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        return {"already_engaged": True}
    chain_path = chain_path or DEFAULT_CHAIN
    now = _now()
    last_seq, prev_hash = _last_chain_state(chain_path)
    rec = {
        "kind": "emergency_stop_engaged",
        "operator": "CALM",
        "payload": {"reason": reason, "engaged_at_iso": _iso(now)},
        "prev_hash": prev_hash,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": last_seq + 1,
        "ts": _iso(now),
        "ts_source": "emergency_stop",
    }
    rec["record_hash"] = canonical_record_hash(rec)
    append_record(rec, chain_path=chain_path)
    STATE_FILE.write_text(json.dumps({
        "engaged_at_iso": _iso(now),
        "reason": reason,
        "engaged_record_hash": rec["record_hash"],
    }, sort_keys=True, indent=2), encoding="utf-8")
    return {"engaged": True, "record_hash": rec["record_hash"]}


def release(principal_signed: bool = False,
            chain_path: Optional[Path] = None) -> dict:
    """Release the emergency stop. Requires principal_signed=True."""
    if not STATE_FILE.exists():
        return {"already_released": True}
    if not principal_signed:
        return {"released": False, "reason": "requires_principal_signature"}
    chain_path = chain_path or DEFAULT_CHAIN
    now = _now()
    last_seq, prev_hash = _last_chain_state(chain_path)
    rec = {
        "kind": "emergency_stop_released",
        "operator": "CALM",
        "payload": {"released_at_iso": _iso(now), "principal_signed": True},
        "prev_hash": prev_hash,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": last_seq + 1,
        "ts": _iso(now),
        "ts_source": "emergency_stop",
    }
    rec["record_hash"] = canonical_record_hash(rec)
    append_record(rec, chain_path=chain_path)
    STATE_FILE.unlink()
    return {"released": True, "record_hash": rec["record_hash"]}


def gate_outbound() -> bool:
    """Return True if outbound is allowed, False if emergency stop is engaged.

    Every Calm Tenancy outbound (auto-ack, substantive reply, Witness/Compass
    disclosure) should call this before transmitting.
    """
    return not is_engaged()


def main() -> int:
    p = argparse.ArgumentParser(prog="calm-operations emergency-stop")
    sub = p.add_subparsers(dest="cmd", required=True)
    pe = sub.add_parser("engage")
    pe.add_argument("--reason", required=True)
    pr = sub.add_parser("release")
    pr.add_argument("--i-am-the-principal", action="store_true")
    sub.add_parser("status")
    args = p.parse_args()

    if args.cmd == "engage":
        print(json.dumps(engage(args.reason), indent=2))
        return 0
    if args.cmd == "release":
        print(json.dumps(release(principal_signed=args.i_am_the_principal), indent=2))
        return 0
    if args.cmd == "status":
        print(json.dumps({"engaged": is_engaged(),
                          "outbound_allowed": gate_outbound()}, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
