import unittest
from datetime import datetime

from knesset_data.dataservice.committees import Committee, CommitteeMeeting
from knesset_data.dataservice.exceptions import KnessetDataServiceRequestException, KnessetDataServiceObjectException
from knesset_data.dataservice.mocks import MockMember, MockCommitteeMeeting
from knesset_data.utils.testutils import data_dependant_test


class CommitteeWithVeryShortTimeoutAndInvalidService(Committee):
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 1
    METHOD_NAME = "Invalid Method Name"


class CommitteeMeetingWithVeryShortTimeoutAndInvalidService(CommitteeMeeting):
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 1
    METHOD_NAME = "FOOBARBAZBAX"


class MockMemberWithBadFeed(MockMember):

    @classmethod
    def _get_soup(cls, url, params=None, proxies=None):
        def find(soup_instance, name, **kwargs):
            return None
        return type("MockSoup", (object,), {"find": find})()


class MockMemberWithEntriesAfterErrors(MockMember):
    SOUP_MEMBER_IDS = [203, 200]


class MockCommitteeMeetingWithParseError(MockCommitteeMeeting):

    @classmethod
    def _parse_element(cls, element):
        if element == 2:
            raise Exception("committee meeting parse error")
        return super(MockCommitteeMeetingWithParseError, cls)._parse_element(element)


class TestDataServiceRequestExceptions(unittest.TestCase):

    def test_member_exception(self):
        # get_page - raises an exception as soon as it's encountered
        exception = None
        try:
            list(MockMember.get_page())
        except Exception as e:
            exception = e
        self.assertEqual(str(exception), "member with exception on init")
        # get - raises an exception as soon as it's encountered
        exception = None
        try:
            MockMember.get(215)
        except Exception as e:
            exception = e
        self.assertEqual(str(exception), "member with exception on get")

    def test_member_skipped_exceptions(self):
        # get_page with skip_exceptions - yields exception objects on error
        self.assertEqual([o.message if isinstance(o, KnessetDataServiceObjectException) else o.id
                          for o in MockMember.get_page(skip_exceptions=True)],
                         [200, 201, 202, 'member with exception on init', 'member with exception on parse'])

    def test_filtered_generator_propagates_skip_exceptions(self):
        results = list(MockMember.get_all_present_members(skip_exceptions=True))
        self.assertEqual([o.message if isinstance(o, KnessetDataServiceObjectException) else o.id
                          for o in results],
                         [200, 201, 202, 'member with exception on init', 'member with exception on parse'])

    def test_all_pages_raises_on_feed_parse_error_by_default(self):
        with self.assertRaises(AttributeError):
            list(MockMemberWithBadFeed.get_all())

    def test_all_pages_yields_feed_parse_error_when_skipping(self):
        results = list(MockMemberWithBadFeed.get_all(skip_exceptions=True))
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], AttributeError)

    def test_all_pages_continues_after_entry_error_when_skipping(self):
        results = list(MockMemberWithEntriesAfterErrors.get_all(skip_exceptions=True))
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], KnessetDataServiceObjectException)
        self.assertEqual(results[1].id, 200)

    def test_function_generator_raises_parse_error_by_default(self):
        with self.assertRaisesRegex(Exception, 'committee meeting parse error'):
            list(MockCommitteeMeetingWithParseError.get(1, datetime(2016, 1, 1)))

    def test_function_generator_yields_parse_error_when_skipping(self):
        results = list(MockCommitteeMeetingWithParseError.get(1, datetime(2016, 1, 1), skip_exceptions=True))
        self.assertEqual(len(results), 3)
        self.assertIsInstance(results[1], Exception)
        self.assertEqual(results[2].id, 3)

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
            str(exception)
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
            str(exception)
        ], [
            'FOOBARBAZBAX',
            'committees',
            'http://online.knesset.gov.il/WsinternetSps/KnessetDataService/CommitteeScheduleData.svc/FOOBARBAZBAX?CommitteeId=%271%27&FromDate=%272016-01-01T00%3A00%3A00%27',
            "('Connection aborted.', error(104, 'Connection reset by peer'))",
        ])
