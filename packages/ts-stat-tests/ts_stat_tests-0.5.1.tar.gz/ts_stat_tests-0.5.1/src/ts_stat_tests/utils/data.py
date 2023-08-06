import pandas as pd


def load_airline():
    # Inspiration from: sktime.datasets.load_airline()
    data_source = "https://raw.githubusercontent.com/sktime/sktime/main/sktime/datasets/data/Airline/Airline.csv"
    y = pd.read_csv(data_source, index_col=0, dtype={1: float}).squeeze("columns")
    y.index = pd.PeriodIndex(y.index, freq="M", name="Period")
    y.name = "Number of airline passengers"
    return y
