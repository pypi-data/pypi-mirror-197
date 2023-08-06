# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo',
 'mojo.xmods',
 'mojo.xmods.xcollections',
 'mojo.xmods.xeventing',
 'mojo.xmods.xlogging',
 'mojo.xmods.xnetworking',
 'mojo.xmods.xthreading']

package_data = \
{'': ['*']}

install_requires = \
['debugpy>=1.6.6,<2.0.0',
 'mojo-waiting>=1.0.0,<2.0.0',
 'netifaces>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'mojo-xmodules',
    'version': '0.0.5',
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
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
