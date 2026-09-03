# Implementation Tasks: jira-confluence-automation
**Date:** 2026-09-03  
**Format:** Phase-based task breakdown with acceptance criteria  
**Purpose:** Detailed task list for team assignment, tracking, and sprint planning

---

## Phase 1: Specification Completion (Weeks 1–3)

### Task 1.1: Create Complete OpenAPI v3 Specification
**Owner:** Spec Lead + Backend Lead  
**Duration:** 3 days  
**Depends on:** None  
**Acceptance Criteria:**
- [ ] `spec/openapi.yaml` created with all endpoints from specification.md
- [ ] All CRUD operations documented (POST, GET, PUT, DELETE automations/runs)
- [ ] Request/response bodies reference JSON schemas (using `$ref`)
- [ ] All HTTP status codes documented (200, 201, 400, 401, 403, 404, 500, 502)
- [ ] Error response schema included (`error`, `details`, `timestamp`)
- [ ] Authentication scheme documented (`bearerAuth` with JWT/API token)
- [ ] Examples included for at least 2 endpoints
- [ ] OpenAPI validates with `swagger-cli validate spec/openapi.yaml` (no errors)
- [ ] Linting passes with `spectacle lint spec/openapi.yaml`

### Task 1.2: Create Automation JSON Schema
**Owner:** Backend Lead + Product Owner  
**Duration:** 2 days  
**Depends on:** Task 1.1  
**Acceptance Criteria:**
- [ ] `spec/schemas/automation.json` created with JSON Schema Draft 7
- [ ] Required properties: `id`, `name`, `steps`
- [ ] Optional properties: `description`, `triggers`, `createdAt`, `updatedAt`, `createdBy`
- [ ] `id` is UUID format (v4)
- [ ] `name` is string, min 1 char, max 255 chars
- [ ] `description` is string, max 1000 chars
- [ ] `triggers` is array of trigger objects (reference to triggers.json)
- [ ] `steps` is array of step objects (reference to step.json), min 1 step
- [ ] Schema validates with `ajv validate spec/schemas/automation.json` or equivalent
- [ ] 2+ example automations in `spec/samples/automation-*.json`

### Task 1.3: Create Step JSON Schema
**Owner:** Backend Lead + Product Owner  
**Duration:** 2 days  
**Depends on:** Task 1.2  
**Acceptance Criteria:**
- [ ] `spec/schemas/step.json` created
- [ ] Required properties: `type`, `operation`, `config`
- [ ] `type` is string enum: "jira", "confluence", "condition", "loop"
- [ ] `operation` is string representing the operation (e.g., "createIssue", "updatePage")
- [ ] `config` is object with operation-specific parameters
- [ ] `config` includes `retryPolicy` (maxRetries: 0–5, backoffMs: 1000–60000)
- [ ] `config` includes `onError` (enum: "fail", "continue", "skip")
- [ ] `config` includes `timeout` (in milliseconds, 10000–3600000)
- [ ] Example steps for each operation type in `spec/samples/step-*.json`
- [ ] Schema validates with ajv

### Task 1.4: Create Triggers JSON Schema
**Owner:** Backend Lead + Product Owner  
**Duration:** 1.5 days  
**Depends on:** Task 1.2  
**Acceptance Criteria:**
- [ ] `spec/schemas/triggers.json` created
- [ ] Three trigger types defined:
  - `cron`: { `type`: "cron", `expression`: "0 0 * * *", `timezone`: "UTC" }
  - `webhook`: { `type`: "webhook", `path`: "/webhooks/automation-{id}", `allowedSources`: ["jira", "confluence"] }
  - `manual`: { `type`: "manual" }
- [ ] Cron expression validated against POSIX cron format
- [ ] Webhook path includes automation ID placeholder
- [ ] Timezone field uses IANA timezone database (e.g., "America/New_York")
- [ ] Examples for each trigger type in `spec/samples/trigger-*.json`
- [ ] Schema validates with ajv

### Task 1.5: Create RunEvent JSON Schema
**Owner:** Backend Lead  
**Duration:** 1 day  
**Depends on:** Task 1.2  
**Acceptance Criteria:**
- [ ] `spec/schemas/run_event.json` created
- [ ] Required properties: `runId`, `automationId`, `status`, `startedAt`
- [ ] Optional properties: `finishedAt`, `result`, `logs`, `error`
- [ ] `runId` is UUID format
- [ ] `automationId` is UUID format
- [ ] `status` is enum: "pending", "running", "succeeded", "failed", "cancelled"
- [ ] Timestamps are ISO 8601 format (string, format: "date-time")
- [ ] `result` is object (structure defined per operation type)
- [ ] `logs` is array of log entries: { `timestamp`, `level`, `message`, `correlationId` }
- [ ] `error` is object: { `code`, `message`, `details` }
- [ ] Example run events in `spec/samples/run-event-*.json`
- [ ] Schema validates with ajv

### Task 1.6: Create Error Response JSON Schema
**Owner:** Backend Lead  
**Duration:** 1 day  
**Depends on:** Task 1.1  
**Acceptance Criteria:**
- [ ] `spec/schemas/error.json` created
- [ ] Required fields: `code`, `message`, `timestamp`
- [ ] Optional fields: `details`, `path`, `traceId`
- [ ] `code` is string enum (e.g., "VALIDATION_ERROR", "AUTH_FAILED", "NOT_FOUND", "CONFLICT", "INTERNAL_ERROR")
- [ ] `message` is human-readable string
- [ ] `timestamp` is ISO 8601 format
- [ ] `details` is object mapping field names to error messages (for validation errors)
- [ ] Example error responses for each error code in `spec/samples/error-*.json`
- [ ] Schema validates with ajv

### Task 1.7: Create Authentication & Authorization Specification
**Owner:** Backend Lead + Security Reviewer  
**Duration:** 2 days  
**Depends on:** Task 1.1  
**Acceptance Criteria:**
- [ ] `spec/auth.md` created and documented:
  - [ ] Authentication method defined (JWT, API token, or OAuth 2.0 + decision rationale)
  - [ ] Token format specified (e.g., "Bearer <JWT>" or "Bearer <API-TOKEN>")
  - [ ] Token expiration policy (e.g., 24 hours for JWT, no expiry for API tokens)
  - [ ] Refresh token mechanism (if applicable)
  - [ ] Scope definitions with descriptions:
    - [ ] `automations:read` — read automation definitions
    - [ ] `automations:write` — create, update, delete automations
    - [ ] `runs:read` — view run history and logs
    - [ ] `runs:execute` — trigger automation runs
    - [ ] `admin` — manage users, roles, credentials
  - [ ] Scope-to-endpoint mapping table (which endpoints require which scopes)
  - [ ] RBAC roles defined (e.g., Admin, Editor, Viewer, Executor)
  - [ ] Role permissions matrix
  - [ ] OAuth flow (if used): authorization code flow, token endpoint, user info endpoint
  - [ ] Security headers documented (Authorization, X-Correlation-ID, etc.)
  - [ ] Error responses for auth failures (401, 403)
- [ ] Examples provided (JWT structure, API token format)
- [ ] Reviewed and approved by security team

### Task 1.8: Create Run Lifecycle State Machine
**Owner:** Backend Lead + Product Owner  
**Duration:** 1.5 days  
**Depends on:** Task 1.5  
**Acceptance Criteria:**
- [ ] `spec/run-lifecycle.md` created with:
  - [ ] State diagram (text or Mermaid) showing all transitions
  - [ ] States: `pending` → `running` → (`succeeded` | `failed` | `cancelled`)
  - [ ] Invalid transitions defined (e.g., cannot transition from `succeeded` to `running`)
  - [ ] Timeout rules:
    - [ ] `pending` timeout: 5 minutes (move to `failed` if not picked up by worker)
    - [ ] `running` timeout: configurable per automation (default 1 hour, max 24 hours)
    - [ ] Timeout behavior: log timeout error, transition to `failed`
  - [ ] Cancellation rules: who can cancel (automation owner, admin), when is cancellation allowed
  - [ ] Retry behavior:
    - [ ] Retry policy per step (maxRetries, backoffMs)
    - [ ] Max retries per run (to prevent infinite loops)
    - [ ] Exponential backoff example: 1s, 2s, 4s, 8s, 16s
  - [ ] Concurrency rules (separate from this spec but referenced)
  - [ ] Status change logging (who, when, why)
- [ ] Examples of state transitions for common scenarios

### Task 1.9: Create Concurrency Policy Specification
**Owner:** Backend Lead + Product Owner  
**Duration:** 1 day  
**Depends on:** Task 1.8  
**Acceptance Criteria:**
- [ ] `spec/concurrency.md` created with:
  - [ ] Question: Can the same automation run multiple times concurrently?
    - [ ] Decision: Yes/No + rationale
    - [ ] If Yes: max concurrent runs per automation (e.g., 3)
    - [ ] If No: document queueing behavior
  - [ ] Question: Can you update an automation while a run is in progress?
    - [ ] Decision: Yes (applied to next run) / No (lock automation during active run) + rationale
  - [ ] Question: Can you delete an automation with active runs?
    - [ ] Decision: Yes (archive) / No (reject with error) + rationale
  - [ ] Database-level constraints (unique indexes, foreign keys, check constraints)
  - [ ] Race condition scenarios documented (e.g., simultaneous create & delete)
  - [ ] Conflict resolution strategy (pessimistic locking, optimistic locking, eventual consistency)
- [ ] Examples of concurrency scenarios and expected behavior

### Task 1.10: Create Jira/Confluence Integration Specification
**Owner:** Backend Lead + Product Owner  
**Duration:** 2 days  
**Depends on:** None  
**Acceptance Criteria:**
- [ ] `spec/integrations.md` created with:
  - [ ] Jira integration:
    - [ ] Supported versions (Cloud / Server / Data Center, version ranges)
    - [ ] Authentication methods: OAuth 2.0, API token, or both
    - [ ] OAuth flow diagram (authorization code, token endpoint)
    - [ ] API endpoints used (list of Jira REST API endpoints in scope)
    - [ ] Rate limiting strategy (respect Jira rate limits, retry-after handling)
    - [ ] Error handling (Jira API errors → run result mapping)
  - [ ] Confluence integration:
    - [ ] Supported versions (Cloud, Server, Data Center, version ranges)
    - [ ] Authentication methods: OAuth 2.0, API token
    - [ ] API endpoints used
    - [ ] Rate limiting, error handling (same as Jira)
  - [ ] Credential storage & rotation:
    - [ ] Credentials stored in vault (not DB, not env vars in application code)
    - [ ] Token refresh flow (e.g., OAuth 2.0 refresh token handling)
    - [ ] Credential rotation policy (e.g., rotate tokens every 90 days)
  - [ ] Security considerations:
    - [ ] No credentials logged
    - [ ] TLS/SSL for all API calls
    - [ ] Credential scoping (least privilege)
    - [ ] Audit logging of credential usage
  - [ ] Sandbox environment setup:
    - [ ] Jira sandbox instance URL and credentials (for testing)
    - [ ] Confluence sandbox instance URL and credentials
    - [ ] Test data available (sample projects, pages)
  - [ ] Fallback & resilience:
    - [ ] Circuit breaker pattern for external API calls
    - [ ] Timeout values (per request, per run)
    - [ ] Retry logic with exponential backoff
- [ ] Examples of OAuth flow, credential management

### Task 1.11: Create Operations Reference Guide
**Owner:** Product Owner + Backend Lead  
**Duration:** 2 days  
**Depends on:** Task 1.3  
**Acceptance Criteria:**
- [ ] `spec/operations.md` created with MVP operations list:
  - For each operation:
    - [ ] Operation name (e.g., "CreateJiraIssue")
    - [ ] Target system (Jira / Confluence)
    - [ ] Parameters (input fields, types, required/optional)
    - [ ] Preconditions (what must be true before execution)
    - [ ] Postconditions (what will be true after execution)
    - [ ] Success result format
    - [ ] Failure scenarios and error codes
    - [ ] Example input/output (in spec/samples/)
  - [ ] Jira operations (MVP):
    - [ ] Create Issue
    - [ ] Update Issue (field values)
    - [ ] Transition Issue (workflow)
    - [ ] Add Comment
  - [ ] Confluence operations (MVP):
    - [ ] Create Page
    - [ ] Update Page
    - [ ] Add Comment
    - [ ] Move Page
  - [ ] (Future operations listed as backlog)
