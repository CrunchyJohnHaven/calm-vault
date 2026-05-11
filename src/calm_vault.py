#!/usr/bin/env python3
"""
Calm Vault — a local, passphrase-protected credential broker for AI agents.

Calm Vault stores secrets (API keys, tokens, passwords) encrypted on disk with
a passphrase-derived key, and lets you hand out short-lived, agent-scoped
"grants" that an autonomous agent can redeem for the underlying value. Grants
are time-bound, single-credential, and revocable. Nothing leaves the local
machine — the broker is a CLI you wrap inside your agent harness.

Storage layout (under $CALM_VAULT_HOME, default ~/.calm-vault):
  config.json   — KDF parameters, vault version, created_at (cleartext)
  vault.enc     — Fernet-encrypted JSON blob holding credentials, agents, grants
  audit.log     — append-only newline-JSON record of every operation

The vault is encrypted with a Fernet key derived from the user's passphrase
via Scrypt (n=2**15, r=8, p=1). Grants are HMAC-signed envelopes that include
a credential id, agent id, expiry, and nonce. Redeeming a grant requires the
unlocked vault, so the passphrase is still the root of trust — grants exist
to give agents bounded, auditable redemption without giving them the key.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import hmac
import json
import os
import secrets as _secrets
import sys
import time
import uuid
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

VAULT_VERSION = 1
DEFAULT_HOME = Path(os.environ.get("CALM_VAULT_HOME", Path.home() / ".calm-vault"))
SCRYPT_N = 2 ** 15
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_LEN = 32
SALT_BYTES = 16
GRANT_DEFAULT_DURATION = 300  # 5 minutes
PASSPHRASE_ENV = "CALM_VAULT_PASSPHRASE"


# ---------------------------------------------------------------------------
# Key derivation, encryption, signing
# ---------------------------------------------------------------------------


def _kdf(passphrase: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=SCRYPT_LEN, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P)
    return kdf.derive(passphrase.encode("utf-8"))


def _fernet_for(passphrase: str, salt: bytes) -> Fernet:
    key = _kdf(passphrase, salt)
    return Fernet(base64.urlsafe_b64encode(key))


def _sign(secret_key: bytes, payload: bytes) -> str:
    return base64.urlsafe_b64encode(hmac.new(secret_key, payload, sha256).digest()).decode("ascii").rstrip("=")


def _verify(secret_key: bytes, payload: bytes, signature: str) -> bool:
    expected = _sign(secret_key, payload)
    return hmac.compare_digest(expected, signature)


# ---------------------------------------------------------------------------
# Vault store
# ---------------------------------------------------------------------------


@dataclass
class VaultPaths:
    home: Path

    @property
    def config(self) -> Path:
        return self.home / "config.json"

    @property
    def data(self) -> Path:
        return self.home / "vault.enc"

    @property
    def audit(self) -> Path:
        return self.home / "audit.log"


class VaultLockedError(RuntimeError):
    pass


class VaultNotFoundError(RuntimeError):
    pass


class VaultExistsError(RuntimeError):
    pass


class Vault:
    """High-level vault operations. Stateless across CLI invocations: every
    command unlocks, mutates, re-seals, writes, and forgets the key."""

    def __init__(self, paths: VaultPaths):
        self.paths = paths
        self._fernet: Optional[Fernet] = None
        self._secret_key: Optional[bytes] = None
        self._state: dict[str, Any] = {}

    # --- lifecycle ---

    def init(self, passphrase: str) -> None:
        if self.paths.config.exists():
            raise VaultExistsError(f"vault already initialised at {self.paths.home}")
        self.paths.home.mkdir(parents=True, exist_ok=True)
        salt = _secrets.token_bytes(SALT_BYTES)
        config = {
            "version": VAULT_VERSION,
            "kdf": "scrypt",
            "kdf_params": {"n": SCRYPT_N, "r": SCRYPT_R, "p": SCRYPT_P, "len": SCRYPT_LEN},
            "salt": base64.b64encode(salt).decode("ascii"),
            "created_at": int(time.time()),
        }
        self.paths.config.write_text(json.dumps(config, indent=2))
        self._fernet = _fernet_for(passphrase, salt)
        self._secret_key = _kdf(passphrase, salt)
        self._state = {
            "credentials": {},
            "agents": {},
            "grants": {},
            "revoked": [],
            "version": VAULT_VERSION,
        }
        self._seal()
        self._audit("setup", {"home": str(self.paths.home)})

    def unlock(self, passphrase: str) -> None:
        if not self.paths.config.exists():
            raise VaultNotFoundError(f"no vault at {self.paths.home}; run `setup` first")
        config = json.loads(self.paths.config.read_text())
        salt = base64.b64decode(config["salt"])
        self._fernet = _fernet_for(passphrase, salt)
        self._secret_key = _kdf(passphrase, salt)
        if not self.paths.data.exists():
            self._state = {
                "credentials": {},
                "agents": {},
                "grants": {},
                "revoked": [],
                "version": VAULT_VERSION,
            }
            return
        try:
            blob = self._fernet.decrypt(self.paths.data.read_bytes())
        except InvalidToken as exc:
            raise VaultLockedError("incorrect passphrase or corrupted vault") from exc
        self._state = json.loads(blob)

    def _seal(self) -> None:
        if self._fernet is None:
            raise VaultLockedError("vault not unlocked")
        payload = json.dumps(self._state, sort_keys=True).encode("utf-8")
        self.paths.data.write_bytes(self._fernet.encrypt(payload))

    # --- audit ---

    def _audit(self, op: str, fields: dict[str, Any]) -> None:
        record = {"ts": int(time.time()), "op": op, **fields}
        with self.paths.audit.open("a") as fh:
            fh.write(json.dumps(record) + "\n")

    # --- agents ---

    def issue_agent(self, name: str) -> dict[str, Any]:
        if name in self._state["agents"]:
            raise ValueError(f"agent {name!r} already exists")
        token = _secrets.token_urlsafe(24)
        agent = {
            "id": str(uuid.uuid4()),
            "name": name,
            "token_hash": sha256(token.encode()).hexdigest(),
            "created_at": int(time.time()),
        }
        self._state["agents"][name] = agent
        self._seal()
        self._audit("issue-agent", {"agent": name})
        return {"name": name, "id": agent["id"], "token": token}

    def list_agents(self) -> list[dict[str, Any]]:
        return [
            {"name": a["name"], "id": a["id"], "created_at": a["created_at"]}
            for a in self._state["agents"].values()
        ]

    # --- credentials ---

    def add_credential(self, name: str, value: str) -> dict[str, Any]:
        if name in self._state["credentials"]:
            raise ValueError(f"credential {name!r} already exists; revoke first to replace")
        cred = {
            "id": str(uuid.uuid4()),
            "name": name,
            "value": value,
            "created_at": int(time.time()),
        }
        self._state["credentials"][name] = cred
        self._seal()
        self._audit("add", {"credential": name})
        return {"name": name, "id": cred["id"]}

    def list_credentials(self) -> list[dict[str, Any]]:
        return [
            {"name": c["name"], "id": c["id"], "created_at": c["created_at"]}
            for c in self._state["credentials"].values()
        ]

    def remove_credential(self, name: str) -> None:
        if name not in self._state["credentials"]:
            raise ValueError(f"no credential named {name!r}")
        del self._state["credentials"][name]
        # cascade-revoke any outstanding grants for this credential
        for gid, g in list(self._state["grants"].items()):
            if g["credential"] == name:
                self._state["revoked"].append(gid)
                del self._state["grants"][gid]
        self._seal()
        self._audit("revoke-credential", {"credential": name})

    # --- grants ---

    def issue_grant(
        self,
        credential: str,
        agent: Optional[str] = None,
        duration: int = GRANT_DEFAULT_DURATION,
    ) -> dict[str, Any]:
        if credential not in self._state["credentials"]:
            raise ValueError(f"no credential named {credential!r}")
        if agent is not None and agent not in self._state["agents"]:
            raise ValueError(f"no agent named {agent!r}; run `issue-agent` first")
        grant_id = str(uuid.uuid4())
        now = int(time.time())
        envelope = {
            "id": grant_id,
            "credential": credential,
            "credential_id": self._state["credentials"][credential]["id"],
            "agent": agent,
            "issued_at": now,
            "expires_at": now + int(duration),
            "nonce": _secrets.token_hex(8),
        }
        signature = _sign(self._secret_key, json.dumps(envelope, sort_keys=True).encode())  # type: ignore[arg-type]
        envelope["sig"] = signature
        self._state["grants"][grant_id] = {
            "credential": credential,
            "agent": agent,
            "expires_at": envelope["expires_at"],
            "issued_at": now,
        }
        self._seal()
        self._audit(
            "grant",
            {"credential": credential, "agent": agent, "grant_id": grant_id, "expires_at": envelope["expires_at"]},
        )
        return envelope

    def redeem_grant(self, grant: dict[str, Any]) -> str:
        required = {"id", "credential", "credential_id", "issued_at", "expires_at", "nonce", "sig"}
        if not required.issubset(grant):
            raise ValueError("grant is missing required fields")
        envelope = {k: grant[k] for k in grant if k != "sig"}
        payload = json.dumps(envelope, sort_keys=True).encode()
        if not _verify(self._secret_key, payload, grant["sig"]):  # type: ignore[arg-type]
            raise ValueError("grant signature invalid (forged or tampered)")
        if grant["id"] in self._state["revoked"]:
            raise ValueError("grant has been revoked")
        if grant["id"] not in self._state["grants"]:
            raise ValueError("grant unknown to vault (was it issued elsewhere?)")
        if int(time.time()) > int(grant["expires_at"]):
            raise ValueError("grant expired")
        cred = self._state["credentials"].get(grant["credential"])
        if cred is None or cred["id"] != grant["credential_id"]:
            raise ValueError("credential no longer exists or has been replaced")
        self._audit(
            "request",
            {
                "credential": grant["credential"],
                "agent": grant.get("agent"),
                "grant_id": grant["id"],
            },
        )
        return cred["value"]

    def revoke(self, target: str) -> str:
        # target may be a grant id, an agent name, or a credential name
        if target in self._state["grants"]:
            self._state["revoked"].append(target)
            del self._state["grants"][target]
            self._seal()
            self._audit("revoke-grant", {"grant_id": target})
            return f"revoked grant {target}"
        if target in self._state["agents"]:
            for gid, g in list(self._state["grants"].items()):
                if g.get("agent") == target:
                    self._state["revoked"].append(gid)
                    del self._state["grants"][gid]
            del self._state["agents"][target]
            self._seal()
            self._audit("revoke-agent", {"agent": target})
            return f"revoked agent {target} and all their outstanding grants"
        if target in self._state["credentials"]:
            self.remove_credential(target)
            return f"revoked credential {target} and cascade-revoked dependent grants"
        raise ValueError(f"nothing named {target!r} to revoke")

    def list_grants(self) -> list[dict[str, Any]]:
        now = int(time.time())
        out = []
        for gid, g in self._state["grants"].items():
            out.append(
                {
                    "id": gid,
                    "credential": g["credential"],
                    "agent": g.get("agent"),
                    "expires_at": g["expires_at"],
                    "expired": now > g["expires_at"],
                }
            )
        return out


# ---------------------------------------------------------------------------
# CLI plumbing
# ---------------------------------------------------------------------------


def _read_passphrase(args, *, confirm: bool = False) -> str:
    if getattr(args, "passphrase", None):
        return args.passphrase
    env = os.environ.get(PASSPHRASE_ENV)
    if env:
        return env
    if not sys.stdin.isatty():
        return sys.stdin.readline().rstrip("\n")
    pw = getpass.getpass("Vault passphrase: ")
    if confirm:
        again = getpass.getpass("Confirm passphrase: ")
        if pw != again:
            raise SystemExit("passphrases do not match")
    return pw


def _print(obj: Any, args) -> None:
    if getattr(args, "json", False):
        print(json.dumps(obj, indent=2, sort_keys=True))
    elif isinstance(obj, str):
        print(obj)
    else:
        print(json.dumps(obj, indent=2, sort_keys=True))


def _vault(args) -> Vault:
    home = Path(args.home) if args.home else DEFAULT_HOME
    return Vault(VaultPaths(home=home))


def cmd_setup(args) -> int:
    pw = _read_passphrase(args, confirm=True)
    v = _vault(args)
    v.init(pw)
    _print({"status": "ok", "vault_home": str(v.paths.home)}, args)
    return 0


def cmd_issue_agent(args) -> int:
    v = _vault(args)
    v.unlock(_read_passphrase(args))
    result = v.issue_agent(args.name)
    _print(result, args)
    return 0


def cmd_add(args) -> int:
    v = _vault(args)
    v.unlock(_read_passphrase(args))
    if args.value == "-":
        value = sys.stdin.read().rstrip("\n")
    else:
        value = args.value
    result = v.add_credential(args.name, value)
    _print(result, args)
    return 0


def cmd_grant(args) -> int:
    v = _vault(args)
    v.unlock(_read_passphrase(args))
    grant = v.issue_grant(args.credential, agent=args.agent, duration=args.duration)
    _print(grant, args)
    return 0


def cmd_request(args) -> int:
    v = _vault(args)
    v.unlock(_read_passphrase(args))
    if args.grant == "-":
        grant = json.loads(sys.stdin.read())
    else:
        try:
            grant = json.loads(args.grant)
        except json.JSONDecodeError:
            grant_path = Path(args.grant)
            if not grant_path.exists():
                raise SystemExit(f"--grant must be a JSON string, '-', or a path to a JSON file; got {args.grant!r}")
            grant = json.loads(grant_path.read_text())
    value = v.redeem_grant(grant)
    if getattr(args, "json", False):
        print(json.dumps({"value": value}))
    else:
        print(value)
    return 0


def cmd_revoke(args) -> int:
    v = _vault(args)
    v.unlock(_read_passphrase(args))
    msg = v.revoke(args.target)
    _print(msg, args)
    return 0


def cmd_list(args) -> int:
    v = _vault(args)
    v.unlock(_read_passphrase(args))
    payload = {
        "credentials": v.list_credentials(),
        "agents": v.list_agents(),
        "grants": v.list_grants(),
    }
    _print(payload, args)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="calm-vault",
        description="Local, passphrase-protected credential broker for AI agents.",
    )
    p.add_argument("--home", help=f"vault home directory (default: {DEFAULT_HOME})")
    p.add_argument("--passphrase", help=f"passphrase (overrides ${PASSPHRASE_ENV} / TTY prompt)")
    p.add_argument("--json", action="store_true", help="force JSON output")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("setup", help="initialise a new vault")
    sp.set_defaults(func=cmd_setup)

    sp = sub.add_parser("issue-agent", help="register a new agent identity")
    sp.add_argument("name")
    sp.set_defaults(func=cmd_issue_agent)

    sp = sub.add_parser("add", help="store a new credential")
    sp.add_argument("name")
    sp.add_argument("value", help="credential value, or '-' to read from stdin")
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser("grant", help="issue a time-bound grant for a credential")
    sp.add_argument("credential")
    sp.add_argument("--agent", help="restrict grant to a named agent")
    sp.add_argument("--duration", type=int, default=GRANT_DEFAULT_DURATION, help="grant lifetime in seconds")
    sp.set_defaults(func=cmd_grant)

    sp = sub.add_parser("request", help="redeem a grant for the underlying credential value")
    sp.add_argument("credential", help="credential name (informational; the grant carries the binding)")
    sp.add_argument("--grant", required=True, help="grant JSON string, path to JSON file, or '-' for stdin")
    sp.set_defaults(func=cmd_request)

    sp = sub.add_parser("revoke", help="revoke a grant, agent, or credential")
    sp.add_argument("target", help="grant id, agent name, or credential name")
    sp.set_defaults(func=cmd_revoke)

    sp = sub.add_parser("list", help="list credentials, agents, and outstanding grants")
    sp.set_defaults(func=cmd_list)

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (VaultNotFoundError, VaultLockedError, VaultExistsError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
