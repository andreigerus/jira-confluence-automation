- Use this tool when asked to convert story points into a t-shirt size estimate.
- Tool location: `./tools/convert_estimate.py`.
- Invocation: run `python tools/convert_estimate.py <points> [<points> ...]`.
  + `points` — one or more story point values (numbers), space-separated.
- Size mapping: 1 → XS, 2 → S, 3–5 → M, 8 → L, 13 → XL, 21+ → XXL.
- The script prints one line per input in the form `<points> -> <size>`.
- When presenting results to the user, state each story point value alongside its resulting t-shirt size.
- Do not guess the size mapping manually if this tool is available — invoke the script and report its output.
