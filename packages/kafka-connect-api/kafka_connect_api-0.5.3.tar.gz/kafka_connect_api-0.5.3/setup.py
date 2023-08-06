# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kafka_connect_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

extras_require = \
{':extra == "awslambda"': ['jsonschema>=4.3.0,<5.0.0']}

setup_kwargs = {
    'name': 'kafka-connect-api',
    'version': '0.5.3',
    'description': 'Apache Kafka Connect client',
    'long_description': '========================================\nApache Kafka Connect API Python client\n========================================\n\n|PYPI_VERSION| |PYPI_LICENSE|\n\n|CODE_STYLE| |TDD| |BDD|\n\n|DOCS_BUILD|\n\nDocumentation: https://kafka-connect-api.readthedocs.io.\n\n\nInstall\n========\n\n.. code-block::\n\n    pip install kafka-connect-api\n\nUsage\n======\n\n.. code-block:: python\n\n    from kafka_connect_api.kafka_connect_api import Api, Cluster\n\n    api = Api(connect.cluster, port=8083)\n    cluster = Cluster(api)\n    print(cluster.connectors)\n\n\nFeatures\n==========\n\nAllows you to interact with the Kafka Connect API (`API Reference`_) in a simple way.\n\n* Connection to cluster (supports Basic Auth)\n* List all connectors in the cluster\n* Describe the connector configuration\n* Update the connector configuration\n* Pause / Resume Connector\n* Restart all tasks for the connector\n\nSome pre-made functions can help with operational activities.\nSee `kafka_connect_api.aws_lambdas.py`\n\n.. _API Reference: https://docs.confluent.io/platform/current/connect/references/restapi.html\n\n.. |DOCS_BUILD| image:: https://readthedocs.org/projects/kafka-connect-api/badge/?version=latest\n        :target: https://kafka-connect-api.readthedocs.io/en/latest/\n        :alt: Documentation Status\n\n.. |PYPI_VERSION| image:: https://img.shields.io/pypi/v/kafka-connect-api.svg\n        :target: https://pypi.python.org/pypi/kafka_connect_api\n\n.. |PYPI_LICENSE| image:: https://img.shields.io/pypi/l/kafka-connect-api\n    :alt: PyPI - License\n    :target: https://github.com/compose-x/kafka-connect-api/blob/master/LICENSE\n\n.. |PYPI_PYVERS| image:: https://img.shields.io/pypi/pyversions/kafka-connect-api\n    :alt: PyPI - Python Version\n    :target: https://pypi.python.org/pypi/kafka-connect-api\n\n.. |PYPI_WHEEL| image:: https://img.shields.io/pypi/wheel/kafka-connect-api\n    :alt: PyPI - Wheel\n    :target: https://pypi.python.org/pypi/kafka-connect-api\n\n.. |CODE_STYLE| image:: https://img.shields.io/badge/codestyle-black-black\n    :alt: CodeStyle\n    :target: https://pypi.org/project/black/\n\n.. |TDD| image:: https://img.shields.io/badge/tdd-pytest-black\n    :alt: TDD with pytest\n    :target: https://docs.pytest.org/en/latest/contents.html\n\n.. |BDD| image:: https://img.shields.io/badge/bdd-behave-black\n    :alt: BDD with Behave\n    :target: https://behave.readthedocs.io/en/latest/\n\n.. |QUALITY| image:: https://sonarcloud.io/api/project_badges/measure?project=compose-x_kafka-connect-api&metric=alert_status\n    :alt: Code scan with SonarCloud\n    :target: https://sonarcloud.io/dashboard?id=compose-x_kafka-connect-api\n\n.. |PY_DLS| image:: https://img.shields.io/pypi/dm/kafka-connect-api\n    :target: https://pypi.org/project/kafka-connect-api/\n',
    'author': 'John Preston',
    'author_email': 'john@compose-x.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
