import yaml
import unittest
import contextlib
import requests
import os

from knesset_data.protocols.committee import CommitteeMeetingProtocol


def get_protocol_text_cached(CommitteeSessionID):
    filename = 'data/protocols_text_cache/{}/{}/{}.txt'.format(
            str(CommitteeSessionID)[0], str(CommitteeSessionID)[1], str(CommitteeSessionID)
    )
    if os.path.exists(filename):
        with open(filename) as f:
            text = f.read()
    else:
        res = requests.get(
            'https://storage.googleapis.com/knesset-data-pipelines/data/committees/meeting_protocols_text/files/{}/{}/{}.txt'.format(
                str(CommitteeSessionID)[0], str(CommitteeSessionID)[1], str(CommitteeSessionID)
            ))
        assert res.status_code == 200
        text = res.content.decode('utf-8')
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            f.write(text)
    return text


class TestCommitteeMeetingProtocol(CommitteeMeetingProtocol):

    @classmethod
    @contextlib.contextmanager
    def get_from_CommitteeSessionID(cls, CommitteeSessionID):
        with cls._get_from('CommitteeSessionID', CommitteeSessionID) as p:
            p.text = get_protocol_text_cached(CommitteeSessionID)
            yield p


class TestMeetings(unittest.TestCase):

    def test_meetings(self):
        with open('knesset_data/protocols/tests/test_meetings.yaml') as f:
            tests = yaml.load(f)
        for test in tests:
            print("test['CommitteeSessionID'] =", test['CommitteeSessionID'])
            with TestCommitteeMeetingProtocol.get_from_CommitteeSessionID(test['CommitteeSessionID']) as protocol:
                assert set(protocol.attendees['mks']) == set(test['expected']['mks']), \
                    'meeting ID {} -actual mks = {}'.format(test['CommitteeSessionID'], protocol.attendees['mks'])
                assert set(protocol.attendees['manager']) == set(test['expected']['manager']), \
                    'meeting ID {} -actual manager = {}'.format(test['CommitteeSessionID'], protocol.attendees['manager'])
                assert set(protocol.attendees['legal_advisors']) == set(test['expected']['legal_advisors']), \
                    'meeting ID {} -actual legal advisors: {}'.format(test['CommitteeSessionID'], protocol.attendees['legal_advisors'])
                assert protocol.attendees['invitees'] == test['expected']['invitees'], \
                    'meeting ID {} - actual invitees: {}'.format(test['CommitteeSessionID'], protocol.attendees['invitees'])
                assert set(protocol.attendees['financial_advisors']) == set(test['expected']['financial_advisors']), \
                    'meeting ID {} - actual financial advisors: {}'.format(test['CommitteeSessionID'], protocol.attendees['financial_advisors'])
