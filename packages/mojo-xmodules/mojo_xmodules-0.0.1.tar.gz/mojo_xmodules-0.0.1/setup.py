# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo', 'mojo.xmods', 'mojo.xmods.xthreading']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mojo-xmodules',
    'version': '0.0.1',
    'description': 'Automation Mojo X-Modules',
    'long_description': '# Automation Mojo X-Modules (mojo-xmodules)\nThis package contains helper modules that extend the function of standard python modules.\n\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
