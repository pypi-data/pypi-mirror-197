# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src/gdptools_pygeoapi_plugin'}

packages = \
['_pygeoapi_process']

package_data = \
{'': ['*']}

install_requires = \
['click<8',
 'gdptools==0.0.32',
 'numpy>=1.21.0,<2.0.0',
 'pygeoapi>=0.11.0,<0.12.0']

entry_points = \
{'console_scripts': ['gdptools-pygeoapi-plugin = '
                     'gdptools_pygeoapi_plugin.__main__:main']}

setup_kwargs = {
    'name': 'gdptools-pygeoapi-plugin',
    'version': '0.0.4.dev0',
    'description': 'Gdptools Pygeoapi Plugin',
    'long_description': "---\n\ntitle: README\n---Gdptools Pygeoapi Plugin\n========================\n\n[![PyPI](https://img.shields.io/pypi/v/gdptools-pygeoapi-plugin.svg)](https://pypi.org/project/gdptools-pygeoapi-plugin/)\n[![Status](https://img.shields.io/pypi/status/gdptools-pygeoapi-plugin.svg)](https://pypi.org/project/gdptools-pygeoapi-plugin/)\n[![Python Version](https://img.shields.io/pypi/pyversions/gdptools-pygeoapi-plugin)](https://pypi.org/project/gdptools-pygeoapi-plugin)\n[![License](https://img.shields.io/pypi/l/gdptools-pygeoapi-plugin)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)\n\n[![Read the documentation at https://gdptools-pygeoapi-plugin.readthedocs.io/](https://img.shields.io/readthedocs/gdptools-pygeoapi-plugin/latest.svg?label=Read%20the%20Docs)](https://gdptools-pygeoapi-plugin.readthedocs.io/)\n[![Tests](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools-pygeoapi-plugin/workflows/Tests/badge.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools-pygeoapi-plugin/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/wma/nhgf/toolsteam/gdptools-pygeoapi-plugin/branch/main/graph/badge.svg)](https://codecov.io/gh/wma/nhgf/toolsteam/gdptools-pygeoapi-plugin)\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://code.usgs.gov/pre-commit/pre-commit)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://code.usgs.gov/psf/black)\n[![Poetry](https://img.shields.io/badge/poetry-enabled-blue)](https://python-poetry.org/)\n[![Conda](https://img.shields.io/badge/conda-enabled-green)](https://anaconda.org/)\n\n# Features\n\n- TODO\n\n# Requirements\n\n- TODO\n\n# Installation\n\nYou can install _Gdptools Pygeoapi Plugin_ via [pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):\n\n        pip install gdptools-pygeoapi-plugin\n\n# Usage\n\nPlease see the [Command-line Reference](Usage_) for details.\n\n# Contributing\n\nContributions are very welcome. To learn more, see the Contributor Guide\\_.\n\n# License\n\nDistributed under the terms of the [CC0 1.0 Universal license](https://creativecommons.org/publicdomain/zero/1.0/legalcode), _Gdptools Pygeoapi Plugin_ is free and open source software.\n\n# Issues\n\nIf you encounter any problems, please [file an issue](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools-pygeoapi-plugin/issues) along with a detailed description.\n\n# Credits\n\nThis project was generated from [@chill](https://code.usgs.gov/chill)'s [Pygeoapi Plugin Cookiecutter](https://code.usgs.gov/wma/nhgf/pygeoapi-plugin-cookiecutter) template.\n",
    'author': 'Richard McDonald',
    'author_email': 'rmcd@usgs.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://code.usgs.gov/wma/nhgf/toolsteam/gdptools-pygeoapi-plugin',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
