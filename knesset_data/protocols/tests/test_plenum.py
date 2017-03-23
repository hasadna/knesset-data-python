# -*- coding: utf-8 -*-
import unittest
from knesset_data.protocols.plenum import PlenumProtocolFile
from datetime import datetime
import os


# this function is used by test_base to test the base protocol functionality
def plenum_protocol_assertions(test_case, protocol):
    test_case.assertEqual(protocol.knesset_num_heb, 'עשרים')
    test_case.assertEqual(protocol.meeting_num_heb, 'שמונים')
    test_case.assertEqual(protocol.booklet_num_heb, 'י"א')
    test_case.assertEqual(protocol.booklet_meeting_num_heb, "פ'")
    test_case.assertEqual(protocol.date_string_heb, ('23', 'דצמבר', '2015'))
    test_case.assertEqual(protocol.time_string, ('11', '00'))
    test_case.assertEqual(protocol.datetime, datetime(2015, 12, 23, 11, 0))
    test_case.assertEqual(protocol.knesset_num, 20)
    test_case.assertEqual(protocol.booklet_num, 11)
    test_case.assertEqual(protocol.booklet_meeting_num, 80)


class TestPlenumProtocolFile(unittest.TestCase):
    maxDiff = None

    def test_from_file(self):
        with PlenumProtocolFile.get_from_filename(os.path.join(os.path.dirname(__file__), '20_ptm_318579.doc')) as protocol:
            plenum_protocol_assertions(self, protocol)

    def _get_protocol_data(self, protocol, keys):
        res = {}
        for k in keys:
            try:
                res[k] = getattr(protocol, k)
            except Exception, e:
                res[k] = e.message
        return res

    def test_from_data(self):
        data = open(os.path.join(os.path.dirname(__file__), '20_ptm_381742.doc')).read()
        with PlenumProtocolFile.get_from_data(data) as protocol:
            expected_data = {'knesset_num_heb': 'עשרים',
                             'meeting_num_heb': 'מאתיים-ותשע-עשרה',
                             "booklet_num_heb": None,
                             'booklet_meeting_num_heb': 'רי"ט',
                             'date_string_heb': ('21', 'מרס', '2017'),
                             'time_string': ('16', '00'),
                             'datetime': datetime(2017, 3, 21, 16, 0),
                             "knesset_num": 20,
                             'booklet_num': "'NoneType' object has no attribute 'decode'",
                             "booklet_meeting_num": 219}
            actual_data = self._get_protocol_data(protocol, expected_data)
            self.assertEqual(actual_data, expected_data)
