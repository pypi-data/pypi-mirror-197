# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['langchain_contrib',
 'langchain_contrib.tools',
 'langchain_contrib.tools.terminal',
 'langchain_contrib.tools.terminal.patchers',
 'langchain_contrib.utils',
 'langchain_contrib.utils.tests']

package_data = \
{'': ['*']}

install_requires = \
['langchain>=0.0.112,<0.0.113', 'pexpect>=4.8.0,<5.0.0']

setup_kwargs = {
    'name': 'langchain-contrib',
    'version': '0.0.1',
    'description': '',
    'long_description': '# langchain-contrib\n\nA collection of utilities that are too experimental for [langchain proper](https://github.com/hwchase17/langchain), but are nonetheless generic enough to potentially be useful for multiple projects. Currently consists of code dumped from [ZAMM](https://github.com/amosjyng/zamm), but is of course open to contributions with lax procedures.\n\n## Quickstart\n\n```bash\npip install langchain-contrib\n```\n\nTo add interop with [`vcr-langchain`](https://github.com/amosjyng/vcr-langchain), simply install it as well:\n\n```bash\npip install vcr-langchain\n```\n',
    'author': 'Amos Jun-yeung Ng',
    'author_email': 'me@amos.ng',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
