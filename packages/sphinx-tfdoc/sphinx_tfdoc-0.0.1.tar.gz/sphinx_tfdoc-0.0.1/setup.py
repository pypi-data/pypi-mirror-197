# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinx_tfdoc']

package_data = \
{'': ['*'], 'sphinx_tfdoc': ['templates/*']}

install_requires = \
['Jinja2', 'sphinx>=6', 'tabulate']

setup_kwargs = {
    'name': 'sphinx-tfdoc',
    'version': '0.0.1',
    'description': '',
    'long_description': 'None',
    'author': 'Tommy Wang',
    'author_email': 'twang@august8.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
