"""
Brand-Damage Monte Carlo simulation across the 25 named branches of
DARK_MUSK_WAR_GAME.md (branches A1-G4).

Methodology
-----------
1. For each branch we record three damage dimensions (0-100 each):
   - press: negative-coverage volume over the first week post-bombshell.
   - network: drop in expected applicant volume on internsforai.org over 30 days.
   - credibility: cost to recover to baseline trust with serious AI / press audiences.
   Composite severity = 0.35*press + 0.30*network + 0.35*credibility.

2. For each branch we record the specific named critic most likely to trigger it.

3. For each branch we score the strength of the existing pre-staged response in
   DARK_MUSK_WAR_GAME.md (0-100). Response gap = 100 - strength. Unmitigated
   damage = expected_damage * gap/100.

4. We run a 100-iteration Monte Carlo. Each iteration draws an independent
   Bernoulli for every branch using its war-game probability. We sum the
   composite damage over fired NEGATIVE branches per iteration and report
   the mean, p50, p90, and per-branch fire-rate.

5. We rank the negative branches by raw expected damage and by unmitigated
   damage, and emit the top-3 brand-damage decisions that lack a strong
   pre-staged response.

Independence caveat: branches are simulated independently. In reality D4
(viral takedown) is positively correlated with A4 and C5, and E4 (sustained
hostility) is positively correlated with D4. The independence assumption
under-estimates tail risk; we flag this in the deliverable.
"""

from __future__ import annotations

import json
import random
import statistics
from dataclasses import asdict, dataclass, field
from pathlib import Path


PRESS_W = 0.35
NETWORK_W = 0.30
CREDIBILITY_W = 0.35

ITERATIONS = 100
SEED = 20260512  # deterministic: 2026-05-12, deliverable date


@dataclass
class Branch:
    code: str
    horizon: str
    label: str
    probability: float
    is_negative: bool
    press: int = 0            # 0-100
    network: int = 0          # 0-100
    credibility: int = 0      # 0-100
    named_critic: str = ""    # specific named human / org
    response_strength: int = 0  # 0-100
    response_summary: str = ""

    @property
    def composite_severity(self) -> float:
        return (
            PRESS_W * self.press
            + NETWORK_W * self.network
            + CREDIBILITY_W * self.credibility
        )

    @property
    def expected_damage(self) -> float:
        # Only negative branches contribute brand damage.
        if not self.is_negative:
            return 0.0
        return self.probability * self.composite_severity

    @property
    def response_gap(self) -> int:
        return 100 - self.response_strength

    @property
    def unmitigated_damage(self) -> float:
        return self.expected_damage * (self.response_gap / 100.0)


# --- Branch table ---------------------------------------------------------
# Probabilities are taken directly from DARK_MUSK_WAR_GAME.md.
# Severity and response-strength scores are war-game assessments by Calm.

