# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qrm']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.7,<5.0',
 'paramiko>=2.8.0,<3.0.0',
 'pyqt5>=5.15,<6.0',
 'treelib>=1.6.1,<2.0.0']

entry_points = \
{'console_scripts': ['qrm = qrm.cli:main']}

setup_kwargs = {
    'name': 'qrm',
    'version': '0.1.4',
    'description': 'PyQt5 based reMarkable explorer',
    'long_description': "# QrM - Qt5 based file explorer for reMarkable\n\nUse a Qt5 based UI to ~manage~ view, upload, delete content of/to your\nreMarkable I/II via SSH.\n\n[Project page](https://projects.om-office.de/frans/qrm)\n\n\n## Usage\n\nRun `qrm` to connect to and see a list of content on a (WiFi enabled and switched on)\nreMarkable device.\n\nRun `qrm config-auth <KEY>=<VALUE> ...` to configure stuff, e.g.\n\n```\nqrm config-auth host=192.168.178.13 password='s0rry_Pl4in+ex+!'\n```\n\nRun `qrm [ls|list]` to list content on the connected device\n\nRun `qrm [upload|push] <FILE> [<FILE>]` to copy stuff onto the connected device\n\nRun `qrm reboot` to .. you know..\n\n\n### ToDo for v1.0\n\n* Allow hostnames instead of IP addresses\n* Make use of shared keys and configuration in `~/.ssh/config`\n* Support drag&drop to add content in UI\n* Support deletion\n\n## Installation\n\n```\npip3 install [--user] qrm\n```\n\n\n## Development & Contribution\n\n```\n# provide dependencies, consider also using pyenv\npip3 install -U poetry pre-commit\n\ngit clone --recurse-submodules https://projects.om-office.de/frans/qrm.git\n\ncd qrm\n\n# activate a pre-commit gate keeper\npre-commit install\n\n# if you need a specific version of Python inside your dev environment\npoetry env use ~/.pyenv/versions/3.10.4/bin/python3\n\npoetry install\n```\n\n## License\n\nFor all code contained in this repository the rules of GPLv3 apply unless\notherwise noted. That means that you can do what you want with the source\ncode as long as you make the files with their original copyright notice\nand all modifications available.\n\nSee [GNU / GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) for details.\n\n\n## Read\n\n*(nothing here yet)*\n",
    'author': 'Frans Fürst',
    'author_email': 'frans.fuerst+gitlab@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://projects.om-office.de/frans/qrm.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
