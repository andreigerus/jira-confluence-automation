# Spec Review: Gaps, Contradictions & Unclear Requirements
**Reviewer:** Senior Developer  
**Date:** 2026-09-03  
**Scope:** constitution.md + specification.md

---

## Executive Summary
Both spec documents establish good governance principles and high-level structure, but lack implementation detail. Critical gaps exist around:
- Automation operations & triggers (undefined)
- Authentication & authorization granularity (vague)
- API error handling (minimal)
- Database migrations & rollback procedures (mentioned but not detailed)
- Frontend-backend contract specifics (missing)

**Risk Level:** **HIGH** — implementation teams will need to make significant assumptions.

---

## Critical Gaps (blocking implementation)

### 1. **Automation Operations Not Defined**
- **Gap:** Constitution & Specification both define "automation" as a sequence of operations against Jira/Confluence, but neither specifies WHAT operations are supported.
- **Impact:** Backend engineers cannot implement step execution without knowing the operation set (e.g., create issue, update field, move to workflow state, post comment, etc.).
- **Action Required:** Create `spec/operations.md` defining supported operations with parameters, preconditions, and postconditions.

### 2. **Trigger Types Incomplete**
- **Specification Section:** "triggers: array (cron, webhook, manual)"
- **Gap:** No schema for trigger objects. Cron format not specified (e.g., cron expression vs readable format?). Webhook trigger mechanism undefined (who calls the webhook? how is it secured?).
- **Action Required:** Define trigger schemas in `spec/schemas/triggers.json` with examples.

### 3. **Step Configuration Schema Missing**
- **Gap:** JSON Schema for automation shows `"steps":{"type":"array","items":{"type":"object"}}` but doesn't define step object structure.
- **Impact:** Frontend cannot render step editor. Backend cannot validate step definitions.
- **Action Required:** Create `spec/schemas/step.json` with full schema for step type, operation, parameters, error handling.

### 4. **Error Response Format Underspecified**
- **Specification:** Only mentions `{ error, details }` for 400 errors.
- **Gap:** No structure for `error` (string code? object?), no structure for `details` (array? object with field mappings?). No error response schemas for other status codes (401, 403, 500).
- **Action Required:** Define `spec/schemas/error.json` with examples for each error category.

### 5. **Authentication Scopes Not Defined**
- **Both documents mention:** `Authorization: Bearer <token>` with "write scope" and "read scope".
- **Gap:** No definition of what scopes exist (write, read, admin, execute?). No mapping of scopes to endpoints. No OAuth flow details.
- **Action Required:** Create `spec/auth.md` defining scopes, OAuth 2.0 flow (if used), API token format, and scope-to-endpoint matrix.

### 6. **Vault Reference Format Unknown**
- **Specification:** "secrets: reference to vault keys (no raw secrets stored)"
- **Gap:** What does a vault reference look like? Is it a UUID, a path, a string identifier? How does the backend resolve it? Are there secret creation/rotation APIs?
- **Action Required:** Define secret management model in `spec/secrets.md` (or append to auth.md).

### 7. **Pagination & Filtering Missing**
- **Specification:** Endpoint list shows `GET /automations/{id}` but no `GET /automations` (list) endpoint defined.
- **Gap:** No pagination parameters (limit, offset, cursor?). No filtering/sorting requirements.
- **Action Required:** Define list endpoint(s) with pagination, filter, and sort options; add to OpenAPI.

### 8. **Run Lifecycle Underspecified**
- **Specification:** "status: enum(pending,running,succeeded,failed)"
- **Gap:** 
  - No state transition diagram or invalid transitions defined.
  - No timeout/SLA for `running` state. What if a run hangs?
  - No retry behavior defined.
  - No polling interval guidance for frontend.
  - Can a run be cancelled? Re-triggered?
- **Action Required:** Define run lifecycle state machine in `spec/run-lifecycle.md`.

### 9. **Concurrency & Locking Policy Absent**
- **Gap:** Can the same automation run multiple times concurrently? If a run is in progress, can you update its definition? Can you delete an automation with active runs?
- **Impact:** Database schema, backend queuing, frontend UI behavior all depend on this.
- **Action Required:** Define concurrency policy and document in `spec/concurrency.md`.

