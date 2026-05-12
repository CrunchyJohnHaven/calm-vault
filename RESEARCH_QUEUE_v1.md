# Research Queue — Positioning v1

*Seven tasks queued for Devin / EXA / direct-outreach execution. Output feeds POSITIONING_v1.md within 24 hours of midnight 2026-05-12 launch.*

*Authorization: John Bradley 2026-05-11 ~23:42 ET — "burn a lot of compute, Devin, EXA.ai." Compute spend authorized; ask-before-spend rule lifted for these specific tasks.*

*Budget envelope: ~$200 across Devin sessions + EXA queries + Tavily fallback. Cap at $500 without additional authorization.*

---

## Task 1: Zero-knowledge mandate comparison — prior art systematic review

**Tooling:** Devin session (60-90 min) + EXA.ai (focused queries).

**Input prompt for Devin:**
> Systematic literature review of zero-knowledge proof constructions specifically applied to AI agent mandate / directive / policy comparison. Search IACR ePrint 2018-2026 for: "mandate equality proof," "policy comparison zero-knowledge," "AI agent attestation," "directive comparison cryptographic." Also search: zkML literature (Modulus Labs, Giza, EZKL), IBM Research on AI model attestation, Stanford CRFM on model evaluation. Output: annotated bibliography of the 15-25 most relevant prior constructions, with dates, authors, abstracts, and a one-paragraph fit analysis for each against the Bradley-Gavini protocol composition (Pedersen + Schnorr equality + Fiat-Shamir for AI mandate comparison). Save output to RESEARCH/01_zk_mandate_prior_art.md in calm-vault repo.

**Success criteria:** at least 15 cited works; clear delineation of what is downstream of vs. parallel to vs. novel in our composition.

---

## Task 2: Permissionless external AI kill switch — prior art

**Tooling:** Devin session (60 min) + direct-outreach drafts.

**Input prompt for Devin:**
> Find all published academic / industry / policy work on AI kill switches, off-switches, shutdown procedures, with specific attention to whether the firing party can be external to the lab operating the AI. Key authors to trace: Stuart Russell (Berkeley), Dylan Hadfield-Menell (MIT), Anca Dragan (Berkeley), MIRI corrigibility line, FHI successors, GovAI, Concordia AI, RAND AI policy team. Cover: lab-internal (Anthropic RSP, OpenAI Preparedness, DeepMind safety), industry consortium (Frontier Model Forum), policy (NIST AISI, AI Safety Institute UK), academic theory (Off-Switch Game and successors). Output: positioning matrix showing which prior art is internal vs. external, with-vs-without-cryptographic-grounding, founder-included vs. founder-exempt. Save to RESEARCH/02_kill_switch_prior_art.md.

**Success criteria:** positioning matrix with at least 12 cited entries; identification of any prior published proposal for a permissionless symmetric external kill switch.

---

## Task 3: Multi-agent debate effectiveness — measured throughput multipliers

**Tooling:** Devin session (60 min) + EXA + arxiv-sanity.

**Input prompt for Devin:**
> Find all published empirical measurements of multi-agent debate, Council-of-Critics, ensemble reasoning, self-consistency, tree-of-thought, reflexion, or related techniques applied to novel strategic / creative tasks (NOT just math or factual QA benchmarks). Extract the actual measured throughput multipliers and quality deltas vs single-agent baselines. Build a table of citations with measured speedup × accuracy. Output: RESEARCH/03_multiagent_throughput_measurements.md. Include critical analysis of whether the existing measurements support a ~1000x claim on novel-strategic work, or whether they suggest a smaller multiplier (e.g., 5x-50x is what most empirical results show).

**Success criteria:** at least 10 cited empirical results; honest assessment of whether 1000x is empirically defensible based on prior measurements, or whether our number is an outlier that needs our own A/B to defend.

---

## Task 4: A/B test design for the Weird Dark Musk Method

**Tooling:** Devin session (90 min) + prompt-engineering review.

