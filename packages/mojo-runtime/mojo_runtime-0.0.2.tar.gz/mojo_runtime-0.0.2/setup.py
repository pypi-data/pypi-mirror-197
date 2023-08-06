# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['packages', 'packages.mojo.runtime', 'packages.mojo.runtime.activation']

package_data = \
{'': ['*']}

install_requires = \
['coverage>=7.0.4,<8.0.0', 'mojo-xmodules>=0.0.5,<0.0.6']

setup_kwargs = {
    'name': 'mojo-runtime',
    'version': '0.0.2',
    'description': 'Automation Mojo Runtime Module (mojo-runtime)',
    'long_description': '# Contextualize\nA package used to create a global context that allows for the distribution of options and configuration.\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
