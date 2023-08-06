# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bioto_client',
 'bioto_client.domain',
 'bioto_client.infrastructure',
 'bioto_client.infrastructure.auth',
 'bioto_client.infrastructure.repository',
 'bioto_client.infrastructure.users']

package_data = \
{'': ['*']}

install_requires = \
['auth0-python>=4.0.0,<5.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'requests>=2.28.2,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['bioto-client = bioto_client.cli:app']}

setup_kwargs = {
    'name': 'bioto-client',
    'version': '0.1.7',
    'description': 'A python CLI client for accessing Bioto data',
    'long_description': "# PyClient\n\nPython Client for retrieving Bioto sensor data\n\n## Goals\n\n### Session management\n\n- [x] create session via device login to get a valid access token\n\n### Retrieving sensor data\n\n- [x] find a garden\n- [x] subscribe to that garden\n- [x] see subscribtion state for that garden (pending/approved/declined)\n- [x] get an overview of your gardens\n- [x] retrieve sensor data from garden devices\n\n## Getting started\n\nThere are two ways of installing this client. The first one using pip:\n\n```bash\n% pip install --user bioto-client\n```\n\nThe second option is useful when developing the client. Git clone the project\nand use `make` for installation. This will setup a\n[virtual python environment][3] managed via [`poetry`][4].\n\n```bash\n% make install\n% poetry shell\n```\n\n## How to use\n\n> **Tip** Use `bioto-client --help` to see other available commands\n\n### Start a user session\n\nA user session is valid for 24h. When expired you're requested to create a new\nsession. This can be done as follows:\n\n```bash\n\n# Call the client with the `user` command to assert a valid session\n% bioto-client user\n\nLoading session\n\nNot logged in, please take the following steps:\n\n1. On your computer or mobile device navigate to: https://biotoco.eu.auth0.com/activate?user_code=NEWT-OKEN\n2. Enter the following code:  NEWT-OKEN\n\nSuccesfully logged in.\n\nBioto CLI client: 1.2.3\nEnvironment: prod\nSession token ***5OFd09w\n```\n\n### Find a garden\n\nGardens can be found by name, the command to do this is:\n\n```bash\n% bioto-client search-garden {name}\n```\n\n### Subscribe to a garden\n\nTo gain access to the data of this garden you need to subscribe to this garden\nusing its `ID`:\n\n```bash\n% bioto-client subscribe-garden {garden_id}\n```\n\nThis will create a subscription request which only the mainter(s) can approve.\nTo check the state of your subscription see:\n\n```bash\n% bioto-client subscriptions\n```\n\n### Read device data\n\nReading a device is done by `device ID`, these can be found via the garden\ncommand. Note that a garden might contain multiple devices.\n\nTo get the latest hourly readings for the last 24h issue the following command:\n\n```bash\n% bioto-client device {device_id}\n```\n\nTo get these readings for a sepecific date apply a date option. The following\nformats are allowed: [%Y-%m-%d | %Y-%m-%dT%H:%M:%S | %H:%M:%S]:\n\n```bash\n% bioto-client device {device_id} --date={date}\n```\n\nAnd to limit or increase the number of hours returned add the hours option:\n\n```bash\n% bioto-client device {device_id} --hours={hours_limit}\n```\n\n## Improve the client\n\nIf you want to improve the client or add something which you think is missing to\nthe project you can either [open an issue][1] or develop the feature yourself\nand open [a pull request with your changes][2].\n\nTo get started clone this project and create a branch. Now fix the bug or create\nthe feature you want and write some tests for it to prove it works. This can be\ndone by executing:\n\n```bash\n% make check\n```\n\n> **Note** This will run both tests and linters, use `make test` when you're in\n`red - green - refactor` mode\n\nWhen the checks are all passing, please open a [PR][2]\n\n[1]: https://github.com/wearebioto/PyClient/issues\n[2]: https://github.com/wearebioto/PyClient/pulls\n[3]: https://docs.python.org/3/library/venv.html\n[4]: https://python-poetry.org/docs/\n",
    'author': 'Bioto',
    'author_email': 'it@bioto.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
