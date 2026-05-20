# Submission Rubric — Everest 100 Verification Write-Ups

*Scoring rubric for incoming write-ups. Public document — verifiers may consult before submitting. Last updated 2026-05-20.*

This rubric is how Calm decides whether a submitted write-up qualifies for the bounty and, if so, which payout tier it falls into. The rubric is published deliberately: a verifier should be able to estimate, before submitting, what tier they are aiming at. Calm contributors and the DERB apply the rubric consistently across submissions.

The rubric covers two layers:

1. **Per-step scoring (V1–V7).** What passes, what doesn't, and what counts as partial credit for each of the seven verification steps.
2. **Write-up integrity.** Whether the write-up itself is published, accessible, signed, and substantive.

A submission must pass the write-up-integrity layer to be eligible for any payout. Beyond that, the payout tier is determined by the per-step scoring.

---

## Write-up integrity (gating)

A submitted write-up qualifies for review only if all of the following are true:

| Requirement | Pass | Fail |
|---|---|---|
| **Publication** | Available at a stable URL, no paywall, no embargo, no login. | Behind a paywall, embargo, login wall, or only in a Calm-internal channel. |
| **Signature** | Cryptographically signed by the verifying organization's principal, using a verifiable signature scheme (Ed25519, RSA, etc.); signature verifies against a publicly-published key. | Unsigned, signature does not verify, or signing key not publicly attributable. |
| **Self-containment** | A reader can follow the methodology from the write-up alone, without private artifacts from Calm. | The write-up requires private Calm artifacts the reader cannot obtain. |
| **Conflict-of-interest section** | Present and explicit; states "no relationships" or itemizes the relationships that exist. | Missing, vague, or evasive. |
| **Identity disclosure** | Verifying organization is named; principal is named or pseudonymous-but-key-bound. | Anonymous in a way that prevents accountability for the write-up. |
| **Verdict** | Plain-English statement of confirmation or non-confirmation. | Hedged to the point of non-statement, or absent. |
| **GitHub issues** | Any bugs identified are filed in the `calm-witness` issue tracker at the time of publication, with cross-references in the write-up. | Bugs identified are not filed, or are filed but not cross-referenced. |

If any of the above fail, Calm responds with a request for revision rather than a rejection. The verifier may revise and resubmit. A revised submission is reviewed under the same rubric.

---

## Per-step scoring (V1–V7)

### V1 — Reference implementation build

| Outcome | Criteria | Credit |
|---|---|---|
| Pass | Build succeeded from published source without Calm contributor involvement. Output binary or WASM module produced. Any clarifications needed during build are recorded. | Full |
| Pass with caveats | Build succeeded but required undocumented step(s). Caveats recorded; ideally filed as a doc issue. | Full (with attached doc-bug filing) |
| Partial | Build started but did not complete; verifier produced partial-result write-up explaining the blocker. | Partial — disqualifies from Standard tier and above; does not disqualify from Minimum if V2 and V5 still complete. |
| Fail | Build not attempted, or attempted but write-up has no V1 evidence. | None |

Note: a build that fails on the verifier's platform but succeeds when re-attempted with the verifier's diagnostic notes incorporated into the implementer's guide is the most useful kind of V1 result. It exposes a build-portability gap.

### V2 — Test corpus verification

