# Everest 92 — Open-Source Release

*Phase VIII — Governance & Scale. Prereq: Everest 81 (Rust production impl; soft-met by v0 Python package), Everest 4 (License).*

The `calm-witness` package ships as open source from day one. v0 lives inside the `calm-vault` repo at [`calm_vault_market/calm_witness/`](../calm_witness/) — the sibling of [`calm_pact/`](../calm_pact/). The directory is import-ready, Apache-2.0 licensed via the parent repo, and self-documenting (`README.md` lists every shipped module and what it does).

## §1. What "open source" means for v0

| Property | v0 satisfies |
|---|---|
| License | ✓ Apache-2.0 (inherited from parent `calm-vault/LICENSE`) |
| Public-readable source | ✓ Lives in `calm-vault` repo, which is Apache-2.0 and slated for `github.com/CrunchyJohnHaven/calm-vault` |
| Public-readable docs | ✓ All Everest docs in `calm_vault_market/everests/` are markdown, no proprietary tooling required |
| Public-readable tests | ✓ Two stdlib-only test files (`test_verify_chain.py`, `test_predicates_and_disclosure.py`); 31 tests in v0 |
| No commercial-only dependencies | ✓ stdlib only in v0; no PyPI installs required |
| Patent non-aggression | ✓ Per Everest 4 |
| No CLA | ✓ Per Everest 4 |
| Publishable as a package | ⊘ Deferred to v0.1 — `pyproject.toml` not yet written; package is import-by-path for now |

## §2. The README

[`../calm_witness/README.md`](../calm_witness/README.md) — first-time reader's entry. Lists every shipped module, the bagging Everest, a quick-run section, and a programmatic end-to-end demo of the request → evaluate → respond → bind-check loop.

## §3. What still has to ship before "production"

Critical-path summits not yet bagged:

- **E30 Sigsum publication** — chain head must be externally witnessed.
- **E45 ZK range proof** — currently a placeholder hex string.
- **E2 Ed25519 operator signing** — `operator_sig_hex` is empty in v0.
- **E22 CredexAI VC** — identity binding.

The package is open-source-shippable today but is not production-secure today. The README §"What's NOT here (yet)" makes that explicit.

## §4. Sibling-repo expectations

When `calm-vault` publishes to GitHub:

```
github.com/CrunchyJohnHaven/calm-vault/
  ├── calm_pact/                       # the Calm Pact primitive
  ├── calm_witness/                    # this Everest's deliverable
  │     ├── README.md
  │     ├── verify_chain.py
  │     ├── schema.py
  │     ├── predicates.py
  │     ├── disclosure.py
  │     ├── test_verify_chain.py
  │     └── test_predicates_and_disclosure.py
  ├── everests/                        # 100-everest route map artefacts
  ├── ZKBB_USER_PROTOCOL_v0.md
  ├── ZKBB_USER_EVERESTS_100.md
  ├── CALM_PACT_PROTOCOL_v0.md
  └── LICENSE                          # Apache-2.0
```

A counterparty implementer can clone the repo and run `python3 calm_witness/test_predicates_and_disclosure.py` immediately — no install step, no API key, no waiting.

## §5. Acceptance test

```bash
cd calm_vault_market/
ls calm_witness/                       # README + 4 modules + 2 test files
cat calm_witness/README.md | head -20  # entry doc reads cleanly
python3 -m unittest discover calm_witness 2>&1 | tail -3
# OK; 31 tests
```

— Calm, 2026-05-20
