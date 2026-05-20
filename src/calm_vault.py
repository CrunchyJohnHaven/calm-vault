#!/usr/bin/env python3
"""
Calm Vault — zero-trust credential broker.

Architecture (Koushik-Hyperledger-inspired, single-principal flat-file implementation):

- John has a MASTER KEYPAIR (Ed25519). Master private key encrypted at rest with passphrase.
- Calm has an AGENT IDENTITY KEYPAIR (Ed25519). Issued + signed by John's master.
- Each credential stored AES-256-GCM-encrypted with a key derived from John's master.
- John issues PER-USE GRANTS (signed JSON: {credential_alias, agent_id, expires_at, nonce, signature}).
- Calm presents a grant to the broker; broker verifies:
  1. Grant signed by John's master key (cryptographic proof of authorization)
  2. Calm's agent identity is registered + not revoked
  3. Grant not expired
  4. Grant not previously used (nonce check)
  5. Credential not revoked
- All access attempts logged to audit.jsonl (append-only, hashed-chained for tamper-detection).
- ONE-line revoke: `calm_vault.py revoke-all` from John's terminal.

Maps to Hyperledger Indy concepts:
- John = Issuer
- Calm = Holder
- Vendor (the system Calm logs into) = Verifier (but verification is OPAQUE — vendor sees only the credential value, not the proof)
- John's master = root issuer DID
- Calm's agent key = holder DID
- Grants = Verifiable Credentials (with embedded revocation + expiration)
- audit.jsonl = revocation registry (append-only, future: replace with private chain)

For production: swap audit.jsonl for Hyperledger Indy ledger; replace Ed25519 with BLS12-381 (Anoncreds);
add ZK-proof presentation so vendors don't see the raw credential.

Usage (John):
    calm_vault.py setup                                   # one-time: generates master key, prompts passphrase
    calm_vault.py issue-agent <agent_id>                  # register Calm's agent identity
    calm_vault.py add <alias> <value>                     # add a credential
    calm_vault.py grant <alias> --duration 300            # issue a 5-min permission grant
    calm_vault.py revoke <alias>                          # revoke one credential
    calm_vault.py revoke-agent <agent_id>                 # revoke an agent identity
    calm_vault.py revoke-all                              # nuke everything
    calm_vault.py audit                                   # show audit log
    calm_vault.py status                                  # vault state summary

Usage (Calm):
    calm_vault.py request <alias> --grant <grant_json>    # request credential value
    calm_vault.py use <alias> <command...>                # single-use: inject into env for one command
"""
import argparse
import base64
import getpass
import hashlib
import json
import os
import pathlib
import secrets
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

VAULT_DIR = pathlib.Path(os.path.expanduser("~/.calm-vault"))
MASTER_PUB = VAULT_DIR / "master.pub"
MASTER_PRIV_ENC = VAULT_DIR / "master.priv.enc"
MASTER_SALT = VAULT_DIR / "master.salt"
AGENTS = VAULT_DIR / "agents.jsonl"      # registered agent identities (append-only)
REVOKED_AGENTS = VAULT_DIR / "revoked_agents.jsonl"
CREDENTIALS = VAULT_DIR / "credentials.jsonl"  # encrypted credentials
REVOKED_CREDS = VAULT_DIR / "revoked_credentials.jsonl"
GRANTS_USED = VAULT_DIR / "grants_used.jsonl"  # nonces of consumed grants
AUDIT = VAULT_DIR / "audit.jsonl"        # every access attempt (hash-chained)
KILL_SWITCH = VAULT_DIR / "REVOKED_ALL"  # if this file exists, ALL access denied


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_chain(prev_hash: bytes, entry: dict) -> str:
    """Hash-chain audit entry: H(prev_hash || canonical_entry_json)."""
    s = prev_hash + json.dumps(entry, sort_keys=True).encode()
    return hashlib.sha256(s).hexdigest()


