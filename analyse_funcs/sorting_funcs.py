import pandas as pd


def get_biggest_cities_hotels_df(df: pd.DataFrame) -> pd.DataFrame:
    return pd.concat(
        (
            max(
                (
                    df.loc[df["Country"] == country].loc[
                        df.loc[df["Country"] == country]["City"] == city
                    ]
                    for city in pd.unique(df.loc[df["Country"] == country]["City"])
                ),
                key=lambda x: len(x),
            )
            for country in pd.unique(df["Country"])
        )
    )


def get_biggest_cities_series(df: pd.DataFrame) -> pd.Series:
    gb = df.groupby(["Country", "City"])
    return pd.Series((row[0][1] for row in gb), index=(row[0][0] for row in gb))
