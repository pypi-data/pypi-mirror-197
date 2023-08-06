# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_python', 'hypermodern_python.wikipedia']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'marshmallow>=3.19.0,<4.0.0', 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-python = hypermodern_python.__main__:main']}

setup_kwargs = {
    'name': 'hypermodern-python-tuto',
    'version': '0.1.1',
    'description': "Repo to follow the Claudio Jolowicz's tutorial about Hypermodern Python (https://cjolowicz.github.io/posts/hypermodern-python-01-setup/)",
    'long_description': "# hypermodern-python-tuto\n\nRepo to follow the Claudio Jolowicz's [tutorial about Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/).\n\n[![Tests](https://github.com/le-chartreux/hypermodern-python-tuto/workflows/Tests/badge.svg)](https://github.com/le-chartreux/hypermodern-python-tuto/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/le-chartreux/hypermodern-python-tuto/branch/master/graph/badge.svg)](https://codecov.io/gh/le-chartreux/hypermodern-python-tuto)\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-python-tuto.svg)](https://pypi.org/project/hypermodern-python-tuto/)\n\n## Table of contents\n\n- [Description of the application](#description-of-the-application)\n- [Install](#install)\n- [Use](#use)\n- [Tools used](#tools-used)\n  - [Generic tools](#generic-tools)\n  - [Generic Python tools](#generic-python-tools)\n    - [Multi-purpose](#multi-purpose)\n    - [Setup](#setup)\n    - [Test](#test)\n    - [Linting](#linting)\n    - [Security](#security)\n    - [Formatting](#formatting)\n    - [Type checking](#type-checking)\n    - [Documentation](#documentation)\n  - [Specific Python tools](#specific-python-tools)\n    - [UI](#ui)\n    - [Communication](#communication)\n    - [Data validation](#data-validation)\n\n## Description of the application\n\nThe app created is a CLI application that queries a random Wikipedia page and displays its title and summary.\n\n## Install\n\nTODO\n\n## Use\n\nTODO\n\n## Tools used\n\n### Generic tools\n\nTools that can be used in every development project, no matter if it's a Python project or not.\n\n- [git](https://git-scm.com/), to manage versions of the source code\n- [GitHub](https://github.com/le-chartreux/hypermodern-python-tuto), to host the git repository and execute Actions\n- [pre-commit](https://pre-commit.com/), to manage pre-commit hooks\n- [Codecov](https://about.codecov.io/), to mesure code coverage on repos\n- [PyPI](https://pypi.org/), to publish packages\n\n### Generic Python tools\n\nTools that can be used in every Python project, no matter its content.\n\n#### Multi-purpose\n\n- [poetry](https://python-poetry.org/), to make development and distribution easy (packaging, virtualization, dependencies, launching and publishing)\n- [nox](https://nox.thea.codes/en/stable/), to run tasks in multiple Python environments (like tests, linting, reformatting, etc.)\n\n#### Setup\n\n- [pyenv](https://github.com/pyenv/pyenv), to manage Python versions\n\n#### Test\n\n- [pytest](https://docs.pytest.org/en/latest/), a framework to write unit tests. Also used to run doctests\n- [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/), to mesure the code coverage (degree to which the source code of a program is executed while running its test suite)\n- [pytest-mock](https://pytest-mock.readthedocs.io/en/latest/), to use the [unittest](https://docs.python.org/3/library/unittest.html) mocking in the pytest way\n- [xdoctest](https://pypi.org/project/xdoctest/), to execute the doctests (tests in documentation strings)\n\n#### Linting\n\n- [flake8](https://flake8.pycqa.org/en/latest/), a linter aggregator\n- [flake8-import-order](https://github.com/PyCQA/flake8-import-order), to verify that imports are grouped and ordered in a consistent way\n- [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear), to find bugs and design problems\n- [flake8-annotations](https://pypi.org/project/flake8-annotations/), to detect the absence of type annotations\n- [flake8-black](https://pypi.org/project/flake8-black/), to check if the code follows [black](https://black.readthedocs.io/en/stable/) formatting\n- [flake8-docstrings](https://pypi.org/project/flake8-docstrings/), to check that the code is correctly documented\n- [darglint](https://pypi.org/project/darglint/), to check that docstrings match function definitions\n\n#### Security\n\n- [Bandit](https://bandit.readthedocs.io/en/latest/), to find security issues (used inside linting with [flake8-bandit](https://pypi.org/project/flake8-bandit/))\n- [Safety](https://pyup.io/safety/), to check if some packages are insecure\n\n#### Formatting\n\n- [black](https://black.readthedocs.io/en/stable/), to format the code\n\n#### Type checking\n\n- [mypy](https://mypy-lang.org/), the classic type checker\n- [pytype](https://google.github.io/pytype/), a static type checker\n- [typeguard](https://typeguard.readthedocs.io/en/latest/), a runtime type check\n\n#### Documentation\n\n- [Sphinx](https://www.sphinx-doc.org/en/master/), the documentation tool used by the official Python documentation.\n- [autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html), Sphinx official plugin to generate API documentation from the docstrings.\n- [napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html), Sphinx official plugin to allow compatibility with Google-style docstrings.\n- [sphinx-autodoc-typehints](https://pypi.org/project/sphinx-autodoc-typehints/), Sphinx plugin to detect type hints in generated documentation.\n\n### Specific Python tools\n\nTools to match specific needs of the projet.\n\n#### UI\n\n- [click](https://click.palletsprojects.com/en/8.1.x/), to create CLI applications\n\n#### Communication\n\n- [requests](https://requests.readthedocs.io/en/latest/), to make HTTP requests\n\n#### Data validation\n\n- [marshmallow](https://marshmallow.readthedocs.io/en/stable/), to serialize, deserialize and validate data\n- ~~[dessert](https://desert.readthedocs.io/en/stable/), to generate marshmallow serialization schemas~~ → not used because too limited (can't work with data where fields names are different from the ones of the target dataclass)\n\nI used [marshmallow](https://marshmallow.readthedocs.io/en/stable/) to follow the tutorial, but  [pydantic](https://docs.pydantic.dev/) is more known, and I find it easier to use.\n",
    'author': 'le-chartreux',
    'author_email': 'le-chartreux-vert@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/le-chartreux/hypermodern-python-tuto',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
