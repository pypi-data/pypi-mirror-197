# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['search',
 'search.internals',
 'search.schemas',
 'search.schemas.examples',
 'search.schemas.raws',
 'search.schemas.sources']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0',
 'orjson>=3.8.1,<4.0.0',
 'poetry==1.1.15',
 'pydantic>=1.10.4,<2.0.0',
 'ujson>=5.5.0,<6.0.0']

setup_kwargs = {
    'name': 'dep-search',
    'version': '2.3.0',
    'description': 'Search dep',
    'long_description': None,
    'author': 'everhide',
    'author_email': 'i.tolkachnikov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<=3.11',
}


setup(**setup_kwargs)
