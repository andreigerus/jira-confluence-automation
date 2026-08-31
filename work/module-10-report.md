# Module 10 Completion Report

## Instruction Files
```
conduct-uat.agent.md
create-status-report.agent.md
creating-instructions.agent.md
main.agent.md
```

## main.agent.md Contents

`````markdown
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
`````

## Sample Instruction
- File: conduct-uat.agent.md
- Contents:

`````markdown
- Input: user provides a feature/user story with acceptance criteria (Given/When/Then or plain bullet list) and, optionally, a target environment/build to test against.
- If acceptance criteria are missing or ambiguous, ask the user to clarify before proceeding — do not assume undocumented behavior.
- Processing:
  + Map each acceptance criterion to one test case.
  + For each test case, execute/verify the described action against actual system behavior (UI, API response, output, etc.).
  + Record the actual result observed vs. the expected result stated in the criterion.
  + Mark each test case as Pass, Fail, or Blocked (environment/dependency issue prevented testing).
  + Note reproduction steps for any Fail or Blocked case.
- Output: a Markdown UAT report containing:
  + Feature/story name and reporting date.
  + A table with columns: Test Case, Expected Result, Actual Result, Status (Pass/Fail/Blocked), Notes.
  + A summary line with pass/fail/blocked counts.
- Constraints:
  + Only test against documented acceptance criteria — do not invent new criteria.
  + Do not mark a case Pass without an observed actual result.
  + Keep notes factual and concise — no fluff or subjective language.
  + Flag ambiguous criteria explicitly instead of guessing intent.
`````