### 10. **Jira/Confluence Integration Details Missing**
- **Gap:** How are credentials passed to step execution? OAuth token, API key, or password? How are refresh tokens handled? What Jira/Confluence API versions are supported?
- **Impact:** Critical for security and compatibility.
- **Action Required:** Create `spec/integrations.md` with auth flow for Jira/Confluence.

---

## Contradictions (spec conflicts)

### 1. **Backward Compatibility Window Conflict**
- **Constitution:** "keep last 2 major API versions supported"
- **Specification:** "breaking changes require major version bump and migration notes"
- **Contradiction:** How long do you support 2 versions? Is there a sunset date? Timeline unclear.
- **Resolution:** Define API versioning policy with sunset timelines in `spec/versioning.md`.

### 2. **PATCH vs PUT Conflict**
- **Specification (PUT endpoint):** "Replace/update automation; clients may PATCH instead"
- **Contradiction:** PATCH endpoint is NOT defined in the API section, yet it's mentioned as an option.
- **Impact:** Frontend doesn't know which to use. Backend unsure if PATCH is required or optional.
- **Resolution:** Either define PATCH endpoint in OpenAPI or remove the mention.

### 3. **Role-Based Access Control Mentioned but Undefined**
- **Constitution:** "access control with RBAC"
- **Specification:** No roles, permissions, or RBAC schema defined anywhere.
- **Contradiction:** How can QA test RBAC if roles aren't specified?
- **Resolution:** Add role definitions and permission matrix to `spec/auth.md`.

### 4. **Supported Operations Not Aligned**
- **Constitution:** "operations executed against Jira/Confluence"
- **Specification:** No definition of which operations are in scope.
- **Contradiction:** Product owner, backend, and QA will disagree on MVP scope.
- **Resolution:** Create `spec/operations.md` with MVP operations list.

---

## Unclear Requirements (ambiguous or vague)

### 1. **What Constitutes "Valid Schema" for Automation?**
- Strict JSON Schema validation? Coercion allowed? Custom validators?
- Error messages: field-level or high-level summary?

### 2. **Log Retention Policy**
- How long are run logs kept?
- Can logs be queried beyond the run event endpoint?
- Log pagination/truncation rules?

### 3. **Metrics & Observability**
- Exact Prometheus metric names and labels?
- What are SLOs vs SLAs for background runs?
- Alerting thresholds?

### 4. **Frontend Specification**
- Only mentioned as "React 18 + Vite SPA" in constitution.
- No frontend API contract defined.
- No frontend component/page specifications.
- **Action:** Create `spec/frontend.md` with frontend-backend contracts (or Pact artifacts).

### 5. **Database Migration Validation**
- What is a "sanity check" for migrations?
- Must rollback succeed for migrations to pass CI?
- How are long-running migrations handled (production concern)?

### 6. **Feature Flags & Versioning Relationship**
- Constitution mentions feature flags for new automations.
- How do feature flags interact with API versioning?
- Who controls feature flags (frontend, backend, config service)?

### 7. **Automation Update During Active Run**
- Can you update an automation while a run is in progress?
- Does the update apply to running run or only future runs?
- Versioning implications?

### 8. **Timeout Specifications**
- What's the max duration for a single automation run?
- What's the max duration for a single step?
- Timeout vs. polling interval for status checks?

### 9. **Backout Procedure**
- Constitution references `infra/ops.md` but this file is not mentioned elsewhere or in the repo.
- What are the exact backout steps?
- Database snapshot/restore strategy?

### 10. **Contract Test Format**
- Specification mentions Pact or equivalent but doesn't define:
  - Pact dialect (v2, v3, v4)?
  - Consumer/provider test split?
  - Lifecycle (generate contracts, verify provider, run in CI)?

### 11. **Automation Definition Mutability**
- Can you change step order? Remove steps?
- Schema evolution: if you add a required field, are existing automations invalid?
- Backward compatibility for automation definitions?

### 12. **Run Result Schema**
- `RunEvent` includes `"result":{"type":"object"}` but structure is undefined.
- What does success result look like? Failure result?
- What data is captured (output values, logs, errors)?

### 13. **Credentials for Jira/Confluence**
- Are API keys stored in the vault, or is OAuth token flow used?
- Can users manage their own credentials in the frontend, or is admin-only?
- Token expiration handling?

