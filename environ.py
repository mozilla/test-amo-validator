import glob
import os
import site
import sys


class conf:
    done = False


def setup():
    if conf.done:
        return
    site.addsitedir('./zamboni/apps')
    site.addsitedir('./zamboni-lib/lib')
    site.addsitedir('./zamboni')
    site.addsitedir('./zamboni-lib/lib')

    sys.path.append('./zamboni/lib')
    sys.path.append('./zamboni-lib/lib/python')

    for spec in ['./zamboni/apps/*',
                 './zamboni-lib/src/*']:
        for d in glob.glob(spec):
            sys.path.append(d)

    conf.done = True