- [ ] Operations organized by system and type
- [ ] Approved by product owner (scope confirmation)

### Task 1.12: Create Example Requests & Responses
**Owner:** Backend Lead  
**Duration:** 2 days  
**Depends on:** Tasks 1.2–1.6, 1.11  
**Acceptance Criteria:**
- [ ] `spec/samples/` directory created with files:
  - [ ] `automation-simple.json` — minimal automation with 1 step
  - [ ] `automation-complex.json` — automation with cron trigger, multiple steps, error handling
  - [ ] `step-create-issue.json` — step for creating Jira issue
  - [ ] `step-update-page.json` — step for updating Confluence page
  - [ ] `trigger-cron.json` — cron trigger example
  - [ ] `trigger-webhook.json` — webhook trigger example
  - [ ] `run-event-success.json` — successful run result
  - [ ] `run-event-failed.json` — failed run with error details
  - [ ] `error-validation.json` — validation error response
  - [ ] `error-auth.json` — authentication error response
- [ ] All examples are valid JSON and conform to their respective schemas
- [ ] Examples are realistic and usable in API documentation

### Task 1.13: Validate & Lint All Specifications
**Owner:** Spec Lead  
**Duration:** 1 day  
**Depends on:** Tasks 1.1–1.12  
**Acceptance Criteria:**
- [ ] All JSON schemas validate with `ajv compile spec/schemas/*.json` (no errors)
- [ ] OpenAPI validates with `swagger-cli validate spec/openapi.yaml` (no errors)
- [ ] All `$ref` references resolve (no broken links)
- [ ] All example files in spec/samples/ conform to their schemas (validation passes)
- [ ] Markdown files pass spell-check and link validation
- [ ] No TODO or FIXME markers in spec files
- [ ] Spec lint report generated and documented

### Task 1.14: Product Owner Sign-off on Spec
**Owner:** Product Owner  
**Duration:** 1 day  
**Depends on:** Task 1.13  
**Acceptance Criteria:**
- [ ] Product owner reviews all spec documents
- [ ] Product owner approves:
  - [ ] Operations list (MVP scope)
  - [ ] Authentication & authorization model
  - [ ] Run lifecycle & concurrency rules
  - [ ] API contract (endpoints, payloads)
- [ ] Sign-off documented in spec/SIGN-OFF.md (date, name, approval)
- [ ] Any changes requested by PO incorporated
- [ ] Spec locked (no further changes without PO review)

---

## Phase 2: Foundation & Setup (Weeks 2–4)

### Task 2.1: Create Docker Compose Development Stack
**Owner:** DevOps Lead  
**Duration:** 2 days  
**Depends on:** Phase 1 complete  
**Acceptance Criteria:**
- [ ] `infra/docker-compose.yml` created with services:
  - [ ] PostgreSQL 15 (image: postgres:15-alpine or postgres:15)
  - [ ] Backend Node.js (build from backend/Dockerfile)
  - [ ] Frontend Node.js (build from frontend/Dockerfile, optional)
  - [ ] Volumes: postgres_data (persistent), logs (optional)
  - [ ] Networks: defined for inter-service communication
  - [ ] Env variables: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, DATABASE_URL, NODE_ENV
- [ ] `infra/.env.example` created with template variables (no secrets)
- [ ] `infra/.env.local` gitignored (not committed)
- [ ] README in infra/ with setup instructions
- [ ] `docker-compose up` starts all services successfully
- [ ] Services are healthy and interconnected (backend can connect to postgres)
- [ ] Logs are accessible (docker-compose logs <service>)

### Task 2.2: Create Database Migration Framework
**Owner:** Backend Lead + DevOps  
**Duration:** 2 days  
**Depends on:** Task 2.1  
**Acceptance Criteria:**
- [ ] Migration tool chosen (node-pg-migrate or knex) and documented
- [ ] Migration directory created: `backend/migrations/`
- [ ] Migration template/boilerplate created (up/down functions)
- [ ] Initial migration script: `001-initial-schema.js` or `.sql` that creates:
  - [ ] `automations` table (id UUID PK, name TEXT, definition JSONB, created_at TIMESTAMP, updated_at TIMESTAMP, created_by UUID)
  - [ ] `runs` table (run_id UUID PK, automation_id UUID FK, status TEXT, started_at TIMESTAMP, finished_at TIMESTAMP, result JSONB)
  - [ ] `audit_logs` table (id SERIAL PK, actor TEXT, action TEXT, target JSONB, created_at TIMESTAMP)
  - [ ] `users` table (id UUID PK, email TEXT UNIQUE, role TEXT, created_at TIMESTAMP) [if needed]
  - [ ] Indexes on frequently queried columns (automation_id, status, created_at)
  - [ ] Foreign key constraints with appropriate cascading behavior
- [ ] Rollback script for initial migration (drop tables)
- [ ] Migration runs successfully in docker-compose postgres service
- [ ] Migration can be rolled back without errors
- [ ] Migration is idempotent (running twice is safe)

### Task 2.3: Set Up CI/CD Pipeline (GitHub Actions)
**Owner:** DevOps Lead  
**Duration:** 3 days  
**Depends on:** None (parallel with other Phase 2 tasks)  
**Acceptance Criteria:**
- [ ] `.github/workflows/` directory created
- [ ] Workflow files created:
  - [ ] `lint.yml` — linting for frontend, backend, spec
    - [ ] Backend: ESLint, Prettier
    - [ ] Frontend: ESLint, Prettier
    - [ ] Spec: markdown lint, OpenAPI lint
  - [ ] `test.yml` — unit & integration tests
    - [ ] Backend: Jest or Mocha/Chai
    - [ ] Frontend: Jest/Vitest
    - [ ] Coverage reports (aim for >80%)
  - [ ] `contract-tests.yml` — Pact contract tests
  - [ ] `build.yml` — build artifacts (Docker images, frontend bundle)
  - [ ] `openapi-check.yml` — validate OpenAPI spec
- [ ] All workflows trigger on PR and push to main/master
- [ ] Workflow status visible in PR checks
- [ ] Workflow artifact retention configured (14 days default)
- [ ] Secrets configured in GitHub (DOCKER_USERNAME, etc., if needed for deployment)
- [ ] Workflow completion time monitored (target: <10 minutes for all checks)

### Task 2.4: Set Up Pact Contract Testing Framework
**Owner:** QA Lead + Backend Lead  
**Duration:** 2 days  
**Depends on:** Task 2.3  
**Acceptance Criteria:**
- [ ] Pact library installed (pact, @pact-foundation/pact)
- [ ] Pact version and dialect chosen (v2/v3/v4)
- [ ] Consumer test example created (frontend mocks backend):
  - [ ] `frontend/tests/contract/consumers/automations.pact.js` (or .test.js)
  - [ ] Tests create and get automation via mocked API
  - [ ] Pact file generated: `pacts/frontend-backend.json`
- [ ] Provider test example created (backend verifies Pact):
  - [ ] `backend/tests/contract/provider.pact.js` (or .test.js)
  - [ ] Starts test server, runs Pact verification
  - [ ] Verification passes
- [ ] Pact broker configured (local or cloud):
  - [ ] Broker URL documented
  - [ ] Consumer publishes Pact on successful tests
  - [ ] Provider fetches Pact for verification
- [ ] Contract tests integrated into CI/CD (runs after unit tests)
- [ ] Contract test failure blocks PR merge

### Task 2.5: Set Up Logging & Structured Logging
**Owner:** Backend Lead  
**Duration:** 1.5 days  
**Depends on:** Task 2.1  
**Acceptance Criteria:**
- [ ] Logger library chosen (winston, bunyan, or pino) and installed
- [ ] Logger configured for JSON output (not text)
- [ ] Log fields standardized:
  - [ ] `timestamp` (ISO 8601)
  - [ ] `level` (debug, info, warn, error)
  - [ ] `message` (human-readable)
  - [ ] `correlationId` (or traceId for request tracking)
  - [ ] `userId` (if authenticated)
  - [ ] `service` (e.g., "backend-api", "backend-worker")
  - [ ] `module` (e.g., "automations-controller")
- [ ] Middleware added to Express for request logging:
  - [ ] Logs HTTP method, path, status, duration
  - [ ] Generates/propagates correlationId
  - [ ] Excludes health check and metrics endpoints (spam prevention)
- [ ] Log levels configured per environment (debug in dev, warn in prod)
- [ ] Sensitive data filtering (credentials, tokens not logged)
- [ ] Logger exported for use in modules (e.g., `const logger = require('./logger')`)
- [ ] Test: logger output captured and verified in unit tests

### Task 2.6: Set Up Prometheus Metrics Endpoint
**Owner:** DevOps Lead + Backend Lead  
**Duration:** 1.5 days  
**Depends on:** Task 2.1  
**Acceptance Criteria:**
- [ ] Prometheus client library installed (prom-client)
- [ ] Metrics endpoint created: `GET /metrics`
- [ ] Metrics endpoint returns Prometheus exposition format (text/plain)
- [ ] Basic metrics defined:
  - [ ] `http_request_total` (counter, labels: method, path, status)
  - [ ] `http_request_duration_seconds` (histogram, labels: method, path)
  - [ ] `db_query_duration_seconds` (histogram, labels: query_type)
  - [ ] `db_connection_pool_size` (gauge)
  - [ ] `runs_total` (counter, labels: status)
  - [ ] `runs_duration_seconds` (histogram)
- [ ] Metrics endpoint excluded from auth checks (public)
- [ ] Metrics endpoint excluded from request logging (spam prevention)
- [ ] Sample metrics output documented in README
- [ ] Prometheus scrape config example in `infra/` (for future monitoring stack)

### Task 2.7: Create API Key/Token Generation Utilities
**Owner:** Backend Lead  
**Duration:** 1 day  
**Depends on:** Task 1.7  
**Acceptance Criteria:**
- [ ] JWT token generation utility created (backend/src/utils/jwt.js or similar):
  - [ ] Signs JWT with secret (from env variable JWT_SECRET)
  - [ ] Includes payload: { userId, scopes, iat, exp, iss }
  - [ ] Expiration configurable (default 24 hours)
  - [ ] Returns token string
- [ ] JWT verification utility:
  - [ ] Verifies signature and expiration
  - [ ] Returns decoded payload or throws error
- [ ] API token generation utility (if using API tokens):
  - [ ] Generates cryptographically secure random token
  - [ ] Format: "api_<user-id>_<random>" (for readability)
  - [ ] Stored as hash in database (not plaintext)
- [ ] Test coverage:
  - [ ] Valid token verification passes
  - [ ] Expired token verification fails
  - [ ] Invalid signature fails
  - [ ] Token generation produces unique tokens

### Task 2.8: Set Up Local Development Documentation
**Owner:** DevOps Lead + Backend Lead  
**Duration:** 1 day  
**Depends on:** Tasks 2.1–2.7  
**Acceptance Criteria:**
- [ ] `DEVELOPMENT.md` created at repo root with:
  - [ ] Prerequisites (Node version, Docker, npm/yarn)
  - [ ] Quick start (clone, `docker-compose up`, test with curl/postman)
  - [ ] Environment setup (.env.local instructions)
  - [ ] Database schema diagram or description
  - [ ] Common commands (run tests, start services, view logs)
  - [ ] Troubleshooting guide (common issues & solutions)
  - [ ] Contribution guidelines (git workflow, code style, PR process)
  - [ ] IDE setup (recommended VS Code extensions, debugger config)
- [ ] `README.md` updated with link to DEVELOPMENT.md
- [ ] `infra/README.md` created with infrastructure details
- [ ] All code examples tested and working
- [ ] Documented by someone unfamiliar with the project (clarity check)

---

## Phase 3: Backend MVP (Weeks 5–8)

