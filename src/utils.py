import json
import os
from datetime import datetime, timezone


CACHE_FILE = "cache/posted.json"


def load_posted():
    """
    Load previously notified offer IDs.
    """

    if not os.path.exists(CACHE_FILE):
        return []

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_posted(posted):
    """
    Save notified offer IDs.
    """

    os.makedirs("cache", exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(posted, f, indent=4)


def discord_timestamp(iso_date):
    """
    Convert ISO date to Discord timestamp.

    Example:
    <t:1786208400:F>
    """

    if not iso_date:
        return "Unknown"

    try:
        dt = datetime.fromisoformat(
            iso_date.replace("Z", "+00:00")
        ).astimezone(timezone.utc)

        return f"<t:{int(dt.timestamp())}:F>"

    except Exception:
        return iso_date


def format_price(price):
    """
    Convert Epic integer price to readable format.

    Example:
    1999 -> $19.99
    """

    if price is None:
        return "Unknown"

    return f"${price / 100:.2f}"


def get_best_image(images):
    """
    Pick the nicest image from Epic's keyImages.
    """

    if not images:
        return None

    preferred = [
        "DieselStoreFrontWide",
        "OfferImageWide",
        "Thumbnail",
        "DieselGameBox"
    ]

    for image_type in preferred:
        for image in images:
            if image.get("type") == image_type:
                return image.get("url")

    return images[0].get("url")


def is_raw_slug(slug):
    """
    Detect Epic's internal hash IDs.
    """

    if not slug:
        return False

    return (
        len(slug) >= 20
        and all(c in "0123456789abcdef" for c in slug.lower())
    )


def get_store_url(game):
    """
    Build the Epic Games Store URL.
    """

    mappings = game.get("offerMappings") or []

    for mapping in mappings:
        if mapping.get("pageType") == "productHome":
            return (
                "https://store.epicgames.com/en-US/p/"
                + mapping["pageSlug"]
            )

    slug = game.get("urlSlug")

    if slug and not is_raw_slug(slug):
        return f"https://store.epicgames.com/en-US/p/{slug}"

    slug = game.get("productSlug")

    if slug and not is_raw_slug(slug):
        return f"https://store.epicgames.com/en-US/p/{slug}"

    return "https://store.epicgames.com/en-US/free-games"