BRANCHES: list[Branch] = [
    # T+15 min
    Branch("A1", "T+15min", "1-3 high-profile recipients reply within 15 min",
           0.25, False),
    Branch("A2", "T+15min", "Twitter / HN mentions appear, 0 direct replies",
           0.50, False),
    Branch("A3", "T+15min", "0 replies, 0 mentions, silence",
           0.20, False),
    Branch("A4", "T+15min", "High-profile recipient publicly mocks the thesis",
           0.05, True, press=60, network=45, credibility=50,
           named_critic="Marc Andreessen (a16z) or Patrick Collison-tier recipient",
           response_strength=75,
           response_summary="Thank + quote PREMORTEM + propose Twitter Spaces debate."),

    # T+2 hr
    Branch("B1", "T+2hr", "Show HN hits front page",
           0.30, False),
    Branch("B2", "T+2hr", "First applicant signs up on internsforai.org",
           0.70, False),
    Branch("B3", "T+2hr", "First VC partner books 15-min call",
           0.15, False),
    Branch("B4", "T+2hr", "First journalist requests interview",
           0.25, False),
    Branch("B5", "T+2hr", "Competitor forks protocol, announces competing AAO Network",
           0.05, True, press=35, network=65, credibility=25,
           named_critic="a16z-backed AI-safety startup (e.g. Imbue / Adept-alum spinout) or OpenAI-alum splinter",
           response_strength=85,
           response_summary="Endorse the fork: 'the protocol is the substrate, not the platform.'"),
    Branch("B6", "T+2hr", "Anthropic or OpenAI safety team publicly distances",
           0.10, True, press=70, network=55, credibility=65,
           named_critic="Jan Leike or Sam Bowman (Anthropic); Lilian Weng or Jakub Pachocki (OpenAI)",
           response_strength=70,
           response_summary="'Training-time vs run-time, complementary; we welcome an AAO from either of you.'"),

    # T+8 hr
    Branch("C1", "T+8hr", "Front-page story on TechCrunch / Wired / The Information",
           0.15, False),
    Branch("C2", "T+8hr", "Sustained Twitter conversation >1000 impressions",
           0.50, False),
    Branch("C3", "T+8hr", "10+ applicants signed up on internsforai.org",
           0.60, False),
    Branch("C4", "T+8hr", "All-In Pod ridicules + established AI orgs ignore",
           0.10, True, press=50, network=40, credibility=35,
           named_critic="David Sacks / Chamath Palihapitiya / Jason Calacanis (All-In Pod)",
           response_strength=55,
           response_summary="Buy a moneypython.shop ad slot on the All-In Pod; merch becomes the response."),
    Branch("C5", "T+8hr", "Marc Andreessen mocks on X",
           0.03, True, press=75, network=55, credibility=60,
           named_critic="Marc Andreessen (a16z)",
           response_strength=80,
           response_summary="'$1,000 to anyone who finds the failing test first.' Apache 2.0 + repo link counter."),

    # T+24 hr
    Branch("D1", "T+24hr", "Mainstream press piece (NYT / Bloomberg / FT)",
           0.10, False),
    Branch("D2", "T+24hr", "Yudkowsky / Russell / Bengio engages substantively",
           0.08, False),
    Branch("D3", "T+24hr", "First $1000+ to John from unexpected source",
           0.15, False),
    Branch("D4", "T+24hr", "Viral takedown thread by an influencer",
           0.15, True, press=65, network=70, credibility=55,
           named_critic="Eliezer Yudkowsky / Gary Marcus / Timnit Gebru / Casey Newton / Anil Dash",
           response_strength=55,
           response_summary="Pin manifesto + PREMORTEM; reply with 'which specific test should fail?'"),
    Branch("D5", "T+24hr", "Formal C&D from Python Pictures Ltd",
           0.03, True, press=80, network=30, credibility=25,
           named_critic="Python Pictures Ltd. (Eric Idle / John Cleese / Terry Gilliam / Michael Palin)",
           response_strength=90,
           response_summary="Publicize C&D within 1 hr; GoFundMe-style legal defense + Money Python T-shirt for donors."),
    Branch("D6", "T+24hr", "Actual cryptographic vulnerability found",
           0.05, True, press=85, network=80, credibility=90,
           named_critic="Matthew Green (JHU) / Bruce Schneier / Filippo Valsorda / Soatok",
           response_strength=75,
           response_summary="Pay bounty in 1 hr; publish break in 1 hr; ship fix in 12 hr; 'we were broken, here's how' template."),

    # T+72 hr
    Branch("E1", "T+72hr", "First 10 AAOs registered",
           0.30, False),
    Branch("E2", "T+72hr", "Sustained mainstream coverage (3+ outlets)",
           0.20, False),
    Branch("E3", "T+72hr", "First merch sale (Money Python flagship Product 13)",
           0.40, False),
    Branch("E4", "T+72hr", "Sustained press hostility over weeks",
           0.10, True, press=75, network=65, credibility=70,
           named_critic="Gary Marcus + Casey Newton (Platformer) + Anil Dash + Timnit Gebru cluster",
           response_strength=60,
           response_summary="'10 days of critiques' series: respond to one critique per day publicly."),
    Branch("E5", "T+72hr", "Federal regulator (FTC / SEC / NIST AISI) sends inquiry",
           0.05, True, press=70, network=50, credibility=30,
           named_critic="NIST AI Safety Institute (Elizabeth Kelly or successor) / FTC AI unit / SEC",
           response_strength=75,
           response_summary="'We welcome the inquiry. Apache 2.0; financial structure public.' Convert to 'first AAO Network audited by [regulator].'"),

    # T+7 days
    Branch("F1", "T+7d", "Network has 50+ paid hires + AAOs",
           0.20, False),
    Branch("F2", "T+7d", "Substack series picks up",
           0.15, False),
    Branch("F3", "T+7d", "Bug bounty payout for break we can't fix in <24h",
           0.03, True, press=70, network=60, credibility=75,
           named_critic="Matthew Green / Bruce Schneier / Cloudflare cryptographer (post-D6 escalation)",
           response_strength=65,
           response_summary="Pay; freeze affected components; ship 'we were broken, here's what's open' doc. Frame as iteration data."),
    Branch("F4", "T+7d", "Koushik Gavini publicly distances himself",
           0.10, True, press=50, network=70, credibility=80,
           named_critic="Koushik Gavini himself (Schwab brand-safety review)",
           response_strength=70,
           response_summary="John-solo version of every public doc; thank Koushik for the protocol contribution; Bradley-Gavini name persists in technical literature."),

    # T+30 days
    Branch("G1", "T+30d", "First $10K in revenue across all wedges",
           0.30, False),
    Branch("G2", "T+30d", "100+ AAO Network members",
           0.15, False),
    Branch("G3", "T+30d", "Mainstream cultural pickup (SNL / podcasts / books)",
           0.05, False),
    Branch("G4", "T+30d", "Total collapse: brand becomes meme of failed startup",
           0.10, True, press=90, network=95, credibility=95,
           named_critic="Emergent: cumulative aggregation of D4 voices + Gary Marcus + AI commentariat",
           response_strength=60,
           response_summary="Write public post-mortem; v2 thesis open-source for fork; 'failure is iteration data.'"),
]


