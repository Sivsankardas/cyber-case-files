"""
Shared freshness helpers. Every fetcher that can get a real published/added
timestamp from its source attaches it here, so every post can show the
audience exactly how old the underlying data is -- instead of implying
everything is minute-fresh just because it was *fetched* live.
"""
from datetime import datetime, timezone


def parse_iso(dt_str: str):
    """Best-effort parse of common ISO-ish timestamp formats. Returns None on failure."""
    if not dt_str:
        return None
    candidates = [dt_str, dt_str.replace("Z", "+00:00")]
    for c in candidates:
        try:
            dt = datetime.fromisoformat(c)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            continue
    return None


def age_minutes(dt: datetime) -> float:
    if dt is None:
        return float("inf")
    return (datetime.now(timezone.utc) - dt).total_seconds() / 60


def humanize_age(dt) -> str:
    """
    Turn a datetime (or None) into something like '⚡ 12 min ago',
    '🕓 6 hours ago', '📅 3 days ago', or a clear 'age unknown' note.
    """
    if dt is None:
        return "🕓 Exact detection time not provided by source"
    mins = age_minutes(dt)
    if mins == float("inf"):
        return "🕓 Exact detection time not provided by source"
    if mins < 60:
        return f"⚡ {int(mins)} min ago"
    hours = mins / 60
    if hours < 48:
        return f"🕓 {int(hours)} hr ago"
    days = hours / 24
    return f"📅 {int(days)} days ago"
