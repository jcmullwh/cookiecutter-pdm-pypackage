# {{cookiecutter.project_name}}

<p align="center">
    <em>{{cookiecutter.project_short_description}}</em>
</p>

[![build]({{cookiecutter.repository_url}}/workflows/Build/badge.svg)]({{cookiecutter.repository_url}}/actions)
[![codecov](https://codecov.io/gh/{{cookiecutter.repository_name}}/branch/master/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.repository_name}}/branch/master)
[![PyPI version](https://badge.fury.io/py/{{cookiecutter.dist_name}}.svg)](https://badge.fury.io/py/{{cookiecutter.dist_name}})

---

**Documentation**: <a href="{{cookiecutter.docs_url}}" target="_blank">{{cookiecutter.docs_url}}</a>

**Source Code**: <a href="{{cookiecutter.repository_url}}" target="_blank">{{cookiecutter.repository_url}}</a>

---

## Development
### Setup Environment
We use PDM to manage the development environment and production build. Ensure it's installed on your system.

### Install PDM
You can install PDM via pip:
```
pip install pdm
```
Alternatively, follow the official installation guide.

### Initialize the Project
After installing PDM, install the project dependencies and set up the environment:
```
pdm install
```

### Run Unit Tests
You can run all the tests with:
```
pdm run test
```
To generate a coverage report in XML format:
```
pdm run test-cov-xml
```

### Format the Code
Execute the following command to apply linting and check typing:
```
pdm run lint
```
To perform a lint check without making changes:
```
pdm run lint-check
```

### Publish a New Version
You can bump the version, create a commit, and associated tag with one command using PDM:
```
pdm run bump-patch
pdm run bump-minor
pdm run bump-major
```


### Build the Project
To build the project, use:
```
pdm build
```

### Serve the Documentation
You can serve the MkDocs documentation with:
```
pdm run docs-serve
```
It will automatically watch for changes in your code.

To build the static documentation site:
```
pdm run docs-build
```

### Additional Scripts
PDM allows you to define custom scripts in your pyproject.toml. Here are the available scripts:

test: Runs the unit tests.
test-cov-xml: Runs tests with coverage report in XML format.
lint: Applies linting and type checking.
lint-check: Checks linting without making changes.
docs-serve: Serves the documentation locally.
docs-build: Builds the static documentation site.
You can execute any of these scripts using:
```
pdm run <script-name>
```
For example:
```
pdm run lint
```

### License
This project is licensed under the terms of the {{cookiecutter.open_source_license}}.