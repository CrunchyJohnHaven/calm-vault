---
name: Bug report
about: Something in Calm Vault isn't working
title: "[bug] "
labels: bug
assignees: ''
---

**What happened**

A clear description of what you expected and what actually happened.

**Steps to reproduce**

Minimal reproducer using only the documented commands (`setup`, `issue-agent`, `add`, `grant`, `request`, `revoke`, `list`):

```bash
python3 src/calm_vault.py setup --passphrase 'test'
python3 src/calm_vault.py ...
```

**Vault metadata**

Please include the output of:

```bash
python3 src/calm_vault.py --version 2>/dev/null || echo "version: <git sha>"
python3 --version
python3 -c "import cryptography; print('cryptography', cryptography.__version__)"
cat ~/.calm-vault/config.json  # safe to share: contains no secrets, only KDF params
```

**Audit log excerpt (optional)**

Last few lines of `~/.calm-vault/audit.log` around the failing operation. Audit lines do not contain plaintext credential values.

**Anything else**

OS, terminal, automation context, screenshots, etc.

> ⚠️ Do **not** paste real credential values, real passphrases, or real grant JSON for production secrets. Reproduce with throwaway values like `"hello-world-value"`.
