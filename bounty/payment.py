#!/usr/bin/env python3
"""AAL Bug Bounty — payment dispatcher.

Once a human reviewer marks a submission ``accepted``, this script fires the
payout on the rail the reporter requested:

  - **Stripe** — payouts via Stripe Connect Express (preferred for US reporters)
  - **Wise**   — international bank transfer via Wise's Transfers API
  - **USDC on Base** — on-chain ERC-20 transfer to a reporter-supplied address

A human always runs this script with explicit consent — there is no auto-pay.
The Cloudflare Worker only records submissions; nothing here is exposed to the
public internet. Run it from a hardened reviewer workstation.

Flow:

  1. Reviewer marks the submission accepted in D1 (see ``review.sql`` examples
     below) and records ``payout_usd_cents`` plus the verified payout
     destination on the appropriate rail.
  2. Reviewer runs ``python3 bounty/payment.py --id AAL-XXXX-XXXX-XXXX``.
  3. The script reads the accepted row, dispatches to the matching rail, and
     writes ``paid_at`` / ``payout_ref`` back to D1 on success.
  4. The reviewer manually opens a Component 3 attestation referencing the
     tracking id and the published payout reference, then writes a row into
     ``bounty_attestations``.

This file documents the flow inline and ships a working CLI. Every external
call is gated behind ``--confirm`` so accidental invocation cannot move money.

Environment:
    STRIPE_API_KEY                Stripe secret key (sk_live_... or sk_test_...).
    WISE_API_TOKEN                Wise API token.
    WISE_PROFILE_ID               Wise business profile id.
    USDC_BASE_RPC_URL             Base mainnet JSON-RPC endpoint.
    USDC_BASE_PRIVATE_KEY         Hex private key for the payout wallet.
    BOUNTY_D1_NAME                D1 database name (default: ``aal-bounty``).
    BOUNTY_WRANGLER               Path to wrangler (default: ``wrangler``).

Apache 2.0 · github.com/CrunchyJohnHaven/calm-vault
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


# ---------------------------------------------------------------------------
# D1 plumbing
# ---------------------------------------------------------------------------


def d1_name() -> str:
    return os.environ.get("BOUNTY_D1_NAME", "aal-bounty")


def wrangler_bin() -> str:
    return os.environ.get("BOUNTY_WRANGLER", "wrangler")


def d1_query(sql: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
    cmd = [
        wrangler_bin(),
        "d1",
        "execute",
        d1_name(),
        "--remote",
        "--json",
        "--command",
        sql,
    ]
    if params:
        cmd += ["--params", json.dumps(params)]

    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"wrangler d1 failed (exit {proc.returncode}): {proc.stderr.strip()}"
        )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"wrangler d1 returned non-JSON: {e}: {proc.stdout[:200]}")

    if isinstance(payload, list):
        rows: list[dict[str, Any]] = []
        for group in payload:
            results = group.get("results") if isinstance(group, dict) else None
            if isinstance(results, list):
                rows.extend(results)
        return rows
    return []


def load_accepted_submission(tracking_id: str) -> dict[str, Any]:
    rows = d1_query(
        """
        SELECT tracking_id, bug_class, payment_rail, accepted, paid_at,
               payout_usd_cents, payout_rail, payout_ref, contact, handle
        FROM bounty_submissions
        WHERE tracking_id = ?1 LIMIT 1
        """,
        [tracking_id],
    )
    if not rows:
        raise SystemExit(f"submission {tracking_id} not found")

    row = rows[0]
    if not int(row.get("accepted") or 0):
        raise SystemExit(
            f"{tracking_id} is not marked accepted. Reviewer must run:\n"
            f"  UPDATE bounty_submissions SET accepted=1, status='accepted',"
            f" payout_usd_cents=<cents>, payout_rail='<rail>'"
            f" WHERE tracking_id='{tracking_id}';"
        )
    if row.get("paid_at"):
        raise SystemExit(f"{tracking_id} was already paid at unix={row['paid_at']}")

    amount_cents = int(row.get("payout_usd_cents") or 0)
    if amount_cents <= 0 or amount_cents > 10_000_00:
        raise SystemExit(f"payout_usd_cents={amount_cents} out of range")
    return row


def mark_paid(tracking_id: str, rail: str, ref: str) -> None:
    now = int(time.time())
    d1_query(
        """
        UPDATE bounty_submissions
        SET status='paid', paid_at=?1, payout_rail=?2, payout_ref=?3, updated_at=?1
        WHERE tracking_id=?4
        """,
        [now, rail, ref, tracking_id],
    )


# ---------------------------------------------------------------------------
# Rail: Stripe (preferred for US reporters)
# ---------------------------------------------------------------------------


def pay_via_stripe(row: dict[str, Any], destination: str, confirm: bool) -> str:
    """Send a Stripe Connect transfer to ``destination`` (an ``acct_...`` id).

    Stripe Express accounts are the recommended onboarding flow for bounty
    recipients: they handle KYC and 1099 reporting for US contractors. The
    reviewer onboards the reporter via a Connect onboarding link out of band,
    captures the resulting account id, and passes it here.
    """
    api_key = os.environ.get("STRIPE_API_KEY")
    if not api_key:
        raise SystemExit("STRIPE_API_KEY is not set")
    if not destination.startswith("acct_"):
        raise SystemExit("--destination for stripe must be a Connect account id (acct_...)")

    amount_cents = int(row["payout_usd_cents"])
    body = urllib.parse.urlencode(
        {
            "amount": str(amount_cents),
            "currency": "usd",
            "destination": destination,
            "transfer_group": f"aal-bounty:{row['tracking_id']}",
            "description": f"AAL Bug Bounty payout for {row['tracking_id']}",
            "metadata[tracking_id]": row["tracking_id"],
            "metadata[bug_class]": row["bug_class"],
        }
    ).encode("utf-8")

    if not confirm:
        print(f"DRY-RUN stripe transfer ${amount_cents/100:,.2f} → {destination}")
        return "dry-run"

    req = urllib.request.Request(
        "https://api.stripe.com/v1/transfers",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Idempotency-Key": f"aal-bounty:{row['tracking_id']}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Stripe error {e.code}: {e.read().decode('utf-8', 'replace')}")
    return str(payload.get("id") or "")


# ---------------------------------------------------------------------------
# Rail: Wise (international bank transfer)
# ---------------------------------------------------------------------------


def _wise_request(path: str, method: str, body: dict[str, Any] | None) -> dict[str, Any]:
    token = os.environ.get("WISE_API_TOKEN")
    if not token:
        raise SystemExit("WISE_API_TOKEN is not set")
    url = f"https://api.wise.com{path}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Wise error {e.code}: {e.read().decode('utf-8', 'replace')}")


def pay_via_wise(row: dict[str, Any], recipient_id: str, confirm: bool) -> str:
    """Send a Wise transfer to ``recipient_id`` (a pre-created Wise recipient).

    The reviewer creates the Wise recipient via the Wise dashboard or API,
    captures the integer recipient id, and passes it here. Wise handles
    currency conversion and local-rails delivery; we always quote in USD.
    """
    profile_id = os.environ.get("WISE_PROFILE_ID")
    if not profile_id:
        raise SystemExit("WISE_PROFILE_ID is not set")

    amount_usd = int(row["payout_usd_cents"]) / 100.0

    if not confirm:
        print(f"DRY-RUN wise transfer ${amount_usd:,.2f} USD → recipient {recipient_id}")
        return "dry-run"

    quote = _wise_request(
        f"/v2/quotes",
        "POST",
        {
            "sourceAmount": amount_usd,
            "sourceCurrency": "USD",
            "targetCurrency": "USD",
            "profile": int(profile_id),
            "payOut": "BANK_TRANSFER",
        },
    )
    transfer = _wise_request(
        "/v1/transfers",
        "POST",
        {
            "targetAccount": int(recipient_id),
            "quoteUuid": quote["id"],
            "customerTransactionId": f"aal-bounty-{row['tracking_id']}",
            "details": {"reference": f"AAL Bounty {row['tracking_id']}"},
        },
    )
    funded = _wise_request(
        f"/v3/profiles/{profile_id}/transfers/{transfer['id']}/payments",
        "POST",
        {"type": "BALANCE"},
    )
    return str(funded.get("status") or transfer.get("id") or "")


# ---------------------------------------------------------------------------
# Rail: USDC on Base
# ---------------------------------------------------------------------------


def pay_via_usdc_base(row: dict[str, Any], address: str, confirm: bool) -> str:
    """Send USDC on Base mainnet to ``address``.

    USDC on Base is the canonical on-chain rail for international reporters
    who don't want to KYC. We use the official Circle USDC contract:

        0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913   (USDC on Base mainnet)

    This function builds and signs an ERC-20 ``transfer(address,uint256)``
    call from the configured payout wallet, submits via the configured RPC,
    and returns the resulting tx hash. We import ``web3`` lazily so the rest
    of the CLI works without crypto deps installed.
    """
    if not address.lower().startswith("0x") or len(address) != 42:
        raise SystemExit("--destination for usdc_base must be a 0x-prefixed ETH address")

    amount_usd = int(row["payout_usd_cents"]) / 100.0
    usdc_units = int(round(amount_usd * 1_000_000))  # USDC has 6 decimals
    if usdc_units <= 0:
        raise SystemExit("USDC units would be zero")

    if not confirm:
        print(f"DRY-RUN usdc-base transfer ${amount_usd:,.2f} ({usdc_units} units) → {address}")
        return "dry-run"

    rpc = os.environ.get("USDC_BASE_RPC_URL")
    pk = os.environ.get("USDC_BASE_PRIVATE_KEY")
    if not rpc or not pk:
        raise SystemExit("USDC_BASE_RPC_URL and USDC_BASE_PRIVATE_KEY must be set")

    try:
        from web3 import Web3  # type: ignore
    except ImportError:
        raise SystemExit("pip install web3 to enable USDC payouts")

    usdc_contract = Web3.to_checksum_address("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913")
    erc20_abi = [
        {
            "constant": False,
            "inputs": [
                {"name": "_to", "type": "address"},
                {"name": "_value", "type": "uint256"},
            ],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function",
        },
    ]

    w3 = Web3(Web3.HTTPProvider(rpc))
    account = w3.eth.account.from_key(pk)
    contract = w3.eth.contract(address=usdc_contract, abi=erc20_abi)

    tx = contract.functions.transfer(
        Web3.to_checksum_address(address), usdc_units
    ).build_transaction(
        {
            "from": account.address,
            "nonce": w3.eth.get_transaction_count(account.address),
            "chainId": 8453,
            "maxFeePerGas": w3.to_wei("0.01", "gwei") + w3.eth.gas_price,
            "maxPriorityFeePerGas": w3.to_wei("0.001", "gwei"),
        }
    )
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", dest="tracking_id", required=True, help="Submission tracking id.")
    ap.add_argument(
        "--rail",
        choices=("stripe", "wise", "usdc_base"),
        help="Override the rail recorded in D1. Defaults to the reporter's choice.",
    )
    ap.add_argument(
        "--destination",
        required=True,
        help=(
            "Rail-specific destination — Stripe Connect acct id, Wise recipient id, "
            "or 0x-prefixed Base address."
        ),
    )
    ap.add_argument(
        "--confirm",
        action="store_true",
        help="Actually send funds. Without this, the script dry-runs.",
    )
    args = ap.parse_args(argv)

    row = load_accepted_submission(args.tracking_id)
    rail = args.rail or row.get("payout_rail") or row.get("payment_rail")
    if rail not in ("stripe", "wise", "usdc_base"):
        raise SystemExit(f"unknown rail {rail!r}")

    if rail == "stripe":
        ref = pay_via_stripe(row, args.destination, args.confirm)
    elif rail == "wise":
        ref = pay_via_wise(row, args.destination, args.confirm)
    else:
        ref = pay_via_usdc_base(row, args.destination, args.confirm)

    print(f"[{args.tracking_id}] rail={rail} ref={ref}")
    if args.confirm and ref and ref != "dry-run":
        mark_paid(args.tracking_id, rail, ref)
        print(f"[{args.tracking_id}] marked paid in D1.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
