# Module 17 Completion Report

## Specification Contents

# SpecKit Specification — jira-confluence-automation

> Source: SpecKit executable specification for `jira-confluence-automation`.
> Location: `spec/specification.md` (human + machine readable)

## Metadata
- name: jira-confluence-automation
- version: 0.1.0
- authors: Automation Team
- tech-stack: React 18 + Vite (frontend), Node.js + Express (backend), PostgreSQL 15 (Docker)
- last-updated: 2026-09-03

---

## Purpose
This specification is the authoritative, testable description of the system's public behavior, API contracts, data models, operational requirements, and acceptance criteria. Implementations must make tests and fixtures in `spec/` pass.

## How to use this file (brief)
- Read the API sections to implement endpoints and contract tests.
- Use the JSON schemas as authoritative request/response shapes for validation and DB schema.
- Run contract tests and acceptance test scenarios in CI; PRs that change behavior must update these specs first.

---

## Runnable artifacts in `spec/`
- `spec/openapi.yaml` — canonical OpenAPI v3 contract (generate from this doc or hand-edit)
- `spec/schemas/automation.json` — JSON Schema for automation definitions
- `spec/schemas/run_event.json` — JSON Schema for run events/logs
- `spec/samples/` — example requests and responses used by tests
- `spec/contract/` — Pact or contract test artifacts (consumer/provider)

> Note: If these files are missing, use the examples below to generate them.

---

## API: High-level summary (backend)
Base URL: `/api/v1`

Authentication: `Authorization: Bearer <token>` (JWT or API token). All endpoints require auth unless marked public.

Endpoints (required)

- `POST /api/v1/automations`
  - Summary: Create a new automation definition
  - Auth: required (write scope)
  - Request: `application/json` — body conforms to `Automation` schema
  - Responses:
    - `201` — created (body: Automation resource)
    - `400` — validation error (body: { error, details })

- `GET /api/v1/automations/{id}`
  - Summary: Retrieve automation definition
  - Responses: `200` (Automation), `404` (not found)

- `PUT /api/v1/automations/{id}`
  - Summary: Replace/update automation; clients may PATCH instead
  - Responses: `200` (updated), `400`/`404`

- `POST /api/v1/automations/{id}/run`
  - Summary: Trigger an on-demand run
  - Request: optional body with run parameters override
  - Responses: `202` (accepted — returns runId), `400`, `404`

- `GET /api/v1/runs/{runId}`
  - Summary: Get run status & logs
  - Responses: `200` — run event JSON matching `RunEvent` schema

- `GET /api/v1/health`
  - Summary: readiness & liveness
  - `200` — { status: "ok", components: {postgres: true, queue: true} }

---

## Data Models (JSON Schema excerpts)

### Automation (spec/schemas/automation.json)
- id: UUID
- name: string
- description: string
- triggers: array (cron, webhook, manual)
- steps: array of step objects (type, config)
- secrets: reference to vault keys (no raw secrets stored)

