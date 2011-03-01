#!/usr/bin/env python
import os
import sys

import environ
environ.setup()

import nose
from nose.plugins import Plugin
from nosenicedots.plugin import NiceDots

class Environ(Plugin):
    enabled = True

    def options(self, parser, env):
        """Register commandline options.
        """

    def configure(self, options, conf):
        """Configure plugin.
        """

    def wantDirectory(self, dir):
        if dir.endswith('zamboni') or dir.endswith('zamboni-lib'):
            return False

if __name__ == '__main__':
    args = list(sys.argv)
    args.extend(['--with-nicedots'])
    nose.main(argv=args, plugins=[Environ(), NiceDots()])