### Task 3.1: Set Up Express Server & Middleware
**Owner:** Backend Lead  
**Duration:** 1.5 days  
**Depends on:** Phase 2 complete  
**Acceptance Criteria:**
- [ ] `backend/src/server.js` created as Express application entry point
- [ ] Server listens on port 4000 (configurable via env variable)
- [ ] Middleware stack configured (in order):
  - [ ] Body parser (JSON, max 10MB)
  - [ ] CORS (allow frontend origin)
  - [ ] Request logging (correlationId generation)
  - [ ] Authentication middleware (optional, except for specific routes)
  - [ ] Error handling middleware (catches all exceptions, logs, returns spec-compliant error)
- [ ] Health check endpoint: `GET /api/v1/health` returns:
  ```json
  { "status": "ok", "components": { "postgres": true, "queue": true }, "timestamp": "ISO-8601" }
  ```
- [ ] Metrics endpoint: `GET /metrics` exposed (public)
- [ ] Error handler returns `{ code, message, timestamp, details }` per spec
- [ ] Server starts without errors: `npm run start`
- [ ] Test: curl localhost:4000/api/v1/health returns 200

### Task 3.2: Implement Authentication Middleware
**Owner:** Backend Lead  
**Duration:** 1.5 days  
**Depends on:** Task 3.1 + Task 1.7 (spec)  
**Acceptance Criteria:**
- [ ] Authentication middleware created (`backend/src/middleware/auth.js`)
- [ ] Extracts Bearer token from Authorization header
- [ ] Verifies token (JWT signature, expiration)
- [ ] Decodes token and attaches user/scopes to request object (req.user, req.scopes)
- [ ] Returns 401 if no token provided
- [ ] Returns 401 if token invalid/expired
- [ ] Returns 403 if scopes insufficient (used by route-level scope check)
- [ ] Skips auth for public endpoints (health, metrics)
- [ ] Unit tests:
  - [ ] Valid token passes
  - [ ] Expired token rejected
  - [ ] Invalid signature rejected
  - [ ] Missing token rejected
  - [ ] Scopes correctly decoded

### Task 3.3: Implement Scope-Based Authorization
**Owner:** Backend Lead  
**Duration:** 1 day  
**Depends on:** Task 3.2  
**Acceptance Criteria:**
- [ ] Scope validation middleware created (`backend/src/middleware/scope.js`)
- [ ] Middleware takes required scope(s) as parameter
- [ ] Checks if req.user.scopes includes required scope
- [ ] Returns 403 if scope insufficient
- [ ] Usage: `router.post('/automations', requireScope('automations:write'), handler)`
- [ ] Unit tests:
  - [ ] User with required scope passes
  - [ ] User without scope rejected (403)
  - [ ] Multiple scopes: user must have all (AND logic)

### Task 3.4: Create Automation CRUD Endpoints (Create & Get)
**Owner:** Backend Engineer 1  
**Duration:** 2 days  
**Depends on:** Task 3.3 + Task 1.2 (schema)  
**Acceptance Criteria:**
- [ ] `POST /api/v1/automations` endpoint:
  - [ ] Accepts JSON body conforming to Automation schema
  - [ ] Validates schema with ajv (validation error → 400 with error details)
  - [ ] Validates no duplicate names (or returns 409 Conflict)
  - [ ] Creates record in `automations` table
  - [ ] Returns 201 with created automation (including id, timestamps)
  - [ ] Logs audit entry: { action: "CREATE_AUTOMATION", actor: userId, target: automationId }
  - [ ] Requires scope: `automations:write`
- [ ] `GET /api/v1/automations/{id}` endpoint:
  - [ ] Retrieves automation by id
  - [ ] Returns 200 with automation object
  - [ ] Returns 404 if not found
  - [ ] Requires scope: `automations:read`
  - [ ] Logs audit entry: { action: "READ_AUTOMATION", actor: userId, target: automationId }
- [ ] Integration tests:
  - [ ] Create valid automation → 201 created
  - [ ] Create invalid automation → 400 with error details
  - [ ] Get existing automation → 200
  - [ ] Get non-existent automation → 404
  - [ ] Create without auth → 401
  - [ ] Create without scope → 403

### Task 3.5: Create Automation CRUD Endpoints (List, Update, Delete)
**Owner:** Backend Engineer 2  
**Duration:** 2 days  
**Depends on:** Task 3.4  
**Acceptance Criteria:**
- [ ] `GET /api/v1/automations` endpoint:
  - [ ] Returns paginated list of automations
  - [ ] Query parameters: `limit` (default 20, max 100), `offset` (default 0)
  - [ ] Response: `{ data: [...], total: N, limit, offset }`
  - [ ] Filter by status (if status field exists) or other criteria
  - [ ] Returns 200
  - [ ] Requires scope: `automations:read`
- [ ] `PUT /api/v1/automations/{id}` endpoint:
  - [ ] Accepts JSON body (full automation update)
  - [ ] Validates schema (validation error → 400)
  - [ ] Updates automation in DB
  - [ ] Returns 200 with updated automation
  - [ ] Returns 404 if not found
  - [ ] Requires scope: `automations:write`
  - [ ] Logs audit entry: { action: "UPDATE_AUTOMATION", actor: userId, target: automationId, changes: {...} }
  - [ ] Prevents update if automation has active run (or per concurrency policy)
- [ ] `DELETE /api/v1/automations/{id}` endpoint:
  - [ ] Deletes automation (soft delete or hard delete per policy)
  - [ ] Returns 204 No Content on success
  - [ ] Returns 404 if not found
  - [ ] Requires scope: `automations:write`
  - [ ] Logs audit entry: { action: "DELETE_AUTOMATION", actor: userId, target: automationId }
  - [ ] Prevents deletion if automation has active run (or per policy)
- [ ] Integration tests for all scenarios

### Task 3.6: Create Run Trigger Endpoint
**Owner:** Backend Engineer 1  
**Duration:** 1.5 days  
**Depends on:** Task 3.4 + Task 1.8 (lifecycle)  
**Acceptance Criteria:**
- [ ] `POST /api/v1/automations/{id}/run` endpoint:
  - [ ] Accepts optional JSON body with run parameter overrides
  - [ ] Validates automation exists (404 if not)
  - [ ] Creates record in `runs` table with status=pending
  - [ ] Enqueues job for background worker
  - [ ] Returns 202 Accepted with run object: { runId, automationId, status: "pending", startedAt }
  - [ ] Requires scope: `runs:execute`
  - [ ] Logs audit entry: { action: "TRIGGER_RUN", actor: userId, target: runId }
  - [ ] Respects concurrency policy (reject if max concurrent runs exceeded, or queue)
- [ ] Integration tests:
  - [ ] Trigger run for existing automation → 202 with runId
  - [ ] Trigger run for non-existent automation → 404
  - [ ] Without auth → 401
  - [ ] Without scope → 403

### Task 3.7: Create Run Status Endpoint
**Owner:** Backend Engineer 2  
**Duration:** 1.5 days  
**Depends on:** Task 3.6 + Task 1.5 (schema)  
**Acceptance Criteria:**
- [ ] `GET /api/v1/runs/{runId}` endpoint:
  - [ ] Retrieves run and its details
  - [ ] Returns 200 with RunEvent object: { runId, automationId, status, startedAt, finishedAt, result, logs }
  - [ ] Returns 404 if not found
  - [ ] Requires scope: `runs:read`
  - [ ] Logs: array of { timestamp, level, message, correlationId }
  - [ ] Result: object matching operation output (or error if failed)
  - [ ] Pagination/filtering of logs (if logs are large)
- [ ] Integration tests:
  - [ ] Get existing run → 200 with details
  - [ ] Get non-existent run → 404
  - [ ] Run in progress: status=running, finishedAt=null
  - [ ] Run succeeded: status=succeeded, result=<output>
  - [ ] Run failed: status=failed, result=<error>

### Task 3.8: Set Up Background Job Queue
**Owner:** Backend Engineer 1  
**Duration:** 2 days  
**Depends on:** Task 2.1 (docker-compose)  
**Acceptance Criteria:**
- [ ] Job queue library chosen (Bull, RabbitMQ, or simple polling from DB)
- [ ] Queue connection configured (Redis, message broker, or DB)
- [ ] Job structure defined: { runId, automationId, steps, createdAt }
- [ ] Queue worker process created (`backend/src/worker/index.js` or similar):
  - [ ] Connects to queue
  - [ ] Polls for pending jobs (or subscribes to queue)
  - [ ] Picks up jobs in FIFO order
  - [ ] Updates run status: pending → running
  - [ ] Executes steps sequentially (see Task 3.9)
  - [ ] On completion: updates run status (succeeded/failed)
  - [ ] On error: logs error, updates run status (failed)
  - [ ] Handles worker crash gracefully (dead-letter queue or retry)
- [ ] Worker can be started: `npm run worker`
- [ ] Unit/integration tests:
  - [ ] Job enqueued successfully
  - [ ] Worker picks up job
  - [ ] Job status transitions correctly

### Task 3.9: Implement Dummy Step Execution
**Owner:** Backend Engineer 2  
**Duration:** 2 days  
**Depends on:** Task 3.8 + Task 1.11 (operations)  
**Acceptance Criteria:**
- [ ] Step executor created (`backend/src/worker/step-executor.js`):
  - [ ] Takes step object and context (runId, automation, etc.)
  - [ ] Routes to operation handler based on step.operation
  - [ ] For MVP, operations are "dummy" (log and return success):
    - [ ] CreateJiraIssue → logs "Creating issue", returns { issueKey: "DEMO-123" }
    - [ ] UpdateJiraIssue → logs "Updating issue", returns { success: true }
    - [ ] AddJiraComment → logs "Adding comment", returns { commentId: "123" }
    - [ ] Etc. (all operations return mock success)
  - [ ] Captures logs (timestamp, level, message) to result.logs
  - [ ] Implements retry logic (via step.config.retryPolicy):
    - [ ] Max retries, exponential backoff
    - [ ] On retry exhaustion: update step result with error
  - [ ] Implements timeout (via step.config.timeout):
    - [ ] If execution exceeds timeout: kill step, mark as failed
    - [ ] Log timeout error
  - [ ] Implements error handling (via step.config.onError):
    - [ ] onError="fail" → stop run, mark as failed
    - [ ] onError="continue" → log error, continue to next step
    - [ ] onError="skip" → skip step, continue (no error logged)
- [ ] Unit tests:
  - [ ] Step execution succeeds
  - [ ] Step retry logic works (fail, retry, succeed)
  - [ ] Step timeout triggers
  - [ ] Error handling: fail vs. continue vs. skip

### Task 3.10: Implement Run State Transitions
**Owner:** Backend Engineer 1  
**Duration:** 1.5 days  
**Depends on:** Task 3.9 + Task 1.8 (lifecycle)  
**Acceptance Criteria:**
- [ ] State transition manager created:
  - [ ] Validates state transitions (no invalid transitions)
  - [ ] Updates run status in DB with timestamp
  - [ ] Handles concurrency (optimistic locking or pessimistic)
  - [ ] Logs state changes to audit log
- [ ] Run lifecycle in worker:
  - [ ] Start: pending → running (set startedAt)
  - [ ] Each step: capture result
  - [ ] After all steps: running → succeeded or failed
  - [ ] Set finishedAt timestamp
  - [ ] Persist result object
- [ ] Timeout handling:
  - [ ] Pending timeout (5 min): pending → failed
  - [ ] Running timeout (per automation config, default 1h): running → failed
  - [ ] Log timeout reason
- [ ] Unit tests:
  - [ ] pending → running → succeeded
  - [ ] pending → running → failed
  - [ ] Pending timeout → failed
  - [ ] Running timeout → failed
  - [ ] Invalid transition rejected

### Task 3.11: Implement Audit Logging
**Owner:** Backend Engineer 2  
**Duration:** 1 day  
**Depends on:** Task 2.2 (DB schema)  
**Acceptance Criteria:**
- [ ] Audit logging middleware/helper created:
  - [ ] Takes action, actor (user ID), target (automation/run ID), optional details
  - [ ] Inserts into `audit_logs` table
  - [ ] Timestamp is server time (no client control)
  - [ ] Async (non-blocking)
