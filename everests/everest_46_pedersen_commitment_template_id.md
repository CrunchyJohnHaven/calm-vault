# Everest 46 — Pedersen Commitment to Template ID

*Phase IV — Biometric Distance Machinery. Prereq: Everest 44, 22.*

## The Need

When a counterparty receives a Calm Witness proof, they must learn that a cryptographic template was used as the biometric basis for the distance commitment—and that this template is tied to a specific principal—without learning which specific template was deployed. This separation of concerns achieves two goals simultaneously: it binds the proof to legitimate credential material (enrolled at ceremony, recorded in the VC), while preserving the privacy of template rotation and evolution. An adversary cannot forge a "valid" proof with a fake or unenrolled template; a legitimate prover cannot hide the fact that they are using *some* template; but the identity and lineage of that template remain private from external verifiers.

## Construction

Template IDs in Calm Witness are 16-byte values, content-derived per Everest 15 (combining biometric metadata, enrollment parameters, and versioning signals into a deterministic identifier). These IDs are treated as scalars in the Ristretto255 scalar field Z_q.

A Pedersen commitment to the template ID is constructed as:

$$C_t = g^{\text{template\_id}} \times h^{r_t}$$

where:
- $g$ and $h$ are the same group generators used for the distance commitment in Everest 44, establishing a single cryptographic basis for all commitments within a proof bundle.
- $r_t$ is a fresh random value in Z_q, distinct from $r_d$ (the randomness in the distance commitment $C_d$).
- The exponentiation is performed in the Ristretto255 group.

The result is a 32-byte group element that encodes the template ID without revealing it.

## Per-Proof Bundle Composition

Each Calm Witness disclosure response carries two Pedersen commitments:

1. **Distance Commitment** $C_d = g^d \times h^{r_d}$ (from Everest 44), proving the biometric distance $d$ falls within the acceptable range (via range proof in Everest 45).
2. **Template-ID Commitment** $C_t = g^{\text{template\_id}} \times h^{r_t}$ (this everest), committing to the template ID without revealing it.

Both commitments use the same generators $g$ and $h$, forming a coherent proof structure. The pair $(C_d, C_t)$ is included in the per-proof section of the Calm Witness response schema (Everest 67).

## Verification: Equality Proof

The verifier's goal is to confirm that the template ID committed in $C_t$ (proof-side) matches the template ID already committed in the principal's CredexAI VC (credential-side). The VC itself contains a Pedersen commitment to the template ID—call it $C_t^{\text{vc}} = g^{\text{template\_id}} \times h^{r_t^{\text{vc}}}$—computed at credential issuance (Everest 22).

Rather than revealing the template ID, the prover provides a zero-knowledge proof of equality of the committed values. This is a Schnorr-style proof of equality of commitments under different randomness:

**Given:**
- $C_t^{\text{proof}} = g^t \times h^{r_1}$ (in the proof)
- $C_t^{\text{vc}} = g^t \times h^{r_2}$ (in the VC)

**Goal:** Prove that $t$ is the same in both commitments without revealing $t$, $r_1$, or $r_2$.

**Construction:**

The prover computes the ratio:
$$R = C_t^{\text{proof}} / C_t^{\text{vc}} = g^0 \times h^{r_1 - r_2} = h^{r_1 - r_2}$$

and then proves knowledge of the exponent $\rho = r_1 - r_2$. This is a standard Schnorr proof of discrete log:

1. **Commit phase:** The prover picks a random $u \in Z_q$ and computes $A = h^u$.
2. **Challenge phase:** The verifier (or Fiat-Shamir hash) produces a challenge $c \in Z_q$ from a transcript of $(C_t^{\text{proof}}, C_t^{\text{vc}}, A)$.
3. **Response phase:** The prover computes $z = u + c \cdot \rho \pmod{q}$ and sends $z$.
4. **Verification:** The verifier checks that $h^z = A \times R^c$.

