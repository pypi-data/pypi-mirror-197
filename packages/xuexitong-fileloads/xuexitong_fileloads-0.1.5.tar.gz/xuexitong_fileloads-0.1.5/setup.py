# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xuexitong_fileloads']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xuexitong-fileloads',
    'version': '0.1.5',
    'description': '用来下载学习通课件资料',
    'long_description': '# chaoxingxuexitong-fileloads\n 下载学习通课件视频\n',
    'author': 'ziru-w',
    'author_email': '77319678+ziru-w@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
