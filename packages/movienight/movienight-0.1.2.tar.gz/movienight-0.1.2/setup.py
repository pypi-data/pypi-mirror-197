# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['movienight', 'movienight.datasets']

package_data = \
{'': ['*'], 'movienight.datasets': ['data/*']}

install_requires = \
['dash[diskcache]>=2.8.1,<3.0.0',
 'diskcache>=5.4.0,<6.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'plotly>=5.13.1,<6.0.0',
 'sentence-transformers>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'movienight',
    'version': '0.1.2',
    'description': '',
    'long_description': 'Movie Night\n============\n\n**movienight** is a python package that uses NLP to return a list of recommended movies based on free form text input. **movienight** is not intended to be that useful and is more of a personal project.\n\n    ├──src/movienight/\n    │   └── _MovieNight.py           <- Holds all classes and functions relevant to MovieNigh\n    │       └── datasets/        \n    │           ├── _base.py         <- Utility function to load tmdb dataset\n    │           ├── _tmdb.py         <- Script used to query TMDB api\n    │           ├── _config.py       <- Config file that holds TMDB api key. Fill in with your own api key.\n    │           └── data             <- Holds datasets used by MovieNight\n    ├──MovieFinderApp/\n    │   └── movie\n    ├── demo.ipynb                   <- Notebook used to test MovieNight functionality\n    └── README.md\n\nQuick Start\n------------\nThis project uses ```poetry``` to manage dependencies. Download ```poetry``` following the instructions found [here](https://python-poetry.org/docs/), then navigate to the directory that contains the ```pyproject.toml``` file and run:\n\n```\npoetry install\n```',
    'author': 'dan-kwon',
    'author_email': 'danielkwon02@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