- [ ] Audit entries for all sensitive operations:
  - [ ] CREATE_AUTOMATION, UPDATE_AUTOMATION, DELETE_AUTOMATION
  - [ ] TRIGGER_RUN, READ_RUN
  - [ ] All with actor (userId) and target (resource ID)
  - [ ] Failures also logged (e.g., DELETE_AUTOMATION_FAILED)
- [ ] No sensitive data logged (credentials, full payloads)
- [ ] Audit logs queryable (future: `GET /api/v1/audit-logs`)
- [ ] Tests:
  - [ ] Audit entry created for each action
  - [ ] Actor and target correctly recorded
  - [ ] Timestamps correct

### Task 3.12: Write Integration Test Suite
**Owner:** QA Lead  
**Duration:** 2 days  
**Depends on:** All Tasks 3.1–3.11  
**Acceptance Criteria:**
- [ ] Integration test suite created (`backend/tests/integration/`):
  - [ ] Test file per endpoint (automations.test.js, runs.test.js, etc.)
  - [ ] Fixtures for test data (sample automations, users)
  - [ ] Database setup/teardown (migrations in test DB)
- [ ] Tests for happy path + error paths:
  - [ ] Create, read, update, delete automations
  - [ ] Pagination, filtering
  - [ ] Run trigger, status check
  - [ ] Error handling (validation, auth, not found, conflict)
- [ ] Auth tests:
  - [ ] No token → 401
  - [ ] Expired token → 401
  - [ ] Invalid scope → 403
  - [ ] Valid token + scope → 200
- [ ] Data integrity tests:
  - [ ] Create automation → verify in DB
  - [ ] Update automation → verify changes persisted
  - [ ] Delete automation → verify removal from DB
  - [ ] Trigger run → verify run record created, status=pending
- [ ] Coverage target: >80% of API code
- [ ] Tests run in CI (GitHub Actions)

### Task 3.13: Ensure No Secrets in Logs/Errors
**Owner:** Backend Lead + Security  
**Duration:** 1 day  
**Depends on:** Tasks 3.1–3.12  
**Acceptance Criteria:**
- [ ] Code review for secrets in logs (grep for password, token, key, secret)
- [ ] Error responses sanitized (no stack traces, internal paths, or credentials)
- [ ] Logging middleware excludes sensitive headers (Authorization, X-API-Key)
- [ ] Test: trigger error with secret in request → error response does not include secret
- [ ] Security review sign-off

---

## Phase 4: Frontend MVP (Weeks 6–9)

### Task 4.1: Set Up React + Vite Project
**Owner:** Frontend Lead  
**Duration:** 1.5 days  
**Depends on:** Phase 2 complete  
**Acceptance Criteria:**
- [ ] Frontend project initialized (Vite template or manual setup)
- [ ] TypeScript configured (tsconfig.json, strict mode)
- [ ] Folder structure created:
  - [ ] `src/pages/` (page components)
  - [ ] `src/components/` (reusable components)
  - [ ] `src/services/` (API client)
  - [ ] `src/hooks/` (custom React hooks)
  - [ ] `src/context/` (state management)
  - [ ] `src/types/` (TypeScript types/interfaces)
  - [ ] `src/utils/` (helpers)
  - [ ] `public/` (static assets)
