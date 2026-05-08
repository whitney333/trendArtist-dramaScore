"""Primary data source: Netflix's public TSV export.

Netflix publishes a tab-separated file containing weekly Top 10 rankings
for every country they track (~94 countries, 240+ weeks of history).
This is far more stable than HTML scraping because:

1. It's a structured data export, not a rendered web page
2. No CSS class names or DOM structure to break on redesign
3. Contains all countries and weeks in a single ~28MB download
4. Updated weekly by Netflix alongside their website

The TSV columns are:
    country_name, country_iso2, week, category, weekly_rank,
    show_title, season_title, cumulative_weeks_in_top_10

We filter this down to only the 18 TRACKED_COUNTRIES defined in config,
and only the latest week (unless a specific week is requested).
"""

import csv
import logging
from collections import defaultdict
from io import StringIO
from datetime import datetime, UTC
import requests

from src.config import TRACKED_COUNTRIES
from src.models import CountryRanking, RankingEntry

logger = logging.getLogger(__name__)

TSV_URL = "https://www.netflix.com/tudum/top10/data/all-weeks-countries.tsv"

CATEGORY_MAP = {
    "Films": "films",
    "TV": "tv",
}


def _parse_int(value: str) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def _country_slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def fetch_tsv(session: requests.Session) -> str:
    resp = session.get(TSV_URL, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_tsv(tsv_text: str, target_week=None, include_all_weeks=False):
    reader = csv.DictReader(StringIO(tsv_text), delimiter="\t")

    grouped = defaultdict(list)
    latest_week = ""

    tracked = set(_country_slug(c) for c in TRACKED_COUNTRIES)

    for row in reader:
        week = row["week"]
        raw_country_name = row["country_name"]
        country = _country_slug(raw_country_name)

        if week > latest_week:
            latest_week = week

        if target_week and week != target_week:
            continue

        if country not in tracked:
            continue

        key = (week, country, row["category"])
        grouped[key].append(row)

    if target_week is None and not include_all_weeks:
        grouped = {
            k: v for k, v in grouped.items()
            if k[0] == latest_week
        }

    results = []

    for (week, country, category), rows in grouped.items():

        entries = tuple(
            RankingEntry(
                rank=_parse_int(r["weekly_rank"]),
                title=r["show_title"],
                weeks_in_top_10=_parse_int(r["cumulative_weeks_in_top_10"]),
            )
            for r in sorted(rows, key=lambda x: _parse_int(x["weekly_rank"]))
        )

        results.append(
            CountryRanking(
                week=week,
                country=_country_slug(country),
                country_name=country,
                category=CATEGORY_MAP.get(category, category.lower()),
                source="tsv",
                fetched_at=datetime.now(UTC),
                rankings=entries,
            )
        )

    return tuple(results)


def fetch_latest_week(session):
    return parse_tsv(fetch_tsv(session))


def fetch_specific_week(session, week: str):
    return parse_tsv(fetch_tsv(session), target_week=week)


def fetch_recent_weeks(session, weeks: int):
    all_data = parse_tsv(fetch_tsv(session), include_all_weeks=True)

    weeks_sorted = sorted({x.week for x in all_data}, reverse=True)
    selected = set(weeks_sorted[:weeks])

    return tuple(x for x in all_data if x.week in selected)