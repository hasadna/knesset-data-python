import unittest
from datetime import datetime
from knesset_data.dataservice.committees import CommitteeMeeting
from ...mocks import MockCommitteeMeeting
import json
from collections import OrderedDict


class TestCommitteeMeetings(unittest.TestCase):

    def _get_meetings(self, committee_id, datetime_from, datetime_to):
        # the knesset dataservice allows to get meetings only using a function with these parameters
        # see https://github.com/hasadna/knesset-data/issues/25
        return MockCommitteeMeeting.get(committee_id, datetime_from, datetime_to)

    def test_committee_meeting(self):
        meetings = list(self._get_meetings(1, datetime(2016, 1, 1), datetime(2016, 1, 5)))
        self.assertTrue(isinstance(meetings[0].datetime, datetime))
        # for more details about the available data see knesset_data/dataservice/committees.py
        # TODO: add assertion here for each relevant field

    def test_protocol(self):
        meetings = list(self._get_meetings(1, datetime(2016, 2, 16), datetime(2016, 2, 17)))
        # because parsing the protocol requires heavy IO and processing - we provide it as a generator
        # also, we need to ensure temp files are deleted
        with meetings[0].protocol as protocol:
            # see knesset_data/protocols/tests/test_committee.py for example of getting more data from the protocol
            self.assertEqual(protocol.text, "protocol text")

    def test_table_schema(self):
        meeting = next(self._get_meetings(1, datetime(2016, 2, 16), datetime(2016, 2, 17)))
        self.assertEqual(meeting.all_schema_field_values(), OrderedDict([('id', 1),
                                                                         ('committee_id', None),
                                                                         ('datetime', datetime(2013, 5, 1, 16, 33)),
                                                                         ('title', None),
                                                                         ('session_content', None),
                                                                         ('url', 'mock url 1'),
                                                                         ('location ', None),
                                                                         ('place ', None),
                                                                         ('meeting_stop ', None),
                                                                         ('agenda_canceled ', None),
                                                                         ('agenda_sub ', None),
                                                                         ('agenda_associated ', None),
                                                                         ('agenda_associated_id ', None),
                                                                         ('agenda_special ', None),
                                                                         ('agenda_invited1 ', None),
                                                                         ('agenda_invite ', None),
                                                                         ('note ', None),
                                                                         ('start_datetime ', datetime(2013, 5, 1, 16, 44)),
                                                                         ('topid_id ', None),
                                                                         ('creation_date ', None),
                                                                         ('streaming_url ', None),
                                                                         ('meeting_start ', None),
                                                                         ('is_paused ', None),
                                                                         ('date_order ', None),
                                                                         ('date ', None),
                                                                         ('day ', None),
                                                                         ('month ', None),
                                                                         ('material_id ', None),
                                                                         ('material_committee_id ', None),
                                                                         ('material_expiration_date ', None),
                                                                         ('material_hour ', None),
                                                                         ('old_url ', None),
                                                                         ('background_page_link ', None),
                                                                         ('agenda_invited ', None)]))
