# `vezzo`:  a small library to parse version strings from binfie tools

<div align="center">
    <a href="https://badge.fury.io/py/vezzo"><img src="https://badge.fury.io/py/vezzo.svg" alt="PyPI version" height="18"></a>
    <a href="https://zenodo.org/badge/latestdoi/615520033"><img src="https://zenodo.org/badge/615520033.svg" alt="DOI"></a>
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/vezzo">
</div
## Background

It is a common pattern when running binfie tools to run checks on the versions 
of the tool's dependencies. For example, the tool might depend on `blastn` being
of version 2.10.0 or higher. This library provides a simple way to parse the 
version from the output of running `blastn -version` and compare it to the minimum
version required. To run the comparison, we use the `semver` [library](https://python-semver.readthedocs.io/en/latest/).

## Usage
The main function provided by the library is `vezzo.verify_from_config`. This 
function takes in the path to a YAML file that specifies the version requirements and checks them against the observed versions installed in the enviroment. It expects the dependencies to be in the path. The YAML file should be a list of dictionaries, where each dictionary specifies the requirements for a single tool. The dictionary should have the following fields:

```yaml
- name: blastn
  req_version: ">=2.10.0"
  version_flag: -version
  exit_code: 0

- name: samtools
  req_version: ">=1.16.0"
  version_flag: --version
  exit_code: 0
```

The `name` field is the name of the tool. The `req_version` field that specifies
the requirements in terms of the version of the tool. This takes one the following
format:
    - <1.2.3: the observed version must be less than 1.2.3
    - <=1.2.3: the observed version must be less than or equal to 1.2.3
    - >1.2.3: the observed version must be greater than 1.2.3
    - >=1.2.3: the observed version must be greater than or equal to 1.2.3
    - ==1.2.3: the observed version must be equal to 1.2.3
    - !=1.2.3: the observed version must not be equal to 1.2.3

The `version_flag` field specifies the flag to pass to the tool to get the version
string. This can be empty string, as is the case for `bwa`, which does not have a flag.

The `exit_code` field specifies the exit code that the tool returns when the version 
string is returned. The majority of cases this is 0, but `bwa`, for instance, returns

By specifying all the version requirements in a YAML config file that ships with your
package it is easy to check dependencies and modify requirement all in one location.

A full working example is provided in the `example` directory. To run the example,
simply run `python example/example1.py`.

The output from the example is (the exact output will depend on the versions you have, and any tweaks you make to the example config file):

```bash
blastn version 2.13.0 DOES NOT match requirements >=2.14.0.... ❌ 
samtools version 1.17.0 matches requirements >=1.16.0.... ✔ 
There was 1 tool that failed the version requirements. Please ensure these are corrected before proceeding. 😢 
```

The basic code might look like this:

```python
for is_match, obs_version, exp_version, tool in vezzo.verify_from_config(config):
    if is_match:
        sys.stderr.write(
            f"\033[32m {tool} version {obs_version} matches requirements {exp_version}.... \u2714 \033[0m\n"
        )
    else:
        sys.stderr.write(
            f"\033[31m {tool} version {obs_version} DOES NOT matches requirements {exp_version}.... \u274C \033[0m\n"
        )
        fails += 1

if fails > 0:
    sys.stderr.write(
        f"\033[31m There {'was' if fails == 1 else 'were'} {fails} tool{'s' if fails > 0 else ''} that failed the version requirements. Please ensure these are corrected before proceeding. \U0001F622 \033[0m\n"
    )
    sys.exit(1)
```

As as can be seen, the function returns a generator that yields a tuple of the following
format: `(is_match, obs_version, exp_version, tool)`. The `is_match` field is a boolean
that indicates whether the observed version matches the expected version criteria. 
The `obs_version` field is the observed version string. The `exp_version` field is the
expected string requirement in the format outlined above. The `tool` field is the name of the tool.

## Installation

The library can be installed via `pip`:

```bash
pip install vezzo
```

## Author
Anders Goncalves da Silva (@andersgs)
