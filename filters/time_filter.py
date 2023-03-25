"""
This file contains all the time-related filter function.
"""


from enum import Enum
from functools import reduce
from typing import Callable
import pandas as pd



from file_reader.preprocessing import DataPipeline


class Weekday(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6

def below_interval(days:int = 0, hours:int = 0, mins:int = 0 , secs:int = 0)-> DataPipeline:
    """
    Returns a function that filters the rental time below a certain criteria
    """
    time_delta_object = pd.Timedelta(
        days=days,
        hours=hours,
        minutes=mins,
        seconds=secs)

    def filter_pipeline(df: pd.DataFrame) -> pd.DataFrame:
        return df[df["rent"] < time_delta_object]

    return filter_pipeline

def over_interval(days:int = 0, hours:int = 0, mins:int = 0 , secs:int = 0)-> DataPipeline:
    """
    Returns a function that filters the rental time over a certain criteria
    """
    time_delta_object = pd.Timedelta(
        days=days,
        hours=hours,
        minutes=mins,
        seconds=secs)

    def filter_pipeline(df: pd.DataFrame) -> pd.DataFrame:
        return df[df["rent"] > time_delta_object]

    return filter_pipeline



def weekday_filter(weekdays:list[Weekday])->DataPipeline:
    """
    Returns a function that filters the renting day on a list of specific weekdays
    """
    def filter_pipeline(df:pd.DataFrame) -> pd.DataFrame:

        weekday_mask_list:list[pd.Series[bool]] = [ (df['infodate'].dt.day_of_week == wd.value) for wd in weekdays]
        weekday_mask = reduce(lambda accum_mask, current_mask: accum_mask | current_mask, weekday_mask_list)

        return df[weekday_mask]

    return filter_pipeline