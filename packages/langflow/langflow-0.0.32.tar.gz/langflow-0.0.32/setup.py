# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'langflow/backend'}

packages = \
['langflow_backend',
 'langflow_backend.api',
 'langflow_backend.custom',
 'langflow_backend.interface',
 'langflow_backend.utils']

package_data = \
{'': ['*'],
 'langflow_backend': ['frontend/*',
                      'frontend/static/css/*',
                      'frontend/static/js/*']}

install_requires = \
['beautifulsoup4>=4.11.2,<5.0.0',
 'fastapi>=0.91.0,<0.92.0',
 'google-api-python-client>=2.79.0,<3.0.0',
 'google-search-results>=2.4.1,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'langchain_ibis==0.0.100',
 'openai>=0.26.5,<0.27.0',
 'typer>=0.7.0,<0.8.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['langflow = langflow_backend.__main__:main']}

setup_kwargs = {
    'name': 'langflow',
    'version': '0.0.32',
    'description': 'A Python package with a built-in web application',
    'long_description': '<!-- Title -->\n\n# ⛓️ LangFlow\n\n~ A User Interface For [LangChain](https://github.com/hwchase17/langchain) ~\n\n<p>\n<img alt="GitHub Contributors" src="https://img.shields.io/github/contributors/logspace-ai/langflow" />\n<img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/logspace-ai/langflow" />\n<img alt="" src="https://img.shields.io/github/repo-size/logspace-ai/langflow" />\n<img alt="GitHub Issues" src="https://img.shields.io/github/issues/logspace-ai/langflow" />\n<img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/logspace-ai/langflow" />\n<img alt="Github License" src="https://img.shields.io/github/license/logspace-ai/langflow" />  \n</p>\n\n<a href="https://github.com/logspace-ai/langflow">\n    <img width="100%" src="https://github.com/logspace-ai/langflow/blob/main/img/langflow-demo.gif?raw=true"></a>\n\nLangFlow is a GUI for [LangChain](https://github.com/hwchase17/langchain), designed with [react-flow](https://github.com/wbkd/react-flow) to provide an effortless way to experiment and prototype flows with drag-and-drop components and a chat box.\n\n## 📦 Installation\n\nYou can install LangFlow from pip:\n\n`pip install langflow`\n\nNext, run:\n\n`python -m langflow` or just `langflow`\n\n## 🎨 Creating Flows\n\nCreating flows with LangFlow is easy. Simply drag sidebar components onto the canvas and connect them together to create your pipeline. LangFlow provides a range of [LangChain components](https://langchain.readthedocs.io/en/latest/reference.html) to choose from, including LLMs, prompt serializers, agents, and chains.\n\nExplore by editing prompt parameters, link chains and agents, track an agent\'s thought process, and export your flow.\n\n\n## 👋 Contributing\n\nWe welcome contributions from developers of all levels to our open-source project on GitHub. If you\'d like to contribute, please check our contributing guidelines and help make LangFlow more accessible.\n\n## 📄 License\n\nLangFlow is released under the MIT License. See the LICENSE file for details.\n',
    'author': 'Logspace',
    'author_email': 'contact@logspace.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
