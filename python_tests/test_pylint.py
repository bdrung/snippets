# Copyright (C) 2010, Stefano Rivera <stefanor@debian.org>
# Copyright (C) 2017, Benjamin Drung <bdrung@debian.org>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

"""test_pylint.py - Run pylint"""

import os
import re
import subprocess
import sys
import unittest

from . import get_source_files, unittest_verbosity

CONFIG = os.path.join(os.path.dirname(__file__), 'pylint.conf')


class PylintTestCase(unittest.TestCase):
    def test_pylint(self):
        """Test: Run pylint on Python source code"""

        if sys.version_info[0] == 3:
            pylint_binary = 'pylint3'
        else:
            pylint_binary = 'pylint'
        cmd = [pylint_binary, '--rcfile=' + CONFIG, '--'] + get_source_files()
        if unittest_verbosity() >= 2:
            sys.stderr.write("Running following command:\n{}\n".format(" ".join(cmd)))
        process = subprocess.Popen(cmd, env={'PYLINTHOME': '.pylint.d'}, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, close_fds=True)
        out, err = process.communicate()

        # Strip trailing summary (introduced in pylint 1.7). This summary might look like:
        #
        # ------------------------------------
        # Your code has been rated at 10.00/10
        #
        out = re.sub('^(-+|Your code has been rated at .*)$', '', out.decode(),
                     flags=re.MULTILINE).rstrip()

        self.assertEqual(len(err), 0, pylint_binary + ' crashed. Error output:\n' + err.decode())
        self.assertEqual(len(out), 0, pylint_binary + " found issues:\n" + out)
