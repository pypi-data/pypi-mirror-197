# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ballyregan',
 'ballyregan.core',
 'ballyregan.models',
 'ballyregan.providers',
 'cli',
 'cli.core']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=15.1.1,<16.0.0',
 'aiohttp-proxy>=0.1.2,<0.2.0',
 'aiohttp>=3.8.3,<4.0.0',
 'bs4>=0.0.1,<0.0.2',
 'click>=8.1.3,<9.0.0',
 'html5lib>=1.1,<2.0',
 'loguru>=0.6.0,<0.7.0',
 'lxml>=4.9.1,<5.0.0',
 'pandas>=1.5.0,<2.0.0',
 'prettytable>=3.4.1,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'typer[all]>=0.6.1,<0.7.0',
 'update>=0.0.1,<0.0.2']

entry_points = \
{'console_scripts': ['ballyregan = cli.app:run']}

setup_kwargs = {
    'name': 'ballyregan',
    'version': '1.0.3',
    'description': 'Find fetch & validate free proxies fast.',
    'long_description': '<h1>Ballyregan 🔷</h1>\n<p><em>Find fetch & validate free proxies fast.</em></p>\n\n<p>\n  <a href="https://pypi.org/project/ballyregan" target="_blank">\n      <img src="https://img.shields.io/pypi/v/ballyregan?label=pypi%20package" alt="Package version">\n  </a>\n  <a href="https://pypi.org/project/ballyregan" target="_blank">\n      <img src="https://img.shields.io/pypi/pyversions/ballyregan.svg?color=%2334D058" alt="Supported Python versions">\n  </a>\n  <a href="https://pypi.org/project/ballyregan" target="_blank">\n      <img src="https://img.shields.io/badge/license-Apache%202.0-yellow" alt="License: Apache 2.0">\n  </a>\n</p>\n\n---\n\n<br>\n\nBallyregan is a package & CLI that allows you to fetch free tested proxies really fast!\n\nKey features:\n  * **Fetch** free tested proxies super fast with [ProxyFetcher](https://github.com/idandaniel/ballyregan/blob/main/src/ballyregan/fetcher.py)\n  * **Validate** your own proxies with [ProxyValidator](https://github.com/idandaniel/ballyregan/blob/main/src/ballyregan/validator.py)\n  * **Filter** custom proxy list by protocol & anonymity with [ProxyFilterer](https://github.com/idandaniel/ballyregan/blob/main/src/ballyregan/filterer.py)\n\n<br>\n\n---\n\n## How does it work?\nWhen you use the ProxyFetcher to fetch a proxy, it performs several steps:\n1. Gather all the available proxies from a list of built in providers (each provider gathers it\'s own and returns it to the fetcher).\n\n  - > Provider - any website that serves free proxy lists (e.g https://free-proxy-list.net).\n\n2. Filter all the gathered proxies by the given protocols and anonymities (if exist).\n3. Validate the filtered proxies and return them.\n\n<br>\n\n> **Note** <br>\n> You can write and append your own custom providers and pass it to the ProxyFetcher class as attribute. <br>\n> Every custom proxy provider must implement the [IProxyProvider](https://github.com/idandaniel/ballyregan/blob/main/src/ballyregan/providers/interface.py) base interface.\n\n<br>\n\n## Behind the scenes\nFetching a proxy is an [IO bound operation](https://en.wikipedia.org/wiki/I/O_bound) which depends on network. A common approach for this problem is performing your network requests async. <br>\nAfter digging a bit, testing Threads, Greenlets and async operations, we decided to go the async way. <br>\nTo perform async http requests, ballyregan uses [aiohttp](https://docs.aiohttp.org/en/stable/) and [asyncio](https://docs.python.org/3/library/asyncio.html),\nas <em>"asyncio is often a perfect fit for IO-bound and high-level structured network code."</em> (from asyncio docs). <br>\nBy using the power of async http requests, ballyregan is able to validate thousands of proxies really fast. <br>\n\n---\n\n## Install\n\n```sh\npip install ballyregan\n```\n\n## Usage\n\n### Package 📦\n\n#### Create a fetcher instance\n```python\nfrom ballyregan import ProxyFetcher\n\n# Setting the debug mode to True, defaults to False\nfetcher = ProxyFetcher(debug=True)\n```\n\n#### Get one proxy\n```python\nproxy = fetcher.get_one()\nprint(proxy)\n```\n\n#### Get multiple proxies\n```python\nproxies = fetcher.get(limit=4)\nprint(proxies)\n```\n\n#### Get proxies by filters\n```python\nfrom ballyregan.models import Protocols, Anonymities\n\nproxies = fetcher.get(\n  limit=4,\n  protocols=[Protocols.HTTPS, Protocols.SOCKS5],\n  anonymities=[Anonymities.ELITE]\n)\nprint(proxies)\n```\n\n### CLI 💻\n\n#### Get all proxies\n```sh\nballyregan get --all\n```\n\n#### Get one proxy\n```sh\nballyregan get\n```\n\n#### Use debug mode\n```sh\nballyregan --debug get [OPTIONS]\n```\n\n#### Format output to json\n```sh\nballyregan get -o json\n```\n\n#### Get proxies by limit\n```sh\nballyregan get -l 4\n```\n\n#### Get proxies by filters\n```sh\nballyregan get -l 4 -p https -p socks5 -a elite\n```\n\n---\n\n## Author\n\n👤 **Idan Daniel**\n\n* Github: [@idandaniel](https://github.com/idandaniel)\n\n## Show your support\n\nGive a ⭐️ if this project helped you!\n\n## 📝 License\n\nCopyright © 2022 [Idan Daniel](https://github.com/idandaniel).<br />\nThis project is [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0) licensed.\n\n',
    'author': 'idandaniel',
    'author_email': 'idandaniel12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
