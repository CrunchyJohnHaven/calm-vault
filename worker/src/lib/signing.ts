// Server-side Ed25519 signing for /verify metadata.
//
// On first use the Worker lazily generates an Ed25519 keypair via Web Crypto
// and persists it in the signing_keys D1 table. Subsequent requests reuse it.
// The public key is exposed at /verify/keys so any peer agent can verify
// signed metadata returned from /verify/{org_id}.

import type { Env } from "../env";
import { base64ToBytes, bytesToBase64 } from "./hex";

const KEY_ID = "primary";

interface KeyRow {
  algorithm: string;
  private_key_b64: string;
  public_key_b64: string;
}

let _cached: { priv: CryptoKey; pubB64: string } | null = null;

export async function getSigningKey(
  env: Env,
): Promise<{ priv: CryptoKey; pubB64: string }> {
  if (_cached) return _cached;
  const row = await env.DB.prepare(
    "SELECT algorithm, private_key_b64, public_key_b64 FROM signing_keys WHERE id = ?",
  )
    .bind(KEY_ID)
    .first<KeyRow>();
  if (row) {
    const priv = await crypto.subtle.importKey(
      "pkcs8",
      base64ToBytes(row.private_key_b64),
      { name: "Ed25519" },
      false,
      ["sign"],
    );
    _cached = { priv, pubB64: row.public_key_b64 };
    return _cached;
  }
  // Generate a fresh keypair.
  const pair = (await crypto.subtle.generateKey(
    { name: "Ed25519" },
    true,
    ["sign", "verify"],
  )) as CryptoKeyPair;
  const privPkcs8 = new Uint8Array(
    (await crypto.subtle.exportKey("pkcs8", pair.privateKey)) as ArrayBuffer,
  );
  const pubRaw = new Uint8Array(
    (await crypto.subtle.exportKey("raw", pair.publicKey)) as ArrayBuffer,
  );
  const privB64 = bytesToBase64(privPkcs8);
  const pubB64 = bytesToBase64(pubRaw);
  // INSERT OR IGNORE handles the race where two requests both try to
  // generate the key on a cold start.
  await env.DB.prepare(
    `INSERT OR IGNORE INTO signing_keys (id, algorithm, private_key_b64, public_key_b64, created_at)
     VALUES (?, 'Ed25519', ?, ?, ?)`,
  )
    .bind(KEY_ID, privB64, pubB64, Math.floor(Date.now() / 1000))
    .run();
  // Re-read so we pick up whichever request won the INSERT.
  const winner = await env.DB.prepare(
    "SELECT algorithm, private_key_b64, public_key_b64 FROM signing_keys WHERE id = ?",
  )
    .bind(KEY_ID)
    .first<KeyRow>();
  const winnerPriv = await crypto.subtle.importKey(
    "pkcs8",
    base64ToBytes(winner!.private_key_b64),
    { name: "Ed25519" },
    false,
    ["sign"],
  );
  _cached = { priv: winnerPriv, pubB64: winner!.public_key_b64 };
  return _cached;
}

export async function signCanonical(
  env: Env,
  canonical: string,
): Promise<string> {
  const { priv } = await getSigningKey(env);
  const sig = await crypto.subtle.sign(
    "Ed25519",
    priv,
    new TextEncoder().encode(canonical),
  );
  return bytesToBase64(new Uint8Array(sig));
}

export async function getPublicKeyB64(env: Env): Promise<string> {
  const { pubB64 } = await getSigningKey(env);
  return pubB64;
}

// Test-only: reset the in-memory cache (vitest reuses module state across tests).
export function _resetSigningCache(): void {
  _cached = null;
}
