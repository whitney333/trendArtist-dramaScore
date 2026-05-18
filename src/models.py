# src/models.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ContentRef:
    provider: str
    provider_content_id: str


@dataclass(frozen=True)
class RankingEntry:
    rank: int
    title: str
    weeks_in_top_10: int
    content_ref: Optional[ContentRef] = None
    match_status: str = "unmatched"
    linked_artist_ids: tuple[str, ...] = ()
    # global only
    hours_viewed: int = 0
    views: int = 0


@dataclass(frozen=True)
class CountryRanking:
    week: str
    country: str
    country_name: str
    category: str
    fetched_at: datetime
    source: str
    rankings: tuple[RankingEntry, ...]


@dataclass(frozen=True)
class FetchResult:
    source_used: str
    rankings: tuple[CountryRanking, ...]
    fetched_count: int
    errors: tuple[str, ...] = ()
