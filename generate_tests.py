"""wee! Code generation.

FIXME: use templates, duh.
"""

import json
import pprint
import optparse
import os
import re
import sys

import environ
environ.setup()


nonchar = re.compile(r'[^a-zA-Z0-9]+')


class gen:
    cnt = 2
    fn = set()


def uniq(n):
    if n in gen.fn:
        n = "%s_%s" % (n, gen.cnt)
        gen.cnt += 1
    gen.fn.add(n)
    return n


def main():
    p = optparse.OptionParser(usage='%prog addon_dir')
    (options, args) = p.parse_args()
    if len(args) != 1:
        p.error('incorrect args')
    addon_dir = args[0]
    from test_validator import _validator
    code = []
    for name in os.listdir(addon_dir):
        if name.startswith('.'):
            continue
        path = os.path.join(addon_dir, name)
        short = '_'.join([nonchar.sub('_', f).lower()
                          for f in name.split()[0:2]])
        xpi = [os.path.join(path, x) for x in os.listdir(path)
               if not x.startswith('.')]
        assert len(xpi) == 1, 'Unexpected: %r' % xpi
        xpi = xpi[0]
        res = json.loads(_validator(xpi))
        code.extend(["",
                     "    def test_%s(self):" % uniq(short),
                     '        """%s"""' % name,
                     "        d = self.validate(%r)" % os.path.basename(xpi),
                     "        eq_(d['errors'], %d)" % res['errors'],
                     "        eq_(d['warnings'], %d)" % res['warnings'],
                     "        eq_(d['notices'], %d)" % res['notices'],
                     "        eq_(sorted([m['message'] for m in d['messages']]),",
                     "            %s)" % pprint.pformat(list(sorted(
                                            [m['message'] for m in
                                             res['messages']])), indent=17)])
    print "\n".join(code)


if __name__ == '__main__':
    main()
