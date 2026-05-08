# src/config.py

from dataclasses import dataclass
from typing import Final
import os


NETFLIX_TSV_URL: Final[str] = (
    "https://www.netflix.com/tudum/top10/data/all-weeks-countries.tsv"
)

REQUEST_TIMEOUT: Final[int] = 30

HTML_REQUEST_DELAY_SECONDS: Final[float] = 1.5

TRACKED_COUNTRIES: Final[tuple[str, ...]] = (
    "south-korea",
    "hong-kong",
    "taiwan",
    "japan",
    "thailand",
    "vietnam",
    "philippines",
    "indonesia",
    "united-states",
    "canada",
    "brazil",
    "mexico",
    "united-kingdom",
    "germany",
    "france",
    "spain",
    "italy",
    "australia",
)


CATEGORY_MAPPING: Final[dict[str, str]] = {
    "Films": "films",
    "TV": "tv",
}


COUNTRY_NAME_MAPPING: Final[dict[str, str]] = {
    "South Korea": "south-korea",
    "Hong Kong": "hong-kong",
    "Taiwan": "taiwan",
    "Japan": "japan",
    "Thailand": "thailand",
    "Vietnam": "vietnam",
    "Philippines": "philippines",
    "Indonesia": "indonesia",
    "United States": "united-states",
    "Canada": "canada",
    "Brazil": "brazil",
    "Mexico": "mexico",
    "United Kingdom": "united-kingdom",
    "Germany": "germany",
    "France": "france",
    "Spain": "spain",
    "Italy": "italy",
    "Australia": "australia",
}


USER_AGENT: Final[str] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/147.0.0.0 Safari/537.36"
)


@dataclass(frozen=True)
class NetflixConfig:
    netflix_tsv_url: str = NETFLIX_TSV_URL
    request_timeout: int = REQUEST_TIMEOUT
    html_request_delay_seconds: float = HTML_REQUEST_DELAY_SECONDS


def load_config() -> NetflixConfig:
    return NetflixConfig(
        netflix_tsv_url=os.getenv(
            "NETFLIX_TSV_URL",
            NETFLIX_TSV_URL,
        ),
        request_timeout=int(
            os.getenv(
                "REQUEST_TIMEOUT",
                REQUEST_TIMEOUT,
            )
        ),
        html_request_delay_seconds=float(
            os.getenv(
                "HTML_REQUEST_DELAY_SECONDS",
                HTML_REQUEST_DELAY_SECONDS,
            )
        ),
    )
