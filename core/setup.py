# -*- coding: utf-8 -*-

import os
from typing import List
from setuptools import setup, find_packages

SOURCE_PATH = os.path.abspath(__file__)
SOURCE_DIR = os.path.dirname(SOURCE_PATH)
RECC_DIR = os.path.join(SOURCE_DIR, "recc")
README_PATH = os.path.join(SOURCE_DIR, "README.md")
REQUIREMENTS_MAIN = os.path.join(SOURCE_DIR, "requirements.main.txt")
REQUIREMENTS_DOCS = os.path.join(SOURCE_DIR, "requirements.docs.txt")
REQUIREMENTS_TEST = os.path.join(SOURCE_DIR, "requirements.test.txt")
REQUIREMENTS_SETUP = os.path.join(SOURCE_DIR, "requirements.setup.txt")

# Ensure we're in the proper directory whether or not we're being used by pip.
os.chdir(SOURCE_DIR)

from recc.util.version import normalize_version, version_text  # noqa


def read_file(path, encoding="utf-8") -> str:
    with open(path, encoding=encoding) as f:
        return f.read()


def read_packages(path, encoding="utf-8") -> List[str]:
    content = read_file(path, encoding)
    lines = content.split("\n")
    lines = map(lambda x: x.strip(), lines)
    lines = filter(lambda x: x and x[0] != "#", lines)
    return list(lines)


def setup_main():
    long_description = read_file(README_PATH)
    install_requires = read_packages(REQUIREMENTS_MAIN)
    tests_require = read_packages(REQUIREMENTS_TEST)
    setup_requires = read_packages(REQUIREMENTS_SETUP)
    version = normalize_version(version_text)
    packages = find_packages(where=SOURCE_DIR, exclude=("tester*",))

    setup_config = {
        "name": "recc",
        "version": version,
        "description": "The Answer, No-Code Development Platform.",
        "long_description": long_description,
        "long_description_content_type": "text/markdown",
        "license": "MIT License",
        "keywords": [
            "Answer",
            "No-code",
            "Visual Graph",
            "Visual Programming",
            "Machine Learning",
            "Deep Learning",
        ],
        "url": "https://answerdoc.bogonets.com",
        "project_urls": {
            "Documentation": "https://answerdoc.bogonets.com",
            "Source": "https://github.com/bogonets/answer",
        },
        "packages": packages,
        "package_dir": {"recc": "recc"},
        "include_package_data": True,
        "install_requires": install_requires,
        "setup_requires": setup_requires,
        "python_requires": ">=3.8",
        "zip_safe": False,
        "test_suite": "test",
        "tests_require": tests_require,
        "classifiers": [
            "Development Status :: 4 - Beta",
            "Environment :: Web Environment",
            "Environment :: GPU :: NVIDIA CUDA",
            "Framework :: AsyncIO",
            "Intended Audience :: Developers",
            "Intended Audience :: System Administrators",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: JavaScript",
            "Topic :: Scientific/Engineering :: Image Processing",
            "Topic :: Scientific/Engineering :: Image Recognition",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Scientific/Engineering :: Visualization",
            "Topic :: Software Development",
            "Topic :: Utilities",
            "Topic :: Internet :: WWW/HTTP",
            "License :: OSI Approved :: MIT License",
        ],
        "entry_points": {
            "console_scripts": [
                "recc = recc.app.entrypoint:main",
            ]
        },
        "author": "zer0",
        "author_email": "osom8979@gmail.com",
        "maintainer": "zer0",
        "maintainer_email": "osom8979@gmail.com",
    }

    setup(**setup_config)


if __name__ == "__main__":
    setup_main()