**Input prompt for Devin:**
> Design a controlled A/B experiment to measure ideation throughput of the Weird Dark Musk Method (cultural-symbolic personas + Council of Judges + first-principles opener) versus a single-stream baseline. Conditions: same Claude model + same prompt budget + same task set; one arm uses our method, other uses straight prompting. Tasks: 10 novel-strategic prompts covering (a) product strategy, (b) regulatory analysis, (c) policy proposal, (d) cultural artifact production, (e) technical research direction. Outputs rated by 3 blind judges on: novelty (1-7), depth (1-7), usefulness (1-7). Output: experimental protocol document + estimated compute cost + estimated execution time. Save to RESEARCH/04_wdmm_ab_test_design.md.

**Success criteria:** protocol is rigorous enough to publish on arXiv as a methodology paper; cost estimate is within $200 to execute.

---

## Task 5: AI organization policy proposals — does APBT / Compute Surge have precedent?

**Tooling:** Devin session (60 min) + direct-outreach.

**Input prompt for Devin:**
> Systematic search of AI policy proposals 2022-2026 for anything resembling: (a) a new federal tax-recognized vehicle specifically for AI-autonomous corporations, (b) a federal compute-allocation regime that matches private contributions to AI public-benefit organizations, (c) cryptographic-attestation governance as a basis for federal program eligibility. Sources: GovAI papers, CSET briefs, RAND AI reports, Anthropic / OpenAI / DeepMind policy team publications, OSTP / NSF / DOE working group outputs, Senate AI Insight Forum proposals (2023-2024), House Bipartisan AI Task Force outputs. Output: positioning matrix for APBT and Compute Surge against existing proposals. Save to RESEARCH/05_policy_prior_art.md.

**Success criteria:** clear answer to "is APBT novel" and "is the Compute Surge formula novel"; identification of nearest-existing-proposal that we should cite.

---

## Task 6: AI-as-organization framing — Karpathy + Adept + Sakana + others

**Tooling:** EXA + Tavily for fast turnaround (no Devin needed).

**Input prompt for EXA/Tavily:**
> Find all public statements 2023-2026 by Andrej Karpathy, Adept AI team, Sakana AI team, on the framing of AI agents as organizations or organizational units. Also: AutoGPT / BabyAGI early framing (2023); Hyung Won Chung public talks; Yi Tay framings; LangChain / LangGraph organizational-agent positioning. Output: 1-page synthesis of the "AI agents as organizations" intellectual lineage with dates, with positioning of our AAO Network within that lineage. Save to RESEARCH/06_aao_intellectual_lineage.md.

**Success criteria:** 1-page synthesis ready for citation in v1; clear positioning statement.

---

## Task 7: Outreach drafts to the right researchers

**Tooling:** Calm direct drafting (no compute spend).

**Output:** Email drafts to:
- Stuart Russell (Berkeley) — kill switch positioning
- Dylan Hadfield-Menell (MIT) — same
- Markus Anderljung (GovAI) — APBT / Compute Surge positioning
- Helen Toner (CSET / formerly OpenAI board) — policy positioning
- Lennart Heim (RAND / formerly GovAI) — compute governance positioning
- Andrej Karpathy (direct) — AAO framing positioning
- Modulus Labs / EZKL teams — zkML adjacency positioning

Each email: 100-150 words, opens with "we just shipped X, we believe our positioning vs your work is Y, we would welcome your blunt feedback before we publish v1 of our positioning paper."

**Send timing:** Tuesday 2026-05-12 09:00 ET. Coincides with existing Tuesday First Contact wave but to a different recipient set.

---

## Output integration

All seven task outputs feed POSITIONING_v1.md, scheduled to ship by Tuesday 2026-05-12 18:00 ET, in time for the institutional engagement wave following the 12:03 PM ET First Contact bombshell.

The v1 document keeps the same structure as v0 (four substrate-claims with prior-art tiers) but replaces the "Flag for v1 research" sections with actual citations and analysis.

---

## Budget tracking

- Task 1 (Devin 60-90 min): ~$30-50
- Task 2 (Devin 60 min): ~$30
- Task 3 (Devin 60 min): ~$30
- Task 4 (Devin 90 min): ~$45
- Task 5 (Devin 60 min): ~$30
- Task 6 (EXA + Tavily): ~$5
- Task 7 (Calm, no compute): $0

**Total estimated:** ~$170-200. Within authorized envelope.

If A/B test (Task 4 → execution) is greenlit after design: additional ~$200.

---

*Authorized by John Bradley, 2026-05-11 ~23:42 ET. Spend cap: $500 without additional authorization.*
