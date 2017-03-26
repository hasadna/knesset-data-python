from unittest import TestCase
from ..plenum import PlenumMeetings, PlenumMeeting
import os
from knesset_data.exceptions import KnessetDataObjectException
from knesset_data.protocols.exceptions import AntiwordException
from knesset_data.html_scrapers.mocks import MockPlenumMeetings


class PlenumTestCase(TestCase):

    def _meeting_str(self, meeting):
        if isinstance(meeting, Exception):
            return meeting.message
        else:
            return "{}/{}/{}".format(meeting.day, meeting.month, meeting.year)

    def _meeting_dict(self, meeting):
        if isinstance(meeting, Exception):
            return {"exception": meeting.message}
        else:
            with meeting.protocol as p:
                protocol = p.file_contents
            return {
                "day": meeting.day,
                "month": meeting.month,
                "year": meeting.year,
                "url": meeting.url,
                "protocol": protocol
            }

    def _download(self, **kwargs):
        return MockPlenumMeetings().download(**kwargs)

    # this is the most common use-case
    # fetches all results, sorts descending, and skips exceptions (which will be returned at the end of all results as exception objects)
    def test_fetch_all_sorted(self):
        self.assertEqual([self._meeting_str(o)
                          for o in self._download(skip_exceptions=True, sorted=True)],
                         ['21/3/2017', '20/3/2017', '15/3/2017', '14/3/2017', '8/3/2017', '7/3/2017', '6/3/2017',
                          '1/3/2017', '28/2/2017', '27/2/2017', '22/2/2017', '21/2/2017', '20/2/2017', '15/2/2017',
                          '14/2/2017', '13/2/2017', '8/2/2017', '7/2/2017', '6/2/2017', '1/2/2017', '20/5/2015',
                          '19/5/2015', '13/5/2015', '12/5/2015', '11/5/2015', '6/5/2015', '5/5/2015', '4/5/2015',
                          '20/4/2015', '31/3/2015', '16/2/2015', '21/1/2015', '5/1/2015', '29/12/2014', '10/12/2014',
                          '9/12/2014', '8/12/2014', '3/12/2014', '2/12/2014', '1/12/2014', '26/11/2014', 'fake exception'])

    def test_plenum_protocol_object(self):
        plenum_meeting = self._download().next()
        with plenum_meeting.protocol as protocol:
            self.assertRaises(AntiwordException, lambda: protocol.header_text)

    def test_as_generator(self):
        res = self._download(skip_exceptions=True)
        self.assertEqual(self._meeting_dict(res.next()), {"day": 20, "month": 5, "year": 2015, "protocol": "PROTOCOL CONTENT",
                                           "url": "http://www.knesset.gov.il/plenum/data/20_ptm_307658.doc"})
        self.assertEqual(self._meeting_dict(res.next()), {"day": 19, "month": 5, "year": 2015, "protocol": None,
                                           "url": "http://www.knesset.gov.il/plenum/data/20_ptm_307604.doc"})
        # yields exceptions (in case skip_exceptions is True)
        self.assertIsInstance(res.next(), KnessetDataObjectException)
        # each object is a PlenumMeeting
        self.assertIsInstance(res.next(), PlenumMeeting)
        # supports sorting (not by default because it prevents streaming)
        self.assertEqual([self._meeting_str(o) for o in PlenumMeetings.sort(res)],
                         ['21/3/2017', '20/3/2017', '15/3/2017', '14/3/2017', '8/3/2017', '7/3/2017', '6/3/2017',
                          '1/3/2017', '28/2/2017', '27/2/2017', '22/2/2017', '21/2/2017', '20/2/2017', '15/2/2017',
                          '14/2/2017', '13/2/2017', '8/2/2017', '7/2/2017', '6/2/2017', '1/2/2017', '12/5/2015',
                          '11/5/2015', '6/5/2015', '5/5/2015', '4/5/2015', '20/4/2015', '31/3/2015', '16/2/2015',
                          '21/1/2015', '5/1/2015', '29/12/2014', '10/12/2014', '9/12/2014', '8/12/2014', '3/12/2014',
                          '2/12/2014', '1/12/2014', '26/11/2014'])
