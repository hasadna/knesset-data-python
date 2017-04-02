from unittest import TestCase
from ..plenum import PlenumMeetings, PlenumMeeting
import os
from knesset_data.exceptions import KnessetDataObjectException
from knesset_data.protocols.exceptions import AntiwordException
from knesset_data.html_scrapers.mocks import MockPlenumMeetings
from datetime import date


class PlenumTestCase(TestCase):

    def _meeting_str(self, meeting):
        if isinstance(meeting, Exception):
            return meeting.message
        else:
            return meeting.date.strftime("%d/%m/%Y")

    def _meeting_dict(self, meeting):
        if isinstance(meeting, Exception):
            return {"exception": meeting.message}
        else:
            with meeting.protocol as p:
                try:
                    protocol = p.file_contents[:15]
                except Exception, e:
                    protocol = "EXCEPTION"
            return {
                "date": meeting.date,
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
                         ['21/03/2017', '20/03/2017', '15/03/2017', '14/03/2017', '08/03/2017', '07/03/2017', '06/03/2017',
                          '01/03/2017', '28/02/2017', '27/02/2017', '22/02/2017', '21/02/2017', '20/02/2017', '15/02/2017',
                          '14/02/2017', '13/02/2017', '08/02/2017', '07/02/2017', '06/02/2017', '01/02/2017', '20/05/2015',
                          '19/05/2015', '13/05/2015', '12/05/2015', '11/05/2015', '06/05/2015', '05/05/2015', '04/05/2015',
                          '20/04/2015', '31/03/2015', '16/02/2015', '21/01/2015', '05/01/2015', '29/12/2014', '10/12/2014',
                          '09/12/2014', '08/12/2014', '03/12/2014', '02/12/2014', '01/12/2014', '26/11/2014', 'fake exception'])

    def test_plenum_protocol_object(self):
        with self._download().next().protocol as protocol:
            self.assertEqual(protocol.knesset_num, 20)

    def test_as_generator(self):
        res = self._download(skip_exceptions=True)

        self.assertEqual(self._meeting_dict(res.next()), {"date": date(2015, 5, 20), "protocol": '\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1\x00\x00\x00\x00\x00\x00\x00',
                                           "url": "http://www.knesset.gov.il/plenum/data/20_ptm_307658.doc"})
        self.assertEqual(self._meeting_dict(res.next()), {"date": date(2015, 5, 19), "protocol": "EXCEPTION",
                                           "url": "http://www.knesset.gov.il/plenum/data/20_ptm_307604.doc"})
        # yields exceptions (in case skip_exceptions is True)
        self.assertIsInstance(res.next(), KnessetDataObjectException)
        # each object is a PlenumMeeting
        self.assertIsInstance(res.next(), PlenumMeeting)
        # supports sorting (not by default because it prevents streaming)
        self.assertEqual([self._meeting_str(o) for o in PlenumMeetings.sort(res)],
                         ['21/03/2017', '20/03/2017', '15/03/2017', '14/03/2017', '08/03/2017', '07/03/2017', '06/03/2017',
                          '01/03/2017', '28/02/2017', '27/02/2017', '22/02/2017', '21/02/2017', '20/02/2017', '15/02/2017',
                          '14/02/2017', '13/02/2017', '08/02/2017', '07/02/2017', '06/02/2017', '01/02/2017', '12/05/2015',
                          '11/05/2015', '06/05/2015', '05/05/2015', '04/05/2015', '20/04/2015', '31/03/2015', '16/02/2015',
                          '21/01/2015', '05/01/2015', '29/12/2014', '10/12/2014', '09/12/2014', '08/12/2014', '03/12/2014',
                          '02/12/2014', '01/12/2014', '26/11/2014'])
