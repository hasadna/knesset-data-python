from knesset_data.html_scrapers.plenum import PlenumMeeting, PlenumMeetings
import os
import six

if six.PY2:
    def myopen(a, b, **c):
        return open(a, b)
elif six.PY3:
    def myopen(a, b, **c):
        return open(a, b, **c)
else:
    raise RuntimeError('not supported version of py in six module')


class MockPlenumMeetings(PlenumMeetings):

    def __init__(self, full_protocol=True):
        self._full_protocol = full_protocol

    def _get_plenum_meeting(self, *args, **kwargs):
        return MockPlenumMeeting(*args, **kwargs)

    def _read_index_page(self, url):
        if url == self.FULL_URL:
            return myopen(os.path.join(os.path.dirname(__file__), "plenum_display_full.asp"), 'r', encoding='iso_8859_8').read()
        elif url == self.PLENUM_URL:
            return myopen(os.path.join(os.path.dirname(__file__), "plenum_queue.aspx"), 'r', encoding='iso_8859_8').read()
        else:
            raise Exception("unknown url {}".format(url))

    def _read_file(self, url):
        if url == "http://www.knesset.gov.il/plenum/data/20_ptm_307658.doc":
            if self._full_protocol:
                return myopen(os.path.join(os.path.dirname(__file__), "..", "protocols", "tests", "20_ptm_381742.doc"), 'rb').read()
            else:
                return "PROTOCOL CONTENT"
        elif url == "http://www.knesset.gov.il/plenum/data/20_ptm_307568.doc":
            raise Exception("fake exception")
        else:
            return None


class MockPlenumMeeting(PlenumMeeting):
    pass
