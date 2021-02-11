import sys
from typing import Optional
from zipfile import BadZipFile, ZipFile

import pandas as pd


def read_csv_from_zip(
    path: str,
) -> pd.DataFrame:
    """
    Unpack .zip file, read all .csv files, filter invalid data and return dataframe
    """
    read_date = []
    try:
        with ZipFile(path, "r") as myzip:
            files_list = [file for file in myzip.namelist() if file.endswith(".csv")]

            for filename in files_list:
                try:
                    file = myzip.open(filename)
                except UnicodeDecodeError:
                    sys.stderr.write(f"Some problems with encoding of {filename}")
                    continue
                filtered_df = filter_hotels(pd.read_csv(file))

                if filtered_df is None:
                    sys.stderr.write(f"Some problems with colomns of {filename}")
                    continue
                read_date.append(filtered_df.dropna().drop(columns=["Id"]))
    except BadZipFile:
        sys.stderr.write("File is not a zip file")
        sys.exit(1)

    if not read_date:
        sys.stderr.write("No valid information in zip file")
        sys.exit(1)

    return pd.concat(read_date, ignore_index=True)


def filter_hotels(hotels_df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Filter hotels data and create dict
    Checks:
    1) Latitude and Longitude are float
    2) Latitude belongs to the interval [-90, 90]
    3) Longitude belongs to the interval [-180, 180]
    """
    if any(
        map(
            lambda param: param not in hotels_df.keys(),
            ("Country", "City", "Latitude", "Longitude"),
        )
    ):
        return None

    hotels_df["Latitude"] = (
        hotels_df["Latitude"]
        .astype("str")
        .str.extract(r"(-?\d+\.\d+)", expand=False)
        .astype("float")
    )
    hotels_df["Longitude"] = (
        hotels_df["Longitude"]
        .astype("str")
        .str.extract(r"(-?\d+\.\d+)", expand=False)
        .astype("float")
    )

    return hotels_df.loc[
        (hotels_df["Latitude"].astype("float") >= -90)
        & (hotels_df["Latitude"].astype("float") <= 90)
        & (hotels_df["Longitude"].astype("float") >= -180)
        & (hotels_df["Longitude"].astype("float") <= 180)
    ]
