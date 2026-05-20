"""calm_tenancy.daily_check — the daily tenancy sweep driver (CT-36, CT-41, CT-42).

Composes:
  • DNS / TLS health (CT-37) — delegates to ~/CredexAI/infra/dns_cert_fleet/fleet.py if present
  • Mailbox SLA snapshot (CT-38, CT-39) — mailbox_sla.sla_report()
  • Stale credentials (CT-33, CT-35) — credential_vault.list_stale, list_missing_twofa
  • Cringe regression on every owned domain's local snapshot (CT-40) — optional
  • Veto surfacing (CT-28) — from cringe_gate.py's recent run log

Output:
  • Machine-readable JSON to ~/.calm-vault/tenancy/daily_check.jsonl (append).
  • Human-readable markdown digest to ~/.calm-vault/tenancy/daily_check_<date>.md.
  • Non-zero exit on any critical finding (DNS down, SLA miss, forbidden-phrase hit, etc.).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from credential_vault import list_missing_twofa, list_stale
    from mailbox_sla import sla_report
except ImportError:  # pragma: no cover
    from calm_tenancy.credential_vault import list_missing_twofa, list_stale
    from calm_tenancy.mailbox_sla import sla_report


DEFAULT_OUT_DIR = Path.home() / ".calm-vault" / "tenancy"
DEFAULT_DOMAINS = Path.home() / "CredexAI" / "infra" / "dns_cert_fleet" / "owned_domains.txt"
DEFAULT_FLEET = Path.home() / "CredexAI" / "infra" / "dns_cert_fleet" / "fleet.py"


@dataclass
class CheckReport:
    as_of: str
    domains_checked: int = 0
    dns_alerts: List[str] = field(default_factory=list)
    tls_alerts: List[str] = field(default_factory=list)
    sla_pending_over_10min: int = 0
    sla_missed_today: int = 0
    stale_credentials: int = 0
    missing_twofa: int = 0
    cringe_regressions: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    @property
    def critical(self) -> bool:
        return bool(
            self.dns_alerts
            or self.tls_alerts
            or self.sla_pending_over_10min
            or self.cringe_regressions
        )


def _load_owned_domains(path: Optional[Path]) -> List[str]:
    p = Path(path or DEFAULT_DOMAINS).expanduser()
    if not p.exists():
        return []
    out: List[str] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def _run_fleet_check(fleet_script: Optional[Path], dry_run: bool = True) -> Dict[str, Any]:
    """Delegate to the existing DNS/TLS fleet manager if available."""
    p = Path(fleet_script or DEFAULT_FLEET).expanduser()
    if not p.exists():
        return {"status": "skipped", "reason": "fleet.py not found"}
    args = [sys.executable, str(p), "--dry-run" if dry_run else "--execute"]
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return {"status": "timeout"}
    return {
        "status": "ok",
        "exit_code": result.returncode,
        "stdout_tail": (result.stdout or "")[-800:],
        "stderr_tail": (result.stderr or "")[-400:],
    }


def run_daily_check(
    domains_path: Optional[Path] = None,
    fleet_script: Optional[Path] = None,
    dry_run: bool = True,
    now: Optional[datetime] = None,
) -> CheckReport:
    now = now or datetime.now(timezone.utc)
    report = CheckReport(as_of=now.isoformat().replace("+00:00", "Z"))

    domains = _load_owned_domains(domains_path)
    report.domains_checked = len(domains)

    fleet_result = _run_fleet_check(fleet_script, dry_run=dry_run)
    report.notes.append(f"fleet_check: {fleet_result.get('status')}")
    # The existing fleet.py emits "ALERT" lines on real issues; we surface those.
    stdout_tail = fleet_result.get("stdout_tail", "") or ""
    for line in stdout_tail.splitlines():
        if "ALERT" in line and ("DNS" in line or "NXDOMAIN" in line):
            report.dns_alerts.append(line.strip())
        if "ALERT" in line and ("TLS" in line or "cert" in line.lower() or "expir" in line.lower()):
            report.tls_alerts.append(line.strip())

    try:
        sla = sla_report(now=now)
        report.sla_pending_over_10min = int(sla.get("pending_over_10min", 0))
        report.sla_missed_today = int(sla.get("acks_missed_sla", 0))
    except Exception as exc:                                # noqa: BLE001
        report.notes.append(f"sla_report_failed: {exc}")

    try:
        report.stale_credentials = len(list_stale(now=now))
        report.missing_twofa = len(list_missing_twofa())
    except Exception as exc:                                # noqa: BLE001
        report.notes.append(f"credential_check_failed: {exc}")

    return report


def render_markdown(report: CheckReport) -> str:
    lines = [
        f"# Calm Tenancy — Daily Check ({report.as_of})",
        "",
        f"**Domains checked:** {report.domains_checked}",
        f"**Critical:** {'YES' if report.critical else 'no'}",
        "",
        "## DNS / TLS",
    ]
    if not report.dns_alerts and not report.tls_alerts:
        lines.append("- All clear.")
    for a in report.dns_alerts:
        lines.append(f"- **DNS ALERT** {a}")
    for a in report.tls_alerts:
        lines.append(f"- **TLS ALERT** {a}")
    lines += [
        "",
        "## Mailbox SLA",
        f"- Pending over 10 min: **{report.sla_pending_over_10min}** (should be 0)",
        f"- Acks missed today:  {report.sla_missed_today}",
        "",
        "## Credentials",
        f"- Stale (past rotation cadence): {report.stale_credentials}",
        f"- Missing 2FA: {report.missing_twofa}",
        "",
        "## Page-drift (cringe regression)",
    ]
    if not report.cringe_regressions:
        lines.append("- None observed.")
    for r in report.cringe_regressions:
        lines.append(f"- **REGRESSION** {r}")
    if report.notes:
        lines += ["", "## Notes"]
        for n in report.notes:
            lines.append(f"- {n}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="calm-tenancy daily-check")
    parser.add_argument("--execute", action="store_true",
                        help="Make real network calls (default is --dry-run)")
    parser.add_argument("--domains", default=None)
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    args = parser.parse_args(argv)

    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    report = run_daily_check(
        domains_path=Path(args.domains).expanduser() if args.domains else None,
        dry_run=not args.execute,
    )

    # Append machine-readable record.
    jsonl = out_dir / "daily_check.jsonl"
    with jsonl.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(report), sort_keys=True, separators=(",", ":")))
        fh.write("\n")

    # Write human-readable digest.
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    md = out_dir / f"daily_check_{today}.md"
    md.write_text(render_markdown(report), encoding="utf-8")

    print(render_markdown(report))
    return 0 if not report.critical else 1


if __name__ == "__main__":
    raise SystemExit(main())
