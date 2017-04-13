import unittest
import datetime
from ...mocks import MockCommitteeMeeting
from ...committees import CommitteeMeeting
from collections import OrderedDict
from ....utils.testutils import env_conditional_mock


CommitteeMeeting = env_conditional_mock(CommitteeMeeting, MockCommitteeMeeting)


class TestCommitteeMeetings(unittest.TestCase):

    def _get_meetings(self, committee_id, datetime_from, datetime_to):
        # the knesset dataservice allows to get meetings only using a function with these parameters
        # see https://github.com/hasadna/knesset-data/issues/25
        return CommitteeMeeting.get(committee_id, datetime_from, datetime_to)

    def test_committee_meeting(self):
        meetings = list(self._get_meetings(1, datetime.datetime(2016, 1, 1), datetime.datetime(2016, 1, 5)))
        self.assertTrue(isinstance(meetings[0].datetime, datetime))
        # for more details about the available data see knesset_data/dataservice/committees.py
        # TODO: add assertion here for each relevant field

    def test_protocol(self):
        meetings = list(self._get_meetings(1, datetime.datetime(2016, 2, 16), datetime.datetime(2016, 2, 17)))
        # because parsing the protocol requires heavy IO and processing - we provide it as a generator
        # also, we need to ensure temp files are deleted
        with meetings[0].protocol as protocol:
            # see knesset_data/protocols/tests/test_committee.py for example of getting more data from the protocol
            self.assertEqual(len(protocol.text), 48915)

    def test_table_schema(self):
        meeting = next(self._get_meetings(1, datetime.datetime(2016, 2, 16), datetime.datetime(2016, 2, 17)))
        self.assertEqual(meeting.all_schema_field_values(),
                         OrderedDict([('id', 576286),
                                      ('committee_id', 1),
                                      ('datetime', datetime.datetime(2016, 2, 16, 12, 30)),
                                      ('title', u'1. \u05d4\u05e6\u05e2\u05d4 \u05dc\u05ea\u05d9\u05e7\u05d5\u05df \u05ea\u05e7\u05e0\u05d5\u05df \u05d4\u05db\u05e0\u05e1\u05ea \u05d1\u05e0\u05d5\u05e9\u05d0 \u201d\u05d7\u05d5\u05d1\u05ea \u05d4\u05d5\u05d5\u05e2\u05d3\u05d5\u05ea \u05dc\u05e7\u05d9\u05d9\u05dd \u05d9\u05e9\u05d9\u05d1\u05d5\u05ea \u05e4\u05d9\u05e7\u05d5\u05d7 \u05e2\u05dc \u05e2\u05d1\u05d5\u05d3\u05ea \u05d4\u05de\u05de\u05e9\u05dc\u05d4\u201d. 2. \u05d4\u05e7\u05de\u05ea \u05d5\u05e2\u05d3\u05d4 \u05de\u05e6\u05d5\u05de\u05e6\u05de\u05ea-\u05d6\u05de\u05e0\u05d9\u05ea \u05dc\u05d3\u05d9\u05d5\u05df \u05d1\u05d4\u05de\u05dc\u05e6\u05d5\u05ea \u05dc\u05e9\u05d9\u05e0\u05d5\u05d9\u05d9\u05dd \u05d1\u05ea\u05e0\u05d0\u05d9 \u05d7\u05d1\u05e8\u05d9-\u05d4\u05db\u05e0\u05e1\u05ea \u05d5\u05d4\u05d9\u05d5\u05e2\u05e6\u05d9\u05dd \u05d4\u05e4\u05e8\u05dc\u05de\u05e0\u05d8\u05e8\u05d9\u05d9\u05dd. '),
                                      ('session_content', u'1. \u05d4\u05e6\u05e2\u05d4 \u05dc\u05ea\u05d9\u05e7\u05d5\u05df \u05ea\u05e7\u05e0\u05d5\u05df \u05d4\u05db\u05e0\u05e1\u05ea \u05d1\u05e0\u05d5\u05e9\u05d0 "\u05d7\u05d5\u05d1\u05ea \u05d4\u05d5\u05d5\u05e2\u05d3\u05d5\u05ea \u05dc\u05e7\u05d9\u05d9\u05dd \u05d9\u05e9\u05d9\u05d1\u05d5\u05ea \u05e4\u05d9\u05e7\u05d5\u05d7 \u05e2\u05dc \u05e2\u05d1\u05d5\u05d3\u05ea \u05d4\u05de\u05de\u05e9\u05dc\u05d4". 2. \u05d4\u05e7\u05de\u05ea \u05d5\u05e2\u05d3\u05d4 \u05de\u05e6\u05d5\u05de\u05e6\u05de\u05ea-\u05d6\u05de\u05e0\u05d9\u05ea \u05dc\u05d3\u05d9\u05d5\u05df \u05d1\u05d4\u05de\u05dc\u05e6\u05d5\u05ea \u05dc\u05e9\u05d9\u05e0\u05d5\u05d9\u05d9\u05dd \u05d1\u05ea\u05e0\u05d0\u05d9 \u05d7\u05d1\u05e8\u05d9-\u05d4\u05db\u05e0\u05e1\u05ea \u05d5\u05d4\u05d9\u05d5\u05e2\u05e6\u05d9\u05dd \u05d4\u05e4\u05e8\u05dc\u05de\u05e0\u05d8\u05e8\u05d9\u05d9\u05dd. '),
                                      ('url', u'http://fs.knesset.gov.il//20/Committees/20_ptv_321925.doc'),
                                      ('location ', u'\u05d7\u05d3\u05e8 \u05d5\u05e2\u05d3\u05d4'),
                                      ('place ', u'\u05d7\u05d3\u05e8 \u05d4\u05d5\u05d5\u05e2\u05d3\u05d4, \u05d1\u05d0\u05d2\u05e3 \u05e7\u05d3\u05de\u05d4, \u05e7\u05d5\u05de\u05d4 3, \u05d7\u05d3\u05e8 3720'),
                                      ('meeting_stop ', u'16/02/2016 13:31'), ('agenda_canceled ', 0),
                                      ('agenda_sub ', None), ('agenda_associated ', None),
                                      ('agenda_associated_id ', None), ('agenda_special ', None),
                                      ('agenda_invited1 ', None), ('agenda_invite ', True), ('note ', None),
                                      ('start_datetime ', datetime.datetime(2016, 2, 16, 12, 30)), ('topid_id ', 10048),
                                      ('creation_date ', datetime.datetime(2016, 2, 16, 12, 30)),
                                      ('streaming_url ', u'http://video.knesset.gov.il/knesset'),
                                      ('meeting_start ', u'16/02/2016 12:35'), ('is_paused ', False),
                                      ('date_order ', u'2016-02-16'), ('date ', u'16/02/2016'), ('day ', u'16'),
                                      ('month ', u'\u05e4\u05d1\u05e8\u05d5\u05d0\u05e8'), ('material_id ', None),
                                      ('material_committee_id ', None), ('material_expiration_date ', None),
                                      ('material_hour ', None),
                                      ('old_url ', u'http://fs.knesset.gov.il//20/Committees/20_ptv_321925.doc'),
                                      ('background_page_link ', None),
                                      ('agenda_invited ', None)]))
