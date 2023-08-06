# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xuexitong_fileloads']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xuexitong-fileloads',
    'version': '0.1.6',
    'description': '用来下载学习通课件资料',
    'long_description': '# chaoxingxuexitong-fileloads\n 下载学习通课件视频  \n觉得输入太多麻烦可以走极简通道，此时记得至少改个基本目录和链接，其他参数自定义，不改按默认参数。  \n使用方法代码里写了不少  \n只运行代码2即可，代码已作为模块导入  \n\n大致流程依次：\n\nmode_op 模式选择9自定义，中间值仅第一次循环极简,0极简.loop_op 按2自动循环1手动单次.file_class 输入循环下载类型3全部2pdf1mp4不下载0,start_inPage章节内页面\n\n跟着提示即可',
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
