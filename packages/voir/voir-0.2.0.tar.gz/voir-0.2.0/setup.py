# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['voir', 'voir.instruments']

package_data = \
{'': ['*']}

install_requires = \
['omegaconf>=2.3.0,<3.0.0', 'ovld>=0.3.2,<0.4.0', 'ptera>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['voir = voir.cli:main']}

setup_kwargs = {
    'name': 'voir',
    'version': '0.2.0',
    'description': 'Instrument, extend and visualize your programs',
    'long_description': 'None',
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
