# src/transformers/netflix_transformer.py

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.config import COUNTRY_NAME_MAPPING
from src.models import CountryRanking


def week_to_datetime(week_str: str) -> datetime:
    """
    Convert ISO week string to datetime.

    Example:
        "2024-09-01" -> datetime(2024, 9, 1)
    """
    return datetime.fromisoformat(week_str)


def transform_rankings(
    rankings: tuple[CountryRanking, ...],
) -> list[dict[str, Any]]:
    """
    Transform CountryRanking objects into MongoDB-ready documents.

    Output format:
    {
        "week": 35,
        "datetime": datetime(...),
        "country": "KR",
        "rank": "1",
        "name": "Culinary Class Wars: Season 1",
        "weeks_on_chart": "1",
        "year": 2024,
    }
    """

    documents: list[dict[str, Any]] = []

    for country_ranking in rankings:

        dt = week_to_datetime(country_ranking.week)

        iso_year, iso_week, _ = dt.isocalendar()

        country_code = COUNTRY_NAME_MAPPING.get(
            country_ranking.country,
            country_ranking.country.upper(),
        )

        for entry in country_ranking.rankings:

            documents.append(
                {
                    "week": iso_week,
                    "datetime": dt,
                    "country": country_code,
                    "rank": str(entry.rank),
                    "name": entry.title,
                    "weeks_on_chart": str(entry.weeks_in_top_10),
                    "year": iso_year,
                }
            )

    return documents