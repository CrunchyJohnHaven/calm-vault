#!/usr/bin/env python3
"""
obac_cli.py — single command-line driver for the OBAC / AVS / HARP demo.

Subcommands:
  init           Create a new chain.jsonl at the given path.
  keygen         Generate an Ed25519 keypair and print as base64.
  attest         Sign + append a claim about a subject to the chain.
  annotate       Append an annotation referencing a prior claim_id.
  halt           Submit a HARP halt attestation about a subject.
  synthesize     Run AVS over a chain + subject; emit SynthesisOutput JSON.
  quorum         Print HARP quorum status JSON for a subject.
  revoke         Emit revoke.sh from current HARP quorum state.
  verify         Verify chain integrity (signatures + hash links + Merkle root).
  show           Print all claims about a subject in human-readable order.

Keys are stored as base64-encoded raw Ed25519 bytes in files passed by --key-file.
The CLI is intentionally thin — heavy lifting lives in obac.py / avs.py / harp.py.
"""
from __future__ import annotations

import argparse
import base64
import json
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import obac
import avs
import harp
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)


def _load_priv(path: str) -> Ed25519PrivateKey:
    raw = base64.b64decode(pathlib.Path(path).read_text().strip())
    return Ed25519PrivateKey.from_private_bytes(raw)


def cmd_init(args: argparse.Namespace) -> int:
    chain = obac.Chain.new(args.path)
    print(f"chain initialized: {chain.path}")
    return 0


def cmd_keygen(args: argparse.Namespace) -> int:
    priv, pub = obac.gen_keypair()
    priv_b64 = base64.b64encode(
        priv.private_bytes_raw() if hasattr(priv, "private_bytes_raw") else
        priv.private_bytes(
            encoding=__import__("cryptography").hazmat.primitives.serialization.Encoding.Raw,
            format=__import__("cryptography").hazmat.primitives.serialization.PrivateFormat.Raw,
            encryption_algorithm=__import__("cryptography").hazmat.primitives.serialization.NoEncryption(),
        )
    ).decode()
    if args.out_priv:
        p = pathlib.Path(args.out_priv)
        p.write_text(priv_b64 + "\n")
        p.chmod(0o600)
        print(f"private key written: {p} (mode 600)")
    if args.out_pub:
        p = pathlib.Path(args.out_pub)
        p.write_text(obac.pubkey_b64(pub) + "\n")
        print(f"public key written:  {p}")
    print(f"did: {obac.did_for_pubkey(pub)}")
    return 0


def cmd_attest(args: argparse.Namespace) -> int:
    chain = obac.Chain.open(args.chain)
    priv = _load_priv(args.key_file)
    claim = obac.make_claim(
        subject_id=args.subject,
        attester_id=args.attester_id,
        claim_text=args.text,
        claim_type=args.type,
        evidence_pointers=args.evidence or [],
    )
    entry = chain.append_claim(claim, priv)
    print(json.dumps({
        "seq": entry["seq"],
        "claim_id": entry["envelope"]["payload"]["claim_id"],
        "entry_hash": entry["entry_hash"],
    }, indent=2))
    return 0


def cmd_annotate(args: argparse.Namespace) -> int:
    chain = obac.Chain.open(args.chain)
    priv = _load_priv(args.key_file)
    claim = obac.make_claim(
        subject_id=args.subject,
        attester_id=args.attester_id,
        claim_text=args.text,
        claim_type="annotation",
        annotates=args.annotates,
    )
    entry = chain.append_claim(claim, priv)
    print(json.dumps({
        "seq": entry["seq"],
        "annotation_id": entry["envelope"]["payload"]["claim_id"],
        "annotates": args.annotates,
    }, indent=2))
    return 0


def cmd_halt(args: argparse.Namespace) -> int:
    chain = obac.Chain.open(args.chain)
    priv = _load_priv(args.key_file)
    entry = harp.submit_halt(
        chain=chain,
        subject_id=args.subject,
        attester_id=args.attester_id,
        attester_priv=priv,
        violation_layer=args.layer,
        violation_evidence=args.evidence or [],
        rationale=args.rationale or "",
    )
    print(json.dumps({
        "seq": entry["seq"],
        "halt_claim_id": entry["envelope"]["payload"]["claim_id"],
    }, indent=2))
    return 0


def cmd_synthesize(args: argparse.Namespace) -> int:
    chain = obac.Chain.open(args.chain)
    synth = avs.Synthesizer(synthesizer_id=args.synthesizer_id)
    out = synth.synthesize(chain, args.subject)
    text = json.dumps(out, indent=2, sort_keys=True)
    if args.out:
        pathlib.Path(args.out).write_text(text)
        print(f"synthesis written: {args.out}")
    print(text)
    return 0


