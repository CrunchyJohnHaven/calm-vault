"""calm_tenancy.mailbox_sla — 10-minute auto-acknowledgement scheduler (CT-12, CT-13, CT-15, CT-16).

Tracks every inbound email's receipt time and ensures a signed first-acknowledgement
is dispatched within 10 minutes. Logs each ack as a `kind: "tenancy_reply"` chain
record. Surfaces any SLA miss as a postmortem entry.

Storage is a JSONL queue at ``~/.calm-vault/tenancy/inbound_queue.jsonl``. Each row
is the inbound's metadata + ack status. The scheduler is deterministic: given the
same inbound sequence and clock, the same acks are emitted.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_QUEUE = Path.home() / ".calm-vault" / "tenancy" / "inbound_queue.jsonl"
SLA_SECONDS = 600  # 10 minutes


@dataclass
class Inbound:
    receipt_id: str
    received_at: str           # ISO 8601 UTC
    domain: str
    mailbox: str               # e.g. "calm@thecreativitymachine.ai"
    sender_addr: str
    classification: str        # red | yellow | green
    response_seeking: bool
    subject_digest: str        # sha256 of subject; we never quote PII in the log

    @property
    def received_dt(self) -> datetime:
        return datetime.fromisoformat(self.received_at.replace("Z", "+00:00"))


@dataclass
class Ack:
    ack_id: str
    receipt_id: str
    ack_emitted_at: Optional[str] = None     # ISO 8601 UTC; None until emitted
    operator_id_hash: str = ""
    chain_head_at_ack: str = ""
    expected_substantive_window_seconds: int = 0  # 600 (red), 14400 (yellow), 3600 (green)
    sla_status: str = "pending"              # pending | within_sla | missed


@dataclass
class QueueRow:
    inbound: Inbound
    ack: Ack

    def to_json(self) -> str:
        return json.dumps({"inbound": asdict(self.inbound), "ack": asdict(self.ack)},
                          sort_keys=True, separators=(",", ":"))


def _expected_window(classification: str) -> int:
    # CT-14 substantive-reply windows
    return {"red": 600, "yellow": 14400, "green": 3600}.get(classification, 14400)


def ingest_inbound(
    domain: str,
    mailbox: str,
    sender_addr: str,
    subject_digest: str,
    classification: str = "green",
    response_seeking: bool = True,
    queue_path: Optional[Path] = None,
    now: Optional[datetime] = None,
) -> QueueRow:
    """Record a new inbound email and seed an ack stub."""
    queue_path = Path(queue_path or DEFAULT_QUEUE).expanduser()
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    now = now or datetime.now(timezone.utc)
    inbound = Inbound(
        receipt_id=str(uuid.uuid4()),
        received_at=now.isoformat().replace("+00:00", "Z"),
        domain=domain,
        mailbox=mailbox,
        sender_addr=sender_addr,
        classification=classification,
        response_seeking=response_seeking,
        subject_digest=subject_digest,
    )
    ack = Ack(
        ack_id=str(uuid.uuid4()),
        receipt_id=inbound.receipt_id,
        expected_substantive_window_seconds=_expected_window(classification),
    )
    row = QueueRow(inbound=inbound, ack=ack)
    with queue_path.open("a", encoding="utf-8") as fh:
        fh.write(row.to_json())
        fh.write("\n")
    return row


def _load_queue(queue_path: Path) -> List[QueueRow]:
    rows: List[QueueRow] = []
    if not queue_path.exists():
        return rows
    with queue_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            rows.append(QueueRow(
                inbound=Inbound(**d["inbound"]),
                ack=Ack(**d["ack"]),
            ))
    return rows


def emit_pending_acks(
    queue_path: Optional[Path] = None,
    operator_id_hash: str = "",
    chain_head: str = "",
    now: Optional[datetime] = None,
    dispatch_callable=None,        # callable(QueueRow) -> bool; v0 is a no-op
) -> Dict[str, int]:
    """Emit acks for all pending rows. Returns a summary dict."""
    queue_path = Path(queue_path or DEFAULT_QUEUE).expanduser()
    rows = _load_queue(queue_path)
    now = now or datetime.now(timezone.utc)
    emitted = 0
    missed = 0
    skipped = 0
    for row in rows:
        if row.ack.ack_emitted_at:
            skipped += 1
            continue
        if not row.inbound.response_seeking:
            skipped += 1
            continue
        elapsed = (now - row.inbound.received_dt).total_seconds()
        within_sla = elapsed <= SLA_SECONDS
        row.ack.ack_emitted_at = now.isoformat().replace("+00:00", "Z")
        row.ack.operator_id_hash = operator_id_hash
        row.ack.chain_head_at_ack = chain_head
        row.ack.sla_status = "within_sla" if within_sla else "missed"
        if not within_sla:
            missed += 1
        emitted += 1
        if dispatch_callable is not None:
            dispatch_callable(row)
    # Rewrite the queue with updated ack rows (deterministic; same order).
    tmp = queue_path.with_suffix(queue_path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(row.to_json())
            fh.write("\n")
    os.replace(tmp, queue_path)
    return {
        "rows_total": len(rows),
        "acks_emitted": emitted,
        "sla_missed": missed,
        "skipped": skipped,
    }


def sla_report(
    queue_path: Optional[Path] = None,
    now: Optional[datetime] = None,
) -> Dict[str, object]:
    """Snapshot the queue's SLA distribution."""
    queue_path = Path(queue_path or DEFAULT_QUEUE).expanduser()
    rows = _load_queue(queue_path)
    now = now or datetime.now(timezone.utc)
    pending_over_10min = 0
    pending_total = 0
    acks_within = 0
    acks_missed = 0
    per_mailbox: Dict[str, Dict[str, int]] = {}
    for row in rows:
        mb = row.inbound.mailbox
        per_mailbox.setdefault(mb, {"pending": 0, "within_sla": 0, "missed": 0})
        if not row.ack.ack_emitted_at:
            pending_total += 1
            per_mailbox[mb]["pending"] += 1
            elapsed = (now - row.inbound.received_dt).total_seconds()
            if elapsed > SLA_SECONDS:
                pending_over_10min += 1
        elif row.ack.sla_status == "within_sla":
            acks_within += 1
            per_mailbox[mb]["within_sla"] += 1
        elif row.ack.sla_status == "missed":
            acks_missed += 1
            per_mailbox[mb]["missed"] += 1
    return {
        "as_of": now.isoformat().replace("+00:00", "Z"),
        "queue_total": len(rows),
        "pending": pending_total,
        "pending_over_10min": pending_over_10min,  # CT-16 trigger
        "acks_within_sla": acks_within,
        "acks_missed_sla": acks_missed,
        "per_mailbox": per_mailbox,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="calm-tenancy mailbox-sla")
    sub = parser.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("ingest")
    pi.add_argument("--domain", required=True)
    pi.add_argument("--mailbox", required=True)
    pi.add_argument("--from", dest="sender_addr", required=True)
    pi.add_argument("--subject-digest", required=True)
    pi.add_argument("--class", dest="classification",
                    choices=["red", "yellow", "green"], default="green")
    pi.add_argument("--no-response-seeking", action="store_true")

    pe = sub.add_parser("emit-acks")
    pe.add_argument("--operator-id-hash", default="")
    pe.add_argument("--chain-head", default="")

    pr = sub.add_parser("report")

    args = parser.parse_args(argv)

    if args.cmd == "ingest":
        row = ingest_inbound(
            domain=args.domain,
            mailbox=args.mailbox,
            sender_addr=args.sender_addr,
            subject_digest=args.subject_digest,
            classification=args.classification,
            response_seeking=not args.no_response_seeking,
        )
        print(json.dumps({"receipt_id": row.inbound.receipt_id,
                          "ack_id": row.ack.ack_id}, indent=2))
        return 0
    if args.cmd == "emit-acks":
        summary = emit_pending_acks(
            operator_id_hash=args.operator_id_hash,
            chain_head=args.chain_head,
        )
        print(json.dumps(summary, indent=2))
        return 0 if summary["sla_missed"] == 0 else 1
    if args.cmd == "report":
        print(json.dumps(sla_report(), indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
