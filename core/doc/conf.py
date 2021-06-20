# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
from recc.util.version import version_text


SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
STATIC_DIR = os.path.join(SCRIPT_DIR, "static")
SOURCE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))

# Project information

project = "recc"
author = "zer0"
version = version_text

# General configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
]
source_suffix = [".rst"]
source_encoding = "utf-8"
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".tox"]
templates_path = ["_templates"]
language = "ko"

# HTML Output

html_theme = "sphinx_rtd_theme"
if os.path.isdir(STATIC_DIR):
    html_static_path = [STATIC_DIR]
