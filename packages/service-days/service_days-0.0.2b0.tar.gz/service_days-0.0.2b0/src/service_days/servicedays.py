import json
from datetime import date, timedelta
from enum import Enum, IntFlag
import logging

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
                    week_schedule=(Day.MON, Day.TUE, Day.WED, Day.THU, Day.FRI)) -> date:
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
    if cur_day not in week_schedule:
        if cur_day.value < min_sched_day:
            # max sched day, previous week
            cur_svc_date = start_date - timedelta(weeks=1)
            cur_svc_date = cur_svc_date + timedelta((max_sched_day - cur_svc_date.weekday()) % 7)
            logger.debug(f"Adjusting for current day not in schedule: {cur_day} < {min_sched_day}")
            logger.debug(f"New base date date: {cur_svc_date}")

        elif min_sched_day < cur_day.value < max_sched_day:
            # go backwards by day,until we hit previous sched day
            while cur_day not in week_schedule:
                cur_svc_date -= timedelta(days=1)
                cur_day = Day(cur_svc_date.weekday())

        elif max_sched_day < cur_day.value:
            # go backwards by day,until we hit previous sched day
            while cur_day not in week_schedule:
                cur_svc_date -= timedelta(days=1)
                cur_day = Day(cur_svc_date.weekday())
        else:
            raise ValueError(f"Unexpected condition: {cur_day}")

    new_date = cur_svc_date + timedelta(weeks=weeks)
    if len(week_schedule) > 1:
        if days == 0:
            # if weeks > len(week_schedule):
            #     new_date -= timedelta(new_date.weekday() - len(week_schedule) + 1)
            # elif new_date.weekday() > len(week_schedule) - 1:
            #     new_date -= timedelta(new_date.weekday() - len(week_schedule) + 1)
            # Make sure new_date is in the week_schedule
            t_day = Day(new_date.weekday())
            while t_day not in week_schedule:
                # If result is not one of the days in the week schedule, increment by 1 day
                new_date += timedelta(days=1)
                t_day = Day(new_date.weekday())

        else:
            for _ in range(days):
                # increment # of days passed in
                new_date += timedelta(days=1)
                t_day = Day(new_date.weekday())

                while t_day not in week_schedule:
                    # If result is not one of the days in the week schedule, increment by 1 day
                    new_date += timedelta(days=1)
                    t_day = Day(new_date.weekday())

    else:
        business_date = []
        for wd in week_schedule:
            if wd >= (7 - start_date.weekday()):
                next_day = (wd - (7 - start_date.weekday()) + 1) + (7 * (work_days_to_add - 1))
            else:
                next_day = (wd + start_date.weekday() + 1) + (7 * (work_days_to_add - 1))
            business_date.append(next_day)
        start_date += timedelta(min(business_date))
        new_date = start_date
    return new_date


def map_schedule_txt_list_to_day_num_list(process_sched_day_list, in_place=False):
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

        _extracted_from_map_schedule_txt_list_to_day_num_list_16(
            item, work_list, index
        )
    return work_list


def _extracted_from_map_schedule_txt_list_to_day_num_list_16(item, work_list, index):
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
