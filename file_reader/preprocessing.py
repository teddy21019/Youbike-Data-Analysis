"""
Reading of Youbike Data and future cleaning pipeline
"""

from functools import cached_property
from typing import Self, Callable
import pandas as pd

DataPipeline = Callable[[pd.DataFrame], pd.DataFrame]

class YoubikeDataReader:
    """
    Reader of the youbike data file.

    Reads a single youbike data, typically a month.

    Data type transform:
    >>> {
            'rent_time'     : 'datetime64[ns]',
            'return_time'   : 'datetime64[ns]',
            'rent'          : 'timedelta64[ns]',
            'infodate'     : 'datetime64[ns]',
        }
    """
    def __init__(self, file_path:str) -> None:

        self.df: pd.DataFrame =  pd.read_csv(file_path)
        self.df = self.df.astype({
            'rent_time'     : 'datetime64[ns]',
            'return_time'   : 'datetime64[ns]',
            'rent'          : 'timedelta64[ns]',
            'infodate'     : 'datetime64[ns]',
            })

class YoubikeDataFactory:
    """
    Takes in a `YoubikeDataReader`, so that the loaded CSV can be reused over without needing to reload.
    Call the `filter__` functions to construct a data filtering pipeline.

    The filter
    """
    def __init__(self, data_reader: YoubikeDataReader) -> None:
        self.data_reader = data_reader

        self.pipeline_list:list[DataPipeline] = []

    def filter_location(self, location_filter: DataPipeline)->Self:
        """Pass a pipeline function that filters a location"""
        self.add_pipeline(location_filter)
        return self

    def filter_time(self, time_filter: DataPipeline)->Self:
        """Pass a pipeline function that filters a time or time interval"""
        self.add_pipeline(time_filter)
        return self

    def add_pipeline(self, pipeline: DataPipeline)-> Self:
        """Pass a pipeline function."""
        self.pipeline_list.append(pipeline)
        return self

    @cached_property
    def df(self):
        """Retrieve the processed dataframe.

        Only when `df` is called will the pipeline be actually calculated.

        It is a cached property, so if new pipeline is added afterward, it will not be updated!!!"""
        return self.build()

    def build(self):
        """Rebuild the dataframe from pipeline"""
        try:
            del self.df
        except:
            pass

        temp_df = self.data_reader.df.copy()
        for fn in self.pipeline_list:
            temp_df = fn(temp_df)

        return temp_df

    def duplicate(self, n=1) -> list[Self]:
        """
        Create a copy of this factory up to current pipeline element.

        Use this function to construct a series of data with mutual preprocessing pipeline
        """
        descendant_factories: list[Self] = [self.__class__(self.data_reader) for _ in range(n)]
        for i in range(n):
            descendant_factories[i].pipeline_list = self.pipeline_list.copy()
        return descendant_factories