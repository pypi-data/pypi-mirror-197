# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octopus_sensing_processing']

package_data = \
{'': ['*']}

install_requires = \
['CherryPy>=18.6.0,<19.0.0', 'numpy>=1.21.0,<2.0.0']

entry_points = \
{'console_scripts': ['octopus-sensing-processing = '
                     'octopus_sensing_processing.main:main']}

setup_kwargs = {
    'name': 'octopus-sensing-processing',
    'version': '1.0.1',
    'description': 'Web base data processing for https://octopus-sensing.nastaran-saffar.me',
    'long_description': 'Octopus Sensing Processing\n==========================\n\nOctopus Sensing Processing is a real-time data processing for [Octopus Sensing](https://octopus-sensing.nastaran-saffar.me/). \nIt can be used for processing data in real-time. You can define your favorite processor and process your data in real-time and publish the processing result. For example if you define an emotion recognition processor, Octopus Sensing Processing can prepare the input of your processor in real-time and publish your created prediction by streaming them as json data or other applications could send a request for receiving them when they needed the processing result.\n\n[Octopus Sensing Processing](https://github.com/octopus-sensing/octopus-sensing-processing) is \na separated project and can be installed if we need to visualize data. \nIt can be used for displaying recorded data with\nthe same format as we recorded through Octopus Sensing.\n\n**To see the full documentation go to [Otopus Sensing](https://octopus-sensing.nastaran-saffar.me/processing) website.**\n\nCopyright\n---------\n\nCopyright © 2022 [Nastaran Saffaryazdi]\n\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU\nGeneral Public License as published by the Free Software Foundation, either version 3 of the\nLicense, or (at your option) any later version.\n\nSee [License file](https://github.com/octopus-sensing/octopus-sensing/blob/master/LICENSE)  for full terms.',
    'author': 'Aidin Gharibnavaz',
    'author_email': 'aidin@aidinhut.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/octopus-sensing/octopus-sensing-processing',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
