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
