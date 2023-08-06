# -*- coding: utf-8 -*-

"""

test_core_module

Unit test the core module

Copyright (C) 2023 Rainer Schwarzbach

This file is part of sabemos.

sabemos is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

sabemos is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import re

from unittest import TestCase

import sabemos


class CoreModule(TestCase):

    """Core module tests"""

    def test_version(self):
        """Test if the module version matches a SemVer subset"""
        self.assertTrue(
            bool(
                re.match(
                    r"\A\d+(?:\.\d+)+(?:-(?:alpha|beta|rc)\d+)?\Z",
                    sabemos.__version__,
                )
            )
        )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
