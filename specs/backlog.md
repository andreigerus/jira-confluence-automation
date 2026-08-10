# Implementation Backlog: AI-Powered Conversational Checkout

Source spec: [project_spec.md](./project_spec.md)

**Definition of Done (Internal Beta Launch-Ready):** No blocker or critical issues open across any phase below.

**Workstream split:** Integration track (ERP + BigCommerce + Checkout API — backend/DevOps) runs in parallel with the AI track (fraud scoring + conversational/chat UX — data/ML + frontend/design). PM and QA work across both tracks.

---

## Phase 1: Setup *(~Weeks 1–2)*

- [ ] Stand up Checkout API service skeleton (repo, CI/CD pipeline, base project structure)
- [ ] Provision environments (dev/staging) for Checkout API
- [ ] Set up OpenAI Apps SDK / Instant Checkout developer access and sandbox credentials
- [ ] Set up BigCommerce sandbox store + API credentials for the project
- [ ] Set up Oracle ERP sandbox/test instance access and credentials
- [ ] Define and document Checkout API contract (endpoints for product query, order submission, order status)
- [ ] **Spike:** Prototype minimal OpenAI Instant Checkout flow end-to-end against sandbox data (highest-risk/least-known integration — de-risk first)
- [ ] Set up project tracking board reflecting this backlog (phases/tasks/owners)
- [ ] Confirm team role assignments across Integration track and AI track

## Phase 2: Core Features *(~Weeks 3–7)*

### Conversational / Chat UX (AI track)
- [ ] Implement product query handling (ChatGPT → Checkout API → BigCommerce catalog)
- [ ] Design and implement conversational product presentation (single-item selection flow)
- [ ] Implement purchase confirmation dialogue flow (intent → confirm → collect shipping/payment)
- [ ] Implement in-chat chatbot support for checkout questions (order total, shipping, payment issues)
- [ ] Implement guest checkout data collection (shipping/contact info, no login required)

### Fraud/Risk Scoring (AI track)
- [ ] Select/train initial fraud/risk scoring model
- [ ] Define risk score thresholds and approve/decline/flag policy
- [ ] Define manual review process for flagged transactions
- [ ] Implement fraud scoring service endpoint callable from Checkout API

### Checkout API & Payments (Integration track)
- [ ] Implement order submission endpoint (receives order + payment token from Instant Checkout)
- [ ] Implement payment capture via existing BigCommerce payment gateway
- [ ] Implement approve/decline handling based on fraud score result
- [ ] Implement order confirmation response back to ChatGPT

## Phase 3: Integration *(~Weeks 8–10)*

- [ ] Integrate Checkout API with BigCommerce product catalog (live sandbox data)
- [ ] Integrate Checkout API with BigCommerce payment gateway (capture/settlement)
- [ ] Define Oracle ERP order payload schema/contract
- [ ] Implement order payload sync from Checkout API to Oracle ERP
- [ ] Handle ERP sync failure/retry scenarios
- [ ] Integrate fraud scoring service into the live order submission flow
- [ ] Full end-to-end wiring: ChatGPT → Checkout API → BigCommerce → Fraud Service → ERP
- [ ] Verify PCI-DSS boundary compliance across integration points (no raw card data outside gateway/tokenization)
- [ ] Verify GDPR/CCPA data handling for customer data collected in chat (US-only scope)

## Phase 4: Testing *(~Weeks 10–12)*

- [ ] Write unit tests for Checkout API (order submission, payment capture, fraud decision handling)
- [ ] Write integration tests: Checkout API ↔ BigCommerce
- [ ] Write integration tests: Checkout API ↔ Oracle ERP
- [ ] Write integration tests: Checkout API ↔ OpenAI Instant Checkout
- [ ] Write end-to-end tests covering full conversational purchase flow (browse → buy → confirm)
- [ ] Test fraud model accuracy and false-positive rate against test transaction sets
- [ ] Run load/performance testing on Checkout API under expected chat traffic
- [ ] Run security/PCI-DSS compliance testing on payment data handling
- [ ] Fix all blocker/critical issues found during testing (required for launch-ready DoD)

## Phase 5: Documentation *(~Week 12)*

- [ ] Write Checkout API integration/API docs (endpoints, request/response contracts)
- [ ] Write ERP payload schema/contract documentation
- [ ] Write on-call/incident response runbook for Checkout API and integration failures
- [ ] Write customer-facing help content / FAQ for chat checkout experience
- [ ] Review and finalize [project_spec.md](./project_spec.md) open questions based on decisions made during implementation

---

## Post-MVP / Deferred (Not in this backlog)

- Multi-item cart purchases via chat
- Order status/tracking via chat
- Returns/refunds via chat
- Promo codes/discounts
- Authenticated (logged-in) chat checkout
