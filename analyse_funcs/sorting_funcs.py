import pandas as pd


def get_top_cities_hotels_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analise dataframe with all hotels and return dataframe with only hotels in the biggest cities
    """
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


def get_top_cities_series(df: pd.DataFrame) -> pd.Series:
    """
    Analise dataframe with all hotels and return pd.Series with the biggest cities
    """
    gb = df.groupby(["Country", "City"])
    return pd.Series((row[0][1] for row in gb), index=(row[0][0] for row in gb))