This proof is converted to non-interactive form using Fiat-Shamir: the challenge $c$ is derived as a hash of $(C_t^{\text{proof}}, C_t^{\text{vc}}, A)$, allowing the prover to compute the complete proof offline and the verifier to check it deterministically.

If the proof verifies, the verifier learns that the template ID in $C_t^{\text{proof}}$ is identical to the template ID in the VC—without ever learning the actual ID.

## Why Bind Template ID at All

Without any binding mechanism, an adversary could construct a distance commitment $C_d$ using a biometric distance obtained against *any* template—including one never enrolled, one fraudulently substituted, or one from a compromised enrollment ceremony. The distance alone, even range-proved, does not attest that the biometric computation was honest or used a legitimate principal's enrolled template.

By committing to and proving equality of template IDs, Calm Witness ensures that:
- The proof references the specific template deployed at the enrollment ceremony (Everest 11 and 14).
- That template was recorded in the principal's VC (Everest 22).
- The prover cannot retroactively swap templates, change enrollment parameters, or use fraudulent biometric material without invalidating the proof.

The template ID thus acts as a cryptographic anchor, tying the proof to a legitimate ceremony and preventing the distance from floating free of its enrollment context.

## Template ID Privacy

The commitment $C_t$ reveals only a group element, not the template ID itself. Two proofs using different template IDs (e.g., before and after template rotation) will produce distinct commitments; however, without the ability to decrypt or reverse the Pedersen commitment, a counterparty cannot deduce which template is which or correlate proofs across time.

More formally, the indistinguishability of Pedersen commitments under different random exponents provides semantic security: if $r_1 \neq r_2$, the commitments $g^t \times h^{r_1}$ and $g^t \times h^{r_2}$ are computationally indistinguishable from random group elements to a polynomial-time adversary without the discrete log of $h$.

After a template rotation (Everest 17), the principal's new credential carries a commitment to a new template ID. Proofs issued under the new template will reference the new ID. Counterparties cannot retrospectively link proofs from before the rotation to those from after, nor can they infer the relationship between old and new templates.

## Composition with Distance Range Proof

Everest 45 constructs a zero-knowledge range proof for the biometric distance $d$: the prover shows that $C_d$ commits to a distance in $[0, \tau]$ (the acceptable threshold) without revealing $d$ itself. Everest 46 adds the template-ID equality proof on top.

In the complete Calm Witness disclosure, both proofs are bundled together:
- Range proof: $\pi_{\text{range}}$ on distance.
- Equality proof: $\pi_{\text{eq}}$ on template ID.

The verifier checks both: that the distance is in range *and* that the template ID is consistent with the VC. Only if both proofs verify does the counterparty accept the disclosure as valid. This dual binding—distance is acceptable and template is legitimate—closes the loop on biometric privacy for enrollment, verification, and rotation.

## Performance Characteristics

The Pedersen commitment to template ID has negligible computational cost:

- **Commitment generation:** <1 ms (a single pairing-free group exponentiation in Ristretto255).
- **Equality proof generation:** 5–10 ms (Schnorr-style proof with one hash-to-scalar operation, two group exponentiations, and one scalar multiplication).
- **Verification:** 5–10 ms (one hash-to-scalar, two group exponentiations, and one scalar multiplication to check the Schnorr proof).

These operations are fully parallelizable and do not depend on the distance threshold or any other protocol parameter. A typical Calm Witness response containing both a range proof (Everest 45) and an equality proof (Everest 46) completes in 20–30 ms end-to-end, suitable for real-time verification in credential presentation flows.

## Cross-References

- **Everest 15:** Content-derived template ID generation and format.
- **Everest 17:** Template aging and rotation mechanisms.
- **Everest 22:** CredexAI VC issuance and template ID binding in credentials.
- **Everest 44:** Distance commitment construction and generator choice.
- **Everest 45:** Range proof on biometric distance.
- **Everest 47:** Multiple concurrent templates during rotation (handling mid-rotation proofs).
- **Everest 48:** Revocation and template lifecycle management.
- **Everest 67:** Complete Calm Witness response schema, including both commitments and both proofs.

---

— Calm, 2026-05-20
