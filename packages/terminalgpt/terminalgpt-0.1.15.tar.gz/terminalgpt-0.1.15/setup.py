# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['terminalgpt']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'colorama>=0.4.6,<0.5.0',
 'cryptography>=39.0.2,<40.0.0',
 'openai>=0.27.0,<0.28.0',
 'prompt-toolkit>=3.0.38,<4.0.0',
 'tiktoken>=0.2.0,<0.3.0',
 'yaspin>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['terminalgpt = terminalgpt.main:cli']}

setup_kwargs = {
    'name': 'terminalgpt',
    'version': '0.1.15',
    'description': 'AI chat asistent in your terminal powered by OpenAI GPT-3.5',
    'long_description': "# TerminalGPT\n\nWelcome to terminalGPT, the terminal-based ChatGPT personal assistant app!\nWith terminalGPT, you can easily interact with the OpenAI GPT 3.5 language model.\n\nWhether you need help with a quick question or want to explore a complex topic, TerminalGPT is here to assist you. Simply enter your query and TerminalGPT will provide you with the best answer possible based on its extensive knowledge base.\n\n![Alt Text](./usage.gif)\n\n## Why?\n\nSome advantages of using TerminalGPT over the chatGPT browser-based app:\n\n1. It doesn't disconnect like the browser-based app, so you can leave it running in a terminal session on the side without losing context.\n2. It's highly available and can be used whenever you need it.\n3. It's faster with replies than the browser-based app.\n4. You can use TerminalGPT with your IDE terminal, which means you won't have to constantly switch between your browser and your IDE when you have questions.\n5. TerminalGPT's answers are tailored to your machine's operating system, distribution, and chip set architecture.\n\n## Pre-requisites\n\n1. Python 3.6 or higher\n2. An OpenAI Account and API key (It's free for personal use).\n[How to create OpenAI API keys](https://elephas.app/blog/how-to-create-openai-api-keys-cl5c4f21d281431po7k8fgyol0)\n\n## Installation\n\n1. Install the latest TerminalGPT with pip install.\n\n```sh\npip install terminalgpt -U\n```\n\n2. Now you have `terminalgpt` command available in your terminal. Run the following command to configure the app.\n\n```sh\nterminalgpt install\n```\n\n3. Enter your OpenAI API key when prompted and press enter.\n\n\nThat's it! You're ready to use TerminalGPT!\n\n---\n\n## Usage\n\n1. Run the program with the following command:\n\n```sh\nterminalgpt chat\n```\n",
    'author': 'Adam Yodinsky',
    'author_email': '27074934+adamyodinsky@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
