# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scandal']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scandal',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Crowbar\n',
    'author': 'Nicholas Gates',
    'author_email': 'nick@nickgates.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
