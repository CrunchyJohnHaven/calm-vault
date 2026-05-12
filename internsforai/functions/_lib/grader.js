// Test grading. MC + text are graded deterministically; free-text rewrites
// (kind === "text") are graded by keyword presence; summaries / long-form
// are graded by Anthropic Claude Haiku.

import { clamp } from "./util.js";

// Deterministic answer keys + grading rubric per question id.
// kind: 'mc' answer_index | 'text' { keywords: [], min_words, max_words } | 'summary' { rubric } | 'long' { rubric }
export const KEYS = {

  // --- light_judgment ---
  lj_1: { kind: "mc", answer: 1, weight: 1 },
  lj_2: { kind: "mc", answer: 2, weight: 1 },
  lj_3: { kind: "mc", answer: 1, weight: 1 },
  lj_4: { kind: "mc", answer: 1, weight: 1 },
  lj_5: { kind: "mc", answer: 1, weight: 1 },
  lj_6: { kind: "mc", answer: 0, weight: 1 },
  lj_7: { kind: "text", weight: 1, keywords: ["does not", "do not", "doesn't", "doesnt", "not store", "no", "passwords", "plain text", "plaintext"], min_words: 5 },
  lj_8: { kind: "text", weight: 1, keywords: ["test", "auto-graded", "ai", "skills"], min_words: 6, max_words: 60 },
  lj_9: { kind: "summary", weight: 2, rubric: "An autonomous AI organization (AAO) is run by AI cofounder with shared infra; humans build via placement, keep 80%, network gets 20%; arbitration centralized on John in v0 (caveat).", min_words: 30, max_words: 65 },
  lj_10:{ kind: "summary", weight: 2, rubric: "Resend's 2026 deliverability up 11pp YoY due to automatic DKIM/SPF/DMARC alignment; 41% of new senders correctly provisioned in 1h vs 12% prior; DNS propagation lag is the remaining gap; pilot fallback subdomain cut abandonment 19% across 8400 sessions.", min_words: 30, max_words: 65 },
  lj_aao:{ kind: "long", weight: 3, rubric: "Propose a concrete feature for sameasyou.ai / SSS / IFA. Should name WHAT (concrete deliverable), WHY (clear value to network), and HOW to MEASURE success (1+ metric). 200-500 words. Reward thoughtfulness, penalize vagueness." },

  // --- mechanical ---
  m_1: { kind: "mc", answer: 0, weight: 1 },
  m_2: { kind: "mc", answer: 0, weight: 1 },
  m_3: { kind: "mc", answer: 2, weight: 1 },
  m_4: { kind: "mc", answer: 1, weight: 1 },
  m_5: { kind: "mc", answer: 2, weight: 1 },
  m_6: { kind: "text", weight: 1, keywords: ["123 mulberry", "apt 4b", "new york", "10013"], min_words: 4 },
  m_7: { kind: "text", weight: 1, keywords: ["jane smith", "31", "jane@example.com", "light_judgment", "mechanical"], min_words: 6 },
  m_aao: { kind: "long", weight: 3, rubric: "Concrete workflow for mechanical work + AI cofounder. WHAT/WHY/HOW-TO-MEASURE. 200-500 words." },

  // --- heavy_judgment ---
  hj_1: { kind: "mc", answer: 1, weight: 1 },
  hj_2: { kind: "mc", answer: 0, weight: 1 },
  hj_3: { kind: "mc", answer: 0, weight: 1 },
  hj_4: { kind: "mc", answer: 0, weight: 1 },
  hj_5: { kind: "mc", answer: 1, weight: 1 },
  hj_6: { kind: "summary", weight: 2, rubric: "200-word paragraph edited for clarity + tone; meaning preserved; jargon replaced; redundancy removed; sentence rhythm improved.", min_words: 100, max_words: 220 },
  hj_7: { kind: "summary", weight: 2, rubric: "100-word abstract of the technosocialism manifesto covering: (1) intern experience broken, (2) socialism for tools + capitalism for kill, (3) 80/20 split, (4) Dennis the Peasant rhetorical move.", min_words: 70, max_words: 120 },
  hj_aao: { kind: "long", weight: 3, rubric: "Concrete heavy-judgment workflow inside an AAO. WHAT/WHY/HOW-TO-MEASURE. 200-500 words." },

  // --- specialized ---
  sp_1: { kind: "mc", answer: 1, weight: 1 },
  sp_2: { kind: "mc", answer: 2, weight: 1 },
  sp_3: { kind: "mc", answer: 1, weight: 1 },
  sp_4: { kind: "mc", answer: 1, weight: 1 },
  sp_5: { kind: "mc", answer: 1, weight: 1 },
  sp_6: { kind: "summary", weight: 2, rubric: "Code-review comment for unparameterized JOINs. Direct, kind, actionable. Mentions parameterization / prepared statements / SQL injection risk. <=120 words.", min_words: 30, max_words: 140 },
  sp_7: { kind: "summary", weight: 2, rubric: "README deploy section for Cloudflare Pages + D1. 8-12 bullets. Covers: create D1, run migrations, configure wrangler, pages secret put, deploy via pages publish or git push, smoke test. <=120 words.", min_words: 60, max_words: 160 },
  sp_aao: { kind: "long", weight: 3, rubric: "Concrete specialized contribution to an AAO. WHAT/WHY/HOW-TO-MEASURE. 200-500 words." },

  // --- domain_expert ---
  de_1: { kind: "mc", answer: 2, weight: 1 },
  de_2: { kind: "mc", answer: 2, weight: 1 },
  de_3: { kind: "mc", answer: 1, weight: 1 },
  de_4: { kind: "mc", answer: 1, weight: 1 },
  de_5: { kind: "mc", answer: 1, weight: 1 },
  de_6: { kind: "long", weight: 3, rubric: "Concrete regulatory / standards risk to an AAO Network in the next 24 months + one v0 mitigation. Must name the domain (law/medicine/finance/etc), specific risk, specific mitigation. 300-500 words." },
  de_aao: { kind: "long", weight: 3, rubric: "Concrete domain-expert workflow inside an AAO. WHAT/WHY/HOW-TO-MEASURE. 200-500 words." }
};

