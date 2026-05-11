/**
 * POST /api/reviewer/submit
 *
 * Takes a reviewer's edited markdown/HTML and opens a PR against main on
 * CrunchyJohnHaven/calm-vault. The PR is never auto-merged; the function
 * verifies auto_merge is OFF before returning.
 *
 * Env vars:
 *   GITHUB_PR_BOT_TOKEN — required at runtime. Must have `repo` scope (or
 *                          fine-grained Contents + Pull requests + Metadata on
 *                          this repo). Never logged in plaintext.
 */
import type { VercelRequest, VercelResponse } from "@vercel/node";
import { Octokit } from "@octokit/rest";
import { createTwoFilesPatch } from "diff";
import { ALLOWED_FILES, PR_TARGET, isAllowedPath } from "./_allowed.js";
import {
  BadInputError,
  basenameNoExt,
  checkRateLimit,
  clientIp,
  loadGitHubToken,
  slugifyReviewer,
  validateContact,
  validateEdited,
  validateOriginalFilePath,
  validateReviewerName,
  validateSummary,
  wordCount,
} from "./_util.js";

interface SubmitBody {
  reviewer?: unknown;
  original_file?: unknown;
  edited?: unknown;
  summary?: unknown;
  contact?: unknown;
}

export default async function handler(
  req: VercelRequest,
  res: VercelResponse,
): Promise<void> {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    res.status(405).json({ ok: false, error: "method not allowed" });
    return;
  }

  // 0. Rate limit (10/hour/IP, in-memory per instance).
  const ip = clientIp(req);
  const rl = checkRateLimit(ip);
  res.setHeader("X-RateLimit-Limit", "10");
  res.setHeader("X-RateLimit-Remaining", String(rl.remaining));
  res.setHeader("X-RateLimit-Reset", String(Math.floor(rl.resetAt / 1000)));
  if (!rl.allowed) {
    res
      .status(429)
      .json({ ok: false, error: "rate limit exceeded; try again later" });
    return;
  }

  // 1. Validate input.
  let reviewer: string;
  let originalFile: string;
  let edited: string;
  let summary: string;
  let contact: string | undefined;
  try {
    const body = parseBody(req.body) as SubmitBody;
    reviewer = validateReviewerName(body.reviewer);
    originalFile = validateOriginalFilePath(body.original_file, isAllowedPath);
    edited = validateEdited(body.edited);
    summary = validateSummary(body.summary);
    contact = validateContact(body.contact);
  } catch (err) {
    if (err instanceof BadInputError) {
      res.status(400).json({ ok: false, error: err.message });
      return;
    }
    if (err instanceof SyntaxError) {
      res.status(400).json({ ok: false, error: "invalid JSON body" });
      return;
    }
    throw err;
  }

  // 2. Load token (never logs the value).
  const { token, status } = loadGitHubToken();
  console.log(`[reviewer/submit] github token ${status}`);
  if (!token) {
    res.status(500).json({
      ok: false,
      error: "server misconfigured: GITHUB_PR_BOT_TOKEN env var is missing",
    });
    return;
  }

  const octokit = new Octokit({ auth: token });
  const { owner, repo, base } = PR_TARGET;

  try {
    // 3. Fetch the file at HEAD of base. We need the sha for updates.
    const original = await octokit.repos.getContent({
      owner,
      repo,
      path: originalFile,
      ref: base,
    });

    if (Array.isArray(original.data) || original.data.type !== "file") {
      res
        .status(400)
        .json({ ok: false, error: "original_file is not a file blob" });
      return;
    }
    const sha = original.data.sha;
    const originalContent = Buffer.from(
      original.data.content,
      original.data.encoding as BufferEncoding,
    ).toString("utf8");

    // 4. Detect "no changes".
    if (normalize(originalContent) === normalize(edited)) {
      res.status(400).json({ ok: false, error: "no changes detected" });
      return;
    }

    // 5. Create a fresh branch off base.
    const baseRef = await octokit.git.getRef({
      owner,
      repo,
      ref: `heads/${base}`,
    });
    const baseSha = baseRef.data.object.sha;
    // Millisecond timestamp + 6-char nonce so two submissions in the same
    // second from the same reviewer to the same file can't collide on createRef.
    const ts = Date.now();
    const nonce = Math.random().toString(36).slice(2, 8);
    const branch = `reviewer/${slugifyReviewer(reviewer)}/${basenameNoExt(originalFile)}-${ts}-${nonce}`;
    await octokit.git.createRef({
      owner,
      repo,
      ref: `refs/heads/${branch}`,
      sha: baseSha,
    });

    // 6. Commit the edited content to the new branch.
    const commitMessage = `[reviewer-pass] ${basenameNoExt(originalFile)} — ${summary}`;
    await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path: originalFile,
      message: commitMessage,
      content: Buffer.from(edited, "utf8").toString("base64"),
      sha,
      branch,
      committer: {
        name: "calm-vault reviewer bot",
        email: "noreply@sameasyou.ai",
      },
      author: {
        name: `reviewer:${reviewer}`,
        email: contact ?? "noreply@sameasyou.ai",
      },
    });

    // 7. Compute a small diff preview for the PR body.
    const patch = createTwoFilesPatch(
      `a/${originalFile}`,
      `b/${originalFile}`,
      originalContent,
      edited,
      "before",
      "after",
      { context: 3 },
    );
    const diffPreview = trimDiff(patch, 6000);

    // 8. Open the PR.
    const originalWords = wordCount(originalContent);
    const editedWords = wordCount(edited);
    const wordDelta = editedWords - originalWords;
    const charDelta = edited.length - originalContent.length;

    const title = `[reviewer-pass] ${basenameNoExt(originalFile)} — ${summary}`;
    const body = renderPrBody({
      reviewer,
      contact,
      originalFile,
      originalWords,
      editedWords,
      wordDelta,
      charDelta,
      summary,
      diffPreview,
    });

    const pr = await octokit.pulls.create({
      owner,
      repo,
      head: branch,
      base,
      title,
      body,
      maintainer_can_modify: true,
      draft: false,
    });

    // 9. Confirm auto-merge is OFF (the create call above does not enable it,
    //    but the brief asks for an explicit verification via the PR API).
    const verify = await octokit.pulls.get({
      owner,
      repo,
      pull_number: pr.data.number,
    });
    if (verify.data.auto_merge != null) {
      console.warn(
        `[reviewer/submit] WARNING auto_merge is set on PR #${pr.data.number}; disabling`,
      );
      // No REST endpoint exists for disabling auto-merge — GitHub only exposes
      // the GraphQL `disablePullRequestAutoMerge` mutation.
      try {
        await octokit.graphql(
          `mutation DisableAutoMerge($pullRequestId: ID!) {
            disablePullRequestAutoMerge(input: { pullRequestId: $pullRequestId }) {
              pullRequest { number }
            }
          }`,
          { pullRequestId: verify.data.node_id },
        );
      } catch (e) {
        const msg = e instanceof Error ? e.message : String(e);
        console.warn(
          `[reviewer/submit] could not disable auto_merge on PR #${pr.data.number}: ${msg}`,
        );
      }
    }

    // Brief calls for a row in lab/labor/REGISTRY.md via a worker. That file
    // lives outside this repo, so log a warning and continue rather than
    // failing the submission.
    console.warn(
      `[reviewer/submit] REGISTRY row not appended (registry is out-of-repo); pr=${pr.data.html_url}`,
    );

    res.status(200).json({
      ok: true,
      pr_url: pr.data.html_url,
      pr_number: pr.data.number,
      branch,
      auto_merge: false,
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    // GitHub errors that came back with a status (octokit) — surface a clean 4xx/5xx.
    const status = isErrorWithStatus(err) ? err.status : 500;
    console.error(`[reviewer/submit] error status=${status} message=${message}`);
    res.status(status >= 400 && status < 600 ? status : 500).json({
      ok: false,
      error: message,
    });
  }
}

