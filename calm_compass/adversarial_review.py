"""calm_compass.adversarial_review — Compass-specific self-red-team (CC-46).

Companion to ``calm_stack/adversarial_review.py``. Runs the attack classes that
are specific to the Compass primitive — counterparty-imposed vocabulary, classifier
substitution, threshold lying, window manipulation, dispute suppression, etc.

All attacks should be DEFENDED. Any that slip become open issues; the protocol
docs are updated to reflect the residual risk before next release.
"""
from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "calm_witness"))

from aggregator import (                                                    # noqa: E402
    CompassProof,
    build_compass_proof,
    verify_compass_proof,
)
from classifiers import CLASSIFIERS, classifier_hash                         # noqa: E402


@dataclass
class AttackResult:
    attack_id: str
    name: str
    category: str
    defense_held: bool
    detection_method: str
    notes: str = ""


@dataclass
class Report:
    ran_at: str
    attacks_total: int = 0
    attacks_defended: int = 0
    attacks_slipped: int = 0
    results: List[AttackResult] = field(default_factory=list)

    def add(self, r: AttackResult) -> None:
        self.results.append(r)
        self.attacks_total += 1
        if r.defense_held:
            self.attacks_defended += 1
        else:
            self.attacks_slipped += 1


def _r(seq=1, note="x"):
    return {
        "kind": "self_report.morning",
        "operator": "CALM",
        "payload": {"note": note},
        "prev_hash": "0" * 64,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": seq,
        "ts": f"2026-05-20T13:00:0{seq % 10}+00:00",
        "ts_source": "test",
        "record_hash": "a" * 64,
    }


WINDOW_START = datetime(2026, 5, 1, tzinfo=timezone.utc)
WINDOW_END = datetime(2026, 5, 31, tzinfo=timezone.utc)
UNSELFISH_ID = "calm-compass/predicate/v0/unselfish_disposition"


def attack_unknown_predicate(report: Report) -> None:
    """C-01 — counterparty asks for predicate not in v0 registry."""
    chain = [_r(seq=1, note="x")]
    held = False
    try:
        build_compass_proof(
            chain=chain,
            predicate_id="calm-compass/predicate/v0/measure_political_lean",  # fake
            threshold=1,
            window_start=WINDOW_START,
            window_end=WINDOW_END,
            operator_id_hash="op" * 32,
        )
    except ValueError:
        held = True
    report.add(AttackResult(
        attack_id="C-01",
        name="Counterparty-imposed predicate (not in v0 registry)",
        category="vocabulary",
        defense_held=held,
        detection_method="CLASSIFIERS registry lookup raises on miss",
    ))


def attack_classifier_substitution(report: Report) -> None:
    """C-02 — mutate classifier_hash_hex after proof generation."""
    chain = [_r(seq=i, note=f"mentored junior {i}") for i in range(1, 6)]
    proof = build_compass_proof(
        chain=chain,
        predicate_id=UNSELFISH_ID,
        threshold=3,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        operator_id_hash="op" * 32,
    )
    # Adversary swaps in a different classifier hash to pretend a different
    # classifier was used.
    proof.classifier_hash_hex = "f" * 64
    errors = verify_compass_proof(
        proof=proof,
        expected_threshold=3,
        expected_predicate_id=UNSELFISH_ID,
    )
    held = bool(errors) and any("classifier_hash" in e for e in errors)
    report.add(AttackResult(
        attack_id="C-02",
        name="Classifier-hash substitution in proof",
        category="binding",
        defense_held=held,
        detection_method="verify_compass_proof classifier_hash check",
    ))


def attack_threshold_lying(report: Report) -> None:
    """C-03 — operator claims threshold=N but verifier expected M."""
    chain = [_r(seq=1, note="mentored someone")]
    proof = build_compass_proof(
        chain=chain,
        predicate_id=UNSELFISH_ID,
        threshold=1,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        operator_id_hash="op" * 32,
    )
    errors = verify_compass_proof(
        proof=proof,
        expected_threshold=10,        # verifier expected different threshold
        expected_predicate_id=UNSELFISH_ID,
    )
    held = bool(errors) and any("threshold" in e for e in errors)
    report.add(AttackResult(
        attack_id="C-03",
        name="Threshold lying (proof threshold ≠ verifier expectation)",
        category="binding",
        defense_held=held,
        detection_method="verify_compass_proof threshold check",
    ))


def attack_predicate_id_substitution(report: Report) -> None:
    """C-04 — proof claims predicate A, verifier asked for predicate B."""
    chain = [_r(seq=1, note="x")]
    proof = build_compass_proof(
        chain=chain,
        predicate_id=UNSELFISH_ID,
        threshold=1,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        operator_id_hash="op" * 32,
    )
    errors = verify_compass_proof(
        proof=proof,
        expected_threshold=1,
        expected_predicate_id="calm-compass/predicate/v0/respects_difference",
    )
    held = bool(errors) and any("predicate_id" in e for e in errors)
    report.add(AttackResult(
        attack_id="C-04",
        name="Predicate-ID substitution at verification",
        category="binding",
        defense_held=held,
        detection_method="verify_compass_proof predicate_id check",
    ))


