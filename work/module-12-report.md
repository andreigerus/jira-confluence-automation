# Module 12 Completion Report

## Instruction File
- Filename: instructions/convert-estimate.agent.md

`````markdown
- Use this tool when asked to convert story points into a t-shirt size estimate.
- Tool location: `./tools/convert_estimate.py`.
- Invocation: run `python tools/convert_estimate.py <points> [<points> ...]`.
  + `points` — one or more story point values (numbers), space-separated.
- Size mapping: 1 → XS, 2 → S, 3–5 → M, 8 → L, 13 → XL, 21+ → XXL.
- The script prints one line per input in the form `<points> -> <size>`.
- When presenting results to the user, state each story point value alongside its resulting t-shirt size.
- Do not guess the size mapping manually if this tool is available — invoke the script and report its output.
`````

## Script File
- Filename: tools/convert_estimate.py
- Language: Python

`````python
import argparse

SIZE_THRESHOLDS = [
    (1, "XS"),
    (2, "S"),
    (5, "M"),
    (8, "L"),
    (13, "XL"),
]
DEFAULT_SIZE = "XXL"


def story_points_to_size(points):
    for threshold, size in SIZE_THRESHOLDS:
        if points <= threshold:
            return size
    return DEFAULT_SIZE


def main():
    parser = argparse.ArgumentParser(description="Convert story points to t-shirt sizes.")
    parser.add_argument("points", type=float, nargs="+", help="One or more story point values")
    args = parser.parse_args()

    for points in args.points:
        print(f"{points} -> {story_points_to_size(points)}")


if __name__ == "__main__":
    main()
`````

## Script Execution Output
```
usage: convert_estimate.py [-h] points [points ...]

Convert story points to t-shirt sizes.

positional arguments:
  points      One or more story point values

options:
  -h, --help  show this help message and exit
```
