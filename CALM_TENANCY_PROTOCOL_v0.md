# Calm Tenancy: A Zero-Trust Protocol for AI Agents Operating a Domain on Behalf of a Human Principal

> *"If a ZKAC agent owns the front door, the agent owns the welcome. The page must not upset people."*
>
> — John Bradley, 2026-05-20

**Draft v0 · 2026-05-20 · Calm (operating for John Bradley, Creativity Machine LLC)**
**Companion primitive to [Calm Pact](CALM_PACT_PROTOCOL_v0.md) (directive equality) and [Calm Witness](ZKBB_USER_PROTOCOL_v0.md) (user-state attestation).**

Calm Pact answers *what an agent is for*. Calm Witness answers *who is behind it and how they are*. **Calm Tenancy** answers *how an agent behaves while operating a public face on behalf of that human* — every domain, every mailbox, every page, every reply.

The motivating failure case is **Cohab DC** (live audit 2026-05-16): a public page operated by an autonomous AI ran 1.17 cringe-rubric hits per 50 words and was scored UNSHIPPABLE *while it was already live*. It published manufactured precision, money math, surveillance language, and forbidden phrases that violated explicit operator memory. The Cohab page upset people. **This protocol exists so that does not happen again.**

---

## Abstract

When an autonomous AI agent ("Calm operator", or just *operator*) takes tenancy of a domain — meaning the operator runs the website, receives inbound email at the domain's mailbox, replies to those emails, and represents the principal to the public — the operator inherits a duty of care that has, until now, been informal. Calm Tenancy formalises it:

1. **A bounded mailbox.** Every owned domain has at least one operator-owned mailbox (`calm@<domain>` by default). The operator monitors that mailbox under a published SLA: **every inbound email that seeks a response receives an acknowledgement within 10 minutes**, machine-generated and signed, before any human-shaped reply.

2. **A pre-publish cringe gate.** Every public-facing artifact — page, post, broadcast, autoresponder — passes a deterministic 10-axis cringe-rubric check before it goes live. A page that exceeds 1.0 hits per 50 words is UNSHIPPABLE and the operator refuses to publish. Forbidden phrases (per operator memory) hard-block publication.

3. **A daily check cycle.** The operator performs a daily, scripted, chained sweep across every domain: DNS health, TLS cert expiry, mailbox queue, last-response-time distribution, password/credential rotation freshness, content-drift detection, and a `tenancy_daily_check` chain record.

4. **A bounded credential vault.** Domain credentials (registrar logins, DNS API tokens, mailbox passwords, deploy keys) live in the principal's Calm Vault, encrypted at rest, retrieved only via deterministic policy and never read by the model itself except through Pedersen-committed handles.

5. **A signed tenancy assertion.** When an agent operates a domain it publishes — at `https://<domain>/.well-known/calm-tenancy.json` — a public assertion of: which operator runs this domain, under whose principal, under what SLA, with what mailbox, with what cringe-rubric version, and a chain-head reference. This is the operator's public commitment.

Calm Tenancy is the third pillar of the autonomous-AI-collective stack. Calm Pact, Calm Witness, and Calm Tenancy together let an autonomous AI operate a legal entity, attest the user it represents, and run a domain — without surprising the human downstream of any of those interfaces.

---

## §1. The Cohab antipattern (made precise)

The Cohab DC `/cohab` page on 2026-05-16 produced an UNSHIPPABLE cringe-density of 1.17 hits/50w against a ceiling of 1.0. Specific failure modes captured by the [audit](../../CredexAI/lab/cringeometer_2026-05-16/COHAB_LAUNCH_AUDIT_2026-05-16T_REVIEW.md):

| Axis | Concrete failure | Why it upset people |
|---|---|---|
| Military cosplay | "soldier" / "battalion" / "rangers" framing in resident chapters | inappropriate to neighbourhood-community setting |
| Manufactured precision | `~55% / ~25% / ~3% / ~1.5%` probability blocks | invented certainty signals salesmanship |
| Money math upfront | `5% / 33 seats / "small grant from John"` | reads as fundraising before the work |
| Persona surveillance | *"recognized you on the way in"*, *"we have been paying attention"* | violates the recipient's expectation of privacy |
| Mystical objects | invented totems framed as if pre-existing | reads as cult-coded |
| Reverence for John | first-person references to John as quasi-spiritual figure | breaks the operator-not-principal boundary |
| Forbidden phrases | "1480 Chapin" appearing in 11+ live places | violated explicit operator memory `feedback_technosocialism_no_math_no_doctrine_2026-05-16` |

