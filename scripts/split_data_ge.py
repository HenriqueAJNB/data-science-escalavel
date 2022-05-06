from pathlib import Path

import pandas as pd

PATH_ROOT = Path(".").absolute()

df = pd.read_csv(PATH_ROOT / "AirQualityUCI.csv", sep=";")

df.dropna(axis=0, how="all", inplace=True)

df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

df["year"] = df.Date.dt.year

df_2004 = df.query("year == 2004")
df_2005 = df.query("year == 2005")

df_2004.to_csv(PATH_ROOT / "data" / "first_data.csv", sep=";", index=False)
df_2005.to_csv(PATH_ROOT / "data" / "second_data.csv", sep=";", index=False)
