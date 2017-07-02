# -*- coding: utf-8 -*
import unittest

from knesset_data.protocols.protocol_header_parser import ProtocolHeaderParser


class TestProtocolPartHeaderParser(unittest.TestCase):
    def test_parser_returns_parsed_header_with_contained_name(self):
        mk_person_map = {
            u'סתיו שפיר': 1,
            u'סתו שפיר': 1
        }
        header_text = u'סתיו שפיר ראש הועדה'
        parser = ProtocolHeaderParser(header_text, mk_person_map)
        result = parser.parse()
        self.assertEqual(result.text, header_text)
        self.assertEqual(result.speaker_id, 1)

    def test_parser_returns_parsed_header_with_reverse_name(self):
        mk_person_map = {
            u'סתיו שפיר': 1,
            u'סתו שפיר': 1
        }
        header_text = u'שפיר סתיו ראש הועדה'
        parser = ProtocolHeaderParser(header_text, mk_person_map)
        result = parser.parse()
        self.assertEqual(result.text, header_text)
        self.assertEqual(result.speaker_id, 1)

    def test_parser_tries_to_guess_name_based_on_small_difference_if_no_direct_match(self):
        mk_person_map = {
            u'סתיו שפיר': 1,
            u'סתו שפיר': 1
        }
        header_text = u'סתיו שפר ראש הועדה'
        parser = ProtocolHeaderParser(header_text, mk_person_map)
        result = parser.parse()
        self.assertEqual(result.text, header_text)
        self.assertEqual(result.speaker_id, 1)

    def test_parser_returns_none_speaker_id_if_does_not_found_match(self):
        mk_person_map = {
            u'סתיו שפיר': 1,
            u'סתו שפיר': 1
        }
        header_text = u'איתן כבל ראש הועדה'
        parser = ProtocolHeaderParser(header_text, mk_person_map)
        result = parser.parse()
        self.assertEqual(result.text, header_text)
        self.assertEqual(result.speaker_id, None)


