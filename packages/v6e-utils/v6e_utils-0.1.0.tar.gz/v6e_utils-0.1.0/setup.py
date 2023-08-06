# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['v6e_utils',
 'v6e_utils.api_clients',
 'v6e_utils.data_helper',
 'v6e_utils.dataframe_helper',
 'v6e_utils.report_factory']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.0',
 'geopy>=2.2.0',
 'numpy>=1.20.0',
 'openpyxl>=3.0.9',
 'pandas>=1.2.0',
 'pysftp>=0.2.9',
 'requests>=2.26.0',
 'tqdm>=4.62.2']

setup_kwargs = {
    'name': 'v6e-utils',
    'version': '0.1.0',
    'description': 'A collection of utility functions for V6E projects',
    'long_description': 'None',
    'author': 'Luis Valverde',
    'author_email': 'lvalverde@istmocenter.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
