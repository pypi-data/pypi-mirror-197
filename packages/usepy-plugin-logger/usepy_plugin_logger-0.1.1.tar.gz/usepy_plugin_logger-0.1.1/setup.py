# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['usepy_logger']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'usepy[logger]>=0.1.41,<0.2.0']

setup_kwargs = {
    'name': 'usepy-plugin-logger',
    'version': '0.1.1',
    'description': '一个全局拦截日志并转为loguru日志的插件',
    'long_description': '### 一个全局拦截日志并转为loguru日志的插件\n\n<a href="https://pypi.org/project/usepy-plugin-logger" target="_blank">\n    <img src="https://img.shields.io/pypi/v/usepy-plugin-logger.svg" alt="Package version">\n</a>\n\n<a href="https://pypi.org/project/usepy-plugin-logger" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/usepy-plugin-logger.svg" alt="Supported Python versions">\n</a>\n\n#### 文档\n\n[useLogger | UsePy](https://usepy.code05.com/api/logger.html) \n\n#### 安装\n\n> pip install usepy-plugin-logger\n\n#### 使用\n\n```python\nfrom usepy.logger import useLogger\n\nuseLogger() # 使用默认配置\n\n```\n\n如果你自身项目正在使用`loguru`，这一切似乎感觉毫无变化。因为默认的配置只是修改了一点输出样式。\n\n如果想要感受它带来的“魔法”，需要稍微配置一下。\n\n```python\nfrom usepy.logger import useLogger\nuseLogger(packages=["scrapy",  "django",  "usepy"]) \n\n```\n\n##### Logstash/Filebeat\n\n日志的更重要能力是将日志记录发送到`Logstash`/`Filebeat`，这样就可以将日志记录存储到`Elasticsearch`中，方便进行日志分析。所以统一日志的最终输出格式是非常重要的。\n\n`useLogger`内置一个`logstash_handler`统一化输出格式。\n\n```python\nfrom usepy import useTimeIt\nfrom usepy.logger import useLogger, logstash_handler\nuseLogger(\n handlers=[\n logstash_handler(level="DEBUG",  extra={"app_name":  "spider"})\n ],\n packages=["usepy"],  # hook拦截 usepy 的日志\n extra={"project_name":  "usepy"}\n)\nlogger.warning("test warning")\nlogger.info("test info")\nlogger.debug("test debug")\n\n```\n\n\n',
    'author': 'nowanti',
    'author_email': 'believel.y@qq.com',
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
