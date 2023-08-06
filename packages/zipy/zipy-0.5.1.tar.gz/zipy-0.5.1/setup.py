# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zipy', 'zipy.cmdline']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pydantic>=1.10.5,<2.0.0', 'web3>=5.31.3,<6.0.0']

setup_kwargs = {
    'name': 'zipy',
    'version': '0.5.1',
    'description': 'Zipy is a toolbox containing a set of convenient python function',
    'long_description': '# Introduction\nzipy is a toolbox for usual python development\n\n# Development\n# Prerequisite\n- install poetry\n\n## Build dev environment\n```\ncd <path-to-project>\n\npoetry install\n\npoetry env use 3.10\n\npre-commit install\n```\n',
    'author': '冒险岛真好玩',
    'author_email': '17826800084g@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4',
}


setup(**setup_kwargs)