/* -------------------------------------------------------------------------- */

function parseBody(body: unknown): unknown {
  if (body == null) throw new BadInputError("missing request body");
  if (typeof body === "string") return JSON.parse(body);
  return body;
}

function normalize(s: string): string {
  // Treat trailing whitespace/newline-only changes as identical.
  return s.replace(/\r\n/g, "\n").replace(/[ \t]+\n/g, "\n").replace(/\s+$/g, "");
}

function trimDiff(patch: string, max: number): string {
  if (patch.length <= max) return patch;
  return patch.slice(0, max) + "\n... (truncated)\n";
}

function isErrorWithStatus(e: unknown): e is { status: number } {
  return (
    typeof e === "object" &&
    e !== null &&
    "status" in e &&
    typeof (e as { status: unknown }).status === "number"
  );
}

interface PrBodyArgs {
  reviewer: string;
  contact: string | undefined;
  originalFile: string;
  originalWords: number;
  editedWords: number;
  wordDelta: number;
  charDelta: number;
  summary: string;
  diffPreview: string;
}

function renderPrBody(a: PrBodyArgs): string {
  const fileLabel =
    ALLOWED_FILES.find((f) => f.path === a.originalFile)?.label ??
    a.originalFile;
  const contactLine = a.contact
    ? `**Contact:** ${a.contact}`
    : "**Contact:** _(none provided)_";
  const deltaSign = (n: number) => (n >= 0 ? `+${n}` : `${n}`);

  return [
    `Reviewer-submitted edit via https://sameasyou.ai/reviewer/submit.`,
    ``,
    `**Reviewer:** ${a.reviewer}`,
    contactLine,
    `**File:** \`${a.originalFile}\` (${fileLabel})`,
    ``,
    `**Summary:** ${a.summary}`,
    ``,
    `**Stats**`,
    `- words: ${a.originalWords} → ${a.editedWords} (${deltaSign(a.wordDelta)})`,
    `- chars: ${deltaSign(a.charDelta)}`,
    ``,
    `**Accept / reject checklist**`,
    `- [ ] Edits preserve factual accuracy (dates, names, claims).`,
    `- [ ] Tone matches the rest of the document.`,
    `- [ ] No new external links to untrusted sources.`,
    `- [ ] No accidental deletion of authorship / attribution.`,
    `- [ ] Word delta is appropriate for the stated summary.`,
    ``,
    `**Diff preview**`,
    "```diff",
    a.diffPreview.trim(),
    "```",
    ``,
    `_This PR was opened automatically and **never auto-merges**. A human merges or closes it._`,
  ].join("\n");
}
