# -*- coding: utf-8 -*-

from recc.driver.uvloop import install_uvloop_driver
from recc.util.version import version_text

install_uvloop_driver()

__version__ = version_text
