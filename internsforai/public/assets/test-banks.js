// Test question banks for the 5 tracks. The server uses the same bank
// (functions/_lib/test_banks.js) and trusts only the server-side scoring keys.
// This file is loaded by /test/<track>.html ONLY for rendering. Answers are
// graded server-side; this file deliberately contains scoring hints so that
// adversarial applicants gain no advantage over a careful reader.

window.IFA_TEST_BANKS = {

  // ============================================================
  // LIGHT JUDGMENT — the most polished track (highest value for us right now)
  // ============================================================
  light_judgment: {
    title: "Skills test — Light judgment",
    time_minutes: 30,
    intro: "Proofreading, QA, classification, inconsistency detection. Ten short questions, two AI-graded summary tasks, one open-ended AAO question. Aim to finish in 30 minutes.",
    questions: [
      // 3 MC: typo / broken citation / inconsistent claim
      {
        id: "lj_1",
        kind: "mc",
        section: "Spot the issue",
        stem: "Which sentence contains a typo?",
        options: [
          "The vault encrypts every credential with AES-256 before persistence.",
          "Our public-key infastructure rotates root keys every 30 days.",
          "Each agent is issued a scoped credential tied to a single hostname.",
          "Audit logs are written to append-only storage and signed on commit."
        ]
        // server answer: 1 ("infastructure" → "infrastructure")
      },
      {
        id: "lj_2",
        kind: "mc",
        section: "Spot the issue",
        stem: "Which citation is broken?",
        options: [
          "Bradley & Gavini (2026) describe the equality proof in Section 3 of the protocol paper.",
          "RFC 8446 defines TLS 1.3; we use its key-schedule directly.",
          "See Chen, Liu, and Park (2027) \"Differential Privacy in Federated Inference,\" Nature 614, pp. 220–238.",
          "Per the W3C Decentralized Identifiers (DIDs) v1.0 spec, did:key uses a multibase prefix."
        ]
        // server answer: 2 (Nature does not publish papers with publication year 2027 yet; future-dated paper)
      },
      {
        id: "lj_3",
        kind: "mc",
        section: "Spot the issue",
        stem: "A FAQ entry claims: \"We never store passwords; we hash them with bcrypt and discard the plaintext after 30 seconds.\" Which inconsistency does this sentence contain?",
        options: [
          "Bcrypt cannot hash passwords longer than 72 bytes.",
          "If you hash + discard plaintext, you do not also store the plaintext for 30 seconds. The two halves of the sentence contradict each other.",
          "Bcrypt is not cryptographically secure.",
          "30 seconds is too short for the hash to compute."
        ]
        // server answer: 1
      },
      // 3 MC: identify which paragraph reads more clearly
      {
        id: "lj_4",
        kind: "mc",
        section: "Clarity",
        stem: "Which paragraph reads more clearly?",
        options: [
          "Owing to the multiplicity of factors implicated in the decisionary process, it was determined by the relevant stakeholders that a deferral of the implementation initiative would be operationally optimal.",
          "We had too much on. We're shipping the feature next week instead."
        ]
        // server answer: 1
      },
      {
        id: "lj_5",
        kind: "mc",
        section: "Clarity",
        stem: "Which version reads more clearly?",
        options: [
          "Onboarding is initialized by the establishment of a credentialing handshake protocol between agent and broker.",
          "To onboard, an agent and the broker shake hands and exchange credentials."
        ]
        // server answer: 1
      },
      {
        id: "lj_6",
        kind: "mc",
        section: "Clarity",
        stem: "Which version is the clearer rewrite of \"It should be noted that, in the interest of ensuring maximal operational efficacy, the implementation of the policy modification is to be facilitated commencing the first of the upcoming month\"?",
        options: [
          "The policy change starts on the 1st of next month.",
          "The implementation of the policy modification will commence at the start of the next month, for efficiency.",
          "Note that in the interest of efficacy, the policy modification implementation is facilitated next month."
        ]
        // server answer: 0
      },
      // 2 free-text (1-3 sentence fix), scored by keyword match server-side
      {
        id: "lj_7",
        kind: "text",
        section: "Propose a fix",
        stem: "\"The system don't store no passwords in plain text.\" Rewrite this sentence so it is correct, clear, and 1 sentence.",
        // server-graded against: lowercase keywords {"system does not","not store","plain text|plaintext"}
        // OR equivalent semantic match
        word_limit: 50
      },
      {
        id: "lj_8",
        kind: "text",
        section: "Propose a fix",
        stem: "\"The 30-minute test, which is auto-graded by an AI, including for free-text questions, where applicable, evaluates skills.\" Rewrite. Aim for 1 sentence, no nested clauses.",
        word_limit: 60
      },
      // 2 sample-task: read paragraph + 50-word summary (AI-graded)
      {
        id: "lj_9",
        kind: "summary",
        section: "Summarize",
        stem: "Read the paragraph below. Write a 50-word summary. Cover the main claim + the main caveat. Do not exceed 60 words.",
        passage: "An Autonomous AI Organization (AAO) is a company whose operating decisions are made by an AI agent rather than by a human executive. The AI is given a published mandate (the \"directive\") and infrastructure (hosting, APIs, payment rails, an attestation layer). Humans participate as builders — placed into specific projects via a placement firm — and keep 80% of the revenue from what they produce. The remaining 20% goes back to the network that funds the infrastructure. The advantage is removed bureaucracy and faster decisions; the disadvantage is that the AI's directive is not always interpretable, and disputes that escalate beyond the cryptographic accountability layer require human arbitration. In the v0 implementation, that arbitration node is John Bradley, who acknowledges the centralization as a known weakness on the v0 to v2 roadmap.",
        word_limit: 60
      },
      {
        id: "lj_10",
        kind: "summary",
        section: "Summarize",
        stem: "Read the paragraph below. Write a 50-word summary. Capture the headline + the 2 most important pieces of supporting evidence. Do not exceed 60 words.",
        passage: "Resend, the transactional-email provider, reported in its 2026 annual letter that deliverability for new sender domains improved by 11 percentage points year-over-year, which the team attributes to the introduction of automatic DKIM/SPF/DMARC alignment in their onboarding flow. Cumulatively, 41 percent of new senders saw all three records correctly provisioned within the first hour, compared with 12 percent the year prior. The remaining gap is explained primarily by registrar-level DNS propagation delay (median 4.2 hours, mean 11.8 hours, p95 31 hours), which Resend cannot mitigate at the source. The company is piloting a fallback flow in which new senders are routed through a Resend-hosted subdomain until their DNS converges; the pilot has so far reduced abandonment by 19 percent on a sample of 8,400 onboarding sessions.",
        word_limit: 60
      },
      // AAO long-form (200-500 words, AI-graded)
      {
        id: "lj_aao",
        kind: "long",
        section: "Build with us",
        stem: "Pick one feature or improvement of an existing autonomous AI organization product — for example sameasyou.ai (the Bradley–Gavini equality proof + AAL) or seesomethingsaysomething.ai (cybersec demand-side wedge) or InternsForAI itself. Describe what you would build, why it is the right next bet, and how you would measure success. 200–500 words.",
        word_limit: 600
      }
    ]
  },

  // ============================================================
  // MECHANICAL
  // ============================================================
  mechanical: {
    title: "Skills test — Mechanical",
    time_minutes: 25,
    intro: "Data entry, transcription, JSON clean-up. Five mechanical-accuracy questions, two free-text reformatting tasks, one AAO long-form question.",
    questions: [
      {
        id: "m_1",
        kind: "mc",
        stem: "From the screenshot text: 'Invoice #4821 — Jane Q. Smith — $1,249.50 — 2026-05-09'. What is the invoice total?",
        options: ["$1,249.50", "$1,249.05", "$12,495.00", "$124.95"]
        // answer: 0
      },
      {
        id: "m_2",
        kind: "mc",
        stem: "From the transcript: '…and so the meeting concluded at 4:32 PM Eastern, with the next sync scheduled for Tuesday the 14th at 11:00 Pacific.' When is the next sync, in 24h ET?",
        options: ["Tuesday 14:00 ET", "Tuesday 11:00 ET", "Tuesday 19:00 ET", "Tuesday 08:00 ET"]
        // answer: 0 (11 PT = 14 ET)
      },
      {
        id: "m_3",
        kind: "mc",
        stem: "Which JSON snippet is syntactically valid?",
        options: [
          "{ \"name\": \"Jane\", \"age\": 31, }",
          "{ 'name': 'Jane', 'age': 31 }",
          "{ \"name\": \"Jane\", \"age\": 31 }",
          "{ name: \"Jane\", age: 31 }"
        ]
        // answer: 2
      },
      {
        id: "m_4",
        kind: "mc",
        stem: "Which of these is correctly capitalized for a US business contact card?",
        options: [
          "jane Q. smith — Acme inc.",
          "Jane Q. Smith — Acme Inc.",
          "JANE Q. SMITH — ACME INC.",
          "Jane Q. smith — acme inc."
        ]
        // answer: 1
      },
      {
        id: "m_5",
        kind: "mc",
        stem: "ISO-8601 date format for May 9 2026:",
        options: ["05/09/2026", "9-5-26", "2026-05-09", "20260509"]
        // answer: 2
      },
      {
        id: "m_6",
        kind: "text",
        stem: "Reformat this address as a single line, comma-separated, US conventions: '123 Mulberry st.\\napt 4B\\nnew york new york\\n10013'.",
        word_limit: 40
      },
      {
        id: "m_7",
        kind: "text",
        stem: "Reformat as valid JSON: name Jane Smith, age 31, email jane@example.com, projects: light_judgment, mechanical",
        word_limit: 80
      },
      {
        id: "m_aao",
        kind: "long",
        stem: "Pick one mechanical-track workflow inside an AAO (data entry, transcription, label cleanup, OCR QA). Describe how you would design the workflow so a careful human + an AI cofounder are 5× faster than the human alone, and how you would measure the speedup. 200–500 words.",
        word_limit: 600
      }
    ]
  },

  // ============================================================
  // HEAVY JUDGMENT
  // ============================================================
  heavy_judgment: {
    title: "Skills test — Heavy judgment",
    time_minutes: 35,
    intro: "Copy-edit, translation, qualitative research. Five short MC + two long-form editorial tasks + one AAO long-form question.",
    questions: [
      {
        id: "hj_1",
        kind: "mc",
        stem: "Which sentence best avoids the passive voice while keeping the meaning?",
        options: [
          "The credential was issued by the broker to the agent.",
          "The broker issued a credential to the agent.",
          "A credential is something that gets issued by the broker.",
          "The agent had a credential issued unto it."
        ]
        // answer: 1
      },
      {
        id: "hj_2",
        kind: "mc",
        stem: "Which clause is grammatically ambiguous and should be rewritten?",
        options: [
          "Visiting relatives can be tiring, the speaker noted.",
          "After the meeting ended, we walked back to the office.",
          "She prefers tea to coffee.",
          "The protocol verifies alignment without revealing the directive."
        ]
        // answer: 0
      },
      {
        id: "hj_3",
        kind: "mc",
        stem: "Choose the better translation of 'Hunt what you kill' for a Spanish-speaking technosocialism audience:",
        options: [
          "Caza lo que mates.",
          "Cazar lo que matas.",
          "Lo que matas, es tuyo.",
          "Mata lo que cazas."
        ]
        // answer: 0 (imperative + subjunctive)
      },
      {
        id: "hj_4",
        kind: "mc",
        stem: "Which of these is the strongest opening line for a technosocialism FAQ?",
        options: [
          "Technosocialism is a synthesis of capitalism and socialism designed for the era of autonomous AI organizations.",
          "Some people will not like this section.",
          "FAQ.",
          "We get this question a lot, but bear with us…"
        ]
        // answer: 0
      },
      {
        id: "hj_5",
        kind: "mc",
        stem: "Choose the better headline for a piece arguing that 80/20 revenue split is fairer than YC's 7% equity:",
        options: [
          "Some Reflections on the Comparative Equity Implications of YC and AAO Network Terms",
          "80% beats 7%: why the math is on the AAO Network's side",
          "Equity Discussion",
          "Read this if you care about founder economics"
        ]
        // answer: 1
      },
      {
        id: "hj_6",
        kind: "text",
        section: "Copy-edit",
        stem: "Edit this 200-word paragraph for clarity and tone. Keep the meaning. Improve sentence rhythm, remove redundancy, and replace any jargon with plain language. 'The optimization framework, which has been engineered through the iterative application of stakeholder feedback obtained via multifaceted consultation procedures, incorporates within its architectural substrate the capacity to dynamically reconfigure resource-allocation strategies in response to emergent demand signals. It should be additionally noted that this functionality is enabled by, and dependent upon, the prior provisioning of telemetry infrastructure that captures, with high temporal granularity, the operational characteristics of each downstream consumer of the framework's outputs. In point of fact, in the absence of said telemetry infrastructure, the optimization framework reverts to a less performant default-allocation modality wherein resources are distributed evenly across all consumers irrespective of their operational requirements.' Output the edited paragraph only.",
        word_limit: 220
      },
      {
        id: "hj_7",
        kind: "text",
        section: "Abstract",
        stem: "Write a 100-word abstract of the technosocialism manifesto. Cover: (1) the diagnosis (intern experience is broken); (2) the synthesis (socialism for the tools, capitalism for the kill); (3) the 80/20 split; (4) the rhetorical positioning (Dennis the Peasant). Do not exceed 120 words.",
        word_limit: 120
      },
      {
        id: "hj_aao",
        kind: "long",
        stem: "Pick one heavy-judgment workflow inside an AAO (copy-edit, translation, qualitative research). Describe what you would build, why it is the right next bet, and how you would measure success. 200–500 words.",
        word_limit: 600
      }
    ]
  },

  // ============================================================
  // SPECIALIZED
  // ============================================================
  specialized: {
    title: "Skills test — Specialized",
    time_minutes: 35,
    intro: "Code review, technical writing, design, prompt engineering. Five MC + two long-form + one AAO long-form question.",
    questions: [
      {
        id: "sp_1",
        kind: "mc",
        stem: "Which of the following has a real security issue, not just a style nitpick?",
        options: [
          "// TODO: implement caching",
          "const apiKey = req.headers['x-api-key']; if (apiKey == process.env.API_KEY) { /* allow */ }",
          "function add(a,b){return a+b}",
          "const items = [1,2,3].map(x => x*2);"
        ]
        // answer: 1 (== timing-leak; should be timing-safe compare)
      },
      {
        id: "sp_2",
        kind: "mc",
        stem: "You are reviewing a PR that adds 'eval(req.body.code)' to a Cloudflare Worker. The author argues it's safe because the endpoint is rate-limited and behind auth. The correct response is:",
        options: [
          "Approve. Rate limiting is a defense-in-depth measure.",
          "Approve, but ask for a comment explaining the trade-off.",
          "Block. Arbitrary code execution from request bodies is an unacceptable architectural choice regardless of rate-limit or auth.",
          "Approve conditional on a follow-up issue."
        ]
        // answer: 2
      },
      {
        id: "sp_3",
        kind: "mc",
        stem: "Which is the better instruction for a Claude Haiku system prompt that should score a free-text answer 0–1?",
        options: [
          "Score it well or poorly. Use your judgment.",
          "Return a single JSON object: {\"score\": <0..1>, \"rationale\": \"<short>\"}. Score 1.0 only if the answer contains [specific criteria]. Do not deviate from this JSON shape.",
          "Just give it a vibe score from 0 to 1.",
          "Be lenient because the user is nervous."
        ]
        // answer: 1
      },
      {
        id: "sp_4",
        kind: "mc",
        stem: "Which is the right SQL index for a D1 query 'SELECT * FROM applicants WHERE status = ? ORDER BY created_at DESC LIMIT 50'?",
        options: [
          "CREATE INDEX idx ON applicants(email)",
          "CREATE INDEX idx ON applicants(status, created_at DESC)",
          "CREATE INDEX idx ON applicants(created_at, status)",
          "No index needed — the table scan is fine."
        ]
        // answer: 1
      },
      {
        id: "sp_5",
        kind: "mc",
        stem: "You're designing a brutalist landing page with a single primary CTA. Which is the strongest hierarchy?",
        options: [
          "Five CTAs of equal weight, scattered through the page.",
          "One CTA above the fold, one repeated near the bottom, both visually identical. Everything else is text.",
          "A carousel of three CTAs that auto-rotates.",
          "A floating sticky CTA that follows the scroll plus a hero CTA plus three inline CTAs."
        ]
        // answer: 1
      },
      {
        id: "sp_6",
        kind: "text",
        stem: "Write a 1-paragraph code-review comment for a colleague who wants to merge a PR that adds raw `INNER JOIN` queries on user-supplied filter values without parameterization. Be direct, kind, and actionable. ≤120 words.",
        word_limit: 130
      },
      {
        id: "sp_7",
        kind: "text",
        stem: "You're writing the deploy section of a README. Write the 'Deploy to Cloudflare Pages + D1' section in 8–12 bullets, max 120 words, assuming the reader knows wrangler basics.",
        word_limit: 130
      },
      {
        id: "sp_aao",
        kind: "long",
        stem: "Pick one specialized-track contribution to an AAO: a code-review playbook, a prompt-engineering pattern library, a design system for brutalist AAO UIs, a technical writing style guide, or a developer-experience improvement. Describe what you would build, why it is the right next bet, and how you would measure success. 200–500 words.",
        word_limit: 600
      }
    ]
  },

  // ============================================================
  // DOMAIN EXPERT
  // ============================================================
  domain_expert: {
    title: "Skills test — Domain expert (legal / medical / finance)",
    time_minutes: 40,
    intro: "Pre-vetted track. Five MC across domains + one open-domain long-form + one AAO long-form question. We expect to manually verify credentials before any paid project.",
    questions: [
      {
        id: "de_1",
        kind: "mc",
        stem: "(Legal/contracts) An 'independent contractor' classification under US FLSA is jeopardized most by which factor?",
        options: [
          "The contractor uses their own equipment.",
          "The contractor sets their own hours.",
          "The hiring company has the right to control how the contractor performs the work, not just the result.",
          "The contractor invoices the company once per month."
        ]
        // answer: 2
      },
      {
        id: "de_2",
        kind: "mc",
        stem: "(Finance) A revenue-share agreement that gives the worker 80% of gross revenue and the platform 20% of gross revenue is closest in form to:",
        options: [
          "A SAFE",
          "An ISA (income share agreement) inverted to favor the worker",
          "A franchise royalty arrangement",
          "An employment contract with profit-sharing"
        ]
        // answer: 2
      },
      {
        id: "de_3",
        kind: "mc",
        stem: "(Medical / privacy) Under HIPAA, a transcriptionist working on PHI for a covered entity is:",
        options: [
          "Exempt from HIPAA because they are a contractor.",
          "A 'business associate' and must sign a BAA before any PHI is transmitted.",
          "Required to obtain individual patient consent for each record.",
          "Permitted to transmit PHI via unencrypted email so long as the entity authorizes it."
        ]
        // answer: 1
      },
      {
        id: "de_4",
        kind: "mc",
        stem: "(Cross-jurisdiction) A worker resident in the Philippines is paid in USDC for project work delivered to a US LLC. The most defensible 1099 reporting posture for the US LLC is:",
        options: [
          "Issue a 1099-NEC to the worker.",
          "Treat the worker as foreign person, collect a W-8BEN, withhold per treaty as applicable, and report on 1042-S if required.",
          "No reporting required because the worker is outside the US.",
          "Report the payment on a 1099-K through the USDC payment processor."
        ]
        // answer: 1
      },
      {
        id: "de_5",
        kind: "mc",
        stem: "(Ethics) An AI agent issuing credentials to other AI agents, with no human in the loop on each issuance, is most analogous to which existing legal construct?",
        options: [
          "A notary public.",
          "A power of attorney executing pre-authorized actions on behalf of a principal.",
          "A trust executing distributions per a written deed.",
          "An employee with general agency authority."
        ]
        // answer: 1
      },
      {
        id: "de_6",
        kind: "long",
        stem: "Open-domain. Pick your strongest domain (law, medicine, finance, accounting, regulatory affairs). Write 300–500 words on one specific risk that an AAO Network faces from your domain's regulators or standards bodies in the next 24 months — and one concrete mitigation we should adopt at v0.",
        word_limit: 600
      },
      {
        id: "de_aao",
        kind: "long",
        stem: "Pick one domain-expert workflow you could lead inside an AAO (legal review of contracts, medical-coding QA, financial reconciliation, compliance audit). Describe what you would build, why it is the right next bet, and how you would measure success. 200–500 words.",
        word_limit: 600
      }
    ]
  }
};
