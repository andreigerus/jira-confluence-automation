# SpecKit Constitution — jira-confluence-automation

## Overview
This SpecKit constitution captures the authoritative specification for the `jira-confluence-automation` project. The spec is the source of truth for behavior, interfaces, contracts, deployment, and acceptance criteria. It is written for automation engineers, backend/frontend developers, QA, and operations.

## Purpose
- Define executable, testable expectations for features and integrations with Jira and Confluence.
- Make contracts explicit to reduce integration friction across teams.
- Provide a governable change process for evolving automation behavior.

## Scope
- Frontend: React 18 + Vite SPA providing UI to configure, preview, and run automations.
- Backend: Node.js (LTS) + Express providing REST API and background workers to execute automations.
- Data: PostgreSQL 15 running in Docker for persistence of configurations, audit logs, and scheduling state.
- Integrations: Jira Cloud/Server and Confluence REST APIs; OAuth or API token based authentication.
- CI/CD, tests, monitoring and infra as code for local developer reproducibility.

## Stakeholders
- Product owner / Automation SME
- Backend engineers (Node/Express)
- Frontend engineers (React/Vite)
- QA / SRE / DevOps
- Integrations consumers (teams using the automation)

## Principles
- Specs first: update specs before implementation. Executable specs gate pull requests.
- Contract-driven integration: produce API contracts (OpenAPI) and consumer-driven contract tests (Pact or similar).
- Small, reversible changes: migrations, feature flags, and backward compatibility policies.
- Observability and auditability: every automation run must be auditable.
- Security by design: credentials never stored in repo, secrets via environment / vault.

## Tech Stack
- Frontend: React 18, Vite, TypeScript (recommended)
- Backend: Node.js (LTS), Express, TypeScript optional
- Database: PostgreSQL 15 (Docker container)
- Container runtime: Docker / Docker Compose for local dev
- Testing: Jest / Vitest, Supertest for HTTP tests, Pact for contract tests
- CI: GitHub Actions (or equivalent) to run specs and contract tests

## Repository layout (recommended)
- `frontend/` — React + Vite app
- `backend/` — Express app, API, workers, migrations
- `spec/` — SpecKit files, contract definitions, example requests/responses
- `infra/` — docker-compose.yml, local env, deployment manifests
- `scripts/` — helper scripts (seed, migrate, run-contract-tests)

## Services & Contracts (high level)
- Service: `backend` (Express)
  - Base path: `/api/v1`
  - Authentication: `Authorization: Bearer <token>` (JWT or API token)
  - Required endpoints (examples):
    - `POST /api/v1/automations` — create automation (body: spec)
    - `GET /api/v1/automations/:id` — get automation
    - `POST /api/v1/automations/:id/run` — trigger run
    - `GET /api/v1/runs/:id` — fetch run status and logs
    - `GET /api/v1/health` — health check
- Contracts: publish OpenAPI v3 file at `/spec/openapi.yaml` and generate server/client stubs.

## Data Contracts
- Store automation definitions as JSON schema; include examples in `spec/samples/`.
- Record run events with schema: `{ runId, automationId, status, startedAt, finishedAt, result }`.
- Define DB migrations and a policy: all schema changes require a migration script + rollback plan.

## Acceptance Criteria (executable)
- Each public API endpoint must have acceptance tests (integration) demonstrating expected inputs/outputs.
- Contract tests: consumer tests for the frontend + provider verification in backend CI.
- Security tests: ensure endpoints requiring auth reject unauthorized requests.
- Database integration: migration applied and validated in CI using a disposable Postgres (Docker).

## Local Development & Docker
- Provide `infra/docker-compose.yml` with services: `postgres:15`, `backend`, `frontend` (optional)
- Local env variables loaded from `.env.local` (do NOT commit). Example keys documented in `infra/.env.example`.

## CI/CD Gates
- PR checks must include:
  - Linting for frontend and backend
  - Unit tests and integration tests
  - Contract tests (Pact verify provider)
  - OpenAPI validation that spec file is syntactically valid
  - DB migrations sanity check

## Versioning & Compatibility
- API follows semantic versioning for breaking changes: bump major and accompany with migration notes.
- Maintain a compatibility policy: keep last 2 major API versions supported or provide migration tooling.

## Security & Secrets
- Do not store secrets in repo; use GitHub Secrets / Vault for CI and runtime.
- Use short‑lived tokens for integrations when possible; rotate regularly.
- Audit logs for sensitive operations and access control with RBAC.

## Observability & SLOs
- Emit structured logs (JSON) with correlation IDs for runs.
- Expose Prometheus metrics endpoint `/metrics` and basic request tracing.
- Define SLOs for background run completion and API error rate.

## Change Process (governance)
- Update spec: create or modify files in `spec/` and include example requests/responses.
- Contract-first change: update OpenAPI + consumer tests before implementation wherever feasible.
- Review: maintainers review and merge; CI must pass contract verification.
- Migration: include migration + rollback in `backend/migrations` for schema changes.

## Testing Strategy
- Unit tests for logic, integration tests for DB + API, end‑to‑end tests for key flows.
- Consumer-driven contract tests between `frontend` and `backend`.
- Smoke tests on every deploy (run a sample automation against a sandbox Jira/Confluence instance).

## Rollout & Backout
- Feature flags for new automations; blue/green or canary deployments recommended for backend.
- Backout procedure documented in `infra/ops.md` including database rollback steps.

## Glossary
- Automation: declarative definition representing a sequence of operations executed against Jira/Confluence.
- Run: an execution instance of an automation.
- Spec: executable specification (OpenAPI, JSON schema, contract tests) serving as source of truth.

---

Last updated: 2026-09-03
