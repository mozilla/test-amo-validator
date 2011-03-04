import glob
import os
import site
import sys


class conf:
    done = False


def rel(path):
    return os.path.join(os.path.dirname(__file__), path)


def setup():
    if conf.done:
        return
    site.addsitedir(rel('zamboni/apps'))
    site.addsitedir(rel('zamboni-lib/lib'))
    site.addsitedir(rel('zamboni'))
    site.addsitedir(rel('zamboni-lib/lib'))

    sys.path.append(rel('zamboni/lib'))
    sys.path.append(rel('zamboni-lib/lib/python'))

    for spec in [rel('zamboni/apps/*'),
                 rel('zamboni-lib/src/*')]:
        for d in glob.glob(spec):
            sys.path.append(d)

    conf.done = True