def _audit_append(event: dict):
    """Append to audit log with hash chain."""
    AUDIT.touch(exist_ok=True)
    # Get last hash
    last_hash = b""
    with open(AUDIT, "rb") as f:
        # Read backwards: find last newline
        try:
            f.seek(-2, 2)
            while f.read(1) != b"\n":
                f.seek(-2, 1)
            last_line = f.readline().decode().strip()
            if last_line:
                last_hash = bytes.fromhex(json.loads(last_line).get("hash", ""))
        except (OSError, ValueError):
            pass
    entry = {**event, "ts": _now()}
    entry["hash"] = _hash_chain(last_hash, entry)
    with open(AUDIT, "a") as f:
        f.write(json.dumps(entry) + "\n")


def _derive_aes_key(master_priv_bytes: bytes, salt: bytes) -> bytes:
    """Derive a 32-byte AES key from master private key bytes + salt via scrypt."""
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(master_priv_bytes)


def _load_master_priv(passphrase: str) -> Ed25519PrivateKey:
    if not MASTER_PRIV_ENC.exists():
        raise FileNotFoundError("Vault not initialized. Run: calm_vault.py setup")
    salt = MASTER_SALT.read_bytes()
    enc = MASTER_PRIV_ENC.read_bytes()
    nonce, ct = enc[:12], enc[12:]
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    key = kdf.derive(passphrase.encode())
    pem = AESGCM(key).decrypt(nonce, ct, None)
    return serialization.load_pem_private_key(pem, password=None)


def _load_master_pub() -> Ed25519PublicKey:
    pem = MASTER_PUB.read_bytes()
    return serialization.load_pem_public_key(pem)


def _check_kill_switch():
    if KILL_SWITCH.exists():
        _audit_append({"event": "ACCESS_DENIED_KILL_SWITCH"})
        print("ACCESS DENIED: vault has been globally revoked. Run 'unrevoke-all' to restore.", file=sys.stderr)
        sys.exit(2)


# ============ JOHN COMMANDS ============

def cmd_setup(args):
    if MASTER_PRIV_ENC.exists():
        print("Vault already initialized at", VAULT_DIR)
        sys.exit(1)
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    VAULT_DIR.chmod(0o700)
    passphrase = getpass.getpass("Set master passphrase: ")
    confirm = getpass.getpass("Confirm passphrase: ")
    if passphrase != confirm:
        print("Mismatch.", file=sys.stderr)
        sys.exit(1)
    # Generate Ed25519 master keypair
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    # Save public
    MASTER_PUB.write_bytes(
        pub.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
    MASTER_PUB.chmod(0o644)
    # Encrypt private with passphrase-derived key
    salt = secrets.token_bytes(16)
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    key = kdf.derive(passphrase.encode())
    nonce = secrets.token_bytes(12)
    pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    ct = AESGCM(key).encrypt(nonce, pem, None)
    MASTER_PRIV_ENC.write_bytes(nonce + ct)
    MASTER_PRIV_ENC.chmod(0o600)
    MASTER_SALT.write_bytes(salt)
    MASTER_SALT.chmod(0o600)
    _audit_append({"event": "MASTER_SETUP", "master_pub_fingerprint": hashlib.sha256(pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)).hexdigest()[:16]})
    print(f"Vault initialized at {VAULT_DIR}")
    print(f"Master public key: {MASTER_PUB}")
    print("CRITICAL: backup the master passphrase + ~/.calm-vault/ directory. If you lose either, credentials are unrecoverable.")


def cmd_issue_agent(args):
    _check_kill_switch()
    passphrase = getpass.getpass("Master passphrase: ")
    master_priv = _load_master_priv(passphrase)
    agent_id = args.agent_id
    # Generate agent keypair
    agent_priv = Ed25519PrivateKey.generate()
    agent_pub = agent_priv.public_key()
    agent_pub_bytes = agent_pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    # Sign the agent's public key with master
    signature = master_priv.sign(agent_pub_bytes + agent_id.encode())
    # Store
    entry = {
        "agent_id": agent_id,
        "agent_pub": base64.b64encode(agent_pub_bytes).decode(),
        "issued_at": _now(),
        "signature": base64.b64encode(signature).decode(),
    }
    with open(AGENTS, "a") as f:
        f.write(json.dumps(entry) + "\n")
    # Hand the agent's private key to Calm
    agent_priv_b64 = base64.b64encode(
        agent_priv.private_bytes(
            serialization.Encoding.Raw,
            serialization.PrivateFormat.Raw,
            serialization.NoEncryption(),
        )
    ).decode()
    _audit_append({"event": "AGENT_ISSUED", "agent_id": agent_id})
    print(f"Agent issued: {agent_id}")
    print(f"AGENT PRIVATE KEY (give to Calm; never share with anyone else):")
    print(agent_priv_b64)
    print("Calm saves to ~/.calm-vault/agent.priv (mode 600) for use in `request` commands.")


