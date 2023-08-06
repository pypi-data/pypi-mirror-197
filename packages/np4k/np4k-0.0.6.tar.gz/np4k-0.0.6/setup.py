# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['np4k', 'np4k.videos']

package_data = \
{'': ['*'], 'np4k': ['resources/misc/*', 'resources/text/*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'cssselect>=1.2.0,<2.0.0',
 'feedfinder2>=0.0.4,<0.0.5',
 'feedparser>=6.0.10,<7.0.0',
 'jieba3k>=0.35.1,<0.36.0',
 'lxml>=4.9.2,<5.0.0',
 'nltk>=3.8.1,<4.0.0',
 'pillow>=9.4.0,<10.0.0',
 'pythainlp>=3.1.1,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.2,<3.0.0',
 'tinysegmenter>=0.4,<0.5',
 'tldextract>=3.4.0,<4.0.0']

setup_kwargs = {
    'name': 'np4k',
    'version': '0.0.6',
    'description': '',
    'long_description': '\n\nnp4k',
    'author': 'Airvue',
    'author_email': 'dev@airvue.news',
    'maintainer': 'Airvue',
    'maintainer_email': 'dev@airvue.news',
    'url': 'https://github.com/airvuetech/newspaper4k/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

