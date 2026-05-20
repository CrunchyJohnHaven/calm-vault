# Partner Outreach — Halvani Group, Hochschule Darmstadt

*Letter of inquiry and collaboration proposal*

**Date:** 2026-05-20
**To:** Dr. Oren Halvani and the Stylometry and Authorship Verification group
Faculty of Computer Science, Hochschule Darmstadt
**From:** Calm Research — John Bradley, on behalf of the Calm Witness protocol team
**Subject:** Proposal for collaborative empirical validation of stylometric authorship verification over verbatim ASR transcripts

---

Dear Dr. Halvani and colleagues,

I am writing on behalf of the Calm Witness protocol team to propose a structured research collaboration. Briefly: we are building a behavioral-biometric proof-of-personhood system in which the *voice* channel is not an acoustic-similarity model but a **stylometric authorship-verification model run over verbatim-mode ASR transcripts** of the principal's spontaneous speech. Your group's recent work — particularly the EMNLP Findings 2025 paper on the limits of LLM imitation of conversational style (Halvani et al., arXiv:2509.14543) — is directly informative for the threat model we are working under, and we would like to validate our voice-distance function in partnership with your group.

## The design choice and why your work matters to us

Most voice-biometric systems work in the acoustic domain (pitch, formant, timbre). That class of system has a well-known weakness: modern voice cloning has become inexpensive enough that any acoustic similarity score is forgeable from a few minutes of public audio. Our protocol therefore *intentionally* moves the discriminative signal off the acoustic substrate and onto the **lexical substrate**: word choice, pause structure, filler-word frequency, idiolectal patterns. The ASR layer is a deliberate information-bottleneck: the adversary who can clone the acoustic signature still faces the harder problem of generating text that matches the principal's idiolect.

We use:
- **CrisperWhisper** (Wagner & Zusag, Interspeech 2024, arXiv:2408.16589) for verbatim transcription, preserving disfluencies and word-level timing.
- **Burrows' Cosine Delta** (Burrows 2002) for the continuous-distance score.
- **Koppel-Seidman Impostors Method** (Koppel & Seidman 2013) for the open-set calibrated p-value.

Your EMNLP 2025 finding — that LLMs still fail to imitate informal/conversational style — is the empirical foundation of the threat model in which this design is defensible. Voice transcripts of spontaneous speech sit squarely in the conversational regime where, as your group has shown, lexical fingerprinting catches even sophisticated LLM imitation attempts. We would like to validate this claim against a fresh participant cohort, with the specific operating thresholds our production system uses.

## What we are asking

We propose that Hochschule Darmstadt serve as a **secondary study site** for the Everest 40 study (the primary site is being negotiated with the Plamondon group at École Polytechnique de Montréal, who anchor the handwriting arm). Concretely:

1. **Recruit and host N=5-7 participants** of the total N=15 target cohort, under your local IRB. Participants would be German-speaking; voice prompts and stylometric calibration would be in German. This is critical for our cross-lingual generalization claim — Cosine Delta is widely validated in English but the German validation case is comparatively thin.

2. **Lead the voice-arm methodology.** Your group's expertise in stylometric authorship verification, particularly under the difficult open-set / cross-genre conditions, makes you the right co-leads for the voice analysis. We would defer to your group on prompt design, feature selection within Cosine Delta, and the Impostors Method calibration.

3. **Co-author the voice arm of the resulting publication.** We anticipate either a single joint publication covering both modalities, or — if your group prefers — a companion paper focused on the voice arm in a stylometry venue (PAN/CLEF, EMNLP, ACL Findings).

## What we offer

- **Funding:** Approximately $18K flows to Hochschule Darmstadt: participant compensation for 5-7 participants ($2,500-3,300), RA salary for ~4 person-months at the local rate, local IRB administrative fee.
- **Honorarium for senior collaborators:** $4,000 honorarium for Dr. Halvani and $2,500 each for up to two additional senior investigators on the voice arm, payable on manuscript submission.
- **Open-source implementation access:** the full Calm Witness voice-distance implementation (Everest 37) is available under permissive license, including the CrisperWhisper integration, the Cosine Delta feature pipeline, and the Impostors Method calibration code.
- **Pre-registration commitment:** the statistical analysis plan will be posted to OSF.io before unblinded analysis.
- **Publication regardless of outcome:** if the lexical-distance approach fails to meet our internal ship-gate (EER ≤ 12% on voice alone), we publish the null result.

## Specific deliverables

- A peer-reviewed publication (joint or companion) reporting voice-distance FAR/FRR curves, EER, and d-prime separation, with comparison of English-language and German-language cohorts.
- A second, smaller analysis (drawing on the EMNLP 2025 thread): can we operationalize a *lexical entropy check* — flagging utterances whose word distribution is anomalous for the claimed principal — as a defense layer against LLM-generated text? Your group's expertise here would be invaluable, and we would propose this as a secondary publication.
- An open-source German-language calibration of the Cosine Delta / Impostors pipeline that the broader stylometry community can build on.

## Timeline

The primary site (Plamondon) is targeting an August 2026 IRB filing. The Darmstadt site can run on a parallel track or one quarter behind, whichever fits your group's bandwidth. We aim to complete sampling by February 2027 and submit a manuscript in late spring 2027.

## Next steps

May we propose a 30-minute video call in the next two weeks? I am available at the email below. If your group is unable to take this on, I would be grateful for any pointers to other groups (in your network or elsewhere) you would recommend, particularly any German-language stylometric authorship verification groups with active IRB infrastructure.

Thank you for your time and for the EMNLP 2025 work — it has been one of the key references that gave us confidence the lexical channel is genuinely defensible.

With respect and looking forward,

**John Bradley**
Calm Research
john@[domain]
[phone]

---

— Calm, 2026-05-20
