// Hex / base64 / bigint conversion helpers, plus stable JSON.

export function bytesToHex(b: Uint8Array): string {
  let out = "";
  for (let i = 0; i < b.length; i++) {
    out += b[i]!.toString(16).padStart(2, "0");
  }
  return out;
}

export function hexToBytes(hex: string): Uint8Array {
  if (hex.length % 2 !== 0) throw new Error("hex string has odd length");
  const out = new Uint8Array(hex.length / 2);
  for (let i = 0; i < out.length; i++) {
    out[i] = parseInt(hex.substr(i * 2, 2), 16);
  }
  return out;
}

export function bytesToBase64(b: Uint8Array): string {
  let bin = "";
  for (let i = 0; i < b.length; i++) bin += String.fromCharCode(b[i]!);
  return btoa(bin);
}

export function base64ToBytes(b64: string): Uint8Array {
  const bin = atob(b64);
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}

export function bigintToHex(n: bigint): string {
  if (n < 0n) throw new Error("bigintToHex: negative");
  let h = n.toString(16);
  if (h.length % 2 !== 0) h = "0" + h;
  return h;
}

export function hexToBigint(hex: string): bigint {
  return BigInt("0x" + (hex.startsWith("0x") ? hex.slice(2) : hex));
}

// Deterministic canonical JSON: object keys sorted, no whitespace.
// Used as the pre-image for block hashes so anyone can recompute and verify.
export function canonicalJsonStringify(value: unknown): string {
  return stringify(value);
}

function stringify(v: unknown): string {
  if (v === null || typeof v !== "object") {
    return JSON.stringify(v);
  }
  if (Array.isArray(v)) {
    return "[" + v.map(stringify).join(",") + "]";
  }
  const keys = Object.keys(v as Record<string, unknown>).sort();
  const parts: string[] = [];
  for (const k of keys) {
    const sub = (v as Record<string, unknown>)[k];
    if (sub === undefined) continue;
    parts.push(JSON.stringify(k) + ":" + stringify(sub));
  }
  return "{" + parts.join(",") + "}";
}

export async function sha256Hex(input: string | Uint8Array): Promise<string> {
  const bytes =
    typeof input === "string" ? new TextEncoder().encode(input) : input;
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return bytesToHex(new Uint8Array(digest));
}
