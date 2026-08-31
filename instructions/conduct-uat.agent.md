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
