# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['start_sdk']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.84,<2.0.0',
 'httpx>=0.23.3,<0.24.0',
 'loguru>=0.6.0,<0.7.0',
 'pydantic>=1.10.5,<2.0.0',
 'python-dotenv>=0.21,<0.22']

setup_kwargs = {
    'name': 'start-sdk',
    'version': '0.0.10',
    'description': 'Settings for Github, Cloudflare Images API',
    'long_description': '# start_sdk\n\n![Github CI](https://github.com/justmars/start-sdk/actions/workflows/main.yml/badge.svg)\n\nSettings for Github, Cloudflare Images API\n\n## Development\n\nSee [documentation](https://justmars.github.io/start-sdk).\n\n1. Run `poetry shell`\n2. Run `poetry update`\n3. Run `pytest`\n',
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
