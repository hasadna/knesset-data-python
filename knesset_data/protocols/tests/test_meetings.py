import yaml
import unittest
import contextlib
import requests
from cached_property import cached_property

from knesset_data.protocols.committee import CommitteeMeetingProtocol


class TestCommitteeMeetingProtocol(CommitteeMeetingProtocol):

    @classmethod
    @contextlib.contextmanager
    def get_from_CommitteeSessionID(cls, CommitteeSessionID):
        with cls._get_from('CommitteeSessionID', CommitteeSessionID) as p:
            res = requests.get('https://storage.googleapis.com/knesset-data-pipelines/data/committees/meeting_protocols_text/files/{}/{}/{}.txt'.format(
                str(CommitteeSessionID)[0], str(CommitteeSessionID)[1], str(CommitteeSessionID)
            ))
            assert res.status_code == 200
            p.text = res.content.decode('utf-8')
            yield p


class TestMeetings(unittest.TestCase):

    def test_meetings(self):
        with open('knesset_data/protocols/tests/test_meetings.yaml') as f:
            tests = yaml.load(f)
        for test in tests:
            with TestCommitteeMeetingProtocol.get_from_CommitteeSessionID(test['CommitteeSessionID']) as protocol:
                assert protocol.attendees['mks'] == test['expected']['mks']
                assert protocol.attendees['manager'] == test['expected']['manager']
                assert protocol.attendees['legal_advisors'] == test['expected']['legal_advisors']
                assert protocol.attendees['invitees'] == test['expected']['invitees']

