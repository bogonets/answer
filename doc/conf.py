# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

from recc.util.version import version_text

SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
STATIC_DIR = os.path.join(SCRIPT_DIR, "_static")
LOCALE_DIR = os.path.join(SCRIPT_DIR, "_locale")
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "_templates")
EXTENSIONS_DIR = os.path.join(SCRIPT_DIR, '_extensions')

sys.path.insert(0, EXTENSIONS_DIR)


# Project information

project = "answer"
copyright = "2021, BOGONET"  # noqa
author = "zer0"
version = version_text

# General configuration

extensions = [
    "sphinx.ext.autodoc",
    "recommonmark",
    "furo",
    "google_analytics",
]
source_suffix = [".rst", ".md"]
source_encoding = "utf-8"
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".tox"]
templates_path = [TEMPLATES_DIR]
language = "ko"

# HTML Output
html_theme = "furo"
html_static_path = [STATIC_DIR]

# Locale
locale_dirs = [LOCALE_DIR]
gettext_compact = False

# Google Analytics
google_analytics_enabled = True
google_analytics_id = "UA-162764112-2"
