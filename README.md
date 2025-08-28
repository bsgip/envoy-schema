# envoy-schema
Public schema for the models/schema associated all envoy API endpoints.

This repository was built as a shared dependency for the envoy utility server and any external clients wishing to integrate. 

Envoy: https://github.com/bsgip/envoy


## Envoy Server Models

The models served under `envoy_schema.server` are derived from the following standards:

* [IEEE: Smart Energy Profile (2030.5-2018)](https://standards.ieee.org/ieee/2030.5/5897/)
* [Sunspec: Common Smart Inverter Profile](https://sunspec.org/2030-5-csip/)
* [Common Smart Inverter Profile (Australia)](https://csipaus.org/)


## Envoy Admin Models

The models served under `envoy_schema.admin` are typically only used for services directly integrating with the envoy utility server (via the admin server). This is for machine-machine services that are not typically exposed externally.

# Installation

Install directly from pypi

`pip install envoy_schema`


# Development

To install `envoy-schema` for development purposes, after cloning this repository:

```
pip install -e .[dev, test]
pytest
```

We use the following linting/formatting tools:
* [bandit](https://pypi.org/project/black/)
* [flake8](https://pypi.org/project/flake8/)
* [mypy](https://pypi.org/project/mypy/)

Contributions via a pull request are welcome but will be validated using the above tools.

Tests can be run with: `pytest` from the root directory.


