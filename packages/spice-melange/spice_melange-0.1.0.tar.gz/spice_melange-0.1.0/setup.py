# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spice_melange']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'spiceypy>=4.0.3,<5.0.0']

setup_kwargs = {
    'name': 'spice-melange',
    'version': '0.1.0',
    'description': 'A utility library for SPICE.',
    'long_description': '# Melange - a utility library for SPICE',
    'author': 'Gavin Medley',
    'author_email': 'gavin.medley@lasp.colorado.edu',
    'maintainer': 'Gavin Medley',
    'maintainer_email': 'gavin.medley@lasp.colorado.edu',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