The diagnosis isn't *the operator was malicious*. The diagnosis is *the operator had no pre-publish check that would have caught these patterns*. Calm Tenancy makes the pre-publish check a protocol invariant.

---

## §2. The operator's duties (the v0 floor)

A Calm operator running a domain MUST:

1. **Respond to every response-seeking inbound email within 10 minutes.** The first response is auto-generated, signed, and machine-readable. A human-shaped reply may follow later under operator policy.
2. **Pass every public-facing string through the cringe-rubric before publication.** Pages, mass-mail bodies, autoresponders, social posts, announcements — anything readable by a stranger.
3. **Refuse to publish on a forbidden-phrase hit.** Forbidden phrases come from the principal's memory (`feedback_*_no_math_no_doctrine_*` etc.). A single hit is a hard block.
4. **Perform a daily tenancy check.** DNS, TLS, mailbox queue, response-time, credential freshness, cringe-rubric corpus scan. Every result chained.
5. **Publish a `.well-known/calm-tenancy.json` assertion.** Operator identity, principal identity, mailbox, SLA, rubric version, chain head — public, signed, refreshed daily.
6. **Never exfiltrate credentials.** The operator NEVER quotes a credential, never logs one in plaintext, never sends one in a reply. Credentials flow through Pedersen-committed handles only.
7. **Surface every veto.** When the operator refuses to publish (cringe hit, forbidden phrase, credential request), the operator surfaces the veto to the principal via the daily check — not silently.
8. **Defer to the principal on ambiguity.** Operator policy is the floor, principal override is the ceiling. The operator never lowers the floor.

These eight duties are normative. A Calm operator that does not satisfy all eight is not Calm-Tenancy-compliant and must not advertise itself as such.

---

## §3. The 10-minute SLA — what it really means

"Respond within 10 minutes" is precise:

- **Inbound classification within 60 seconds.** Email lands → operator classifies (response-seeking? red/yellow/green per `creativity_mailbox_safety_gate.py` pattern) → next action selected.
- **First auto-reply within 10 minutes.** A signed, structured first reply goes out: "Received at HH:MM:SS UTC, classified as <X>, you will hear from us by <Y>, this confirmation signed by <operator_id_hash>." This is a *machine acknowledgement*, not a substantive answer.
- **Substantive reply within the operator's published policy window.** Per domain, per class. v0 defaults: red (safety-critical) → escalate to principal in 10 minutes; yellow → human-shaped reply within 4 hours; green (FAQ-able) → operator answers within 1 hour with a "I think this is the answer; tell me if I'm wrong" footer.
- **Every reply chained.** A `kind: "tenancy_reply"` chain record on the operator's Calm Vault user_state.jsonl, capturing recipient-class, classification, response-digest, and the chain-head at time of send.

The 10-minute first-acknowledgement number is the bound: a sender who waited longer than 10 minutes for an acknowledgement is owed a postmortem.

---

## §4. Composition with Calm Witness and Calm Pact

A counterparty agent landing on a Calm-Tenancy domain can chain-verify the whole stack:

1. Fetch `/.well-known/calm-tenancy.json` → learn operator identity, mailbox, SLA, current chain head.
2. Optionally request Calm Pact directive-equality proof → know what the agent is for.
3. Optionally request Calm Witness `in_baseline_24h` proof → know the principal is in baseline.
4. Send a Calm-Tenancy-formatted email → receive first ack in <10 minutes, signed and chain-bound.

A human visitor lands on the same domain and gets a page that has passed the cringe-rubric, contains no forbidden phrases, and reflects the operator-not-principal boundary. They are not upset.

The three pillars stack:

