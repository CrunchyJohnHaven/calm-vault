// Tiny JSON-response + error-shape helpers.

export const CORS_HEADERS: Record<string, string> = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
  "Access-Control-Max-Age": "86400",
};

export function jsonResponse(
  body: unknown,
  status = 200,
  extraHeaders: Record<string, string> = {},
): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      ...CORS_HEADERS,
      ...extraHeaders,
    },
  });
}

export function errorResponse(
  status: number,
  code: string,
  message: string,
): Response {
  return jsonResponse({ error: { code, message } }, status);
}

export function htmlResponse(html: string, status = 200): Response {
  return new Response(html, {
    status,
    headers: {
      "Content-Type": "text/html; charset=utf-8",
      ...CORS_HEADERS,
    },
  });
}

export async function readJson<T>(request: Request): Promise<T> {
  try {
    return (await request.json()) as T;
  } catch {
    throw new HttpError(400, "invalid_json", "Request body is not valid JSON.");
  }
}

export class HttpError extends Error {
  constructor(
    public readonly status: number,
    public readonly code: string,
    message: string,
  ) {
    super(message);
  }
}

export function requireString(
  v: unknown,
  field: string,
  opts: { maxLen?: number; minLen?: number } = {},
): string {
  if (typeof v !== "string") {
    throw new HttpError(
      400,
      "invalid_field",
      `Field '${field}' must be a string.`,
    );
  }
  const trimmed = v.trim();
  const min = opts.minLen ?? 1;
  if (trimmed.length < min) {
    throw new HttpError(
      400,
      "invalid_field",
      `Field '${field}' must be at least ${min} character(s).`,
    );
  }
  const max = opts.maxLen ?? 1024;
  if (trimmed.length > max) {
    throw new HttpError(
      400,
      "invalid_field",
      `Field '${field}' must be at most ${max} characters.`,
    );
  }
  return trimmed;
}
