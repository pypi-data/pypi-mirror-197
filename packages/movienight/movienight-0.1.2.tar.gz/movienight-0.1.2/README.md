Movie Night
============

**movienight** is a python package that uses NLP to return a list of recommended movies based on free form text input. **movienight** is not intended to be that useful and is more of a personal project.

    ├──src/movienight/
    │   └── _MovieNight.py           <- Holds all classes and functions relevant to MovieNigh
    │       └── datasets/        
    │           ├── _base.py         <- Utility function to load tmdb dataset
    │           ├── _tmdb.py         <- Script used to query TMDB api
    │           ├── _config.py       <- Config file that holds TMDB api key. Fill in with your own api key.
    │           └── data             <- Holds datasets used by MovieNight
    ├──MovieFinderApp/
    │   └── movie
    ├── demo.ipynb                   <- Notebook used to test MovieNight functionality
    └── README.md

Quick Start
------------
This project uses ```poetry``` to manage dependencies. Download ```poetry``` following the instructions found [here](https://python-poetry.org/docs/), then navigate to the directory that contains the ```pyproject.toml``` file and run:

```
poetry install
```