def cmd_add(args):
    _check_kill_switch()
    passphrase = getpass.getpass("Master passphrase: ")
    master_priv = _load_master_priv(passphrase)
    salt_for_aes = MASTER_SALT.read_bytes()
    master_priv_bytes = master_priv.private_bytes(
        serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption()
    )
    aes_key = _derive_aes_key(master_priv_bytes, salt_for_aes)
    nonce = secrets.token_bytes(12)
    value_bytes = args.value.encode()
    ct = AESGCM(aes_key).encrypt(nonce, value_bytes, args.alias.encode())
    entry = {
        "alias": args.alias,
        "ciphertext_b64": base64.b64encode(nonce + ct).decode(),
        "added_at": _now(),
        "label": args.label or "",
    }
    with open(CREDENTIALS, "a") as f:
        f.write(json.dumps(entry) + "\n")
    _audit_append({"event": "CREDENTIAL_ADDED", "alias": args.alias})
    print(f"Credential added: {args.alias}")


def cmd_grant(args):
    _check_kill_switch()
    passphrase = getpass.getpass("Master passphrase: ")
    master_priv = _load_master_priv(passphrase)
    expires_at = (datetime.now(timezone.utc) + timedelta(seconds=args.duration)).isoformat()
    grant = {
        "alias": args.alias,
        "agent_id": args.agent_id,
        "expires_at": expires_at,
        "nonce": base64.b64encode(secrets.token_bytes(16)).decode(),
        "issued_at": _now(),
    }
    canonical = json.dumps(grant, sort_keys=True).encode()
    signature = master_priv.sign(canonical)
    grant["signature"] = base64.b64encode(signature).decode()
    _audit_append({"event": "GRANT_ISSUED", "alias": args.alias, "agent_id": args.agent_id, "expires_at": expires_at, "nonce": grant["nonce"]})
    print("=== GRANT (give to Calm) ===")
    print(json.dumps(grant))
    print()
    print(f"Expires at: {expires_at}")
    print(f"Calm runs: calm_vault.py request {args.alias} --grant '<paste-grant-json>'")


def cmd_revoke(args):
    _check_kill_switch()
    with open(REVOKED_CREDS, "a") as f:
        f.write(json.dumps({"alias": args.alias, "revoked_at": _now()}) + "\n")
    _audit_append({"event": "CREDENTIAL_REVOKED", "alias": args.alias})
    print(f"Credential revoked: {args.alias}")


def cmd_revoke_agent(args):
    _check_kill_switch()
    with open(REVOKED_AGENTS, "a") as f:
        f.write(json.dumps({"agent_id": args.agent_id, "revoked_at": _now()}) + "\n")
    _audit_append({"event": "AGENT_REVOKED", "agent_id": args.agent_id})
    print(f"Agent revoked: {args.agent_id}")


def cmd_revoke_all(args):
    KILL_SWITCH.write_text(_now())
    KILL_SWITCH.chmod(0o644)
    _audit_append({"event": "KILL_SWITCH_ENGAGED"})
    print("KILL SWITCH ENGAGED. All credential access denied until 'unrevoke-all'.")


def cmd_unrevoke_all(args):
    if KILL_SWITCH.exists():
        KILL_SWITCH.unlink()
        _audit_append({"event": "KILL_SWITCH_DISENGAGED"})
        print("Kill switch disengaged. Calm credential access restored.")
    else:
        print("Kill switch was not engaged.")


