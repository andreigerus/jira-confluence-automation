- Use this tool when asked to calculate compound interest given a principal, annual rate, compounding frequency, and time period.
- Tool location: `./tools/compound_interest.py`.
- Invocation: run `python tools/compound_interest.py <principal> <annual_rate> <compounds_per_year> <years>`.
  + `principal` — starting amount, as a plain number (e.g. `15847`).
  + `annual_rate` — annual interest rate as a decimal, not a percentage (e.g. `0.0734` for 7.34%).
  + `compounds_per_year` — number of times interest compounds per year (e.g. `12` for monthly, `4` for quarterly, `1` for annually).
  + `years` — total time period in years, as a decimal if it includes months (e.g. `8.5833` for 8 years 7 months).
- Convert years+months input to a decimal before invoking: `years + months/12`.
- The script prints two lines: `Final amount: <value>` and `Interest earned: <value>`, each rounded to 2 decimal places.
- When presenting results to the user, restate the inputs (principal, rate, compounding frequency, time period) alongside the final amount and interest earned.
- Do not recompute the math manually if this tool is available — invoke the script and report its output.