export async function gradeAttempt(env, track, answers) {
  // load track-specific keys
  const trackPrefixes = {
    light_judgment: "lj_",
    mechanical: "m_",
    heavy_judgment: "hj_",
    specialized: "sp_",
    domain_expert: "de_"
  };
  const prefix = trackPrefixes[track];
  if (!prefix) throw new Error("Unknown track: " + track);

  const qids = Object.keys(KEYS).filter(k => k.startsWith(prefix));
  let mcAchieved = 0, mcMax = 0, textAchieved = 0, textMax = 0, aiAchieved = 0, aiMax = 0;
  const per = [];

  const aiQueue = [];

  for (const qid of qids) {
    const key = KEYS[qid];
    const ans = answers[qid];
    const slot = { qid, kind: key.kind, weight: key.weight, score: 0, note: "" };
    if (key.kind === "mc") {
      mcMax += key.weight;
      if (Number(ans) === key.answer) {
        slot.score = 1;
        mcAchieved += key.weight;
        slot.note = "correct";
      } else {
        slot.note = ans == null ? "no answer" : ("chose " + ans + ", correct " + key.answer);
      }
    } else if (key.kind === "text") {
      textMax += key.weight;
      const s = (typeof ans === "string" ? ans : "").trim().toLowerCase();
      const words = s ? s.split(/\s+/).filter(Boolean).length : 0;
      let frac = 0;
      if (s) {
        const hits = key.keywords.filter(k => s.includes(k.toLowerCase()));
        frac = hits.length / key.keywords.length;
        slot.note = "kw hits " + hits.length + "/" + key.keywords.length + " · " + words + " words";
        if (key.min_words && words < key.min_words) { frac *= 0.5; slot.note += " · below min_words"; }
        if (key.max_words && words > key.max_words) { frac *= 0.8; slot.note += " · over max_words"; }
      } else {
        slot.note = "no answer";
      }
      slot.score = frac;
      textAchieved += frac * key.weight;
    } else if (key.kind === "summary" || key.kind === "long") {
      aiMax += key.weight;
      aiQueue.push({ qid, key, answer: (typeof ans === "string" ? ans : "").trim() });
      slot.note = "queued for AI grading";
      slot.score = 0; // filled in below
      per.push(slot);
      continue;
    }
    per.push(slot);
  }

  // AI grading (1 prompt per AI-graded question, in parallel).
  if (aiQueue.length > 0) {
    const aiResults = await Promise.all(aiQueue.map(item => gradeWithClaude(env, item)));
    aiQueue.forEach((item, idx) => {
      const slot = per.find(p => p.qid === item.qid);
      const r = aiResults[idx];
      slot.score = clamp(Number(r.score) || 0, 0, 1);
      slot.note = r.rationale || "(no rationale)";
      aiAchieved += slot.score * item.key.weight;
    });
  }

  const mc_score   = mcMax   > 0 ? mcAchieved   / mcMax   : 0;
  const text_score = textMax > 0 ? textAchieved / textMax : 0;
  const ai_score   = aiMax   > 0 ? aiAchieved   / aiMax   : 0;

  // Composite: deterministic weights (mc 35%, text 20%, ai 45%).
  const composite = clamp(100 * (0.35 * mc_score + 0.20 * text_score + 0.45 * ai_score), 0, 100);

  let verdict;
  if (composite >= 70) verdict = "PASS";
  else if (composite >= 50) verdict = "SHORTLIST";
  else verdict = "FAIL";

  // 1-sentence rationale aggregate for John.
  const ai_feedback =
    "MC " + (mc_score * 100).toFixed(0) + "% · text " + (text_score * 100).toFixed(0) + "% · AI " + (ai_score * 100).toFixed(0) +
    "% · composite " + composite.toFixed(1) + " → " + verdict;

  return { mc_score, text_score, ai_score, composite, verdict, per_question: per, ai_feedback };
}

