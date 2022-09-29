import pandas as pd
from datetime import datetime


def etl():

    # Extract
    data = pd.read_csv("../data/advertising.csv")

    # Transform
    data["Timestamp"] = pd.to_datetime(data["Timestamp"])

    first_data = data[
        (data["Timestamp"] >= datetime(2016, 1, 1))
        & (data["Timestamp"] < datetime(2016, 5, 1))
    ]
    second_data = data[
        (data["Timestamp"] >= datetime(2016, 5, 1))
        & (data["Timestamp"] < datetime(2016, 8, 1))
    ]

    # Load
    first_data.to_csv("../data/first_data.csv")
    second_data.to_csv("../data/second_data.csv")


if __name__ == "__main__":
    etl()
