# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nops_metadata', 'nops_metadata.tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.102',
 'pydantic>=1.8.0',
 'pyrsistent>=0.17.3',
 'pyspark[sql]==3.3.1']

setup_kwargs = {
    'name': 'nops-metadata',
    'version': '0.4.8',
    'description': 'Metadata producer tooling used in nOps.io',
    'long_description': 'None',
    'author': 'nOps Engineers',
    'author_email': 'eng@nops.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
