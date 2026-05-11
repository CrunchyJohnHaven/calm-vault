// ULID-shaped, lexicographically sortable, URL-safe ids.
// 10-char base32 timestamp + 16-char base32 randomness.

const CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";

function encodeBase32(value: bigint, len: number): string {
  const out = new Array<string>(len);
  let v = value;
  for (let i = len - 1; i >= 0; i--) {
    const r = Number(v & 31n);
    out[i] = CROCKFORD[r]!;
    v >>= 5n;
  }
  return out.join("");
}

function randomBytes(n: number): Uint8Array {
  const buf = new Uint8Array(n);
  crypto.getRandomValues(buf);
  return buf;
}

export function newId(prefix: string): string {
  const ts = BigInt(Date.now());
  const tsPart = encodeBase32(ts, 10);
  const rand = randomBytes(10);
  let randInt = 0n;
  for (const b of rand) randInt = (randInt << 8n) | BigInt(b);
  const randPart = encodeBase32(randInt, 16);
  return `${prefix}_${tsPart}${randPart}`;
}

export function newOrgId(): string {
  return newId("org");
}

export function newCustomerId(): string {
  return newId("cus");
}

export function newAttestationId(): string {
  return newId("att");
}
