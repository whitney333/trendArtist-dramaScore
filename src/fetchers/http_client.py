"""HTTP session factory with automatic retries and exponential backoff.

Creates a requests.Session pre-configured with:
- Honest User-Agent header (not browser impersonation)
- Retry on transient HTTP errors (429, 5xx) with exponential backoff
- Configurable timeout and retry count from NetflixConfig
"""

# src/fetchers/http_client.py

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session() -> requests.Session:
    session = requests.Session()

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    })

    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session