def cmd_quorum(args: argparse.Namespace) -> int:
    chain = obac.Chain.open(args.chain)
    res = harp.check_quorum(
        chain, args.subject,
        k=args.k,
        window_seconds=args.window,
        min_attester_reliability=args.min_reliability,
    )
    print(json.dumps(res.to_dict(), indent=2))
    return 0 if res.concurred else 3


def cmd_revoke(args: argparse.Namespace) -> int:
    chain = obac.Chain.open(args.chain)
    res = harp.check_quorum(chain, args.subject, k=args.k, window_seconds=args.window)
    script = harp.emit_revoke_script(res, agent_ids=args.agents)
    out_path = pathlib.Path(args.out)
    out_path.write_text(script)
    out_path.chmod(0o755)
    print(f"revoke script: {out_path}")
    print(f"concurred:     {res.concurred}")
    print(f"layer:         {res.layer}")
    return 0 if res.concurred else 3


def cmd_verify(args: argparse.Namespace) -> int:
    chain = obac.Chain.open(args.chain)
    ok, errors = chain.verify_integrity()
    print(json.dumps({
        "ok": ok,
        "entries": len(chain.entries),
        "head_hash": chain.head_hash(),
        "merkle_root": chain.merkle_root(),
        "errors": errors,
    }, indent=2))
    return 0 if ok else 4


def cmd_show(args: argparse.Namespace) -> int:
    chain = obac.Chain.open(args.chain)
    rows = []
    for e in chain.entries:
        p = e["envelope"]["payload"]
        if args.subject and p["subject_id"] != args.subject:
            continue
        rows.append({
            "seq": e["seq"],
            "attester": p["attester_id"],
            "type": p["claim_type"],
            "submitted_at": p["submitted_at"],
            "claim_id": p["claim_id"][:12],
            "text": (p["claim_text"][:80] + "...") if len(p["claim_text"]) > 80 else p["claim_text"],
        })
    print(json.dumps(rows, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="OBAC / AVS / HARP CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.add_argument("--path", required=True)

    s = sub.add_parser("keygen")
    s.add_argument("--out-priv", help="write base64-encoded private key here")
    s.add_argument("--out-pub", help="write base64-encoded public key here")

    s = sub.add_parser("attest")
    s.add_argument("--chain", required=True)
    s.add_argument("--key-file", required=True)
    s.add_argument("--subject", required=True)
    s.add_argument("--attester-id", required=True)
    s.add_argument("--text", required=True)
    s.add_argument("--type", default="factual",
                   choices=["factual", "opinion", "critique", "endorsement"])
    s.add_argument("--evidence", nargs="*", default=[])

    s = sub.add_parser("annotate")
    s.add_argument("--chain", required=True)
    s.add_argument("--key-file", required=True)
    s.add_argument("--subject", required=True)
    s.add_argument("--attester-id", required=True)
    s.add_argument("--text", required=True)
    s.add_argument("--annotates", required=True)

    s = sub.add_parser("halt")
    s.add_argument("--chain", required=True)
    s.add_argument("--key-file", required=True)
    s.add_argument("--subject", required=True)
    s.add_argument("--attester-id", required=True)
    s.add_argument("--layer", required=True)
    s.add_argument("--evidence", nargs="*", default=[])
    s.add_argument("--rationale", default="")

    s = sub.add_parser("synthesize")
    s.add_argument("--chain", required=True)
    s.add_argument("--subject", required=True)
    s.add_argument("--synthesizer-id", default="avs-cli")
    s.add_argument("--out", help="write JSON here as well as stdout")

    s = sub.add_parser("quorum")
    s.add_argument("--chain", required=True)
    s.add_argument("--subject", required=True)
    s.add_argument("-k", type=int, default=harp.DEFAULT_K)
    s.add_argument("--window", type=float, default=harp.DEFAULT_WINDOW_SECONDS)
    s.add_argument("--min-reliability", type=float, default=harp.DEFAULT_MIN_RELIABILITY)

    s = sub.add_parser("revoke")
    s.add_argument("--chain", required=True)
    s.add_argument("--subject", required=True)
    s.add_argument("--agents", nargs="+", required=True)
    s.add_argument("--out", default="revoke.sh")
    s.add_argument("-k", type=int, default=harp.DEFAULT_K)
    s.add_argument("--window", type=float, default=harp.DEFAULT_WINDOW_SECONDS)

    s = sub.add_parser("verify"); s.add_argument("--chain", required=True)
    s = sub.add_parser("show")
    s.add_argument("--chain", required=True)
    s.add_argument("--subject")

    args = p.parse_args(argv)
    return {
        "init": cmd_init, "keygen": cmd_keygen, "attest": cmd_attest,
        "annotate": cmd_annotate, "halt": cmd_halt, "synthesize": cmd_synthesize,
        "quorum": cmd_quorum, "revoke": cmd_revoke, "verify": cmd_verify,
        "show": cmd_show,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
