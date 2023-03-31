import pandas as pd


def NTU_location_filter(df: pd.DataFrame)-> pd.DataFrame:
    """
    Filters the Youbike dataframe to focus solely on names containing "臺大"
    """
    mask_start_ntu = df.rent_station.str.contains('臺大')
    mask_end_ntu = df.return_station.str.contains('臺大')
    df_with_ntu = df[mask_end_ntu & mask_start_ntu]
    return df_with_ntu
