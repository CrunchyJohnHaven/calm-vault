// Block-hash construction for org chains.
//
// Each org has a chain:
//   genesis -> attestation_1 -> attestation_2 -> ...
//
// A block's hash is sha256(canonical_json(block)). prev_hash chains them.

import { canonicalJsonStringify, sha256Hex } from "./hex";

export interface GenesisBlock {
  kind: "genesis";
  org_id: string;
  org_legal_name: string;
  founder_name: string;
  jurisdiction: string;
  commitment_c: string;
  created_at: number;
  prev_hash: null;
}

export interface AttestationBlock {
  kind: "attestation";
  attester_org_id: string;
  target_org_id: string;
  attestation_kind: string;
  signature: string;
  prev_hash: string;
  created_at: number;
}

export type Block = GenesisBlock | AttestationBlock;

export async function blockHash(block: Block): Promise<string> {
  const canonical = canonicalJsonStringify(block);
  return await sha256Hex(canonical);
}