Example (short):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Automation",
  "type": "object",
  "required": ["id","name","steps"],
  "properties": {
    "id": {"type":"string","format":"uuid"},
    "name": {"type":"string"},
    "description": {"type":"string"},
    "triggers": {"type":"array","items":{"type":"object"}},
    "steps": {"type":"array","items":{"type":"object"}}
  }
}
```

### RunEvent (spec/schemas/run_event.json)
- runId, automationId, status: enum(pending,running,succeeded,failed), timestamps, logs

```json
{
  "title":"RunEvent",
  "type":"object",
  "required":["runId","automationId","status","startedAt"],
  "properties":{
    "runId":{"type":"string","format":"uuid"},
    "automationId":{"type":"string","format":"uuid"},
    "status":{"type":"string","enum":["pending","running","succeeded","failed"]},
    "startedAt":{"type":"string","format":"date-time"},
    "finishedAt":{"type":"string","format":"date-time"},
    "result":{"type":"object"}
  }
}
```

---

## Database: Core tables (Postgres 15)
Provide migrations for these tables. Sample DDL (simplified):

- `automations`:
  - `id UUID PRIMARY KEY`, `name TEXT`, `definition JSONB NOT NULL`, `created_at TIMESTAMP`, `updated_at TIMESTAMP`

- `runs`:
  - `run_id UUID PRIMARY KEY`, `automation_id UUID REFERENCES automations(id)`, `status TEXT`, `started_at TIMESTAMP`, `finished_at TIMESTAMP`, `result JSONB`

- `audit_logs`:
  - `id SERIAL PRIMARY KEY`, `actor TEXT`, `action TEXT`, `target JSONB`, `created_at TIMESTAMP`

Migrations must be created using the project's migration tool (recommend `node-pg-migrate` or `knex`) and include rollback scripts.

---

## Acceptance Criteria & Test Matrix
Each row must be implemented as an automated test in `spec/tests/`.

- Create automation: valid schema -> `POST /automations` returns 201 and persisted resource.
- Create automation: invalid schema -> 400 with error details.
- Run automation: `POST /automations/{id}/run` responds 202 and creates a `runs` record with status `pending`.
- Run lifecycle: worker picks up run -> run status transitions to `running` then `succeeded` or `failed` and logs are stored.
- Auth: requests without bearer token -> 401; token without required scope -> 403.
- Contract: frontend consumer tests assert API shapes; backend provider verifies in CI.

---

## Contract Testing
- Use Pact or equivalent for consumer-driven contracts.
- Consumers (frontend) produce Pact files in `spec/contract/consumer/`.
- Providers (backend) run Pact verification in CI against the running test server.

---

## Local Docker Development (example)
`infra/docker-compose.yml` should include:

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: jira_automation_dev
    ports:
      - 5432:5432
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgres://postgres:postgres@postgres:5432/jira_automation_dev
    ports:
      - 4000:4000

volumes:
  postgres_data:
```

Developers should copy `infra/.env.example` to `infra/.env` and never commit secrets.

---

## CI Pipeline (GitHub Actions example steps)
- Lint (frontend & backend)
- Unit tests
- Build frontend artifacts
- Start ephemeral Postgres (service container)
- Run backend migrations against ephemeral DB
- Run integration & acceptance tests (`spec/tests/`)
- Run contract provider verification (Pact)
- Publish OpenAPI checks and artifacts

PRs that change API contract must include updated `spec/openapi.yaml` and updated consumer Pacts.

---

## Security Requirements
- All stored credentials referenced by automations must be vault references; never store raw secrets in DB or repo.
- OAuth tokens and API keys stored in CI secrets and runtime vault.
- Enforce least privilege on integration tokens.

---

## Observability & Ops
- `/metrics` endpoint for Prometheus
- Structured logs (JSON) with `runId` and `correlationId`
- Health & readiness endpoints
- Alerts for worker backlog and high failure rate

---

## Migration & Backout Strategy
- For breaking schema changes: create a migration and a rollback. Run migration in canary environment before prod.
- Provide backout steps in `infra/ops.md` including restoring DB snapshot and redeploy old image.

---

## Release Notes & Versioning
- API follows semantic versioning; breaking changes require major version bump and migration notes.
- Keep a changelog at `spec/CHANGELOG.md`.

---

## Example: Minimal OpenAPI fragment (to be expanded into `spec/openapi.yaml`)

```yaml
openapi: 3.0.3
info:
  title: jira-confluence-automation API
  version: 0.1.0
paths:
  /api/v1/automations:
    post:
      summary: Create automation
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Automation'
      responses:
        '201':
          description: Created
components:
  schemas:
    Automation:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        steps:
          type: array

```

---

## Governance & Change Process
- Update `spec/` first for behavior changes. Tests and OpenAPI must be updated with the spec changes.
- Code reviews must validate spec changes and ensure contract test updates accompany them.

