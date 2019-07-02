#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is part of the dodoo-tester (R) project.
# Copyright (c) 2018 XOE Corp. SAS
# Authors: David Arnold, et al.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, see <http://www.gnu.org/licenses/>.
#

# import mock
from __future__ import absolute_import, division, print_function, unicode_literals

import os

from click.testing import CliRunner
from dodoo import odoo
from future import standard_library

from dodoo_tester.cli import pytest, test

standard_library.install_aliases()


# from dodoo import odoo


# from ..utils import manifest, gitutils


def test_execute_crm_tests(odoodb, odoocfg):
    result = CliRunner().invoke(
        test,
        [
            "--config",
            str(odoocfg),
            "--database",
            str(odoodb),
            "--include",
            "crm",
            "--include",
            "project",
            "--exclude",
            "project",
        ],
    )
    assert result.exit_code == 0


def test_execute_pytest(odoodb, odoocfg):

    testfile_path = os.path.join(
        odoo.__path__[0], "addons", "base", "tests", "test_expression.py"
    )
    result = CliRunner().invoke(
        pytest, ["--config", str(odoocfg), "--database", str(odoodb), testfile_path]
    )
    assert result.exit_code == 0
