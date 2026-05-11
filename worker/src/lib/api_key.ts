// API-key generation + hashing.

import { bytesToHex, sha256Hex } from "./hex";

// 32 hex characters = 16 random bytes = 128 bits of entropy.
export function generateApiKey(): string {
  const buf = new Uint8Array(16);
  crypto.getRandomValues(buf);
  return bytesToHex(buf);
}

export function apiKeyHash(apiKey: string): Promise<string> {
  return sha256Hex(apiKey);
}
