"""
vezzo: a small library to parse version strings from binfie tools
"""

import re
import subprocess
import pathlib
from typing import Tuple
import semver
import yaml
from .exceptions import UnableToParseVersionString, UnableToGenerateVersionOutputString

# the official semver regex pattern from semver.org (https://semver.org/)
# modified to be able to pick the version string from the output of binfie tools
# and allow for option patch version
semver_pattern = re.compile(
    r"v?(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)(?:\.(?P<patch>0|[1-9]\d*))?(?:-(?P<prerelease>[\da-z\-]+(?:\.[\da-z\-]+)*))?(?:\+(?P<buildmetadata>[\da-z\-]+(?:\.[\da-z\-]+)*))?"
)


def parse(version_string: str) -> semver.VersionInfo:
    """
    Parse a version string from a binfie tool and return a semver.VersionInfo object

    Args:
        version_string (str): the version string to parse typically obtained from
        running a binfie tool with the --version flag

    Returns:
        semver.VersionInfo: a semver.VersionInfo object representing the version string

    Exceptions:
        UnableToParseVersionString: is raised when the version string cannot be parsed,
        the developer can then decide what to do with the exception
    """
    match = semver_pattern.search(version_string)
    try:
        return semver.VersionInfo(
            major=match.group("major"),
            minor=match.group("minor"),
            patch=0
            if match.group("patch") is None
            else match.group(
                "patch"
            ),  # to deal with edge cases that don't report a patch version
            prerelease=match.group("prerelease"),
            build=match.group("buildmetadata"),
        )
    except ValueError as error:
        raise UnableToParseVersionString(
            f"Error parsing version string: {error}"
        ) from error
    except AttributeError as error:
        raise UnableToParseVersionString(
            f"Error parsing version string: {error}"
        ) from error


def verify(exp_version: str, obs_version: str) -> Tuple[bool, str]:
    """
    Verify that the observed version meets the expectations of the expected version.
    Returns a tuple of a boolean and a string. The boolean is True if the observed
    version meets the expectations of the expected version. The string is the
    observed version.

    Args:
        exp_version (str): the expected version stringm with one of the following
        prefix modifiers:
            - <1.2.3: the observed version must be less than 1.2.3
            - <=1.2.3: the observed version must be less than or equal to 1.2.3
            - >1.2.3: the observed version must be greater than 1.2.3
            - >=1.2.3: the observed version must be greater than or equal to 1.2.3
            - ==1.2.3: the observed version must be equal to 1.2.3
            - !=1.2.3: the observed version must not be equal to 1.2.3
        obs_version (str): the observed version string, typically obtained from
        running a binfie tool with the --version flag

    Returns:
        Tuple[bool, str]: a tuple of a boolean and a string. The boolean is True if the
        observed version meets the expectations of the expected version. The string is
        the observed version.

    Exceptions:
        UnableToParseVersionString: is raised when the obs_string cannot be parsed.

    """
    try:
        obs = parse(obs_version)
        return (semver.VersionInfo.match(obs, exp_version), obs)
    except UnableToParseVersionString as error:
        raise UnableToParseVersionString(
            f"Error parsing version string: {error}"
        ) from error


def get_version_string(cmd: str, version_flag: str, exit_code: int) -> str:
    """
    Given the command and the flag for the version string (note the version string
    might be empty as in BWA), return a unicode string with the version string embedded
    in it.
    """
    cmd = [cmd, version_flag]
    chk_output = exit_code == 0
    try:
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=chk_output,
            encoding="utf-8",
        )
        if len(process.stdout) > 0:
            return process.stdout
        if len(process.stderr) > 0:
            return process.stderr
        raise UnableToGenerateVersionOutputString(
            f"Invalid output with command {' '.join(cmd)}"
        )

    except subprocess.CalledProcessError as error:
        raise error


def verify_from_config(config: pathlib.Path):
    """
    Based on a YAML config file with the following entries (one per tool):
    - name: the name of the tool to verify (e.g., blastn)
        req_version: version string expected from the tool (e.g., >=1.2.3)
        version_flag: -version
        output: stderr
        exit_code: 0

    First step, parse the config into a dictionary. Next, for each tool, run the
    command to capture the version string. Then, verify that the version string
    meets the expectations of the expected version string.
    Args:
        config (pathlib.Path): the path to the YAML config file
    """

    with open(config, "r", encoding="utf8") as stream:
        config = yaml.safe_load(stream)

    for tool in config:
        version_string = get_version_string(
            tool["name"],
            tool["version_flag"],
            tool["exit_code"],
        )
        result, obs_version = verify(tool["req_version"], version_string)
        yield result, obs_version, tool["req_version"], tool["name"]
