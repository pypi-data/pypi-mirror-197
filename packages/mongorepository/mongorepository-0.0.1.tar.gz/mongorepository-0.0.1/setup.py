# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongorepository',
 'mongorepository.models',
 'mongorepository.repositories',
 'mongorepository.repositories.mongo_async',
 'mongorepository.repositories.sync']

package_data = \
{'': ['*']}

install_requires = \
['async-cache>=1.1.1,<2.0.0', 'motor>=3.1.1,<4.0.0', 'pydantic>=1.10.6,<2.0.0']

setup_kwargs = {
    'name': 'mongorepository',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Ramon Rodrigues',
    'author_email': 'ramon.srodrigues01@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
