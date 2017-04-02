from knesset_data.html_scrapers.plenum import PlenumMeeting, PlenumMeetings
import os


class MockPlenumMeetings(PlenumMeetings):

    def __init__(self, full_protocol=True):
        self._full_protocol = full_protocol

    def _get_plenum_meeting(self, *args, **kwargs):
        return MockPlenumMeeting(*args, **kwargs)

    def _read_index_page(self, url):
        if url == self.FULL_URL:
            return open(os.path.join(os.path.dirname(__file__), "plenum_display_full.asp")).read()
        elif url == self.PLENUM_URL:
            return open(os.path.join(os.path.dirname(__file__), "plenum_queue.aspx")).read()
        else:
            raise Exception("unknown url {}".format(url))

    def _read_file(self, url):
        if url == "http://www.knesset.gov.il/plenum/data/20_ptm_307658.doc":
            if self._full_protocol:
                return open(os.path.join(os.path.dirname(__file__), "..", "protocols", "tests", "20_ptm_381742.doc")).read()
            else:
                return "PROTOCOL CONTENT"
        elif url == "http://www.knesset.gov.il/plenum/data/20_ptm_307568.doc":
            raise Exception("fake exception")
        else:
            return None


class MockPlenumMeeting(PlenumMeeting):
    pass