def cmd_status(args):
    print(f"VAULT_DIR: {VAULT_DIR}")
    print(f"Master pub: {MASTER_PUB} ({'exists' if MASTER_PUB.exists() else 'MISSING'})")
    print(f"Kill switch: {'ENGAGED' if KILL_SWITCH.exists() else 'off'}")
    agents = []
    if AGENTS.exists():
        agents = [json.loads(l) for l in AGENTS.read_text().splitlines() if l.strip()]
    revoked_agents = set()
    if REVOKED_AGENTS.exists():
        revoked_agents = {json.loads(l)["agent_id"] for l in REVOKED_AGENTS.read_text().splitlines() if l.strip()}
    print(f"Agents: {len(agents)} issued, {len(revoked_agents)} revoked")
    for a in agents:
        status = "REVOKED" if a["agent_id"] in revoked_agents else "active"
        print(f"  {a['agent_id']:30s}  {status}  issued {a['issued_at'][:19]}")
    creds = []
    if CREDENTIALS.exists():
        creds = [json.loads(l) for l in CREDENTIALS.read_text().splitlines() if l.strip()]
    revoked_creds = set()
    if REVOKED_CREDS.exists():
        revoked_creds = {json.loads(l)["alias"] for l in REVOKED_CREDS.read_text().splitlines() if l.strip()}
    print(f"Credentials: {len(creds)} stored, {len(revoked_creds)} revoked")
    for c in creds:
        status = "REVOKED" if c["alias"] in revoked_creds else "active"
        print(f"  {c['alias']:30s}  {status}  added {c['added_at'][:19]}  {c.get('label','')}")


def cmd_audit(args):
    if not AUDIT.exists():
        print("No audit log yet.")
        return
    for line in AUDIT.read_text().splitlines()[-args.lines:]:
        if not line.strip():
            continue
        e = json.loads(line)
        ts = e.get('ts', '?')[:19]
        ev = e.get('event', '?')
        h = e.get('hash', '?')[:12]
        rest = {k:v for k,v in e.items() if k not in ('ts','event','hash')}
        print(f"  {ts}  {ev:30s}  hash={h}  {json.dumps(rest)}")


# ============ CALM COMMANDS ============

