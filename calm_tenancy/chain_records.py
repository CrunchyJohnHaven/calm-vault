"""calm_tenancy.chain_records — append Calm Tenancy records to the principal's chain (CT-15, CT-41).

Two record kinds:
  • ``tenancy_reply``       — one per outbound ack/substantive reply emitted by the operator.
  • ``tenancy_daily_check`` — one per daily check sweep.

These ride on the same ``~/.calm-vault/user_state.jsonl`` chain as Calm Witness
records. Schema is validated by Calm Witness's ``schema.py`` (which already
includes the permissive defaults for these kinds in its KIND_REGISTRY).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_CHAIN = Path.home() / ".calm-vault" / "user_state.jsonl"


def canonical_record_hash(record: Dict[str, Any]) -> str:
    """Re-implementation of Calm Witness canonicalization to keep this module standalone."""
    stripped = {k: v for k, v in record.items() if k != "record_hash"}
    canonical = json.dumps(stripped, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _last_chain_state(chain_path: Path):
    last_seq = 0
    prev_hash = "0" * 64
    if not chain_path.exists():
        return last_seq, prev_hash
    with chain_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            last_seq = rec.get("seq", last_seq)
            if isinstance(rec.get("record_hash"), str):
                prev_hash = rec["record_hash"]
    return last_seq, prev_hash


def build_tenancy_reply(
    receipt_id: str,
    ack_id: str,
    domain: str,
    mailbox: str,
    classification: str,
    response_value: str,             # "ack_first" | "substantive" | "refused" | "escalated"
    operator_id_hash: str,
    chain_path: Optional[Path] = None,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Build (but do not append) a ``kind: tenancy_reply`` chain record."""
    chain_path = Path(chain_path or DEFAULT_CHAIN).expanduser()
    last_seq, prev_hash = _last_chain_state(chain_path)
    now = now or datetime.now(timezone.utc)
    record = {
        "kind": "tenancy_reply",
        "operator": "CALM",
        "payload": {
            "receipt_id": receipt_id,
            "ack_id": ack_id,
            "domain": domain,
            "mailbox": mailbox,
            "classification": classification,
            "response_value": response_value,
            "operator_id_hash": operator_id_hash,
        },
        "prev_hash": prev_hash,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": last_seq + 1,
        "ts": now.isoformat().replace("+00:00", "Z"),
        "ts_source": "operator_local_clock",
    }
    record["record_hash"] = canonical_record_hash(record)
    return record


def build_tenancy_daily_check(
    domains_checked: int,
    dns_alerts: int,
    tls_alerts: int,
    sla_pending_over_10min: int,
    sla_missed_today: int,
    stale_credentials: int,
    missing_twofa: int,
    cringe_regressions: int,
    digest_sha256: str = "",
    chain_path: Optional[Path] = None,
    now: Optional[datetime] = None,
) -> Dict[str, Any]:
    """Build (but do not append) a ``kind: tenancy_daily_check`` chain record."""
    chain_path = Path(chain_path or DEFAULT_CHAIN).expanduser()
    last_seq, prev_hash = _last_chain_state(chain_path)
    now = now or datetime.now(timezone.utc)
    record = {
        "kind": "tenancy_daily_check",
        "operator": "CALM",
        "payload": {
            "domains_checked": domains_checked,
            "dns_alerts": dns_alerts,
            "tls_alerts": tls_alerts,
            "sla_pending_over_10min": sla_pending_over_10min,
            "sla_missed_today": sla_missed_today,
            "stale_credentials": stale_credentials,
            "missing_twofa": missing_twofa,
            "cringe_regressions": cringe_regressions,
            "digest_sha256": digest_sha256,
        },
        "prev_hash": prev_hash,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": last_seq + 1,
        "ts": now.isoformat().replace("+00:00", "Z"),
        "ts_source": "operator_local_clock",
    }
    record["record_hash"] = canonical_record_hash(record)
    return record


def append_record(record: Dict[str, Any], chain_path: Optional[Path] = None) -> None:
    """Append a fully-built record to the chain. Caller is responsible for chain integrity."""
    p = Path(chain_path or DEFAULT_CHAIN).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
        fh.write("\n")


__all__ = [
    "build_tenancy_reply",
    "build_tenancy_daily_check",
    "append_record",
    "canonical_record_hash",
]
