# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zernpol']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.2,<2.0']

setup_kwargs = {
    'name': 'zernpol',
    'version': '0.1.5',
    'description': 'Tools to handle Zernike polynoms and Indexing systems',
    'long_description': '\nThis simple package offers tools to handle Zernike Polynoms and the different indexing systems (as the\nNoll system for instance).\n\nThe package offers object and non-object oriented functions. \n\n\n\n\nInstall\n-------\n\nFrom pip:\n    \n    > pip install zernpol \n    \nFrom sources:\n    \n    > git clone https://gricad-gitlab.univ-grenoble-alpes.fr/guieus/zernpol.git\n    > cd zernpol \n    > python setup.py install \n\n\nDocumentation \n-------------\n\nPlease visits: https://zernpol.readthedocs.io/en/latest/#\n\n\n\n',
    'author': 'Sylvain Guieu',
    'author_email': 'sylvain.guieu@univ-grenoble-alpes.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
