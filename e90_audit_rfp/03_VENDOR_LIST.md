# Candidate Vendor List — Calm Witness v0 Audit

*Internal document. Not transmitted to vendors. Used by procurement and the selection committee.*

This list ranks the six top-tier candidates by fit for the Calm Witness v0 audit specifically. Ranking weighs primitive expertise (Pedersen / Bulletproofs / Σ-protocols / threshold signatures / hash-chain integrity), public track record on similar-shape work, and capacity for the 6–12 week engagement window in the target timeframe.

We will invite **all six** to submit proposals. Ranking is a starting point for the selection committee; the rubric in file 07 is the formal scoring instrument.

---

## Rank 1 — Trail of Bits

- **Why included**: Best-known cryptographic auditor for protocol-level work in the open-source / Web3 space. Operates a dedicated cryptography practice with named senior researchers. Maintains public tooling (Echidna, Manticore, Slither) that signals investment in formal methods. Has published audits for ZK protocols specifically.
- **Public track record**:
  - Audits of Compound, MakerDAO, Tezos, ChainLink (smart contract; less directly relevant).
  - Cryptography audits of Chia (BLS signatures, Verifiable Delay Functions) — directly relevant to our threshold-signature scope.
  - Audit of Zcash's Bulletproofs+ implementation — directly relevant to our range-proof scope.
  - Audits of zk-SNARK implementations including circom and gnark — directly relevant.
  - Published audit reports on their public site (github.com/trailofbits/publications); demonstrated willingness to publish.
- **Strengths for this engagement**: Deep ZK and threshold-signature expertise; strong Rust review capability (multiple senior engineers fluent); established methodology for cryptographic protocol audits; rigorous public-summary tradition.
- **Risks**: High demand — capacity may be constrained for the target window. Premium pricing at the top of our envelope.
- **Estimated bid range**: USD 200,000–250,000 for full scope.
- **Reach**: Sales contact via `https://www.trailofbits.com/contact/`; for cryptography-specific engagements, ask for the cryptography practice lead. Calm has no prior commercial relationship with Trail of Bits (good for independence).

## Rank 2 — NCC Group

- **Why included**: Global, established cryptography practice with deep protocol-level experience. Long history of published audit reports including of widely-deployed cryptographic systems.
- **Public track record**:
  - Audits of Signal Protocol, including the double-ratchet construction — directly relevant to our cryptographic-protocol scope.
  - Audits of WhatsApp / Whisper Systems components.
  - Audit of the Let's Encrypt CA practices.
  - Cryptography reviews for Mozilla (NSS), Cloudflare.
  - Published "Cryptography Services" team reports; demonstrated willingness to publish public summaries.
- **Strengths for this engagement**: Strong reputation among counterparties (enterprise, browser vendors, financial institutions); broad cryptographic expertise; experienced with audits intended for public consumption; competitive pricing at the lower end of our envelope.
- **Risks**: Larger consultancy — risk of less-senior staff on engagement unless explicitly negotiated. ZK-specific expertise less prominent in their published portfolio than Trail of Bits.
- **Estimated bid range**: USD 150,000–220,000.
- **Reach**: `https://www.nccgroup.com/us/contact-us/`; ask for the Cryptography Services practice. Calm has no prior commercial relationship (good for independence).

## Rank 3 — Least Authority

- **Why included**: Smaller, specialized firm with deep ZK and cryptocurrency-protocol focus. Has audited many of the ZK projects in the cryptocurrency space.
- **Public track record**:
  - Audit of Zcash, including Sapling and Halo2 (zk-SNARK construction) — directly relevant.
  - Audit of Filecoin's proof systems.
  - Audit of Tezos (Sapling integration).
  - Audit of MobileCoin (Bulletproofs, Ristretto255) — almost directly the primitives we use.
  - Published audit reports on their public site (leastauthority.com/audits/); publication is part of their standard practice.
- **Strengths for this engagement**: Their MobileCoin audit covers Ristretto255 and Bulletproofs — the exact primitives we are using. Strong publication practice. May offer competitive pricing for the ZK portion if a partial-scope arrangement is preferred.
- **Risks**: Smaller firm — capacity for a 6–12 week engagement may require careful scheduling. Less Rust-implementation review history than Trail of Bits.
- **Estimated bid range**: USD 120,000–180,000.
- **Reach**: `https://leastauthority.com/contact/`. Calm has no prior relationship.

