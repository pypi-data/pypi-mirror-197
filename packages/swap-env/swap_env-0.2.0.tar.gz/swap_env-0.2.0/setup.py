# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['swap_env']

package_data = \
{'': ['*']}

install_requires = \
['inquirerpy>=0.3.4,<0.4.0']

entry_points = \
{'console_scripts': ['swap-env = swap_env.cli:app']}

setup_kwargs = {
    'name': 'swap-env',
    'version': '0.2.0',
    'description': 'A simple CLI for swapping between .env files',
    'long_description': "# Swap Env\n\n`swap-env` is a simple CLI for swapping between different `.env` files.\n\n![demo](https://user-images.githubusercontent.com/71074961/224817847-828bace2-5ab1-47d9-8ad2-e6a3e47d57f8.gif)\n\n## Requirements\n\n`python >= 3.10`\n\n## Installation\n\n- with [`pipx`](https://pypa.github.io/pipx/) (recommended):\n\n```bash\n$ pipx install swap-env\n```\n\n- with `pip`:\n\n```bash\n$ pip install swap-env\n```\n\n## Usage\n\nSave any `.env` files you regularly use to `~/.swap-env/`. Name them `.env.<name>` and you'll access them via `<name>` in `swap-env`.\n\n```bash\n$ ls -A1 ~/.swap-env\n.env.dev\n.env.test\n```\n\nThen simply run `swap-env` and select the file you want to use. A symlink will be created at `./.env` to that file.\n\n```bash\n$ swap-env\n? Select a .env file:\n❯ dev\n  test\n  \n? Select a .env file: dev\n\n$ ls -l .env\n... .env@ -> ~/.swap-env/.env.dev\n```\n\nIf you have a local `.env` file (not a symlink), you will be prompted whether to save it first.\n",
    'author': 'Ben Berry-Allwood',
    'author_email': 'benberryallwood@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/benberryallwood/swap-env',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
