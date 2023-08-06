# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['puty']
setup_kwargs = {
    'name': 'puty',
    'version': '0.0.2',
    'description': 'data purifier with schema',
    'long_description': '[![version badge](https://badge.fury.io/py/puty.svg)](https://badge.fury.io/py/puty)\n\n**puty** is data purifier with schema\n\n## Warning\n\nThis repository is on developing. Some bugs may exist, possible to change suddenly. And no document yet.\n\n\n## Installation\n\n    pip install puty\n',
    'author': 'jrog612',
    'author_email': 'jrog612@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jrog612/puty',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
