# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecs_composex_msk_cluster']

package_data = \
{'': ['*']}

install_requires = \
['compose-x-common>=1.2,<2.0', 'ecs_composex>=0.23.7,<0.24.0']

setup_kwargs = {
    'name': 'ecs-composex-msk-cluster',
    'version': '0.3.0.post0',
    'description': 'msk_cluster - AWS MSK Cluster module for ECS Compose-X',
    'long_description': '\n.. meta::\n    :description: ECS Compose-X MSK Cluster\n    :keywords: AWS, ECS, docker, compose, MSK, kafka\n\n================\nmsk_cluster\n================\n\n.. image:: https://img.shields.io/pypi/v/ecs_composex_msk_cluster.svg\n    :target: https://pypi.python.org/pypi/ecs_composex_msk_cluster\n\n\nThis package is an extension to `ECS Compose-X`_ that manages Creation of new MSK clusters and automatically links\nto services to grant access and permissions.\n\nInstall\n==========\n\n.. code-block:: bash\n\n    python3 -m venv venv\n    source venv/bin/activate\n    # With poetry\n\n    pip install pip poetry -U\n    poetry install\n\n    # Via pip\n    pip install pip -U\n    pip install ecs-composex-msk-cluster\n\nSyntax Reference\n==================\n\n.. code-block:: yaml\n\n    x-msk_cluster:\n          Properties: {}\n          Lookup: {}\n          Settings: {}\n          Services: {}\n\n`Full documentation <https://msk-cluster.docs.compose-x.io/>`_\n\nExamples can be found in ``use-cases`` in this repository.\n\n.. _ECS Compose-X: https://docs.compose-x.io\n.. _Properties for MSK Cluster: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html\n',
    'author': 'johnpreston',
    'author_email': 'john@compose-x.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
