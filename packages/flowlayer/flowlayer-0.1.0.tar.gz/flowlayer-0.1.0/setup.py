# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flowlayer', 'flowlayer.core']

package_data = \
{'': ['*']}

install_requires = \
['filelock>=3.0.12,<4.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'networkx>=2.5,<3.0',
 'numpy>=1.20.2,<2.0.0',
 'pydot>=1.4.2,<2.0.0',
 'semver>=2.13.0,<3.0.0']

setup_kwargs = {
    'name': 'flowlayer',
    'version': '0.1.0',
    'description': 'Easily build your data processing workflows.',
    'long_description': 'None',
    'author': 'sam',
    'author_email': 'contact@justsam.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
