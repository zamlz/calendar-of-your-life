#!/usr/bin/env python3
"""
Making a simple date offset calculator for calendar of your life apps
"""

from __future__ import annotations

import json
import os
import string
import sys
from argparse import ArgumentParser
from datetime import date
from enum import StrEnum
from pathlib import Path
from typing import List, Optional, Union

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel


WEEKS_PER_YEAR = 52
TOTAL_YEARS = 100
BASE64 = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
ANSI_BOLD = "\033[1m"
ANSI_INVERT = "\033[7m"
ANSI_RESET = "\033[0m"


class Color(StrEnum):
    BLACK = 'black'
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'
    MAGENTA = 'magenta'
    CYAN = 'cyan'
    GRAY = 'gray'


COLOR_MAP = {
    Color.BLACK: "\033[0;30m",
    Color.RED: "\033[0;31m",
    Color.GREEN: "\033[0;32m",
    Color.YELLOW: "\033[0;33m",
    Color.BLUE: "\033[0;34m",
    Color.MAGENTA: "\033[0;35m",
    Color.CYAN: "\033[0;36m",
    Color.GRAY: "\033[0;37m",
}


class DateRange(BaseModel):
    start: date
    end: date

    @property
    def duration(self) -> int:
        return (self.end - self.start).days


class LifeEvent(DateRange):
    name: str
    color: Color


class LifeCalendar(BaseModel):
    name: str
    birthday: date
    events: List[LifeEvent]

    @classmethod
    def from_json(cls, calendar_path: Path) -> LifeCalendar:
        with open(calendar_path, 'r') as calendar_file:
            calendar_data = json.load(calendar_file)
            return cls(**calendar_data)

    def __getitem__(self, week: DateRange) -> Optional[LifeEvent]:
        life_event = None
        # smaller events have a higher priority on the calendar!
        for event in reversed(sorted(self.events, key=lambda x: x.duration)):
            # fully bounded
            if event.start >= week.start and event.end <= week.end:
                return event
            # out of bounds cases
            elif week.start > event.end or week.end < event.start:
                continue
            # partial intersection
            elif week.start >= event.start and week.start <= event.end:
                life_event = event
            elif week.end >= event.start and week.end <= event.end:
                life_event = event
        return life_event


def render_calendar(calendar: LifeCalendar):
    PADDING = " "*6
    print(f"\n{PADDING}{ANSI_BOLD}{calendar.name}{ANSI_RESET}")
    print(PADDING + "-"*WEEKS_PER_YEAR)

    for year_idx in range(TOTAL_YEARS):
        year_start = None
        year_end = None

        print(f"{year_idx+1:3} : ", end='')

        for week_idx in range(WEEKS_PER_YEAR):
            week_start = (
                calendar.birthday + \
                relativedelta(years=year_idx, weeks=week_idx)
            )
            week_end = (
                calendar.birthday + \
                relativedelta(years=year_idx, weeks=week_idx+1)
            )
            if year_start is None:
                year_start = week_start
            year_end = week_end
            week = DateRange(start=week_start, end=week_end)
            event = calendar[week]
            display_char = '.'
            if event:
                base64_char = BASE64[week_idx]
                display_char = (
                    COLOR_MAP[event.color] +
                    ANSI_INVERT +
                    ANSI_BOLD +
                    base64_char +
                    ANSI_RESET
                )
            print(display_char, end='')
        print(f"  [{year_start}, {year_end}] // Age {year_idx}")


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('calendar_path', type=Path)
    args = parser.parse_args()
    calendar = LifeCalendar.from_json(args.calendar_path)
    render_calendar(calendar)


if __name__ == "__main__":
    main()
