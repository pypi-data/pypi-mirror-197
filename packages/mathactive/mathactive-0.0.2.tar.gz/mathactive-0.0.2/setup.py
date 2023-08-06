# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mathactive',
 'mathactive.microlessons',
 'mathactive.webapp',
 'mathactive.webapp.migrations',
 'mathactive.website']

package_data = \
{'': ['*'], 'mathactive': ['data/*']}

install_requires = \
['django>=4.1,<5.0',
 'editdistance>=0.6,<0.7',
 'fastapi>=0.89.1,<0.90.0',
 'jupyter>=1.0,<2.0',
 'pandas>=1.5,<2.0',
 'python-statemachine[diagrams]>=1.0,<2.0',
 'scikit-learn>=1.2,<2.0',
 'scipy>=1.10.1,<2.0.0',
 'spacy>=3.4.0,<4.0']

setup_kwargs = {
    'name': 'mathactive',
    'version': '0.0.2',
    'description': 'Conversational math active learning.',
    'long_description': None,
    'author': 'hobs',
    'author_email': 'hobson@totalgood.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