---

## Next actions (developer-friendly)
- Add `spec/openapi.yaml` from the OpenAPI fragment and expand endpoints.
- Create JSON Schema files under `spec/schemas/` and place example samples in `spec/samples/`.
- Add contract tests: frontend produces Pacts; backend adds verification job in CI.

---

## Appendices
- Glossary, sample payloads, and detailed DB migration examples should live in `spec/appendix/`.

---

Last updated: 2026-09-03

---

## Commit History

```
24ab0d0 (HEAD -> master, origin/master) Implement Phase 1 specification foundati
on (Tasks 1.1-1.4)
723ec11 spec: add SpecKit constitution and specification
6bd666c Merge branch 'master' of https://github.com/andreigerus/jira-confluence-
automation
2f4edb5 Add Module 16 report
9b46305 Fix: restore task.md with proper content
05d399b commit task.md
def3f3f Merge branch 'master' of https://github.com/andreigerus/jira-confluence-
automation
e1b7e80 Add Module 15 completion report - Bulk File Processing
80ae77a Add validate-instructions to main instruction catalog
7304e4a Add individual transaction file validator and comprehensive validation i
nstructions
d2ec606 Add batch processing strategy annotations to backlog tasks
c726656 Add validation-rules.md with credit card, expiration, and special charac
ter checks
ace4fff Add Module 14 completion report - MCP GitHub integration
dcea960 Add Module 19 GitHub coding agent delegation opportunities to backlog
8788d55 Update backlog with GitHub issue numbers for Phase 1 tasks
feffa16 Add MCP echo-windows server with echo and get_time tools
524b7cd Add compound interest and estimate conversion tools with instructions; m
odule reports
b864285 Add module 03 completion report
a2d4c83 Initial commit
a725181 Add language selection and numerology prediction
```

## Commit Count

```
20
```

## Project Files

```
.github/copilot-instructions.md
.github/prompts/to-calculate-compound-interest.prompt.md
.github/prompts/to-conduct-uat.prompt.md
.github/prompts/to-convert-estimate.prompt.md
.github/prompts/to-create-status-report.prompt.md
.gitignore
.vscode/mcp.json
.vscode/settings.json
README.md
TODO.md
calculator/.gitignore
calculator/README.md
calculator/calculator.py
calculator/index.html
calculator/main.py
calculator/script.js
calculator/style.css
index.html
instructions/calculate-compound-interest.agent.md
instructions/conduct-uat.agent.md
instructions/convert-estimate.agent.md
instructions/create-status-report.agent.md
instructions/creating-instructions.agent.md
instructions/main.agent.md
instructions/validate-instructions.agent.md
reports/example.md
reports/instructions.md
reports/template.md
script.js
spec/analyze.md
spec/checklist.md
spec/clarify.md
spec/constitution.md
spec/openapi.yaml
spec/plan.md
spec/samples/automation-cron.json
spec/samples/automation-webhook.json
spec/samples/step-confluence-create-page.json
spec/samples/step-jira-create-issue.json
spec/samples/trigger-cron.json
spec/samples/trigger-manual.json
spec/samples/trigger-webhook.json
spec/schemas/automation.json
spec/schemas/step.json
spec/schemas/triggers.json
spec/specification.md
spec/tasks.md
specs/backlog.md
specs/project_spec.md
styles.css
tools/compound_interest.py
tools/convert_estimate.py
tools/mcp-calculate.ps1
tools/mcp-echo.ps1
tools/validate-transaction-file.py
work/module-03-report.md
work/module-08-report.md
work/module-09-report.md
work/module-10-report.md
work/module-12-report.md
work/module-13-report.md
work/module-14-report.md
work/module-15-report.md
work/module-16-report.md
work/task.md
work/test-transactions-invalid.json
work/test-transactions-valid.json
work/validation-rules.md
```
