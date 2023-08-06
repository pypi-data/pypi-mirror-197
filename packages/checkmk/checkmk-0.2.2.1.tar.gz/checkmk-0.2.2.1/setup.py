# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['checkmk']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['cmk = checkmk.cli:main', 'omd = checkmk.cli:main']}

setup_kwargs = {
    'name': 'checkmk',
    'version': '0.2.2.1',
    'description': 'Checkmk placeholder',
    'long_description': '# Checkmk placeholder\n',
    'author': 'Frans Fürst',
    'author_email': 'frans.fuerst+gitlab@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://projects.om-office.de/frans/checkmk-pip.git',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
