
import json
import os
import sys
import unittest
from cStringIO import StringIO

from nose.exc import SkipTest
from nose.tools import eq_
from validator.validate import validate

def _validator(file_path):
    # TODO(Kumar) This is currently copied from Zamboni because
    # it's really hard to import from zamboni outside of itself.
    # TODO(Kumar) remove this when validator is fixed, see bug 620503
    from validator.testcases import scripting
    import validator.constants
    js = os.environ.get('SPIDERMONKEY_INSTALLATION', 'js')
    scripting.SPIDERMONKEY_INSTALLATION = js
    validator.constants.SPIDERMONKEY_INSTALLATION = js
    apps = os.path.join(os.path.dirname(__file__), 'apps.json')
    orig = sys.stderr
    sys.stderr = StringIO()
    try:
        result = validate(file_path, format='json',
                        # Test all tiers at once. This will make sure we see
                        # all error messages.
                        determined=True,
                        approved_applications=apps,
                        spidermonkey=js)
        sys.stdout.write(sys.stderr.getvalue())
        if 'Traceback' in sys.stderr.getvalue():
            # the validator catches and ignores certain errors in an attempt
            # to remain versatile.  There should not be any exceptions
            # while testing.
            raise RuntimeError(
                "An exception was raised during validation. Check stderr")
    finally:
        sys.stderr = orig
    return result


_cached_validation = {}


class ValidatorTest(unittest.TestCase):

    def msg_set(self, d):
        return sorted(set([m['message'] for m in d['messages']]))

    def validate(self, xpi):
        path = os.path.join(os.path.dirname(__file__), 'addons', xpi)
        if path in _cached_validation:
            return _cached_validation[path]
        v = json.loads(_validator(path))
        _cached_validation[path] = v
        return v

    def assertPartialMsg(self, msgs, partial_msg):
        found = False
        for m in msgs:
            if m.startswith(partial_msg):
                found = True
        assert found, ('Unexpected: %r' % msgs)


class JavaScriptTests(ValidatorTest):

    def test_createelement__used(self):
        """createElement() used to create script tag. The createElement()
        function was used to create a script tag in a JavaScript file.
        Add-ons are not allowed to create script tags or load code
        dynamically from the web.
        """
        d = self.validate('glee-20101227219.xpi')
        msg = self.msg_set(d)
        self.assertPartialMsg(msg, 'createElement() used to create script tag')

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
        assert u'JavaScript Compile-Time Error' in msg, (
                                                    'Unexpected: %r' % msg)

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


class GeneralTests(ValidatorTest):

    def test_contains_jar_files(self):
        """Add-on contains JAR files- no emUnpack"""
        d = self.validate('test-theme-3004.jar')
        msg = self.msg_set(d)
        assert u'Add-on contains JAR files, no <em:unpack>' in msg, (
            'Unexpected: %r' % msg)

    def test_potentially_illegal_name(self):
        """Add-on has potentially illegal name."""
        d = self.validate('add-on20110110322.xpi')
        msg = self.msg_set(d)
        assert u'Add-on has potentially illegal name.' in msg, (
            'Unexpected: %r' % msg)

    def test_banned_element(self):
        """Banned element in install"""
        d = self.validate('gabbielsan_tools-1.01-ff.xpi')
        msg = self.msg_set(d)
        assert u'Banned element in install.rdf' in msg, ('Unexpected: %r' % msg)

    def test_blacklisted_file(self):
        """Blacklisted file extensions found"""
        d = self.validate('babuji-20110124355.xpi')
        msg = self.msg_set(d)
        assert u'Flagged file extension found' in msg, (
                                            'Unexpected: %r' % msg)

    def test_blacklisted_file_2(self):
        """Blacklisted file type found"""
        d = self.validate('peerscape-3.1.5-fx.xpi')
        msg = self.msg_set(d)
        assert u'Flagged file type found' in msg, ('Unexpected: %r' % msg)

    def test_em_type_not(self):
        """em-type not found"""
        d = self.validate('babuji-20110124355.xpi')
        msg = self.msg_set(d)
        assert u'No <em:type> element found in install.rdf' in msg, (
                                            'Unexpected: %r' % msg)

    def test_obsolete_element(self):
        """Obsolete element in installRDF"""
        d = self.validate('gabbielsan_tools-1.01-ff.xpi')
        msg = self.msg_set(d)
        assert u'Banned element in install.rdf' in msg, ('Unexpected: %r' % msg)

    def test_unknown_file(self):
        """Unknown file found in add-on"""
        d = self.validate('gabbielsan_tools-1.01-ff.xpi')
        msg = self.msg_set(d)
        assert u'Unrecognized element in install.rdf' in msg, (
                                            'Unexpected: %r' % msg)

    def test_unrecognized_element(self):
        """Unrecognized element in install"""
        d = self.validate('littlemonkey-1.8.56-sm.xpi')
        msg = self.msg_set(d)
        assert u'Addon missing install.rdf.' in msg, ('Unexpected: %r' % msg)

    def test_invalid_id(self):
        """invalid id"""
        d = self.validate('add-ongoogle-201101121132.xpi')
        msg = self.msg_set(d)
        assert u'The value of <em:id> is invalid.' in msg, (
                                                'Unexpected: %r' % msg)

    def test_xpi_cannot(self):
        """XPI cannot be opened"""
        d = self.validate('lavafox_test-theme-20101130538.xpi')
        msg = self.msg_set(d)
        assert u'The XPI could not be opened.' in msg, (
                                                'Unexpected: %r' % msg)

    def test_invalid_version(self):
        d = self.validate('invalid maximum version number.xpi')
        msg = self.msg_set(d)
        assert u'Invalid maximum version number' in msg, (
                                                'Unexpected: %r' % msg)


