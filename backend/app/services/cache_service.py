"""
Thin Redis cache helpers used by service layer.

Usage:
    from app.services.cache_service import get_cached, set_cached, make_key

    key = make_key("cities", "search", query)
    cached = get_cached(key)
    if cached is not None:
        return cached
    result = expensive_db_call()
    set_cached(key, result, ttl=CITY_TTL)
    return result
"""

import json
import logging
from typing import Any

from app.config.cache import redis_client

logger = logging.getLogger(__name__)

# ── TTLs (seconds) ────────────────────────────────────────────
CITY_TTL = 3600        # 1 hour  — cities rarely change
TRANSPORT_TTL = 1800   # 30 min  — routes are stable
HOTEL_TTL = 900        # 15 min  — prices/availability more volatile


def make_key(*parts: str | int) -> str:
    """Build a namespaced cache key: 'travel:part1:part2:...'"""
    return "travel:" + ":".join(str(p) for p in parts)


def get_cached(key: str) -> Any | None:
    """Return deserialized value or None on miss / error."""
    try:
        raw = redis_client.get(key)
        if raw is None:
            return None
        return json.loads(raw)
    except Exception as exc:
        logger.warning("Cache GET error for key=%s: %s", key, exc)
        return None


def set_cached(key: str, value: Any, ttl: int) -> None:
    """Serialize and store value with TTL. Silently swallows errors."""
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception as exc:
        logger.warning("Cache SET error for key=%s: %s", key, exc)


def delete_cached(key: str) -> None:
    """Remove a key. Silently swallows errors."""
    try:
        redis_client.delete(key)
    except Exception as exc:
        logger.warning("Cache DELETE error for key=%s: %s", key, exc)
