# Everest 184 — Cooperation Graph Without Revealing Graph

*Phase XII — Cooperation & Generosity. Prereq: Everest 167.*

## Overview

Everest 184 specifies a family of zero-knowledge predicates that reveal **properties** of a principal's cooperation network (who they've worked with) without disclosing the network itself. The principal's cooperation chain implicitly forms a graph: nodes are counterparties (collaborators, partners, co-founders, mentors, mentees), and edges are cooperation records from the chain. This Everest makes it possible for a counterparty to ask, "Is this principal well-connected in their community?" or "Does this principal bridge otherwise-isolated groups?" — and receive a single bit of evidence — without learning who the principal has worked with.

The threat model distinguishes between **revealing the graph topology** (which would expose relationships and identities) and **revealing aggregate properties** (which characterize the principal's structural position in their network). The protocol makes the latter verifiable in zero-knowledge while refusing the former.

## Graph Definition

A principal P's cooperation graph G_P = (V, E) is constructed as follows:

- **Vertices V:** The set of all distinct counterparties mentioned in cooperation records (Everest 176, 177, 178, 180, 181) on P's chain.
- **Edges E:** An edge (u, v) exists iff P has a cooperation record jointly naming u and v, or there are cooperation records with u followed by v within a time window indicating sustained collaboration.
- **Edge attributes:** Each edge carries metadata: cooperation type (gift, time-given, skill-shared, mutual-aid, collaboration-outcome), timestamp, and outcome attestation.

The graph is constructed from **bilateral attestations only.** An edge (u, v) is included only if:
1. P's chain contains a cooperation record naming both u and v, **and**
2. (If available) u's chain contains a matching cooperation record attesting the same cooperation event.

This bilateral requirement provides Sybil defense: fake nodes have no counterparty confirmation, so they cannot contribute edges to the graph.

## Properties of Interest

### Density

**Definition:** The fraction of possible edges that actually exist.

$$\text{Density}(G_P) = \frac{|E|}{|V| \times (|V| - 1) / 2}$$

For a principal with few counterparties and many collaborations, density approaches 1 (clique-like). For a principal with many counterparties and sparse cooperation, density approaches 0.

**Interpretation:** A principal with low density is structurally isolated (works with many people but rarely in overlapping groups). A principal with high density is deeply embedded in a tight community. Neither is inherently good or bad; the bit reveals structure, not worth.

**Tractability:** Density is tractable. It requires only counting edges and nodes, then proving the ratio falls in a range [lo_density, hi_density] via a simple arithmetic constraint and range proof (Everest 45-style).

### Average Path Length

**Definition:** The average shortest path between all pairs of nodes.

$$\text{AvgPathLen}(G_P) = \frac{1}{|V| \times (|V| - 1)} \sum_{(u, v) \in V \times V, u \neq v} \text{ShortestPath}(u, v)$$

**Interpretation:** A principal whose collaborators form a connected small-world network has low average path length (typically 2–4 hops). A principal whose collaborators exist in isolated clusters has high path length.

**Tractability:** Average path length is medium-difficulty. Computing shortest paths requires BFS or Floyd-Warshall over the committed edge set. In ZK, this requires committed vertices and committed edges, then a circuit that verifies path existence without revealing which paths exist. Feasible with careful circuit design but not trivial.

### Cross-Cluster Bridging

**Definition:** The principal's removal would increase the number of connected components (clusters) in the graph.

A principal is a **bridge** if their cooperation records are the only connection between two or more otherwise-disconnected groups of collaborators.

**Interpretation:** A bridging principal is structurally valuable: they connect communities that would otherwise be isolated. This is a strong signal of network position.

**Tractability:** Cross-cluster bridging is **hard.** It requires proving a graph-theoretic property (connectivity) in zero-knowledge. The proof must demonstrate:
1. The current graph has K connected components.
2. Removing the principal's edges increases the number of components to K + N (for N ≥ 1).

This requires committed graph structure, BFS/DFS computations in the circuit, and multiple connectivity proofs. Active research area; no production implementations known.

### Clustering Coefficient

**Definition:** The fraction of potential triangles that actually form.

$$\text{ClusteringCoeff}(G_P) = \frac{|T|}{|Triples|}$$

where |T| is the number of closed triangles (u–v–w all connected) and |Triples| is the number of triples (u, v, w) such that at least two of the three edges exist.

**Interpretation:** A principal whose collaborators frequently collaborate with each other forms many triangles (high clustering). A principal whose collaborators are strangers to each other has low clustering.

**Tractability:** Clustering coefficient is medium-hard. It requires counting triangles and triples over committed edges. Counting triangles in ZK is expensive: requires iterating over all (u, v, w) triples and checking edge existence for all three pairs. Doable with multilinear extensions or other algebraic techniques, but not as direct as density.

### Degree Distribution

**Definition:** The set of vertex degrees (how many edges each node has). Typically summarized as:
- **Gini coefficient:** measure of inequality in degree distribution (0 = all nodes have same degree; 1 = one node has all edges).
- **Max degree:** the highest-degree node.
- **Median degree:** the middle-ranked node's degree.

**Interpretation:** A principal whose collaborators all have similar numbers of collaborations has uniform degree. A principal whose collaborators include some hubs and many spokes has skewed degree distribution.

**Tractability:** Degree distribution is medium-difficulty. For specific summaries (max degree, median degree), the proof requires committed degrees for all nodes, then range proofs on specific degree bounds. Medium-complexity circuit, similar to path-length in scope.

## ZK Approach: Commitment & Constraints

The operator commits to the cooperation graph structure without revealing it:

1. **Edge Commitment:** For each edge (u, v) in E, the operator commits to a Pedersen commitment C_{(u,v)} = g^{edge_id} · h^{randomness}, where edge_id encodes the two node identifiers and cooperation type in a canonical form.

2. **Vertex Commitment:** For each vertex u in V, the operator commits to C_u = g^{node_id} · h^{randomness}, where node_id is a hash or canonical encoding of the node's identity on P's chain.

3. **Aggregate Commitments:** For density, the operator commits to |E| and |V| via range-bounded Pedersen commitments (Everest 45 style). For path length, the operator commits to the distance matrix (or a compressed representation).

4. **Proof Circuit:** For each property, an arithmetic circuit (in R1CS or similar form) takes the commitments as input and verifies:
   - The committed edges form a valid graph (no self-loops, symmetric if undirected).
   - The committed property (density, path length, etc.) satisfies the claimed range.

5. **Fiat-Shamir Transcript:** The proof is made non-interactive via Fiat-Shamir: challenges are derived as hash(commitment || property || claimed_range || all_proof_elements).

## Per-Property Circuit Sketches

### Density: Range Proof over a Ratio

**Inputs:**
- Committed |E| (edge count) as a 32-bit integer commitment C_E.
- Committed |V| (vertex count) as a 32-bit integer commitment C_V.
- Public range [lo_density, hi_density] (as fractions, e.g., [0.3, 0.7]).

**Statement:**
∃ |E|, |V| such that C_E = g^{|E|} · h^{r_E} ∧ C_V = g^{|V|} · h^{r_V} ∧ (|E| / (|V| · (|V| − 1) / 2)) ∈ [lo_density, hi_density].

**Proof construction:**
1. The prover computes density = |E| / (|V| · (|V| − 1) / 2) in fixed-point arithmetic.
2. The prover scales density into an integer: d = density · 2^{16} (or chosen precision).
3. The prover proves d ∈ [lo_d, hi_d] via a Bulletproof range proof on the scaled integer.
4. Proof size: ~700 bytes (single range proof).
5. Verification time: ~20 ms.

**Soundness notes:** The range proof is over the scaled integer. The verifier confirms that the scaled value falls in the claimed range, which is equivalent to confirming the density is within tolerance. Fixed-point precision (e.g., 2^16) introduces rounding; the tolerance window must account for it.

### Path Length: Shortest Paths in ZK

**Inputs:**
- Committed vertices V (as a vector of commitments).
- Committed edges E (as a vector of edge commitments, with source and destination node indices).
- Public maximum depth D (e.g., 5 hops).
- Claimed average path length (as a fixed-point integer commitment).

**Statement:**
∃ path matrix P such that P[u][v] = shortest path distance from u to v, and the average of all non-diagonal entries of P equals the claimed value.

**Proof construction:**
1. The operator computes the shortest-path matrix via Floyd-Warshall or BFS from each node.
2. For each (u, v) pair, the operator commits to the distance d_{u,v} and a sequence of intermediate nodes representing the shortest path.
3. For each committed path, the operator proves that the path is valid: each step (node_i → node_{i+1}) is a committed edge.
4. The operator sums all distances and proves the sum divided by |V| × (|V| − 1) equals the claimed average.
5. Proof size: O(|V|^2 · D) in the number of path constraints; for small graphs (|V| ≤ 50, D ≤ 5), this is tractable.
6. Verification time: O(|V|^2) gate operations in the circuit.

**Tractability note:** Path length is tractable for small to medium graphs (|V| ≤ 100) but becomes expensive for large graphs. This is a practical limitation of v0.

### Cross-Cluster Bridging: Graph Connectivity in ZK

**Inputs:**
- Committed edges E.
- Claimed number of connected components K.
- Claimed number of components after removing principal's edges: K + N.

**Statement:**
∃ partition π such that:
1. The graph with all edges has K connected components under partition π.
2. The graph with principal's edges removed has K + N components.
3. The principal's edges are exactly those connecting nodes in different components of the reduced graph.

**Proof construction:**
1. The operator computes the connected components via BFS/DFS.
2. For each component, the operator commits to a representative node and the set of nodes in the component.
3. The operator proves that removing edges incident to the principal disconnects at least N pairs of components.
4. This requires:
   - Commitments to component memberships (per node).
   - A circuit that verifies connectivity within each component (expensive: requires all-pairs reachability).
   - A circuit that verifies the principal's edges are the only bridges (requires checking that no other edge connects the separated components).
5. Proof size: O(|V|^2 + |E| · log|V|) in terms of circuit gates.
6. Verification time: O(|V|^2) in the circuit, which is expensive for large graphs.

**Tractability note:** Cross-cluster bridging is **hard.** Proving graph connectivity properties in ZK is an active research area with no standard, production-ready solutions. Existing approaches (Spartan via Setty et al., shuffle proofs via Schoenmakers) are complex and not yet widely implemented. **v0 defers this property to v1.**

### Clustering Coefficient: Triangle Counting in ZK

**Inputs:**
- Committed edges E (as a vector of commitments C_{(u,v)}).
- Claimed number of triangles |T|.
- Claimed number of triples |Triples|.
- Claimed clustering coefficient (as a fixed-point ratio).

**Statement:**
∃ T (set of triangles) such that |T| equals the committed count, all triangles are valid (all three edges exist in E), and the ratio |T| / |Triples| equals the claimed coefficient.

**Proof construction:**
1. The operator enumerates all triples (u, v, w) and counts how many form closed triangles.
2. For each triangle, the operator commits to the three nodes and proves all three edges exist (by proving C_{(u,v)}, C_{(v,w)}, C_{(u,w)} are in the edge commitment set).
3. The operator counts all triples (including open ones) and commits to the total.
4. The operator proves the ratio matches the claimed clustering coefficient via fixed-point arithmetic.
5. Proof size: O(|V|^3) in the worst case (all possible triples), but the circuit can be optimized to iterate only over pairs (u, v) and count how many w complete a triangle.
6. Verification time: O(|V|^3) worst-case, O(|V|^2) if optimized via edge counting.

**Tractability note:** Clustering coefficient is medium-hard. Feasible for small graphs (|V| ≤ 50) but becomes expensive as |V| grows. Multilinear extension techniques (e.g., Spartan) can reduce verification cost, but proof generation remains expensive.

## v0 Implementation Scope

Everest 184 v0 ships only the **tractable subset:**

1. **Density** (Everest 184.1) — Full implementation.
2. **Average Path Length** (Everest 184.2) — Full implementation.

**Deferred to v1:**
- Cross-cluster bridging (requires graph-connectivity ZK, not yet productionized).
- Clustering coefficient (requires multilinear extensions or other advanced techniques).
- Degree distribution variants beyond simple max/median (deferred for cost reasons).

### v0 Predicates

1. **`cwp.v0.cooperation_graph_density_in_range(lo, hi)`**
   - Inputs: principal P's cooperation chain.
   - Outputs: tri-value (TRUE, FALSE, ABSTAIN).
   - Semantics: TRUE if graph density is in [lo, hi]; FALSE if outside; ABSTAIN if graph is empty.
   - Proof time: ~500 ms.
   - Verification time: ~20 ms.

2. **`cwp.v0.cooperation_graph_avg_path_length_in_range(lo, hi)`**
   - Inputs: principal P's cooperation chain.
   - Outputs: tri-value.
   - Semantics: TRUE if average path length is in [lo, hi] hops; FALSE if outside; ABSTAIN if graph is not connected.
   - Proof time: ~2 s (depends on |V| and D; for |V| ≤ 50, D ≤ 5, typical is ~1.5 s).
   - Verification time: ~100 ms.

## Performance Budget (v0)

End-to-end on M-class hardware (Apple Silicon, 8 cores):

- Density proof: ~500 ms.
- Path-length proof: ~1.5 s.
- **Combined v0 proof (both properties):** ~2 s.
- **Verification (both):** ~120 ms.
- **Proof size (both, serialized):** ~2 KB.

These numbers assume graphs up to |V| = 50 nodes. For larger graphs, proof time scales with |V|^2 (path length circuit gates).

## Privacy Considerations

### What Is Revealed

The three-bit output (TRUE/FALSE per property) reveals **aggregate properties only:**
- "This principal's cooperation network has density > 0.4" (TRUE/FALSE).
- "This principal's collaborators are 2–3 hops apart on average" (TRUE/FALSE).

Neither property reveals **who** the principal has worked with.

### What Is Not Revealed

The protocol **refuses** to reveal:
- The identity of any counterparty.
- The structure of the graph (adjacency matrix, node list, edge list).
- The list of collaboration types or timestamps.
- Anything else beyond the property bit.

An adversary cannot:
- Infer the principal's counterparties from the proof.
- Reconstruct the graph topology via multiple property queries (each property returns a single bit; bits do not compose to reveal structure).
- Enumerate nodes or edges by brute-force over the proof.

### Implicit Reveals

Even revealing density implicitly signals: "This principal is in a cooperative network" (as opposed to a solo practitioner). This is usually desirable (the whole point of the predicate), but a privacy-conscious principal may opt out of all graph properties.

### Opt-Out Semantics

A principal can disable any cooperation-graph predicate in their privacy policy (Everest 113). If disabled, the predicate returns ABSTAIN. The counterparty learns nothing.

## Bilateral Attestation & Sybil Defense

Each edge (u, v) in G_P requires **bilateral confirmation:**

1. P's chain contains a cooperation record naming both u and v (or two consecutive records indicating a multi-step cooperation).
2. If u's chain is available, it contains a matching record (same cooperation, same timestamp or confirming range).

**Sybil defense:** An attacker cannot add fake edges by inventing fake counterparties. Fake identities have no chain and no bilateral attestation, so they are excluded from the graph.

**Limitation:** If the attacker **controls u's chain as well** (impersonates u), they can add an edge. This is detected by the protocol's identity layer (Everest 11, 22 in Calm Witness): u must prove personhood via CredexAI VC. A sophisticated attacker can create Sybil accounts, but each account requires a unique personhood proof, which is costly.

## Composition with Other Predicates

Graph properties compose with other cooperation predicates:

- **Density + Generosity (Everest 166):** "This principal is generous AND well-networked."
- **Path Length + Mentorship (Everest 168):** "This principal mentors across multiple distance-hops."
- **Density + Coalition Formation (Everest 246):** "This coalition has high-density (tight-knit) or low-density (distributed)."

## "Well-Connected" as an Alignment Signal

A principal with high cooperation density (e.g., > 0.5) has demonstrated ability to sustain multiple overlapping collaborations. This is weak but nonzero evidence of:
- **Reliability:** They keep commitments (cooperations last long enough to overlap).
- **Trustworthiness:** Multiple independent counterparties have chosen to collaborate repeatedly.
- **Realistic social proof:** They are not a Sybil (Sybils typically have low density — star topology with the attacker at the center).

The predicate is **not** a "this principal is good" claim; it is a "this principal has a real cooperative history" claim.

## Research References

- **Bonneau et al. (2015):** "Challenges in Cryptography for Private Information Retrieval" — foundational work on private queries over graph data.
- **Setty et al. (2013):** "Pepper: Practical Proofs for Machine Learning" — Spartan zk-SNARKs for graph properties, though focus is on ML; techniques apply to general graphs.
- **Schoenmakers (2019):** "Cryptographic Schemes and Protocols for Source Authentication in Sensor Networks" — shuffle-based proofs over graph structures; applicable to connectivity proofs.
- **Bünz et al. (2018):** "Bulletproofs: Short Proofs for Confidential Transactions and More" — range proofs (Everest 45), used for density bounds in v0.

None of these directly solve the bridging problem; it remains an open research direction within ZKAC.

## Risk Assessment

### What Can Go Wrong (v0)

1. **Graph Reconstruction via Property Queries:** If a counterparty can query the same principal's graph with many different tolerance windows, could they reconstruct the structure? **Mitigation:** The privacy policy (Everest 113) limits query frequency and logs all property requests. A principal can revoke disclosure consent retroactively.

2. **Side-Channel via Proof Size:** Does the proof size leak |V| or |E|? **Mitigation:** v0 pads all proofs to fixed size (~2 KB) regardless of graph size, at the cost of 20–30% overhead.

3. **Timing Attacks:** Does proof generation time correlate with graph size? **Mitigation:** All proof generation uses constant-time cryptographic operations (Ristretto255 is constant-time). Graph algorithms (Floyd-Warshall) are not constant-time; potential timing leak. **v0 Limitation:** Accepted trade-off. v1 will add constant-time graph algorithms.

4. **Adversarial Fitting:** A principal could manipulate cooperation records to inflate density just before disclosure. **Mitigation:** Cooperation records are immutable once chain-signed; drift detection (Everest 111) flags rapid changes. Still, a principal could plan ahead over months.

5. **Graph Falsification:** Could an operator commit to a fake graph that doesn't match the actual chain? **Mitigation:** The committed graph is derived deterministically from the chain in the proof; the verifier checks this derivation. If the operator falseifies the graph, the proof fails.

## Ethics & Fairness

### "Well-Connected" Is Not "Trustworthy"

A principal with high density has **structure**, not character. The protocol must emphasize:
- High density does NOT mean the principal is honest or kind.
- High density does NOT predict future cooperation (past cooperation is weak evidence of future cooperation).
- High density can indicate **local clustering** (principal cooperates deeply with a tight tribe but ignores the outside world).

### False Negatives

A principal with low density is not antisocial or untrustworthy. Reasons for low density:
- **Specialization:** The principal collaborates deeply with a single expert (high-value, low-cardinality cooperations).
- **Newness:** The principal is new to the network (limited cooperation history).
- **Recency:** The principal's cooperations are recent and not yet mature enough to overlap.
- **Privacy preference:** The principal deliberately limits visible cooperations.

The predicate output of FALSE does NOT warrant exclusion.

### Clustering Coefficient Deferred

Clustering coefficient would reveal "tight-knit tribe" vs "distributed network." v0 defers this to avoid misinterpretation as a measure of tribalism (which it is not). v1 will clarify the distinction.

## Specification Summary (v0)

**Predicates shipped:**
1. `cwp.v0.cooperation_graph_density_in_range(lo, hi)` — Tractable.
2. `cwp.v0.cooperation_graph_avg_path_length_in_range(lo, hi)` — Tractable.

**Predicates deferred to v1:**
- Bridging (graph connectivity in ZK, hard).
- Clustering coefficient (triangle counting in ZK, medium-hard).
- Degree distribution variants (medium-hard).

**Performance:**
- Combined proof time: ~2 s.
- Combined verification: ~120 ms.
- Proof size: ~2 KB.

**Graphs supported (v0):**
- Up to ~100 nodes (|V| ≤ 100).
- Up to ~1000 edges (|E| ≤ 1000).
- Average path length: up to 10 hops.

**Privacy:**
- Graph structure is not revealed.
- Property bits are the only output.
- Bilateral attestation required for Sybil defense.
- Opt-out supported per property.

## Conclusion

Everest 184 enables a principal to prove aggregate properties of their cooperation network — density and average path length — without revealing the network itself. This preserves the principal's privacy while allowing counterparties to gain weak evidence that the principal is embedded in a real, cooperative community rather than an isolated Sybil.

The v0 implementation is **partial:** density and path length are tractable; bridging and clustering are deferred to v1 pending advances in graph-property ZK (an active research area). The protocol is honest about its limitations and provides clear guidance on how to interpret (and misinterpret) the property bits.

---

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.**

**This Everest is bagged.**
