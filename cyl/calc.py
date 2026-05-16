import calendar
from datetime import date, datetime
from typing import NamedTuple


class DateDiff(NamedTuple):
    years: int
    months: int
    days: int


class RemainingTime(NamedTuple):
    years: int
    months: int
    days: int
    hours: int
    minutes: int
    seconds: int
    total_months: int
    total_days: int


def date_difference(start: date, end: date) -> DateDiff:
    """Compute calendar difference between two dates as (years, months, days)."""
    years = end.year - start.year
    months = end.month - start.month
    days = end.day - start.day

    if days < 0:
        months -= 1
        _, days_in_end_month = calendar.monthrange(end.year, end.month)
        days += days_in_end_month

    if months < 0:
        years -= 1
        months += 12

    return DateDiff(years, months, days)


def target_date(birthday: date, target_age: int) -> date:
    """Return the date when the person reaches target_age."""
    try:
        return date(birthday.year + target_age, birthday.month, birthday.day)
    except ValueError:
        # Feb 29 birthday in a non-leap target year → use Feb 28
        return date(birthday.year + target_age, birthday.month, 28)


def remaining_time(birthday: date, target_age: int, now: datetime | None = None) -> RemainingTime:
    """Return all remaining-time components from now until birthday + target_age."""
    if now is None:
        now = datetime.now()

    td = target_date(birthday, target_age)
    target_dt = datetime(td.year, td.month, td.day)

    total_secs = int((target_dt - now).total_seconds())

    hours = (total_secs % 86400) // 3600
    minutes = (total_secs % 3600) // 60
    seconds = total_secs % 60

    diff = date_difference(now.date(), td)
    total_months = diff.years * 12 + diff.months
    total_days = max(0, (td - now.date()).days)

    return RemainingTime(diff.years, diff.months, diff.days, hours, minutes, seconds, total_months, total_days)


def weeks_elapsed(birthday: date, today: date | None = None) -> int:
    """Return how many weeks have elapsed since birthday (for life-grid use)."""
    if today is None:
        today = date.today()
    return max(0, (today - birthday).days // 7)


def today_progress(now: datetime | None = None) -> float:
    """Fraction of today elapsed: 0.0 at midnight, approaches 1.0 at end of day."""
    if now is None:
        now = datetime.now()
    return (now.hour * 3600 + now.minute * 60 + now.second) / 86400


def week_progress(now: datetime | None = None) -> float:
    """Fraction of Mon-Sun week elapsed: 0.0 at Monday 00:00."""
    if now is None:
        now = datetime.now()
    elapsed = now.weekday() * 86400 + now.hour * 3600 + now.minute * 60 + now.second
    return elapsed / (7 * 86400)


def lifetime_progress(birthday: date, target_age: int, today: date | None = None) -> float:
    """Fraction of life elapsed from birthday to target_date, clamped to [0, 1]."""
    if today is None:
        today = date.today()
    td = target_date(birthday, target_age)
    total_days = (td - birthday).days
    if total_days <= 0:
        return 1.0
    return max(0.0, min(1.0, (today - birthday).days / total_days))
