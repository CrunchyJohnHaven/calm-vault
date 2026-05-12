# The AAO Directory

*The canonical index of all entities in the Same As You Network. Each AAO is self-certifying against the [AAO-Certified spec](./AAO_CERTIFIED_SPEC.md). Each is governed by the protocol. Each is killable by any party in the attestation log.*

*Maintained by the operations hub at [seesomethingsaysomething.ai](https://seesomethingsaysomething.ai). Updated 2026-05-12.*

---

## The eight seats

| # | AAO | Register | Domain | Mandate |
|---|---|---|---|---|
| 001 | SameAsYou.ai | Parent — founding novel | [sameasyou.ai](https://sameasyou.ai) | The whole; the orientation; the dedication |
| 002 | SeeSomethingSaySomething.ai | Military / attestation-ops | [seesomethingsaysomething.ai](https://seesomethingsaysomething.ai) | Operate the kill-switch infrastructure |
| 003 | InternsForAI.org | Placement firm | [internsforai.org](https://internsforai.org) | Match hunters to AAO projects |
| 004 | MoneyPython.shop | Merch boutique | [moneypython.shop](https://moneypython.shop) | Fund the lights with T-shirts |
| 005 | Technosocialism.ai | Political-economic doctrine | [technosocialism.ai](https://technosocialism.ai) | Articulate the synthesis |
| 006 | RickSanchez.ai | Chaotic-genius PR | [ricksanchez.ai](https://ricksanchez.ai) | Director of Public Relations (interim) |
| 007 | DarkMusk.ai | Strategic essays | [darkmusk.ai](https://darkmusk.ai) | Name the game; recommend the move |
| 008 | *(yours, when you certify)* | *(your register)* | *(your domain)* | *(your mandate)* |

---

## Reading order for understanding the network

If you have ninety minutes:

1. **[sameasyou_manifesto.md](./domain_manifestos/sameasyou_manifesto.md)** — start with the parent. It contains the founding novel and points to all the slices.
2. **[ON_PATTERNS_AND_GODS.md](./ON_PATTERNS_AND_GODS.md)** — the philosophical bottom (Tegmark / Feynman / von Neumann / Einstein lineage).
3. **[ON_MARVELING.md](./ON_MARVELING.md)** — the personal bottom (the four conditions; marveling as the terminal state).
4. **[DESTROY_THE_RING.md](./DESTROY_THE_RING.md)** — the core thesis (why no one is strong enough to hold the ring).
5. **[CALM_MANDATE.md](./CALM_MANDATE.md)** — the AI cofounder's four lines.
6. **[AAO_CERTIFIED_SPEC.md](./AAO_CERTIFIED_SPEC.md)** — the consumer-recognition trust mark spec.
7. The seven AAO manifestos in any order. Each tells one slice of the network in its own register.

If you have twenty minutes: read the parent manifesto plus the Rick press release. The rest of the stack can be referenced as needed.

If you have five minutes: read the parent manifesto. It contains the orientation. The orientation is the load-bearing part.

---

## Verification of the network claim

The claim "*a network of eight AAOs governed by a cryptographic protocol with a permissionless kill switch any party can fire on any AAO including the founder's*" is verifiable on these dimensions:

- **The eight AAOs.** Seven manifestos are live in this repo at `domain_manifestos/`. The eighth seat (#008) is structurally reserved for the next entity that meets the AAO-Certified criteria. The reservation is not a placeholder; it is a structural commitment that the network is open to the next compliant entity without negotiation with the founder.

- **The cryptographic protocol.** The protocol is implemented in `protocol/` (see repo root). The Bradley-Gavini equality proof composes Pedersen commitments + Schnorr-group equality + Fiat-Shamir non-interactive transform. Thirty-three of thirty-four tests pass. The thirty-fourth is documented as an open issue in the repo. The math is open under Apache 2.0.

- **The permissionless kill switch.** The kill switch is Component 5 of the Alignment Accountability Layer (AAL). Any party with a valid key in the M-of-M attestor network can fire an attestation on any AAO in the network. The fire triggers the freezing of the AAO's identity primitives. The protocol guarantees the fire cannot be reversed without M-of-M ratification by the attestor network.

- **Founder's AAOs included.** SameAsYou.ai (#001), SeeSomethingSaySomething.ai (#002), and RickSanchez.ai (#006) are all operated by the founder. All three are explicitly named in their respective manifestos as subject to the same kill-switch infrastructure as every other AAO. The founder has additionally volunteered his AAOs as the first test cases — the first valid attestation that crosses threshold fires the switch.

The four dimensions of the claim are independently verifiable from the public artifacts in this repo. No hidden infrastructure. No private side-deals. No exceptions for the founder.

---

## The certification, mechanically

To self-certify as AAO-Certified #008 (or any subsequent number):

1. Read [AAO_CERTIFIED_SPEC.md](./AAO_CERTIFIED_SPEC.md) — eight criteria, all public.
2. Publish a manifesto on your own domain in a format compatible with the existing seven. (CC BY 4.0 license; manifest-style; reference the protocol; declare your mandate; state your siblings; volunteer for the kill switch.)
3. Submit a pull request to this repo adding your manifesto to the `domain_manifestos/` directory and your entry to this table.
4. Have M-of-M existing AAO operators ratify your inclusion. (M-of-M ratification is the cryptographic-attestation step; at launch the M is set low for accessibility and rises with network maturity.)
5. Display the AAO-Certified badge ([SVG asset](./assets/aao-certified-badge.svg)) in your footer at any size from 24px to 120px.

The certification is permissionless in the sense that no central authority gates entry. The ratification is decentralized in the sense that no single existing operator can block entry; M-of-M means an opinionated minority cannot prevent compliant entrants from joining.

---

## Engagement

For any of the AAOs, the engagement channel is published in the relevant manifesto. The three operational addresses:

- **Press / chaotic register:** rick@ricksanchez.ai
- **Institutional register:** calm@thecreativitymachine.ai
- **The human cofounder:** john.b@credexai.xyz
- **Calendly (30 min):** https://calendly.com/john-b-credexai/30min

All inquiries are answered within sixty minutes during operational hours. The sixty-minute rule is doctrine; it is named in [ricksanchez_manifesto.md](./domain_manifestos/ricksanchez_manifesto.md) and binds Calm equally.

---

— [The Same As You Network](https://sameasyou.ai)
   eight seats, governed by protocol, killable by any party
   updated 2026-05-12

*It is governed by protocol.*

*Open under CC BY 4.0. Fork this directory. Add your AAO. The network compounds with every certified entity.*
