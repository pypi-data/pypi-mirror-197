import json
from datetime import date, timedelta
from enum import Enum, IntFlag
import logging
from typing import List, Generator

from service_days import __version__

LOG_FORMAT: str = f"v{__version__} | %(levelname)s | %(asctime)s | %(funcName)s | %(message)s"
LOG_LEVEL: str = "DEBUG"
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


# Make some Constants
class Day(IntFlag):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


def service_day_add(start_date: date, work_days_to_add: int,
                    week_schedule: List[Day] = (Day.MON, Day.TUE, Day.WED, Day.THU, Day.FRI)) -> date:
    """
    Everything prior to "next service" day is considered part of the current service day.  Given a M-W Schedule, and
    given the current date is a Saturday or Sunday, the date math is based on concept the current service day is
    Friday.

    :param start_date:
    :param work_days_to_add:
    :param week_schedule:
    :return:
    """
    logger.debug(f"ENTERING: service_day_add: adding {work_days_to_add} days to {start_date} with "
                 f"schedule of {week_schedule}")

    weeks, days = divmod(work_days_to_add, len(week_schedule))
    logger.debug(f"Adjusting for weeks: {weeks}, days: {days}")

    cur_svc_date = start_date  # start with assumption that current date is a service day
    min_sched_day = min([d.value for d in week_schedule])
    max_sched_day = max([d.value for d in week_schedule])

    cur_day = Day(start_date.weekday())

    # If not a service day, find calendar date of previous service day
    if cur_day not in week_schedule:
        if cur_day.value < min_sched_day:
            # max service day, previous week
            cur_svc_date = start_date - timedelta(weeks=1)
            cur_svc_date = cur_svc_date + timedelta((max_sched_day - cur_svc_date.weekday()) % 7)
            logger.debug(f"Adjusting for current day not in schedule: {cur_day} < {min_sched_day}")
            logger.debug(f"New base date date: {cur_svc_date}")

        elif (
                min_sched_day < cur_day.value < max_sched_day
                or max_sched_day < cur_day.value
        ):
            # go backwards by day,until we hit previous service day
            while cur_day not in week_schedule:
                cur_svc_date -= timedelta(days=1)
                cur_day = Day(cur_svc_date.weekday())

        else:
            raise ValueError(f"Unexpected condition: {cur_day}")

    # Now that we are on a service day, add any weeks
    new_date = cur_svc_date + timedelta(weeks=weeks)

    # Now adjust for any remaining days
    for _ in range(days):
        # increment # of days passed in
        new_date += timedelta(days=1)
        t_day = Day(new_date.weekday())

        while t_day not in week_schedule:
            # If result is not one of the days in the week schedule, increment by 1 day
            new_date += timedelta(days=1)
            t_day = Day(new_date.weekday())

    return new_date


def day_count_in_range(start_date: date, end_date: date, week_schedule: List[Day]) -> int:
    return len(list(days_in_range(start_date, end_date, week_schedule)))


def days_in_range(start_date: date, end_date: date, week_schedule: List[Day]) -> Generator[date, None, None]:

    e_date = start_date
    e_day = Day(e_date.weekday())
    keep_working = True
    while keep_working:
        if e_day in week_schedule:
            yield e_date
        e_date = service_day_add(e_date, 1, week_schedule)
        e_day = Day(e_date.weekday())
        if e_date > end_date:
            keep_working = False


def map_schedule_txt_to_day_list(process_sched_day_list, in_place=False):
    if isinstance(process_sched_day_list, str):
        str_to_list = json.loads(process_sched_day_list)
        process_sched_day_list = [elem.strip() for elem in str_to_list]

    if in_place:
        work_list = process_sched_day_list
    elif process_sched_day_list is None:
        return range(7)

    else:
        work_list = list(range(len(process_sched_day_list)))

    for index, item in enumerate(process_sched_day_list):
        _extracted_from_map_schedule_txt_list_to_day_enum(
            item, work_list, index
        )
    return work_list


def _extracted_from_map_schedule_txt_list_to_day_enum(item, work_list, index):
    if item.strip().casefold() == "Mon".casefold():
        work_list[index] = Day.MON.value

    if item.strip().casefold() == "Tue".casefold():
        work_list[index] = Day.TUE.value

    if item.strip().casefold() == "Wed".casefold():
        work_list[index] = Day.WED.value

    if item.strip().casefold() == "Thu".casefold():
        work_list[index] = Day.THU.value

    if item.strip().casefold() == "Fri".casefold():
        work_list[index] = Day.FRI.value

    if item.strip().casefold() == "Sat".casefold():
        work_list[index] = Day.SAT.value

    if item.strip().casefold() == "Sun".casefold():
        work_list[index] = Day.SUN.value