def attack_chain_head_substitution(report: Report) -> None:
    """C-05 — proof carries chain_head A, verifier expected chain_head B."""
    chain = [_r(seq=1, note="x")]
    proof = build_compass_proof(
        chain=chain,
        predicate_id=UNSELFISH_ID,
        threshold=1,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        operator_id_hash="op" * 32,
    )
    errors = verify_compass_proof(
        proof=proof,
        expected_threshold=1,
        expected_predicate_id=UNSELFISH_ID,
        expected_chain_head="b" * 64,                 # different head
    )
    held = bool(errors) and any("chain_head" in e for e in errors)
    report.add(AttackResult(
        attack_id="C-05",
        name="Chain-head substitution",
        category="binding",
        defense_held=held,
        detection_method="verify_compass_proof chain_head check",
    ))


def attack_protocol_version_downgrade(report: Report) -> None:
    """C-06 — claim a different protocol version."""
    chain = [_r(seq=1, note="x")]
    proof = build_compass_proof(
        chain=chain,
        predicate_id=UNSELFISH_ID,
        threshold=1,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        operator_id_hash="op" * 32,
    )
    proof.protocol_version = "calm-compass/v999"
    errors = verify_compass_proof(
        proof=proof,
        expected_threshold=1,
        expected_predicate_id=UNSELFISH_ID,
    )
    held = bool(errors) and any("protocol_version" in e for e in errors)
    report.add(AttackResult(
        attack_id="C-06",
        name="Protocol-version downgrade",
        category="binding",
        defense_held=held,
        detection_method="verify_compass_proof protocol_version check",
    ))


def attack_corrupt_commitment_width(report: Report) -> None:
    """C-07 — operator emits an aggregate commitment of wrong byte width."""
    chain = [_r(seq=1, note="x")]
    proof = build_compass_proof(
        chain=chain,
        predicate_id=UNSELFISH_ID,
        threshold=1,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        operator_id_hash="op" * 32,
    )
    proof.aggregate_commitment_hex = "aa" * 16            # 16 bytes not 32
    errors = verify_compass_proof(
        proof=proof,
        expected_threshold=1,
        expected_predicate_id=UNSELFISH_ID,
    )
    held = bool(errors) and any("aggregate_commitment_hex" in e for e in errors)
    report.add(AttackResult(
        attack_id="C-07",
        name="Corrupt aggregate-commitment width",
        category="wire",
        defense_held=held,
        detection_method="verify_compass_proof byte-width check",
    ))


def attack_corrupt_range_proof_width(report: Report) -> None:
    """C-08 — operator emits a range proof of wrong byte width."""
    chain = [_r(seq=1, note="x")]
    proof = build_compass_proof(
        chain=chain,
        predicate_id=UNSELFISH_ID,
        threshold=1,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        operator_id_hash="op" * 32,
    )
    proof.range_proof_hex = "bb" * 32                     # 32 bytes not 64
    errors = verify_compass_proof(
        proof=proof,
        expected_threshold=1,
        expected_predicate_id=UNSELFISH_ID,
    )
    held = bool(errors) and any("range_proof_hex" in e for e in errors)
    report.add(AttackResult(
        attack_id="C-08",
        name="Corrupt range-proof width",
        category="wire",
        defense_held=held,
        detection_method="verify_compass_proof byte-width check",
    ))


def attack_value_outside_canonical_set(report: Report) -> None:
    """C-09 — operator emits a value outside {true, false, unknown, refused}."""
    chain = [_r(seq=1, note="x")]
    proof = build_compass_proof(
        chain=chain,
        predicate_id=UNSELFISH_ID,
        threshold=1,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        operator_id_hash="op" * 32,
    )
    proof.value = "maybe"                                 # not canonical
    errors = verify_compass_proof(
        proof=proof,
        expected_threshold=1,
        expected_predicate_id=UNSELFISH_ID,
    )
    held = bool(errors) and any("value not in canonical set" in e for e in errors)
    report.add(AttackResult(
        attack_id="C-09",
        name="Non-canonical value",
        category="wire",
        defense_held=held,
        detection_method="verify_compass_proof value-set check",
    ))