// Single-question Claude Haiku grader. Returns { score: 0..1, rationale: string }.
// Never throws — failures degrade to a fair-middle 0.5 with the error in rationale.
export async function gradeWithClaude(env, { qid, key, answer }) {
  if (!answer) return { score: 0, rationale: "No answer." };
  if (!env.ANTHROPIC_API_KEY) {
    // Local-dev fallback: length-based heuristic.
    const words = answer.split(/\s+/).filter(Boolean).length;
    const target = (key.min_words || 30) + 20;
    return { score: Math.min(1, words / target) * 0.7, rationale: "(no ANTHROPIC_API_KEY; heuristic length score " + words + " words)" };
  }
  const model = env.ANTHROPIC_MODEL || "claude-3-5-haiku-latest";
  const sys =
    "You are grading a 30-minute skills test for InternsForAI, a placement firm for autonomous AI organizations. " +
    "Return strict JSON: {\"score\": <number 0..1>, \"rationale\": \"<one sentence, ≤30 words>\"}. " +
    "Score 0 only if the answer is missing, off-topic, or clearly low-effort. " +
    "Score 1.0 only if the answer fully meets the rubric. " +
    "Score 0.6 for a serviceable answer that misses one criterion. " +
    "Be strict but fair. Be brief in the rationale.";
  const user =
    "Rubric for question " + qid + ":\n" + key.rubric + "\n\n" +
    "Candidate answer:\n---\n" + answer + "\n---\n\n" +
    "Return strict JSON. No prose outside the JSON.";

  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "x-api-key": env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
      },
      body: JSON.stringify({
        model,
        max_tokens: 256,
        temperature: 0,
        system: sys,
        messages: [{ role: "user", content: user }]
      })
    });
    if (!r.ok) {
      const t = await r.text().catch(() => "");
      return { score: 0.5, rationale: "Anthropic " + r.status + " " + t.slice(0, 80) };
    }
    const j = await r.json();
    const text = (j.content || []).map(c => c.text || "").join("");
    // Extract the first JSON object in the response.
    const m = text.match(/\{[\s\S]*\}/);
    if (!m) return { score: 0.5, rationale: "Could not parse grader output." };
    const parsed = JSON.parse(m[0]);
    return {
      score: clamp(Number(parsed.score) || 0, 0, 1),
      rationale: typeof parsed.rationale === "string" ? parsed.rationale : ""
    };
  } catch (e) {
    return { score: 0.5, rationale: "Grader error: " + String(e).slice(0, 80) };
  }
}
