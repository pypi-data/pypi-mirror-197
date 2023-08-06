# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdbundle_pycortexmdebug',
 'gdbundle_pycortexmdebug.cmdebug',
 'gdbundle_pycortexmdebug.cmdebug.cmdebug',
 'gdbundle_pycortexmdebug.cmdebug.scripts']

package_data = \
{'': ['*']}

install_requires = \
['gdbundle>=0.0.3,<0.1.0', 'lxml>=4.5.2,<5.0.0']

setup_kwargs = {
    'name': 'gdbundle-pycortexmdebug',
    'version': '0.0.7',
    'description': 'gdbundle wrapper for PyCortexMDebug',
    'long_description': '[![GitHub](https://img.shields.io/badge/GitHub-memfault/gdbundle--pycortexmdebug-8da0cb?style=for-the-badge&logo=github)](https://github.com/memfault/gdbundle-PyCortexMDebug)\n[![PyPI\nversion](https://img.shields.io/pypi/v/gdbundle-pycortexmdebug.svg?style=for-the-badge)](https://pypi.org/project/gdbundle-pycortexmdebug/)\n[![PyPI\npyversions](https://img.shields.io/pypi/pyversions/gdbundle-pycortexmdebug.svg?style=for-the-badge)](https://pypi.python.org/pypi/gdbundle-pycortexmdebug/)\n\n# gdbundle-PyCortexMDebug\n\nThis is a [gdbundle](https://github.com/memfault/gdbundle) plugin for\n[bnahill/PyCortexMDebug](https://github.com/bnahill/PyCortexMDebug)\n\nThe original `PyCortexMDebug` plugin is embedded as a git submodule, rather than\nspecifying as a typical dependency, because it is not as of yet deployed to\nPyPi, and so this package cannot depend on it via `git+` dependency spec.\n\n## Compatibility\n\n- GDB\n\n## Installation\n\nAfter setting up [gdbundle](https://github.com/memfault/gdbundle), install the\npackage from PyPi.\n\n```bash\n$ pip install gdbundle-PyCortexMDebug\n```\n\nIf you\'ve decided to manually manage your packages using the\n`gdbundle(include=[])` argument, add it to the list of plugins.\n\n```bash\n# .gdbinit\n\n[...]\nimport gdbundle\nplugins = ["PyCortexMDebug"]\ngdbundle.init(include=plugins)\n```\n\n## Building\n\nBe sure to `git submodule update --init` to get the `cmdebug` dependency.\n\n```bash\n$ poetry build\n$ poetry publish\n```\n',
    'author': 'Tyler Hoffman',
    'author_email': 'tyler@memfault.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
