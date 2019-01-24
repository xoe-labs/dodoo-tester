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

import subprocess
from builtins import str


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
