# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cg', 'cg.rootutils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cg-rootutils',
    'version': '0.0.1',
    'description': 'A Suite of Utilities for ROOT',
    'long_description': '# ROOTUtils - A Suite of Utilities for ROOT\n\n<!-- ToDo -->\n',
    'author': 'ChunkyGrumbler',
    'author_email': 'ChunkyGrumbler@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ChunkyGrumbler/ROOTUtils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
