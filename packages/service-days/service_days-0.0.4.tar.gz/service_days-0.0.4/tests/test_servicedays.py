from typing import T, List
from unittest import TestCase

from hamcrest.core.description import Description

from service_days.servicedays import service_day_add, Day, map_schedule_txt_to_day_list, days_in_range, day_count_in_range

from datetime import date

from hamcrest import *

from hamcrest.core.base_matcher import BaseMatcher


class DateInSchedule(BaseMatcher):
    def __init__(self, schedule: List[Day] = None):
        self.schedule = schedule

    def describe_to(self, description: Description) -> None:
        pass

    def _matches(self, item: date) -> bool:
        t_day = Day(item.weekday())
        return t_day in self.schedule


class Test(TestCase):

    def test_service_day_add_simple_add_to_default_week(self):
        # Default Schedule (Mon-Fri)
        # Monday -> Tuesday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, 1), equal_to(date(2023, 3, 7)))

        # Tuesday -> Wednesday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, 1), equal_to(date(2023, 3, 8)))

        # Wednesday -> Thursday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, 1), equal_to(date(2023, 3, 9)))

        # Thursday -> Friday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, 1), equal_to(date(2023, 3, 10)))

        # Friday -> Monday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, 1), equal_to(date(2023, 3, 13)))

        # Saturday -> Monday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, 1), equal_to(date(2023, 3, 13)))

        # Sunday -> Monday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, 1), equal_to(date(2023, 3, 13)))

        # --- ADD 2 ---
        # Default Schedule (Mon-Fri)
        add_days = 2
        # Monday -> Wednesday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 8)))

        # Tuesday -> Thursday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 9)))

        # Wednesday -> Friday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 10)))

        # Thursday -> Monday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 13)))

        # Friday -> Tuesday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 14)))

        # Saturday -> Tu
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 14)))

        # Sunday -> Tuesday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 14)))

        # --- ADD 3 ---
        # Default Schedule (Mon-Fri)
        add_days = 3
        # Monday -> Thursday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 9)))

        # Tuesday -> Friday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 10)))

        # Wednesday -> Monday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 13)))

        # Thursday -> Tuesday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 14)))

        # Friday -> Wednesday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 15)))

        # Saturday -> Wednesday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 15)))

        # Sunday -> Wednesday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 15)))

        #
        # Default Schedule (Mon-Fri)
        add_days = 4
        # Monday -> Friday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 10)))

        # Tuesday -> Monday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 13)))

        # Wednesday -> Tuesday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 14)))

        # Thursday -> Wednesday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 15)))

        # Friday -> Thursday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 16)))

        # Saturday -> Thursday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 16)))

        # Sunday -> Thursday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 16)))

        #
        # Default Schedule (Mon-Fri)
        add_days = 5
        # Monday -> Monday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 13)))

        # Tuesday -> Tuesday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 14)))

        # Wednesday -> Wednesday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 15)))

        # Thursday -> Thursday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 16)))

        # Friday -> Friday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 17)))

        # Saturday -> Friday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 17)))

        # Sunday -> Friday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 17)))

        # --- ADD 6 ---
        # Default Schedule (Mon-Fri)
        add_days = 6

        # Monday -> Next Tuesday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 14)))

        # Tuesday -> Next Wednesday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 15)))

        # Wednesday -> Next Thursday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 16)))

        # Thursday -> Next Friday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 17)))

        # Friday -> Monday After Next
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 20)))

        # Saturday -> Monday After Next
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 20)))

        # Sunday -> Monday After Next
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 20)))

        # --- ADD 7 ---
        # Default Schedule (Mon-Fri)
        add_days = 7

        # Monday -> Next Wednesday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 15)))

        # Tuesday -> Next Thursday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 16)))

        # Wednesday -> Next Friday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 17)))

        # Thursday -> Monday After Next
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 20)))

        # Friday -> Tuesday After Next
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 21)))

        # Saturday -> Tuesday After Next
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 21)))

        # Sunday -> Monday After Next
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 21)))

        # --- ADD 8 ---
        # Default Schedule (Mon-Fri)
        add_days = 8

        # Monday -> Next Thursday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 16)))

        # Tuesday -> Next Friday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 17)))

        # Wednesday -> Monday After Next
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 20)))

        # Thursday -> Tuesday After Next
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 21)))

        # Friday -> Wednesday After Next
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 22)))

        # Saturday -> Wednesday After Next
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 22)))

        # Sunday -> Wednesday After Next
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days), equal_to(date(2023, 3, 22)))

    def test_service_day_add_to_fri_sat_sun(self):
        schedule = (Day.FRI, Day.SAT, Day.SUN)
        # Monday -> Friday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, 1, schedule), equal_to(date(2023, 3, 10)))

        # Tuesday -> Friday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, 1, schedule), equal_to(date(2023, 3, 10)))

        # Wednesday -> Friday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, 1, schedule), equal_to(date(2023, 3, 10)))

        # Thursday -> Friday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, 1, schedule), equal_to(date(2023, 3, 10)))

        # Friday -> Saturday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, 1, schedule), equal_to(date(2023, 3, 11)))

        # Saturday -> Sunday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, 1, schedule), equal_to(date(2023, 3, 12)))

        # Sunday -> Friday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, 1, schedule), equal_to(date(2023, 3, 17)))

        # --- ADD 2 ---
        add_days = 2
        # Monday -> Saturday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 11)))

        # Tuesday -> Saturday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 11)))

        # Wednesday -> Saturday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 11)))

        # Thursday -> Saturday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 11)))

        # Friday -> Sunday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 12)))

        # Saturday -> Friday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 17)))

        # Sunday -> Sunday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # --- ADD 3 ---

        add_days = 3
        # Monday -> Sunday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 12)))

        # Tuesday -> Sunday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 12)))

        # Wednesday -> Sunday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 12)))

        # Thursday -> Sunday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 12)))

        # Friday -> Next Friday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 17)))

        # Saturday -> Next Saturday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Sunday -> Next Sunday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 19)))

        # --- ADD 4 ---
        add_days = 4
        # Monday -> Next Friday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 17)))

        # Tuesday -> Next Friday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 17)))

        # Wednesday -> Next Friday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 17)))

        # Thursday -> Next Friday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 17)))

        # Friday -> Next Saturday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Saturday -> Next Sunday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 19)))

        # Sunday -> Friday after next
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 24)))

        # --- ADD 5 ---
        add_days = 5
        # Monday -> Next Saturday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Tuesday -> Next Saturday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Wednesday -> Next Saturday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Thursday -> Next Saturday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Friday -> Next Sunday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 19)))

        # Saturday -> Friday After Next
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 24)))

        # Sunday -> Saturday After Next
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # --- ADD 6 ---
        add_days = 6

        # Monday -> Sunday after next
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 19)))

        # Tuesday -> Sunday after next
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 19)))

        # Wednesday -> Sunday after next
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 19)))

        # Thursday -> Sunday after next
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 19)))

        # Friday -> Friday After Next
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 24)))

        # Saturday -> Saturday After Next
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Sunday -> Sunday After Next
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 26)))

        # --- ADD 7 ---
        add_days = 7

        # Monday -> Friday after Next
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 24)))

        # Tuesday -> Friday after next
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 24)))

        # Wednesday -> Friday after next
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 24)))

        # Thursday -> Friday after next
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 24)))

        # Friday -> Saturday After Next
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Saturday -> Sunday after next
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 26)))

        # Sunday -> Three Fridays out
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 31)))

        # --- ADD 8 ---
        # Default Schedule (Mon-Fri)
        add_days = 8

        # Monday -> Third Saturday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Tuesday -> Third Saturday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Wednesday -> Third Saturday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Thursday -> Third Saturday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Friday -> Third Sunday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 26)))

        # Saturday -> Third Friday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 31)))

        # Sunday -> Third Saturday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 1)))

    def test_service_day_add_to_mon_wed_sat(self):
        schedule = (Day.MON, Day.WED, Day.SAT)
        add_days = 1
        # Monday -> Wednesday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 8)))

        # Tuesday -> Wednesday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 8)))

        # Wednesday -> Saturday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 11)))

        # Thursday -> Saturday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 11)))

        # Friday -> Saturday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 11)))

        # Saturday -> Monday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 13)))

        # Sunday -> Monday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 13)))

        # --- ADD 2 ---
        add_days = 2
        # Monday -> Saturday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 11)))

        # Tuesday -> Saturday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 11)))

        # Wednesday -> Monday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 13)))

        # Thursday -> Monday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 13)))

        # Friday -> Monday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 13)))

        # Saturday -> Wednesday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 15)))

        # Sunday -> Wednesday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 15)))

        # --- ADD 3 ---

        add_days = 3
        # Monday -> Monday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 13)))

        # Tuesday -> Monday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 13)))

        # Wednesday -> Wednesday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 15)))

        # Thursday -> Wednesday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 15)))

        # Friday -> Wednesday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 15)))

        # Saturday ->  Saturday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Sunday -> Saturday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # --- ADD 4 ---
        add_days = 4
        # Monday -> Next Wednesday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 15)))

        # Tuesday -> Next Wednesday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 15)))

        # Wednesday -> Next Saturday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Thursday -> Next Saturday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Friday -> Next Saturday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Saturday -> Next Monday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 20)))

        # Sunday -> Next Monday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 20)))

        # --- ADD 5 ---
        add_days = 5
        # Monday -> Next Saturday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Tuesday -> Next Saturday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 18)))

        # Wednesday -> Next Monday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 20)))

        # Thursday -> Next Monday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 20)))

        # Friday -> Next Monday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 20)))

        # Saturday -> Next Wednesday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 22)))

        # Sunday -> Next Wednesday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 22)))

        # --- ADD 6 ---
        add_days = 6

        # Monday -> Monday after next
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 20)))

        # Tuesday -> Monday after next
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 20)))

        # Wednesday -> Wednesday after next
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 22)))

        # Thursday -> Wednesday after next
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 22)))

        # Friday -> Wednesday After Next
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 22)))

        # Saturday -> Saturday After Next
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Sunday -> Saturday After Next
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # --- ADD 7 ---
        add_days = 7

        # Monday -> Wednesday after Next
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 22)))

        # Tuesday -> Wednesday after next
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 22)))

        # Wednesday -> Saturday after next
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Thursday -> Saturday after next
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Friday -> Saturday After Next
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Saturday -> Monday after next
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 27)))

        # Sunday -> Monday after next
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 27)))

        # --- ADD 8 ---
        # Default Schedule (Mon-Fri)
        add_days = 8

        # Monday -> Third Saturday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Tuesday -> Third Saturday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 25)))

        # Wednesday -> Third Monday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 27)))

        # Thursday -> Third Monday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 27)))

        # Friday -> Third Monday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 27)))

        # Saturday -> Third Wednesday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 29)))

        # Sunday -> Third Wednesday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 29)))

    def test_service_day_add_to_tues_only(self):
        schedule = [Day.TUE]
        add_days = 1
        # Monday -> Tuesday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 7)))

        # Tuesday -> Next Tuesday
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 14)))

        # Wednesday -> Tuesday
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 14)))

        # Thursday -> Tuesday
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 14)))

        # Friday -> Tuesday
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 14)))

        # Saturday -> Tuesday
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 14)))

        # Sunday -> Tuesday
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 14)))

        # --- ADD 2 ---
        add_days = 2
        # Monday -> Next Tuesday
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 14)))

        # Tuesday -> Tuesday after next
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 21)))

        # Wednesday -> Tuesday after next
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 21)))

        # Thursday -> Tuesday after next
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 21)))

        # Friday -> Tuesday after next
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 21)))

        # Saturday -> Tuesday after next
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 21)))

        # Sunday -> Tuesday after next
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 21)))

        # --- ADD 3 ---

        add_days = 3
        # Monday -> Jump 2 Tuesdays
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 21)))

        # Tuesday -> Jump 2 Tuesdays
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 28)))

        # Wednesday -> Jump 2 Tuesdays
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 28)))

        # Thursday -> Jump 2 Tuesdays
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 28)))

        # Friday -> Jump 2 Tuesdays
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 28)))

        # Saturday ->  Jump 2 Tuesdays
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 28)))

        # Sunday -> Jump 2 Tuesdays
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 28)))

        # --- ADD 4 ---
        add_days = 4
        # Monday -> Jump 3 Tuesdays
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 3, 28)))

        # Tuesday -> Jump 3 Tuesdays
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 4)))

        # Wednesday -> Jump 3 Tuesdays
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 4)))

        # Thursday -> Jump 3 Tuesdays
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 4)))

        # Friday -> Jump 3 Tuesdays
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 4)))

        # Saturday -> Jump 3 Tuesdays
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 4)))

        # Sunday -> Jump 3 Tuesdays
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 4)))

        # --- ADD 5 ---
        add_days = 5
        # Monday -> Jump 4 Tuesdays
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 4)))

        # Tuesday -> Jump 4 Tuesdays
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 11)))

        # Wednesday -> Jump 4 Tuesdays
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 11)))

        # Thursday -> Jump 4 Tuesdays
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 11)))

        # Friday -> JUMP 4 Tuesdays
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 11)))

        # Saturday -> Jump 4 Tuesdays
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 11)))

        # Sunday -> Jump 4 Tuesdays
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 11)))

        # --- ADD 6 ---
        add_days = 6

        # Monday -> Jump 5 Tuesdays
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 11)))

        # Tuesday -> Jump 5 Tuesdays
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 18)))

        # Wednesday -> Jump 5 Tuesdays
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 18)))

        # Thursday -> Jump 5 Tuesdays
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 18)))

        # Friday -> Jump 5 Tuesdays
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 18)))

        # Saturday -> Jump 5 Tuesdays
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 18)))

        # Sunday -> Jump 5 Tuesdays
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 18)))

        # --- ADD 7 ---
        add_days = 7

        # Monday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 18)))

        # Tuesday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 25)))

        # Wednesday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 25)))

        # Thursday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 25)))

        # Friday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 25)))

        # Saturday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 25)))

        # Sunday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 25)))

        # --- ADD 8 ---
        # Default Schedule (Mon-Fri)
        add_days = 8

        # Monday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 6)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 4, 25)))

        # Tuesday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 7)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 5, 2)))

        # Wednesday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 8)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 5, 2)))

        # Thursday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 9)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 5, 2)))

        # Friday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 10)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 5, 2)))

        # Saturday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 11)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 5, 2)))

        # Sunday -> Jump 6 Tuesdays
        t_date = date(2023, 3, 12)
        assert_that(service_day_add(t_date, add_days, schedule), equal_to(date(2023, 5, 2)))

    def test_map_schedule_txt_list_to_day_num_list(self):
        test_str = '["Mon", "Tue"]'
        assert_that(map_schedule_txt_to_day_list(test_str), equal_to([Day.MON, Day.TUE]))

    def test_days_in_period(self):
        test_schedule = [Day.MON, Day.WED, Day.FRI, Day.SUN]

        assert_that(day_count_in_range(date(2023, 3, 6), date(2023, 3, 18), test_schedule),
                    equal_to(7), "Test Days in Period")

        assert_that(day_count_in_range(date(2023, 3, 6), date(2023, 3, 19), test_schedule),
                    equal_to(8), "Test Days in Period")

    def test_service_range(self):
        test_schedule = [Day.MON, Day.WED, Day.FRI, Day.SUN]
        in_schedule = DateInSchedule(test_schedule)
        day_gen = days_in_range(date(2023, 3, 6), date(2023, 3, 18),test_schedule )

        assert_that(list(day_gen), only_contains(in_schedule), "all days in range are in schedule")
