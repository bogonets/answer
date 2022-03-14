# -*- coding: utf-8 -*-

import os
from sys import executable, version_info
from unittest import IsolatedAsyncioTestCase, main
from recc.subprocess.async_python_subprocess import AsyncPythonSubprocess
from recc.util.version import parse_version_numbers


class AsyncPythonSubprocessTestCase(IsolatedAsyncioTestCase):
    async def test_version_tuple(self):
        python = AsyncPythonSubprocess(executable)
        version = await python.version_tuple()
        self.assertEqual(version_info[:3], version)

    async def test_list(self):
        print("test_list cwd: ", os.getcwd())
        python = AsyncPythonSubprocess(executable)
        packages = await python.list()
        self.assertLess(0, len(packages))

    async def test_show(self):
        python = AsyncPythonSubprocess(executable)
        show = await python.show("numpy")
        self.assertLess(0, len(show))
        self.assertEqual("numpy", show["Name"])

    async def test_show_as_info(self):
        python = AsyncPythonSubprocess(executable)
        show = await python.show_as_info("numpy")
        self.assertEqual("numpy", show.name)
        self.assertLessEqual((1, 22, 2), parse_version_numbers(show.version))
        summary = "NumPy is the fundamental package for array computing with Python."
        self.assertEqual(summary, show.summary)
        self.assertEqual("https://www.numpy.org", show.homepage)
        self.assertEqual("Travis E. Oliphant et al.", show.author)
        self.assertEqual("", show.author_email)
        self.assertEqual("BSD", show.license)
        self.assertTrue(os.path.isdir(show.location))
        self.assertEqual(0, len(show.requires))
        self.assertLess(0, len(show.required_by))


if __name__ == "__main__":
    main()
