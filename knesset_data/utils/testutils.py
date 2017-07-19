import tempfile
import filecmp
import os
import unittest
import six

# solve issues with unicode for python3/2
if six.PY2:
    def decode(a, b):
        return a.decode(b)
    unicode = unicode
elif six.PY3:
    def decode(a, b):
        return a
    unicode = str


class TestCaseFileAssertionsMixin(object):

    def assertFileContents(self, expected_file_name, actual_content):
        with open(expected_file_name) as f:
            self.assertEqual(decode(f.read(),'utf-8').rstrip("\n"), actual_content.rstrip("\n"))


def data_dependant_test():
    return unittest.skip('test has hard dependency on spcecific data from Knesset, should be rewritten to be less fragile')
