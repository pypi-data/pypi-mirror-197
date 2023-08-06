# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycngal']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.20.1,<0.21.0', 'networkx>=3.0,<4.0']

setup_kwargs = {
    'name': 'python-cngal',
    'version': '0.1.0',
    'description': 'A Python wrapper for cngal.org API',
    'long_description': '# python-cngal\nA Python wrapper for cngal.org API\n\n## 数据来源\n\n1. [数据汇总页面](https://app.cngal.org/data)\n2. [Swagger UI](https://api.cngal.org/swagger/index.html)\n3. [GitHub 文档](https://github.com/CnGal/CnGalWebSite/blob/master/Docs/AboutCode/APIInstructions/Summary.md)',
    'author': '快乐的老鼠宝宝',
    'author_email': 'keaitianxinmail@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
