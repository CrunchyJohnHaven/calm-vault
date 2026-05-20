"""calm_tenancy.credential_vault — credential registry, rotation, never-quote enforcement (CT-29, CT-31, CT-32).

v0 maintains a metadata registry only; actual secrets live in
``~/.calm-vault/master.priv.enc`` and the existing Calm Vault age-encrypted
artifacts. The operator NEVER sees the secret directly — it operates on the
registry's opaque handle and asks the vault to perform the operation.

The "never-quote rule" (CT-31) scans operator-generated outbound text for any
substring of any registered credential. Any match → outbound rejected. The
scanner is deterministic and self-contained: it loads the secrets locally,
scans, and discards. No secrets ever leave this process.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DEFAULT_REGISTRY = Path.home() / ".calm-vault" / "tenancy" / "credentials_registry.jsonl"

# CT-32 default rotation cadences.
ROTATION_CADENCE_DAYS = {
    "password":    90,
    "api_token":   30,
    "deploy_key":  180,
    "mailbox":     180,
    "registrar":   365,
    "dns_token":   90,
    "smtp":        180,
}


@dataclass
class CredentialMeta:
    """Metadata about a credential. Secret value lives elsewhere."""
    handle: str                  # e.g. "calm-vault.com:cloudflare-api"
    domain: str
    kind: str                    # password | api_token | deploy_key | mailbox | registrar | dns_token | smtp
    label: str                   # human-readable
    secret_pointer: str          # opaque path/identifier to the secret store; never the secret
    last_rotated_iso: str
    twofa_enabled: bool = False
    notes: str = ""

    def next_rotation_due(self) -> datetime:
        cadence = ROTATION_CADENCE_DAYS.get(self.kind, 90)
        return _parse_iso(self.last_rotated_iso) + timedelta(days=cadence)

    def is_stale(self, now: Optional[datetime] = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return now >= self.next_rotation_due()


def _parse_iso(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def _registry_path(path: Optional[Path]) -> Path:
    p = Path(path or DEFAULT_REGISTRY).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def register(meta: CredentialMeta, path: Optional[Path] = None) -> None:
    p = _registry_path(path)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(meta), sort_keys=True, separators=(",", ":")))
        fh.write("\n")


def load_all(path: Optional[Path] = None) -> List[CredentialMeta]:
    p = _registry_path(path)
    out: List[CredentialMeta] = []
    if not p.exists():
        return out
    with p.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            out.append(CredentialMeta(**json.loads(line)))
    return out


def list_stale(now: Optional[datetime] = None, path: Optional[Path] = None) -> List[CredentialMeta]:
    """CT-33 stale-credential daily alert."""
    return [c for c in load_all(path) if c.is_stale(now=now)]


def list_missing_twofa(path: Optional[Path] = None) -> List[CredentialMeta]:
    """CT-35 2FA inventory."""
    return [c for c in load_all(path) if not c.twofa_enabled]


def mark_rotated(handle: str, now: Optional[datetime] = None,
                 path: Optional[Path] = None) -> bool:
    """Append a rotation event. The original record stays; the newest wins."""
    creds = load_all(path)
    match: Optional[CredentialMeta] = None
    for c in creds:
        if c.handle == handle:
            match = c
    if match is None:
        return False
    now = now or datetime.now(timezone.utc)
    fresh = CredentialMeta(**{**asdict(match),
                              "last_rotated_iso": now.isoformat().replace("+00:00", "Z")})
    register(fresh, path=path)
    return True


# --- CT-31 never-quote rule -------------------------------------------------

def scan_outbound_for_credentials(
    outbound_text: str,
    loaded_secrets: List[str],
    min_len: int = 8,
) -> List[Tuple[int, str]]:
    """Return list of (offset, masked-fingerprint) for any secret found in outbound_text.

    Secrets shorter than ``min_len`` are skipped (prevents false-positive on
    common substrings); for password-like 8+ char secrets the check is exact.
    """
    hits: List[Tuple[int, str]] = []
    for secret in loaded_secrets:
        if not secret or len(secret) < min_len:
            continue
        idx = outbound_text.find(secret)
        if idx >= 0:
            fp = hashlib.sha256(secret.encode("utf-8")).hexdigest()[:12]
            hits.append((idx, fp))
    return hits


def never_quote_check(outbound_text: str, loaded_secrets: List[str]) -> Dict[str, object]:
    """The full CT-31 check. Returns a structured decision."""
    hits = scan_outbound_for_credentials(outbound_text, loaded_secrets)
    return {
        "allowed": not hits,
        "hit_count": len(hits),
        "hits_fingerprints": [fp for _, fp in hits],   # only fingerprints; never the secret
        "reason": "ok" if not hits else "outbound contains a registered credential substring",
    }


# --- CLI --------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="calm-tenancy credential-vault")
    sub = parser.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("register")
    pr.add_argument("--handle", required=True)
    pr.add_argument("--domain", required=True)
    pr.add_argument("--kind", required=True,
                    choices=list(ROTATION_CADENCE_DAYS.keys()))
    pr.add_argument("--label", required=True)
    pr.add_argument("--secret-pointer", required=True,
                    help="Opaque path/identifier to where the secret actually lives. NOT the secret itself.")
    pr.add_argument("--twofa-enabled", action="store_true")
    pr.add_argument("--notes", default="")

    ps = sub.add_parser("stale")
    pa = sub.add_parser("audit-twofa")
    pm = sub.add_parser("mark-rotated")
    pm.add_argument("--handle", required=True)

    pn = sub.add_parser("never-quote-check")
    pn.add_argument("--outbound", required=True,
                    help="Path to outbound text; will be scanned, not stored.")
    pn.add_argument("--secrets-file", required=True,
                    help="Path to file with one secret per line (read locally, never sent).")

    args = parser.parse_args(argv)

    if args.cmd == "register":
        meta = CredentialMeta(
            handle=args.handle, domain=args.domain, kind=args.kind,
            label=args.label, secret_pointer=args.secret_pointer,
            last_rotated_iso=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            twofa_enabled=args.twofa_enabled, notes=args.notes,
        )
        register(meta)
        print(f"registered: {args.handle}")
        return 0
    if args.cmd == "stale":
        stale = list_stale()
        print(json.dumps([asdict(c) for c in stale], indent=2))
        return 0 if not stale else 3
    if args.cmd == "audit-twofa":
        missing = list_missing_twofa()
        print(json.dumps([asdict(c) for c in missing], indent=2))
        return 0 if not missing else 4
    if args.cmd == "mark-rotated":
        ok = mark_rotated(args.handle)
        return 0 if ok else 1
    if args.cmd == "never-quote-check":
        outbound = Path(args.outbound).expanduser().read_text(encoding="utf-8")
        secrets_text = Path(args.secrets_file).expanduser().read_text(encoding="utf-8")
        secrets = [line.strip() for line in secrets_text.splitlines()
                   if line.strip() and not line.startswith("#")]
        decision = never_quote_check(outbound, secrets)
        print(json.dumps(decision, indent=2))
        return 0 if decision["allowed"] else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
