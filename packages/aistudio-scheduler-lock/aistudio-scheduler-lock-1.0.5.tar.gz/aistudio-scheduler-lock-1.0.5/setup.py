# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aistudio_scheduler_lock',
 'aistudio_scheduler_lock.locks',
 'aistudio_scheduler_lock.migrations',
 'aistudio_scheduler_lock.schedules']

package_data = \
{'': ['*']}

install_requires = \
['Django==3.2.6', 'django-apscheduler==0.6.2']

setup_kwargs = {
    'name': 'aistudio-scheduler-lock',
    'version': '1.0.5',
    'description': 'Implements a distributed locking scheme for schedulers running on HA mode.',
    'long_description': 'None',
    'author': 'Yogesh Ketkar',
    'author_email': 'yogesh.ketkar@automationedge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
