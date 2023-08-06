from __future__ import annotations

import itertools as it
import os
from configparser import ConfigParser
from pathlib import Path


def load_config(path=None) -> dict:
    """
    Parse config file.
    Parameters may be overridden by ``SQLTRACK_DSN_<PARAM>`` environment variables.
    Path defaults to ``./sqltrack.conf``.
    """
    path = Path(path if path is not None else "sqltrack.conf")
    parser = ConfigParser()
    # parse config file, if it exists
    if path.exists():
        with open(path, encoding='UTF-8') as fp:
            parser.read_file(it.chain(("[DEFAULT]",), fp))
    config = dict(parser["DEFAULT"])
    # check environment for overrides
    for k, v in os.environ.items():
        if k.startswith("SQLTRACK_DSN_"):
            _, _, name = k.partition("SQLTRACK_DSN_")
            config[name.lower()] = v
    return config


def coalesce(*values) -> object:
    """
    Returns the first none-None value.
    """
    for v in values:
        if v is not None:
            return v
    return None
