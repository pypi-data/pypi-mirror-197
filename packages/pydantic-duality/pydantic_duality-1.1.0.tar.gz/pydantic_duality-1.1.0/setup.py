# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_duality']

package_data = \
{'': ['*']}

install_requires = \
['cached-classproperty>=0.1.0', 'pydantic>=1.9.2', 'typing-extensions>=4.4.0']

setup_kwargs = {
    'name': 'pydantic-duality',
    'version': '1.1.0',
    'description': 'Automatically generate two versions of your pydantic models: one with Extra.forbid and one with Extra.ignore',
    'long_description': '\n<p align="center">\n  <a href="https://ovsyanka83.github.io/pydantic-duality/"><img src="https://raw.githubusercontent.com/Ovsyanka83/pydantic-duality/main/docs/_media/logo_with_text.svg" alt="Pydantic Duality"></a>\n</p>\n<p align="center">\n  <b>Automatically and lazily generate three versions of your pydantic models: one with Extra.forbid, one with Extra.ignore, and one with all fields optional</b>\n</p>\n\n---\n\n<p align="center">\n<a href="https://github.com/ovsyanka83/pydantic-duality/actions?query=workflow%3ATests+event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/Ovsyanka83/pydantic-duality/actions/workflows/test.yaml/badge.svg?branch=main&event=push" alt="Test">\n</a>\n<a href="https://codecov.io/gh/ovsyanka83/pydantic-duality" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/ovsyanka83/pydantic-duality?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/pydantic-duality/" target="_blank">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/pydantic-duality?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/pydantic-duality/" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/pydantic-duality?color=%2334D058" alt="Supported Python versions">\n</a>\n</p>\n\n## Installation\n\n```bash\npip install pydantic-duality\n```\n\n## Quickstart\n\nGiven the following models:\n\n```python\n\nfrom pydantic_duality import DualBaseModel\n\n\nclass User(DualBaseModel):\n    id: UUID\n    name: str\n\nclass Auth(DualBaseModel):\n    some_field: str\n    user: User\n```\n\nUsing pydantic-duality is roughly equivalent to making all of the following models by hand:\n\n```python\n\nfrom pydantic import BaseModel\n\n# Equivalent to User and User.__request__\nclass UserRequest(BaseModel, extra=Extra.forbid):\n    id: UUID\n    name: str\n\n# Rougly equivalent to Auth and Auth.__request__\nclass AuthRequest(BaseModel, extra=Extra.forbid):\n    some_field: str\n    user: UserRequest\n\n\n# Rougly equivalent to User.__response__\nclass UserResponse(BaseModel, extra=Extra.ignore):\n    id: UUID\n    name: str\n\n# Rougly equivalent to Auth.__response__\nclass AuthResponse(BaseModel, extra=Extra.ignore):\n    some_field: str\n    user: UserResponse\n\n\n# Rougly equivalent to User.__patch_request__\nclass UserPatchRequest(BaseModel, extra=Extra.forbid):\n    id: UUID | None\n    name: str | None\n\n# Rougly equivalent to Auth.__patch_request__\nclass AuthPatchRequest(BaseModel, extra=Extra.forbid):\n    some_field: str | None\n    user: UserPatchRequest | None\n\n```\n\nSo it takes you up to 3 times less code to write the same thing. Note also that pydantic-duality does everything lazily so you will not notice any significant performance or memory usage difference when using it instead of writing everything by hand. Think of it as using all the customized models as cached properties.\n\nInheritance, inner models, custom configs, [custom names](https://ovsyanka83.github.io/pydantic-duality/#/?id=customizing-schema-names), config kwargs, isinstance and subclass checks work intuitively and in the same manner as they would work if you were not using pydantic-duality.\n\n## Help\n\nSee [documentation](https://ovsyanka83.github.io/pydantic-duality/#/) for more details\n',
    'author': 'Stanislav Zmiev',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Ovsyanka83/pydantic-duality',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
