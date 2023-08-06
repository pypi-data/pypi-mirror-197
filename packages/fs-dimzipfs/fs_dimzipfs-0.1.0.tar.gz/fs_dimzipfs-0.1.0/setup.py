# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fs', 'fs.dimzipfs']

package_data = \
{'': ['*']}

install_requires = \
['fs>=2.4.16,<3.0.0', 'lxml>=4.9.2,<5.0.0']

entry_points = \
{'fs.opener': ['dimzip = fs.dimzipfs.opener:DIMZipOpener']}

setup_kwargs = {
    'name': 'fs-dimzipfs',
    'version': '0.1.0',
    'description': 'Pyfilesystem2 implementation for DAZ Install Manager Packages',
    'long_description': 'fs.dimzipfs\n===========\n\n``fs.dimzipfs`` is a PyFileSystem2 interface for DAZ Install Manager packages.\n\nThe exposed filesystem is as defined in Manifest.dsx, not the zipfile.\n\nSupported Python versions\n-------------------------\n\n- Python 3.11\n\nUsage\n-----\n\n.. code:: python\n\n    >>> from fs.dimzipfs import DIMZipFS\n\n    >>> DIMZipFS(\'IM00013176-02_DAZStudio421Win64bit.zip\').listdir(\'\')\n    ....\n    [\'Application[PC-64-DAZ Studio-4.5]\', \'Temp[PC-64]\']\n\n    >>> DIMZipFS(\'IM00013176-42_DefaultResourcesforDAZStudio420.zip\').opendir(\'Content\').listdir(\'\')\n    ....\n    [\'data\', \'Light Presets\', \'Props\', "ReadMe\'s", \'Render Presets\', \'Runtime\', \'Scenes\', \'Scripts\', \'Shader Presets\']\n\nLicense\n-------\n\nThis module is published under the MIT license.',
    'author': 'Omni Flux',
    'author_email': 'omniflux@omniflux.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Omniflux/fs.dimzipfs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11',
}


setup(**setup_kwargs)
