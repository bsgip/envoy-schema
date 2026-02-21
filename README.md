# envoy-schema - forked for Synergy storage extension

This is a forked project with a long lived branch which implements the CSIP-Aus storage extension (https://csipaus.org/ns/v1.3-beta/storage) proposed by Synergy

The original project, which focuses implementation on the current accepted CSIP-Aus standards, is developed by [BSGIP here](https://github.com/bsgip/envoy-schema)

## Assumed workflow

This repository's [main branch](https://github.com/synergy-au/envoy-schema/tree/main) is intended to always follow the original [BSGIP main](https://github.com/bsgip/envoy-schema) 
e.g. using GitHub's built in "Sync Fork" feature

Whenever a "sync" occurs, efforts should be made to merge these into the longlived [csipaus.org/ns/v1.3-beta/storage branch](https://github.com/synergy-au/envoy-schema/tree/csipaus.org/ns/v1.3-beta/storage)

All changes that can apply to both repositories/branches is preferred to be resolved by raising a pull request against the original [BSGIP main](https://github.com/bsgip/envoy-schema)
and then merging this into main. Of course this could be too slow for implementation purposes and should be reviewed on a case by case basis.

All remaining sections should reflect the original documentation as part of the [original repository](https://github.com/bsgip/envoy-schema). 
<br><br>


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


