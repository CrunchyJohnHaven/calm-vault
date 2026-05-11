/**
 * Reviewer auto-PR allowlist.
 *
 * Only files in this list can be edited via the public /reviewer/submit form.
 * Adding a file here makes it editable by anonymous reviewers; remove anything
 * that should not be reviewable in public.
 *
 * Paths are repo-relative, forward-slash, and never start with `/`.
 */
export const ALLOWED_FILES: ReadonlyArray<{
  path: string;
  label: string;
  kind: "markdown" | "html";
}> = [
  { path: "CALM_PACT_PROTOCOL_v0.md", label: "CALM Pact Protocol v0", kind: "markdown" },
  { path: "ANNALS.md", label: "Annals", kind: "markdown" },
  { path: "BOOK_TITLE.md", label: "Book title", kind: "markdown" },
  { path: "README.md", label: "Project README", kind: "markdown" },
  {
    path: "paper/bradley-gavini-protocol-v0.html",
    label: "Paper — Bradley-Gavini Protocol v0 (HTML)",
    kind: "html",
  },
  { path: "landing/index.html", label: "Landing — sameasyou.ai", kind: "html" },
  { path: "landing-sss/index.html", label: "Landing — SSS", kind: "html" },
];

const ALLOWED_PATH_SET = new Set(ALLOWED_FILES.map((f) => f.path));

export function isAllowedPath(p: string): boolean {
  return ALLOWED_PATH_SET.has(p);
}

export const PR_TARGET = {
  owner: "CrunchyJohnHaven",
  repo: "calm-vault",
  base: "main",
} as const;
