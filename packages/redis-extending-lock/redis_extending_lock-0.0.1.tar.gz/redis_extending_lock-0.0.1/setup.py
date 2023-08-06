# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redis_extending_lock']

package_data = \
{'': ['*']}

install_requires = \
['aiomisc>=17.0.6,<18.0.0', 'redis>=4.5.1,<5.0.0']

setup_kwargs = {
    'name': 'redis-extending-lock',
    'version': '0.0.1',
    'description': 'Reacquiring lock for redis',
    'long_description': '# redis-reacquiring-lock',
    'author': 'Alexander Vasin',
    'author_email': 'hi@alvass.in',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
