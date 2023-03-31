import pandas as pd
import requests as rq
from pathlib import Path

COORD_FILE =  Path("DATA") / "coord.pq"
COORD_SOURCE_URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

def load_geoinfo() -> pd.DataFrame:
    """
    Loads the coordination info for the Youbike 2.0 data.

    If file not found, download it from the internet, and save it as a parque
    object. Cleaning is done in this step.

    Return a pandas dataframe.
    """
    if COORD_FILE.exists():
        return pd.read_parquet(COORD_FILE)

    print("coordination file not found. Downloading...")
    try:
        respond_obj = __download_geoinfo()
        geo_df = pd.DataFrame(respond_obj)
        geo_df['sna'] = geo_df['sna'].str.replace('YouBike2.0_', '')
        youbike_stop_loc = geo_df[['sno','sna','lat', 'lng']]

        if not COORD_FILE.parent.exists(): COORD_FILE.parent.mkdir(parents=True)

        youbike_stop_loc.to_parquet(COORD_FILE)

        return youbike_stop_loc

    except rq.ConnectTimeout as ce:
        raise rq.ConnectionError("Please check the Internet")


def __download_geoinfo()-> dict:
    """Downloads youbike 2.0 info"""
    youbike_stop_data = rq.get(COORD_SOURCE_URL).json()

    return youbike_stop_data