- [ ] Vite config:
  - [ ] Port 3000 (configurable)
  - [ ] API proxy to backend (http://localhost:4000)
  - [ ] Source maps enabled for debugging
  - [ ] Build optimizations configured
- [ ] ESLint & Prettier configured
- [ ] `npm run dev` starts dev server on port 3000
- [ ] `npm run build` produces minified bundle

### Task 4.2: Create API Client Service
**Owner:** Frontend Engineer 1  
**Duration:** 1.5 days  
**Depends on:** Task 4.1 + Task 3.7 (backend endpoints)  
**Acceptance Criteria:**
- [ ] API client created (`src/services/api.js` or `api.ts`):
  - [ ] Base URL from env variable (VITE_API_BASE_URL)
  - [ ] Interceptor for Authorization header (Bearer token)
  - [ ] Request/response serialization
  - [ ] Error handling (return error object or throw)
  - [ ] Correlation ID passed in header
- [ ] API methods (exported functions):
  - [ ] `getAutomations(limit, offset)` → GET /api/v1/automations
  - [ ] `getAutomation(id)` → GET /api/v1/automations/{id}
  - [ ] `createAutomation(data)` → POST /api/v1/automations
  - [ ] `updateAutomation(id, data)` → PUT /api/v1/automations/{id}
  - [ ] `deleteAutomation(id)` → DELETE /api/v1/automations/{id}
  - [ ] `triggerRun(automationId)` → POST /api/v1/automations/{id}/run
  - [ ] `getRun(runId)` → GET /api/v1/runs/{runId}
  - [ ] `getHealth()` → GET /api/v1/health
- [ ] Types/interfaces defined (TypeScript):
  - [ ] Automation, Run, RunEvent, Error (from spec schemas)
  - [ ] Request/response types
- [ ] Unit tests:
  - [ ] API methods called with correct URL/method/body
  - [ ] Authorization header added
  - [ ] Error responses handled

### Task 4.3: Create Login/Authentication Page
**Owner:** Frontend Engineer 2  
**Duration:** 1 day  
**Depends on:** Task 4.2 + Task 1.7 (auth spec)  
**Acceptance Criteria:**
- [ ] Login page component created (`src/pages/Login.tsx` or `.jsx`):
  - [ ] Form with API token input (or OAuth redirect button if using OAuth)
  - [ ] Button to authenticate
  - [ ] Error message display (invalid token, network error)
  - [ ] Loading state during login
- [ ] Authentication logic:
  - [ ] On submit: send token to backend (health check or validation endpoint)
  - [ ] On success: store token in localStorage/sessionStorage
  - [ ] Redirect to dashboard
  - [ ] On error: display error message
- [ ] Context/state management for auth:
  - [ ] Context created (`src/context/AuthContext.tsx`)
  - [ ] Provides: `user`, `token`, `isAuthenticated`, `login()`, `logout()`
  - [ ] Token persisted (localStorage), restored on app load
- [ ] Protected route wrapper:
  - [ ] `ProtectedRoute` component that redirects to login if not authenticated
- [ ] Tests:
  - [ ] Valid token → success, redirect to dashboard
  - [ ] Invalid token → error message
  - [ ] Token persisted after reload

### Task 4.4: Create Automation List Page
**Owner:** Frontend Engineer 1  
**Duration:** 2 days  
**Depends on:** Task 4.2 + Task 4.3  
**Acceptance Criteria:**
- [ ] List page component created (`src/pages/AutomationList.tsx`):
  - [ ] Displays table of automations (id, name, description, created date)
  - [ ] Pagination controls (limit, offset based on spec)
  - [ ] Total count displayed
  - [ ] Loading state (spinner) while fetching
  - [ ] Error state (error message, retry button)
  - [ ] Empty state message if no automations
- [ ] Actions per row:
  - [ ] View/Edit button → navigate to detail page
  - [ ] Delete button → confirm, then delete
  - [ ] Run button → trigger run
- [ ] Top-level actions:
  - [ ] Create automation button → navigate to editor
  - [ ] Filter/search (optional for MVP, can be in Task 4.8)
- [ ] Responsive design:
  - [ ] Table scrollable on mobile
  - [ ] Actions in dropdown menu on mobile (if needed)
- [ ] API integration:
  - [ ] Calls `getAutomations()` on mount
  - [ ] Pagination: update params, refetch
  - [ ] Delete: calls `deleteAutomation()`, refetch list
  - [ ] Run: calls `triggerRun()`, navigate to run detail
- [ ] Tests:
  - [ ] List loads and displays automations
  - [ ] Pagination works
  - [ ] Delete action works
  - [ ] Run action works

### Task 4.5: Create Automation Detail/Editor Page
**Owner:** Frontend Engineer 2  
**Duration:** 3 days  
**Depends on:** Task 4.2 + Task 1.2, 1.3 (schemas)  
**Acceptance Criteria:**
- [ ] Detail page component created (`src/pages/AutomationDetail.tsx`):
  - [ ] Displays automation in view mode (read-only) or edit mode (form)
  - [ ] Edit button toggles between view and edit modes
  - [ ] Fields:
    - [ ] Name (text input, required, max 255 chars)
    - [ ] Description (textarea, optional, max 1000 chars)
    - [ ] Triggers (repeatable, configurable per trigger type)
    - [ ] Steps (repeatable, drag-to-reorder, add/remove)
    - [ ] Save button (disabled if form invalid)
    - [ ] Cancel button (discards changes)
- [ ] Step editor component (`src/components/StepEditor.tsx`):
  - [ ] Dropdown to select step operation (from spec/operations.md list)
  - [ ] Dynamic form fields based on selected operation (from schema)
  - [ ] Retry policy configuration (maxRetries, backoffMs)
  - [ ] Error handling config (onError: fail/continue/skip)
  - [ ] Timeout configuration
  - [ ] Delete step button
  - [ ] Move up/down buttons (or drag)
- [ ] Trigger editor component (`src/components/TriggerEditor.tsx`):
  - [ ] Dropdown: Cron, Webhook, Manual
  - [ ] Conditional fields per trigger type:
    - [ ] Cron: expression input, timezone picker
    - [ ] Webhook: read-only URL display
    - [ ] Manual: (no fields)
  - [ ] Validation of cron expression (basic regex or library)
- [ ] Form validation:
  - [ ] Validate per JSON Schema (via Ajv library in frontend or mock)
  - [ ] Display inline error messages (field-level)
  - [ ] Disable submit if invalid
- [ ] API integration:
  - [ ] On load: `getAutomation(id)` (edit mode) or show empty form (create mode)
  - [ ] On save: `createAutomation()` or `updateAutomation()`
  - [ ] Success: navigate to list or show success message
  - [ ] Error: display error message, form remains editable
- [ ] Tests:
  - [ ] Load automation → displays correctly
  - [ ] Edit automation → save → verify API call
  - [ ] Create automation → save → verify API call
  - [ ] Form validation → errors displayed
  - [ ] Cancel → discards changes

### Task 4.6: Create Run History/Status Page
**Owner:** Frontend Engineer 1  
**Duration:** 2 days  
**Depends on:** Task 4.2 + Task 4.4  
**Acceptance Criteria:**
- [ ] Run list page component (`src/pages/RunList.tsx` or filter on detail page):
  - [ ] Display runs for an automation (or all runs if global view)
  - [ ] Table columns: runId, automationId, status, startedAt, finishedAt, duration
  - [ ] Status badge (color-coded: pending=yellow, running=blue, succeeded=green, failed=red)
  - [ ] Pagination (similar to automation list)
  - [ ] Click row to view run details
  - [ ] Polling or manual refresh to see live status
- [ ] Run detail page component (`src/pages/RunDetail.tsx`):
  - [ ] Display run status, timestamps, result
  - [ ] Logs section: display logs array (timestamp, level, message)
  - [ ] Logs can be filtered by level (debug, info, warn, error)
  - [ ] Logs are scrollable (or paginated if large)
  - [ ] Error details displayed if run failed
  - [ ] Result/output displayed if run succeeded
  - [ ] Auto-refresh while run is in progress (poll every 2-5 seconds)
  - [ ] Stop auto-refresh when run completes
- [ ] API integration:
  - [ ] `getRun(runId)` on mount and during polling
  - [ ] Handle error responses gracefully
- [ ] Tests:
  - [ ] Run list loads
  - [ ] Clicking run navigates to detail
  - [ ] Auto-refresh works
  - [ ] Logs display correctly

### Task 4.7: Create Consumer Contract Tests (Pact)
**Owner:** QA Lead  
**Duration:** 2 days  
**Depends on:** Task 4.2 + Task 2.4 (Pact setup)  
**Acceptance Criteria:**
- [ ] Consumer Pact tests created (`frontend/tests/contract/`):
  - [ ] `automations.pact.test.js` (or .ts):
    - [ ] Test: create automation → POST /api/v1/automations
    - [ ] Test: get automations → GET /api/v1/automations
    - [ ] Test: get automation → GET /api/v1/automations/{id}
    - [ ] Test: update automation → PUT /api/v1/automations/{id}
    - [ ] Test: delete automation → DELETE /api/v1/automations/{id}
  - [ ] `runs.pact.test.js`:
    - [ ] Test: trigger run → POST /api/v1/automations/{id}/run
    - [ ] Test: get run → GET /api/v1/runs/{runId}
- [ ] Each test:
  - [ ] Defines expected request (method, path, headers, body)
  - [ ] Defines expected response (status, headers, body structure)
  - [ ] Uses Pact mock server to mock backend
  - [ ] Executes API client code
  - [ ] Verifies mock was called as expected
  - [ ] Generates Pact file (`pacts/frontend-backend.json`)
- [ ] Pact runs in CI after unit tests
- [ ] Pact is published to broker (or saved for manual verification by backend)
- [ ] Tests pass

### Task 4.8: Implement Error Handling & User Feedback
**Owner:** Frontend Engineer 2  
**Duration:** 1.5 days  
**Depends on:** Task 4.1 + Task 1.6 (error spec)  
**Acceptance Criteria:**
- [ ] Error handling component/context:
  - [ ] Captures API errors globally (network, 4xx, 5xx)
  - [ ] Formats error messages for user (code → human-readable)
  - [ ] Displays toast/modal with error
- [ ] Validation error feedback:
  - [ ] Field-level errors displayed inline (red text below field)
  - [ ] Submit button disabled if form invalid
  - [ ] Error cleared when field corrected
- [ ] User feedback components:
  - [ ] Toast notifications (success, error, warning)
  - [ ] Loading spinners on buttons and pages
  - [ ] Confirmation modals (delete, overwrite)
  - [ ] Error boundary (catch React errors, display fallback)
- [ ] Empty states:
  - [ ] No automations → "Create your first automation" with button
  - [ ] No runs → "No runs yet"
- [ ] Network error recovery:
  - [ ] Retry button on error states
  - [ ] Auto-retry with exponential backoff (or manual only)
- [ ] Tests:
  - [ ] API error → user sees friendly message
  - [ ] Validation error → inline error message
  - [ ] Network error → can retry

### Task 4.9: Implement Styling & Responsive Design
**Owner:** Frontend Lead  
**Duration:** 2 days  
**Depends on:** All Task 4.x  
**Acceptance Criteria:**
- [ ] CSS framework chosen (Tailwind, Bootstrap, Material-UI, etc.)
- [ ] Color scheme defined (light mode, dark mode if applicable)
- [ ] Responsive breakpoints:
  - [ ] Mobile (< 640px)
  - [ ] Tablet (640-1024px)
  - [ ] Desktop (>1024px)
- [ ] Components styled:
  - [ ] Buttons, inputs, tables, modals, toasts
  - [ ] Consistent spacing, typography, colors
- [ ] Accessibility:
  - [ ] Color contrast passes WCAG AA
  - [ ] Keyboard navigation (Tab, Enter, Escape)
  - [ ] ARIA labels on interactive elements
  - [ ] Focus visible on inputs/buttons
- [ ] Dark mode (optional but nice to have)
- [ ] Screenshots/visual regression tests (optional for MVP)
- [ ] QA sign-off (UI looks good, responsive)

### Task 4.10: Build & Optimize Frontend Bundle
**Owner:** Frontend Lead  
**Duration:** 1 day  
**Depends on:** Task 4.9  
**Acceptance Criteria:**
- [ ] Vite build optimizations:
  - [ ] Code splitting (separate vendor chunks, component chunks)
  - [ ] Lazy loading for routes (dynamic import)
  - [ ] Minification (CSS, JS)
  - [ ] Asset optimization (images, fonts)
- [ ] Bundle size analyzed:
  - [ ] `npm run build` produces summary
  - [ ] Main bundle <150KB (gzipped)
  - [ ] Vendor bundle <200KB (gzipped)
- [ ] Build time acceptable (<30 seconds)
- [ ] Sourcemaps enabled for production debugging
- [ ] Docker image created for frontend:
  - [ ] `frontend/Dockerfile` (multi-stage: build, serve with nginx)
  - [ ] Image size reasonable (<200MB)
- [ ] CI integration: build job validates bundle size

### Task 4.11: Write Frontend Integration Tests
**Owner:** QA Lead  
**Duration:** 2 days  
**Depends on:** All Task 4.x  
**Acceptance Criteria:**
- [ ] Integration test suite created (`frontend/tests/integration/`):
  - [ ] Test file per page (Login.test.js, AutomationList.test.js, etc.)
  - [ ] Mock API responses (MSW - Mock Service Worker, or stub)
- [ ] Tests for user flows:
  - [ ] Login flow: enter token, submit, redirect to dashboard
  - [ ] Create automation: fill form, submit, see in list
  - [ ] Edit automation: change field, save, see updated
  - [ ] Delete automation: click delete, confirm, removed from list
  - [ ] Trigger run: click run button, navigate to run detail, see status
  - [ ] View run: see logs, status updates
- [ ] Error scenarios:
  - [ ] API error → error message displayed, can retry
  - [ ] Invalid form → error highlighted, submit disabled
  - [ ] Network error → handled gracefully
- [ ] Coverage target: >60% (lower than backend due to UI complexity)
- [ ] Tests run in CI (GitHub Actions)

---

## Phase 5: Jira/Confluence Integration (Weeks 9–11)

### Task 5.1: Create Jira API Client Library
**Owner:** Backend Engineer 1  
**Duration:** 2 days  
**Depends on:** Task 3.8 (worker) + Task 1.10 (spec)  
**Acceptance Criteria:**
- [ ] Jira client created (`backend/src/clients/jira.js`):
  - [ ] Constructor takes Jira instance URL and auth credentials (token or OAuth)
  - [ ] Methods for API operations:
    - [ ] `createIssue(project, summary, description, type)` → returns issueKey
    - [ ] `updateIssue(issueKey, fields)` → updates fields (summary, description, assignee, etc.)
    - [ ] `transitionIssue(issueKey, transitionId, fields)` → moves issue in workflow
    - [ ] `addComment(issueKey, comment)` → adds comment, returns commentId
    - [ ] `getIssue(issueKey)` → retrieves issue details
  - [ ] HTTP client configured (axios or node-fetch):
    - [ ] Base URL, headers, auth injection
    - [ ] Timeout handling
    - [ ] Retries for transient errors (5xx, 429)
    - [ ] Rate limit handling (backoff on 429)
  - [ ] Error handling:
    - [ ] Catches HTTP errors, throws custom exception with code/message
    - [ ] 401 → authentication error
    - [ ] 404 → not found
    - [ ] 400 → validation error
    - [ ] 429 → rate limited
    - [ ] 5xx → server error (retryable)
  - [ ] Logging:
    - [ ] All requests logged (with correlation ID)
    - [ ] Sensitive data (credentials, tokens) NOT logged
- [ ] Unit tests:
  - [ ] Mock Jira API responses
  - [ ] Successful operation → correct API call, return value
  - [ ] API error → throws exception with correct code/message
  - [ ] Retry logic: transient error → retry → success

### Task 5.2: Create Confluence API Client Library
**Owner:** Backend Engineer 2  
**Duration:** 2 days  
**Depends on:** Task 5.1 (similar pattern)  
**Acceptance Criteria:**
- [ ] Confluence client created (`backend/src/clients/confluence.js`):
  - [ ] Constructor takes Confluence URL and auth
  - [ ] Methods:
    - [ ] `createPage(spaceKey, title, body)` → returns pageId
    - [ ] `updatePage(pageId, title, body, version)` → updates page
    - [ ] `addComment(pageId, comment)` → adds comment
    - [ ] `getPage(pageId)` → retrieves page details
    - [ ] `movePage(pageId, parentId)` → moves page in hierarchy
  - [ ] Same HTTP/error/logging patterns as Jira client
- [ ] Unit tests (same structure as Jira)

### Task 5.3: Create Operation Handlers for Jira
**Owner:** Backend Engineer 1  
**Duration:** 2 days  
**Depends on:** Task 5.1 + Task 3.9 (step executor) + Task 1.11 (operations)  
**Acceptance Criteria:**
- [ ] Step handlers created (in `backend/src/worker/handlers/`):
  - [ ] `CreateJiraIssueHandler.js`:
    - [ ] Input: { project, summary, description, issueType }
    - [ ] Calls jiraClient.createIssue()
    - [ ] Output: { issueKey, url }
    - [ ] Errors: validation error, auth error, not found
  - [ ] `UpdateJiraIssueHandler.js`:
    - [ ] Input: { issueKey, fields: { summary, description, assignee, ... } }
    - [ ] Calls jiraClient.updateIssue()
    - [ ] Output: { success: true, issueKey }
  - [ ] `TransitionJiraIssueHandler.js`:
    - [ ] Input: { issueKey, transitionId, fields }
    - [ ] Calls jiraClient.transitionIssue()
    - [ ] Output: { success: true, issueKey, newStatus }
  - [ ] `AddJiraCommentHandler.js`:
    - [ ] Input: { issueKey, comment }
    - [ ] Calls jiraClient.addComment()
    - [ ] Output: { commentId, url }
- [ ] Each handler:
  - [ ] Validates input (required fields, formats)
  - [ ] Calls API client
  - [ ] Captures result
  - [ ] Handles errors (returns error object, not throws)
  - [ ] Logs operation details (not credentials)
- [ ] Step executor routes to handler based on operation name
- [ ] Unit tests for each handler:
  - [ ] Valid input → success result
  - [ ] Invalid input → validation error
  - [ ] API error → error result

### Task 5.4: Create Operation Handlers for Confluence
**Owner:** Backend Engineer 2  
**Duration:** 2 days  
**Depends on:** Task 5.2 + Task 3.9  
**Acceptance Criteria:**
- [ ] Handlers:
  - [ ] `CreateConfluencePageHandler.js`
  - [ ] `UpdateConfluencePageHandler.js`
  - [ ] `AddConfluenceCommentHandler.js`
  - [ ] `MoveConfluencePageHandler.js`
- [ ] Same structure as Jira handlers
- [ ] Unit tests for each

### Task 5.5: Implement Credential Management
**Owner:** Backend Lead + DevOps  
**Duration:** 2 days  
**Depends on:** Task 1.10 (spec)  
**Acceptance Criteria:**
- [ ] Credential storage strategy decided:
  - [ ] Option 1: HashiCorp Vault (or similar)
  - [ ] Option 2: Environment variables (for testing)
  - [ ] Option 3: Encrypted DB storage
- [ ] For MVP: use Option 2 (env vars for testing) or Option 3 (if short-term)
- [ ] Credential retrieval service created (`backend/src/services/credentials.js`):
  - [ ] `getJiraCredential(automationId)` → { url, token/password }
  - [ ] `getConfluenceCredential(automationId)` → { url, token/password }
  - [ ] Errors if credential not found (automation doesn't have integration set up)
- [ ] Credentials linked to automations:
  - [ ] Automation object can specify credential ID or key
  - [ ] Step executor retrieves credentials before calling handlers
- [ ] Security:
  - [ ] Credentials never logged
  - [ ] Credentials never returned in API responses
  - [ ] Credentials rotated manually or via integration config (future)
- [ ] Testing setup:
  - [ ] Test credentials provided for Jira/Confluence sandboxes
  - [ ] Test credentials loaded from env variables in CI
- [ ] Unit tests:
  - [ ] Retrieve credential successfully
  - [ ] Credential not found → error
  - [ ] Sensitive data not exposed

### Task 5.6: Set Up Jira/Confluence Sandbox Environments
**Owner:** DevOps  
**Duration:** 1.5 days  
**Depends on:** None (parallel)  
**Acceptance Criteria:**
- [ ] Jira sandbox instance provisioned (or existing dev instance)
  - [ ] URL documented
  - [ ] Test project created (e.g., "DEMO", "AUTOMATION")
  - [ ] Test user account with API token
  - [ ] Token stored in GitHub Secrets (JIRA_TEST_TOKEN, JIRA_TEST_URL)
- [ ] Confluence sandbox instance provisioned
  - [ ] URL documented
  - [ ] Test space created
  - [ ] Test user account with API token
  - [ ] Token stored in GitHub Secrets
- [ ] Network access verified (backend can reach sandboxes from CI)
- [ ] Documentation in `infra/SANDBOX_SETUP.md`:
  - [ ] How to request sandbox access
  - [ ] How to create test project/space
  - [ ] API token generation steps

### Task 5.7: Implement Integration Tests Against Sandbox
**Owner:** QA Lead + Backend Engineer  
**Duration:** 3 days  
**Depends on:** Tasks 5.3–5.6  
**Acceptance Criteria:**
- [ ] Integration test suite created (`backend/tests/integration/jira-confluence/`):
  - [ ] `jira-operations.test.js`:
    - [ ] Create issue in test project → verify in Jira
    - [ ] Update issue → verify changes
    - [ ] Add comment → verify comment appears
    - [ ] Transition issue → verify status changed
  - [ ] `confluence-operations.test.js`:
    - [ ] Create page in test space → verify in Confluence
    - [ ] Update page → verify changes
    - [ ] Add comment → verify comment appears
  - [ ] End-to-end test:
    - [ ] Create automation with Jira steps
    - [ ] Trigger run
    - [ ] Verify run succeeds
    - [ ] Verify issue created in Jira
- [ ] Tests:
  - [ ] Use sandbox credentials from env
  - [ ] Create test data with unique names (timestamp-based to avoid conflicts)
  - [ ] Clean up test data after run (or mark as test)
  - [ ] Robust error handling (retry on transient failures)
- [ ] CI integration:
  - [ ] Tests run in CI after unit tests (or in separate workflow)
  - [ ] Sandbox credentials available via GitHub Secrets
  - [ ] Failures reported with sandbox URL for manual investigation

### Task 5.8: Implement Rate Limiting & Resilience
**Owner:** Backend Engineer 1  
**Duration:** 1.5 days  
**Depends on:** Tasks 5.1–5.2  
**Acceptance Criteria:**
- [ ] Rate limiting strategy:
  - [ ] Monitor Jira/Confluence rate limit headers (X-RateLimit-*)
  - [ ] Implement exponential backoff when rate limited (429)
  - [ ] Queue requests if near rate limit
  - [ ] Log rate limit events
- [ ] Circuit breaker pattern:
  - [ ] Track consecutive failures to Jira/Confluence
  - [ ] Open circuit if threshold exceeded (e.g., 5 failures)
  - [ ] Half-open state: allow test request, close if success
  - [ ] Failure: retry after interval (exponential backoff)
  - [ ] Log circuit state changes
- [ ] Timeout handling:
  - [ ] Per-request timeout (10-30 seconds)
  - [ ] Per-run timeout (1-24 hours, configured per automation)
  - [ ] On timeout: mark run/step as failed, log reason
- [ ] Retry logic:
  - [ ] Retryable errors: 5xx, 429, network timeouts
  - [ ] Non-retryable: 4xx (except 429), 401, 403
  - [ ] Backoff formula: baseMs * (2 ^ retryCount) with jitter
  - [ ] Max retries per step (from spec)
- [ ] Unit tests:
  - [ ] Rate limit response → backoff applied
  - [ ] Circuit breaker opens/closes
  - [ ] Timeout triggers
  - [ ] Retries succeed after transient error

### Task 5.9: Handle OAuth Token Refresh (if applicable)
**Owner:** Backend Lead  
**Duration:** 1.5 days  
**Depends on:** Task 5.5 (credentials)  
**Acceptance Criteria:**
- [ ] If using OAuth (not just API tokens):
  - [ ] Token refresh endpoint called when token expired (401)
  - [ ] Refresh token stored securely (vault)
  - [ ] New access token stored in vault
  - [ ] Request retried with new token
  - [ ] Refresh fails → mark automation as requiring re-authentication
- [ ] Unit tests:
  - [ ] Expired token → refresh succeeds → retry succeeds
  - [ ] Refresh fails → error returned
  - [ ] Refresh token itself invalid → authentication error

### Task 5.10: Security Review of Integrations
**Owner:** Security Reviewer  
**Duration:** 1 day  
**Depends on:** Tasks 5.1–5.9  
**Acceptance Criteria:**
- [ ] Code review for security issues:
  - [ ] No credentials hardcoded
  - [ ] No credentials logged
  - [ ] HTTPS used for all external calls (TLS verification)
  - [ ] Input validation (SQL injection, script injection prevention)
  - [ ] Error messages don't leak sensitive info
  - [ ] Rate limiting prevents abuse
  - [ ] OAuth state parameter validated (if applicable)
- [ ] Dependency scan:
  - [ ] Dependencies checked for known vulnerabilities (npm audit)
  - [ ] Vulnerable packages updated or isolated
- [ ] Penetration testing (lightweight):
  - [ ] Attempt to bypass credential storage
  - [ ] Attempt to exfiltrate tokens
  - [ ] Attempt to execute commands via step parameters
- [ ] Sign-off document created: `security/integration-review.md`

---

## Phase 6: Advanced Features & Polish (Weeks 11–13)

### Task 6.1: Implement Cron Trigger Scheduling
**Owner:** Backend Engineer 1  
**Duration:** 2 days  
**Depends on:** Task 1.4 (triggers spec) + Task 3.6  
**Acceptance Criteria:**
- [ ] Cron scheduler implemented:
  - [ ] Library chosen (node-cron, cron, or similar)
  - [ ] For each automation with cron trigger:
    - [ ] Parse cron expression
    - [ ] Schedule job at start time
    - [ ] On trigger: enqueue run (same as manual trigger)
  - [ ] Scheduler restarts on server restart (jobs recreated from DB)
  - [ ] Timezone support (IANA zones from spec)
- [ ] Database:
  - [ ] Trigger config stored in automation definition
  - [ ] Schedule state (last run time) optional (for display)
- [ ] Logging:
  - [ ] Cron trigger fired → log with correlationId
  - [ ] Job enqueued → log
  - [ ] Job failed to enqueue → error alert
- [ ] Unit tests:
  - [ ] Cron expression parsed
  - [ ] Job scheduled at correct time
  - [ ] Job fires and enqueues run

### Task 6.2: Implement Webhook Trigger Support
**Owner:** Backend Engineer 2  
**Duration:** 1.5 days  
**Depends on:** Task 1.4 (triggers spec) + Task 3.6  
**Acceptance Criteria:**
- [ ] Webhook endpoint created:
  - [ ] `POST /api/v1/webhooks/automations/{automationId}/{webhookId}` (or similar)
  - [ ] No authentication required (or API key in URL)
  - [ ] Accepts any JSON body (from external source)
  - [ ] Enqueues run (same as manual trigger, but with webhook payload as context)
- [ ] Webhook URL generation:
  - [ ] When automation with webhook trigger is created
  - [ ] URL format stable and predictable
  - [ ] URL includes automation ID and webhook token
- [ ] Idempotency:
  - [ ] Prevent duplicate runs on webhook retry (use idempotency key from header or body)
  - [ ] Store processed webhook IDs, reject duplicates with 409
- [ ] Rate limiting:
  - [ ] Limit requests per webhook (e.g., 100/min)
  - [ ] Return 429 if exceeded
- [ ] Logging:
  - [ ] Webhook payload logged (sanitized)
  - [ ] Run enqueued → logged
- [ ] Unit tests:
  - [ ] Webhook call → run enqueued
  - [ ] Duplicate webhook → rejected
  - [ ] Rate limit → 429

### Task 6.3: Implement Advanced Pagination & Filtering
**Owner:** Backend Engineer 1  
**Duration:** 1 day  
**Depends on:** Task 3.5 (list endpoint)  
**Acceptance Criteria:**
- [ ] Pagination:
  - [ ] Cursor-based pagination (or offset-based, choice from spec)
  - [ ] Query params: `limit` (default 20, max 100), `cursor` or `offset`
  - [ ] Response includes: `data`, `limit`, `nextCursor` (or `offset`)
  - [ ] Stable sort order (by created_at or id, then by name)
- [ ] Filtering:
  - [ ] By status (if applicable)
  - [ ] By creation date (range: from, to)
  - [ ] By owner/creator (if multi-user)
  - [ ] By tags (if tags field exists)
- [ ] Sorting:
  - [ ] Query param: `sort=field:asc` (or similar)
  - [ ] Allowed fields: name, createdAt, updatedAt
  - [ ] Default: createdAt:desc
- [ ] Full-text search (optional):
  - [ ] Query param: `search=<text>`
  - [ ] Searches name + description
- [ ] Database optimization:
  - [ ] Indexes on filter/sort columns
  - [ ] Query plans reviewed
- [ ] Unit tests:
  - [ ] Pagination works
  - [ ] Filtering works
  - [ ] Sorting works
  - [ ] Search works
  - [ ] Invalid params handled gracefully

### Task 6.4: Implement Run Log Filtering & Streaming
**Owner:** Backend Engineer 2  
**Duration:** 1.5 days  
**Depends on:** Task 3.7 (run status endpoint)  
**Acceptance Criteria:**
- [ ] Log filtering:
  - [ ] Query params: `level` (debug, info, warn, error)
  - [ ] Return only logs at or above level (error logs when level=warn)
  - [ ] Pagination: limit, offset
- [ ] Log streaming (optional for MVP, nice to have):
  - [ ] WebSocket endpoint: `/api/v1/runs/{runId}/logs/stream`
  - [ ] Client connects, receives log entries as run progresses
  - [ ] Close connection when run completes
  - [ ] Or use polling (frontend polls every 2-5 seconds)
- [ ] Large log handling:
  - [ ] Logs truncated if exceeds size (e.g., 10MB per run)
  - [ ] Oldest logs dropped
  - [ ] Note in response: "logs truncated"
- [ ] Tests:
  - [ ] Log filtering by level works
  - [ ] Pagination works
  - [ ] Streaming works (or polling)

### Task 6.5: Implement Audit Log Querying
**Owner:** Backend Engineer 1  
**Duration:** 1 day  
**Depends on:** Task 3.11 (audit logs)  
**Acceptance Criteria:**
- [ ] Audit log endpoint created:
  - [ ] `GET /api/v1/audit-logs` (admin only)
  - [ ] Pagination: limit, offset
  - [ ] Filtering: by actor, action, target, date range
  - [ ] Sorting: by createdAt
- [ ] Response format:
  - [ ] { data: [...], limit, offset, total }
  - [ ] Each entry: { id, actor, action, target, createdAt }
- [ ] Retention policy:
  - [ ] Logs kept for N days (e.g., 90 days)
  - [ ] Automated cleanup: delete logs older than retention
  - [ ] Or archive to cold storage (future)
- [ ] Scope:
  - [ ] Requires `admin` scope (or similar)
- [ ] Tests:
  - [ ] Query audit logs
  - [ ] Filter by action
  - [ ] Pagination works
  - [ ] Unauthorized access rejected

### Task 6.6: Set Up Prometheus Metrics & Dashboarding
**Owner:** DevOps Lead  
**Duration:** 2 days  
**Depends on:** Task 2.6 (metrics endpoint)  
**Acceptance Criteria:**
- [ ] Additional metrics defined (beyond basic from Phase 2):
  - [ ] `automations_total` (gauge or counter by status)
  - [ ] `runs_queued_total` (gauge, current queue depth)
  - [ ] `runs_success_rate` (gauge, percentage)
  - [ ] `run_duration_seconds` (histogram by automation)
  - [ ] `step_duration_seconds` (histogram by operation)
  - [ ] `jira_api_calls_total` (counter by operation, status)
  - [ ] `confluence_api_calls_total` (counter by operation, status)
  - [ ] `db_query_errors_total` (counter)
  - [ ] `queue_processing_time_seconds` (histogram)
- [ ] Monitoring stack (local and optional for prod):
  - [ ] Prometheus scrape config in `infra/prometheus.yml`
  - [ ] Grafana dashboard created: `infra/grafana-dashboard.json`
  - [ ] Dashboard shows:
    - [ ] Runs over time (success/failure)
    - [ ] API latency (p50, p95, p99)
    - [ ] Queue depth and processing rate
    - [ ] Error rate by operation
    - [ ] Resource usage (CPU, memory, DB connections)
  - [ ] Docker Compose extended (optional): add Prometheus, Grafana services
- [ ] Alerting rules:
  - [ ] Alert if error rate > 5% for 5 minutes
  - [ ] Alert if queue depth > 1000
  - [ ] Alert if API latency p95 > 500ms
  - [ ] Alert if Jira/Confluence API unreachable
  - [ ] Rules file: `infra/prometheus-alerts.yml`
- [ ] Documentation:
  - [ ] How to view dashboard
  - [ ] How to interpret metrics
  - [ ] How to add custom metrics

### Task 6.7: Implement Feature Flags (Optional)
**Owner:** Backend Lead  
**Duration:** 1 day  
**Depends on:** None (independent)  
**Acceptance Criteria:**
- [ ] Feature flag library chosen (LaunchDarkly, Unleash, or simple env-based)
- [ ] For MVP: simple env-based flags (e.g., `FEATURE_CRON_ENABLED=true`)
- [ ] Flags:
  - [ ] `FEATURE_CRON_ENABLED` — enable/disable cron triggers
  - [ ] `FEATURE_WEBHOOK_ENABLED` — enable/disable webhook triggers
  - [ ] `FEATURE_ADVANCED_FILTERING` — enable/disable advanced search
- [ ] Usage:
  - [ ] Check flag before executing feature
  - [ ] Log flag state (for debugging)
- [ ] Testing:
  - [ ] Unit tests with flags enabled/disabled
- [ ] Documentation:
  - [ ] All flags documented in README or `infra/.env.example`

### Task 6.8: Implement Performance Optimizations
**Owner:** Backend Engineer + DevOps  
**Duration:** 1.5 days  
**Depends on:** Phase 5 complete  
**Acceptance Criteria:**
- [ ] Database optimizations:
  - [ ] Query analysis (EXPLAIN PLAN for slow queries)
  - [ ] Indexes added (if needed)
  - [ ] Connection pooling tuned
  - [ ] Slow query log enabled
- [ ] Caching (optional for MVP):
  - [ ] Cache automation definitions (TTL 5-10 min)
  - [ ] Invalidate on update
- [ ] API response optimization:
  - [ ] Compress responses (gzip)
  - [ ] Return only needed fields (projection)
  - [ ] Lazy load related data (if needed)
- [ ] Worker optimization:
  - [ ] Batch job dequeue (process multiple jobs per cycle)
  - [ ] Connection pooling to external APIs
  - [ ] Parallel step execution (if spec allows)
- [ ] Frontend optimization:
  - [ ] Code splitting verified
  - [ ] Lazy loading working
  - [ ] Bundle size <300KB gzipped
  - [ ] Images optimized
- [ ] Benchmarking:
  - [ ] Create performance test: create 100 automations, trigger 100 runs
  - [ ] Measure: API response times, queue processing time, run duration
  - [ ] Document baseline and targets

---

## Phase 7: Testing & QA (Weeks 12–14)

### Task 7.1: Execute Full Acceptance Test Suite
**Owner:** QA Lead  
**Duration:** 2 days  
**Depends on:** All previous phases (but parallel with Phase 6)  
**Acceptance Criteria:**
- [ ] Test matrix from spec executed:
  - [ ] Create automation: valid schema → created
  - [ ] Create automation: invalid schema → 400
  - [ ] Run automation: trigger → 202 with runId
  - [ ] Run lifecycle: pending → running → succeeded/failed
  - [ ] Auth: no token → 401; wrong scope → 403
  - [ ] Concurrency: parallel runs / update during run (per policy)
  - [ ] Jira integration: create/update/transition/comment succeeds
  - [ ] Confluence integration: create/update/comment succeeds
  - [ ] Error scenarios: API error → run fails, logged
  - [ ] Timeouts: run timeout → failed
  - [ ] Retries: transient error → retry → success
- [ ] All tests pass
- [ ] Test results documented: `work/TEST_RESULTS.md`

### Task 7.2: Contract Test Verification
**Owner:** QA Lead  
**Duration:** 1 day  
**Depends on:** Task 4.7 (consumer tests) + Task 3.12 (provider tests)  
**Acceptance Criteria:**
- [ ] Consumer Pacts generated (by frontend tests)
- [ ] Pacts published to broker (or saved)
- [ ] Backend provider tests run and verify all Pacts
- [ ] All verifications pass
- [ ] CI job: contract tests in pipeline, passing

### Task 7.3: Execute Security Testing
**Owner:** Security + QA  
**Duration:** 1.5 days  
**Depends on:** Phase 5 complete (integrations)  
**Acceptance Criteria:**
- [ ] OWASP Top 10 review:
  - [ ] **A1: Injection** — test SQL injection, script injection (none successful)
  - [ ] **A2: Broken Auth** — test credential bypass, token replay, scope escalation (none successful)
  - [ ] **A3: Sensitive Data Exposure** — verify HTTPS, data encryption at rest (if applicable), log sanitization (credentials not logged)
  - [ ] **A4: XML External Entity** — not applicable (using JSON)
  - [ ] **A5: Broken Access Control** — test authorization bypass, user accessing other's resources (denied)
  - [ ] **A6: Security Misconfiguration** — check exposed endpoints, default creds, debug endpoints in prod (none exposed)
  - [ ] **A7: Cross-Site Scripting (XSS)** — test input sanitization, script injection in step parameters (sanitized)
  - [ ] **A8: Insecure Deserialization** — check JSON deserialization, no arbitrary code execution
  - [ ] **A9: Using Components with Known Vulnerabilities** — npm audit, dependency scanning (no known CVE)
  - [ ] **A10: Insufficient Logging & Monitoring** — verify all sensitive actions logged, audit trail complete
- [ ] Penetration testing (lightweight):
  - [ ] Attempt to access other user's automations (403)
  - [ ] Attempt to elevate privileges (fail)
  - [ ] Attempt to inject SQL (sanitized or parameterized)
  - [ ] Attempt to exfiltrate credentials (blocked)
- [ ] Credential handling audit:
  - [ ] No credentials in logs (grep test)
  - [ ] Credentials in vault or env (secure)
  - [ ] Token refresh working
  - [ ] Rotation policy documented
- [ ] Report: `security/penetration-test-report.md`

### Task 7.4: Execute Load & Performance Testing
**Owner:** QA + DevOps  
**Duration:** 2 days  
**Depends on:** Phase 5 complete  
**Acceptance Criteria:**
- [ ] Load test scenarios:
  - [ ] Scenario 1: 100 concurrent users, continuous load for 5 minutes
    - [ ] Baseline: response times, error rate, queue depth
    - [ ] Acceptable: <5% errors, p95 latency <500ms, queue processes
  - [ ] Scenario 2: 500 concurrent automations executing simultaneously
    - [ ] Baseline: queue throughput, worker processing time
    - [ ] Acceptable: all runs complete within 1 hour (or SLA target)
  - [ ] Scenario 3: 1000 API requests/sec
    - [ ] Baseline: API response time, connection pool
    - [ ] Acceptable: <1% errors, p95 <200ms
- [ ] Database stress test:
  - [ ] Scenario: 10K automations, 100K runs
  - [ ] Baseline: query time, connection pool
  - [ ] Acceptable: queries <100ms, connections pooled
- [ ] Frontend performance:
  - [ ] Load automation list (10K items)
  - [ ] Baseline: page load time, scroll performance
  - [ ] Acceptable: <2s load, smooth scroll
- [ ] Report: `work/LOAD_TEST_RESULTS.md`
  - [ ] Metrics, baseline, acceptable range, results, issues found

### Task 7.5: Execute UAT with Product Owner
**Owner:** QA Lead + Product Owner  
**Duration:** 1.5 days  
**Depends on:** All previous phases (but parallel with Phase 6 end)  
**Acceptance Criteria:**
- [ ] UAT environment prepared (staging or prod-like)
- [ ] UAT test cases defined (derived from user stories):
  - [ ] Create automation with cron trigger
  - [ ] Manually trigger automation
  - [ ] View run history and logs
  - [ ] Update automation
  - [ ] Handle automation failure (error visible to user)
  - [ ] Create automation with multiple Jira steps
- [ ] Product owner executes test cases:
  - [ ] All test cases pass (or documented failures)
  - [ ] UI/UX acceptable (layout, colors, responsiveness)
  - [ ] Performance acceptable (load times, responsiveness)
  - [ ] Documentation clear (help text, error messages)
- [ ] Feedback documented:
  - [ ] Issues/bugs found → prioritized (P0/P1/P2)
  - [ ] Suggestions captured
  - [ ] Sign-off: "Ready for production" or "Fix issues before launch"

### Task 7.6: Create System Documentation
**Owner:** Tech Writer or Lead  
**Duration:** 1.5 days  
**Depends on:** All phases  
**Acceptance Criteria:**
- [ ] User documentation:
  - [ ] Getting started guide
  - [ ] How to create automation
  - [ ] How to set up Jira/Confluence credentials
  - [ ] How to trigger and monitor runs
  - [ ] Troubleshooting guide
  - [ ] FAQ
- [ ] API documentation (generated from OpenAPI):
  - [ ] Endpoint reference
  - [ ] Error codes
  - [ ] Example requests/responses
  - [ ] Authentication guide
- [ ] Operations documentation (`infra/ops.md`):
  - [ ] Deployment checklist
  - [ ] Incident response (alert → resolution)
  - [ ] Scaling procedures
  - [ ] Database backup/restore
  - [ ] Log analysis
- [ ] Architecture documentation:
  - [ ] System diagram
  - [ ] Data flow
  - [ ] Component interactions
  - [ ] Technology choices & rationale
- [ ] All docs in repo (Markdown or wiki format)

### Task 7.7: Fix Issues & Regressions
**Owner:** Full team  
**Duration:** 1 day  
**Depends on:** Tasks 7.1–7.6 (testing results)  
**Acceptance Criteria:**
- [ ] P0 issues (critical) fixed immediately
- [ ] P1 issues (high) fixed before launch
- [ ] P2 issues (medium) documented for v1.1
- [ ] No new regressions introduced
- [ ] All tests pass again

---

## Phase 8: Deployment & Launch (Weeks 14–16)

### Task 8.1: Prepare Infrastructure as Code
**Owner:** DevOps Lead  
**Duration:** 2 days  
**Depends on:** Phase 7 complete  
**Acceptance Criteria:**
- [ ] Kubernetes manifests created (or Cloud Run, ECS, etc.):
  - [ ] `backend.yaml` — deployment, service, replicas
  - [ ] `frontend.yaml` — deployment (or cloud static hosting)
  - [ ] `postgres.yaml` — stateful set, PVC for persistence
  - [ ] `ingress.yaml` — URL routing, TLS termination
  - [ ] Resource limits: CPU, memory per container
  - [ ] Health checks: liveness, readiness probes
  - [ ] Scaling policies: HPA (if applicable)
- [ ] Configuration management:
  - [ ] ConfigMaps for non-secret config (URLs, feature flags)
  - [ ] Secrets for sensitive data (DB password, API tokens)
  - [ ] Environment variables injected from ConfigMaps/Secrets
- [ ] Database:
  - [ ] PostgreSQL Helm chart or custom deployment
  - [ ] Persistent volume for data
  - [ ] Backup strategy (snapshots, dumps)
  - [ ] Restore procedure documented
- [ ] Network policies (if Kubernetes):
  - [ ] Pod-to-pod communication restricted
  - [ ] Egress to external APIs (Jira/Confluence) allowed
- [ ] All manifests validated (kubectl dry-run, kubeval, etc.)

### Task 8.2: Set Up Monitoring & Alerting
**Owner:** DevOps/SRE  
**Duration:** 1.5 days  
**Depends on:** Task 6.6 (metrics)  
**Acceptance Criteria:**
- [ ] Monitoring stack deployed:
  - [ ] Prometheus scrapes metrics from backend
  - [ ] Grafana dashboards created (from local version)
  - [ ] Logs aggregated (ELK, Datadog, CloudWatch, etc.)
- [ ] Alerting configured:
  - [ ] Alert rules deployed (Prometheus AlertManager)
  - [ ] Notification channels set up (Slack, PagerDuty, email)
  - [ ] Escalation policy defined
  - [ ] Alert on-call team assigned
- [ ] Dashboards created:
  - [ ] Executive dashboard (high-level metrics)
  - [ ] Operations dashboard (system health, queue, errors)
  - [ ] Business dashboard (runs completed, success rate)
- [ ] Alert testing:
  - [ ] Trigger test alert → verify delivery to Slack/PagerDuty
  - [ ] Acknowledge alert → verify in system

### Task 8.3: Create Deployment Runbook
**Owner:** DevOps Lead  
**Duration:** 1 day  
**Depends on:** Tasks 8.1–8.2  
**Acceptance Criteria:**
- [ ] Runbook created: `infra/DEPLOYMENT.md`
  - [ ] Pre-deployment checklist:
    - [ ] All tests pass in CI
    - [ ] Code reviewed and approved
    - [ ] Database migrations reviewed
    - [ ] Feature flags configured
    - [ ] Monitoring/alerting ready
  - [ ] Deployment steps:
    - [ ] Run migrations (with rollback test)
    - [ ] Build Docker images
    - [ ] Push to registry
    - [ ] Deploy to canary environment
    - [ ] Run smoke tests
    - [ ] Gradually shift traffic (5%, 25%, 50%, 100%)
    - [ ] Monitor error rate/latency
    - [ ] Deploy to full production
  - [ ] Post-deployment:
    - [ ] Run smoke tests in production
    - [ ] Verify monitoring alerts firing correctly
    - [ ] Verify logs flowing
    - [ ] Document deployment time, any issues
  - [ ] Rollback procedure:
    - [ ] Revert database migrations (if needed)
    - [ ] Redeploy previous image
    - [ ] Verify health
    - [ ] Post-mortem on what went wrong
- [ ] Runbook tested by ops team (dry run or review)

### Task 8.4: Create Backout Procedure
**Owner:** DevOps Lead + Backend Lead  
**Duration:** 1 day  
**Depends on:** Task 8.3  
**Acceptance Criteria:**
- [ ] Backout procedure documented: `infra/BACKOUT.md`
  - [ ] When to backout (e.g., >5% error rate sustained)
  - [ ] Decision maker (on-call lead, product owner)
  - [ ] Steps:
    - [ ] Stop accepting new requests (drain connections)
    - [ ] Revert code to previous version
    - [ ] Revert database (if migrations applied)
    - [ ] Clear caches
    - [ ] Monitor for stability (30 minutes)
  - [ ] Verification:
    - [ ] Error rate drops
    - [ ] API responding normally
    - [ ] No pending runs lost (or recovered from queue)
  - [ ] Communication:
    - [ ] Notify stakeholders (user, product owner, eng)
    - [ ] Post-mortem scheduled
- [ ] Database rollback tested (in staging)
  - [ ] Run migrations → verify
  - [ ] Rollback → verify

### Task 8.5: Prepare Staging Environment
**Owner:** DevOps Lead  
**Duration:** 1.5 days  
**Depends on:** Task 8.1  
**Acceptance Criteria:**
- [ ] Staging environment deployed (prod-like infra):
  - [ ] Same Kubernetes/container setup as prod
  - [ ] Staging DNS/URL
  - [ ] Staging database (empty or with test data)
  - [ ] Staging Jira/Confluence sandbox credentials
- [ ] Staging verified:
  - [ ] All services up and healthy
  - [ ] Backend API responding
  - [ ] Frontend loads
  - [ ] Can create automation and trigger run
  - [ ] Logs flowing to monitoring stack
- [ ] Staging access:
  - [ ] Dev team can access
  - [ ] Product owner can access (for UAT)
  - [ ] Access logging enabled

### Task 8.6: Execute Canary Deployment Plan
**Owner:** DevOps Lead + On-call Lead  
**Duration:** 3–6 hours (day-of deployment)  
**Depends on:** Tasks 8.1–8.5  
**Acceptance Criteria:**
- [ ] Pre-deployment (1 hour before):
  - [ ] CI/CD pipeline green (all tests pass)
  - [ ] On-call team on standby
  - [ ] Monitoring dashboard visible
  - [ ] Slack channel open for real-time updates
  - [ ] Chat bridge between ops and dev
- [ ] Canary deployment (5% traffic, 30 minutes):
  - [ ] Deploy new image to canary pod(s)
  - [ ] Monitor: error rate, latency, queue depth
  - [ ] Target: <0.1% error increase, <50ms latency increase
  - [ ] If healthy: proceed to next stage
  - [ ] If unhealthy: roll back immediately
- [ ] Expanded deployment (25% traffic, 1 hour):
  - [ ] Deploy to more pods
  - [ ] Same monitoring
  - [ ] If healthy: proceed
- [ ] Full deployment (100% traffic, stable for 1 hour):
  - [ ] Deploy to all pods
  - [ ] Final monitoring check
  - [ ] Decommission old version
  - [ ] Document deployment time
- [ ] Post-deployment (1 hour after):
  - [ ] Run manual smoke tests
  - [ ] Verify key metrics (success rate, latency)
  - [ ] Check logs for errors
  - [ ] Customer report: all systems nominal
- [ ] On-call handoff:
  - [ ] On-call team briefed on deployment
  - [ ] Alert escalation path confirmed
  - [ ] Postmortem scheduled (if issues)

### Task 8.7: Plan Launch Communication
**Owner:** Product Owner + Marketing  
**Duration:** 0.5 days  
**Depends on:** All previous tasks  
**Acceptance Criteria:**
- [ ] Launch announcement prepared:
  - [ ] Email to users (features, how to get started)
  - [ ] Slack message to company
  - [ ] Blog post (if applicable)
  - [ ] API documentation link
- [ ] Launch date/time chosen (off-peak if possible)
- [ ] Comms reviewed and approved
- [ ] On-call team aware of launch

### Task 8.8: Execute Launch Day
**Owner:** DevOps Lead + On-call Team + Product Owner  
**Duration:** Deployment day  
**Depends on:** All Phase 8 tasks  
**Acceptance Criteria:**
- [ ] Follow deployment runbook to completion
- [ ] Canary deployment succeeds
- [ ] Full deployment succeeds
- [ ] Post-deployment checks pass
- [ ] Launch announcement sent
- [ ] Monitoring alerts working
- [ ] Initial customer reports: positive

---

## Phase 9: Post-Launch & Iteration (Weeks 16+)

### Task 9.1: Monitor Production (First 2 Weeks)
**Owner:** On-call Team + SRE  
**Duration:** Ongoing  
**Depends on:** Phase 8 complete  
**Acceptance Criteria:**
- [ ] Daily standup (first week, then daily on-call only):
  - [ ] Error rate (target: <1%)
  - [ ] API latency (p95: <200ms)
  - [ ] Queue depth (should process within minutes)
  - [ ] Worker health (processes running)
  - [ ] Database health (CPU, connections, disk space)
  - [ ] Jira/Confluence API availability
- [ ] Issues tracked:
  - [ ] Any errors logged
  - [ ] Performance spikes investigated
  - [ ] Customer reports addressed immediately
- [ ] Metrics baseline:
  - [ ] Documented in `work/PRODUCTION_METRICS_BASELINE.md`
  - [ ] Shared with team

### Task 9.2: Collect User Feedback
**Owner:** Product Owner + QA  
**Duration:** Week 1–2 post-launch  
**Acceptance Criteria:**
- [ ] User interviews (5–10 active users):
  - [ ] What's working well?
  - [ ] What's frustrating?
  - [ ] Missing features?
- [ ] In-app feedback form (if applicable):
  - [ ] Collect feedback during automation creation/run
- [ ] Support tickets reviewed:
  - [ ] Common issues
  - [ ] Roadmap feedback
- [ ] Feedback compiled in `work/USER_FEEDBACK.md`

### Task 9.3: Fix P1/P2 Issues
**Owner:** Full team  
**Duration:** Week 1–2 post-launch  
**Acceptance Criteria:**
- [ ] P1 issues (critical, affects users):
  - [ ] Reproduced and root-caused
  - [ ] Fix deployed within 24 hours
  - [ ] Verified in production
- [ ] P2 issues (high, inconvenient):
  - [ ] Scheduled for sprint
  - [ ] Fixed within 1 week
- [ ] All fixes tested before deployment
- [ ] Deployment follows standard runbook

### Task 9.4: Plan v1.1 Roadmap
**Owner:** Product Owner + Engineering Lead  
**Duration:** Week 2–3 post-launch  
**Acceptance Criteria:**
- [ ] Feedback prioritized:
  - [ ] Must-have (P0): roadmap for next 4 weeks
  - [ ] Nice-to-have (P1): roadmap for next 8 weeks
  - [ ] Future (P2): backlog
- [ ] Roadmap discussed with team:
  - [ ] Capacity planning
  - [ ] Dependencies, risks
  - [ ] Success metrics
- [ ] Roadmap documented: `specs/ROADMAP.md`
  - [ ] Features, priority, estimated effort
- [ ] Team alignment meeting held

### Task 9.5: Conduct Retrospective
**Owner:** Engineering Lead + Product Owner  
**Duration:** Week 2–3 post-launch  
**Acceptance Criteria:**
- [ ] Retrospective meeting scheduled (team + stakeholders)
- [ ] Agenda:
  - [ ] What went well?
  - [ ] What could be improved?
  - [ ] What surprised us?
  - [ ] Action items for next phase
- [ ] Notes taken: `work/RETROSPECTIVE_NOTES.md`
- [ ] Action items tracked and assigned
- [ ] Process improvements implemented (e.g., faster deployments, better monitoring)

### Task 9.6: Plan Next Phase/Release
**Owner:** Engineering Lead + Product Owner  
**Duration:** Week 3 post-launch  
**Acceptance Criteria:**
- [ ] v1.1 sprint planned:
  - [ ] User stories / features selected
  - [ ] Estimated effort
  - [ ] Timeline (e.g., 4 weeks)
  - [ ] Team assignments
- [ ] Specification updates for new features:
  - [ ] Gaps identified and closed
  - [ ] Contract changes documented
- [ ] Kickoff meeting scheduled

---

## Task Summary by Phase

| Phase | Duration | Key Deliverables | Success Criteria |
|-------|----------|------------------|------------------|
| 1 | 3 weeks | Complete spec, OpenAPI, schemas, auth, operations | Spec approved, all files valid, no TODOs |
| 2 | 2–3 weeks | Docker setup, CI/CD, DB migrations, Pact framework | `docker-compose up` works, CI green |
| 3 | 4 weeks | Backend API, auth, worker, dummy operations, audit logs | All endpoints working, >80% coverage, contracts verified |
| 4 | 4 weeks | Frontend app, pages, components, contract tests | All pages functional, Pacts published & verified |
| 5 | 3 weeks | Jira/Confluence clients, real operations, integration tests | Real operations work against sandbox, security approved |
| 6 | 3 weeks | Scheduling, webhooks, advanced filtering, observability | Performance benchmarks met, monitoring active |
| 7 | 3 weeks | Full testing, QA, security audit, UAT, documentation | All tests pass, <5 issues, UAT sign-off |
| 8 | 2 weeks | Infrastructure, deployment runbook, canary launch | Prod deployment green, <1% error rate, live |
| 9 | Ongoing | Production monitoring, feedback, v1.1 planning | Baseline metrics, roadmap defined |

---

## Critical Path & Dependencies

**Critical Path (longest dependency chain):**
1. Phase 1: Spec completion → gates everything
2. Phase 2: Infrastructure → gates backend/frontend dev
3. Phase 3: Backend API → gates frontend, integration, production
4. Phase 5: Integrations → gates advanced features, testing
5. Phase 7: Testing & QA → gates production
6. Phase 8: Deployment → launch

**Parallel Tracks:**
- Frontend (Phase 4) can start once Phase 2 spec is 50% done
- Phase 6 can start once Phase 5 begins
- Phase 7 can start once Phases 3–5 complete

---

## Task Status Tracking

Use this structure to track progress:
- Create GitHub issues for each task
- Link issues to milestones (Phase 1, Phase 2, etc.)
- Use labels: `phase-1`, `backend`, `frontend`, `qa`, `ops`, `docs`
- Assign to team members
- Track in project board (Kanban: To Do, In Progress, Done)

---

**Last Updated:** 2026-09-03  
**Next Review:** After Phase 1 complete (end of Week 3)
