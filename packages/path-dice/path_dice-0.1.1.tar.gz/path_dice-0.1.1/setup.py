# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['path_dice']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'path-dice',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'Hyeonjin Kim',
    'author_email': 'ilhj1228@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
