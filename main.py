#!/usr/bin/env python3
"""
Making a simple date offset calculator for calendar of your life apps
"""

import os
import sys
from datetime import date
from pathlib import Path
from typing import List, Literal, Optional, Union


import yaml
import termcolor
from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, validator


# Global Constants
# ---------------------------------------------------------------------------

WEEKS_PER_YEAR = 52
TOTAL_YEARS = 100

# Data Models
# ---------------------------------------------------------------------------

class DateRange(BaseModel):
    start: date
    end: date

class LifeEvent(BaseModel):
    name: str
    start: date
    end: date
    color: str

    @validator('color')
    def check_color_exist(cls, v):
        if v not in termcolor.COLORS.keys():
            raise ValueError(f"Color '{v}' is not supported by termcolor")
        return v


class LifeCalendar(BaseModel):
    birthday: date
    events: List[LifeEvent]

# Calendar Operations
# ---------------------------------------------------------------------------

class Calendar():

    def __init__(self, calendar_path: Union[Path, str]) -> None:
        with open(calendar_path, 'r') as calendar_file:
            calendar_data = yaml.load(calendar_file, yaml.FullLoader)
            self._data = LifeCalendar(**calendar_data)


    def get_event(self, week: DateRange) -> Optional[LifeEvent]:
        life_event = None
        for event in self._data.events:
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

    def display(self):
        for year_idx in range(TOTAL_YEARS):
            print(f"{year_idx+1:3} : ", end='')
            for week_idx in range(WEEKS_PER_YEAR):
                week = DateRange(
                    start = (
                        self._data.birthday + \
                        relativedelta(years=year_idx, weeks=week_idx)
                    ),
                    end = (
                        self._data.birthday + \
                        relativedelta(years=year_idx, weeks=week_idx+1)
                    )
                )
                event = self.get_event(week)
                if event:
                    termcolor.cprint("#", event.color, end='')
                else:
                    print(".", end='')
            print("")

# Runtime Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    c = Calendar(sys.argv[1])
    c.display()
