
import json
import os
import unittest

from nose.tools import eq_
from validator.validate import validate

def _validator(file_path):
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

    def validate(self, xpi):
        path = os.path.join(os.path.dirname(__file__), 'addons', xpi)
        return json.loads(_validator(path))

    def test_createelement__used(self):
        """createElement() used to create script tagThe createElement()
        function was used to create a script tag in a JavaScript file.
        Add-ons are not allowed to create script tags or load code
        dynamically from the web.
        """
        d = self.validate('glee-20101227219.xpi')
        eq_(d['errors'], 0)
        eq_(d['warnings'], 36)
        eq_(d['notices'], 2)
        eq_(sorted([m['message'] for m in d['messages']]),
            [                u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Global Overwrite',
             u'Global Overwrite',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global overwrite',
             u'Global overwrite',
             u'Global overwrite',
             u'Global overwrite',
             u'Global overwrite',
             u'Markup parsing error',
             u'Obsolete element in install.rdf',
             u'Obsolete element in install.rdf',
             u'Potentially malicious JS',
             u'Variable element type being created',
             u'Variable element type being created',
             u'Variable element type being created',
             u'createElement() used to create script tagThe createElement() function was used to create a script tag in a JavaScript file. Add-ons are not allowed to create script tags or load code dynamically from the web.'])

    def test_dangerous_global(self):
        """Dangerous Global Object"""
        d = self.validate('feedly-addon-201101111013.xpi')
        eq_(d['errors'], 0)
        eq_(d['warnings'], 21)
        eq_(d['notices'], 0)
        eq_(sorted([m['message'] for m in d['messages']]),
            [                u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Global Overwrite',
             u'Global Overwrite',
             u'Global Overwrite',
             u'Global Overwrite',
             u'Global Overwrite',
             u'Global Overwrite',
             u'Global Overwrite',
             u'Global Overwrite',
             u'Global Overwrite',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global overwrite',
             u'Global overwrite',
             u'Global overwrite',
             u'Global overwrite',
             u'Potentially malicious JS',
             u'Potentially malicious JS'])

    def test_global_called(self):
        """Global called in dangerous manner"""
        d = self.validate('babuji-20110124355.xpi')
        eq_(d['errors'], 0)
        eq_(d['warnings'], 29)
        eq_(d['notices'], 1)
        eq_(sorted([m['message'] for m in d['messages']]),
            [                u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Blacklisted file extension found',
             u'Global Overwrite',
             u'Global Overwrite',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'No <em:type> element found in install.rdf',
             u'Unchanged translation entities',
             u'Unexpected encodings in L10n files'])

    def test_global_overwrite(self):
        """Global overwrite"""
        d = self.validate('add-on20110110356.xpi')
        eq_(d['errors'], 0)
        eq_(d['warnings'], 0)
        eq_(d['notices'], 0)
        eq_(sorted([m['message'] for m in d['messages']]),
            [])

    def test_invalid_control(self):
        """Invalid control character in JS file"""
        d = self.validate('amazonassist-201103011128.xpi')
        eq_(d['errors'], 0)
        eq_(d['warnings'], 30)
        eq_(d['notices'], 0)
        eq_(sorted([m['message'] for m in d['messages']]),
            [                u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file',
             u'Invalid control character in JS file'])

    def test_javascript_syntax(self):
        """JavaScript Syntax Error"""
        d = self.validate('stumbleupon-3.76-fx+sm+mz.xpi')
        eq_(d['errors'], 0)
        eq_(d['warnings'], 123)
        eq_(d['notices'], 4)
        eq_(sorted([m['message'] for m in d['messages']]),
            [                u'Add-on contains JAR files, no <em:unpack>',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Global Overwrite',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'JavaScript Syntax Error',
             u'No <em:type> element found in install.rdf',
             u'Obsolete element in install.rdf',
             u'Obsolete element in install.rdf',
             u'Potentially malicious JS',
             u'Potentially malicious JS',
             u'Typeless iframes/browsers must be local.',
             u'Unchanged translation entities'])

    def test_potentially_malicious(self):
        """Potentially malicious JS"""
        d = self.validate('add-on201101101027.xpi')
        eq_(d['errors'], 0)
        eq_(d['warnings'], 48)
        eq_(d['notices'], 1)
        eq_(sorted([m['message'] for m in d['messages']]),
            [                u'Add-on contains JAR files, no <em:unpack>',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Missing translation entity',
             u'Potentially malicious JS',
             u'Unchanged translation entities',
             u'Unchanged translation entities',
             u'Unchanged translation entities',
             u'Unchanged translation entities'])

    def test_variable_element(self):
        """Variable element type being created"""
        d = self.validate('glee-20101227219.xpi')
        eq_(d['errors'], 0)
        eq_(d['warnings'], 36)
        eq_(d['notices'], 2)
        eq_(sorted([m['message'] for m in d['messages']]),
            [                u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Dangerous Global Object',
             u'Global Overwrite',
             u'Global Overwrite',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global called in dangerous manner',
             u'Global overwrite',
             u'Global overwrite',
             u'Global overwrite',
             u'Global overwrite',
             u'Global overwrite',
             u'Markup parsing error',
             u'Obsolete element in install.rdf',
             u'Obsolete element in install.rdf',
             u'Potentially malicious JS',
             u'Variable element type being created',
             u'Variable element type being created',
             u'Variable element type being created',
             u'createElement() used to create script tagThe createElement() function was used to create a script tag in a JavaScript file. Add-ons are not allowed to create script tags or load code dynamically from the web.'])
