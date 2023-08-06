# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tantaroba', 'tantaroba.scripts']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'numpy>=1.24.2,<2.0.0', 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'tantaroba',
    'version': '0.4.0',
    'description': 'Python package template',
    'long_description': '# tantaroba\n\nCollection of miscellanoeus utilities commonly used across different projects.\n\n## Installation\n```\npip install tantaroba\n```\n\n## Usage\nDescribe how to launch and use tantaroba project.\n',
    'author': 'Mattia Tantardini',
    'author_email': 'mattia.tantardini@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/tantardini/tantaroba',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
