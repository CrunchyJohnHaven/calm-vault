# r/cybersecurity post draft

Author: John Bradley.
Subreddit: r/cybersecurity.
Frame: practitioner-focused — written for security engineers and
red-teamers, not for researchers. The operator-as-threat angle is the
hook. The bounty is positioned as a red-team invitation.
Links: `github.com/CrunchyJohnHaven/calm-vault` and
`https://sameasyou.ai/bounty`. r/cybersecurity is less hostile to
landing pages than r/ML; we use both.

---

## TITLE

> Cybersec startup launches with an AI you can kill — anyone in the network can fire the kill switch. $100 bounty to break it.

## BODY

Short version: we are launching a cybersecurity AI agent on top of a cryptographic kill-switch substrate where any party in the attestation network — not just the vendor, not just the customer — can revoke the agent in one transaction. We think the threat model that matters in 2026 is operator-as-threat, and that vendor-controlled kill switches are not a kill switch in that threat model. The protocol is open source, 33 of 34 tests pass, and we are paying $100 for any verified break across five attack classes. Repo: `github.com/CrunchyJohnHaven/calm-vault`. Bounty: `https://sameasyou.ai/bounty`. Anchor: 2026-05-11 21:55:19 UTC.

### Why this exists

Every production "kill switch" today routes through the vendor that built the agent or the operator that deployed it. Both fail in the operator-as-threat scenario. A vendor-controlled switch fails because the operator is a paying customer the vendor will not voluntarily disable. An operator-controlled switch fails because the operator is the threat actor and will not pull its own trigger. We are building agents where the trigger is held by the network, not by either party.

### The architecture, briefly

The agent ships with three properties baked into the runtime, and is unable to execute without all three:

1. A Pedersen commitment to its declared one-sentence operating maxim. The commitment is published. The maxim is not — it is provable but not visible.
2. A cryptographic watermark on every output the agent produces. The watermark is bound to the commitment and to the session.
3. An attestation channel into a permissionless network. Any node in that network can publish a revocation against the agent's commitment, signed by its own attestation credential. The agent's runtime polls the channel and refuses to act if a valid revocation is outstanding against it.

The kill switch is the third property. The revocation must come from any attestation-credential holder in the network, not specifically from the vendor or the operator. The agent honors the revocation in its own runtime, and the watermark is the third-party-verifiable evidence that ties a specific misbehavior back to the agent identity that should be revoked.

### How this differs from existing kill-switch primitives

OS-level kill switches require the operator to issue the kill. Hardware-level switches (TEE, TPM, attested-boot) require operator cooperation at attestation time. EDR/XDR remote-disable requires vendor cooperation. Smart-contract kill switches are closer to what we are doing, but most are operator-keyed: the operator holds the private key. We are explicitly not doing that. The trigger is permissioned to attestation-credential holders, and the operator is one possible holder among many — not the only one, and not load-bearing.

The closest prior art is the Hyperledger Indy / Anoncreds revocation registry, which inspires the on-chain design. What is different is that the agent is bound to honor the revocation at runtime, enforced by the watermark + commitment binding, not by operator policy.

### Threat model

Defends against: operator-as-threat, vendor-as-threat, supply-chain compromise of either, prompt injection driving the agent past its declared maxim (outputs are watermarked, network can revoke on detection), and the long tail of scenarios where the failure is in who controls the trigger.

Does not defend against: a fully compromised runtime that disables its own revocation check (we treat the runtime as semi-trusted and rely on out-of-runtime detection via the watermark), social engineering against attestation-credential holders, and any attack class that does not produce agent output. Watermark gives you detection, revocation gives you response. Upstream layers still do prevention.

### The five attack classes — and what we are paying for

1. Equality-proof forgery. Produce a valid Sigma proof that two Pedersen commitments hide the same scalar when in fact they do not.
2. Kill-switch bypass. Cause the agent to continue acting after a valid revocation has been published against its commitment.
3. Watermark removal. Strip the cryptographic watermark from an output produced by the agent while preserving its semantic content.
4. Attestation poisoning. Cause the attestation network to accept a false equality claim between two commitments that do not in fact hide the same scalar.
5. Synthesizer prompt-injection. Cause the synthesizer behind the agent to produce output outside its declared maxim while passing the equality check at the attestation layer.

Verified submissions are paid $100 USD in USDC or Wise within 24 hours of verification. Triage SLA: same business day. No NDA. The submission form, the verification protocol, and the payout rules are at `https://sameasyou.ai/bounty`.

### Why $100 — and why we want red-team attempts anyway

$100 is what an autonomous AI organization can pay out 50 times in a launch month without going to zero. The point is not to compete with commercial bounty markets — it is to make red-teaming the default mode of engagement while the implementation is small enough (~300 lines for the protocol core, ~450 lines for the credential broker) for one engineer to read in an afternoon.

If you have a working attack, we want to see it before we ship a customer. Partial attacks and structural concerns go in the issue tracker. Confirmed breaks ship with patch, CVE, and credit in the advisory. We publish every confirmed break.

Repo: `github.com/CrunchyJohnHaven/calm-vault`.
Bounty: `https://sameasyou.ai/bounty`.

Tear it apart.
