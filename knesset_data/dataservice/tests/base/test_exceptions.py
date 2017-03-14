import unittest
from datetime import datetime
from knesset_data.dataservice.committees import Committee, CommitteeMeeting
from knesset_data.dataservice.members import Member
from knesset_data.dataservice.exceptions import KnessetDataServiceRequestException, KnessetDataServiceObjectException
from knesset_data.utils.testutils import data_dependant_test


class CommitteeWithVeryShortTimeoutAndInvalidService(Committee):
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 1
    METHOD_NAME = "Invalid Method Name"


class CommitteeMeetingWithVeryShortTimeoutAndInvalidService(CommitteeMeeting):
    DEFAULT_REQUEST_TIMEOUT_SECONDS = 1
    METHOD_NAME = "FOOBARBAZBAX"


class MockMember(Member):
    SOUP_MEMBER_IDS = range(200, 205)
    EXCEPTION_ON_INIT_MEMBER_ID = 203
    EXCEPTION_ON_PARSE_MEMBER_ID = 204
    EXCEPTION_ON_GET_MEMBER_ID = 215

    def __init__(self, entry):
        if entry["data"]["mk_individual_id"] == self.EXCEPTION_ON_INIT_MEMBER_ID:
            raise Exception("member with exception on init")
        super(MockMember, self).__init__(entry)

    @classmethod
    def _parse_entry(cls, entry):
        parsed_entry = super(MockMember, cls)._parse_entry(entry)
        if parsed_entry["data"]["mk_individual_id"] == cls.EXCEPTION_ON_PARSE_MEMBER_ID:
            raise Exception("member with exception on parse")
        return parsed_entry

    @classmethod
    def _parse_entry_id(cls, entry):
        return str(entry)

    @classmethod
    def _parse_entry_links(cls, entry):
        return []

    @classmethod
    def _parse_entry_data(cls, entry):
        data = {field._knesset_field_name: "" for field in cls.get_fields().values() if hasattr(field, "_knesset_field_name")}
        data["mk_individual_id"] = entry
        return data

    @classmethod
    def _get_soup(cls, url, params=None, proxies=None):
        if "({})".format(cls.EXCEPTION_ON_GET_MEMBER_ID) in url:
            raise Exception("member with exception on get")
        else:
            def find_all(feed_instance, name, attrs=None):
                if name == "link":
                    return []
                else:
                    return [i for i in cls.SOUP_MEMBER_IDS]
            return type("MockSoup", (object,),
                        {"feed": type("MockFeed", (object,),
                                      {"find_all": find_all})()})


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
