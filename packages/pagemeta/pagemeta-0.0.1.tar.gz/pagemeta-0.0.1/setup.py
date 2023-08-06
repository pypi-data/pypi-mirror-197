# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pagemeta']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'httpx>=0.23.3,<0.24.0',
 'python-dotenv>=0.21,<0.22']

setup_kwargs = {
    'name': 'pagemeta',
    'version': '0.0.1',
    'description': 'Extract Open Graph metadata from a URL via BeautifulSoup.',
    'long_description': '# pagemeta\n\n![Github CI](https://github.com/justmars/pagemeta/actions/workflows/main.yml/badge.svg)\n\n## Development\n\nSee [documentation](https://justmars.github.io/pagemeta).\n\n1. Run `poetry shell`\n2. Run `poetry update`\n3. Run `pytest`\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://mv3.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
