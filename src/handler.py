from src.run_pipeline import run_pipeline


def lambda_handler(event, context):
    rankings = run_pipeline(
        target_week=event.get("target_week"),
        backfill_weeks=event.get("backfill_weeks"),
    )

    return {
        "statusCode": 200,
        "body": {
            "count": len(rankings),
        },
    }
