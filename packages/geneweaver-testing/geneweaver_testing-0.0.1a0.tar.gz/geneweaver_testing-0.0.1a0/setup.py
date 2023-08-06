# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['testing',
 'testing.fixtures',
 'testing.package',
 'testing.schemas',
 'testing.sytax']

package_data = \
{'': ['*']}

install_requires = \
['black>=23.1.0,<24.0.0',
 'isort>=5.12.0,<6.0.0',
 'mypy>=1.0.1,<2.0.0',
 'pytest>=7.2.2,<8.0.0',
 'ruff>=0.0.254,<0.0.255']

setup_kwargs = {
    'name': 'geneweaver-testing',
    'version': '0.0.1a0',
    'description': '',
    'long_description': '# Geneweaver Testing\nThis package is used to test the Geneweaver project. It contains tools for running tests against Geneweaver project\npackages and components to aid in the development of Geneweaver. \n\n## Package Modules\nLike all Geneweaver packages, this package is namespaced under the `geneweaver` package. The root of this package is\n`geneweaver.testing`. The following modules are available in this package:\n\n### `geneweaver.testing.fixtures`\nThis module contains pytest fixtures that are used to test Geneweaver packages. These fixtures can be used to set up\ntest contexts for Geneweaver packages.\n\n### `geneweaver.testing.package`\nThis module contains tools for testing and validating Geneweaver packages. \n\n### `geneweaver.testing.schemas`\nThis module contains tools for validating that methods and functions in Geneweaver packages conform to the Geneweaver\nproject schemas. This package **does not** contain the schemas themselves. The schemas are defined in the\n`geneweaver-core` / `geneweaver.core.schemas` package.\n\n### `geneweaver.testing.syntax`\nThis module contains tools for running syntax and style checks on Geneweaver packages. This ensures that Geneweaver\npackages each conform to the same style and syntax standards.\n\n## Usage\n',
    'author': 'Alexander Berger',
    'author_email': 'alexander.berger@jax.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
