"""calm_tenancy.cli — unified Calm Tenancy CLI (CT-48).

One entry point for every shipped subcommand. Mirrors the calm-witness CLI
pattern. Subcommands:

    cringe-check         Pre-publish content gate (single file or stdin).
    precheck             Walk a built-site tree and gate every file.
    well-known           Generate ``.well-known/calm-tenancy.json`` for a domain or fleet.
    mailbox              Subcommands for the 10-minute auto-ack scheduler.
    credentials          Subcommands for the credential vault.
    daily                Run the daily tenancy check.
    classify             Classify an inbound (red/yellow/green) + response-seeking.

All subcommands are also runnable as standalone scripts; this CLI is the
ergonomic single-name surface.
"""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional


def _make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="calm-tenancy",
                                description="Calm Tenancy CLI (v0.0.1).")
    sub = p.add_subparsers(dest="cmd", required=True)

    cc = sub.add_parser("cringe-check",
                        help="Pre-publish cringe gate (one file).")
    cc.add_argument("path", nargs="?")
    cc.add_argument("--stdin", action="store_true")
    cc.add_argument("--phrases")
    cc.add_argument("--quiet", action="store_true")
    cc.set_defaults(handler="cringe")

    pc = sub.add_parser("precheck",
                        help="Walk a built-site tree and gate every file.")
    pc.add_argument("root")
    pc.add_argument("--phrases")
    pc.add_argument("--ext", action="append")
    pc.add_argument("--json", action="store_true")
    pc.set_defaults(handler="precheck")

    wk = sub.add_parser("well-known",
                        help="Generate .well-known/calm-tenancy.json for one or all domains.")
    wk.add_argument("--domain", help="Single domain; omit with --fleet")
    wk.add_argument("--fleet", action="store_true",
                    help="Generate for every owned domain")
    wk.add_argument("--out-dir")
    wk.set_defaults(handler="well_known")

    mb = sub.add_parser("mailbox",
                        help="Mailbox SLA subcommands (ingest / emit-acks / report).")
    mb.add_argument("mb_cmd", choices=["ingest", "emit-acks", "report"])
    mb.add_argument("rest", nargs=argparse.REMAINDER,
                    help="Pass-through args to the underlying subcommand")
    mb.set_defaults(handler="mailbox")

    cv = sub.add_parser("credentials",
                        help="Credential vault subcommands.")
    cv.add_argument("cv_cmd",
                    choices=["register", "stale", "audit-twofa", "mark-rotated",
                             "never-quote-check"])
    cv.add_argument("rest", nargs=argparse.REMAINDER)
    cv.set_defaults(handler="credentials")

    dl = sub.add_parser("daily", help="Run the daily tenancy check.")
    dl.add_argument("--execute", action="store_true")
    dl.add_argument("--domains")
    dl.add_argument("--out-dir")
    dl.set_defaults(handler="daily")

    cl = sub.add_parser("classify",
                        help="Classify an inbound text from stdin.")
    cl.set_defaults(handler="classify")

    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = _make_parser().parse_args(argv)

    if args.handler == "cringe":
        from cringe_gate import main as f
        forwarded = []
        if args.stdin:
            forwarded.append("--stdin")
        elif args.path:
            forwarded.append(args.path)
        if args.phrases:
            forwarded += ["--phrases", args.phrases]
        if args.quiet:
            forwarded.append("--quiet")
        return f(forwarded)

    if args.handler == "precheck":
        from precheck import main as f
        forwarded = [args.root]
        if args.phrases:
            forwarded += ["--phrases", args.phrases]
        for e in (args.ext or []):
            forwarded += ["--ext", e]
        if args.json:
            forwarded.append("--json")
        return f(forwarded)

    if args.handler == "well_known":
        from well_known import main as f
        if args.fleet:
            sub_args = ["fleet"]
            if args.out_dir:
                sub_args += ["--out-dir", args.out_dir]
        else:
            sub_args = ["generate", "--domain", args.domain]
        return f(sub_args)

    if args.handler == "mailbox":
        from mailbox_sla import main as f
        return f([args.mb_cmd] + (args.rest or []))

    if args.handler == "credentials":
        from credential_vault import main as f
        return f([args.cv_cmd] + (args.rest or []))

    if args.handler == "daily":
        from daily_check import main as f
        forwarded = []
        if args.execute:
            forwarded.append("--execute")
        if args.domains:
            forwarded += ["--domains", args.domains]
        if args.out_dir:
            forwarded += ["--out-dir", args.out_dir]
        return f(forwarded)

    if args.handler == "classify":
        from classify import classify_and_route
        text = sys.stdin.read()
        c, rs, w = classify_and_route(text)
        import json as j
        print(j.dumps({"classification": c, "response_seeking": rs,
                       "expected_window_seconds": int(w)}, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
