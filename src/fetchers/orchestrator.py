"""Fetcher orchestrator: TSV primary, HTML fallback.

This module implements the resilience strategy for data collection.
Rather than depending on a single source that could break (as the
original run.py did with HTML scraping), we use a fallback chain:

    1. Try the TSV export (fast, structured, stable)
    2. If that fails, fall back to HTML scraping (slower, fragile)
    3. If both fail, return an empty result with error details

The orchestrator never raises exceptions - it always returns a
ScrapeResult, even on total failure. Errors are collected in the
result's errors tuple for the handler to log and store.
"""

# src/fetchers/orchestrator.py

from src.fetchers.tsv_fetcher import (
    fetch_latest_week,
    fetch_specific_week,
    fetch_recent_weeks,
)


def fetch_rankings(session, target_week=None, backfill_weeks=None):
    if target_week:
        return fetch_specific_week(session, target_week)

    if backfill_weeks:
        return fetch_recent_weeks(session, backfill_weeks)

    return fetch_latest_week(session)
