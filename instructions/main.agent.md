# Instructions Catalog

Each entry below is an instruction file with a one-line description. Optional sub-fields after `+`:
- **Keywords** — trigger words/phrases: if user's request matches, load this instruction.
- **Target** — file glob pattern: if current file or context matches, consider this instruction relevant.
- **Exceptions** — edge cases or clarifications that don't fit in the one-liner.

---

- [`./instructions/creating-instructions.agent.md`](./creating-instructions.agent.md) — how to create, catalog, and wire up new instructions/skills for any IDE (VSCode/Copilot, Cursor, Claude Code).
  + Keywords: create instruction, create agent, instruction catalog, bootstrap instructions, main.agent.md
- [`./instructions/create-status-report.agent.md`](./create-status-report.agent.md) — generate a concise weekly status report (Markdown, bullet points, accomplishments/blockers/next week, max 20 lines).
  + Keywords: status report, weekly report, accomplishments, blockers
- [`./instructions/conduct-uat.agent.md`](./conduct-uat.agent.md) — conduct User Acceptance Testing against acceptance criteria and produce a Markdown UAT report.
  + Keywords: UAT, user acceptance testing, acceptance criteria, test case, pass fail blocked
