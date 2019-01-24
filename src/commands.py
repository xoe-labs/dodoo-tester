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

import os
from builtins import super

import click
from dodoo import CommandWithOdooEnv, odoo

from .git import Git


def _get_changed_modules_from_git(git_dir, base_ref="origin/master"):
    """ Returns odoo changed odoo modules as per git diff-index.
    :param base_ref: branch or remote/branch or sha to compare
    :return: List of unique modules changed """

    changed_paths = Git(git_dir).get_changed_paths(base_ref)
    res = []
    for path in changed_paths:
        module_root = odoo.modules.module.get_module_root(path)
        if not module_root:
            continue
        res.append(os.path.basename(module_root))
    return set(res)


class CommandWithOdooEnvExtended(CommandWithOdooEnv):
    def _parse_env_args(self, ctx):
        def _get(flag):
            return ctx.params.get(flag)

        database = _get("database")
        if not database:
            click.BadParameter(
                "The --database parameter is required for testing. You cannot "
                "specify the database in the config file."
            )
        odoo_args = super(CommandWithOdooEnvExtended, self)._parse_env_args(ctx)

        # fmt: off
        # Always present params
        git_dir, ref = _get("git_dir")       # noqa
        include      = _get("include")       # noqa
        exclude      = _get("exclude")       # noqa
        tags         = _get("tags")          # noqa
        # fmt: on

        if tags:
            odoo_args.extend(["--test-tags", tags])
        odoo_args.extend(["--log-db", database])
        odoo_args.extend(["--log-db-level", "warning"])

        changed = _get_changed_modules_from_git(git_dir, ref) if git_dir else set()
        modules = (changed | set(include)) - set(exclude)

        if not modules:
            click.echo("No module to test. Exiting...")
            click.get_current_context().exit()
        odoo_args.extend(["-i", ",".join(modules)])
        odoo_args.extend(["-u", ",".join(modules)])
        odoo_args.extend(["--test-enable"])
        return odoo_args
