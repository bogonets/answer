# -*- coding: utf-8 -*-

import os
from typing import Tuple
from configparser import ConfigParser

PYVENV_CFG_FILENAME = "pyvenv.cfg"
CFG_KEY_HOME = "home"
CFG_KEY_INCLUDE_SYSTEM = "include-system-site-packages"
CFG_KEY_VERSION = "version"

_FAKE_SECTION_NAME = "default"
_FAKE_DEFAULT_SECTION = f"[{_FAKE_SECTION_NAME}]"


class PyvenvCfg:

    home: str
    include_system_site_packages: bool
    version: str

    def to_version_tuple(self) -> Tuple[int, ...]:
        return tuple([int(d) for d in self.version.split("-")[0].split(".")])


def exists_pyvenv_cfg(env_root: str) -> bool:
    return os.path.exists(os.path.join(env_root, PYVENV_CFG_FILENAME))


def read_pyvenv_cfg(env_root: str) -> PyvenvCfg:
    if not env_root:
        raise ValueError("Empty argument")

    cfg_path = os.path.join(env_root, PYVENV_CFG_FILENAME)
    if not os.path.isfile(cfg_path):
        raise FileNotFoundError(f"Not found '{cfg_path}' file")
    if not os.access(cfg_path, os.R_OK):
        raise PermissionError(f"Not readable '{cfg_path}' file")

    with open(cfg_path) as f:
        content = _FAKE_DEFAULT_SECTION + "\n" + f.read()

    parser = ConfigParser()
    parser.read_string(content, cfg_path)
    home = parser.get(_FAKE_SECTION_NAME, CFG_KEY_HOME)
    include_system = parser.getboolean(_FAKE_SECTION_NAME, CFG_KEY_INCLUDE_SYSTEM)
    version = parser.get(_FAKE_SECTION_NAME, CFG_KEY_VERSION)

    result = PyvenvCfg()
    result.home = home
    result.include_system_site_packages = include_system
    result.version = version
    return result


def read_site_packages_dir(env_root: str) -> str:
    cfg = read_pyvenv_cfg(env_root)
    versions = cfg.to_version_tuple()
    if len(versions) < 2:
        raise RuntimeError(f"Wrong python version: {versions}")
    major = versions[0]
    minor = versions[1]
    return os.path.join(env_root, "lib", f"python{major}.{minor}", "site-packages")
