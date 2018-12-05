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
import os
import subprocess
from builtins import str, super
from contextlib import closing, contextmanager

import click
import psycopg2
from click_odoo import CommandWithOdooEnv, odoo
from future import standard_library

from .format import process

standard_library.install_aliases()


# from utils import manifest, gitutils

_logger = logging.getLogger(__name__)


class Git(object):
    def __init__(self, git_dir):
        self.git_dir = git_dir

    def run(self, command):
        """Execute git command in bash
        :param list command: Git cmd to execute in self.git_dir
        :return: String output of command executed.
        """
        cmd = ["git", "--git-dir=" + self.git_dir] + command
        try:
            res = subprocess.check_output(cmd)
        except subprocess.CalledProcessError:
            res = None
        # Python 2.7
        if isinstance(res, str):
            res = res.strip("\n")
        # Python 3.X
        if isinstance(res, bytes):
            res = res.strip(b"\n")
        return res

    def fetch_remote(self, ref):
        """ Fetches a remote ref, independent of current refspec config """
        if "/" not in ref:
            return
        parts = ref.split("/", 1)
        remote = parts[0]
        ref_branch = parts[1]
        refmap_option = "--refmap=+refs/heads/{ref_branch}:"
        "refs/remotes/{remote}/{ref_branch}".format(**locals())
        self.run(["fetch", refmap_option] + parts)

    def get_changed_paths(self, base_ref="HEAD"):
        """Get name of items changed in self.git_dir
        This is a wrapper method of git command:
            git diff-index --name-only --cached {base_ref}
        :param base_ref: String of branch or sha base.
            e.g. "master" or "SHA_NUMBER"
        :return: List of name of items changed
        """
        self.fetch_remote(base_ref)
        command = ["diff-index", "--name-only", "--cached", base_ref]
        res = self.run(command)
        items = res.decode("UTF-8").split("\n") if res else []
        return items

    def get_branch_name(self):
        """Get branch name
        :return: String with name of current branch name"""
        command = ["rev-parse", "--abbrev-ref", "HEAD"]
        res = self.run(command)
        return res


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


@contextmanager
def OdooTestExecution(self):
    try:
        yield odoo.service.server.start(preload=[self.database], stop=True)
    finally:
        with closing(
            psycopg2.connect(dbname=self.database)
        ) as conn, conn.cursor() as cr:
            cr.execute(
                """SELECT name, level, message, path, func, line
                          FROM ir_logging"""
            )
            logs = cr.fetchall()
            # PostgreSQL 9.2 renamed pg_stat_activity.procpid to pid:
            # http://www.postgresql.org/docs/9.2/static/release-9-2.html#AEN110389
            pid_col = "pid" if conn.server_version >= 90200 else "procpid"

            cr.execute(
                """
                SELECT pg_terminate_backend(%(pid_col)s)
                FROM pg_stat_activity
                WHERE datname = %%s
                AND %(pid_col)s != pg_backend_pid()"""
                % {"pid_col": pid_col},
                (self.database,),
            )

    ctx = click.get_current_context()
    success = process(logs)
    if not success:
        ctx.fail("Tests failed")


@click.command(
    cls=CommandWithOdooEnvExtended,
    env_options={
        "with_rollback": False,
        "database_required": True,
        "database_must_exist": False,
        "environment_manager": OdooTestExecution,
    },
    default_overrides={"log_level": "warn"},
)
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
def main(env, git_dir, include, exclude, tags):
    """ Run Odoo tests through modern pytest instead of unittest.
    """
    pass


if __name__ == "__main__":  # pragma: no cover
    main()
