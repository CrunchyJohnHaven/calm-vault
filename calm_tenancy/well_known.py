"""calm_tenancy.well_known — generate ``.well-known/calm-tenancy.json`` per domain (CT-04).

Each owned domain publishes a public tenancy assertion at
``https://<domain>/.well-known/calm-tenancy.json``. Counterparties read it
to learn who runs the domain, the operator's SLA, the rubric version,
the current chain head, and a signature.

This module generates the file content. It does NOT push the file to any
host — that step is per-domain manual (or per-CI). The generator outputs
canonical JSON ready to sign + publish.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


SCHEMA_VERSION = "calm-tenancy/v0"
DEFAULT_SLA_FIRST_ACK_SECONDS = 600  # 10 minutes
DEFAULT_RUBRIC_VERSION = "cringe-rubric/v1"
DEFAULT_OUT_DIR = Path.home() / ".calm-vault" / "tenancy" / "well_known"


@dataclass
class TenancyAssertion:
    schema_version: str
    domain: str
    operator_did: str
    principal_did: str
    mailbox: str
    sla: dict
    cringe_rubric_version: str
    chain_head_at_publish: str
    publish_ts: str
    well_known_signature: str = ""

    def canonical_bytes(self) -> bytes:
        d = asdict(self)
        # Sign over everything EXCEPT the signature itself.
        d.pop("well_known_signature", None)
        return json.dumps(d, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), indent=2)


def latest_chain_head(chain_path: Optional[Path] = None) -> str:
    """Read the last record_hash from ``~/.calm-vault/user_state.jsonl``.

    Returns 64 zeros if the chain is empty / missing — the generator still
    produces a well-formed file in that case.
    """
    chain_path = Path(chain_path or Path.home() / ".calm-vault" / "user_state.jsonl")
    if not chain_path.exists():
        return "0" * 64
    last_hash = "0" * 64
    with chain_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                if isinstance(rec.get("record_hash"), str):
                    last_hash = rec["record_hash"]
            except json.JSONDecodeError:
                continue
    return last_hash


def build_assertion(
    domain: str,
    operator_id: str = "john-bradley",
    principal_did: str = "did:credexai:v1:john-bradley",
    mailbox: Optional[str] = None,
    sla_first_ack_seconds: int = DEFAULT_SLA_FIRST_ACK_SECONDS,
    rubric_version: str = DEFAULT_RUBRIC_VERSION,
    chain_head: Optional[str] = None,
    publish_ts: Optional[str] = None,
    sign_fn=None,                                       # callable(bytes) -> sig_hex
) -> TenancyAssertion:
    slug = domain.replace(".", "-")
    a = TenancyAssertion(
        schema_version=SCHEMA_VERSION,
        domain=domain,
        operator_did=f"did:calm:{operator_id}:{slug}",
        principal_did=principal_did,
        mailbox=mailbox or f"calm@{domain}",
        sla={"first_ack_seconds": sla_first_ack_seconds},
        cringe_rubric_version=rubric_version,
        chain_head_at_publish=chain_head or latest_chain_head(),
        publish_ts=(publish_ts or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")),
    )
    if sign_fn is not None:
        a.well_known_signature = sign_fn(a.canonical_bytes())
    else:
        # v0 placeholder: deterministic hash of the canonical bytes so the
        # field is well-formed for testing. Real signing wires in at E22.
        a.well_known_signature = hashlib.sha256(a.canonical_bytes()).hexdigest()
    return a


def load_owned_domains(path: Optional[Path] = None) -> List[str]:
    p = Path(path or Path.home() / "CredexAI" / "infra" / "dns_cert_fleet"
            / "owned_domains.txt").expanduser()
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s and not s.startswith("#"):
            out.append(s)
    return out


def generate_fleet(
    out_dir: Optional[Path] = None,
    owned_domains_path: Optional[Path] = None,
    publish_ts: Optional[str] = None,
) -> List[Path]:
    """Generate one .well-known/calm-tenancy.json per owned domain."""
    out = Path(out_dir or DEFAULT_OUT_DIR).expanduser()
    out.mkdir(parents=True, exist_ok=True)
    written: List[Path] = []
    for domain in load_owned_domains(owned_domains_path):
        a = build_assertion(domain=domain, publish_ts=publish_ts)
        dest = out / f"{domain}.calm-tenancy.json"
        dest.write_text(a.to_json() + "\n", encoding="utf-8")
        written.append(dest)
    return written


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="calm-tenancy well-known")
    sub = parser.add_subparsers(dest="cmd", required=True)

    pg = sub.add_parser("generate", help="Generate for one domain to stdout.")
    pg.add_argument("--domain", required=True)
    pg.add_argument("--operator-id", default="john-bradley")
    pg.add_argument("--mailbox")

    pf = sub.add_parser("fleet", help="Generate for every owned domain into a directory.")
    pf.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))

    args = parser.parse_args(argv)

    if args.cmd == "generate":
        a = build_assertion(domain=args.domain, operator_id=args.operator_id,
                            mailbox=args.mailbox)
        print(a.to_json())
        return 0
    if args.cmd == "fleet":
        written = generate_fleet(out_dir=Path(args.out_dir).expanduser())
        for p in written:
            print(p)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
