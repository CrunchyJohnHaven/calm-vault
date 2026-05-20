"""calm_witness.cli — Everest 84 (SDK ergonomics) entry point.

Single command, named subcommands, one-line help. Wraps the underlying modules
without adding logic. Run:

    python3 -m calm_witness <subcommand>
    python3 cli.py <subcommand>

Subcommands:

    verify-chain     Walk the chain at ~/.calm-vault/user_state.jsonl and verify it.
    eval-predicate   Evaluate a v0 predicate against the chain.
    authorize        Show the default authorization decision for (predicate, class).

Future subcommands ship at their summits:

    enroll           E11 — run the enrollment ceremony driver.
    capture          E12 + E13 — capture a behavioural sample.
    disclose         E66/E67 — issue a Calm Witness response from this operator.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from verify_chain import main as verify_main  # noqa: F401
    from predicates import REGISTRY, P_IN_BASELINE_24H_ID, evaluate
    from authorization import authorize_disclosure
except ImportError:  # pragma: no cover
    from calm_witness.verify_chain import main as verify_main  # noqa: F401
    from calm_witness.predicates import REGISTRY, P_IN_BASELINE_24H_ID, evaluate
    from calm_witness.authorization import authorize_disclosure


def _load_chain(path: Path):
    records = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def cmd_verify(args):
    return verify_main([args.path] + (["-v"] if args.verbose else [])
                       + (["--quiet"] if args.quiet else []))


def cmd_eval(args):
    path = Path(args.path).expanduser()
    if not path.exists():
        print(f"chain not found: {path}", file=sys.stderr)
        return 1
    chain = _load_chain(path)
    if args.predicate not in REGISTRY:
        print(f"unknown predicate: {args.predicate}", file=sys.stderr)
        print(f"available: {sorted(REGISTRY)}", file=sys.stderr)
        return 1
    try:
        result = evaluate(args.predicate, chain_window=chain)
    except NotImplementedError as exc:
        print(f"predicate not yet implemented: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result.to_dict(), indent=2))
    return 0


def cmd_authorize(args):
    decision = authorize_disclosure(args.predicate, args.counterparty_class)
    print(json.dumps({
        "allowed": decision.allowed,
        "reason": decision.reason,
    }, indent=2))
    return 0 if decision.allowed else 3


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="calm-witness", description="Calm Witness CLI (v0).")
    sub = p.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("verify-chain", help="Verify the integrity of user_state.jsonl.")
    pv.add_argument("path", nargs="?",
                    default=str(Path.home() / ".calm-vault" / "user_state.jsonl"))
    pv.add_argument("-v", "--verbose", action="store_true")
    pv.add_argument("--quiet", action="store_true")
    pv.set_defaults(fn=cmd_verify)

    pe = sub.add_parser("eval-predicate", help="Evaluate a v0 predicate against the chain.")
    pe.add_argument("--predicate", default=P_IN_BASELINE_24H_ID,
                    help="Predicate ID (default: in_baseline_24h)")
    pe.add_argument("--path", default=str(Path.home() / ".calm-vault" / "user_state.jsonl"))
    pe.set_defaults(fn=cmd_eval)

    pa = sub.add_parser("authorize",
                        help="Show default authorization decision for (predicate, class).")
    pa.add_argument("predicate", help="Predicate ID")
    pa.add_argument("counterparty_class",
                    help="One of: financial, journalistic, medical, governmental, "
                         "peer-AI-collective, family, anonymous")
    pa.set_defaults(fn=cmd_authorize)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
