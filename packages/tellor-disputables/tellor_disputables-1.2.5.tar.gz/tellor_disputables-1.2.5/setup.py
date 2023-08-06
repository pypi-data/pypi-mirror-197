# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tellor_disputables']

package_data = \
{'': ['*']}

install_requires = \
['asynctest>=0.13.0,<0.14.0',
 'click>=8.1.3,<9.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'pytest-asyncio>=0.19.0,<0.20.0',
 'tabulate>=0.8.9,<0.9.0',
 'telliot-feeds>=0.1.6,<0.2.0',
 'twilio>=7.7.0,<8.0.0',
 'web3>=5.27.0,<6.0.0']

entry_points = \
{'console_scripts': ['cli = tellor_disputables.cli:main',
                     'data = tellor_disputables.data:main']}

setup_kwargs = {
    'name': 'tellor-disputables',
    'version': '1.2.5',
    'description': 'dashboard & text alerts for disputable values reported to Tellor oracles',
    'long_description': 'None',
    'author': 'tallywiesenberg',
    'author_email': 'info@tellor.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
