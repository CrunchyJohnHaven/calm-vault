#!/usr/bin/env python3
"""calm-witness verify-chain — Everest 28 (hash-chain construction & verification).

Walks a ``user_state.jsonl`` file from genesis and verifies:

  1. Each record's ``record_hash`` is the canonical-JSON sha256 of every field
     except ``record_hash`` itself, with sorted keys and ``(",",":")`` separators
     (per USER_STATE_PROTOCOL.md §"Canonicalization rule for record_hash").

  2. Each record's ``prev_hash`` equals the previous record's ``record_hash``,
     or is 64 zeros at the genesis row (seq == 1).

  3. The ``seq`` field is strictly increasing by 1 starting at 1.

Exit code is 0 on full verification, 1 on any failure. Reads exclusively from
the JSONL file; never decrypts, never opens any other vault artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional

try:
    from schema import validate_record  # when run as a script from this dir
except ImportError:  # pragma: no cover - import path tolerance
    from calm_witness.schema import validate_record  # when run as a module

GENESIS_PREV_HASH = "0" * 64


@dataclass
class RecordCheck:
    seq: int
    ok_hash: bool
    ok_link: bool
    ok_seq: bool
    stored_hash: str
    computed_hash: str
    expected_prev: str
    stored_prev: str
    schema_errors: List[str] = field(default_factory=list)

    @property
    def ok_schema(self) -> bool:
        return not self.schema_errors

    @property
    def ok(self) -> bool:
        return self.ok_hash and self.ok_link and self.ok_seq and self.ok_schema


def canonical_record_hash(record: dict) -> str:
    """Compute the canonical sha256 hex of a record, excluding ``record_hash``."""
    stripped = {k: v for k, v in record.items() if k != "record_hash"}
    canonical = json.dumps(stripped, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def verify_chain(
    records: Iterable[dict], check_schema: bool = True
) -> List[RecordCheck]:
    """Return a check result per record, in order.

    If ``check_schema`` is True (default), each record's payload is validated
    against the v0 JSON Schema (Everest 26). Schema errors flag the record as
    failing but do not halt verification of subsequent records.
    """
    results: List[RecordCheck] = []
    prev_record_hash: Optional[str] = None
    expected_seq = 1
    for record in records:
        stored_hash = record.get("record_hash", "")
        computed = canonical_record_hash(record)
        ok_hash = stored_hash == computed

        if prev_record_hash is None:
            expected_prev = GENESIS_PREV_HASH
        else:
            expected_prev = prev_record_hash
        stored_prev = record.get("prev_hash", "")
        ok_link = stored_prev == expected_prev

        seq = record.get("seq", -1)
        ok_seq = seq == expected_seq

        schema_errors = validate_record(record) if check_schema else []

        results.append(
            RecordCheck(
                seq=seq,
                ok_hash=ok_hash,
                ok_link=ok_link,
                ok_seq=ok_seq,
                stored_hash=stored_hash,
                computed_hash=computed,
                expected_prev=expected_prev,
                stored_prev=stored_prev,
                schema_errors=schema_errors,
            )
        )
        prev_record_hash = stored_hash
        expected_seq += 1
    return results


def load_jsonl(path: Path) -> List[dict]:
    records: List[dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}")
    return records


def render_report(path: Path, checks: List[RecordCheck], verbose: bool) -> str:
    lines = [f"calm-witness verify-chain: {path}"]
    failures = [c for c in checks if not c.ok]
    for c in checks:
        status = "OK" if c.ok else "FAIL"
        lines.append(f"  seq={c.seq:>4} {status}")
        if verbose or not c.ok:
            if not c.ok_seq:
                lines.append(f"    seq mismatch: stored={c.seq}")
            if not c.ok_hash:
                lines.append(f"    record_hash mismatch")
                lines.append(f"      stored:   {c.stored_hash}")
                lines.append(f"      computed: {c.computed_hash}")
            if not c.ok_link:
                lines.append(f"    prev_hash link broken")
                lines.append(f"      expected: {c.expected_prev}")
                lines.append(f"      stored:   {c.stored_prev}")
            if not c.ok_schema:
                lines.append(f"    schema errors:")
                for err in c.schema_errors:
                    lines.append(f"      - {err}")
    lines.append("")
    lines.append(
        f"Summary: {len(checks) - len(failures)}/{len(checks)} records verified"
        + (f", {len(failures)} FAILED" if failures else "")
    )
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="calm-witness verify-chain",
        description="Verify the integrity of a Calm Witness user_state.jsonl chain.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=str(Path.home() / ".calm-vault" / "user_state.jsonl"),
        help="Path to user_state.jsonl (default: ~/.calm-vault/user_state.jsonl)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print details for every record, not only failures",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-record output; print only the summary line",
    )
    parser.add_argument(
        "--no-schema",
        action="store_true",
        help="Skip JSON-schema validation (Everest 26); only check hash + link + seq",
    )
    args = parser.parse_args(argv)

    path = Path(args.path).expanduser()
    if not path.exists():
        print(f"calm-witness verify-chain: not found: {path}", file=sys.stderr)
        return 1

    records = load_jsonl(path)
    if not records:
        print(f"calm-witness verify-chain: empty chain: {path}", file=sys.stderr)
        return 1

    checks = verify_chain(records, check_schema=not args.no_schema)
    failures = [c for c in checks if not c.ok]

    if args.quiet:
        verified = len(checks) - len(failures)
        print(
            f"calm-witness verify-chain: {verified}/{len(checks)} verified"
            + (f", {len(failures)} FAILED" if failures else "")
        )
    else:
        print(render_report(path, checks, args.verbose))

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
