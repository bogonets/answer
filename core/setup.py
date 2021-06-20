# -*- coding: utf-8 -*-

import os
import re
import sys
import codecs

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from Cython.Build import cythonize


SOURCE_PATH = os.path.abspath(__file__)
SOURCE_DIR = os.path.dirname(SOURCE_PATH)
RECC_DIR = os.path.join(SOURCE_DIR, "recc")
README_PATH = os.path.join(SOURCE_DIR, "README.md")
REQUIREMENTS_MAIN = os.path.join(SOURCE_DIR, "requirements.main.txt")
REQUIREMENTS_DOCS = os.path.join(SOURCE_DIR, "requirements.docs.txt")
REQUIREMENTS_TEST = os.path.join(SOURCE_DIR, "requirements.test.txt")
REQUIREMENTS_SETUP = os.path.join(SOURCE_DIR, "requirements.setup.txt")

SOURCE_FILTERS = (
    re.compile(r".*__init__\.py$"),
    re.compile(r".*__main__\.py$"),
)

# Ensure we're in the proper directory whether or not we're being used by pip.
os.chdir(SOURCE_DIR)

from recc.util.version import normalize_version, version_text  # noqa


def ignore_filter(sources, filters=SOURCE_FILTERS):
    result = sources
    for f in filters:
        result = list(filter(lambda x: f.match(x) is None, result))
    return result


def is_match_filter(source, filters=SOURCE_FILTERS):
    for f in filters:
        if f.match(source) is not None:
            return True
    return False


def get_children(path):
    result = []
    for parent, _, files in os.walk(path):
        for name in files:
            result.append(os.path.join(parent, name))
    return result


def get_children_with_match(path, regexp=".*"):
    result = []
    for cursor in get_children(path):
        if re.match(regexp, cursor) is not None:
            result.append(cursor)
    return result


def read_file(path, encoding="utf-8"):
    with codecs.open(filename=path, encoding=encoding) as f:
        return f.read()


def find_fist_positional_argument(args):
    # args[0] is script
    for a in args[1:]:
        if a[0] != "-":
            return a


def is_bdist_wheel():
    return find_fist_positional_argument(sys.argv) == "bdist_wheel"


class NoPythonBuildPy(build_py):
    def find_package_modules(self, package, package_dir):
        # ext_suffix = sysconfig.get_config_var("EXT_SUFFIX")
        modules = super().find_package_modules(package, package_dir)
        filtered_modules = []
        for pkg, mod, filepath in modules:
            if is_match_filter(filepath):
                filtered_modules.append((pkg, mod, filepath))
        return filtered_modules


def setup_main():
    long_description = read_file(README_PATH)
    install_requires = read_file(REQUIREMENTS_MAIN).split("\n")
    tests_require = read_file(REQUIREMENTS_TEST).split("\n")
    setup_requires = read_file(REQUIREMENTS_SETUP).split("\n")

    files = get_children_with_match(path=RECC_DIR, regexp=r".*\.py$")
    files = ignore_filter(files)

    compiler_directives = {"language_level": 3}
    cython_modules = cythonize(
        module_list=files, compiler_directives=compiler_directives,
    )
    for ext in cython_modules:
        ext.extra_compile_args = ["-g0"]

    setup_config = {
        "name": "recc",
        "version": normalize_version(version_text),
        "description": "A Python library for the Docker Engine API.",
        "long_description": long_description,
        "long_description_content_type": "text/markdown",
        "url": "https://answerdoc.bogonets.com",
        "project_urls": {
            "Documentation": "https://answerdoc.bogonets.com",
            "Source": "https://github.com/bogonets",
        },
        "packages": find_packages(where=SOURCE_DIR, exclude=("test",)),
        "package_dir": {"recc": "recc"},
        "package_data": {"recc": ["node/*.json"]},
        "install_requires": install_requires,
        "setup_requires": setup_requires,
        "python_requires": ">=3.7",
        "zip_safe": False,
        "test_suite": "test",
        "tests_require": tests_require,
        "classifiers": [
            "Development Status :: 4 - Beta",
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Topic :: Software Development",
            "Topic :: Utilities",
            "Topic :: Internet :: WWW/HTTP",
        ],
        "entry_points": {
            "console_scripts": [
                "recc = recc.app.entrypoint:main",
            ]
        },
        "maintainer": "zer0",
        "maintainer_email": "osom8979@gmail.com",
    }

    if is_bdist_wheel():
        setup_config["ext_modules"] = cython_modules
        setup_config["cmdclass"] = {"build_py": NoPythonBuildPy}

    setup(**setup_config)


if __name__ == "__main__":
    setup_main()
