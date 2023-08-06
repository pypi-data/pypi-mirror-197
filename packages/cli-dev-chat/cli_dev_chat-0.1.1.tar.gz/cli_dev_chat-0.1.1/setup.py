# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['chatgpt']

package_data = \
{'': ['*']}

install_requires = \
['openai']

entry_points = \
{'console_scripts': ['chatgpt = chatgpt.__main__:main']}

setup_kwargs = {
    'name': 'cli-dev-chat',
    'version': '0.1.1',
    'description': 'A command-line interface for interacting with OpenAI chat language models',
    'long_description': 'None',
    'author': 'Jeremy Baron',
    'author_email': 'jbaron34@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
