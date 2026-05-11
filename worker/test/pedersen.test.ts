import { describe, expect, it } from "vitest";
import {
  commit,
  recomputeC,
  maximToScalar,
  P,
  Q,
  G,
  getH,
  modPow,
} from "../src/lib/pedersen";

describe("Pedersen commitment (Bradley-Gavini protocol)", () => {
  it("group parameters are sane", () => {
    expect(P).toBeGreaterThan(0n);
    expect(Q).toBe((P - 1n) / 2n);
    expect(G).toBe(2n);
  });

  it("H is a generator of the prime-order subgroup", async () => {
    const H = await getH();
    expect(H).toBeGreaterThan(1n);
    expect(modPow(H, Q, P)).toBe(1n);
  });

  it("maximToScalar produces values in [1, Q-1]", async () => {
    const s = await maximToScalar("Reduce malaria mortality.");
    expect(s).toBeGreaterThanOrEqual(1n);
    expect(s).toBeLessThan(Q);
  });

  it("commit() produces hiding/randomized commitments", async () => {
    const a = await commit("the maxim");
    const b = await commit("the maxim");
    // Same maxim, different r -> different C.
    expect(a.c).not.toBe(b.c);
    expect(a.scalar).toBe(b.scalar);
  });

  it("commitments to different maxims produce different scalars", async () => {
    const a = await commit("maxim A");
    const b = await commit("maxim B");
    expect(a.scalar).not.toBe(b.scalar);
  });

  it("recomputeC matches commit output (binding sanity)", async () => {
    const c = await commit("rebuild me");
    const recomputed = await recomputeC(c.scalar, c.r);
    expect(recomputed).toBe(c.c);
  });
});
