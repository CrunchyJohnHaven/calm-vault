// Local smoke test for the grader. No Cloudflare, no D1, no API key required.
// Asserts that a "good" answer set scores higher than a "bad" answer set
// across all 5 tracks, and that the verdict logic is monotonic.

import { gradeAttempt } from "../functions/_lib/grader.js";

const FAKE_ENV = {}; // no ANTHROPIC_API_KEY → grader falls back to length heuristic

function badAnswers(prefix, count) {
  const out = {};
  for (let i = 1; i <= count; i++) out[prefix + i] = null;
  return out;
}

function check(name, cond) {
  console.log((cond ? "ok    " : "FAIL  ") + name);
  if (!cond) process.exitCode = 1;
}

// ----- LIGHT JUDGMENT -----
const goodLJ = {
  lj_1: 1, lj_2: 2, lj_3: 1, lj_4: 1, lj_5: 1, lj_6: 0,
  lj_7: "The system does not store passwords in plain text.",
  lj_8: "The 30-minute test is auto-graded by an AI.",
  lj_9: "An autonomous AI organization runs without a human boss; humans build for 80% revenue; 20% goes to the network; v0 centralizes arbitration on John as a known weakness.",
  lj_10: "Resend deliverability up 11pp YoY due to automatic DKIM/SPF/DMARC alignment; 41% of new senders correctly provisioned in 1h vs 12% prior; DNS propagation lag remains; fallback subdomain cut abandonment 19%.",
  lj_aao: "I would build a permissionless attestation viewer for AAL Component 3 — a public feed of signed test passes + project completions. WHAT: a static-site reader plus signature-verification CLI. WHY: external parties currently have no easy way to grade the AAO Network without trusting the operator. HOW TO MEASURE: number of third-party AAOs that adopt attestation-signed reputation in 90 days; number of unique signature verifications per week. This converts our reputation graph from operator-claimed to externally-verifiable, which is the load-bearing claim of the entire AAL stack."
};
const badLJ = badAnswers("lj_", 10);

const r1 = await gradeAttempt(FAKE_ENV, "light_judgment", goodLJ);
const r2 = await gradeAttempt(FAKE_ENV, "light_judgment", badLJ);
check("LJ good > bad composite (" + r1.composite.toFixed(1) + " > " + r2.composite.toFixed(1) + ")", r1.composite > r2.composite);
check("LJ good verdict not FAIL (" + r1.verdict + ")", r1.verdict !== "FAIL");
check("LJ bad verdict FAIL", r2.verdict === "FAIL");

// ----- MECHANICAL -----
const goodM = {
  m_1: 0, m_2: 0, m_3: 2, m_4: 1, m_5: 2,
  m_6: "123 Mulberry St., Apt 4B, New York, NY 10013",
  m_7: '{"name":"Jane Smith","age":31,"email":"jane@example.com","projects":["light_judgment","mechanical"]}',
  m_aao: "I would build a screenshot→structured-CSV pipeline using GPT-4o vision + a careful human reviewer. WHAT: a queue of receipts/invoices/forms is OCRed; the AI proposes fields; the human approves or corrects in a 3-second-per-record UI. WHY: typical OCR has 95% per-field accuracy which is unusable at scale; the AI+human combo gets 99.5%+. HOW TO MEASURE: per-record throughput (target 60/hr per human) and per-field accuracy on a hold-out set (target 99.5%). This is the unsexy mechanical work the network needs done."
};
const badM = badAnswers("m_", 7);
const r3 = await gradeAttempt(FAKE_ENV, "mechanical", goodM);
const r4 = await gradeAttempt(FAKE_ENV, "mechanical", badM);
check("Mech good > bad composite (" + r3.composite.toFixed(1) + " > " + r4.composite.toFixed(1) + ")", r3.composite > r4.composite);
check("Mech bad verdict FAIL", r4.verdict === "FAIL");

// ----- HEAVY JUDGMENT -----
const goodHJ = {
  hj_1: 1, hj_2: 0, hj_3: 0, hj_4: 0, hj_5: 1,
  hj_6: "We refined the optimization framework through stakeholder feedback. It can dynamically rebalance resource allocation in response to demand signals — but only when fine-grained telemetry is in place. Without that telemetry, it falls back to a flat, even allocation across all consumers, ignoring their actual operational needs.",
  hj_7: "The intern experience is broken: bad work, bad bosses, no ownership. Technosocialism inverts this — collective ownership of infrastructure (hosting, AI APIs, brand, attestation layer) and individual ownership of revenue. Workers placed at autonomous AI organizations keep 80% of project revenue; 20% goes back to the network. The mascot is Dennis the Peasant from Monty Python, who acknowledges the project takes itself seriously without becoming humorless.",
  hj_aao: "I would build a translation-pair QA dashboard for sameasyou.ai. WHAT: side-by-side display of EN source + target-language translation + auto-detected divergences + human-correctable annotations. WHY: translation is the cheapest way to widen the AAO Network's reach into non-English markets, but quality is currently uncalibrated. HOW TO MEASURE: BLEU score improvement over baseline DeepL, plus a 'translator-confidence' field that's correlated 70%+ with downstream user complaints. Ship to one language pair first; expand if the correlation holds."
};
const r5 = await gradeAttempt(FAKE_ENV, "heavy_judgment", goodHJ);
check("HJ good composite >= 50 (" + r5.composite.toFixed(1) + ")", r5.composite >= 50);

console.log("\nDone. Smoke test summary:");
console.log("  Light judgment good:  " + r1.composite.toFixed(1) + " → " + r1.verdict);
console.log("  Light judgment bad:   " + r2.composite.toFixed(1) + " → " + r2.verdict);
console.log("  Mechanical good:      " + r3.composite.toFixed(1) + " → " + r3.verdict);
console.log("  Mechanical bad:       " + r4.composite.toFixed(1) + " → " + r4.verdict);
console.log("  Heavy-judg good:      " + r5.composite.toFixed(1) + " → " + r5.verdict);
