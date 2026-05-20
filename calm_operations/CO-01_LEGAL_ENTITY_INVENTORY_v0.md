# CO-01 — Legal Entity Inventory

**Closes:** Everest CO-01 in [`CALM_OPERATIONS_EVERESTS_50.md`](../CALM_OPERATIONS_EVERESTS_50.md) (Phase O-I: Identity Infrastructure)

**Effort:** S · **Status:** BAGGED 2026-05-20

---

## Acceptance Criteria

One canonical, machine-readable list of all entities the operator (Calm Stack) runs, including:
- **Entity ID** (kebab-case)
- **Legal name**
- **Kind** (LLC, C-Corp, S-Corp, 501c3, DAO, sole_proprietorship, partnership, trust)
- **Jurisdiction** (ISO-3166-2)
- **Formation date** (ISO 8601)
- **Status** (active, in_formation, dissolved)
- **Role in Calm Stack** (principal_operator, foundation, research, payments, archival, other)
- **DID assignment** (did:calm:... if assigned, else null)
- **Notes** (operational context)

**Machine-readable format:** JSON Schema–validatable at [`legal_entity_inventory_v0.json`](legal_entity_inventory_v0.json).

---

## JSON Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Legal Entity Inventory",
  "type": "object",
  "required": ["schema_version", "generated_at", "entities"],
  "properties": {
    "schema_version": {
      "type": "string",
      "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$",
      "description": "Semantic version of schema"
    },
    "generated_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp of inventory generation"
    },
    "entities": {
      "type": "array",
      "minItems": 1,
      "uniqueItems": true,
      "items": {
        "type": "object",
        "required": [
          "entity_id",
          "legal_name",
          "kind",
          "jurisdiction",
          "status",
          "role_in_calm_stack"
        ],
        "properties": {
          "entity_id": {
            "type": "string",
            "pattern": "^[a-z0-9_]+$",
            "description": "Unique kebab/snake-case identifier"
          },
          "legal_name": {
            "type": "string",
            "minLength": 1,
            "description": "Official registered name"
          },
          "kind": {
            "type": "string",
            "enum": [
              "LLC",
              "C-Corp",
              "S-Corp",
              "501c3",
              "DAO",
              "sole_proprietorship",
              "partnership",
              "trust"
            ]
          },
          "jurisdiction": {
            "type": "string",
            "pattern": "^[A-Z]{2}(-[A-Z]{2})?$",
            "description": "ISO 3166-2 country-state code (e.g., US-DE, US-NC)"
          },
          "formed_at": {
            "type": ["string", "null"],
            "format": "date",
            "description": "ISO 8601 date; null if in_formation"
          },
          "status": {
            "type": "string",
            "enum": ["active", "in_formation", "dissolved"]
          },
          "role_in_calm_stack": {
            "type": "string",
            "enum": [
              "principal_operator",
              "foundation",
              "research",
              "payments",
              "archival",
              "other"
            ]
          },
          "did": {
            "type": ["string", "null"],
            "pattern": "^(did:calm:[a-zA-Z0-9_-]+)?$",
            "description": "DID identifier if assigned; null otherwise"
          },
          "notes": {
            "type": "string",
            "description": "Operational context; no PII beyond public state records"
          }
        }
      }
    }
  }
}
```

---

## Refusal Floor (Operator-Side Data)

**Critical:** Legal entity inventory is **operator-side state**, not principal-side protected data. The operator (Calm Stack infrastructure) maintains and signs this registry.

### What belongs in this registry:
- Entity legal names (public)
- Formation dates (public in filings)
- Jurisdictions (public)
- Status (public)
- Roles in the Calm Stack (operator-assigned taxonomy)
- DIDs (once assigned; public attestation)

### What MUST NOT be in this registry:
- Social Security numbers
- Residential addresses of officers
- Telephone numbers of officers
- Personal email addresses of officers
- Passport or driver's license numbers
- Financial account details

**Officer names** may be included *only if already public in state-of-formation records* (e.g., registered agent, incorporator, founder disclosures in Delaware DGCL filings). Verify against CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md § 3.2 before including.

---

## Entity Lifecycle

### Adding a New Entity

1. **Sponsor files formation docs** (Secretary of State, IRS, etc.).
2. **Operator verifies public records** (DGCL, IRS E.O. letter, DAO voting results).
3. **Operator appends entity record** to the entities array in `legal_entity_inventory_v0.json`:
   - Assign unique `entity_id`
   - Populate all required fields
   - Set `formed_at` to official effective date
   - Set `status = "in_formation"` or `"active"` based on state
4. **Operator signs the updated JSON** via chain record (see below).
5. **Append chain record** to `/Users/johnbradley/.calm-vault/user_state.jsonl`:
   ```json
   {
     "seq": <incremented>,
     "prev_hash": "<hash of prior line>",
     "ts": "2026-05-20T...",
     "kind": "entity_append",
     "entity_id": "new_entity_id",
     "hash": "sha256(legal_entity_inventory_v0.json)"
   }
   ```

### Retiring an Entity

1. **Operator identifies sunset condition** (e.g., dissolution order, DAO sunset vote).
2. **Update entity record** in JSON:
   - Set `status = "dissolved"`
   - Append to `notes`: "Dissolved [date]; see CO-07 Operator Sunset protocol."
3. **Append chain record** (kind: `entity_sunset`).
4. **Cross-reference CO-07** (Operator Sunset protocol) for impact on signed work and DID rotation.

---

## Cross-References

- **CO-02** (DID Registry): Entities map to DIDs via `did:calm:<principal>:<domain>` URIs. CO-02 extends this registry with resolution endpoints.
- **CO-08** (Cross-Jurisdiction Entity Mapping): Maps which entity signs in which jurisdiction; ties to Witness E79 (multi-jurisdiction disclosure rules).
- **E241** (Calm Witness Foundation Incorporation): Details for Calm Witness Foundation, Inc.; incorporation filing pending; status monitored here.
- **E22** (CredexAI VC Issuance): Foundation and operators become VC issuers; entity_id tied to issuer DID.

---

## Inventory as of 2026-05-20

**See:** [`legal_entity_inventory_v0.json`](legal_entity_inventory_v0.json)

**Current entities:**
1. **Creativity Machine LLC** (US-NC, active, principal_operator)
2. **Calm Witness Foundation, Inc.** (US-DE, in_formation, foundation)
