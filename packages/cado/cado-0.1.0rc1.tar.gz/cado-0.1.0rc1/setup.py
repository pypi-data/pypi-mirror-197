# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cado', 'cado.app', 'cado.cli', 'cado.core', 'cado.examples']

package_data = \
{'': ['*'],
 'cado': ['ui/*',
          'ui/public/*',
          'ui/src/*',
          'ui/src/components/*',
          'ui/src/hooks/*',
          'ui/src/images/*',
          'ui/src/lib/*',
          'ui/src/lib/models/*',
          'ui/src/widgets/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'fastapi>=0.70.0,<0.71.0',
 'pydantic>=1.9.0,<2.0.0',
 'uvicorn[standard]>=0.15.0,<0.16.0']

entry_points = \
{'console_scripts': ['cado = cado.cli.cli:main']}

setup_kwargs = {
    'name': 'cado',
    'version': '0.1.0rc1',
    'description': 'Python notebook development environment.',
    'long_description': '<div align="center">\n  <img src="assets/cado-banner.png">\n  <h1>cado</h1>\n\n  <p>\n    <strong>Python notebook IDE with a focus on reactivity</strong>\n  </p>\n\n  <br>\n  <div>\n    <a href="https://badge.fury.io/py/cado"><img src="https://badge.fury.io/py/cado.svg" alt="PyPI"></a>\n    <a href="https://pepy.tech/project/cado"><img src="https://pepy.tech/badge/cado" alt="Downloads"></a>\n    <a href="https://github.com/gregorybchris/cado/actions/workflows/ci.yaml"><img src="https://github.com/gregorybchris/cado/actions/workflows/ci.yaml/badge.svg" alt="CI"></a>\n  </div>\n  <br>\n</div>\n\n## About\n\n`cado` is a notebook IDE for Python, like [Jupyter](https://jupyter.org/), but with a reactive cell model, taking inspiration from [Observable](https://observablehq.com/). Each cell defines its own outputs that other cells can listen to. When the output of a parent cell updates, the change propagates to all child cells. When a child runs, it uses cached outputs from parent cells, reducing the amount of computation per cell.\n\n## Installation\n\n```bash\npip install cado\n```\n\n## Usage\n\n```bash\n# Start up a cado server\ncado up\n```\n',
    'author': 'Chris Gregory',
    'author_email': 'christopher.b.gregory@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gregorybchris/cado',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4',
}


setup(**setup_kwargs)