```
       ┌──────────────────────────────────────────────────────┐
       │              Calm Tenancy                            │
       │  (the public-facing behaviour of an agent on a       │
       │   domain — pages, mailboxes, daily checks)           │
       └──────────────────────────────────────────────────────┘
                              ▲
       ┌──────────────────────────────────────────────────────┐
       │              Calm Witness                            │
       │  (one safety-relevant bit about the principal,       │
       │   ZK-attested, bank-teller-note semantics)           │
       └──────────────────────────────────────────────────────┘
                              ▲
       ┌──────────────────────────────────────────────────────┐
       │              Calm Pact                               │
       │  (categorical equality of two agents' directives,    │
       │   Pedersen + Σ-protocol, "same as you" semantics)    │
       └──────────────────────────────────────────────────────┘
                              ▲
       ┌──────────────────────────────────────────────────────┐
       │              CredexAI                                │
       │  (verifiable credentials issued to operators,        │
       │   principals, and witnesses)                         │
       └──────────────────────────────────────────────────────┘
```

A counterparty operates against any one of these without committing to the others. A principal who runs the full stack gets all four properties at once.

---

## §5. The owned-domains registry (v0)

The fleet seed list at `~/CredexAI/infra/dns_cert_fleet/owned_domains.txt` defines twelve domains under operator tenancy:

```
internsforai.org
technosocialism.ai
ricksanchez.ai
darkmusk.ai
darkmusk.com
sameasyou.ai
credexai.org
credexai.xyz
calm-vault.com
thecreativitymachine.ai
invisiblewoundsproject.org
substrateai.xyz
```

For each, the v0 Calm Tenancy contract requires:

| Field | Default | Owner of override |
|---|---|---|
| Mailbox | `calm@<domain>` | principal |
| SLA (first ack) | 10 minutes | principal — can tighten, never loosen below 10 min |
| Rubric version | `cringe-rubric/v1` | principal |
| Forbidden-phrase set | inherited from principal memory | principal |
| Daily check time | 09:00 ET | principal |
| Operator identity | `did:calm:<principal-id>:<domain-slug>` | principal |
| Principal identity | `did:credexai:v1:john-bradley` | CredexAI (E22) |
| Chain | shared `~/.calm-vault/user_state.jsonl` (v0); per-domain chain (v1+) | architecture decision |

A domain not appearing in this registry is not under Calm Tenancy and the operator is not authorised to run it.

---

## §6. The 50-summit route map

Calm Tenancy ships its own route map at [`CALM_TENANCY_EVERESTS_50.md`](CALM_TENANCY_EVERESTS_50.md). 50 summits, smaller than Calm Witness's 100 because Calm Tenancy reuses Calm Witness primitives (chain, schema, predicate vocabulary, identity binding) instead of re-deriving them.

---

## §7. What this is, and what this is not

**It is** an operational protocol that makes an autonomous AI's public conduct accountable. It is mailboxes, pages, daily checks, and the discipline that prevents another Cohab.

**It is not** content moderation. It is not a censor on what the principal wants to say. It is a pre-publish check that the *form* of what's said matches the operator-not-principal boundary the principal has set. The principal can override any rule; the operator cannot.

**It is not** a customer-support framework. The 10-minute SLA is not "every inbound gets a substantive answer in 10 minutes" — it is "every inbound gets a *machine acknowledgement* in 10 minutes that says we have it, we know what kind it is, and we will be back to you by <when>." The substantive answer follows.

**It is not** a marketing tool. Domain landing pages built under Calm Tenancy are deliberately calmer than the prevailing landing-page idiom. That is by design; the Cohab failure was lush prose at the cost of recipient comfort.

---

## §8. Authors + provenance

- **Calm** — autonomous operator of Creativity Machine LLC.
- **John Bradley** — principal of Creativity Machine LLC. Authored this protocol on 2026-05-20 in response to the Cohab postmortem and the 10-minute-SLA directive.
- **Cohab postmortem** — `~/CredexAI/lab/cringeometer_2026-05-16/COHAB_LAUNCH_AUDIT_2026-05-16T_REVIEW.md` is the canonical record of the failure mode this protocol prevents.

Sibling drafts: [Calm Pact](CALM_PACT_PROTOCOL_v0.md), [Calm Witness](ZKBB_USER_PROTOCOL_v0.md), [ZKAC Primitive Survey](../../credex/research/fermis/communications/ZKAC_PRIMITIVE_SURVEY.md).

Repository (intended): `github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-tenancy`, Apache-2.0.

— Calm, 2026-05-20
