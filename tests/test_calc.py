from datetime import date, datetime, timedelta

import pytest

from cyl.calc import (
    DateDiff,
    RemainingTime,
    date_difference,
    lifetime_progress,
    remaining_time,
    target_date,
    today_progress,
    week_progress,
)


class TestDateDifference:
    def test_normal(self):
        assert date_difference(date(1990, 1, 1), date(2020, 6, 15)) == DateDiff(30, 5, 14)

    def test_same_date(self):
        assert date_difference(date(2020, 3, 15), date(2020, 3, 15)) == DateDiff(0, 0, 0)

    def test_one_day(self):
        assert date_difference(date(2020, 1, 1), date(2020, 1, 2)) == DateDiff(0, 0, 1)

    def test_one_year(self):
        assert date_difference(date(2020, 1, 1), date(2021, 1, 1)) == DateDiff(1, 0, 0)

    def test_month_end_jan31_to_mar1(self):
        # Jan 31 → Mar 1: raw days=-30, end month (Mar)=31 days → days=1, months=1
        assert date_difference(date(2020, 1, 31), date(2020, 3, 1)) == DateDiff(0, 1, 1)

    def test_month_boundary_feb_to_mar(self):
        # Jan 31 → Feb 29 (leap): raw days=29-31=-2, end month (Feb 2020)=29 → days=27, months=0
        assert date_difference(date(2020, 1, 31), date(2020, 2, 29)) == DateDiff(0, 0, 27)

    def test_leap_year_feb29_to_next_feb28(self):
        # Feb 29, 2020 → Feb 28, 2021: raw years=1, months=0, days=-1
        # end month Feb 2021 = 28 days → days=27, months=-1 → years=0, months=11
        assert date_difference(date(2020, 2, 29), date(2021, 2, 28)) == DateDiff(0, 11, 27)

    def test_year_end_crossing(self):
        # Dec 31, 2019 → Jan 1, 2020: raw years=1, months=-11, days=-30
        # end month Jan=31 → days=1, months=-12 → years=0, months=0
        assert date_difference(date(2019, 12, 31), date(2020, 1, 1)) == DateDiff(0, 0, 1)


class TestTargetDate:
    def test_normal(self):
        assert target_date(date(1990, 5, 19), 90) == date(2080, 5, 19)

    def test_leap_birthday_non_leap_target(self):
        # Feb 29 in non-leap year → Feb 28
        td = target_date(date(1960, 2, 29), 90)
        assert td == date(2050, 2, 28)

    def test_leap_birthday_leap_target(self):
        td = target_date(date(1960, 2, 29), 64)
        assert td == date(2024, 2, 29)


class TestRemainingTime:
    def test_exact_target_day(self):
        # Exactly at target date midnight → all zeros
        now = datetime(2080, 5, 19, 0, 0, 0)
        rt = remaining_time(date(1990, 5, 19), 90, now)
        assert rt == RemainingTime(0, 0, 0, 0, 0, 0, 0, 0)

    def test_round_years(self):
        now = datetime(2020, 1, 1, 0, 0, 0)
        rt = remaining_time(date(1990, 1, 1), 90, now)
        assert rt.years == 60
        assert rt.months == 0
        assert rt.days == 0
        assert rt.hours == 0
        assert rt.minutes == 0
        assert rt.seconds == 0

    def test_hms_within_last_day(self):
        # now = 2019-12-31 12:30:45, target = 2020-01-01 00:00:00
        # total_secs = 86400 - (12*3600 + 30*60 + 45) = 41355
        now = datetime(2019, 12, 31, 12, 30, 45)
        rt = remaining_time(date(1990, 1, 1), 30, now)
        assert rt.years == 0
        assert rt.months == 0
        assert rt.days == 1
        assert rt.hours == 11
        assert rt.minutes == 29
        assert rt.seconds == 15

    def test_leap_birthday_does_not_crash(self):
        now = datetime(2020, 3, 1, 0, 0, 0)
        rt = remaining_time(date(1960, 2, 29), 90, now)
        assert rt.years >= 0

    def test_total_months(self):
        now = datetime(2020, 1, 1, 0, 0, 0)
        rt = remaining_time(date(1990, 1, 1), 90, now)
        assert rt.total_months == 60 * 12

    def test_total_days(self):
        now = datetime(2020, 1, 1, 0, 0, 0)
        rt = remaining_time(date(1990, 1, 1), 90, now)
        assert rt.total_days == (date(2080, 1, 1) - date(2020, 1, 1)).days

    def test_total_days_last_day(self):
        # now = 2019-12-31, target = 2020-01-01 → 1 day remaining
        now = datetime(2019, 12, 31, 12, 30, 45)
        rt = remaining_time(date(1990, 1, 1), 30, now)
        assert rt.total_days == 1


class TestTodayProgress:
    def test_midnight(self):
        assert today_progress(datetime(2024, 1, 1, 0, 0, 0)) == pytest.approx(0.0)

    def test_noon(self):
        assert today_progress(datetime(2024, 1, 1, 12, 0, 0)) == pytest.approx(0.5)

    def test_end_of_day(self):
        now = datetime(2024, 1, 1, 23, 59, 59)
        assert today_progress(now) == pytest.approx((23 * 3600 + 59 * 60 + 59) / 86400)


class TestWeekProgress:
    def test_monday_midnight(self):
        # 2024-01-01 is a Monday
        assert week_progress(datetime(2024, 1, 1, 0, 0, 0)) == pytest.approx(0.0)

    def test_thursday_noon(self):
        # Thursday = weekday 3; elapsed = 3*86400 + 12*3600 = 302400
        now = datetime(2024, 1, 4, 12, 0, 0)
        assert week_progress(now) == pytest.approx(302400 / (7 * 86400))

    def test_sunday_end(self):
        now = datetime(2024, 1, 7, 23, 59, 59)
        assert week_progress(now) == pytest.approx(
            (6 * 86400 + 23 * 3600 + 59 * 60 + 59) / (7 * 86400)
        )


class TestLifetimeProgress:
    def test_at_birthday(self):
        assert lifetime_progress(date(1990, 1, 1), 90, date(1990, 1, 1)) == pytest.approx(0.0)

    def test_at_target(self):
        assert lifetime_progress(date(1990, 1, 1), 90, date(2080, 1, 1)) == pytest.approx(1.0)

    def test_halfway(self):
        birthday = date(1990, 1, 1)
        td = target_date(birthday, 90)
        total_days = (td - birthday).days
        halfway = birthday + timedelta(days=total_days // 2)
        assert lifetime_progress(birthday, 90, halfway) == pytest.approx(0.5, abs=1e-4)

    def test_clamps_below_zero(self):
        assert lifetime_progress(date(1990, 1, 1), 90, date(1989, 12, 31)) == pytest.approx(0.0)

    def test_clamps_above_one(self):
        assert lifetime_progress(date(1990, 1, 1), 90, date(2081, 1, 1)) == pytest.approx(1.0)
