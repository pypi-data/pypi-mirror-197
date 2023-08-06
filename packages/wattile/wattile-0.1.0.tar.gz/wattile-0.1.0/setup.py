# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wattile', 'wattile.models']

package_data = \
{'': ['*'], 'wattile': ['configs/*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'kaleido==0.2.1',
 'matplotlib>=3.0,<4.0',
 'nbmake>=1.3.2,<2.0.0',
 'numpy>=1.22,<2.0',
 'pandas>=1.4.0,<2.0.0',
 'plotly>=5.8.2,<6.0.0',
 'psutil>=5.8.0,<6.0.0',
 'requests>=2.21.0,<3.0.0',
 'scipy>=1.9,<2.0',
 'seaborn>=0.11.2,<0.12.0',
 'setuptools>=65.5.0,<66.0.0',
 'tables>=3.7.0,<4.0.0',
 'tensorboard>=2.8.0,<3.0.0',
 'tensorboardX==1.4',
 'torch>=1.9.0,<2.0.0',
 'xarray>=2022.10.0,<2023.0.0']

setup_kwargs = {
    'name': 'wattile',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