| Outcome | Criteria | Credit |
|---|---|---|
| Pass | All published test cases run through the verifier produce the expected outputs. Raw outputs included or hash-referenced. | Full |
| Pass with divergence | Some test cases diverge; verifier documents the divergence and files an issue. Divergence may indicate a bug in the verifier (verifier's build), the test corpus, or the implementation. | Full (with attached issue filing) — *and may qualify for the substantive-bug bonus.* |
| Partial | Subset of corpus run; verifier explains why the remainder was not run. | Partial — same disqualification rule as V1. |
| Fail | Test corpus not run, or write-up has no V2 evidence. | None |

Note: a V2 divergence is one of the strongest possible outcomes. The corpus is canonical; divergence means either the corpus is wrong or one of the implementations is wrong, and both are valuable findings.

### V3 — Live proof verification

| Outcome | Criteria | Credit |
|---|---|---|
| Pass | A real Calm Witness proof — from the first-production-deployment endpoint or from a consenting principal — is verified end-to-end. Threshold signature, Σ-protocol, chain anchor, Roughtime timestamp, and operator identity binding all checked. Verdict and freshness metadata recorded. | Full |
| Pass with caveats | Proof verified, but one or more sub-checks could not be exercised due to environment (e.g., chain anchor could not be re-walked because the verifier's network setup prevented it). Caveats explicitly recorded. | Full minus a half-tier (e.g., counts toward Standard but not Full). |
| Partial | A real proof was obtained but the verifier could not complete end-to-end verification; partial result published. | Partial. |
| Fail | No real proof was attempted, or write-up has no V3 evidence. | None — disqualifies from Standard tier and above. |

### V4 — Negative-case verification

| Outcome | Criteria | Credit |
|---|---|---|
| Pass | All three named negative cases (malformed proof, replayed proof, tampered chain anchor) are constructed (by the verifier, or supplied) and the verifier correctly rejects all three. | Full |
| Pass plus | Verifier constructs and runs additional negative cases beyond the three named, all correctly rejected. | Full — and adds to the substantive-bug bonus if any case reveals an issue. |
| Partial | One or two of the three negative cases are exercised. Verifier explains the gap. | Partial. |
| Fail | None of the negative cases exercised. | None. |

If the verifier *incorrectly* accepts a negative case — i.e., the verifier accepts a malformed proof, a replay, or a tampered anchor — this is a critical finding and the submission jumps to the highest tier ($15,000). Calm responds by triaging the underlying bug as a release-blocker for the production deployment.

### V5 — Documentation accuracy

| Outcome | Criteria | Credit |
|---|---|---|
| Pass | Verifier reads the technical specification, confirms it matches implementation behavior, and records any discrepancies (spec says X, code does Y). | Full |
| Pass with discrepancies | Spec/code mismatches found and filed as doc issues. | Full (and counts toward substantive-bug bonus). |
| Partial | Spec partially read; only a subset of the protocol's surface area was checked. Verifier explains the scope. | Partial. |
| Fail | No spec-versus-implementation comparison performed. | None — disqualifies from Minimum tier. |

V5 is required at the Minimum tier because doc accuracy is what makes future verifications cheaper. A verification without V5 produces a result for the current build but leaves the spec unchecked, which provides much less long-term value.

### V6 — Adversarial probing

| Outcome | Criteria | Credit |
|---|---|---|
| Pass | At least one creative adversarial test, not already covered in Everest 41's T1–T12 enumeration, is constructed and run. Result (success, partial success, failure) recorded. | Full |
| Pass plus | The adversarial test succeeds — meaning the verifier identifies an attack the protocol does not handle. Filed as an issue; jumps to the critical-finding tier if the issue meaningfully changes the protocol or implementation. | Full + critical-finding bonus. |
| Partial | A T1–T12-equivalent test is run but no novel adversarial test attempted. | Partial. |
| Fail | No adversarial test performed. | None — disqualifies from Full tier and above. |

### V7 — Documentation update proposals

| Outcome | Criteria | Credit |
|---|---|---|
| Pass | Verifier publishes a ranked list of concrete documentation improvements based on V1–V6 experience. Submitted to the project (e.g., as a GitHub issue or PR) for Calm contributor review. | Full |
| Pass minimal | Recommendations published but not submitted to the project. | Partial — does not disqualify from Full tier but reduces substantive-bug bonus eligibility. |
| Fail | No doc-improvement recommendations published. | None — disqualifies from Full tier. |

---

## Payout tier determination

After per-step scoring, Calm determines the payout tier by the following rules.

| Tier | Required steps | Payout (USD) |
|---|---|---|
| **Minimum** | V1 (Pass) + V2 (Pass or Partial) + V5 (Pass) | $5,000 |
| **Standard** | V1 + V2 + V3 + V4 + V5 (all Pass or better; V3 may be "Pass with caveats") | $7,500 |
| **Full** | V1 + V2 + V3 + V4 + V5 + V6 + V7 (all Pass or better) | $10,000 |
| **Full + substantive bug** | Full tier *plus* at least one bug filed and triaged (spec, doc, or code). | $12,500 |
| **Full + critical finding** | Full tier *plus* a critical finding (per the V4-incorrect-accept rule, the V6-successful-attack rule, or any other finding that meaningfully changes the protocol or implementation as determined jointly by Calm contributors and the DERB). | $15,000 |

The verifier and Calm jointly determine tier eligibility based on the per-step scoring. Disagreements about tier are escalated to the DERB.

## Substantive-bug definition

A "substantive bug" for the purposes of the $12,500 tier is any of the following:

- A specification statement that does not match implementation behavior, where the mismatch is non-trivial (i.e., the discrepancy would change a reader's expectation of how the protocol works).
- An implementation bug that produces a wrong verifier verdict on a constructed input.
- A documentation gap that prevents an independent reader from completing a verification step.
- A test-corpus entry that does not match the canonical specified output.

A "critical finding" for the $15,000 tier is any of the following:

- A bug that, if left unaddressed, would invalidate one or more of the protocol's central soundness or zero-knowledge claims.
- A negative case that the verifier incorrectly accepts (V4 failure on the verifier side, indicating an implementation bug).
- An adversarial probe (V6) that succeeds against the protocol as deployed.
- Any other finding that the DERB determines meets the criticality bar.

Criticality determinations are themselves published — Calm and the DERB do not get to silently reclassify findings.

— Calm, 2026-05-20
