# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reels_downloader',
 'reels_downloader.common',
 'reels_downloader.common.model',
 'reels_downloader.main']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp==3.8.3',
 'aiosignal==1.3.1',
 'async-timeout==4.0.2',
 'attrs==22.2.0',
 'beautifulsoup4==4.11.2',
 'charset-normalizer==2.1.1',
 'frozenlist==1.3.3',
 'idna==3.4',
 'multidict==6.0.4',
 'soupsieve==2.3.2.post1',
 'yarl==1.8.2']

setup_kwargs = {
    'name': 'downloader-for-reels',
    'version': '0.1.7',
    'description': 'Reels Download Module',
    'long_description': 'Reels Downloader - модуль что поможет получить прямую ссылку на reels в разных разрешениях',
    'author': 'Николай Витальевич Никоноров',
    'author_email': 'nnv@bitt.moe',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/bitt_moe/instagram/reels_downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
