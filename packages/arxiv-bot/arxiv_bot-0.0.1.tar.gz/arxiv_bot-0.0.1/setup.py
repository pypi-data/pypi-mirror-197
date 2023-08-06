# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arxiv_bot', 'arxiv_bot.knowledge_base', 'knowledge_base']

package_data = \
{'': ['*']}

install_requires = \
['arxiv>=1.4.3,<2.0.0',
 'langchain>=0.0.96,<0.0.97',
 'openai>=0.26.5,<0.27.0',
 'pinecone-client>=2.2.1,<3.0',
 'pypdf2>=3.0.1,<4.0.0',
 'tiktoken>=0.2.0,<0.3.0',
 'tqdm>=4.64.1,<5.0.0',
 'transformers>=4.26.1,<5.0.0']

setup_kwargs = {
    'name': 'arxiv-bot',
    'version': '0.0.1',
    'description': 'ArXiv component of AI assistant',
    'long_description': '# Arxiv Bot\n',
    'author': 'James Briggs',
    'author_email': 'james@aurelio.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
