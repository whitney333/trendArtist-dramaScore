from typing import Any
from pymongo import UpdateOne
from src.storage.mongo import get_database


COLLECTION_NAME = "netflix_charts"


def save_rankings(
    documents: list[dict[str, Any]],
) -> None:
    """
    Save ranking documents into netflix_charts collection.
    Uses bulk upsert to avoid duplicates.
    """

    if not documents:
        return

    db = get_database()

    collection = db[COLLECTION_NAME]

    operations = []

    for doc in documents:

        operations.append(
            UpdateOne(
                {
                    "year": doc["year"],
                    "week": doc["week"],
                    "country": doc["country"],
                    "rank": doc["rank"],
                },
                {"$set": doc},
                upsert=True,
            )
        )

    result = collection.bulk_write(
        operations,
        ordered=False,
    )

    print(
        f"Saved rankings | "
        f"upserted={result.upserted_count} "
        f"modified={result.modified_count}"
    )