class LocalizationTests(ValidatorTest):

    def test_translation(self):
        d = self.validate('babuji-20110124355.xpi')
        msg = self.msg_set(d)
        assert u'Unchanged translation entities' in msg, (
                                                'Unexpected: %r' % msg)

    def test_encodings(self):
        d = self.validate('babuji-20110124355.xpi')
        msg = self.msg_set(d)
        assert u'Unexpected encodings in locale files' in msg, (
                                                'Unexpected: %r' % msg)

    def test_missing_translation(self):
        """Missing Translation files"""
        d = self.validate('download_statusbar-0.9.7.2-fx (1).xpi')
        msg = self.msg_set(d)
        assert u'Missing translation entity' in msg, (
                                                'Unexpected: %r' % msg)


class SecurityTests(ValidatorTest):

    def test_missing_comments(self):
        """Missing comments in <script> tag"""
        d = self.validate('add-on-20110113408.xpi')
        msg = self.msg_set(d)
        assert u'Missing comments in <script> tag' in msg, (
                                                'Unexpected: %r' % msg)

    def test_typeless_iframes_browsers(self):
        """Typeless iframes:browsers must be local"""
        d = self.validate('add-on201101081038.xpi')
        msg = self.msg_set(d)
        assert u'Typeless iframes/browsers must be local.' in msg, (
                                                'Unexpected: %r' % msg)


class NoErrorsExpected(ValidatorTest):

    def test_an_attempt(self):
        """An attempt to overwrite a global varible [sic] made in some JS code"""
        d = self.validate('tmp.xpi')
        eq_(d['errors'], 0)

    def test_don_t_freak(self):
        """don't freak on UTF-8 chs in JS files """
        d = self.validate('test (1).xpi')
        eq_(d['errors'], 0)

    def test_don_t_freak_2(self):
        """don't freak out if install.js is missing"""
        d = self.validate('littlemonkey-1.8.56-sm.xpi')
        msg = self.msg_set(d)
        ok = True
        for m in msg:
            if 'install.js' in msg:
                ok = False
        assert ok, ('Unexpected: %r' % msg)

    def test_unknown_file(self):
        """Unknown file found in add-on"""
        d = self.validate('add-on20101228444 (1).jar')
        eq_(d['errors'], 0)


class SearchTools(ValidatorTest):

    def test_opensearch_providers(self):
        """OpenSearch providers cannot contain <Url :> ..."""
        d = self.validate('sms_search-20110115 .xml')
        msg = self.msg_set(d)
        self.assertPartialMsg(msg,
            'OpenSearch: Per AMO guidelines, OpenSearch providers '
            'cannot contain <Url />')

    def test_opensearch_shortname(self):
        """OpenSearch ShortName values longer than 16 characters"""
        d = self.validate('lexisone_citation_search-20100116 .xml')
        msg = self.msg_set(d)
        assert u'OpenSearch: <ShortName> too long; must be <17 characters' in msg, (
                                                'Unexpected: %r' % msg)

    def test_too_many(self):
        """Too many <ShortName> elements"""
        d = self.validate('addon-12201-latest.xml')
        msg = self.msg_set(d)
        assert u'OpenSearch: Too many <ShortName> elements' in msg, (
                                                'Unexpected: %r' % msg)