### 14. **Docker/Postgres Image Versions**
- Constitution specifies "PostgreSQL 15" but doesn't specify minor version.
- Is `postgres:15-latest` acceptable or must it pin to a specific build?
- Same for Node.js LTS — which LTS?

### 15. **User & Organization Model**
- No user/organization schema defined.
- Are automations global or per-organization?
- Can users share automations?
- Audit log format: who is "actor"?

---

## Missing Specifications

### Missing Files (referenced but not provided)
- [ ] `spec/openapi.yaml` — only a fragment provided
- [ ] `spec/schemas/automation.json` — only minimal example
- [ ] `spec/schemas/run_event.json` — only minimal example
- [ ] `spec/schemas/error.json` — not provided
- [ ] `spec/schemas/triggers.json` — not provided
- [ ] `spec/schemas/step.json` — not provided
- [ ] `spec/operations.md` — not provided
- [ ] `spec/auth.md` — not provided
- [ ] `spec/secrets.md` — not provided
- [ ] `spec/versioning.md` — not provided
- [ ] `spec/run-lifecycle.md` — not provided
- [ ] `spec/concurrency.md` — not provided
- [ ] `spec/integrations.md` — not provided
- [ ] `spec/frontend.md` — not provided
- [ ] `spec/contract/` (consumer/provider tests) — not provided
- [ ] `spec/samples/` (example requests/responses) — not provided
- [ ] `infra/ops.md` (backout procedures) — referenced but missing
- [ ] `spec/CHANGELOG.md` — not provided

### Missing Acceptance Tests
- Specification mentions test matrix but no `spec/tests/` examples provided.
- Contract test format not specified.

---

## Security Gaps

### 1. **Credential Exposure Risk**
- How are Jira/Confluence API keys/tokens passed from frontend to backend?
- Is there a secure token exchange mechanism?
- Can a frontend user steal another user's Jira credentials?

### 2. **Audit Trail Granularity**
- What constitutes a "sensitive operation"?
- Are read operations audited?
- Audit data retention?

### 3. **OAuth State & CSRF**
- If OAuth is used, is state parameter validated?
- Are CSRF tokens enforced for state-changing operations?

---

## Recommendations for Implementation

### Priority 1 (Blocking)
1. Define operations list and step schema (`spec/operations.md`, `spec/schemas/step.json`)
2. Complete OpenAPI spec (`spec/openapi.yaml`) with all endpoints and error schemas
3. Define authentication & authorization (`spec/auth.md`)
4. Specify run lifecycle and concurrency policy (`spec/run-lifecycle.md`, `spec/concurrency.md`)

### Priority 2 (High)
5. Define Jira/Confluence integration (`spec/integrations.md`)
6. Complete JSON schemas (`spec/schemas/` directory)
7. Add example payloads (`spec/samples/`)
8. Define contract test format and repository structure

### Priority 3 (Medium)
9. Create frontend specification (`spec/frontend.md`)
10. Define secret management (`spec/secrets.md`)
11. Create versioning & compatibility policy (`spec/versioning.md`)
12. Document backout procedures (`infra/ops.md`)

### Priority 4 (Low)
13. Add observability details (metric names, SLO definitions)
14. Create glossary enhancements
15. Add migration/rollback examples

---

## Severity Matrix

| Severity | Count | Examples |
|----------|-------|----------|
| Blocking (implementation impossible without clarity) | 10 | Operations, triggers, step schema, auth scopes, pagination, run lifecycle |
| High (major ambiguity, needs resolution) | 8 | Concurrency, Jira/Confluence integration, error handling, PATCH/PUT |
| Medium (unclear but implementation possible) | 12 | Log retention, metrics, frontend spec, feature flags |
| Low (nice to have clarity) | 5 | Docker versions, image pinning, glossary |

---

## Conclusion

The constitution provides good governance structure and the specification outlines the right architecture direction. However, **implementation teams will encounter significant rework if these gaps are not closed before coding starts.** Recommend:

1. **Prioritize Priority 1 work** before starting backend/frontend implementation.
2. **Use contract-driven approach:** create OpenAPI + Pact tests before writing code.
3. **Iterate specs in sprints:** assign a spec owner and gate features on spec completion.
4. **Maintain spec as living document:** update before each PR, not after.

---

**Status:** READY FOR TEAM REVIEW  
**Next Action:** Schedule spec refinement session with product owner, backend lead, frontend lead, and QA.
