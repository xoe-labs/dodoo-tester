#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is part of the click-odoo-tester (R) project.
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

# import click
from click.testing import CliRunner

from src.tester import main

# from click_odoo import odoo


# from ..utils import manifest, gitutils


def test_execute_crm_tests(odoodb, odoocfg):
    result = CliRunner().invoke(
        main,
        [
            "--config",
            odoocfg,
            "--database",
            odoodb,
            "--include",
            "crm",
            "--include",
            "project",
            "--exclude",
            "project",
        ],
    )
    assert result.exit_code == 0