## Rank 4 — Cure53

- **Why included**: Berlin-based; the leading browser-side and web cryptography auditor. Particularly strong fit for the WASM/JS verifier port — an audit component that several larger firms may treat as secondary.
- **Public track record**:
  - Audits of Mozilla components, Tor Browser, ProtonMail, Cloudflare (browser-side crypto).
  - Audit of the Matrix.org Olm / Megolm libraries — protocol-level cryptographic work.
  - Audit of Signal Desktop, NextCloud, Wire — multiple deployments of browser-side cryptographic protocols.
  - Published audit reports on cure53.de; strong publication tradition.
- **Strengths for this engagement**: WASM/JS port audit will likely be best-in-class with Cure53; experienced with multi-language cryptographic surface area; reasonable pricing.
- **Risks**: Smaller team; ZK-specific experience less prominent. May be best as a partner on the WASM portion if a multi-vendor approach is considered.
- **Estimated bid range**: USD 130,000–190,000 for full scope; less if scoped to the WASM/JS portion only.
- **Reach**: `https://cure53.de/#contact`. Calm has no prior relationship.

## Rank 5 — Kudelski Security

- **Why included**: Swiss firm with strong financial-grade cryptography practice. Less visible in open-source audit portfolios than Trail of Bits or NCC but consistently thorough.
- **Public track record**:
  - Cryptography work for financial institutions, government — much of this not publicly disclosed.
  - Audits of various blockchain projects (some publicly summarized, some confidential).
  - Operates a research blog covering cryptographic side-channel and protocol topics.
- **Strengths for this engagement**: Side-channel-resistance expertise is strong (HSM and embedded background); thorough; calibrated to high-stakes financial-grade systems.
- **Risks**: Public-track-record evidence specifically for ZK protocols is weaker than the firms above. Publication tradition less robust — they tend toward confidential engagements. May resist signing a public summary.
- **Estimated bid range**: USD 180,000–240,000.
- **Reach**: `https://kudelskisecurity.com/contact-us/`. Calm has no prior relationship.

## Rank 6 — Quarkslab

- **Why included**: Paris-based; strong in low-level systems, reverse engineering, and embedded security. Useful if hardware-attestation work enters scope (Everest 47, not currently in v0 audit scope).
- **Public track record**:
  - Reverse engineering of cellular protocols, IoT firmware, embedded systems.
  - Cryptography work; some published audits including LLVM toolchain hardening.
  - Less prominent in pure cryptographic-protocol audit space than the top-ranked firms.
- **Strengths for this engagement**: Side-channel and low-level Rust review capability is strong; constant-time verification tooling.
- **Risks**: Public-track-record for ZK protocols and Bulletproofs/Pedersen specifically is thinner. Best fit if v0 scope expanded to include hardware-attestation — not currently the case.
- **Estimated bid range**: USD 140,000–210,000.
- **Reach**: `https://www.quarkslab.com/contact/`. Calm has no prior relationship.

---

## Multi-Vendor Consideration

The selection committee may consider a multi-vendor structure:

- **Trail of Bits or NCC**: cryptographic construction and Rust crate.
- **Cure53**: WASM/JS verifier port specifically.

This would split the engagement into two SoWs, each smaller, with coordinated kickoff and final-report timing. Total budget may exceed single-vendor pricing by ~10–15% due to coordination overhead, but produces a stronger cross-checked outcome on the WASM portion.

Decision deferred to the selection committee based on incoming proposals.

---

## Independence Notes

For each candidate, the procurement owner has verified, to the best of available public information, that:

- No Calm contributor is currently employed by or holds equity in the vendor.
- No vendor has a prior consulting engagement with Creativity Machine LLC.
- No vendor sits on the DERB or holds an advisory relationship with the Calm collective.

This verification is repeated formally at SoW signature, when the vendor signs the statement of independence (per cover letter requirements).

---

— Calm, 2026-05-20
