# Legal Notes — Everest 100 Verification Bounty

*Plain-English legal posture for verifiers. Not legal advice. Last updated 2026-05-20.*

This document collects the legal and tax considerations that affect a verifier's relationship with the Calm Witness verification bounty. It is written for verifiers and their counsel, not in place of counsel. Where a verifier's home jurisdiction or organizational form changes the analysis, the verifier should obtain local advice before accepting payment.

---

## 1. Tax posture

**Bounty payments are taxable income to the recipient.** Calm Witness does not withhold taxes; the verifier (or the verifier's organization) is responsible for reporting and remitting any taxes due in their jurisdiction. The payment is not a gift, not a grant, and not a reimbursement — it is consideration for work product (the published write-up), and it is taxable as such in essentially every jurisdiction we are aware of.

**Calm issues tax documentation as required:**

- US-resident individual verifiers receiving $600 or more in a calendar year receive an **IRS Form 1099-NEC** (nonemployee compensation) from the Calm Witness operator's paying entity. The verifier provides a completed **Form W-9** (or equivalent) before payment.
- Non-US verifiers provide a completed **Form W-8BEN** (individuals) or **W-8BEN-E** (entities) before payment. Calm withholds US federal tax at the applicable treaty rate unless the W-8 establishes an exemption. The verifier is responsible for reclaiming any over-withholding through their own jurisdiction's tax treaty process.
- Organizational verifiers (universities, government agencies, commercial entities) receive payment with whatever invoice-and-receipt documentation their accounting process requires. The verifier specifies the documentation needs at submission time.

**Calm does not provide tax advice.** Verifiers who are uncertain about how to characterize the payment in their home jurisdiction should consult counsel before accepting it. The Calm Witness operator's paying entity can provide its legal name, tax identification number, and country of incorporation on request to facilitate the verifier's own analysis.

---

## 2. Payment rails

The verifier chooses one of the following:

- **USD direct deposit (ACH for US accounts, SWIFT or Wise for international).** Standard. No fee passed to the verifier beyond ordinary correspondent-bank fees for international transfers, which are typically deducted from the recipient amount; Calm grosses up to ensure the verifier receives the agreed bounty net of these fees, with a documented best-effort cap.
- **USD-denominated stablecoin (USDC or comparable, on a chain mutually acceptable to verifier and Calm).** The verifier provides a wallet address and a public attestation that the address is controlled by the verifying organization. Calm transfers within 5 business days of the payout decision becoming final.
- **Other:** If neither of the above suits the verifier — for example, a government agency that cannot accept either rail — Calm and the verifier negotiate an alternative consistent with both parties' compliance obligations.

The bounty amount is denominated in USD regardless of payment rail. Exchange-rate variation between the payout decision and the stablecoin transfer is borne by the verifier; Calm uses the rate at the time of transfer initiation. If the verifier prefers, the conversion rate can be locked at decision time at Calm's discretion, subject to Calm's treasury's ability to bear the exchange risk in the interim.

---

## 3. Sanctions, KYC, and exclusionary screening

Calm screens payees against US OFAC sanctions lists and against the analogous lists in the Calm operator's jurisdiction of incorporation. A verifier on a sanctions list cannot be paid. The verification work is still anchored into the chain as a public record; the unpaid status is disclosed.

Calm does not run a full commercial KYC process for organizational verifiers — the bounty is too small for that to be proportionate. Calm does verify the verifier's identity to the level necessary to attribute the published write-up to a real organization, and to the level necessary to satisfy the operator's banking partner's transactional-screening requirements. Individual verifiers may need to provide passport-level identity documentation in jurisdictions where the operator's bank requires it.

If a verifier's organizational form (for example, an unincorporated community collective) makes it difficult to receive payment through the available rails, Calm and the verifier work together to find a payable entity. Common solutions: payment to a fiscal sponsor; payment to a named individual member of the collective who then handles internal distribution; deferral of payment until the collective incorporates.

---

## 4. Intellectual property of the write-up

**The verifier owns the write-up.** Copyright remains with the verifying organization. Calm requests a license to (a) link to the write-up from the project site and (b) anchor the write-up's content hash into the Calm Witness chain. Neither act requires copyright transfer.

The verifier is free to publish the write-up under whatever license they prefer — including a closed copyright, an open license (CC-BY, CC0), or any other arrangement. Calm prefers but does not require an open license, on the principle that the verification is most valuable when widely reproducible.

If the verifier wants to license the write-up to Calm for inclusion in Calm Witness project documentation — for example, as a case study — that is a separate negotiation outside the bounty.

---

## 5. Liability and warranties

**Calm provides the protocol artifacts under Apache 2.0**, which disclaims warranties. The verifier accepts this when they build from source.

**The verifier does not warrant the correctness of their verification to Calm.** The verifier publishes their methodology and results; Calm reviews and decides on the bounty. Neither side warrants the other's work product.

**Calm does not indemnify the verifier** for findings the verifier publishes. The write-up is the verifier's own publication. Calm responds publicly to findings but does not assume liability for any third-party claims arising from the publication.

If a verifier is concerned about retaliatory legal action — for example, a counterparty claiming the verifier's write-up impairs their use of Calm Witness — the verifier should consult counsel before publication. Calm's process, including the DERB review of contested cases, is intended to make such retaliatory action publicly costly, but it is not a legal shield.

---

## 6. Jurisdictional considerations

A non-exhaustive list of issues a verifier outside the US may want to consider with local counsel:

- **EU verifiers:** GDPR considerations apply if the live test deployment serves any data attributable to identifiable individuals. The test deployment is engineered to not contain such data; the verifier should confirm independently. Bounty payment to an EU verifier is normal cross-border services income; VAT treatment depends on the verifier's status.
- **UK verifiers:** Post-Brexit treatment parallels the EU analysis with UK-specific tax registration thresholds.
- **Verifiers in jurisdictions with capital controls** (some Asian, African, and Latin American countries): the stablecoin rail may not be lawful for the verifier's organization; the USD wire rail may be available subject to local reporting requirements. The verifier should confirm with their banking partner before submitting.
- **Verifiers in jurisdictions where cryptographic protocol research is regulated** (a small but real category): the verifier should confirm that publishing a verification write-up does not run afoul of local export controls or research-disclosure restrictions. Calm cannot advise on this; local counsel is necessary.
- **US government verifiers** (NIST, federal lab staff acting in official capacity): the bounty may not be acceptable per federal ethics rules. The verification is still welcome without payment; the chain anchor and public credit are made regardless. The verifier's agency should determine whether the bounty itself is acceptable; if not, Calm proceeds with the verification on the same terms minus the cash transfer.

---

## 7. Disclosures and conflict of interest

The verifier's conflict-of-interest disclosure (required in the write-up) is treated as a public statement. Calm reads it, files it with the submission record, and reviews against internal records of past contributors and contractors. The disclosure is anchored into the chain along with the write-up.

If the verifier later discovers an additional conflict — for example, a researcher on the verifying team turns out to have received Calm-affiliated honoraria several years prior — the verifier discloses to Calm promptly. Calm and the DERB then determine whether the disclosure changes the verification's eligibility. The disclosure itself is anchored even if the verification's eligibility is unaffected.

---

## 8. Governing law and dispute resolution

The bounty agreement is governed by the laws of the Calm Witness operator's jurisdiction of incorporation (specified at launch). Disputes about payment, eligibility, or tier determination that cannot be resolved through the normal review process (per `05_REVIEW_PROCESS.md`) and the DERB (per Everest 80) are resolved by binding arbitration in the operator's home jurisdiction, conducted in English, with each side bearing its own costs.

Disputes about the protocol itself — for example, a verifier publishes findings and a counterparty disagrees — are not within the bounty's governing-law clause. Those are matters between the verifier and the counterparty, as is normal for any published research finding.

---

## 9. Closing note

The bounty's legal posture is intentionally light-touch. The work is research; the deliverable is a published document; the payment is consideration for the document, not for any ongoing relationship or commitment. A verifier should be able to engage, deliver, get paid, and disengage in a small number of weeks with minimal legal entanglement on either side.

If something in this packet creates friction we did not intend, we want to hear about it. The friction itself is a doc-bug for this packet; file it on the project's issue tracker and we will respond.

— Calm, 2026-05-20
