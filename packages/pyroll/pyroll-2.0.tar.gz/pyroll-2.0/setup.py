# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyroll']

package_data = \
{'': ['*']}

install_requires = \
['pyroll-cli>=2.0,<3.0',
 'pyroll-core>=2.0,<3.0',
 'pyroll-export>=2.0,<3.0',
 'pyroll-report>=2.0,<3.0']

setup_kwargs = {
    'name': 'pyroll',
    'version': '2.0',
    'description': 'A meta package for installing quickly the PyRolL Core, CLI, Report and Export. The provided functionality is similar to the old pyroll package, which was split up into distinct packages with version 2.0.',
    'long_description': '# PyRolL Meta-Package\n\nThis is a meta-package intended to replace the old version 1.0 `pyroll` package and protect from version conflicts.\nIt installs the following packages:\n\n- `pyroll-core`\n- `pyroll-cli`\n- `pyroll-report`\n- `pyroll-export`\n\n## License\n\nThe project is licensed under the [BSD 3-Clause license](LICENSE).\n',
    'author': 'Max Weiner',
    'author_email': 'max.weiner@imf.tu-freiberg.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pyroll.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
