from src.fetchers.orchestrator import fetch_rankings
from src.fetchers.http_client import create_session


def run_pipeline(target_week=None, backfill_weeks=None):
    session = create_session()

    rankings = fetch_rankings(
        session=session,
        target_week=target_week,
        backfill_weeks=backfill_weeks,
    )

    return rankings
