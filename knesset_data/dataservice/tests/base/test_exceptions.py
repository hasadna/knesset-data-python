import unittest
from datetime import datetime

from knesset_data.dataservice.committees import Committee, CommitteeMeeting
from knesset_data.dataservice.exceptions import KnessetDataServiceRequestException, KnessetDataServiceObjectException
from knesset_data.dataservice.mocks import MockMember
from knesset_data.utils.testutils import data_dependant_test


class CommitteeWithVeryShortTimeoutAndInvalidService(Committee):
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 1
    METHOD_NAME = "Invalid Method Name"


class CommitteeMeetingWithVeryShortTimeoutAndInvalidService(CommitteeMeeting):
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 1
    METHOD_NAME = "FOOBARBAZBAX"


class TestDataServiceRequestExceptions(unittest.TestCase):

    def test_member_exception(self):
        # get_page - raises an exception as soon as it's encountered
        exception = None
        try:
            list(MockMember.get_page())
        except Exception, e:
            exception = e
        self.assertEqual(exception.message, "member with exception on init")
        # get - raises an exception as soon as it's encountered
        exception = None
        try:
            MockMember.get(215)
        except Exception, e:
            exception = e
        self.assertEqual(exception.message, "member with exception on get")

    def test_member_skipped_exceptions(self):
        # get_page with skip_exceptions - yields exception objects on error
        self.assertEqual([o.message if isinstance(o, KnessetDataServiceObjectException) else o.id
                          for o in MockMember.get_page(skip_exceptions=True)],
                         [200, 201, 202, 'member with exception on init', 'member with exception on parse'])

    @data_dependant_test()
    def test_committee(self):
        exception = None
        try:
            CommitteeWithVeryShortTimeoutAndInvalidService.get(1)
        except KnessetDataServiceRequestException as e:
            exception = e
        self.assertIsInstance(exception, KnessetDataServiceRequestException)
        self.assertListEqual([
            exception.knesset_data_method_name,
            exception.knesset_data_service_name,
            exception.url,
            str(exception.message)
        ], [
            'Invalid Method Name',
            'committees',
            'http://online.knesset.gov.il/WsinternetSps/KnessetDataService/CommitteeScheduleData.svc/Invalid%20Method%20Name(1)',
            "('Connection aborted.', error(104, 'Connection reset by peer'))",
        ])

    @data_dependant_test()
    def test_committee_meeting(self):
        exception = None
        try:
            CommitteeMeetingWithVeryShortTimeoutAndInvalidService.get(1, datetime(2016, 1, 1))
        except KnessetDataServiceRequestException as e:
            exception = e
        self.assertIsInstance(exception, KnessetDataServiceRequestException)
        self.assertListEqual([
            exception.knesset_data_method_name,
            exception.knesset_data_service_name,
            exception.url,
            str(exception.message)
        ], [
            'FOOBARBAZBAX',
            'committees',
            'http://online.knesset.gov.il/WsinternetSps/KnessetDataService/CommitteeScheduleData.svc/FOOBARBAZBAX?CommitteeId=%271%27&FromDate=%272016-01-01T00%3A00%3A00%27',
            "('Connection aborted.', error(104, 'Connection reset by peer'))",
        ])