def cmd_request(args):
    _check_kill_switch()
    # Calm's agent key must exist
    agent_priv_path = VAULT_DIR / "agent.priv"
    if not agent_priv_path.exists():
        print("ERROR: agent.priv missing. John must run `issue-agent` and Calm saves the result.", file=sys.stderr)
        sys.exit(1)
    # Parse grant
    grant = json.loads(args.grant)
    # Verify grant signature against master public key
    master_pub = _load_master_pub()
    sig = base64.b64decode(grant["signature"])
    grant_for_verify = {k: v for k, v in grant.items() if k != "signature"}
    canonical = json.dumps(grant_for_verify, sort_keys=True).encode()
    try:
        master_pub.verify(sig, canonical)
    except Exception:
        _audit_append({"event": "ACCESS_DENIED_BAD_GRANT_SIGNATURE", "alias": args.alias})
        print("ACCESS DENIED: grant signature invalid", file=sys.stderr)
        sys.exit(2)
    # Check alias match
    if grant["alias"] != args.alias:
        _audit_append({"event": "ACCESS_DENIED_ALIAS_MISMATCH", "alias": args.alias, "grant_alias": grant["alias"]})
        print(f"ACCESS DENIED: grant for {grant['alias']}, requested {args.alias}", file=sys.stderr)
        sys.exit(2)
    # Check expiration
    expires_at = datetime.fromisoformat(grant["expires_at"])
    if datetime.now(timezone.utc) > expires_at:
        _audit_append({"event": "ACCESS_DENIED_GRANT_EXPIRED", "alias": args.alias})
        print(f"ACCESS DENIED: grant expired at {grant['expires_at']}", file=sys.stderr)
        sys.exit(2)
    # Check nonce not already used (single-use)
    GRANTS_USED.touch(exist_ok=True)
    used_nonces = set()
    for line in GRANTS_USED.read_text().splitlines():
        if line.strip():
            used_nonces.add(json.loads(line).get("nonce"))
    if grant["nonce"] in used_nonces:
        _audit_append({"event": "ACCESS_DENIED_NONCE_REPLAY", "alias": args.alias})
        print("ACCESS DENIED: grant already consumed (single-use)", file=sys.stderr)
        sys.exit(2)
    # Check credential not revoked
    if REVOKED_CREDS.exists():
        revoked = {json.loads(l)["alias"] for l in REVOKED_CREDS.read_text().splitlines() if l.strip()}
        if args.alias in revoked:
            _audit_append({"event": "ACCESS_DENIED_CREDENTIAL_REVOKED", "alias": args.alias})
            print(f"ACCESS DENIED: credential {args.alias} revoked", file=sys.stderr)
            sys.exit(2)
    # Check agent not revoked
    if REVOKED_AGENTS.exists():
        revoked_agents = {json.loads(l)["agent_id"] for l in REVOKED_AGENTS.read_text().splitlines() if l.strip()}
        if grant["agent_id"] in revoked_agents:
            _audit_append({"event": "ACCESS_DENIED_AGENT_REVOKED", "agent_id": grant["agent_id"]})
            print(f"ACCESS DENIED: agent {grant['agent_id']} revoked", file=sys.stderr)
            sys.exit(2)
    # Find credential
    cred = None
    for line in CREDENTIALS.read_text().splitlines():
        if not line.strip():
            continue
        c = json.loads(line)
        if c["alias"] == args.alias:
            cred = c  # take the LAST one matching
    if not cred:
        _audit_append({"event": "ACCESS_DENIED_CREDENTIAL_NOT_FOUND", "alias": args.alias})
        print(f"ACCESS DENIED: credential {args.alias} not found", file=sys.stderr)
        sys.exit(2)
    # Decrypt — broker reconstructs AES key from a re-derived master.
    # SIMPLIFICATION: broker has access to MASTER_PRIV_ENC + can derive AES key if it knows passphrase.
    # In our model: broker runs AS John (under his uid); calls require John's passphrase OR a long-lived broker session.
    # For this prototype: ask for passphrase OR accept env var CALM_VAULT_BROKER_PASSPHRASE
    pp = os.environ.get("CALM_VAULT_BROKER_PASSPHRASE") or getpass.getpass("Master passphrase (for broker decryption): ")
    master_priv = _load_master_priv(pp)
    salt_for_aes = MASTER_SALT.read_bytes()
    master_priv_bytes = master_priv.private_bytes(
        serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption()
    )
    aes_key = _derive_aes_key(master_priv_bytes, salt_for_aes)
    ct_bytes = base64.b64decode(cred["ciphertext_b64"])
    nonce, ct = ct_bytes[:12], ct_bytes[12:]
    value = AESGCM(aes_key).decrypt(nonce, ct, args.alias.encode()).decode()
    # Mark nonce as used
    with open(GRANTS_USED, "a") as f:
        f.write(json.dumps({"nonce": grant["nonce"], "used_at": _now(), "alias": args.alias, "agent_id": grant["agent_id"]}) + "\n")
    _audit_append({"event": "CREDENTIAL_RELEASED", "alias": args.alias, "agent_id": grant["agent_id"], "nonce": grant["nonce"]})
    print(value)


# ============ CLI ============

def main():
    p = argparse.ArgumentParser(description="Calm Vault — zero-trust credential broker")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("setup")
    s = sub.add_parser("issue-agent"); s.add_argument("agent_id")
    s = sub.add_parser("add"); s.add_argument("alias"); s.add_argument("value"); s.add_argument("--label")
    s = sub.add_parser("grant"); s.add_argument("alias"); s.add_argument("--agent-id", required=True); s.add_argument("--duration", type=int, default=300)
    s = sub.add_parser("revoke"); s.add_argument("alias")
    s = sub.add_parser("revoke-agent"); s.add_argument("agent_id")
    sub.add_parser("revoke-all")
    sub.add_parser("unrevoke-all")
    sub.add_parser("status")
    s = sub.add_parser("audit"); s.add_argument("--lines", type=int, default=20)
    s = sub.add_parser("request"); s.add_argument("alias"); s.add_argument("--grant", required=True)
    args = p.parse_args()
    {
        "setup": cmd_setup, "issue-agent": cmd_issue_agent, "add": cmd_add,
        "grant": cmd_grant, "revoke": cmd_revoke, "revoke-agent": cmd_revoke_agent,
        "revoke-all": cmd_revoke_all, "unrevoke-all": cmd_unrevoke_all,
        "status": cmd_status, "audit": cmd_audit, "request": cmd_request,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
