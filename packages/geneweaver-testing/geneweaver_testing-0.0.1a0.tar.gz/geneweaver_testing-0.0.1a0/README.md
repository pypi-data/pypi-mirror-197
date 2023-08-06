# Geneweaver Testing
This package is used to test the Geneweaver project. It contains tools for running tests against Geneweaver project
packages and components to aid in the development of Geneweaver. 

## Package Modules
Like all Geneweaver packages, this package is namespaced under the `geneweaver` package. The root of this package is
`geneweaver.testing`. The following modules are available in this package:

### `geneweaver.testing.fixtures`
This module contains pytest fixtures that are used to test Geneweaver packages. These fixtures can be used to set up
test contexts for Geneweaver packages.

### `geneweaver.testing.package`
This module contains tools for testing and validating Geneweaver packages. 

### `geneweaver.testing.schemas`
This module contains tools for validating that methods and functions in Geneweaver packages conform to the Geneweaver
project schemas. This package **does not** contain the schemas themselves. The schemas are defined in the
`geneweaver-core` / `geneweaver.core.schemas` package.

### `geneweaver.testing.syntax`
This module contains tools for running syntax and style checks on Geneweaver packages. This ensures that Geneweaver
packages each conform to the same style and syntax standards.

## Usage
