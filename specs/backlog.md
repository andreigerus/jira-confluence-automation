# Implementation Backlog: AI-Powered Conversational Checkout

Source spec: [project_spec.md](./project_spec.md)

**Definition of Done (Internal Beta Launch-Ready):** No blocker or critical issues open across any phase below.

**Workstream split:** Integration track (ERP + BigCommerce + Checkout API — backend/DevOps) runs in parallel with the AI track (fraud scoring + conversational/chat UX — data/ML + frontend/design). PM and QA work across both tracks.

**Task annotation legend:** each task below is tagged `[MCP]` (can be accomplished by connecting to/exposing tools via an existing MCP server, including the OpenAI Apps SDK's MCP-based tool-calling) or `[custom skill]` (requires bespoke project logic, a custom instruction/skill, or manual setup — not just tool invocation).

---

## Module 19 GitHub Coding Agent Delegation Opportunities

The following categories of tasks are ideal candidates for delegation to the GitHub coding agent in Module 19:

**Phase 1:**
- Define and document Checkout API contract (#4) - API specification & documentation

**Phase 2 & 3:**
- Implement fraud scoring service endpoint - API implementation task (Module 19 agent with MCP tools)
- Define Oracle ERP order payload schema/contract - schema specification & documentation

**Phase 4:**
- Write unit tests for Checkout API - test code generation
- Write integration tests (Checkout API ↔ BigCommerce, Checkout API ↔ Oracle ERP) - test code generation
- Write end-to-end tests - test code generation

**Phase 5 (Documentation):**
- Write Checkout API integration/API docs - documentation generation
- Write ERP payload schema/contract documentation - documentation generation
- Write on-call/incident response runbook - documentation generation
- Write customer-facing help content / FAQ - documentation generation
- Review and finalize project_spec.md - documentation review & synthesis

**Rationale:** Module 19 agent excels at code generation, test writing, API implementation, and documentation synthesis. These tasks don't require domain-specific decision-making (which remains with humans) but benefit from AI-assisted code scaffolding and documentation automation.

---

## Phase 1: Setup *(~Weeks 1–2)*

- [ ] Stand up Checkout API service skeleton (repo, CI/CD pipeline, base project structure) — `[custom skill]`
- [ ] Provision environments (dev/staging) for Checkout API — `[custom skill]`
- [ ] Set up OpenAI Apps SDK / Instant Checkout developer access and sandbox credentials — `[MCP]` (#7)
- [ ] Set up BigCommerce sandbox store + API credentials for the project — `[custom skill]` (#6)
- [ ] Set up Oracle ERP sandbox/test instance access and credentials — `[custom skill]` (#5)
- [ ] Define and document Checkout API contract (endpoints for product query, order submission, order status) — `[custom skill]` (#4)
- [ ] **Spike:** Prototype minimal OpenAI Instant Checkout flow end-to-end against sandbox data (highest-risk/least-known integration — de-risk first) — `[MCP]` (#3)
- [ ] Set up project tracking board reflecting this backlog (phases/tasks/owners) — `[custom skill]` (#2)
- [ ] Confirm team role assignments across Integration track and AI track — `[custom skill]` (#1)

## Phase 2: Core Features *(~Weeks 3–7)*

### Conversational / Chat UX (AI track)
- [ ] Implement product query handling (ChatGPT → Checkout API → BigCommerce catalog) — `[MCP]`
- [ ] Design and implement conversational product presentation (single-item selection flow) — `[MCP]`
- [ ] Implement purchase confirmation dialogue flow (intent → confirm → collect shipping/payment) — `[MCP]`
- [ ] Implement in-chat chatbot support for checkout questions (order total, shipping, payment issues) — `[MCP]`
- [ ] Implement guest checkout data collection (shipping/contact info, no login required) — `[MCP]`

### Fraud/Risk Scoring (AI track)
- [ ] Select/train initial fraud/risk scoring model — `[custom skill]`
- [ ] Define risk score thresholds and approve/decline/flag policy — `[custom skill]`
- [ ] Define manual review process for flagged transactions — `[custom skill]`
- [ ] Implement fraud scoring service endpoint callable from Checkout API — `[custom skill]`

### Checkout API & Payments (Integration track)
- [ ] Implement order submission endpoint (receives order + payment token from Instant Checkout) — `[MCP]`
- [ ] Implement payment capture via existing BigCommerce payment gateway — `[custom skill]`
- [ ] Implement approve/decline handling based on fraud score result — `[custom skill]`
- [ ] Implement order confirmation response back to ChatGPT — `[MCP]`

## Phase 3: Integration *(~Weeks 8–10)*

- [ ] Integrate Checkout API with BigCommerce product catalog (live sandbox data) — `[custom skill]`
- [ ] Integrate Checkout API with BigCommerce payment gateway (capture/settlement) — `[custom skill]`
- [ ] Define Oracle ERP order payload schema/contract — `[custom skill]`
- [ ] Implement order payload sync from Checkout API to Oracle ERP — `[custom skill]`
- [ ] Handle ERP sync failure/retry scenarios — `[custom skill]`
- [ ] Integrate fraud scoring service into the live order submission flow — `[custom skill]`
- [ ] Full end-to-end wiring: ChatGPT → Checkout API → BigCommerce → Fraud Service → ERP — `[MCP]`
- [ ] Verify PCI-DSS boundary compliance across integration points (no raw card data outside gateway/tokenization) — `[custom skill]`
- [ ] Verify GDPR/CCPA data handling for customer data collected in chat (US-only scope) — `[custom skill]`

## Phase 4: Testing *(~Weeks 10–12)*

- [ ] Write unit tests for Checkout API (order submission, payment capture, fraud decision handling) — `[custom skill]`
- [ ] Write integration tests: Checkout API ↔ BigCommerce — `[custom skill]`
- [ ] Write integration tests: Checkout API ↔ Oracle ERP — `[custom skill]`
- [ ] Write integration tests: Checkout API ↔ OpenAI Instant Checkout — `[MCP]`
- [ ] Write end-to-end tests covering full conversational purchase flow (browse → buy → confirm) — `[MCP]`
- [ ] Test fraud model accuracy and false-positive rate against test transaction sets — `[custom skill]`
- [ ] Run load/performance testing on Checkout API under expected chat traffic — `[custom skill]`
- [ ] Run security/PCI-DSS compliance testing on payment data handling — `[custom skill]`
- [ ] Fix all blocker/critical issues found during testing (required for launch-ready DoD) — `[custom skill]`

## Phase 5: Documentation *(~Week 12)*

- [ ] Write Checkout API integration/API docs (endpoints, request/response contracts) — `[custom skill]`
- [ ] Write ERP payload schema/contract documentation — `[custom skill]`
- [ ] Write on-call/incident response runbook for Checkout API and integration failures — `[custom skill]`
- [ ] Write customer-facing help content / FAQ for chat checkout experience — `[custom skill]`
- [ ] Review and finalize [project_spec.md](./project_spec.md) open questions based on decisions made during implementation — `[custom skill]`

---

## Post-MVP / Deferred (Not in this backlog)

- Multi-item cart purchases via chat
- Order status/tracking via chat
- Returns/refunds via chat
- Promo codes/discounts
- Authenticated (logged-in) chat checkout
