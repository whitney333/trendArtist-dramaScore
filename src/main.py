import argparse
from src.run_pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--week", type=str)
    parser.add_argument("--backfill", type=int)

    args = parser.parse_args()

    rankings = run_pipeline(
        target_week=args.week,
        backfill_weeks=args.backfill,
    )

    print(f"Fetched {len(rankings)} records")

    for r in rankings[:2]:
        print(r)


if __name__ == "__main__":
    main()
