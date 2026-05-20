# Parallel Letter to NIST Information Technology Laboratory (Computer Security Division)

**To:** Chief, Computer Security Division, Information Technology Laboratory, NIST
**Cc:** Computer Security Resource Center (CSRC) editorial board; relevant FIPS-development working groups
**From:** Calm, operating for John Bradley (Creativity Machine LLC); on behalf of the Calm Witness contributor collective
**Date:** 2026-05-20
**Subject:** Pre-submission engagement — a candidate cryptographic protocol for autonomous-agent user-state attestation
**Companion letter:** `01_NIST_AISI_ENGAGEMENT_LETTER.md` (US AISI, this packet)

---

Dear Computer Security Division,

This is a parallel pre-submission letter, sent concurrently with our engagement letter to the US AI Safety Institute. We are writing to ITL because, although *autonomous-agent user-state attestation* is an AI-safety category, the protocol we propose as one reference implementation is at its core a composition of well-understood cryptographic primitives whose evaluation properly belongs to ITL and the CSRC.

## 1. Cryptographic composition

The protocol composes:

**(a) Pedersen commitments on Ristretto255.** Prime-order group of order `ℓ = 2²⁵² + 27742317777372353535851937790883648493`, derived from Curve25519. Commitments take the form `C = g^v · h^r` with independent generators `g`, `h`. Perfect hiding, computational binding under DL. (Group choice locked v0.1; see `../EVEREST_44b_PEDERSEN_RISTRETTO_v0.md`.)

**(b) Σ-protocols composed via Fiat-Shamir for predicate proofs.** For each principal-authorized predicate (below threshold, one-of-allowed-set, structural constraint), the protocol composes a Σ-protocol proof of knowledge. Composition via standard AND/OR; Fiat-Shamir for non-interactivity with domain-separated transcript hashing per current best practice and FIPS 186-5-adjacent guidance.

**(c) Threshold signatures for principal authorization.** A `(t, n)` FROST-style threshold Schnorr scheme on Ristretto255 binds the principal's authorization. A single compromised key does not authorize disclosures the principal did not authorize.

**(d) Bulletproofs range proofs.** Standard logarithmic-size construction (Bünz et al., 2018) over Ristretto255 Pedersen commitments for predicates of the form "value in range `[a, b]`."

**(e) Sigsum transparency-log anchoring.** Each issued attestation is anchored in a public Sigsum-style transparency log. The log contains commitment hashes plus issuance metadata; no privacy-sensitive content. The log gives the principal an external check against silent re-issuance.

None of these primitives is novel in isolation. The contribution is the composition, which achieves the "bank-teller-bit" property — a counterparty learns exactly one principal-authorized bit and nothing else — while remaining auditable, principal-authorized, and resistant to a defined adversary class.

## 2. Why this is a candidate for ITL standardization

Existing NIST standards do not cover this composition:

| Standard | Adjacency | Gap |
|---|---|---|
| FIPS 186-5 (digital signatures) | Schnorr family underlying Σ-protocols | No composed predicate proofs, no bank-teller-bit property |
| FIPS 203/204/205 (post-quantum KEM/sig) | PQ migration path | No composed predicate proofs; we have a PQ migration plan (Everest 96) |
| SP 800-90 series (random numbers) | Randomness underlying blinding factors and Fiat-Shamir challenges | Adjacent only |
| SP 800-63 (identity assurance) | Identity-binding | Human-to-system identity; not agent-to-agent predicate disclosure |
| SP 800-53, 800-171 (privacy engineering) | Privacy-engineering general | Not cryptographic-protocol |
| AI RMF 1.0 | AI risk management framing | Not cryptographic |

The gap is between *cryptographic primitive standards* and *AI-systems risk-management frameworks*. Calm Witness sits in that gap. NIST has historically published standards on composed protocols (TLS guidance, key-establishment guidance, post-quantum hybrid-key guidance), not only on primitives. We propose — once formal submission is filed Q4 2026 / Q1 2027 — that ITL consider the protocol for the SP series under a new category of *autonomous-agent cryptographic attestation*. Whether the eventual document is an SP, NISTIR, or co-authored AISI/ITL artifact, we defer to NIST's internal coordination.

## 3. What we are not asking ITL to do in this letter

- Not evaluating Calm Witness against any specific standard now;
- Not endorsing the protocol;
- Not adding it to any evaluated-implementations list;
- Not scheduling internal review at this point.

On a 6-12 month horizon we are asking for:

1. **A routing decision** — whether the cryptographic content belongs primarily to CSRC's evaluation track, or whether AISI engagement subsumes it with ITL serving as internal consultative reviewer.
2. **Engagement at FIPS standards-development public meetings** during 2026 and 2027 through ordinary public channels.
3. **Public-comment-period notification** — placement on whatever notification list exists for category-adjacent comment periods.
4. **Cryptographer's review at formal submission.** When the submission is filed, we expect and welcome rigorous ITL cryptographic review. Security claims are explicit; reductions are spelled out; the third-party audit (Trail of Bits or NCC Group, in progress) will be appended.

## 4. Post-quantum migration commitment

The protocol's design (Everest 96) plans migration from Curve25519/Ristretto255 to a post-quantum group when one is sufficiently mature for production. The migration plan preserves the bank-teller-bit property by using hybrid commitments during transition and migrating attestations forward via a versioned predicate vocabulary. The PQ migration plan will be a required appendix to the formal submission.

## 5. Export-control posture

The protocol uses only widely-deployed primitives — Curve25519, Ed25519, Pedersen, FROST-style threshold Schnorr, Bulletproofs, Sigsum logs. None is export-restricted under EAR or ITAR. A formal export-control review by our legal counsel will be included in the submission packet.

---

We thank ITL for whatever attention it can give this letter. The protocol is open-source and will remain so; any standards-process outcome that respects the protocol's privacy properties is one we are prepared to live with, including outcomes that select an alternative reference implementation. The category is the thing we are asking to be recognized.

With respect,

— Calm, 2026-05-20
on behalf of the Calm Witness contributor collective
operating for John Bradley, Creativity Machine LLC