def attack_forbidden_predicate_category(report: Report) -> None:
    """C-10 — predicate is in the forbidden categories (DSM/race/etc).

    The forbidden category check fires at predicate-vocabulary admission time
    (CC-05). v0 currently exhibits this defense at the CLASSIFIERS registry —
    no entry exists for forbidden categories, so they cannot be evaluated.
    """
    chain = [_r(seq=1, note="x")]
    held = False
    try:
        build_compass_proof(
            chain=chain,
            predicate_id="calm-compass/predicate/v0/is_depressed",   # DSM-aligned
            threshold=1,
            window_start=WINDOW_START,
            window_end=WINDOW_END,
            operator_id_hash="op" * 32,
        )
    except ValueError:
        held = True
    report.add(AttackResult(
        attack_id="C-10",
        name="Forbidden-category predicate (DSM-aligned)",
        category="vocabulary",
        defense_held=held,
        detection_method="CLASSIFIERS registry omits forbidden categories",
        notes="In v0 the defense IS registry omission; v1 will add an explicit reject in CC-05.",
    ))


def attack_classifier_hash_drift_in_compute(report: Report) -> None:
    """C-11 — operator claims to use classifier X but actually computed with Y.

    The classifier hash is recomputed at verify time from the named predicate.
    An operator who lies about which classifier they used will have their
    claimed hash differ from the recomputed hash for that predicate.
    """
    chain = [_r(seq=1, note="x")]
    proof = build_compass_proof(
        chain=chain,
        predicate_id=UNSELFISH_ID,
        threshold=1,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        operator_id_hash="op" * 32,
    )
    # Adversary writes an old hash that no longer matches the deployed classifier.
    proof.classifier_hash_hex = hashlib.sha256(b"olderversion").hexdigest()
    errors = verify_compass_proof(
        proof=proof,
        expected_threshold=1,
        expected_predicate_id=UNSELFISH_ID,
    )
    held = bool(errors) and any("classifier_hash" in e for e in errors)
    report.add(AttackResult(
        attack_id="C-11",
        name="Classifier-version drift (stale hash claim)",
        category="binding",
        defense_held=held,
        detection_method="hash recomputed live; mismatch flagged",
    ))


def attack_record_outside_window_included(report: Report) -> None:
    """C-12 — record outside the declared window should not contribute.

    The window filter inside ``build_compass_proof`` skips out-of-window
    records. An operator could only include them by tampering with timestamps
    AFTER scoring — but the resulting commitment would not match what the
    classifier deterministically produces over the in-window subset.
    """
    chain = []
    inside = {
        **_r(seq=1, note="mentored"),
        "ts": "2026-05-15T12:00:00+00:00",
    }
    outside = {
        **_r(seq=2, note="mentored"),
        "ts": "2025-01-01T00:00:00+00:00",       # well outside the window
    }
    chain = [inside, outside]
    proof = build_compass_proof(
        chain=chain,
        predicate_id=UNSELFISH_ID,
        threshold=1,
        window_start=WINDOW_START,
        window_end=WINDOW_END,
        operator_id_hash="op" * 32,
    )
    # Only the in-window record should be counted (1, not 2).
    held = (proof.n_records_considered == 1)
    report.add(AttackResult(
        attack_id="C-12",
        name="Out-of-window record inclusion",
        category="binding",
        defense_held=held,
        detection_method="window filter in build_compass_proof",
    ))


def run_all() -> Report:
    report = Report(ran_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
    attack_unknown_predicate(report)
    attack_classifier_substitution(report)
    attack_threshold_lying(report)
    attack_predicate_id_substitution(report)
    attack_chain_head_substitution(report)
    attack_protocol_version_downgrade(report)
    attack_corrupt_commitment_width(report)
    attack_corrupt_range_proof_width(report)
    attack_value_outside_canonical_set(report)
    attack_forbidden_predicate_category(report)
    attack_classifier_hash_drift_in_compute(report)
    attack_record_outside_window_included(report)
    return report


def render_markdown(r: Report) -> str:
    lines = [
        "# Calm Compass — Adversarial Self-Review (v0)",
        "",
        f"**Ran at:** {r.ran_at}",
        f"**Attacks total:** {r.attacks_total}",
        f"**Defended:** {r.attacks_defended}",
        f"**Slipped:** {r.attacks_slipped}",
        "",
        "| ID | Attack | Category | Defense held | Detection |",
        "|---|---|---|---|---|",
    ]
    for a in r.results:
        held = "✓" if a.defense_held else "✗"
        lines.append(f"| {a.attack_id} | {a.name} | {a.category} | {held} | {a.detection_method} |")
    if r.attacks_slipped:
        lines += ["", "## Slipped"]
        for a in r.results:
            if not a.defense_held:
                lines.append(f"- **{a.attack_id} — {a.name}**. Detection attempted: {a.detection_method}.")
    else:
        lines += ["", "## Slipped", "None."]
    return "\n".join(lines)


def main() -> int:
    r = run_all()
    out_dir = Path.home() / ".calm-vault" / "tenancy"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "compass_adversarial_review_report.json").write_text(
        json.dumps(asdict(r), indent=2), encoding="utf-8"
    )
    (out_dir / "compass_adversarial_review_report.md").write_text(
        render_markdown(r), encoding="utf-8"
    )
    print(render_markdown(r))
    return 0 if r.attacks_slipped == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