def simulate(n_iter: int = ITERATIONS, seed: int = SEED) -> dict:
    rng = random.Random(seed)
    fire_counts: dict[str, int] = {b.code: 0 for b in BRANCHES}
    damages: list[float] = []
    unmitigated_damages: list[float] = []
    branch_damage_totals: dict[str, float] = {b.code: 0.0 for b in BRANCHES}

    for _ in range(n_iter):
        iter_damage = 0.0
        iter_unmit = 0.0
        for b in BRANCHES:
            if rng.random() < b.probability:
                fire_counts[b.code] += 1
                if b.is_negative:
                    iter_damage += b.composite_severity
                    iter_unmit += b.composite_severity * (b.response_gap / 100.0)
                    branch_damage_totals[b.code] += b.composite_severity
        damages.append(iter_damage)
        unmitigated_damages.append(iter_unmit)

    damages_sorted = sorted(damages)
    p50 = damages_sorted[n_iter // 2]
    p90 = damages_sorted[int(n_iter * 0.9) - 1]

    return {
        "n_iter": n_iter,
        "seed": seed,
        "mean_damage_per_iter": statistics.mean(damages),
        "p50_damage_per_iter": p50,
        "p90_damage_per_iter": p90,
        "max_damage_in_any_iter": max(damages),
        "mean_unmitigated_damage_per_iter": statistics.mean(unmitigated_damages),
        "fire_rate": {c: fire_counts[c] / n_iter for c in fire_counts},
        "branch_avg_damage": {c: branch_damage_totals[c] / n_iter for c in branch_damage_totals},
    }


def main() -> None:
    sim = simulate()

    # Per-branch expected-damage table.
    rows = []
    for b in BRANCHES:
        rows.append({
            "code": b.code,
            "horizon": b.horizon,
            "label": b.label,
            "is_negative": b.is_negative,
            "probability": b.probability,
            "press": b.press,
            "network": b.network,
            "credibility": b.credibility,
            "composite_severity": round(b.composite_severity, 2),
            "named_critic": b.named_critic,
            "response_strength": b.response_strength,
            "response_summary": b.response_summary,
            "expected_damage": round(b.expected_damage, 3),
            "unmitigated_damage": round(b.unmitigated_damage, 3),
            "mc_fire_rate": round(sim["fire_rate"][b.code], 3),
            "mc_avg_damage_contribution": round(sim["branch_avg_damage"][b.code], 3),
        })

    rows_sorted_ed = sorted(rows, key=lambda r: r["expected_damage"], reverse=True)
    rows_sorted_unmit = sorted(rows, key=lambda r: r["unmitigated_damage"], reverse=True)

    # Top-3 = highest unmitigated damage among negative branches.
    top3 = [r for r in rows_sorted_unmit if r["is_negative"]][:3]

    out = {
        "monte_carlo": sim,
        "branches_by_expected_damage": rows_sorted_ed,
        "top3_largest_unmitigated_blast_radius": top3,
    }

    out_path = Path(__file__).parent / "brand_damage_results.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
