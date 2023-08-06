# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shiny_multiprocessing']

package_data = \
{'': ['*']}

install_requires = \
['pebble>=5.0.3,<6.0.0']

setup_kwargs = {
    'name': 'shiny-multiprocessing',
    'version': '0.1.1',
    'description': '',
    'long_description': '# shiny_multiprocessing\n\nA small token piece of code meant to make multiprocessing a bit handier, when\nit comes to executing functions, that need proper monitoring in terms of\nidling, timing out or failing with errors.\n\nIt makes use of Pebble to reliably enforce timeouts on the individual processes\nwhile also providing comfortable retry capabilities for a range of exceptions\nof your selection.\n\nMore documentation to come. Maybe.',
    'author': 'Maximilian Töpfer',
    'author_email': 'maxtoepfer@mailbox.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
