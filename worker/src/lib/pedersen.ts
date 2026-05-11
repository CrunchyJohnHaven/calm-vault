// Pedersen commitments on the RFC 3526 Group 14 (2048-bit MODP).
//
// Direct TypeScript port of calm_pact/protocol.py — the reference implementation
// of the Bradley-Gavini Protocol. Two parties commit to a maxim, exchange
// commitments, and (via a separate equality-proof step) verify they share the
// same underlying mandate without revealing it.
//
//   C = G^s · H^r   (mod P)
//
// where s = SHA-256(mandate) mod Q is the scalar form of the mandate and
// r ∈ [1, Q-1] is a per-commitment blinding factor.
//
// G is the standard generator; H is derived from a public seed via a
// Nothing-Up-My-Sleeve construction so no party knows log_G(H), which is the
// condition for the binding property.
//
// Performance: pure-JS BigInt modular exponentiation on a 2048-bit modulus is
// ~5–30 ms per commitment on a Workers CPU, comparable to the Python reference.

import { hexToBigint, bigintToHex } from "./hex";

// RFC 3526 Group 14 — Sophie Germain safe prime, P = 2*Q + 1.
export const P = BigInt(
  "0x" +
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1" +
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD" +
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245" +
    "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED" +
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D" +
    "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F" +
    "83655D23DCA3AD961C62F356208552BB9ED529077096966D" +
    "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B" +
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9" +
    "DE2BCBF6955817183995497CEA956AE515D2261898FA0510" +
    "15728E5A8AACAA68FFFFFFFFFFFFFFFF",
);

export const Q = (P - 1n) / 2n;
export const G = 2n;

// modular exponentiation: base^exp mod mod, with a square-and-multiply loop.
export function modPow(base: bigint, exp: bigint, mod: bigint): bigint {
  if (mod === 1n) return 0n;
  let result = 1n;
  let b = base % mod;
  if (b < 0n) b += mod;
  let e = exp;
  while (e > 0n) {
    if (e & 1n) result = (result * b) % mod;
    e >>= 1n;
    b = (b * b) % mod;
  }
  return result;
}

// Fermat-inverse for our prime modulus P.
export function modInverseP(a: bigint): bigint {
  return modPow(a, P - 2n, P);
}

// Derive H via NUMS from a public seed — mirror of _derive_h_nums() in Python.
async function deriveHNums(): Promise<bigint> {
  const seed = new TextEncoder().encode("calm-pact-h-nums-v0|RFC3526-group14");
  let counter = 0n;
  // The Python loop never realistically iterates more than once or twice; we cap
  // at 1024 attempts for safety.
  for (let i = 0; i < 1024; i++) {
    const cBuf = new Uint8Array(8);
    let cv = counter;
    for (let j = 7; j >= 0; j--) {
      cBuf[j] = Number(cv & 0xffn);
      cv >>= 8n;
    }
    const input = new Uint8Array(seed.length + cBuf.length);
    input.set(seed, 0);
    input.set(cBuf, seed.length);
    const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", input));
    // big-endian
    let candidate = 0n;
    for (const b of digest) candidate = (candidate << 8n) | BigInt(b);
    candidate = candidate % P;
    if (candidate < 2n) {
      counter += 1n;
      continue;
    }
    const hCandidate = modPow(candidate, 2n, P);
    if (hCandidate !== 1n && modPow(hCandidate, Q, P) === 1n) {
      return hCandidate;
    }
    counter += 1n;
  }
  throw new Error("deriveHNums: exhausted attempts (should not happen)");
}

let _H: bigint | null = null;
export async function getH(): Promise<bigint> {
  if (_H !== null) return _H;
  _H = await deriveHNums();
  return _H;
}

// Mandate string -> scalar in [1, Q-1].
export async function maximToScalar(maxim: string): Promise<bigint> {
  const bytes = new TextEncoder().encode("calm-pact-maxim-v0|" + maxim);
  const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", bytes));
  let scalar = 0n;
  for (const b of digest) scalar = (scalar << 8n) | BigInt(b);
  scalar = scalar % Q;
  if (scalar === 0n) scalar = 1n;
  return scalar;
}

// Cryptographically-random integer in [1, Q-1], sampled uniformly via
// rejection on the 2048-bit space. We treat the 256-byte draw as a uniform
// element of [0, 2^2048) and reject anything outside [1, Q).
function randomBelowQ(): bigint {
  while (true) {
    const buf = new Uint8Array(256);
    crypto.getRandomValues(buf);
    let n = 0n;
    for (const b of buf) n = (n << 8n) | BigInt(b);
    if (n === 0n || n >= Q) continue;
    return n;
  }
}

export interface Commitment {
  // Public commitment value C as a hex string (big-endian).
  c: string;
  // Blinding factor r as hex (private to committer).
  r: string;
  // Scalar form of the mandate, hex (private — never expose externally).
  scalar: string;
}

export async function commit(maxim: string): Promise<Commitment> {
  const H = await getH();
  const s = await maximToScalar(maxim);
  const r = randomBelowQ();
  const c = (modPow(G, s, P) * modPow(H, r, P)) % P;
  return {
    c: bigintToHex(c),
    r: bigintToHex(r),
    scalar: bigintToHex(s),
  };
}

// Re-derive C from a stored (scalar, r) pair. Used by tests + the audit endpoint.
export async function recomputeC(scalarHex: string, rHex: string): Promise<string> {
  const H = await getH();
  const s = hexToBigint(scalarHex);
  const r = hexToBigint(rHex);
  const c = (modPow(G, s, P) * modPow(H, r, P)) % P;
  return bigintToHex(c);
}
