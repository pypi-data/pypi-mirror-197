# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qq_chat_history']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'pyyaml>=6.0,<7.0', 'ujson>=5.7.0,<6.0.0']

entry_points = \
{'console_scripts': ['qq-chat-history = qq_chat_history.cli:run']}

setup_kwargs = {
    'name': 'qq-chat-history',
    'version': '0.2.4',
    'description': 'A tool to extract QQ chat history.',
    'long_description': "# QQ 聊天记录提取器\n\n## 简介\n\n从 QQ 聊天记录文件中提取聊天信息，仅支持 `txt` 格式的聊天记录。\n\n\n## 安装\n\n使用 `pip` 安装，要求 `Python 3.9` 或以上版本。\n\n```bash\n> pip install -U qq-chat-history\n```\n\n## 使用\n\n你可以直接在终端中使用，如下（如果安装到虚拟环境请确保已激活）：\n\n```bash\n> qq-chat-history --help\n```\n\n按照提示传入指定参数，你也可以不带参数直接启动，然后按照提示输入参数。\n\n或者，你可以在代码中使用，如下：\n\n```python\nimport qq_chat_history\n\nlines = '''\n=========\n假装我是 QQ 自动生成的文件头\n=========\n\n1883-03-07 11:22:33 A<someone@example.com>\n关注永雏塔菲喵\n关注永雏塔菲谢谢喵\n\n1883-03-07 12:34:56 B(123123)\nTCG\n\n1883-03-07 13:24:36 C(456456)\nTCG\n\n1883-03-07 22:00:51 A<someone@example.com>\n塔菲怎么你了\n'''.strip().splitlines()\n\nfor msg in qq_chat_history.parse(lines):\n    print(msg.date, msg.id, msg.name, msg.content)\n```\n\n注意 `parse` 方法返回的是一个生成器。\n\n\n## 更新\n\n\n经过不懈努力，本项目在 `0.2` 版本中终于把冗长的类给干掉了，再也不用写 `Parser.get_instance('xxx').parse(lines)` 了，直接调用 `parse` 方法即可。\n\n\n但是，由于 `parse` 这个名字的含义比较不清晰，所以使用方式如下：\n\n\n```python\n# Not recommended 👎\nfrom qq_chat_history import parse\nparse(...)\n\n\n# Recommended 👍\nimport qq_chat_history\nqq_chat_history.parse(...)\n\n\nfrom qq_chat_history import parse as parse_qq\nparse_qq(...)\n```\n\n我个人认为使用 `import` 更符合直觉。\n",
    'author': 'kifuan',
    'author_email': 'kifuan@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kifuan/qq-chat-history',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
