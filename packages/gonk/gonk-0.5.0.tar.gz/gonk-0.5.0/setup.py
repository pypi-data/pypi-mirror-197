# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gonk',
 'gonk.contrib',
 'gonk.contrib.expiration',
 'gonk.contrib.notifications',
 'gonk.contrib.persistance',
 'gonk.contrib.rest_framework',
 'gonk.management',
 'gonk.management.commands',
 'gonk.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0.0,<4.0.0',
 'celery>=5.0.0,<6.0.0',
 'flake8>=6.0.0,<7.0.0',
 'python-dateutil>=2.8.2,<3.0.0']

extras_require = \
{'drf': ['djangorestframework>=3.0.0,<4.0.0'],
 'mercure': ['PyJWT>=1.5.0,<2.0.0', 'requests>=2.0.0,<3.0.0'],
 'persistance': ['django-celery-beat>=2.3.0,<3.0.0']}

setup_kwargs = {
    'name': 'gonk',
    'version': '0.5.0',
    'description': '',
    'long_description': '# Gonk\n\n![gonk](https://c.tenor.com/T0z4i7XQhUkAAAAd/gonk-gonk-droid.gif "Gonk")\n\n## Setup\n\n### Install the library:\n\n```bash\npip install gonk\n```\n\nYou can add contribution add-ons:\n\nFor Mercure support:\n\n```shell\npip install gonk[mercure]\n```\n\nFor Django Rest Framework support:\n\n```shell\npip install gonk[drf]\n```\n\nOr both of them:\n\n```shell\npip install gonk[drf,mercure]\n```\n\n### Add the application to `INSTALLED_APPS` in Django `settings`:\n\n```python\nINSTALLED_APPS = [\n    # ...\n    \'gonk\',\n]\n```\n\n### Launch migrations:\n\n```bash\npython manage.py migrate\n```\n\n## Usage\n\n### Create taskrunner\n\n```python\n# taskrunners.py\nfrom gonk.taskrunners import TaskRunner\nfrom gonk.decorators import register, register_beat\nfrom celery.schedules import crontab\n\n\n# Register taskrunner\n@register(\'my_taskrunner\')\nclass MyTaskRunner(TaskRunner):\n    def revert(self):\n        # Specific implementation\n    \n    def run(self):\n        # Specific implementation\n\n\n# Register scheduled taskrunner\n@register_beat(\'scheduled_taskrunner\', crontab(minute=\'*\'))\nclass ScheduledTaskRunner(TaskRunner):\n    def revert(self):\n        # Specific implementation\n    \n    def run(self):\n        # Specific implementation\n```\n\nWe have to import the taskrunner within every app.\nThe best way to do so is in `apps.py`\n\n```python\nclass MyAppConfig(AppConfig):\n    # ...\n\n    def ready(self):\n        from . import taskrunners\n```\n\n\n### Launch task\n\n```python\nfrom gonk.tasks import Task\n\nargs = {}\nTask.create_task(\'my_taskrunner\', args)\n```\n\n### Revert task\n\n```python\nfrom gonk.tasks import Task\n\nt = Task.objects.last()\nt.revert()\n```\n\n### Cancel task\n\n```python\nfrom gonk.tasks import Task\n\nt = Task.objects.last()\nterminate: bool = False\nt.cancel(terminate=terminate)\n```\n\n### Checkpoints\n\nYou can add checkpoints to register transcendent events within the task. Every checkpoint can send a notification\nto the user to get feedback of the status and progress of the task.\n\n```python\n# taskrunners.py\nfrom gonk.taskrunners import TaskRunner\n\n\nclass MyTaskRunner(TaskRunner):\n    def run(self):\n        # Specific implementation\n        self.task.log_status(\'STARTED\', checkpoint=False)\n        self.task.log_status(\'Checkpoint 1\', checkpoint=True)\n        self.task.log_status(\'FINISHED\')\n```\n\n### Command to list registered taskrunners\n\nWe can list the registered taskrunner with the command `list_taskrunners`.\n\n```bash\npython manage.py list_taskrunners\n```\n\n### Command to launch tasks manually\n\nWe can create tasks using the command `create_tasks`.\n\n```bash\npython manage.py create_task --help\nusage: manage.py create_task [-h] [--input INPUT] [--raw-input RAW_INPUT] [--queue QUEUE] [--when WHEN] [--version] [-v {0,1,2,3}] [--settings SETTINGS] [--pythonpath PYTHONPATH] [--traceback] [--no-color] [--force-color]\n                             [--skip-checks]\n                             task_type\n\npositional arguments:\n  task_type             Task type identifier\n\noptions:\n  -h, --help            show this help message and exit\n  --input INPUT         File input -- can be redirected from standard output\n  --raw-input RAW_INPUT\n                        Raw string input -- Must be in json format\n  --queue QUEUE         Celery queue name in which the task will be run\n  --when WHEN           Scheduled task run date -- ISO Format\n\n```\n\n**Examples:**\n\n```bash\npython manage.py create_task <task_type> --raw-input=\'{}\'\ncat file.json | python manage.py create_task <task_type> --queue="celery" --input -\n```\n\n## Setup\n\n| Environment variable | Type | Description |\n| -------- |  ----------- | ----------- |\n| KEEP_TASK_HISTORY_DAYS | int | Number of days to keep the tasks |\n| DEFAULT_NOTIFICATION_EMAIL | str | Default e-mail to notify |\n\n## Django Rest Framework\n\n> To use Django Rest Framework extension we have to install with the `drf` extra. \n\nIn our project `urls.py` we have to add the Gonk urls:\n\n```python\nfrom django.urls import path, include\n\nurlpatterns = [\n    # ...\n    path(\'tasks/\', include(\'gonk.contrib.rest_framework.urls\')),\n]\n```\n\n## Notifications with Mercure\n\n> To use Mercure extension we have to install with the `mercure` extra. \n\n\nTo send notifications with Mercure we have to setup the following environment variables:\n\n| Variable | Type | Description |\n| -------- |  ----------- | ----------- |\n| MERCURE_HUB_URL | str | Mercure service URL |\n| MERCURE_JWT_KEY | str | Mercure\'s JWT Token to publish events |\n\n```python\n# taskrunners.py\nfrom gonk.taskrunners import TaskRunner\nfrom gonk.contrib.notifications.mercure import MercureNotificationMixin\n\n\nclass MyTaskRunner(MercureNotificationMixin, TaskRunner):\n    # Specific implementation\n\n```\n\n## Development\n\n### Clone repository\n```bash\ngit clone git@gitlab.com:kas-factory/packages/gonk.git && cd gonk\n```\n\n### Install poetry\n\n```bash\npip install poetry\n```\n\n### Install dependencies\n\n```bash\npoetry install\n```\n\n### Run docker-compose\n\n```bash\ndocker-compose up -d\n```\n\n### Launch celery worker\n\n```bash\npoetry run celery -A test_app worker\n```\n\n### Launch celery beat\n\n```bash\npoetry run celery -A test_app beat\n```\n\n> At this point, we have to ensure that `gonk.tasks.to_run`, `gonk.tasks.to_revert` and \n> `gonk.tasks.to_schedule` tasks are detected\n\n\n## Credits\n\n### Authors\n\n- [Francisco Javier Lendínez](https://github.com/FJLendinez/)\n- [Pablo Moreno](https://github.com/pablo-moreno/)\n\n',
    'author': 'Francisco Javier Lendinez Tirado',
    'author_email': 'lendinez@kasfactory.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kasfactory/gonk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
