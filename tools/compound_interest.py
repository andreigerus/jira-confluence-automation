import argparse


def compound_interest(principal, annual_rate, compounds_per_year, years):
    n = compounds_per_year
    final_amount = principal * (1 + annual_rate / n) ** (n * years)
    interest_earned = final_amount - principal
    return final_amount, interest_earned


def main():
    parser = argparse.ArgumentParser(description="Calculate compound interest.")
    parser.add_argument("principal", type=float, help="Initial principal amount")
    parser.add_argument("annual_rate", type=float, help="Annual interest rate as a decimal (e.g. 0.0734 for 7.34%%)")
    parser.add_argument("compounds_per_year", type=float, help="Number of times interest compounds per year")
    parser.add_argument("years", type=float, help="Total number of years")
    args = parser.parse_args()

    final_amount, interest_earned = compound_interest(
        args.principal, args.annual_rate, args.compounds_per_year, args.years
    )

    print(f"Final amount: {final_amount:.2f}")
    print(f"Interest earned: {interest_earned:.2f}")


if __name__ == "__main__":
    main()
