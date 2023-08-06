# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['textual_todo']

package_data = \
{'': ['*']}

install_requires = \
['textual>=0.15.1,<0.16.0']

entry_points = \
{'console_scripts': ['todo = textual_todo.todo:app.run']}

setup_kwargs = {
    'name': 'textual-todo',
    'version': '0.1.0',
    'description': 'A simple TODO app built with Textual.',
    'long_description': '# Textual TODO App\n\n![](_static_app_demo.png)\n\n\n## Tutorial\n\n[Read the tutorial here!](https://mathspp.com/blog/textual-tutorial-build-a-todo-app-in-python)\n\n\n## GIF demo\n\n![](_app_demo.gif)\n',
    'author': 'Rodrigo Girão Serrao',
    'author_email': 'rodrigo@mathspp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
