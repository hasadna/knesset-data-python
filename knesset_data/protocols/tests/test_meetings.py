import yaml
import unittest
import contextlib
import requests
import os
import csv
import itertools

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


def assert_num_speech_parts(CommitteeSessionID, protocol, expected_num_speech_parts):
    parts = protocol.parts
    num_parts = len(parts)
    assert num_parts == expected_num_speech_parts, \
        "expected number of protocol parts = {}, actual = {}, CommitteeSessionID={}".format(
            expected_num_speech_parts, num_parts, CommitteeSessionID
        )


def assert_parts_texts(CommitteeSessionID, protocol, expected_parts_texts):
    parts = protocol.parts
    for expected_part in expected_parts_texts:
        actual_part = parts[expected_part['index']]
        assert actual_part.header == expected_part['header'], \
            'actual header = "{}" expected = "{}" CommitteeSessionID={}'.format(
                actual_part.header, expected_part['header'], CommitteeSessionID
            )
        assert len(actual_part.body.strip()) == expected_part['body_length'], \
            'actual body len = "{}" expected = "{}" CommitteeSessionID={}'.format(
                len(actual_part.body.strip()), expected_part['body_length'], CommitteeSessionID
            )


def assert_protocol_parts_filename(CommitteeSessionID, protocol, expected_parts_filename):
    filename = 'knesset_data/protocols/tests/'+expected_parts_filename
    if not os.path.exists(filename):
        print('expected parts file ({}) does not exist, creating it from actual parts'.format(expected_parts_filename))
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(itertools.chain(
                [['header', 'body']],
                ([part.header, part.body] for part in protocol.parts)
            ))
        assert False
    else:
        with open(filename) as f:
            reader = csv.reader(f)
            expected_parts = []
            for i, row in enumerate(reader):
                if i == 0:
                    assert row == ['header', 'body']
                else:
                    expected_parts.append({'header': row[0], 'body': row[1]})
        actual_parts = protocol.parts
        assert len(expected_parts) == len(actual_parts)
        for i, actual_part in enumerate(actual_parts):
            assert [expected_parts[i]['header'], expected_parts[i]['body']] == [actual_part.header, actual_part.body]


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
        tests = (
            test for test in tests
            if (
                not os.environ.get('COMMITTEE_SESSION_ID')
                or str(test['CommitteeSessionID']) in os.environ.get('COMMITTEE_SESSION_ID').split(',')
            )
        )
        for test in tests:
            print("test['CommitteeSessionID'] =", test['CommitteeSessionID'])
            with TestCommitteeMeetingProtocol.get_from_CommitteeSessionID(test['CommitteeSessionID']) as protocol:
                if test['expected'].get('protocol_parts_filename') is not None:
                    assert_protocol_parts_filename(test['CommitteeSessionID'], protocol, test['expected']['protocol_parts_filename'])
                if test['expected'].get('mks') is not None:
                    assert set(protocol.attendees['mks']) == set(test['expected']['mks']), \
                        'meeting ID {} -actual mks = {}'.format(test['CommitteeSessionID'], protocol.attendees['mks'])
                if test['expected'].get('manager') is not None:
                    assert set(protocol.attendees['manager']) == set(test['expected']['manager']), \
                        'meeting ID {} -actual manager = {}'.format(test['CommitteeSessionID'], protocol.attendees['manager'])
                if test['expected'].get('legal_advisors') is not None:
                    assert set(protocol.attendees['legal_advisors']) == set(test['expected']['legal_advisors']), \
                        'meeting ID {} -actual legal advisors: {}'.format(test['CommitteeSessionID'], protocol.attendees['legal_advisors'])
                if test['expected'].get('invitees') is not None:
                    assert protocol.attendees['invitees'] == test['expected']['invitees'], \
                        'meeting ID {} - actual invitees: {}'.format(test['CommitteeSessionID'], protocol.attendees['invitees'])
                if test['expected'].get('financial_advisors') is not None:
                    assert set(protocol.attendees['financial_advisors']) == set(test['expected']['financial_advisors']), \
                        'meeting ID {} - actual financial advisors: {}'.format(test['CommitteeSessionID'], protocol.attendees['financial_advisors'])
                if test['expected'].get('num_speech_parts') is not None:
                    assert_num_speech_parts(test['CommitteeSessionID'], protocol, test['expected']['num_speech_parts'])
                if test['expected'].get('parts_texts') is not None:
                    assert_parts_texts(test['CommitteeSessionID'], protocol, test['expected']['parts_texts'])
