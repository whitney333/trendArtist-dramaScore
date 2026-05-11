from __future__ import annotations
import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME", "netflix_charts")

MONGODB_URI = (
    f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}"
)

_client: MongoClient | None = None

def get_database():
    """
    Return MongoDB database singleton.
    """

    global _client

    if _client is None:
        _client = MongoClient(MONGODB_URI)

    return _client[os.getenv("DB_NAME")]
