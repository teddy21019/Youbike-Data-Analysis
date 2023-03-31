import pandas as pd
import geo.geo_info

def add_coordinate(youbike_df:pd.DataFrame)-> pd.DataFrame:
    """ Adds coordinate info to the data"""
    geo_df = geo.geo_info.load_geoinfo()

    merged_data = youbike_df.merge(geo_df, left_on='rent_station', right_on='sna') \
        .merge(geo_df, left_on='return_station', right_on='sna', suffixes=('_rent', '_return'))
    return merged_data