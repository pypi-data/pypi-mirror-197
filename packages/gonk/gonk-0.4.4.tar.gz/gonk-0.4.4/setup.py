# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gonk',
 'gonk.contrib',
 'gonk.contrib.expiration',
 'gonk.contrib.notifications',
 'gonk.contrib.persistance',
 'gonk.contrib.rest_framework',
 'gonk.management',
 'gonk.management.commands',
 'gonk.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0.0,<4.0.0',
 'celery>=5.0.0,<6.0.0',
 'flake8>=6.0.0,<7.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

extras_require = \
{'drf': ['djangorestframework>=3.0.0,<4.0.0'],
 'mercure': ['PyJWT>=1.5.0,<2.0.0', 'requests>=2.0.0,<3.0.0'],
 'persistance': ['django-celery-beat>=2.3.0,<3.0.0']}

setup_kwargs = {
    'name': 'gonk',
    'version': '0.4.4',
    'description': '',
    'long_description': None,
    'author': 'Francisco Javier Lendinez Tirado',
    'author_email': 'lendinez@kasfactory.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
