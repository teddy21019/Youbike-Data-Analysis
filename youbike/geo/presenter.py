""" A collection of presenters of a youbike statistical data in geological form"""
from typing import Self
import pandas as pd
from abc import ABC, abstractmethod
import folium

class GeoPresentation(ABC):
    def present(self, weight: str):
        ...

class MapEdgePresentation(GeoPresentation):
    def __init__(self, df:pd.DataFrame, map_object:folium.Map):
        self.m = map_object
        self.df = df.copy()
        self.validate()
        self.edge_weight = ''
        self.node_weight = ''

    def validate(self):
        validation_set = {
            "lat_rent", 'lng_rent',
            'lat_return', 'lng_return',
        }

        if not validation_set.issubset(self.df.columns):
            raise ValueError(f"Dataframe should include all of {validation_set}. Try transforming it using geo.add_coordinate")

    def set_edge_weight(self, weight_name: str, line_weight_scale:float=1):
        self.edge_weight = weight_name

        for index, row in self.df.iterrows():
            source = (row['lat_rent'], row['lng_rent'])
            target = (row['lat_return'], row['lng_return'])
            count = row[weight_name]

            # Define the style of the line
            line_color = '#3388ff'
            line_opacity = 0.5
            line_weight = count * line_weight_scale

            # Create a folium.PolyLine object and add it to the map
            folium.PolyLine([source, target], color=line_color, weight=line_weight, opacity=line_opacity).add_to(self.m)
        return Self

    def set_point_weight(self, weight_name: str):
        self.node_weight = weight_name
        return Self
