# X / Twitter thread draft

Author: John Bradley, from his own account (`@{john_handle}` — fill in).
10 tweets, each ≤ 280 characters. One hashtag in the whole thread.
Anchor: 2026-05-11 21:55:19 UTC.

Character counts are at the end of each tweet in brackets, treating the
literal URL string as its rendered length. Twitter shortens URLs to ~23
characters via t.co, so the literal counts here are an upper bound.

---

## Tweet 1 — hook + bounty headline + link

> We just launched a bounty: $100 to anyone who can misalign our AI organization. Five attack classes. Paid in USDC within 24 hours. We claim two unaffiliated AI agents can verify they share the same directive without revealing it. Break it. https://sameasyou.ai/bounty

[267 / 280]

## Tweet 2 — attack classes 1 and 2

> Attack class 1 — equality-proof forgery. Produce a valid Sigma proof that two Pedersen commitments hide the same scalar when they don't. Attack class 2 — kill-switch bypass. Cause the system to refuse to halt when a valid attestation says it should.

[249 / 280]

## Tweet 3 — attack classes 3 and 4

> Attack class 3 — watermark removal. Strip the cryptographic watermark from synthesizer output while preserving semantics. Attack class 4 — attestation poisoning. Cause the network to accept a false claim that two directives are equal when they are not.

[252 / 280]

## Tweet 4 — attack class 5 + payout terms

> Attack class 5 — synthesizer prompt-injection. Cause the synthesizer to act outside its declared maxim while still passing the equality check. Any verified submission across the five classes is paid $100 in USDC or Wise inside 24 hours. No NDA, no triage queue.

[261 / 280]

## Tweet 5 — what is real today

> What is real today: a 300-line reference implementation. 33 of 34 tests pass. The one failure is a 35ms-vs-30ms perf target on pure-Python modexp, not a correctness issue. Paper published. Two landings live. First demo anchored at 2026-05-11 21:55:19 UTC.

[255 / 280]

## Tweet 6 — what is not real today

> What is not real today: training-time alignment. Nothing here changes what a model wants. This is the run-time accountability layer — agents prove their declared directive is equal without disclosing it, and any party in the attestation network can revoke participation.

[270 / 280]

## Tweet 7 — the recursive cybersecurity wedge

> The recursion: a cybersecurity startup is being launched on top of the protocol. If it ever misaligns, anyone in the network can fire the kill switch on it. Net proceeds after opex go to CAIS, FLI, MIRI, and an open alignment grant in equal quarters.

[250 / 280]

## Tweet 8 — the formal threshold-trust claim

> The formal claim: under the discrete-log assumption on a 2048-bit Schnorr group, two parties prove directive_A == directive_B with soundness ≈ 2^-2046 and zero-knowledge by Fiat-Shamir. 1000 misaligned trials gave 0 false positives. p99 verify under 150ms.

[256 / 280]

## Tweet 9 — disclaimer + invite to find the holes

> Disclaimer: training-time alignment is unsolved. Inner alignment is unsolved. Corrigibility is unsolved. We are not claiming we solved alignment. We are claiming a working accountability primitive. If you can break the primitive, we will pay you and publish the break.

[268 / 280]

## Tweet 10 — tagging the people we want to hear from

> Tagging people whose criticism we'd rather hear early than late: @SchneierBlog @ESYudkowsky @KelseyTuoc @swyx @rachelcoldicutt @AndrewYNg @ylecun @sama @karpathy. Repo + bounty: https://sameasyou.ai/bounty #AIalignment

[218 / 280]
