"""calm_operations.stripe_verify — SUMMIT 247/300 (CO-17) Stripe Live-Mode verification.

The 2026-05-17 lesson: if Stripe is in Test mode, every "successful" checkout
returns NO MONEY. This module is a recurring probe that confirms:

  1. The API key is present.
  2. The API key is a Live-mode key (starts with ``sk_live_``, not ``sk_test_``).
  3. The named Payment Link is in Live mode and returns 200.
  4. A trailing chain record locks the verification time.

Fails LOUDLY (non-zero exit, alert printed) on any issue. Daily-check driver
calls this; CO-18 (payment-link health) layers on top.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "calm_tenancy"))
from chain_records import append_record, canonical_record_hash, _last_chain_state  # noqa: E402


DEFAULT_CHAIN = Path.home() / ".calm-vault" / "user_state.jsonl"


@dataclass
class StripeVerifyResult:
    api_key_present: bool
    api_key_live_mode: bool
    api_balance_ok: bool
    payment_link_id: Optional[str]
    payment_link_status: Optional[str]
    payment_link_live_mode: Optional[bool]
    error: Optional[str]

    @property
    def overall_ok(self) -> bool:
        return (self.api_key_present and self.api_key_live_mode and self.api_balance_ok
                and (self.payment_link_id is None
                     or (self.payment_link_status == "ok" and self.payment_link_live_mode)))


def _http_get(url: str, api_key: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def verify(api_key: Optional[str] = None,
           payment_link_id: Optional[str] = None) -> StripeVerifyResult:
    api_key = api_key or os.environ.get("STRIPE_API_KEY", "")
    if not api_key:
        return StripeVerifyResult(
            api_key_present=False, api_key_live_mode=False, api_balance_ok=False,
            payment_link_id=payment_link_id, payment_link_status=None,
            payment_link_live_mode=None, error="STRIPE_API_KEY not set",
        )
    is_live = api_key.startswith("sk_live_")
    if not is_live:
        return StripeVerifyResult(
            api_key_present=True, api_key_live_mode=False, api_balance_ok=False,
            payment_link_id=payment_link_id, payment_link_status=None,
            payment_link_live_mode=None,
            error=f"API key is NOT live-mode: prefix={api_key[:10]}…",
        )
    try:
        _http_get("https://api.stripe.com/v1/balance", api_key)
        balance_ok = True
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        return StripeVerifyResult(
            api_key_present=True, api_key_live_mode=True, api_balance_ok=False,
            payment_link_id=payment_link_id, payment_link_status=None,
            payment_link_live_mode=None, error=f"balance fetch failed: {exc}",
        )
    pl_status = None
    pl_live = None
    if payment_link_id:
        try:
            data = _http_get(
                f"https://api.stripe.com/v1/payment_links/{payment_link_id}",
                api_key,
            )
            pl_live = bool(data.get("livemode", False))
            pl_status = "ok" if data.get("active") else "inactive"
        except (urllib.error.URLError, urllib.error.HTTPError) as exc:
            pl_status = f"error: {exc}"
            pl_live = None
    return StripeVerifyResult(
        api_key_present=True, api_key_live_mode=True, api_balance_ok=balance_ok,
        payment_link_id=payment_link_id, payment_link_status=pl_status,
        payment_link_live_mode=pl_live, error=None,
    )


def chain_record(result: StripeVerifyResult,
                 chain_path: Optional[Path] = None) -> dict:
    chain_path = chain_path or DEFAULT_CHAIN
    now = datetime.now(timezone.utc)
    last_seq, prev_hash = _last_chain_state(chain_path)
    rec = {
        "kind": "stripe_live_mode_check",
        "operator": "CALM",
        "payload": {**asdict(result), "overall_ok": result.overall_ok},
        "prev_hash": prev_hash,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": last_seq + 1,
        "ts": now.isoformat().replace("+00:00", "Z"),
        "ts_source": "stripe_verify",
    }
    rec["record_hash"] = canonical_record_hash(rec)
    append_record(rec, chain_path=chain_path)
    return rec


def main() -> int:
    p = argparse.ArgumentParser(prog="calm-operations stripe-verify")
    p.add_argument("--api-key", help="Stripe API key (else uses $STRIPE_API_KEY)")
    p.add_argument("--payment-link-id", help="Payment Link to probe (optional)")
    p.add_argument("--no-chain", action="store_true",
                   help="Don't write a chain record (default: writes one)")
    args = p.parse_args()
    result = verify(api_key=args.api_key, payment_link_id=args.payment_link_id)
    if not args.no_chain:
        chain_record(result)
    print(json.dumps(asdict(result) | {"overall_ok": result.overall_ok}, indent=2))
    return 0 if result.overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
