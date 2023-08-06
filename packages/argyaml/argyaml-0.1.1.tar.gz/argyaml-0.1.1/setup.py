# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argyaml', 'argyaml.handlers']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['generate = argyaml.__main__:generate',
                     'main = argyaml.__main__:run']}

setup_kwargs = {
    'name': 'argyaml',
    'version': '0.1.1',
    'description': 'Create a powerful and efficient CLI application using simple and user-friendly yaml config',
    'long_description': '# Argyaml\nArgyaml is a small module for creating _powerful_ and _scalable_ __CLI applications__ based on a _simple_ and _user-friendly_ yaml __configuration file__.\n\n### Motivation\nArgyaml is built over the [argparse](https://docs.python.org/3/library/argparse.html) module, which is a part of python standard library starting python 3.2. While it works well for tiny projects that need to quickly access a few arguments and provide automatically generated help and usage messages for user, it gets very complicated and painful when it comes to large projects or your application grows in complexity.\n\n### Features\n- Independent specification of CLI commands and arguments.\n- No boilerplate code.\n- Ability to set default options for commands, groups, and arguments.\n- Automatic and optimized invocation of command handlers.\n- Handler template files generator.\n\n## Install\n\n```bash\n# pip\npip install argyaml\n\n# poetry\npoetry add argyaml\n```\n\n## Getting started\n```yaml\n# cli-config.yaml\nprog: todo\ndescription: My beautiful todo app\nnext:\n  - command: new\n    next:\n      - command: task\n        description: Create a new task\n        next:\n          - argument: [name]\n            help: the name of task\n  - command: list\n    next:\n      - argument: [-t, --task]\n        help: display tasks only\n        action: \'store_true\'\n```\n\n```python\nfrom argyaml import BaseHandler\n\nbase = BaseHandler()\nbase.args # <-- parsed and ready-to-use arguments\n```\n\n__Learn more about [config file](./wiki#Config).__\n\n\n### Using Handlers\nGenerate template files using `argyaml generate`:\n```bash\n# pip\npython -m argyaml generate\n\n# poetry\npoetry run python -m argyaml generate\n```\nThis will generate the following files:\n```new\nhandlers/\n  _new_task.py\n  _list.py\n```\nNow, whenever `new task` command is called, the corresponding handler init function will be invoked with all additional aruments stored in the `self.args` object.\n\n```python\n# _new_task.py\nfrom argyaml import BaseHandler\n\nclass Handler(BaseHandler.meta()):\n    def __init__(self):\n        print(f"Successfully created task \'{self.args[\'name\']}\'!")\n```\nModify the main file to run the base handler:\n```python\nfrom argyaml import BaseHandler\n\nbase = BaseHandler()\nbase.run()\n```\n\n__Learn more about [BaseHandler](./wiki#BaseHandler) and [argyaml generator](./wiki#Generator).__\n\n## Contributing\nFeel free to open issues. Pull requests are welcome.\n\n## License\nThis project is licensed under the [MIT License](./LICENSE).\n',
    'author': 'Artur Sharapov',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
