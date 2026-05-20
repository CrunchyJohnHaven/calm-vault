"""calm_operations.claim_protocol — SUMMIT 256/300 (CO-25) Shared Vault Protocol.

The claim-before-bag mechanism for parallel sessions. A session claims a SUMMIT
on the chain with a 60-min TTL before working it; another session reading the
chain knows that SUMMIT is in-progress and picks something else. On completion
the original session appends a `kind: "summit_bagged"` record referencing the
claim, releasing the slot.

Single source of truth: the principal's append-only chain at
``~/.calm-vault/user_state.jsonl``. No central coordinator. No race conditions
beyond the natural append-order of the chain itself.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "calm_tenancy"))
from chain_records import append_record, canonical_record_hash, _last_chain_state  # noqa: E402


DEFAULT_CHAIN = Path.home() / ".calm-vault" / "user_state.jsonl"
DEFAULT_TTL_MINUTES = 60


@dataclass
class Claim:
    summit_id: int                    # 1-300
    range_label: str                  # e.g. "Operations"
    session_id: str
    claimed_at_iso: str
    ttl_minutes: int


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def list_active_claims(chain_path: Optional[Path] = None,
                       now: Optional[datetime] = None) -> List[Claim]:
    """Walk the chain and return unexpired, unbagged claims."""
    chain_path = chain_path or DEFAULT_CHAIN
    now = now or _now_utc()
    if not chain_path.exists():
        return []
    claims: Dict[int, Claim] = {}
    bagged: set = set()
    with chain_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            kind = rec.get("kind", "")
            p = rec.get("payload", {})
            if kind == "summit_claim":
                sid = p.get("summit_id")
                if isinstance(sid, int):
                    claims[sid] = Claim(
                        summit_id=sid,
                        range_label=p.get("range_label", ""),
                        session_id=p.get("session_id", ""),
                        claimed_at_iso=p.get("claimed_at_iso", rec.get("ts", "")),
                        ttl_minutes=int(p.get("ttl_minutes", DEFAULT_TTL_MINUTES)),
                    )
            elif kind == "summit_bagged":
                sid = (p.get("summit_id")
                       or p.get("summit_number")
                       or p.get("summit_number_in_route_map"))
                if isinstance(sid, int):
                    bagged.add(sid)
    active: List[Claim] = []
    for sid, c in claims.items():
        if sid in bagged:
            continue
        try:
            claimed_at = datetime.fromisoformat(
                c.claimed_at_iso.replace("Z", "+00:00")
            )
        except ValueError:
            continue
        if now < claimed_at + timedelta(minutes=c.ttl_minutes):
            active.append(c)
    return active


def is_claimed(summit_id: int,
               chain_path: Optional[Path] = None,
               now: Optional[datetime] = None) -> bool:
    return any(c.summit_id == summit_id
               for c in list_active_claims(chain_path, now))


def claim_summit(summit_id: int,
                 range_label: str,
                 session_id: Optional[str] = None,
                 ttl_minutes: int = DEFAULT_TTL_MINUTES,
                 chain_path: Optional[Path] = None,
                 now: Optional[datetime] = None) -> Dict[str, Any]:
    """Append a `kind: "summit_claim"` record. Returns the record."""
    chain_path = chain_path or DEFAULT_CHAIN
    now = now or _now_utc()
    if is_claimed(summit_id, chain_path, now):
        raise ValueError(f"SUMMIT {summit_id}/300 already claimed and unexpired")
    if not (1 <= summit_id <= 300):
        raise ValueError(f"summit_id out of EVEREST range (1-300): {summit_id}")
    session_id = session_id or str(uuid.uuid4())
    last_seq, prev_hash = _last_chain_state(chain_path)
    rec = {
        "kind": "summit_claim",
        "operator": "CALM",
        "payload": {
            "summit_id": summit_id,
            "range_label": range_label,
            "session_id": session_id,
            "claimed_at_iso": _iso(now),
            "ttl_minutes": ttl_minutes,
        },
        "prev_hash": prev_hash,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": last_seq + 1,
        "ts": _iso(now),
        "ts_source": "claim_protocol",
    }
    rec["record_hash"] = canonical_record_hash(rec)
    append_record(rec, chain_path=chain_path)
    return rec


def bag_summit(summit_id: int,
               summit_name: str,
               phase: str,
               evidence_paths: List[str],
               session_id: str,
               chain_path: Optional[Path] = None,
               now: Optional[datetime] = None) -> Dict[str, Any]:
    """Append a `kind: "summit_bagged"` record. Releases the claim."""
    chain_path = chain_path or DEFAULT_CHAIN
    now = now or _now_utc()
    last_seq, prev_hash = _last_chain_state(chain_path)
    rec = {
        "kind": "summit_bagged",
        "operator": "CALM",
        "payload": {
            "summit_id": summit_id,
            "summit_number_in_route_map": summit_id,
            "summit_name": summit_name,
            "phase": phase,
            "bagged_at_local": _iso(now),
            "bagged_by": session_id,
            "evidence_paths": evidence_paths,
        },
        "prev_hash": prev_hash,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": last_seq + 1,
        "ts": _iso(now),
        "ts_source": "claim_protocol",
    }
    rec["record_hash"] = canonical_record_hash(rec)
    append_record(rec, chain_path=chain_path)
    return rec


def main() -> int:
    p = argparse.ArgumentParser(prog="calm-operations claim")
    sub = p.add_subparsers(dest="cmd", required=True)

    pc = sub.add_parser("claim")
    pc.add_argument("--summit-id", type=int, required=True)
    pc.add_argument("--range", required=True)
    pc.add_argument("--ttl-min", type=int, default=DEFAULT_TTL_MINUTES)

    pb = sub.add_parser("bag")
    pb.add_argument("--summit-id", type=int, required=True)
    pb.add_argument("--name", required=True)
    pb.add_argument("--phase", required=True)
    pb.add_argument("--evidence", nargs="+", required=True)
    pb.add_argument("--session-id", required=True)

    pl = sub.add_parser("list")

    args = p.parse_args()
    if args.cmd == "claim":
        rec = claim_summit(args.summit_id, args.range, ttl_minutes=args.ttl_min)
        print(json.dumps({"claimed": args.summit_id,
                          "session_id": rec["payload"]["session_id"]}, indent=2))
        return 0
    if args.cmd == "bag":
        rec = bag_summit(args.summit_id, args.name, args.phase, args.evidence,
                         session_id=args.session_id)
        print(json.dumps({"bagged": args.summit_id,
                          "record_hash": rec["record_hash"]}, indent=2))
        return 0
    if args.cmd == "list":
        active = list_active_claims()
        print(json.dumps([asdict(c) for c in active], indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
