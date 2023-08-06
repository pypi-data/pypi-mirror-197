# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_bracket']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2[fastapi]>=2.0.0-rc.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-bracket',
    'version': '0.1.1',
    'description': 'Nonebot2 插件，用于补全左括号',
    'long_description': '# nonebot-plugin-bracket\n\n[Nonebot2](https://github.com/nonebot/nonebot2) 插件，用于补全消息中的括号，治愈强迫症\n\n\n## 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_bracket\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_bracket\n```\n\n\n## 使用\n\n发送包含括号的消息\n\n如：发送 `（`，机器人会回复 `）`\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
