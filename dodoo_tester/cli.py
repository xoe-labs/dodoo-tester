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

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
from builtins import str

import click
import dodoo
import pytest as pytest_orig
from future import standard_library

from .commands import CommandWithOdooEnvExtended
from .env import OdooPyTestExecution, OdooTestExecution
from .pytest import OdooPlugin

standard_library.install_aliases()


# from utils import manifest, gitutils

_logger = logging.getLogger(__name__)


@click.command(
    cls=CommandWithOdooEnvExtended,
    env_options={
        "database_must_exist": False,
        "environment_manager": OdooTestExecution,
    },
)
@dodoo.options.addons_path_opt(True)
@dodoo.options.db_opt(True)
@click.option(
    "--git-dir",
    default=(None, None),
    nargs=2,
    type=(click.Path(), str),
    help="Autodetect changed modules (through git).",
)
@click.option("--include", "-i", multiple=True, help="Force test run on those modules.")
@click.option(
    "--exclude",
    "-e",
    multiple=True,
    help="Force excluding those modules from tests. Even if "
    "a change has been detected.",
)
@click.option("--tags", "-t", multiple=True, help="Filter on those test tags.")
def test(env, git_dir, include, exclude, tags):
    """ Run Odoo tests through unittest.
    """
    pass


@click.command(
    cls=dodoo.commands.CommandWithOdooEnv,
    env_options={
        "database_must_exist": True,
        "environment_manager": OdooPyTestExecution,
    },
)
@dodoo.options.addons_path_opt(True)
@dodoo.options.db_opt(True)
@click.argument("args", nargs=-1, required=True)
def pytest(env, args):
    """ Run Odoo tests through pytest.
    """
    pytest_orig.main(list(args), plugins=[OdooPlugin()])


if __name__ == "__main__":  # pragma: no cover
    test()
