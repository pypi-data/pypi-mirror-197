import pandas as pd
from pathlib import Path

def load_tmdb():
    """
    """
    filepath_ = Path("src/movienight/datasets/data/tmdb.csv")
    data_ = pd.read_csv(
        filepath_, 
        dtype={
            "id" : int,
            "title" : str,
            "overview" : str,
            "adult": bool,
            "genre_ids" : object,
            "release_date" : str}
        )
    data_["release_date"] = pd.to_datetime(data_["release_date"])
    data_ = data_[data_.overview.notnull()]
    return data_
    