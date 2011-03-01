
import json
import os
import unittest

from nose.tools import eq_
from validator.validate import validate

def _validator(file_path):
    # TODO(Kumar) This is currently copied from Zamboni because
    # it's really hard to import from zamboni outside of itself.
    # TODO(Kumar) remove this when validator is fixed, see bug 620503
    from validator.testcases import scripting
    js = 'js'
    scripting.SPIDERMONKEY_INSTALLATION = js
    import validator.constants
    validator.constants.SPIDERMONKEY_INSTALLATION = js
    apps = os.path.join(os.path.dirname(__file__), 'apps.json')
    return validate(file_path, format='json',
                    # This flag says to stop testing after one tier fails.
                    # bug 615426
                    determined=False,
                    approved_applications=apps,
                    spidermonkey=js)


class TestValidation(unittest.TestCase):

    def msg_set(self, d):
        return sorted(set([m['message'] for m in d['messages']]))

    def validate(self, xpi):
        path = os.path.join(os.path.dirname(__file__), 'addons', xpi)
        return json.loads(_validator(path))

    def test_createelement__used(self):
        """createElement() used to create script tag. The createElement()
        function was used to create a script tag in a JavaScript file.
        Add-ons are not allowed to create script tags or load code
        dynamically from the web.
        """
        d = self.validate('glee-20101227219.xpi')
        msg = self.msg_set(d)
        found = False
        for m in msg:
            if m.startswith('createElement() used to create script tag'):
                found = True
        assert found, ('Unexpected: %r' % msg)

    def test_dangerous_global(self):
        """Dangerous Global Object"""
        d = self.validate('feedly-addon-201101111013.xpi')
        msg = self.msg_set(d)
        assert u'Dangerous Global Object' in msg, ('Unexpected: %r' % msg)

    def test_global_called(self):
        """Global called in dangerous manner"""
        d = self.validate('babuji-20110124355.xpi')
        msg = self.msg_set(d)
        assert u'Global called in dangerous manner' in msg, (
                                                    'Unexpected: %r' % msg)

    # def test_global_overwrite(self):
    #     """Global overwrite"""
    #     d = self.validate('add-on20110110356.xpi')
    #     eq_(d['errors'], 0)
    #     eq_(d['warnings'], 0)
    #     eq_(d['notices'], 0)
    #     eq_(sorted([m['message'] for m in d['messages']]),
    #         [])

    def test_invalid_control(self):
        """Invalid control character in JS file"""
        d = self.validate('amazonassist-201103011128.xpi')
        msg = self.msg_set(d)
        assert u'Invalid control character in JS file' in msg, (
                                                    'Unexpected: %r' % msg)

    def test_javascript_syntax(self):
        """JavaScript Syntax Error"""
        d = self.validate('stumbleupon-3.76-fx+sm+mz.xpi')
        msg = self.msg_set(d)
        assert u'JavaScript Syntax Error' in msg, ('Unexpected: %r' % msg)

    def test_potentially_malicious(self):
        """Potentially malicious JS"""
        d = self.validate('add-on201101101027.xpi')
        msg = self.msg_set(d)
        assert u'Potentially malicious JS' in msg, ('Unexpected: %r' % msg)

    def test_variable_element(self):
        """Variable element type being created"""
        d = self.validate('glee-20101227219.xpi')
        msg = self.msg_set(d)
        assert u'Variable element type being created' in msg, (
            'Unexpected: %r' % msg)
